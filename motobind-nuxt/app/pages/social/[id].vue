<script setup lang="ts">
import type { Post, PostComment } from '~/types'

definePageMeta({ middleware: 'auth' })

const route = useRoute()
const api = useApi()
const auth = useAuthStore()
const toast = useToast()
const mediaUrl = useMediaUrl()

const postId = computed(() => Number(route.params.id))

const { data: fetchedPost, pending, error, refresh } = await useAsyncData(
  `post-${postId.value}`,
  () => api.social.getPost(postId.value, true)
)

const post = ref<Post | null>(null)

    watchEffect(() => {
  if (fetchedPost.value) {
    if (!post.value || post.value.id !== fetchedPost.value.id) {
      post.value = JSON.parse(JSON.stringify(fetchedPost.value))
    }
  }
})


if (error.value || !post.value) {
  throw createError({ statusCode: 404, statusMessage: 'Пост не найден' })
}

useSeoMeta({
  title: `Пост от ${post.value.author || 'пользователя'} — MotoSocial`,
  description: post.value.content.slice(0, 150),
  robots: 'noindex',
})

// Добавление комментария
const newComment = ref('')
const submittingComment = ref(false)
const deletingCommentId = ref<number | null>(null)

async function addComment() {
  if (!newComment.value.trim() || !post.value) return

  submittingComment.value = true
  try {
    const createdComment = await api.social.addComment(postId.value, newComment.value)

    if (post.value.comments) {
      post.value.comments.push(createdComment)
    } else {
      post.value.comments = [createdComment]
    }

    post.value.comments_count += 1

    newComment.value = ''
    toast.success('Комментарий добавлен')
  } catch (e) {
    toast.error('Ошибка добавления комментария')
  } finally {
    submittingComment.value = false
  }
}

// Удаление комментария
async function deleteComment(commentId: number) {
  if (!confirm('Удалить комментарий?') || !post.value) return

  deletingCommentId.value = commentId
  try {
    await api.social.deleteComment(commentId)

    if (post.value.comments) {
      post.value.comments = post.value.comments.filter(c => c.id !== commentId)
      post.value.comments_count = Math.max(0, post.value.comments_count - 1)
    }

    toast.success('Комментарий удалён')
  } catch (e) {
    toast.error('Ошибка удаления')
  } finally {
    deletingCommentId.value = null
  }
}

// Лайк
const isLiking = ref(false)
async function toggleLike() {
  if (isLiking.value || !post.value) return
  isLiking.value = true

  const oldLiked = post.value.is_liked
  const oldCount = post.value.likes_count
  post.value.is_liked = !oldLiked
  post.value.likes_count += oldLiked ? -1 : 1

  try {
    const res = await api.social.toggleLike(postId.value)
    post.value.is_liked = res.liked
    post.value.likes_count = res.likes_count
  } catch (e) {
    post.value.is_liked = oldLiked
    post.value.likes_count = oldCount
    toast.error('Ошибка лайка')
  } finally {
    isLiking.value = false
  }
}

// Удаление поста
async function deletePost() {
  if (!confirm('Удалить пост? Это действие необратимо.')) return
  try {
    await api.social.deletePost(postId.value)
    toast.success('Пост удалён')
    navigateTo('/social')
  } catch (e) {
    toast.error('Ошибка удаления')
  }
}

// Жалоба
const showReportModal = ref(false)
const reportCategories = ref<{ value: string; label: string }[]>([])
const selectedCategory = ref('')
const reportDescription = ref('')
const submittingReport = ref(false)

async function openReport() {
  try {
    reportCategories.value = await api.social.getReportCategories()
    showReportModal.value = true
  } catch (e) {
    toast.error('Ошибка загрузки категорий')
  }
}

async function submitReport() {
  if (!selectedCategory.value) {
    toast.error('Выберите категорию жалобы')
    return
  }
  submittingReport.value = true
  try {
    await api.social.reportPost(postId.value, selectedCategory.value, reportDescription.value)
    toast.success('Жалоба отправлена модератору')
    showReportModal.value = false
    selectedCategory.value = ''
    reportDescription.value = ''
  } catch (e) {
    toast.error('Ошибка отправки жалобы')
  } finally {
    submittingReport.value = false
  }
}

