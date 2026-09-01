<template>
    <div class="container">
        <LoadingOverlay :isLoading="loading" text="Загрузка ленты..."/>
        
        <Header
            title="MotoSocial"
            subtitle="Общайтесь с мотоциклистами, делитесь опытом и вдохновением"
        />
        
        <div class="social-feed">
            <!-- Создание поста -->
            <PostCreator @post-created="handlePostCreated" />
            
            <!-- Лента постов -->
            <div v-if="posts.length > 0" class="posts-feed">
                <PostCard
                    v-for="post in posts"
                    :key="post.id"
                    :post="post"
                    :currentUserId="currentUserId"
                    @like-updated="handleLikeUpdated"
                    @post-deleted="handlePostDeleted"
                    @post-updated="handlePostUpdated"
                />
            </div>
            
            <!-- Пустое состояние -->
            <div v-else-if="!loading" class="empty-state">
                <i class="fa fa-users" style="font-size: 48px; color: var(--text-muted);"></i>
                <p>Пока нет постов</p>
                <p class="empty-hint">Будьте первым, кто поделится новостью!</p>
            </div>
            
            <!-- Пагинация -->
            <div v-if="pagination.total > pagination.per_page" class="pagination">
                <button 
                    @click="loadPosts(pagination.current_page - 1)"
                    :disabled="!pagination.has_prev"
                    class="btn btn-secondary"
                >
                    <i class="fa fa-arrow-left"></i> Назад
                </button>
                <span>Страница {{ pagination.current_page }} из {{ pagination.pages }}</span>
                <button 
                    @click="loadPosts(pagination.current_page + 1)"
                    :disabled="!pagination.has_next"
                    class="btn btn-secondary"
                >
                    Вперед <i class="fa fa-arrow-right"></i>
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import socialApi from '../api/social'
import Header from '../components/Header.vue'
import LoadingOverlay from '../components/LoadingOverlay.vue'
import PostCreator from '../components/social/PostCreator.vue'
import PostCard from '../components/social/PostCard.vue'

export default {
    name: 'Social',
    components: { Header, LoadingOverlay, PostCreator, PostCard },
    data() {
        return {
            loading: false,
            posts: [],
            pagination: {
                current_page: 1,
                per_page: 10,
                total: 0,
                pages: 0,
                has_prev: false,
                has_next: false
            },
            currentUserId: null
        }
    },
    mounted() {
        const user = JSON.parse(localStorage.getItem('user') || '{}')
        this.currentUserId = user.id
        this.loadPosts()
    },
    methods: {
        async loadPosts(page = 1) {
            this.loading = true
            try {
                const response = await socialApi.getPosts(page, 10, null, true)
                this.posts = response.data.posts || []
                this.pagination = {
                    current_page: response.data.current_page,
                    per_page: response.data.per_page,
                    total: response.data.total,
                    pages: response.data.pages,
                    has_prev: response.data.has_prev,
                    has_next: response.data.has_next
                }
            } catch (error) {
                console.error('Ошибка загрузки постов:', error)
            } finally {
                this.loading = false
            }
        },
        
        handlePostCreated() {
            this.loadPosts(1)
        },
        
        handlePostDeleted(postId) {
            this.posts = this.posts.filter(p => p.id !== postId)
            this.pagination.total = Math.max(0, this.pagination.total - 1)
            
            if (this.posts.length === 0 && this.pagination.current_page > 1) {
                this.loadPosts(this.pagination.current_page - 1)
            }
        },
        
        handlePostUpdated(updatedPost) {
            const index = this.posts.findIndex(p => p.id === updatedPost.id)
            if (index !== -1) {
                this.posts[index] = updatedPost
            }
        },
        
        handleLikeUpdated(postId, data) {
            const post = this.posts.find(p => p.id === postId)
            if (post) {
                post.likes_count = data.likes_count
                post.is_liked = data.liked
            }
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

.social-feed {
    margin-top: 20px;
}

.posts-feed {
    margin-top: 20px;
}

.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 16px;
    margin-top: 20px;
}

.empty-state {
    text-align: center;
    padding: 60px 20px;
    background: var(--bg-card);
    border-radius: 16px;
    border: 2px dashed var(--border-color);
}

.empty-state p {
    font-size: 18px;
    color: var(--text-secondary);
    margin-top: 16px;
}

.empty-hint {
    font-size: 14px !important;
    color: var(--text-muted) !important;
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

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.btn-secondary {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}

.btn-secondary:hover:not(:disabled) {
    background: var(--border-color);
}
</style>