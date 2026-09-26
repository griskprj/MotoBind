<template>
  <div class="post-card">
    <div class="post-header">
      <div class="post-author-info" @click="goToProfile">
        <img :src="getAvatarUrl(post.author_avatar)" alt="Avatar" class="avatar">
        <div class="post-author">
          <span class="username">{{ post.author }}</span>
          <span class="date">{{ formatDate(post.created_at) }}</span>
        </div>
      </div>
      <div class="post-actions" v-if="isAuthor">
        <button class="btn-icon" @click="openEditModal">
          <i class="fa fa-edit"></i>
        </button>
        <button class="btn-icon" @click="confirmDelete">
          <i class="fa fa-trash"></i>
        </button>
      </div>
    </div>

    <div class="post-content">
      <p>{{ post.content }}</p>
      <img v-if="post.image" :src="getManualImageUrl(post.image)" alt="Post image" class="post-image">
    </div>

    <div class="post-footer">
      <div class="footer-actions">
        <button class="like-btn" @click="toggleLike" :class="{ liked: post.is_liked }">
          <i class="fa fa-heart"></i>
          <span>{{ post.likes_count || 0 }}</span>
        </button>

        <button class="comment-btn" @click="toggleComments">
          <i class="fa fa-comment"></i>
          <span>{{ post.comments_count || 0 }}</span>
        </button>

        <button
          v-if="post.author_id !== currentUserId"
          class="flag-btn"
          @click="showReportModal = true"
          title="Пожаловаться"
        >
          <i class="fa fa-flag"></i>
        </button>
      </div>
      <button class="outline-btn" @click="openPost">
        <i class="fa fa-arrow-right"></i>
        <span>Подробнее</span>
      </button>
    </div>

    <div v-if="showComments" class="comments-section">
      <div class="comment-input">
        <input
          v-model="commentText"
          placeholder="Написать комментарий..."
          @keyup.enter="submitComment"
        >
        <button style="min-width: 45px;" @click="submitComment" :disabled="!commentText.trim()">
          <i class="fa fa-angle-right"></i>
        </button>
      </div>

      <div v-if="localComments && localComments.length > 0" class="comments-list">
        <div v-for="comment in localComments" :key="comment.id" class="comment">
          <img :src="getAvatarUrl(comment.author_avatar)" alt="Avatar" class="avatar">
          <div class="comment-body">
            <span class="comment-author">{{ comment.author }}</span>
            <span class="comment-text">{{ comment.content }}</span>
            <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
          </div>
          <button
            v-if="comment.user_id === currentUserId"
            class="delete-comment"
            @click="deleteComment(comment.id)"
          >
            <i class="fa fa-times"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Модалка редактирования -->
    <div v-if="showEditModal" class="edit-modal-overlay" @click.self="closeEditModal">
      <div class="edit-modal">
        <div class="edit-modal-header">
          <h3>Редактировать пост</h3>
          <button class="close-btn" @click="closeEditModal">
            <i class="fa fa-times"></i>
          </button>
        </div>

        <div class="edit-modal-body">
          <textarea
            v-model="editContent"
            placeholder="Что нового в мире мотоциклов?"
            rows="4"
            class="edit-textarea"
          ></textarea>

          <div v-if="editImagePreview" class="edit-image-preview">
            <img :src="editImagePreview" alt="Preview">
            <button class="remove-edit-image" @click="removeEditImage">
              <i class="fa fa-times"></i>
            </button>
          </div>

          <div class="edit-actions">
            <label class="image-upload-btn">
              <i class="fa fa-image"></i>
              <span>Изменить фото</span>
              <input type="file" accept="image/*" @change="handleEditImage" hidden>
            </label>
          </div>
        </div>

        <div class="edit-modal-footer">
          <button class="btn btn-secondary" @click="closeEditModal">Отмена</button>
          <button class="btn btn-primary" @click="saveEdit" :disabled="isSaving">
            <i v-if="isSaving" class="fa fa-spinner fa-spin"></i>
            {{ isSaving ? 'Сохранение...' : 'Сохранить' }}
          </button>
        </div>
      </div>
    </div>
  </div>

  <ReportModal
    :isOpen="showReportModal"
    :post="post"
    @close="showReportModal = false"
    @reported="onReported"
  />
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useSocialStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import { getAvatarUrl as resolveAvatarUrl, getManualImageUrl } from '@/utils/mediaUrl'
import socialApi from '@/api/social'

import ReportModal from '../modals/social/ReportModal.vue'

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
  currentUserId: {
    type: [Number, null],
    default: null,
  },
})

const emit = defineEmits(['post-created'])

const router = useRouter()
const toast = useToast()
const socialStore = useSocialStore()

// ===== Local UI state =====
const showComments = ref(false)
const commentText = ref('')
const localComments = ref(null)

const showEditModal = ref(false)
const editContent = ref('')
const editImageFile = ref(null)
const editImagePreview = ref(null)
const editDeleteExistingImage = ref(false)
const isSaving = ref(false)

