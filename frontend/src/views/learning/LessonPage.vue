<template>
  <div class="lesson-page">
    <div v-if="learningStore.currentLessonLoading" class="lesson-page__loading">
      <i class="fa fa-spinner fa-spin" /> Загрузка урока...
    </div>

    <div v-else-if="!lesson" class="lesson-page__empty">
      <i class="fa fa-exclamation-triangle" />
      <p>Урок не найден или недоступен</p>
      <router-link
        :to="{ name: 'learning-courses' }"
        class="btn btn-secondary"
      >
        К курсам
      </router-link>
    </div>

    <template v-else>
      <!-- Хлебные крошки -->
      <nav class="lesson-breadcrumb">
        <router-link :to="{ name: 'learning-courses' }">Курсы</router-link>
        <i class="fa fa-chevron-right" />
        <router-link
          :to="{ name: 'learning-course', params: { slug: lesson.course_slug } }"
        >
          {{ lesson.course_title }}
        </router-link>
        <i class="fa fa-chevron-right" />
        <span>Урок {{ lesson.order }}</span>
      </nav>

      <!-- Контент -->
      <article class="lesson-content">
        <h1 class="lesson-content__title">{{ lesson.title }}</h1>

        <div v-if="lesson.video_url" class="lesson-video">
          <iframe
            :src="lesson.video_url"
            frameborder="0"
            allowfullscreen
            allow="autoplay; encrypted-media"
          />
        </div>

        <MarkdownRenderer v-if="lesson.content" :content="lesson.content" />
      </article>

      <!-- Кнопка «пройдено» -->
      <div class="lesson-complete">
        <button
          type="button"
          class="lesson-complete__btn"
          :class="{ 'lesson-complete__btn--done': lesson.is_completed }"
          :disabled="progressLoading"
          @click="toggleComplete"
        >
          <i :class="lesson.is_completed ? 'fa fa-check-circle' : 'fa fa-circle'" />
          {{ lesson.is_completed ? 'Пройдено' : 'Отметить пройденным' }}
        </button>
      </div>

      <!-- Навигация -->
      <nav class="lesson-nav">
        <button
          v-if="lesson.prev_lesson"
          type="button"
          class="lesson-nav__btn"
          :disabled="!lesson.prev_lesson.is_accessible"
          @click="goTo(lesson.prev_lesson)"
        >
          <i class="fa fa-arrow-left" />
          <span class="lesson-nav__btn-label">
            <span class="lesson-nav__btn-title">{{ lesson.prev_lesson.title }}</span>
            <span class="lesson-nav__btn-sub">Предыдущий урок</span>
          </span>
        </button>
        <div v-else />

        <button
          v-if="lesson.next_lesson"
          type="button"
          class="lesson-nav__btn lesson-nav__btn--right"
          :disabled="!lesson.next_lesson.is_accessible"
          @click="goTo(lesson.next_lesson)"
        >
          <span class="lesson-nav__btn-label">
            <span class="lesson-nav__btn-title">{{ lesson.next_lesson.title }}</span>
            <span class="lesson-nav__btn-sub">
              {{ lesson.next_lesson.is_accessible ? 'Следующий урок' : 'Закрыт' }}
            </span>
          </span>
          <i :class="lesson.next_lesson.is_accessible ? 'fa fa-arrow-right' : 'fa fa-lock'" />
        </button>
      </nav>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import MarkdownRenderer from '@/components/learning/MarkdownRenderer.vue'
import { useLearningStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  slug: { type: String, required: true },
  lessonSlug: { type: String, required: true },
})

const router = useRouter()
const learningStore = useLearningStore()
const authStore = useAuthStore()
const toast = useToast()
const progressLoading = ref(false)

const lesson = computed(() => learningStore.currentLesson)

onMounted(load)

watch(
  () => [props.slug, props.lessonSlug],
  load
)

function load() {
  learningStore
    .loadLesson(props.slug, props.lessonSlug)
    .catch((err) => {
      if (err.response?.status === 403) {
        toast.error('Для доступа к уроку нужна покупка курса')
        router.replace({
          name: 'learning-course',
          params: { slug: props.slug },
        })
      }
    })
}

async function toggleComplete() {
  if (!lesson.value || !authStore.isAuthenticated) {
    toast.error('Войдите, чтобы отмечать прогресс')
    return
  }
  progressLoading.value = true
  try {
    if (lesson.value.is_completed) {
      await learningStore.uncompleteLesson(props.slug, props.lessonSlug)
      toast.success('Отметка снята')
    } else {
      await learningStore.completeLesson(props.slug, props.lessonSlug)
      toast.success('Урок пройден')
    }
  } catch (err) {
    toast.error('Не удалось сохранить прогресс')
  } finally {
    progressLoading.value = false
  }
}

function goTo(navLesson) {
  if (!navLesson.is_accessible) {
    toast.error('Этот урок доступен после покупки курса')
    return
  }
  router.push({
    name: 'learning-lesson',
    params: { slug: props.slug, lessonSlug: navLesson.slug },
  })
}
</script>

<style scoped>
.lesson-page {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  max-width: 900px;
  margin: 0 auto;
}

.lesson-page__loading,
.lesson-page__empty {
  padding: 40px;
  text-align: center;
  color: var(--text-muted);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.lesson-page__empty i {
  font-size: 40px;
  color: var(--warning-text);
}

.lesson-breadcrumb {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: var(--text-sm);
  color: var(--text-muted);
  flex-wrap: wrap;
}

.lesson-breadcrumb a {
  color: var(--text-secondary);
  text-decoration: none;
}

.lesson-breadcrumb a:hover {
  color: var(--accent-text);
}

.lesson-breadcrumb i {
  font-size: 10px;
  opacity: 0.5;
}

.lesson-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.lesson-content__title {
  margin: 0;
  font-size: var(--text-2xl);
  font-weight: var(--fw-bold);
  color: var(--text-primary);
  line-height: var(--leading-tight);
}

.lesson-video {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: var(--bg-secondary);
}

.lesson-video iframe {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  border: none;
}

.lesson-complete {
  display: flex;
  justify-content: center;
  padding: var(--space-4) 0;
  border-top: 1px solid var(--border-light);
}

.lesson-complete__btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: var(--radius-full);
  border: 1px solid var(--border-color);
  background: var(--bg-secondary);
  color: var(--text-secondary);
  font-family: inherit;
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  cursor: pointer;
  transition: all var(--transition-base);
  min-height: 44px;
}

.lesson-complete__btn:hover:not(:disabled) {
  border-color: var(--accent);
  color: var(--accent-text);
}

.lesson-complete__btn--done {
  background: var(--success-trans);
  border-color: var(--success);
  color: var(--success-text);
}

.lesson-complete__btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.lesson-nav {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-3);
  padding-top: var(--space-4);
  border-top: 1px solid var(--border-light);
}

.lesson-nav__btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  font-family: inherit;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-base);
  min-height: 60px;
  text-align: left;
}

.lesson-nav__btn:hover:not(:disabled) {
  border-color: var(--accent);
  color: var(--accent-text);
}

.lesson-nav__btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.lesson-nav__btn--right {
  justify-content: flex-end;
  text-align: right;
}

.lesson-nav__btn-label {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.lesson-nav__btn-title {
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.lesson-nav__btn-sub {
  font-size: var(--text-xs);
  color: var(--text-muted);
}

@media (max-width: 640px) {
  .lesson-nav {
    grid-template-columns: 1fr;
  }
}
</style>
