<script setup lang="ts">
import type { MyLearningResponse, CourseWithProgress } from '~/types'

definePageMeta({ middleware: 'auth' })

useSeoMeta({
  title: 'Моё обучение',
  robots: 'noindex',
})

const api = useApi()
const mediaUrl = useMediaUrl()

const { data, pending, error } = await useAsyncData(
  'my-learning',
  () => api.training.myLearning()
)

// Вычисление процента прогресса
function getProgressPercent(progress: { completed: number; total: number }) {
  if (progress.total === 0) return 0
  return Math.round((progress.completed / progress.total) * 100)
}
</script>

<template>
  <div class="my-learning-page">
    <header class="page-header">
      <h1 class="page-title">Моё обучение</h1>
      <p class="page-subtitle">Курсы, которые вы проходите или уже завершили.</p>
    </header>

    <div v-if="pending" class="loading">
      <BaseSkeleton height="120px" rounded v-for="i in 3" :key="i" />
    </div>

    <div v-else-if="error" class="error">
      Не удалось загрузить данные.
    </div>

    <template v-else-if="data">
      <!-- В процессе -->
      <section v-if="data.in_progress.length > 0" class="course-group">
        <h2 class="group-title">
          В процессе
          <span class="count">{{ data.in_progress.length }}</span>
        </h2>
        <div class="courses-list">
          <BaseCard
            v-for="item in data.in_progress"
            :key="item.course.id"
            hoverable
            clickable
            :to="`/training/courses/${item.course.slug}`"
            class="course-card"
          >
            <div class="course-cover">
              <img
                v-if="item.course.cover_url"
                :src="mediaUrl(item.course.cover_url)!"
                alt="Обложка"
              />
              <div v-else class="cover-placeholder">
                <i class="fa-solid fa-book-open"></i>
              </div>
            </div>
            <div class="course-info">
              <h3 class="course-title">{{ item.course.title }}</h3>
              <p v-if="item.last_viewed_lesson_title" class="last-lesson">
                Последний урок: {{ item.last_viewed_lesson_title }}
              </p>
              <div class="progress-wrap">
                <div class="progress-bar">
                  <div
                    class="progress-fill"
                    :style="{ width: `${getProgressPercent(item.progress)}%` }"
                  />
                </div>
                <span class="progress-text">{{ getProgressPercent(item.progress) }}%</span>
              </div>
            </div>
          </BaseCard>
        </div>
      </section>

      <!-- Завершённые -->
      <section v-if="data.completed.length > 0" class="course-group">
        <h2 class="group-title">
          Завершённые
          <span class="count">{{ data.completed.length }}</span>
        </h2>
        <div class="courses-list">
          <BaseCard
            v-for="item in data.completed"
            :key="item.course.id"
            hoverable
            clickable
            :to="`/training/courses/${item.course.slug}`"
            class="course-card"
          >
            <div class="course-cover">
              <img
                v-if="item.course.cover_url"
                :src="mediaUrl(item.course.cover_url)!"
                alt="Обложка"
              />
              <div v-else class="cover-placeholder">
                <i class="fa-solid fa-check"></i>
              </div>
            </div>
            <div class="course-info">
              <h3 class="course-title">{{ item.course.title }}</h3>
              <div class="progress-wrap completed">
                <div class="progress-bar">
                  <div class="progress-fill" style="width: 100%" />
                </div>
                <span class="progress-text">100%</span>
              </div>
            </div>
          </BaseCard>
        </div>
      </section>

      <!-- Доступные (не начатые) -->
      <section v-if="data.not_started.length > 0" class="course-group">
        <h2 class="group-title">
          Доступные
          <span class="count">{{ data.not_started.length }}</span>
        </h2>
        <div class="courses-list">
          <BaseCard
            v-for="item in data.not_started"
            :key="item.course.id"
            hoverable
            clickable
            :to="`/training/courses/${item.course.slug}`"
            class="course-card"
          >
            <div class="course-cover">
              <img
                v-if="item.course.cover_url"
                :src="mediaUrl(item.course.cover_url)!"
                alt="Обложка"
              />
              <div v-else class="cover-placeholder">
                <i class="fa-solid fa-play"></i>
              </div>
            </div>
            <div class="course-info">
              <h3 class="course-title">{{ item.course.title }}</h3>
              <div class="progress-wrap">
                <div class="progress-bar">
                  <div class="progress-fill" style="width: 0%" />
                </div>
                <span class="progress-text">0%</span>
              </div>
            </div>
          </BaseCard>
        </div>
      </section>

      <!-- Если вообще ничего нет -->
      <div
        v-if="!data.in_progress.length && !data.completed.length && !data.not_started.length"
        class="empty-state"
      >
        <i class="fa-solid fa-graduation-cap"></i>
        <p>У вас пока нет курсов. Перейдите в каталог, чтобы начать обучение!</p>
        <BaseButton to="/training" variant="primary">В каталог курсов</BaseButton>
      </div>
    </template>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.my-learning-page {
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.page-header {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}
.page-title { font-size: var(--text-2xl); font-weight: var(--fw-bold); }
.page-subtitle { font-size: var(--text-sm); color: var(--color-text-secondary); }

.loading { display: flex; flex-direction: column; gap: var(--space-3); }
.error { padding: var(--space-6); text-align: center; color: var(--color-danger); }

.course-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}
.group-title {
  font-size: var(--text-lg);
  font-weight: var(--fw-semibold);
  display: flex;
  align-items: center;
  gap: var(--space-2);

  .count {
    background: var(--color-surface-secondary);
    padding: 2px 8px;
    border-radius: var(--radius-full);
    font-size: var(--text-xs);
    color: var(--color-text-tertiary);
  }
}

.courses-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.course-card {
  display: flex;
  gap: var(--space-4);
  padding: var(--space-3);
  align-items: center;
  overflow: hidden;
}

.course-cover {
  width: 120px;
  height: 68px;
  border-radius: var(--radius-md);
  overflow: hidden;
  flex-shrink: 0;
  background: var(--color-surface-secondary);

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .cover-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-text-tertiary);
    font-size: 24px;
  }
}

.course-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  min-width: 0;
}

.course-title {
  font-size: var(--text-base);
  font-weight: var(--fw-semibold);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.last-lesson {
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.progress-wrap {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.progress-bar {
  flex: 1;
  height: 6px;
  background: var(--color-surface-secondary);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--color-brand);
  border-radius: var(--radius-full);
  transition: width var(--transition-base);
}

.progress-wrap.completed .progress-fill {
  background: var(--color-success);
}

.progress-text {
  font-size: var(--text-xs);
  font-weight: var(--fw-semibold);
  color: var(--color-brand);
  min-width: 32px;
  text-align: right;
}

.progress-wrap.completed .progress-text {
  color: var(--color-success);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-10);
  text-align: center;
  color: var(--color-text-secondary);
  background: var(--color-surface-secondary);
  border-radius: var(--radius-md);

  i { font-size: 48px; opacity: 0.5; }
}
</style>