const showReportModal = ref(false)

// ===== Computed =====
const isAuthor = computed(() => props.post.author_id === props.currentUserId)

// ===== Helpers =====
function getAvatarUrl(path) {
  return resolveAvatarUrl(path)
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function goToProfile() {
  router.push(`/profile/${props.post.author_id}`)
}

function openPost() {
  router.push(`/social/post/${props.post.id}`)
}

function onReported() {
  showReportModal.value = false
}

// ===== Likes =====
async function toggleLike() {
  try {
    await socialStore.toggleLike(props.post.id)
  } catch (err) {
    console.error('Failed to toggle like:', err)
    toast.error('Не удалось поставить лайк')
  }
}

// ===== Comments =====
function toggleComments() {
  showComments.value = !showComments.value
  if (showComments.value && localComments.value === null) {
    loadComments()
  }
}

async function loadComments() {
  try {
    const { data } = await socialApi.getPost(props.post.id)
    localComments.value = data.comments || []
    props.post.comments_count = data.comments_count ?? props.post.comments_count
  } catch (err) {
    console.error('Failed to load comments:', err)
    localComments.value = []
  }
}

async function submitComment() {
  if (!commentText.value.trim()) return
  try {
    const { data } = await socialApi.addComment(props.post.id, commentText.value)
    if (!localComments.value) localComments.value = []
    localComments.value.push(data)
    props.post.comments_count = (props.post.comments_count || 0) + 1
    commentText.value = ''
  } catch (err) {
    console.error('Failed to add comment:', err)
    toast.error('Не удалось добавить комментарий')
  }
}

async function deleteComment(commentId) {
  if (!confirm('Удалить комментарий?')) return
  try {
    await socialApi.deleteComment(commentId)
    localComments.value = (localComments.value || []).filter((c) => c.id !== commentId)
    props.post.comments_count = Math.max(0, (props.post.comments_count || 0) - 1)
  } catch (err) {
    console.error('Failed to delete comment:', err)
    toast.error('Не удалось удалить комментарий')
  }
}

// ===== Edit =====
function openEditModal() {
  editContent.value = props.post.content
  editImagePreview.value = props.post.image ? getManualImageUrl(props.post.image) : null
  editImageFile.value = null
  editDeleteExistingImage.value = false
  showEditModal.value = true
}

function closeEditModal() {
  showEditModal.value = false
  editContent.value = ''
  editImageFile.value = null
  editDeleteExistingImage.value = false
  editImagePreview.value = null
}

function handleEditImage(event) {
  const file = event.target.files[0]
  if (!file) return

  if (file.size > 5 * 1024 * 1024) {
    toast.error('Размер файла не должен превышать 5MB')
    return
  }
  if (!file.type.startsWith('image/')) {
    toast.error('Пожалуйста, загрузите изображение')
    return
  }

  editImageFile.value = file
  editImagePreview.value = URL.createObjectURL(file)
  editDeleteExistingImage.value = false

  editImageFile.value = file
  const reader = new FileReader()
  reader.onload = (e) => {
    editImagePreview.value = e.target.result
  }
  reader.readAsDataURL(file)
}

function removeEditImage() {
  if (props.post.image) {
    editDeleteExistingImage.value = true
  }
  editImageFile.value = null
  editImagePreview.value = null
}

async function saveEdit() {
  if (!editContent.value.trim()) {
    toast.error('Содержимое поста не может быть пустым')
    return
  }

  isSaving.value = true
  try {
    const formData = new FormData()
    formData.append('content', editContent.value.trim())
    if (editImageFile.value) {
      formData.append('image', editImageFile.value)
    }
    if (editDeleteExistingImage.value) {
      formData.append('delete_image', 'true')
    }

    await socialStore.updatePost(props.post.id, formData)
    closeEditModal()
    toast.success('Пост обновлён')
  } catch (err) {
    console.error('Failed to update post:', err)
    toast.error('Не удалось обновить пост')
  } finally {
    isSaving.value = false
  }
}

// ===== Delete =====
function confirmDelete() {
  if (!confirm('Вы уверены, что хотите удалить этот пост?')) return
  deletePost()
}

async function deletePost() {
  try {
    await socialStore.removePost(props.post.id)
    toast.success('Пост удалён')
  } catch (err) {
    console.error('Failed to delete post:', err)
    toast.error('Не удалось удалить пост')
  }
}
</script>

<style scoped>
.post-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
}

.post-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
    padding: 15px 10px;
    overflow-y: hidden;
}

.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
}

.post-author {
    flex: 1;
}

.post-author-info {
    display: flex;
    align-items: center;
    gap: 12px;
    flex: 1;
    cursor: pointer;
    padding: 4px 8px;
    margin: -4px -8px;
    border-radius: 8px;
    transition: background 0.2s;
}

.post-author-info:hover {
    background: var(--bg-secondary);
}

.username {
    font-weight: 600;
    color: var(--text-primary);
    display: block;
}

