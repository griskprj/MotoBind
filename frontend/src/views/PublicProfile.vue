<template>
  <div class="container">
    <n-spin :show="loading">
      <!-- ==================== PROFILE ==================== -->
      <div v-if="profile" class="profile-layout">
        <!-- Header -->
        <n-card :bordered="false" class="profile-header-card">
          <div class="profile-header">
            <n-avatar
              :size="120"
              :src="getAvatarUrl(profile.user.avatar)"
              round
              class="profile-avatar"
            />

            <div class="profile-info">
              <h1 class="profile-username">{{ profile.user.username }}</h1>

              <div class="profile-meta">
                <span v-if="profile.user.location" class="meta-item">
                  <i class="fa fa-map-marker" />
                  {{ profile.user.location }}
                </span>
                <span v-if="profile.user.motorcycle" class="meta-item">
                  <i class="fa fa-motorcycle" />
                  {{ profile.user.motorcycle }}
                </span>
                <span v-if="profile.user.experience" class="meta-item">
                  <i class="fa fa-signal" />
                  {{ getExperienceLabel(profile.user.experience) }}
                </span>
                <span class="meta-item">
                  <i class="fa fa-calendar" />
                  С нами с {{ formatDate(profile.user.created_at) }}
                </span>
              </div>

              <div v-if="profile.user.bio" class="profile-bio">
                <i class="fa fa-quote-left" />
                {{ profile.user.bio }}
              </div>
            </div>
          </div>

          <!-- Статистика -->
          <div class="profile-stats">
            <n-statistic label="Постов" :value="profile.user.stats?.posts_count || 0" />
            <n-statistic label="Лайков" :value="profile.user.stats?.likes_received || 0" />
            <n-statistic label="Комментариев" :value="profile.user.stats?.comments_received || 0" />
          </div>
        </n-card>

        <!-- Посты -->
        <n-card :bordered="false" class="posts-card">
          <template #header>
            <div class="section-title">
              <i class="fa fa-newspaper-o" />
              Посты {{ profile.user.username }}
            </div>
          </template>

          <div v-if="profile.recent_posts?.length" class="posts-grid">
            <n-card
              v-for="post in profile.recent_posts"
              :key="post.id"
              :bordered="false"
              hoverable
              class="post-preview"
              @click="goToPost(post.id)"
            >
              <template v-if="post.image" #cover>
                <img :src="getUploadUrl(post.image)" :alt="post.content" class="post-image">
              </template>

              <p class="post-content">{{ post.content }}</p>

              <div class="post-meta">
                <span>
                  <i class="fa fa-heart" />
                  {{ post.likes_count || 0 }}
                </span>
                <span>
                  <i class="fa fa-comment" />
                  {{ post.comments_count || 0 }}
                </span>
                <span>{{ formatDate(post.created_at) }}</span>
              </div>
            </n-card>
          </div>

          <n-empty
            v-else
            description="Пока нет постов"
            class="empty-posts"
          >
            <template #icon>
              <i class="fa fa-newspaper-o" />
            </template>
          </n-empty>
        </n-card>

        <!-- Кнопка «Назад» -->
        <div class="back-wrapper">
          <AppButton variant="secondary" @click="goBack" class="back-btn">
            <template #icon><i class="fa fa-arrow-left" /></template>
            Назад
          </AppButton>
        </div>
      </div>

      <!-- ==================== ERROR ==================== -->
      <n-result
        v-else-if="!loading && error"
        status="404"
        title="Профиль не найден"
        :description="error"
      >
        <template #footer>
          <AppButton variant="primary" @click="goBack">Вернуться</AppButton>
        </template>
      </n-result>
    </n-spin>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getAvatarUrl, getUploadUrl } from '@/utils/mediaUrl'
import { getUserExperienceLabel, formatDate } from '@/utils/formatters'
import { AppButton } from '@/shared/ui'
import api from '@/api/api'

interface ProfileResponse {
  user: {
    id: number
    username: string
    avatar?: string | null
    location?: string | null
    motorcycle?: string | null
    experience?: string | null
    bio?: string | null
    created_at?: string
    stats?: {
      posts_count?: number
      likes_received?: number
      comments_received?: number
    }
  }
  recent_posts?: Array<{
    id: number
    content: string
    image?: string | null
    likes_count?: number
    comments_count?: number
    created_at?: string
  }>
}

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const profile = ref<ProfileResponse | null>(null)
const error = ref<string | null>(null)

const getExperienceLabel = getUserExperienceLabel

onMounted(() => {
  const userId = route.params.id as string
  if (userId) {
    loadProfile(userId)
  } else {
    error.value = 'ID пользователя не указан'
    loading.value = false
  }
})

async function loadProfile(userId: string) {
  loading.value = true
  try {
    const { data } = await api.get(`/user/profile/${userId}`)
    profile.value = data
  } catch (err: any) {
    console.error('Ошибка загрузки профиля:', err)
    error.value = err.response?.data?.error || 'Пользователь не найден'
  } finally {
    loading.value = false
  }
}

function goToPost(postId: number) {
  router.push(`/social/post/${postId}`)
}

function goBack() {
  router.back()
}
</script>

<style scoped>
.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.profile-layout {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* ===== Header ===== */
.profile-header {
  display: flex;
  gap: 24px;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--border-light);
}

.profile-avatar {
  flex-shrink: 0;
  border: 3px solid var(--accent);
}

.profile-info {
  flex: 1;
  min-width: 0;
}

.profile-username {
  font-size: 26px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 12px;
  word-break: break-word;
}

.profile-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-bottom: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: var(--text-secondary);
}

.meta-item i {
  color: var(--accent);
}

.profile-bio {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  padding: 12px 16px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  border-left: 3px solid var(--accent);
}

.profile-bio i {
  color: var(--accent);
  margin-right: 6px;
  opacity: 0.7;
}

/* ===== Stats ===== */
.profile-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  padding: 16px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
}

/* ===== Posts ===== */
.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 600;
}

.section-title i {
  color: var(--accent);
}

.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.post-preview {
  cursor: pointer;
  transition: transform 0.2s, border-color 0.2s;
}

.post-preview:hover {
  transform: translateY(-4px);
}

.post-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  display: block;
}

.post-content {
  font-size: 14px;
  color: var(--text-primary);
  margin: 0 0 10px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-meta {
  display: flex;
  gap: 12px;
  font-size: 13px;
  color: var(--text-muted);
}

.post-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.empty-posts {
  padding: 32px 0;
}

.back-wrapper {
  display: flex;
  justify-content: flex-start;
}

/* ===== Adaptive ===== */
@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .profile-meta {
    justify-content: center;
  }

  .profile-stats {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .posts-grid {
    grid-template-columns: 1fr;
  }

  .back-wrapper {
    width: 100%;
  }

  .back-btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 12px;
  }

  .profile-username {
    font-size: 20px;
  }

  .profile-stats {
    grid-template-columns: 1fr 1fr 1fr;
    padding: 12px;
  }
}
</style>
