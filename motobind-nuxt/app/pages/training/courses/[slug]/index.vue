<script setup lang="ts">
import type { CourseDetail } from '~/types'

const route = useRoute()
const api = useApi()
const mediaUrl = useMediaUrl()

const { data: course, pending, error } = await useAsyncData(
  `course-${route.params.slug}`,
  () => api.training.getCourse(route.params.slug as string)
)

if (error.value || !course.value) {
  throw createError({ statusCode: 404, statusMessage: 'Курс не найден' })
}

useSeoMeta({
  title: `${course.value.title} — Обучение`,
  description: course.value.short_description || 'Курс по ремонту и обслуживанию мотоциклов.',
  ogType: 'article',
})

const progressPercent = computed(() => {
  if (!course.value?.progress) return 0
  const { completed, total } = course.value.progress
  if (total === 0) return 0
  return Math.round((completed / total) * 100)
})

function lessonLink(lessonSlug: string) {
  return `/training/courses/${course.value!.slug}/lessons/${lessonSlug}`
}
</script>

<template>
  <div v-if="course" class="page-course">
    <header class="course-header">
      <NuxtLink to="/training" class="back-link">
        <i class="fa-solid fa-arrow-left"></i> Все курсы
      </NuxtLink>

      <div class="course-hero">
        <div
          class="course-cover"
          :style="course.cover_url ? { backgroundImage: `url(${mediaUrl(course.cover_url)})` } : {}"
        >
          <div v-if="!course.cover_url" class="cover-placeholder">
            <i class="fa-solid fa-book-open"></i>
          </div>
        </div>

        <div class="course-info">
          <div class="meta">
            <span v-if="course.level" class="badge">{{ course.level }}</span>
            <span v-if="course.is_free" class="free-badge">Бесплатно</span>
            <span class="lessons-count"><i class="fa-solid fa-book-open"></i> {{ course.lessons_count }} уроков</span>
          </div>

          <h1 class="course-title">{{ course.title }}</h1>
          <p class="course-desc">{{ course.short_description }}</p>

          <div class="author">
            <i class="fa-solid fa-user"></i>
            Автор: {{ course.author?.username || 'MotoBind' }}
          </div>

          <div v-if="course.progress && course.progress.total > 0" class="progress-section">
            <div class="progress-label">
              Прогресс: {{ course.progress.completed }} / {{ course.progress.total }} уроков
            </div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: `${progressPercent}%` }" />
            </div>
          </div>
        </div>
      </div>
    </header>

    <section v-if="course.description" class="course-description-section">
      <h2 class="section-title"><i class="fa-solid fa-align-left"></i> Описание</h2>
      <div class="prose">
        <MarkdownRenderer :content="course.description" />
      </div>
    </section>

    <section class="lessons-section">
      <h2 class="section-title"><i class="fa-solid fa-list-ol"></i> Программа курса</h2>
      <div class="lessons-list">
        <NuxtLink
          v-for="lesson in course.lessons"
          :key="lesson.id"
          :to="lesson.is_accessible ? lessonLink(lesson.slug) : '#'"
          class="lesson-item"
          :class="{
            'lesson-item--locked': !lesson.is_accessible,
            'lesson-item--completed': lesson.is_completed
          }"
          :disabled="!lesson.is_accessible"
        >
          <div class="lesson-number">
            <i v-if="lesson.is_completed" class="fa-solid fa-check"></i>
            <span v-else>{{ lesson.order }}</span>
          </div>
          <div class="lesson-content">
            <h3 class="lesson-title">{{ lesson.title }}</h3>
            <div class="lesson-meta">
              <span v-if="lesson.is_free_preview" class="preview-badge">Превью</span>
              <span v-if="lesson.has_video"><i class="fa-solid fa-video"></i> Видео</span>
              <span v-if="!lesson.is_accessible" class="locked-badge">
                <i class="fa-solid fa-lock"></i> Закрыт
              </span>
            </div>
          </div>
          <i class="fa-solid fa-chevron-right arrow" />
        </NuxtLink>
      </div>
    </section>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.page-course { max-width: 900px; margin: 0 auto; display: flex; flex-direction: column; gap: var(--space-8); padding-bottom: var(--space-10); }
