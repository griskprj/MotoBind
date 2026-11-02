<script setup lang="ts">
const route = useRoute()
const api = useApi()
const auth = useAuthStore()
const toast = useToast()

const courseSlug = computed(() => route.params.slug as string)
const lessonSlug = computed(() => route.params.lesson_slug as string)

const { data: lesson, pending, error, refresh } = await useAsyncData(
  `lesson-${courseSlug.value}-${lessonSlug.value}`,
  () => api.training.getLesson(courseSlug.value, lessonSlug.value)
)

if (error.value || !lesson.value) {
  throw createError({ statusCode: 404, statusMessage: 'Урок не найден' })
}

useSeoMeta({
  title: `${lesson.value.title} — ${lesson.value.course_title}`,
  description: `Урок ${lesson.value.order} курса «${lesson.value.course_title}»`,
  ogType: 'article',
})

const isCompleted = ref(lesson.value.is_completed)
const submitting = ref(false)

async function toggleComplete() {
  if (!auth.isAuthenticated) {
    toast.info('Войдите, чтобы сохранять прогресс')
    return
  }

  submitting.value = true
  try {
    if (isCompleted.value) {
      await api.training.uncompleteLesson(courseSlug.value, lessonSlug.value)
      isCompleted.value = false
      toast.success('Отметка снята')
    } else {
      await api.training.completeLesson(courseSlug.value, lessonSlug.value)
      isCompleted.value = true
      toast.success('Урок отмечен как пройденный')
    }
    await refresh()
  } catch (e: any) {
    toast.error(e.message || 'Ошибка сохранения прогресса')
  } finally {
    submitting.value = false
  }
}

function lessonLink(slug: string) {
  return `/training/courses/${courseSlug.value}/lessons/${slug}`
}
</script>

<template>
  <div v-if="lesson" class="page-lesson">
    <header class="lesson-header">
      <div class="header-top">
        <NuxtLink :to="`/training/courses/${courseSlug}`" class="back-link">
          <i class="fa-solid fa-arrow-left"></i> К курсу
        </NuxtLink>
        <span class="course-title-small">{{ lesson.course_title }}</span>
      </div>
      <h1 class="lesson-title">{{ lesson.title }}</h1>
      <div class="meta">
        <span>Урок {{ lesson.order }}</span>
        <span v-if="lesson.is_free_preview" class="preview-badge">Превью</span>
      </div>
    </header>

    <div v-if="lesson.video_url" class="video-wrap">
      <video :src="lesson.video_url" controls class="lesson-video" />
    </div>

    <div class="lesson-content prose">
      <MarkdownRenderer :content="lesson.content" />
    </div>

    <div class="action-bar">
      <BaseButton
        :variant="isCompleted ? 'secondary' : 'primary'"
        :loading="submitting"
        @click="toggleComplete"
      >
        <template #icon>
          <i :class="isCompleted ? 'fa-solid fa-rotate-left' : 'fa-solid fa-check'"></i>
        </template>
        {{ isCompleted ? 'Снять отметку' : 'Отметить пройденным' }}
      </BaseButton>
    </div>

    <nav class="lesson-nav">
      <NuxtLink
        v-if="lesson.prev_lesson"
        :to="lessonLink(lesson.prev_lesson.slug)"
        class="nav-link nav-link--prev"
      >
        <i class="fa-solid fa-arrow-left"></i>
        <div class="nav-text">
          <span class="nav-label">Предыдущий</span>
          <span class="nav-title">{{ lesson.prev_lesson.title }}</span>
        </div>
      </NuxtLink>
      <div v-else class="nav-spacer" />

      <NuxtLink
        v-if="lesson.next_lesson"
        :to="lessonLink(lesson.next_lesson.slug)"
        class="nav-link nav-link--next"
      >
        <div class="nav-text">
          <span class="nav-label">Следующий</span>
          <span class="nav-title">{{ lesson.next_lesson.title }}</span>
        </div>
        <i class="fa-solid fa-arrow-right"></i>
      </NuxtLink>
      <div v-else class="nav-spacer" />
    </nav>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.page-lesson { max-width: 800px; margin: 0 auto; display: flex; flex-direction: column; gap: var(--space-6); padding-bottom: var(--space-10); }
.lesson-header { display: flex; flex-direction: column; gap: var(--space-2); }
.header-top { display: flex; justify-content: space-between; align-items: center; }
.back-link { display: inline-flex; align-items: center; gap: var(--space-2); font-size: var(--text-sm); color: var(--color-text-secondary); width: fit-content; text-decoration: none; &:hover { color: var(--color-brand); } }
.course-title-small { font-size: var(--text-xs); color: var(--color-text-tertiary); text-transform: uppercase; }
.lesson-title { font-size: var(--text-3xl); font-weight: var(--fw-bold); line-height: var(--leading-tight); }
.meta { display: flex; gap: var(--space-3); font-size: var(--text-sm); color: var(--color-text-secondary); }
.preview-badge { color: var(--color-brand); font-weight: var(--fw-semibold); }
.video-wrap { background: #000; border-radius: var(--radius-md); overflow: hidden; aspect-ratio: 16 / 9; }
.lesson-video { width: 100%; height: 100%; display: block; }
.lesson-content { font-size: var(--text-base); line-height: var(--leading-relaxed); color: var(--color-text); :deep(h2), :deep(h3) { margin-top: 1.5em; margin-bottom: 0.5em; font-weight: var(--fw-semibold); } }
.action-bar { display: flex; justify-content: center; padding: var(--space-4) 0; border-top: 1px solid var(--color-border); border-bottom: 1px solid var(--color-border); }
.lesson-nav { display: flex; justify-content: space-between; align-items: center; gap: var(--space-4); }
.nav-link { display: flex; align-items: center; gap: var(--space-3); padding: var(--space-3) var(--space-4); background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); text-decoration: none; color: var(--color-text); transition: border-color var(--transition-fast), box-shadow var(--transition-fast); max-width: 45%; &:hover { border-color: var(--color-brand); box-shadow: var(--shadow-sm); } &--prev { text-align: left; } &--next { text-align: right; flex-direction: row-reverse; } }
.nav-text { display: flex; flex-direction: column; gap: 2px; }
.nav-label { font-size: var(--text-xs); color: var(--color-text-tertiary); }
.nav-title { font-size: var(--text-sm); font-weight: var(--fw-medium); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.nav-spacer { width: 45%; }
@media (max-width: 640px) { .nav-link { max-width: 100%; } .nav-spacer { display: none; } .lesson-nav { flex-direction: column; } }
</style>