.date {
    font-size: 12px;
    color: var(--text-muted);
}

.post-actions {
    display: flex;
    gap: 8px;
}

.btn-icon {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 4px 8px;
    transition: color 0.2s;
}

.btn-icon:hover {
    color: var(--accent-text);
}

.post-content p {
    color: var(--text-primary);
    margin-bottom: 12px;
    line-height: 1.6;
    white-space: pre-wrap;
}

.post-image {
    width: 100%;
    max-height: 400px;
    object-fit: cover;
    border-radius: 12px;
}

.post-footer {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-top: 16px;
    padding-top: 12px;
    border-top: 1px solid var(--border-light);
}

.footer-actions {
    display: flex;
}

.footer-actions button {
    transition: all 0.3s;
}

.like-btn, .comment-btn {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: color 0.2s;
}

.like-btn:hover {
    color: #ef4444;
}

.like-btn.liked {
    color: #ef4444;
}

.like-btn.liked i {
    font-weight: 900;
}

.comment-btn:hover {
    color: var(--accent-text);
}

.comments-section {
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid var(--border-light);
}

.comment-input {
    display: flex;
    gap: 8px;
}

.comment-input input {
    flex: 1;
    padding: 8px 12px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: 20px;
    color: var(--text-primary);
    font-size: 14px;
}

.comment-input input:focus {
    outline: none;
    border-color: var(--accent);
}

.comment-input button {
    background: var(--accent);
    border: none;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    color: white;
    cursor: pointer;
    transition: background 0.2s;
}

.comment-input button:hover {
    background: var(--accent-hover);
}

.comment-input button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.comments-list {
    margin-top: 12px;
}

.comment {
    display: flex;
    gap: 10px;
    padding: 8px 0;
    align-items: flex-start;
}

.avatar-small {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    object-fit: cover;
}

.comment-body {
    flex: 1;
}

.comment-author {
    font-weight: 600;
    font-size: 13px;
    color: var(--text-primary);
    margin-right: 8px;
}

.comment-text {
    color: var(--text-primary);
    font-size: 14px;
}

.comment-date {
    display: block;
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 2px;
}

.delete-comment {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 4px;
}

.delete-comment:hover {
    color: var(--danger);
}

/* ===== МОДАЛКА РЕДАКТИРОВАНИЯ ===== */
.edit-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(6px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2000;
    animation: fadeIn 0.2s ease;
}

.edit-modal {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 24px;
    max-width: 600px;
    width: 92%;
    max-height: 90vh;
    overflow-y: auto;
    animation: slideUp 0.3s ease;
}

.edit-modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.edit-modal-header h3 {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
}

.close-btn {
    background: none;
    border: none;
    color: var(--text-muted);
    font-size: 20px;
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 6px;
    transition: all 0.2s;
}

.close-btn:hover {
    background: var(--bg-secondary);
    color: var(--text-primary);
}

.edit-modal-body {
    margin-bottom: 16px;
}

.edit-textarea {
    width: 100%;
    padding: 12px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: 12px;
    color: var(--text-primary);
    font-size: 14px;
    resize: vertical;
    font-family: inherit;
    margin-bottom: 12px;
}

.edit-textarea:focus {
    outline: none;
    border-color: var(--accent);
}

.edit-image-preview {
    position: relative;
    margin: 12px 0;
    border-radius: 12px;
    overflow: hidden;
}

.edit-image-preview img {
    width: 100%;
    max-height: 300px;
    object-fit: cover;
}

.remove-edit-image {
    position: absolute;
    top: 8px;
    right: 8px;
    background: rgba(0, 0, 0, 0.7);
    color: white;
    border: none;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    cursor: pointer;
    transition: background 0.2s;
}

.remove-edit-image:hover {
    background: rgba(239, 68, 68, 0.9);
}

.edit-actions {
    display: flex;
    gap: 12px;
}

.flag-btn {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 15px;
    transition: color 0.2s;
}
.flag-btn:hover { color: var(--danger); }

.image-upload-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s;
}

.image-upload-btn:hover {
    border-color: var(--accent);
    color: var(--accent-text);
}

.edit-modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    padding-top: 16px;
    border-top: 1px solid var(--border-light);
}

.btn {
    padding: 8px 20px;
    border-radius: 8px;
    font-weight: 500;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.btn-secondary {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}

.btn-secondary:hover {
    background: var(--border-color);
}

.btn-primary {
    background: var(--accent);
    color: white;
}

.btn-primary:hover:not(:disabled) {
    background: var(--accent-hover);
    transform: translateY(-2px);
}

/* ===== АНИМАЦИИ ===== */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px) scale(0.98);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

/* ===== АДАПТИВНОСТЬ ===== */
@media (max-width: 768px) {
    .edit-modal {
        padding: 20px;
        width: 95%;
        max-height: 95vh;
    }

    .edit-modal-footer {
        flex-direction: column;
    }

    .edit-modal-footer .btn {
        width: 100%;
        justify-content: center;
    }
}
</style>
