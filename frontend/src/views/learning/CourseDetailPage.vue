<template>
  <div class="course-detail">
    <div v-if="learningStore.currentCourseLoading" class="course-detail__loading">
      <i class="fa fa-spinner fa-spin" /> Загрузка курса...
    </div>

    <div v-else-if="!course" class="course-detail__empty">
      <i class="fa fa-exclamation-triangle" />
      <p>Курс не найден</p>
      <router-link :to="{ name: 'learning-courses' }" class="btn btn-secondary">
        К списку курсов
      </router-link>
    </div>

    <template v-else>
      <!-- Hero -->
      <div class="course-hero">
        <div class="course-hero__cover">
          <img
            v-if="course.cover_url"
            :src="resolveMedia(course.cover_url)"
            :alt="course.title"
          />
          <div v-else class="course-hero__cover-placeholder">
            <i class="fa fa-graduation-cap" />
          </div>
        </div>
        <div class="course-hero__body">
          <div class="course-hero__category">
            {{ categoryLabel(course.category) }} · {{ levelLabel(course.level) }}
          </div>
          <h1 class="course-hero__title">{{ course.title }}</h1>
          <p v-if="course.short_description" class="course-hero__desc">
            {{ course.short_description }}
          </p>
          <div class="course-hero__meta">
            <span><i class="fa fa-book-open" /> {{ course.lessons_count }} уроков</span>
            <span v-if="course.author">
              <i class="fa fa-user" /> {{ course.author.username }}
            </span>
          </div>

          <div class="course-hero__actions">
            <!-- Прогресс для начатого -->
            <div v-if="course.progress?.completed > 0" class="course-hero__progress">
              <div class="course-hero__progress-bar">
                <div
                  class="course-hero__progress-fill"
                  :style="{ width: `${progressPercent}%` }"
                />
              </div>
              <span class="course-hero__progress-label">
                {{ course.progress.completed }} из {{ course.progress.total }}
              </span>
            </div>

            <button
              v-if="canStart"
              type="button"
              class="btn btn-primary"
              @click="startCourse"
            >
              <i class="fa fa-play" />
              {{ course.progress?.completed > 0 ? 'Продолжить' : 'Начать курс' }}
            </button>

            <div v-else-if="!course.is_free" class="course-hero__buy">
              <span class="course-hero__price">{{ formatPrice(course.price) }}</span>
              <span class="course-hero__soon">Скоро можно будет купить</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Описание -->
      <div v-if="course.description" class="course-section">
        <h2>Описание</h2>
        <MarkdownRenderer :content="course.description" />
      </div>

      <!-- Программа -->
      <div class="course-section">
        <h2>Программа курса</h2>
        <div class="lesson-list">
          <div
            v-for="l in course.lessons"
            :key="l.id"
            class="lesson-item"
            :class="{
              'lesson-item--completed': l.is_completed,
              'lesson-item--locked': !l.is_accessible,
            }"
          >
            <div class="lesson-item__num">
              <i v-if="l.is_completed" class="fa fa-check-circle" />
              <i v-else-if="!l.is_accessible" class="fa fa-lock" />
              <span v-else>{{ l.order }}</span>
            </div>
            <div class="lesson-item__body">
              <div class="lesson-item__title">{{ l.title }}</div>
              <div class="lesson-item__meta">
                <span v-if="l.is_free_preview" class="lesson-item__preview">Превью</span>
                <span v-if="l.has_video">
                  <i class="fa fa-video" /> Видео
                  <template v-if="l.video_duration">
                    · {{ formatDuration(l.video_duration) }}
                  </template>
                </span>
              </div>
            </div>
            <button
              v-if="l.is_accessible"
              type="button"
              class="lesson-item__action"
              @click="openLesson(l)"
            >
              <i class="fa fa-chevron-right" />
            </button>
            <div v-else class="lesson-item__action lesson-item__action--locked">
              <i class="fa fa-lock" />
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MarkdownRenderer from '@/components/learning/MarkdownRenderer.vue'
import { useLearningStore } from '@/stores'
import { resolveMedia } from '@/utils/mediaUrl'

const props = defineProps({
  slug: { type: String, required: true },
})

const router = useRouter()
const learningStore = useLearningStore()

const course = computed(() => learningStore.currentCourse)

const progressPercent = computed(() => {
  const p = course.value?.progress
  if (!p || !p.total) return 0
  return Math.round((p.completed / p.total) * 100)
})

const canStart = computed(() => {
  if (!course.value) return false
  if (course.value.is_free) return true
  if (course.value.is_purchased) return true
  return course.value.lessons?.some((l) => l.is_accessible)
})

onMounted(() => {
  learningStore.loadCourse(props.slug).catch(() => {})
})

function startCourse() {
  if (!course.value) return
  const lastId = course.value.last_viewed_lesson_id
  const target = lastId
    ? course.value.lessons.find((l) => l.id === lastId && l.is_accessible)
    : null
  const lesson =
    target || course.value.lessons.find((l) => l.is_accessible)
  if (lesson) openLesson(lesson)
}

function openLesson(lesson) {
  if (!lesson.is_accessible) return
  router.push({
    name: 'learning-lesson',
    params: { slug: props.slug, lessonSlug: lesson.slug },
  })
}

function categoryLabel(c) {
  const map = {
    riding: 'Вождение',
    repair: 'Ремонт',
    gear: 'Экипировка',
    first_aid: 'Первая помощь',
    law: 'Право',
    travel: 'Путешествия',
  }
  return map[c] || c
}

