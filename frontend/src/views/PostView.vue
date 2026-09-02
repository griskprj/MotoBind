<template>
    <div class="container">
        <LoadingOverlay :isLoading="loading" text="Загрузка поста..."/>
        
        <!-- === HEADER === -->
        <Header
            title="Пост"
            subtitle="Просмотр публикации"
        />

        <!-- === НАВИГАЦИЯ === -->
        <div class="post-nav">
            <button class="btn btn-secondary btn-sm" @click="$router.back()">
                <i class="fa fa-arrow-left"></i> Назад
            </button>
        </div>

        <!-- === ПОСТ === -->
        <div v-if="post" class="post-container">
            <div class="post-card">
                <!-- Шапка поста -->
                <div class="post-header">
                    <div class="post-author-info" @click="goToProfile(post.author_id)">
                        <img 
                            :src="getAvatarUrl(post.author_avatar)" 
                            alt="Avatar" 
                            class="avatar"
                            @error="handleAvatarError"
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
                
                <!-- Контент -->
                <div class="post-content">
                    <p>{{ post.content }}</p>
                    <img v-if="post.image" :src="getImageUrl(post.image)" alt="Post image" class="post-image">
                </div>
                
                <!-- Футер с лайками и комментариями -->
                <div class="post-footer">
                    <button class="like-btn" @click="toggleLike" :class="{ liked: post.is_liked }">
                        <i class="fa fa-heart"></i>
                        <span>{{ post.likes_count || 0 }}</span>
                    </button>
                    
                    <button class="comment-btn">
                        <i class="fa fa-comment"></i>
                        <span>{{ post.comments_count || 0 }}</span>
                    </button>
                </div>
            </div>

            <!-- === КОММЕНТАРИИ === -->
            <div class="comments-section">
                <h3 class="comments-title">
                    <i class="fa fa-comments"></i> 
                    Комментарии ({{ post.comments_count || 0 }})
                </h3>
                
                <!-- Форма добавления комментария -->
                <div class="comment-input-wrapper">
                    <img 
                        :src="getAvatarUrl(currentUser?.avatar)" 
                        alt="Your avatar" 
                        class="avatar-small"
                        @error="handleAvatarError"
                    >
                    <div class="comment-input-group">
                        <input 
                            v-model="commentText" 
                            placeholder="Написать комментарий..."
                            @keyup.enter="submitComment"
                            :disabled="isSubmittingComment"
                        >
                        <button 
                            @click="submitComment" 
                            :disabled="!commentText.trim() || isSubmittingComment"
                            class="btn-send"
                        >
                            <i v-if="isSubmittingComment" class="fa fa-spinner fa-spin"></i>
                            <i v-else class="fa fa-arrow-right"></i>
                        </button>
                    </div>
                </div>
                
                <!-- Список комментариев -->
                <div v-if="comments.length > 0" class="comments-list">
                    <div 
                        v-for="comment in comments" 
                        :key="comment.id" 
                        class="comment-item"
                    >
                        <img 
                            :src="getAvatarUrl(comment.author_avatar)" 
                            alt="Avatar" 
                            class="avatar-small"
                            @error="handleAvatarError"
                        >
                        <div class="comment-body">
                            <div class="comment-header">
                                <span class="comment-author" @click="goToProfile(comment.user_id)">
                                    {{ comment.author }}
                                </span>
                                <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
                            </div>
                            <p class="comment-text">{{ comment.content }}</p>
                        </div>
                        <button 
                            v-if="comment.user_id === currentUserId" 
                            class="delete-comment"
                            @click="deleteComment(comment.id)"
                            title="Удалить комментарий"
                        >
                            <i class="fa fa-times"></i>
                        </button>
                    </div>
                </div>
                
                <!-- Пустое состояние комментариев -->
                <div v-else class="empty-comments">
                    <i class="fa fa-comment-o"></i>
                    <p>Пока нет комментариев. Будьте первым!</p>
                </div>
            </div>
        </div>
        
        <!-- === ПОСТ НЕ НАЙДЕН === -->
        <div v-else-if="!loading && error" class="error-state">
            <i class="fa fa-exclamation-triangle"></i>
            <h3>Пост не найден</h3>
            <p>{{ error }}</p>
            <button class="btn btn-primary" @click="$router.back()">Вернуться</button>
        </div>

        <!-- === МОДАЛКА РЕДАКТИРОВАНИЯ === -->
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
import api from '../api/api'
import socialApi from '../api/social'
import Header from '../components/Header.vue'
import LoadingOverlay from '../components/LoadingOverlay.vue'

