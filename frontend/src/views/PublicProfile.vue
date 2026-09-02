<template>
    <div class="container">
        <LoadingOverlay :isLoading="loading" text="Загрузка профиля..."/>
        
        <div v-if="profile" class="profile-page">
            <!-- === ШАПКА ПРОФИЛЯ === -->
            <div class="profile-header">
                <div class="profile-avatar">
                    <img 
                        :src="getAvatarUrl(profile.user.avatar)" 
                        :alt="profile.user.username"
                    >
                </div>
                
                <div class="profile-info">
                    <h1 class="profile-username">{{ profile.user.username }}</h1>
                    
                    <div class="profile-meta">
                        <span v-if="profile.user.location" class="meta-item">
                            <i class="fa fa-map-marker"></i> {{ profile.user.location }}
                        </span>
                        <span v-if="profile.user.motorcycle" class="meta-item">
                            <i class="fa fa-motorcycle"></i> {{ profile.user.motorcycle }}
                        </span>
                        <span v-if="profile.user.experience" class="meta-item">
                            <i class="fa fa-signal"></i> {{ getExperienceLabel(profile.user.experience) }}
                        </span>
                        <span class="meta-item">
                            <i class="fa fa-calendar"></i> С нами с {{ formatDate(profile.user.created_at) }}
                        </span>
                    </div>
                    
                    <div v-if="profile.user.bio" class="profile-bio">
                        {{ profile.user.bio }}
                    </div>
                </div>
            </div>
            
            <!-- === СТАТИСТИКА === -->
            <div class="profile-stats">
                <div class="stat-item">
                    <span class="stat-value">{{ profile.user.stats?.posts_count || 0 }}</span>
                    <span class="stat-label">Постов</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">{{ profile.user.stats?.likes_received || 0 }}</span>
                    <span class="stat-label">Лайков</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">{{ profile.user.stats?.comments_received || 0 }}</span>
                    <span class="stat-label">Комментариев</span>
                </div>
            </div>
            
            <!-- === ПОСТЫ ПОЛЬЗОВАТЕЛЯ === -->
            <div class="profile-posts">
                <h2 class="section-title">
                    <i class="fa fa-newspaper-o"></i> Посты {{ profile.user.username }}
                </h2>
                
                <div v-if="profile.recent_posts && profile.recent_posts.length > 0" class="posts-grid">
                    <div 
                        v-for="post in profile.recent_posts" 
                        :key="post.id"
                        class="post-preview"
                        @click="goToPost(post.id)"
                    >
                        <div v-if="post.image" class="post-preview-image">
                            <img :src="getImageUrl(post.image)" :alt="post.content">
                        </div>
                        <div class="post-preview-content">
                            <p>{{ post.content }}</p>
                            <div class="post-preview-meta">
                                <span><i class="fa fa-heart"></i> {{ post.likes_count || 0 }}</span>
                                <span><i class="fa fa-comment"></i> {{ post.comments_count || 0 }}</span>
                                <span>{{ formatDate(post.created_at) }}</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div v-else class="empty-state">
                    <i class="fa fa-newspaper-o"></i>
                    <p>У {{ profile.user.username }} пока нет постов</p>
                </div>
            </div>
            
            <!-- === КНОПКА НАЗАД === -->
            <button class="btn btn-secondary back-btn" @click="$router.back()">
                <i class="fa fa-arrow-left"></i> Назад
            </button>
        </div>
        
        <!-- === ОШИБКА === -->
        <div v-else-if="!loading && error" class="error-state">
            <i class="fa fa-exclamation-triangle"></i>
            <h3>Профиль не найден</h3>
            <p>{{ error }}</p>
            <button class="btn btn-primary" @click="$router.back()">Вернуться</button>
        </div>
    </div>
</template>

<script>
import api from '../api/api'
import LoadingOverlay from '../components/LoadingOverlay.vue'

export default {
    name: 'PublicProfile',
    components: { LoadingOverlay },
    data() {
        return {
            loading: true,
            profile: null,
            error: null
        }
    },
    mounted() {
        const userId = this.$route.params.id
        if (userId) {
            this.loadProfile(userId)
        } else {
            this.error = 'ID пользователя не указан'
            this.loading = false
        }
    },
    methods: {
        async loadProfile(userId) {
            this.loading = true
            try {
                const response = await api.get(`/user/profile/${userId}`)
                this.profile = response.data
            } catch (error) {
                console.error('Ошибка загрузки профиля:', error)
                this.error = error.response?.data?.error || 'Пользователь не найден'
            } finally {
                this.loading = false
            }
        },
        
        getAvatarUrl(avatar) {
            if (!avatar) return '/default-avatar.png'
            if (avatar.startsWith('http://') || avatar.startsWith('https://')) return avatar
            if (avatar.startsWith('/')) return avatar
            return `/uploads/${avatar}`
        },
        
        getImageUrl(path) {
            if (!path) return ''
            if (path.startsWith('http://') || path.startsWith('https://')) return path
            if (path.startsWith('/')) return path
            return `/uploads/${path}`
        },
        
        getExperienceLabel(experience) {
            const labels = {
                'beginner': 'Новичок',
                'intermediate': 'Опытный',
                'expert': 'Эксперт'
            }
            return labels[experience] || experience
        },
        
        getSocialIcon(platform) {
            return 'fa fa-link'
        },
        
        formatDate(dateStr) {
            if (!dateStr) return ''
            const date = new Date(dateStr)
            return date.toLocaleDateString('ru-RU', {
                day: '2-digit',
                month: 'short',
                year: 'numeric'
            })
        },
        
        goToPost(postId) {
            this.$router.push(`/social/post/${postId}`)
        }
    }
}
</script>

