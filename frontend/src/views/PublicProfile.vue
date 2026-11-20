<template>
  <div class="container">
    <!-- Загрузка -->
    <div v-if="loading" class="loading-overlay">
      <div class="spinner" />
    </div>

    <!-- Профиль -->
    <div v-else-if="profile" class="profile-layout">
      <!-- Header -->
      <BaseCard class="profile-header-card">
        <div class="profile-header">
          <AppAvatar
            :src="getAvatarUrl(profile.user.avatar)"
            :size="120"
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
          <div class="stat">
            <span class="stat__value">{{ profile.user.stats?.posts_count || 0 }}</span>
            <span class="stat__label">Постов</span>
          </div>
          <div class="stat">
            <span class="stat__value">{{ profile.user.stats?.likes_received || 0 }}</span>
            <span class="stat__label">Лайков</span>
          </div>
          <div class="stat">
            <span class="stat__value">{{ profile.user.stats?.comments_received || 0 }}</span>
            <span class="stat__label">Комментариев</span>
          </div>
        </div>
      </BaseCard>

      <!-- Посты -->
      <BaseCard class="posts-card">
        <template #header>
          <div class="section-title">
            <i class="fa fa-newspaper-o" />
            Посты {{ profile.user.username }}
          </div>
        </template>

        <div v-if="profile.recent_posts?.length" class="posts-grid">
          <article
            v-for="post in profile.recent_posts"
            :key="post.id"
            class="post-preview"
            @click="goToPost(post.id)"
          >
            <img
              v-if="post.image"
              :src="getUploadUrl(post.image)"
              :alt="post.content"
              class="post-image"
            >

            <div class="post-preview__body">
              <p class="post-content">{{ post.content }}</p>

              <div class="post-meta">
                <span><i class="fa fa-heart" /> {{ post.likes_count || 0 }}</span>
                <span><i class="fa fa-comment" /> {{ post.comments_count || 0 }}</span>
                <span>{{ formatDate(post.created_at) }}</span>
              </div>
            </div>
          </article>
        </div>

        <BaseEmptyState
          v-else
          icon="fa fa-newspaper"
          title="Пока нет постов"
          description="Пользователь ещё не публиковал посты"
        />
      </BaseCard>

      <!-- Назад -->
      <div class="back-wrapper">
        <BaseButton variant="secondary" icon="fa fa-arrow-left" @click="goBack">
          Назад
        </BaseButton>
      </div>
    </div>

    <!-- Ошибка -->
    <BaseCard v-else-if="!loading && error" class="error-card">
      <BaseEmptyState
        icon="fa fa-user-slash"
        variant="danger"
        title="Профиль не найден"
        :description="error"
      >
        <BaseButton variant="primary" @click="goBack">Вернуться</BaseButton>
      </BaseEmptyState>
    </BaseCard>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getAvatarUrl, getUploadUrl } from '@/utils/mediaUrl'
import { getUserExperienceLabel, formatDate } from '@/utils/formatters'
import { BaseButton, BaseCard, BaseEmptyState, AppAvatar } from '@/components/ui'
import api from '@/api/api'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const profile = ref(null)
const error = ref(null)

const getExperienceLabel = getUserExperienceLabel

onMounted(() => {
  const userId = route.params.id
  if (userId) {
    loadProfile(userId)
  } else {
    error.value = 'ID пользователя не указан'
    loading.value = false
  }
})

async function loadProfile(userId) {
  loading.value = true
  try {
    const { data } = await api.get(`/user/profile/${userId}`)
    profile.value = data
  } catch (err) {
    console.error('Ошибка загрузки профиля:', err)
    error.value = err.response?.data?.error || 'Пользователь не найден'
  } finally {
    loading.value = false
  }
}

function goToPost(postId) {
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
}

.profile-layout {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* ===== Header ===== */
.profile-header-card :deep(.base-card__body) {
  padding: 24px;
}

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

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.stat__value {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.1;
}

.stat__label {
  font-size: 12px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.4px;
  font-weight: var(--fw-semibold);
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
  display: flex;
  flex-direction: column;
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: pointer;
  transition: transform var(--transition-fast), border-color var(--transition-fast);
}

.post-preview:hover {
  transform: translateY(-4px);
  border-color: var(--accent);
}

.post-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  display: block;
}

.post-preview__body {
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex: 1;
}

.post-content {
  font-size: 14px;
  color: var(--text-primary);
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.5;
}

.post-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  font-size: 13px;
  color: var(--text-muted);
  margin-top: auto;
}

.post-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* ===== Back ===== */
.back-wrapper {
  display: flex;
  justify-content: flex-start;
  margin-top: 4px;
}

/* ===== Loading ===== */
.loading-overlay {
  display: flex;
  justify-content: center;
  padding: 60px 0;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--border-color);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ===== Error ===== */
.error-card :deep(.base-card__body) {
  padding: 0;
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
    padding: 12px;
  }

  .stat__value {
    font-size: 20px;
  }

  .posts-grid {
    grid-template-columns: 1fr;
  }

  .back-wrapper {
    width: 100%;
  }

  .back-wrapper :deep(.base-btn) {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .profile-header-card :deep(.base-card__body) {
    padding: 16px;
  }

  .profile-username {
    font-size: 20px;
  }

  .profile-stats {
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
  }

  .stat__value {
    font-size: 18px;
  }

  .stat__label {
    font-size: 10px;
  }
}
</style>