export default {
    name: 'PostView',
    components: { Header, LoadingOverlay },
    
    data() {
        return {
            loading: true,
            error: null,
            post: null,
            comments: [],
            currentUser: null,
            currentUserId: null,
            
            commentText: '',
            isSubmittingComment: false,
            
            showEditModal: false,
            editContent: '',
            editImageFile: null,
            editImagePreview: null,
            isSaving: false
        }
    },
    
    computed: {
        isAuthor() {
            return this.post?.author_id === this.currentUserId
        }
    },
    
    mounted() {
        const userId = JSON.parse(localStorage.getItem('user') || '{}')
        this.currentUserId = userId.id
        this.currentUser = userId
        
        const postId = this.$route.params.id
        if (postId) {
            this.loadPost(postId)
        } else {
            this.error = 'ID поста не указан'
            this.loading = false
        }
    },
    
    methods: {
        async loadPost(postId) {
            this.loading = true
            try {
                const response = await socialApi.getPost(postId, true)
                this.post = response.data
                this.comments = this.post.comments || []
            } catch (error) {
                console.error('Ошибка загрузки поста:', error)
                this.error = error.response?.data?.error || 'Пост не найден'
            } finally {
                this.loading = false
            }
        },
        
        async toggleLike() {
            try {
                const result = await socialApi.toggleLike(this.post.id)
                this.post.likes_count = result.data.likes_count
                this.post.is_liked = result.data.liked
            } catch (error) {
                console.error('Ошибка лайка:', error)
            }
        },
        
        async submitComment() {
            if (!this.commentText.trim() || this.isSubmittingComment) return
            
            this.isSubmittingComment = true
            try {
                const response = await socialApi.addComment(this.post.id, this.commentText)
                const newComment = response.data
                this.comments.push(newComment)
                this.post.comments_count = (this.post.comments_count || 0) + 1
                this.commentText = ''
            } catch (error) {
                console.error('Ошибка добавления комментария:', error)
                alert('Не удалось добавить комментарий')
            } finally {
                this.isSubmittingComment = false
            }
        },
        
        async deleteComment(commentId) {
            if (!confirm('Удалить комментарий?')) return
            try {
                await socialApi.deleteComment(commentId)
                this.comments = this.comments.filter(c => c.id !== commentId)
                this.post.comments_count = Math.max(0, (this.post.comments_count || 0) - 1)
            } catch (error) {
                console.error('Ошибка удаления комментария:', error)
                alert('Не удалось удалить комментарий')
            }
        },
        
        // ===== РЕДАКТИРОВАНИЕ ПОСТА =====
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
                
                this.post.content = response.data.content
                this.post.image = response.data.image
                
                if (!this.post.image) {
                    this.post.image = null
                }
                
                this.closeEditModal()
            } catch (error) {
                console.error('Ошибка редактирования поста:', error)
                alert('Не удалось обновить пост')
            } finally {
                this.isSaving = false
            }
        },
        
        // ===== УДАЛЕНИЕ ПОСТА =====
        confirmDelete() {
            if (confirm('Вы уверены, что хотите удалить этот пост?')) {
                this.deletePost()
            }
        },
        
        async deletePost() {
            try {
                await socialApi.deletePost(this.post.id)
                this.$router.push('/social')
            } catch (error) {
                console.error('Ошибка удаления поста:', error)
                alert('Не удалось удалить пост')
            }
        },
        
        // ===== НАВИГАЦИЯ =====
        goToProfile(userId) {
            this.$router.push(`/profile/${userId}`)
        },
        
        // ===== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ =====
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
        
        handleAvatarError(event) {
            event.target.src = '/default-avatar.png'
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
        }
    }
}
</script>

<style scoped>
.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

/* ===== НАВИГАЦИЯ ===== */
.post-nav {
    margin-bottom: 20px;
}

.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 8px 20px;
    border-radius: 8px;
    font-weight: 500;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-sm {
    padding: 6px 14px;
    font-size: 13px;
}

.btn-secondary {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}

.btn-secondary:hover {
    background: var(--border-color);
}

/* ===== ПОСТ ===== */
.post-container {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.post-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 24px;
}

.post-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
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

.avatar {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    object-fit: cover;
    background: var(--bg-secondary);
}

.post-author {
    flex: 1;
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
    border-radius: 6px;
    transition: all 0.2s;
}

.btn-icon:hover {
    background: var(--bg-secondary);
    color: var(--text-primary);
}

.post-content p {
    color: var(--text-primary);
    margin-bottom: 16px;
    line-height: 1.8;
    font-size: 16px;
    white-space: pre-wrap;
}