// Проверка, является ли пользователь автором поста
const isAuthor = computed(() => auth.user?.id === post.value?.author_id)

// Форматирование даты
const formatDate = (iso?: string | null) => {
  if (!iso) return ''
  return new Date(iso).toLocaleString('ru-RU', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}
</script>

<template>
  <div v-if="post" class="page-post">
    <header class="page-header">
      <NuxtLink to="/social" class="back-link">
        <i class="fa-solid fa-arrow-left"></i> Назад в ленту
      </NuxtLink>
      <h1 class="page-title">Пост</h1>
    </header>

    <!-- Карточка поста -->
    <BaseCard padding="lg" class="post-card">
      <div class="post-header">
        <div class="author">
          <div class="avatar">
            <i class="fa-solid fa-user"></i>
          </div>
          <div>
            <div class="author-name">{{ post.author || 'Пользователь' }}</div>
            <div class="post-date">{{ formatDate(post.created_at) }}</div>
          </div>
        </div>
        <div class="post-actions">
          <button
            v-if="isAuthor"
            class="action-icon danger"
            title="Удалить"
            @click="deletePost"
          >
            <i class="fa-solid fa-trash"></i>
          </button>
          <button
            class="action-icon"
            title="Пожаловаться"
            @click="openReport"
          >
            <i class="fa-solid fa-flag"></i>
          </button>
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
        <button class="action-btn" :class="{ 'is-liked': post.is_liked }" @click="toggleLike">
          <i class="fa-solid fa-heart"></i> {{ post.likes_count }}
        </button>
        <span class="action-btn">
          <i class="fa-solid fa-comment"></i> {{ post.comments_count }}
        </span>
      </div>
    </BaseCard>

    <!-- Комментарии -->
    <section class="comments-section">
      <h2 class="section-title">
        <i class="fa-solid fa-comments"></i> Комментарии ({{ post.comments?.length || 0 }})
      </h2>

      <!-- Форма добавления -->
      <div class="comment-form">
        <div class="avatar">
          <i class="fa-solid fa-user"></i>
        </div>
        <input
          v-model="newComment"
          type="text"
          placeholder="Написать комментарий..."
          class="comment-input"
          @keydown.enter.prevent="addComment"
        />
        <BaseButton variant="primary" size="sm" :loading="submittingComment" @click="addComment">
          <i class="fa-solid fa-paper-plane"></i>
        </BaseButton>
      </div>

      <!-- Список комментариев -->
      <div v-if="!post.comments || post.comments.length === 0" class="no-comments">
        Пока нет комментариев. Будьте первым!
      </div>

      <div v-else class="comments-list">
        <div v-for="comment in post.comments" :key="comment.id" class="comment-item">
          <div class="avatar">
            <i class="fa-solid fa-user"></i>
          </div>
          <div class="comment-body">
            <div class="comment-header">
              <span class="comment-author">{{ comment.author || 'Пользователь' }}</span>
              <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
            </div>
            <p class="comment-text">{{ comment.content }}</p>
          </div>
          <button
            v-if="comment.user_id === auth.user?.id"
            class="delete-comment-btn"
            title="Удалить комментарий"
            @click="deleteComment(comment.id)"
          >
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>
      </div>
    </section>

    <!-- Модалка жалобы -->
    <BaseModal v-if="showReportModal" title="Пожаловаться на пост" @close="showReportModal = false">
      <div class="report-form">
        <p>Выберите причину жалобы:</p>
        <div class="categories-list">
          <label v-for="cat in reportCategories" :key="cat.value" class="category-radio">
            <input type="radio" :value="cat.value" v-model="selectedCategory" />
            {{ cat.label }}
          </label>
        </div>
        <BaseTextarea
          v-model="reportDescription"
          label="Дополнительное описание (необязательно)"
          placeholder="Опишите проблему подробнее..."
        />
      </div>
      <template #footer>
        <BaseButton variant="ghost" size="sm" @click="showReportModal = false">Отмена</BaseButton>
        <BaseButton variant="primary" size="sm" :loading="submittingReport" @click="submitReport">Отправить</BaseButton>
      </template>
    </BaseModal>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.page-post {
  max-width: 700px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
  padding-bottom: var(--space-10);
}

.page-header { display: flex; flex-direction: column; gap: var(--space-2); }
.back-link { display: inline-flex; align-items: center; gap: var(--space-2); font-size: var(--text-sm); color: var(--color-text-secondary); width: fit-content; text-decoration: none; &:hover { color: var(--color-brand); } }
.page-title { font-size: var(--text-2xl); font-weight: var(--fw-bold); }

.post-card { background: var(--color-surface); }
.post-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: var(--space-3); }
.author { display: flex; gap: var(--space-3); align-items: center; }
.avatar { width: 40px; height: 40px; border-radius: 50%; background: var(--color-surface-secondary); display: flex; align-items: center; justify-content: center; color: var(--color-text-tertiary); font-size: 18px; flex-shrink: 0; }
.author-name { font-weight: var(--fw-semibold); color: var(--color-text); }
.post-date { font-size: var(--text-xs); color: var(--color-text-tertiary); }