<style scoped>
.container {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
}

/* ===== ПРОФИЛЬ ===== */
.profile-page {
    background: var(--bg-card);
    border-radius: 20px;
    padding: 30px;
    border: 1px solid var(--border-color);
}

.profile-header {
    display: flex;
    gap: 30px;
    margin-bottom: 30px;
    padding-bottom: 30px;
    border-bottom: 1px solid var(--border-light);
}

.profile-avatar {
    flex-shrink: 0;
}

.profile-avatar img {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    object-fit: cover;
    border: 4px solid var(--accent);
}

.profile-info {
    flex: 1;
}

.profile-username {
    font-size: 28px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 12px 0;
}

.profile-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    margin-bottom: 16px;
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 14px;
    color: var(--text-secondary);
}

.meta-item i {
    color: var(--accent-text);
}

.profile-bio {
    font-size: 15px;
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 16px;
    padding: 12px 16px;
    background: var(--bg-secondary);
    border-radius: 10px;
    border-left: 3px solid var(--accent);
}

.profile-social {
    display: flex;
    gap: 12px;
}

.social-link {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    color: var(--text-secondary);
    transition: all 0.2s;
}

.social-link:hover {
    background: var(--accent);
    color: white;
    border-color: var(--accent);
    transform: translateY(-2px);
}

/* ===== СТАТИСТИКА ===== */
.profile-stats {
    display: flex;
    justify-content: space-evenly;
    gap: 40px;
    margin-bottom: 30px;
    padding: 20px;
    background: var(--bg-secondary);
    border-radius: 12px;
}

.stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.stat-value {
    font-size: 24px;
    font-weight: 700;
    color: var(--text-primary);
}

.stat-label {
    font-size: 13px;
    color: var(--text-muted);
    margin-top: 2px;
}

/* ===== ПОСТЫ ===== */
.profile-posts {
    margin-bottom: 24px;
}

.section-title {
    font-size: 20px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0 0 20px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-title i {
    color: var(--accent-text);
}

.posts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 16px;
}

.post-preview {
    background: var(--bg-secondary);
    border-radius: 12px;
    border: 1px solid var(--border-color);
    overflow: hidden;
    cursor: pointer;
    transition: all 0.2s;
}

.post-preview:hover {
    transform: translateY(-4px);
    border-color: var(--accent);
    box-shadow: var(--shadow-md);
}

.post-preview-image {
    width: 100%;
    height: 180px;
    overflow: hidden;
}

.post-preview-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.post-preview-content {
    padding: 14px;
}

.post-preview-content p {
    font-size: 14px;
    color: var(--text-primary);
    margin: 0 0 10px 0;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.post-preview-meta {
    display: flex;
    gap: 12px;
    font-size: 13px;
    color: var(--text-muted);
}

.post-preview-meta span {
    display: flex;
    align-items: center;
    gap: 4px;
}

.post-preview-meta i {
    font-size: 13px;
}

/* ===== ПУСТОЕ СОСТОЯНИЕ ===== */
.empty-state {
    text-align: center;
    padding: 40px;
    background: var(--bg-secondary);
    border-radius: 12px;
    border: 2px dashed var(--border-color);
}

.empty-state i {
    font-size: 32px;
    color: var(--text-muted);
    margin-bottom: 12px;
}

.empty-state p {
    color: var(--text-secondary);
    margin: 0;
}

/* ===== КНОПКИ ===== */
.back-btn {
    margin-top: 16px;
}

.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 10px 24px;
    border-radius: 10px;
    font-weight: 500;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
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

.btn-primary:hover {
    background: var(--accent-hover);
    transform: translateY(-2px);
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

/* ===== АДАПТИВНОСТЬ ===== */
@media (max-width: 768px) {
    .profile-header {
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    
    .profile-avatar img {
        width: 100px;
        height: 100px;
    }
    
    .profile-meta {
        justify-content: center;
    }
    
    .profile-social {
        justify-content: center;
    }
    
    .profile-stats {
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
    }
    
    .posts-grid {
        grid-template-columns: 1fr;
    }
    
    .profile-page {
        padding: 20px;
    }
}

@media (max-width: 480px) {
    .profile-page {
        padding: 16px;
    }
    
    .profile-username {
        font-size: 22px;
    }
    
    .profile-stats {
        gap: 16px;
    }
    
    .stat-value {
        font-size: 20px;
    }
}
</style>