.post-image {
    width: 100%;
    max-height: 500px;
    object-fit: cover;
    border-radius: 12px;
}

.post-footer {
    display: flex;
    gap: 24px;
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid var(--border-light);
}

.like-btn,
.comment-btn {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: color 0.2s;
    font-size: 15px;
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

/* ===== КОММЕНТАРИИ ===== */
.comments-section {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 24px;
}

.comments-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0 0 16px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.comments-title i {
    color: var(--accent-text);
}

.comment-input-wrapper {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
}

.avatar-small {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    object-fit: cover;
    background: var(--bg-secondary);
    flex-shrink: 0;
}

.comment-input-group {
    flex: 1;
    display: flex;
    gap: 8px;
}

.comment-input-group input {
    flex: 1;
    padding: 10px 14px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: 20px;
    color: var(--text-primary);
    font-size: 14px;
    outline: none;
    transition: border 0.2s;
}

.comment-input-group input:focus {
    border-color: var(--accent);
}

.comment-input-group input:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.btn-send {
    background: var(--accent);
    border: none;
    padding: 2px;
    border-radius: 50%;
    width: 45px;
    height: 40px;
    color: white;
    cursor: pointer;
    transition: background 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.btn-send:hover {
    background: var(--accent-hover);
}

.btn-send:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.comments-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.comment-item {
    display: flex;
    gap: 12px;
    padding: 12px;
    background: var(--bg-secondary);
    border-radius: 12px;
    align-items: flex-start;
}

.comment-body {
    flex: 1;
}

.comment-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 4px;
}

.comment-author {
    font-weight: 600;
    font-size: 14px;
    color: var(--text-primary);
    cursor: pointer;
}

.comment-author:hover {
    color: var(--accent-text);
}

.comment-date {
    font-size: 11px;
    color: var(--text-muted);
}

.comment-text {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.5;
}

.delete-comment {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 4px;
    transition: color 0.2s;
    flex-shrink: 0;
}

.delete-comment:hover {
    color: var(--danger);
}

.empty-comments {
    text-align: center;
    padding: 30px 20px;
    color: var(--text-muted);
}

.empty-comments i {
    font-size: 32px;
    margin-bottom: 12px;
    opacity: 0.5;
}

.empty-comments p {
    margin: 0;
    font-size: 15px;
}

/* ===== ОШИБКА ===== */
.error-state {
    text-align: center;
    padding: 60px 20px;
    background: var(--bg-card);
    border-radius: 16px;
    border: 1px solid var(--border-color);
}

.error-state i {
    font-size: 48px;
    color: var(--danger);
    margin-bottom: 16px;
}

.error-state h3 {
    font-size: 22px;
    color: var(--text-primary);
    margin: 0 0 8px 0;
}

.error-state p {
    color: var(--text-secondary);
    margin-bottom: 20px;
}

.btn-primary {
    background: var(--accent);
    color: white;
    padding: 10px 24px;
    border-radius: 8px;
    border: none;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-primary:hover {
    background: var(--accent-hover);
    transform: translateY(-2px);
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

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.btn-primary {
    background: var(--accent);
    color: white;
    padding: 8px 20px;
    border-radius: 8px;
    font-weight: 500;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-primary:hover:not(:disabled) {
    background: var(--accent-hover);
    transform: translateY(-2px);
}

.btn-secondary {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
    padding: 8px 20px;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-secondary:hover:not(:disabled) {
    background: var(--border-color);
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
    .container {
        padding: 12px;
    }
    
    .post-card {
        padding: 16px;
    }
    
    .comments-section {
        padding: 16px;
    }
    
    .post-content p {
        font-size: 15px;
    }
    
    .comment-input-wrapper {
        flex-direction: column;
        align-items: stretch;
    }
    
    .avatar-small {
        display: none;
    }
    
    .edit-modal {
        padding: 20px;
        width: 95%;
    }
    
    .edit-modal-footer {
        flex-direction: column;
    }
    
    .edit-modal-footer .btn {
        width: 100%;
        justify-content: center;
    }
}

@media (max-width: 480px) {
    .post-header {
        flex-wrap: wrap;
    }
    
    .post-author-info {
        flex: 1;
        min-width: 0;
    }
    
    .avatar {
        width: 36px;
        height: 36px;
    }
    
    .username {
        font-size: 14px;
    }
    
    .post-content p {
        font-size: 14px;
    }
    
    .comments-title {
        font-size: 16px;
    }
    
    .comment-item {
        padding: 10px;
    }
    
    .comment-text {
        font-size: 13px;
    }
}
</style>