.post-actions { display: flex; gap: var(--space-2); }
.action-icon {
  background: none; border: none; color: var(--color-text-tertiary); cursor: pointer; padding: var(--space-1); border-radius: var(--radius-sm);
  &:hover { color: var(--color-text); background: var(--color-surface-hover); }
  &.danger:hover { color: var(--color-danger); }
}

.post-content { font-size: var(--text-base); line-height: var(--leading-relaxed); color: var(--color-text); white-space: pre-wrap; margin-bottom: var(--space-3); }
.post-image { width: 100%; border-radius: var(--radius-md); margin-bottom: var(--space-3); object-fit: cover; max-height: 400px; }
.post-footer { display: flex; gap: var(--space-4); padding-top: var(--space-3); border-top: 1px solid var(--color-border-light); }
.action-btn { display: flex; align-items: center; gap: var(--space-2); background: none; border: none; color: var(--color-text-secondary); font-size: var(--text-sm); cursor: pointer; transition: color var(--transition-fast); &:hover { color: var(--color-brand); } &.is-liked { color: var(--color-danger); } &.is-liked i { font-weight: 900; } }

/* Комментарии */
.comments-section { display: flex; flex-direction: column; gap: var(--space-4); }
.section-title { font-size: var(--text-lg); font-weight: var(--fw-semibold); display: flex; align-items: center; gap: var(--space-2); i { color: var(--color-brand); } }

.comment-form { display: flex; gap: var(--space-2); align-items: center; background: var(--color-surface); padding: var(--space-3); border-radius: var(--radius-md); border: 1px solid var(--color-border); }
.comment-input { flex: 1; padding: var(--space-2); border: none; background: transparent; color: var(--color-text); font-size: var(--text-base); &:focus { outline: none; } }

.no-comments { text-align: center; padding: var(--space-6); color: var(--color-text-tertiary); background: var(--color-surface-secondary); border-radius: var(--radius-md); }

.comments-list { display: flex; flex-direction: column; gap: var(--space-3); }
.comment-item { display: flex; gap: var(--space-3); background: var(--color-surface); padding: var(--space-3); border-radius: var(--radius-md); border: 1px solid var(--color-border); }
.comment-body { flex: 1; min-width: 0; }
.comment-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--space-1); }
.comment-author { font-weight: var(--fw-semibold); font-size: var(--text-sm); color: var(--color-text); }
.comment-date { font-size: var(--text-xs); color: var(--color-text-tertiary); }
.comment-text { font-size: var(--text-sm); color: var(--color-text-secondary); line-height: var(--leading-relaxed); white-space: pre-wrap; }
.delete-comment-btn { background: none; border: none; color: var(--color-text-tertiary); cursor: pointer; &:hover { color: var(--color-danger); } }

/* Модалка жалобы */
.report-form { display: flex; flex-direction: column; gap: var(--space-4); }
.categories-list { display: flex; flex-direction: column; gap: var(--space-2); }
.category-radio { display: flex; align-items: center; gap: var(--space-2); font-size: var(--text-sm); cursor: pointer; }
</style>
