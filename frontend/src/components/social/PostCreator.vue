<template>
  <div class="post-creator">
    <div class="creator-header">
      <img :src="userAvatar" alt="Avatar" class="avatar">
      <span class="username">{{ userName }}</span>
    </div>

    <div class="creator-body">
      <textarea
        v-model="content"
        placeholder="Что нового в мире мотоциклов? 🏍️"
        rows="3"
        class="content-input"
      ></textarea>

      <div v-if="imagePreview" class="image-preview">
        <img :src="imagePreview" alt="Preview">
        <button class="remove-image" @click="removeImage">
          <i class="fa fa-times"></i>
        </button>
      </div>
    </div>

    <div class="creator-footer">
      <div class="actions">
        <label class="image-upload-btn">
          <i class="fa fa-image"></i>
          <input type="file" accept="image/*" @change="handleImageUpload" hidden>
        </label>
      </div>

      <button
        class="btn btn-primary"
        @click="submitPost"
        :disabled="!content.trim() || isSubmitting"
      >
        <i v-if="isSubmitting" class="fa fa-spinner fa-spin"></i>
        {{ isSubmitting ? 'Публикация...' : 'Опубликовать' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useSocialStore, useAuthStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import { getAvatarUrl as resolveAvatarUrl } from '@/utils/mediaUrl'

const emit = defineEmits(['post-created'])

const toast = useToast()
const socialStore = useSocialStore()
const authStore = useAuthStore()

const content = ref('')
const imageFile = ref(null)
const imagePreview = ref(null)
const isSubmitting = ref(false)

const userName = computed(() => authStore.user?.username || 'Пользователь')
const userAvatar = computed(() => resolveAvatarUrl(authStore.user?.avatar))

function handleImageUpload(event) {
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

  imageFile.value = file
  const reader = new FileReader()
  reader.onload = (e) => {
    imagePreview.value = e.target.result
  }
  reader.readAsDataURL(file)
}

function removeImage() {
  imageFile.value = null
  imagePreview.value = null
}

async function submitPost() {
  if (!content.value.trim() || isSubmitting.value) return

  isSubmitting.value = true
  try {
    const formData = new FormData()
    formData.append('content', content.value.trim())
    if (imageFile.value) {
      formData.append('image', imageFile.value)
    }

    await socialStore.createPost(formData)

    content.value = ''
    removeImage()
    emit('post-created')
    toast.success('Пост опубликован')
  } catch (err) {
    console.error('Failed to create post:', err)
    toast.error('Не удалось создать пост')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.post-creator {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
}

.creator-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
}

.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
}

.username {
    font-weight: 600;
    color: var(--text-primary);
}

.creator-body {
    margin-bottom: 16px;
}

.content-input {
    width: 100%;
    padding: 12px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: 12px;
    color: var(--text-primary);
    font-size: 14px;
    resize: vertical;
    font-family: inherit;
}

.content-input:focus {
    outline: none;
    border-color: var(--accent);
}

.image-preview {
    position: relative;
    margin-top: 12px;
    border-radius: 12px;
    overflow: hidden;
}

.image-preview img {
    width: 100%;
    max-height: 300px;
    object-fit: cover;
}

.remove-image {
    position: absolute;
    top: 8px;
    right: 8px;
    background: rgba(0,0,0,0.7);
    color: white;
    border: none;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    cursor: pointer;
}

.creator-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.actions {
    display: flex;
    gap: 12px;
}

.image-upload-btn {
    cursor: pointer;
    color: var(--text-muted);
    font-size: 20px;
    transition: color 0.2s;
}

.image-upload-btn:hover {
    color: var(--accent-text);
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}
</style>
