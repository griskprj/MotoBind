<template>
    <div class="post-card">
        <div class="post-header">
            <div class="post-author-info" @click="goToProfile">
                <img 
                    :src="getAvatarUrl(post.author_avatar)" 
                    alt="Avatar" 
                    class="avatar"
                >
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
            <img v-if="post.image" :src="getImageUrl(post.image)" alt="Post image" class="post-image">
        </div>
        
        <div class="post-footer">
            <button class="like-btn" @click="toggleLike" :class="{ liked: userLiked }">
                <i class="fa fa-heart"></i>
                <span>{{ post.likes_count || 0 }}</span>
            </button>
            
            <button class="comment-btn" @click="toggleComments">
                <i class="fa fa-comment"></i>
                <span>{{ post.comments_count || 0 }}</span>
            </button>
        </div>
        
        <div v-if="showComments" class="comments-section">
            <div class="comment-input">
                <input 
                    v-model="commentText" 
                    placeholder="Написать комментарий..."
                    @keyup.enter="submitComment"
                >
                <button @click="submitComment" :disabled="!commentText.trim()">
                    <i class="fa fa-send"></i>
                </button>
            </div>
            
            <div v-if="post.comments && post.comments.length > 0" class="comments-list">
                <div v-for="comment in post.comments" :key="comment.id" class="comment">
                    <img 
                        :src="getAvatarUrl(comment.author_avatar)" 
                        alt="Avatar" 
                        class="avatar"
                    >
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
</template>

<script>
import socialApi from '../../api/social'

export default {
    props: {
        post: {
            type: Object,
            required: true
        },
        currentUserId: {
            type: Number,
            required: true
        }
    },
    data() {
        return {
            showComments: false,
            commentText: '',
            userLiked: false,
            showEditModal: false,
            editContent: '',
            editImageFile: null,
            editImagePreview: null,
            isSaving: false
        }
    },
    computed: {
        isAuthor() {
            return this.post.author_id === this.currentUserId
        }
    },
    methods: {
        goToProfile() {
            this.$router.push(`/profile/${this.post.author_id}`)
        },
        getImageUrl(path) {
            if (!path) return ''
            if (path.startsWith('http://') || path.startsWith('https://')) return path
            if (path.startsWith('/')) return path
            return `/uploads/${path}`
        },
        getAvatarUrl(avatar) {
            if (!avatar) return '/default-avatar.png'
            if (avatar.startsWith('http://') || avatar.startsWith('https://')) return avatar
            if (avatar.startsWith('/')) return avatar
            return `/uploads/${avatar}`
        },
        formatDate(dateStr) {
            if (!dateStr) return ''
            const date = new Date(dateStr)
            return date.toLocaleDateString('ru-RU', {
                day: '2-digit',
                month: 'short',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            })
        },
        async toggleLike() {
            try {
                const result = await socialApi.toggleLike(this.post.id)
                this.post.likes_count = result.data.likes_count
                this.userLiked = result.data.liked
                this.$emit('like-updated', this.post.id, result.data)
            } catch (error) {
                console.error('Ошибка лайка:', error)
            }
        },
        toggleComments() {
            this.showComments = !this.showComments
            if (this.showComments && !this.post.comments) {
                this.loadComments()
            }
        },
        async loadComments() {
            try {
                const response = await socialApi.getPost(this.post.id)
                this.post.comments = response.data.comments || []
            } catch (error) {
                console.error('Ошибка загрузки комментариев:', error)
            }
        },
        async submitComment() {
            if (!this.commentText.trim()) return
            try {
                const response = await socialApi.addComment(this.post.id, this.commentText)
                if (!this.post.comments) this.post.comments = []
                this.post.comments.push(response.data)
                this.post.comments_count = (this.post.comments_count || 0) + 1
                this.commentText = ''
            } catch (error) {
                console.error('Ошибка добавления комментария:', error)
            }
        },
        async deleteComment(commentId) {
            if (!confirm('Удалить комментарий?')) return
            try {
                await socialApi.deleteComment(commentId)
                this.post.comments = this.post.comments.filter(c => c.id !== commentId)
                this.post.comments_count = Math.max(0, (this.post.comments_count || 0) - 1)
            } catch (error) {
                console.error('Ошибка удаления комментария:', error)
            }
        },

        // ===== РЕДАКТИРОВАНИЕ =====
        openEditModal() {
            this.editContent = this.post.content
            this.editImagePreview = this.post.image ? this.getImageUrl(this.post.image) : null
            this.editImageFile = null
            this.showEditModal = true
        },
        
        closeEditModal() {
            this.showEditModal = false
            this.editContent = ''
            this.editImageFile = null
            this.editImagePreview = null
        },
        
        handleEditImage(event) {
            const file = event.target.files[0]
            if (!file) return
            
            if (file.size > 5 * 1024 * 1024) {
                alert('Размер файла не должен превышать 5MB')
                return
            }
            
            if (!file.type.startsWith('image/')) {
                alert('Пожалуйста, загрузите изображение')
                return
            }
            
            this.editImageFile = file
            const reader = new FileReader()
            reader.onload = (e) => {
                this.editImagePreview = e.target.result
            }
            reader.readAsDataURL(file)
        },
        
        removeEditImage() {
            this.editImageFile = null
            this.editImagePreview = null
        },
        
        async saveEdit() {
            if (!this.editContent.trim()) {
                alert('Содержимое поста не может быть пустым')
                return
            }
            
            this.isSaving = true
            try {
                const formData = new FormData()
                formData.append('content', this.editContent.trim())
                if (this.editImageFile) {
                    formData.append('image', this.editImageFile)
                }
                
                const response = await socialApi.updatePost(this.post.id, formData)
                
                // Обновляем данные поста
                this.post.content = response.data.content
                this.post.image = response.data.image
                
                // Если изображение было удалено или изменено
                if (!this.post.image) {
                    this.post.image = null
                }
                
                this.$emit('post-updated', this.post)
                this.closeEditModal()
            } catch (error) {
                console.error('Ошибка редактирования поста:', error)
                alert('Не удалось обновить пост')
            } finally {
                this.isSaving = false
            }
        },
        
        // ===== УДАЛЕНИЕ =====
        confirmDelete() {
            if (confirm('Вы уверены, что хотите удалить этот пост?')) {
                this.deletePost()
            }
        },
        
        async deletePost() {
            try {
                await socialApi.deletePost(this.post.id)
                this.$emit('post-deleted', this.post.id)
            } catch (error) {
                console.error('Ошибка удаления поста:', error)
                alert('Не удалось удалить пост')
            }
        },
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
    gap: 20px;
    margin-top: 16px;
    padding-top: 12px;
    border-top: 1px solid var(--border-light);
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