function levelLabel(l) {
  const map = {
    beginner: 'Начальный',
    intermediate: 'Средний',
    advanced: 'Продвинутый',
  }
  return map[l] || l
}

function formatPrice(price) {
  if (!price) return '0 ₽'
  return `${Math.floor(price / 100)} ₽`
}

function formatDuration(seconds) {
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${m}:${String(s).padStart(2, '0')}`
}
</script>

<style scoped>
.course-detail {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  max-width: 1100px;
  margin: 0 auto;
}

.course-detail__loading,
.course-detail__empty {
  padding: 48px 16px;
  text-align: center;
  color: var(--text-muted);
  font-size: var(--text-sm);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.course-detail__empty i {
  font-size: 40px;
  color: var(--warning-text);
}

/* ===== HERO ===== */
.course-hero {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: var(--space-4);
  padding: var(--space-4);
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
}

.course-hero__cover {
  aspect-ratio: 16 / 9;
  border-radius: var(--radius-md);
  overflow: hidden;
  background: var(--bg-primary);
}

.course-hero__cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.course-hero__cover-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
  font-size: 48px;
  opacity: 0.4;
}

.course-hero__body {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  min-width: 0;
}

.course-hero__category {
  font-size: 11px;
  font-weight: var(--fw-semibold);
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: var(--accent-text);
}

.course-hero__title {
  margin: 0;
  font-size: var(--text-2xl);
  font-weight: var(--fw-bold);
  line-height: var(--leading-tight);
  color: var(--text-primary);
}

.course-hero__desc {
  margin: 0;
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: var(--leading-base);
}

.course-hero__meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  font-size: var(--text-xs);
  color: var(--text-muted);
  margin-top: 4px;
}

.course-hero__meta span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.course-hero__meta i {
  font-size: 11px;
  color: var(--accent-text);
}

.course-hero__actions {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  margin-top: auto;
  padding-top: var(--space-3);
}

/* Прогресс */
.course-hero__progress {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.course-hero__progress-bar {
  height: 6px;
  background: var(--border-light);
  border-radius: 3px;
  overflow: hidden;
}

.course-hero__progress-fill {
  height: 100%;
  background: var(--accent);
  border-radius: 3px;
  transition: width var(--transition-base);
}

.course-hero__progress-label {
  font-size: var(--text-xs);
  color: var(--text-muted);
}

/* Кнопка «Начать» */
.course-hero__actions .btn {
  align-self: flex-start;
  padding: 10px 24px;
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

/* Платный курс */
.course-hero__buy {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: var(--space-2) var(--space-3);
  background: var(--accent-trans);
  border-radius: var(--radius-md);
}

.course-hero__price {
  font-size: var(--text-xl);
  font-weight: var(--fw-bold);
  color: var(--accent-text);
}

.course-hero__soon {
  font-size: var(--text-xs);
  color: var(--text-muted);
  font-style: italic;
}

/* ===== СЕКЦИИ ===== */
.course-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  padding: var(--space-4);
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
}

.course-section h2 {
  margin: 0 0 var(--space-2);
  font-size: var(--text-lg);
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
}

/* ===== СПИСОК УРОКОВ ===== */
.lesson-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.lesson-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.lesson-item:hover {
  border-color: var(--accent);
}

.lesson-item--completed {
  background: var(--success-trans);
  border-color: color-mix(in srgb, var(--success) 30%, transparent);
}

.lesson-item--locked {
  opacity: 0.7;
}

.lesson-item__num {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
  border-radius: 50%;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: var(--fw-semibold);
  color: var(--text-secondary);
}

.lesson-item--completed .lesson-item__num {
  background: var(--success);
  border-color: var(--success);
  color: #fff;
}

.lesson-item--locked .lesson-item__num {
  color: var(--text-muted);
}

.lesson-item__num i {
  font-size: 12px;
}

.lesson-item__body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.lesson-item__title {
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  color: var(--text-primary);
  overflow: hidden;
}

.lesson-item__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 11px;
  color: var(--text-muted);
}

.lesson-item__meta span {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.lesson-item__meta i {
  font-size: 10px;
}

.lesson-item__preview {
  padding: 1px 6px;
  background: var(--success-trans);
  color: var(--success-text);
  border-radius: var(--radius-full);
  font-weight: var(--fw-semibold);
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.lesson-item__action {
  width: 32px;
  height: 32px;
  min-height: 32px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  padding: 0;
}

.lesson-item__action:hover {
  border-color: var(--accent);
  color: var(--accent-text);
  background: var(--accent-trans);
}

.lesson-item__action--locked {
  color: var(--text-muted);
  cursor: default;
  opacity: 0.6;
}

.lesson-item__action--locked:hover {
  border-color: var(--border-color);
  color: var(--text-muted);
  background: transparent;
}

/* ===== АДАПТИВ ===== */
@media (max-width: 860px) {
  .course-hero {
    grid-template-columns: 1fr;
  }

  .course-hero__cover {
    max-width: 400px;
  }
}

@media (max-width: 640px) {
  .course-hero {
    padding: var(--space-3);
  }

  .course-hero__title {
    font-size: var(--text-xl);
  }

  .course-section {
    padding: var(--space-3);
  }

  .lesson-item {
    padding: 10px 12px;
    gap: 10px;
  }

  .lesson-item__num {
    width: 28px;
    height: 28px;
    font-size: 12px;
  }

  .lesson-item__title {
    font-size: var(--text-sm);
  }
}
</style>
