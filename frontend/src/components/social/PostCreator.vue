<template>
    <div class="post-creator">
        <div class="creator-header">
            <img :src="userAvatar || '/default-avatar.png'" alt="Avatar" class="avatar">
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

<script>
import socialApi from '../../api/social'

export default {
    data() {
        return {
            content: '',
            imageFile: null,
            imagePreview: null,
            isSubmitting: false
        }
    },
    computed: {
        userName() {
            const user = JSON.parse(localStorage.getItem('user') || '{}')
            return user.username || 'Пользователь'
        },
        userAvatar() {
            const user = JSON.parse(localStorage.getItem('user') || '{}')
            return `/uploads/${user.avatar}`
        }
    },
    methods: {
        handleImageUpload(event) {
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
            
            this.imageFile = file
            const reader = new FileReader()
            reader.onload = (e) => {
                this.imagePreview = e.target.result
            }
            reader.readAsDataURL(file)
        },
        removeImage() {
            this.imageFile = null
            this.imagePreview = null
        },
        async submitPost() {
            if (!this.content.trim() || this.isSubmitting) return
            
            this.isSubmitting = true
            try {
                const formData = new FormData()
                formData.append('content', this.content.trim())
                if (this.imageFile) {
                    formData.append('image', this.imageFile)
                }
                
                await socialApi.createPost(formData)
                this.content = ''
                this.removeImage()
                this.$emit('post-created')
            } catch (error) {
                console.error('Ошибка создания поста:', error)
                alert('Не удалось создать пост')
            } finally {
                this.isSubmitting = false
            }
        }
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