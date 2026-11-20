<script setup lang="ts">
import type { Post } from '~/types'

definePageMeta({ middleware: 'auth' })

useSeoMeta({
  title: 'MotoSocial — Сообщество',
  description: 'Общайтесь с мотоциклистами, делитесь опытом и вдохновением.',
  robots: 'noindex',
})

const api = useApi()
const auth = useAuthStore()
const toast = useToast()
const mediaUrl = useMediaUrl()

// Состояние для постов
const posts = ref<Post[]>([])
const pending = ref(false)
const page = ref(1)

// Состояние для формы создания
const newContent = ref('')
const imageFile = ref<File | null>(null)
const isSubmitting = ref(false)

// Загрузка постов
async function loadPosts() {
  pending.value = true
  try {
    const res = await api.social.getPosts({ page: page.value, per_page: 10 })
    posts.value = res.posts || []
  } catch (e) {
    console.error(e)
    toast.error('Не удалось загрузить ленту')
  } finally {
    pending.value = false
  }
}

onMounted(loadPosts)

// Создание поста
async function createPost() {
  if (!newContent.value.trim() && !imageFile.value) {
    toast.error('Введите текст или прикрепите картинку')
    return
  }

  isSubmitting.value = true
  try {
    await api.social.createPost(newContent.value, imageFile.value)
    newContent.value = ''
    imageFile.value = null
    toast.success('Пост опубликован!')
    await loadPosts() // Обновляем ленту
  } catch (e) {
    toast.error('Ошибка публикации')
  } finally {
    isSubmitting.value = false
  }
}

// Обработка выбора картинки
function onFileChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) imageFile.value = file
}

// Лайк для поста в ленте
const likingId = ref<number | null>(null)

async function toggleLike(post: Post) {
  if (likingId.value === post.id) return
  likingId.value = post.id

  const oldLiked = post.is_liked
  const oldCount = post.likes_count
  post.is_liked = !oldLiked
  post.likes_count += oldLiked ? -1 : 1

  try {
    const res = await api.social.toggleLike(post.id)
    post.is_liked = res.liked
    post.likes_count = res.likes_count
  } catch (e) {
    post.is_liked = oldLiked
    post.likes_count = oldCount
    toast.error('Ошибка лайка')
  } finally {
    likingId.value = null
  }
}
</script>

<template>
  <div class="page-social">
    <header class="page-header">
      <h1 class="page-title">MotoSocial</h1>
      <p class="page-subtitle">Общайтесь с мотоциклистами, делитесь опытом и вдохновением.</p>
    </header>

    <!-- Форма создания поста -->
    <BaseCard padding="lg" class="create-post-card">
      <div class="create-header">
        <div class="avatar">
          <i class="fa-solid fa-user"></i>
        </div>
        <textarea
          v-model="newContent"
          placeholder="Что нового в мире мотоциклов?"
          class="post-textarea"
          rows="3"
        />
      </div>
      <div class="create-footer">
        <label class="attach-btn">
          <input type="file" accept="image/*" class="visually-hidden" @change="onFileChange" />
          <i class="fa-solid fa-image"></i>
          <span v-if="imageFile">{{ imageFile.name }}</span>
        </label>
        <BaseButton variant="primary" :loading="isSubmitting" @click="createPost">
          Опубликовать
        </BaseButton>
      </div>
    </BaseCard>

    <!-- Лента -->
    <div v-if="pending" class="loading">
      <BaseSkeleton height="200px" rounded v-for="i in 3" :key="i" />
    </div>

    <div v-else class="posts-list">
      <div v-if="posts.length === 0" class="empty">Пока нет постов. Будьте первым!</div>

      <BaseCard v-for="post in posts" :key="post.id" padding="lg" class="post-card">
        <div class="post-header">
          <div class="author">
            <div class="avatar">
              <i class="fa-solid fa-user"></i>
            </div>
            <div>
              <div class="author-name">{{ post.author || 'Пользователь' }}</div>
              <div class="post-date">{{ new Date(post.created_at || '').toLocaleDateString('ru-RU') }}</div>
            </div>
          </div>
        </div>

        <p class="post-content">{{ post.content }}</p>
        <img
          v-if="post.image"
          :src="mediaUrl(post.image)!"
          class="post-image"
          loading="lazy"
        />

        <div class="post-footer">
          <button
            class="action-btn"
            :class="{ 'is-liked': post.is_liked }"
            @click="toggleLike(post)"
          >
            <i class="fa-solid fa-heart"></i> {{ post.likes_count }}
          </button>
          <NuxtLink :to="`/social/${post.id}`" class="action-btn">
            <i class="fa-solid fa-comment"></i> {{ post.comments_count }}
          </NuxtLink>
        </div>
      </BaseCard>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.page-social {
  max-width: 700px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
  padding-bottom: var(--space-10);
}

.page-title { font-size: var(--text-3xl); font-weight: var(--fw-bold); }
.page-subtitle { color: var(--color-text-secondary); margin-top: var(--space-1); }

/* Создание поста */
.create-post-card {
  background: var(--color-surface);
}

.create-header {
  display: flex;
  gap: var(--space-3);
  margin-bottom: var(--space-3);
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--color-surface-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-tertiary);
  font-size: 18px;
  flex-shrink: 0;
}

.post-textarea {
  width: 100%;
  min-height: 80px;
  padding: var(--space-2);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface-secondary);
  color: var(--color-text);
  font-family: inherit;
  font-size: var(--text-base);
  resize: vertical;

  &:focus {
    outline: none;
    border-color: var(--color-brand);
  }
}

.create-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: var(--space-3);
  border-top: 1px solid var(--color-border-light);
}

.attach-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-md);
  transition: background var(--transition-fast);

  &:hover { background: var(--color-surface-hover); }
  i { font-size: 18px; }
}

/* Посты */
.posts-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.empty {
  text-align: center;
  padding: var(--space-8);
  color: var(--color-text-secondary);
}

.post-card {
  background: var(--color-surface);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-3);
}

.author {
  display: flex;
  gap: var(--space-3);
  align-items: center;
}

.author-name {
  font-weight: var(--fw-semibold);
  color: var(--color-text);
}

.post-date {
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
}

.post-content {
  font-size: var(--text-base);
  line-height: var(--leading-relaxed);
  color: var(--color-text);
  white-space: pre-wrap;
  margin-bottom: var(--space-3);
}

.post-image {
  width: 100%;
  border-radius: var(--radius-md);
  margin-bottom: var(--space-3);
  object-fit: cover;
  max-height: 400px;
}

.post-footer {
  display: flex;
  gap: var(--space-4);
  padding-top: var(--space-3);
  border-top: 1px solid var(--color-border-light);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  background: none;
  border: none;
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  cursor: pointer;
  transition: color var(--transition-fast);

  &:hover { color: var(--color-brand); }
  &.is-liked { color: var(--color-danger); }
  &.is-liked i { font-weight: 900; }
}

.loading {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}
</style>