.course-header { display: flex; flex-direction: column; gap: var(--space-4); }
.back-link { display: inline-flex; align-items: center; gap: var(--space-2); font-size: var(--text-sm); color: var(--color-text-secondary); width: fit-content; text-decoration: none; &:hover { color: var(--color-brand); } }
.course-hero { display: flex; flex-direction: column; gap: var(--space-6); @include md-up { flex-direction: row; align-items: flex-start; } }
.course-cover { width: 100%; aspect-ratio: 16 / 9; background: var(--color-surface-secondary); background-size: cover; background-position: center; border-radius: var(--radius-lg); overflow: hidden; flex-shrink: 0; @include md-up { width: 400px; } }
.cover-placeholder { display: flex; align-items: center; justify-content: center; height: 100%; color: var(--color-text-tertiary); font-size: 48px; }
.course-info { display: flex; flex-direction: column; gap: var(--space-3); flex: 1; }
.meta { display: flex; flex-wrap: wrap; gap: var(--space-3); font-size: var(--text-sm); font-weight: var(--fw-medium); color: var(--color-brand); }
.badge { background: var(--color-brand-soft); padding: 2px 8px; border-radius: var(--radius-sm); text-transform: uppercase; }
.free-badge { color: var(--color-success); font-weight: var(--fw-semibold); }
.course-title { font-size: var(--text-2xl); font-weight: var(--fw-bold); line-height: var(--leading-tight); }
.course-desc { font-size: var(--text-base); color: var(--color-text-secondary); line-height: var(--leading-relaxed); }
.author { font-size: var(--text-sm); color: var(--color-text-tertiary); display: flex; align-items: center; gap: var(--space-2); }
.progress-section { margin-top: var(--space-2); background: var(--color-surface-secondary); padding: var(--space-3); border-radius: var(--radius-md); }
.progress-label { font-size: var(--text-sm); font-weight: var(--fw-medium); color: var(--color-text); margin-bottom: var(--space-2); }
.progress-bar { height: 8px; background: var(--color-border); border-radius: var(--radius-full); overflow: hidden; }
.progress-fill { height: 100%; background: var(--color-brand); border-radius: var(--radius-full); transition: width var(--transition-base); }
.course-description-section { background: var(--color-surface); padding: var(--space-6); border-radius: var(--radius-lg); border: 1px solid var(--color-border); }
.course-description-section .prose { max-width: none; }
.section-title { font-size: var(--text-xl); font-weight: var(--fw-semibold); display: flex; align-items: center; gap: var(--space-2); margin-bottom: var(--space-4); i { color: var(--color-brand); } }
.lessons-list { display: flex; flex-direction: column; gap: var(--space-2); }
.lesson-item { display: flex; align-items: center; gap: var(--space-4); padding: var(--space-3) var(--space-4); background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); text-decoration: none; color: var(--color-text); transition: all var(--transition-fast); &:hover:not(.lesson-item--locked) { border-color: var(--color-brand); box-shadow: var(--shadow-sm); } &--locked { opacity: 0.6; cursor: not-allowed; } &--completed { background: var(--color-success-soft); border-color: var(--color-success); } }
.lesson-number { width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; border-radius: 50%; background: var(--color-surface-secondary); font-weight: var(--fw-bold); font-size: var(--text-sm); flex-shrink: 0; .lesson-item--completed & { background: var(--color-success); color: #fff; } }
.lesson-content { flex: 1; min-width: 0; }
.lesson-title { font-size: var(--text-base); font-weight: var(--fw-medium); margin-bottom: var(--space-1); }
.lesson-meta { display: flex; gap: var(--space-2); font-size: var(--text-xs); color: var(--color-text-tertiary); }
.preview-badge { color: var(--color-brand); font-weight: var(--fw-semibold); }
.locked-badge { color: var(--color-danger); }
.arrow { color: var(--color-text-tertiary); flex-shrink: 0; }
</style>
