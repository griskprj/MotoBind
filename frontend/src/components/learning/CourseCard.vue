<template>
  <router-link
    :to="{ name: 'learning-course', params: { slug: course.slug } }"
    class="course-card"
  >
    <div class="course-card__cover">
      <img
        v-if="course.cover_url"
        :src="getUploadUrl(course.cover_url)"
        :alt="course.title"
        loading="lazy"
      />
      <div v-else class="course-card__cover-placeholder">
        <i class="fa fa-graduation-cap" />
      </div>
      <span v-if="course.is_free" class="course-card__badge course-card__badge--free">
        Бесплатно
      </span>
      <span v-else class="course-card__badge course-card__badge--paid">
        {{ formatPrice(course.price) }}
      </span>
      <span v-if="course.is_purchased" class="course-card__badge course-card__badge--owned">
        <i class="fa fa-check" /> Куплено
      </span>
    </div>
    <div class="course-card__body">
      <div class="course-card__category">
        {{ categoryLabel(course.category) }}
      </div>
      <div class="course-card__title">{{ course.title }}</div>
      <div v-if="course.short_description" class="course-card__desc">
        {{ course.short_description }}
      </div>
      <div class="course-card__meta">
        <span class="course-card__meta-item">
          <i class="fa fa-book-open" />
          {{ course.lessons_count }} {{ pluralLessons(course.lessons_count) }}
        </span>
        <span class="course-card__meta-item">
          {{ levelLabel(course.level) }}
        </span>
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { getUploadUrl } from '@/utils/mediaUrl'

const props = defineProps({
  course: { type: Object, required: true },
})

function categoryLabel(category) {
  const map = {
    riding: 'Вождение',
    repair: 'Ремонт',
    gear: 'Экипировка',
    first_aid: 'Первая помощь',
    law: 'Право',
    travel: 'Путешествия',
  }
  return map[category] || category
}

function levelLabel(level) {
  const map = {
    beginner: 'Начальный',
    intermediate: 'Средний',
    advanced: 'Продвинутый',
  }
  return map[level] || level
}

function formatPrice(price) {
  if (!price) return '0 ₽'
  return `${Math.floor(price / 100)} ₽`
}

function pluralLessons(n) {
  if (n % 10 === 1 && n % 100 !== 11) return 'урок'
  if ([2, 3, 4].includes(n % 10) && ![12, 13, 14].includes(n % 100)) return 'урока'
  return 'уроков'
}
</script>

<style scoped>
.course-card {
  display: flex;
  flex-direction: column;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  overflow: hidden;
  text-decoration: none;
  color: inherit;
  transition: all var(--transition-base);
  height: 100%;
}

.course-card:hover {
  transform: translateY(-2px);
  border-color: var(--accent);
  box-shadow: var(--shadow-md);
}

.course-card__cover {
  position: relative;
  aspect-ratio: 16 / 9;
  background: var(--bg-secondary);
  overflow: hidden;
}

.course-card__cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.course-card__cover-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
  font-size: 48px;
  opacity: 0.4;
}

.course-card__badge {
  position: absolute;
  top: 10px;
  left: 10px;
  padding: 4px 10px;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: var(--fw-semibold);
  backdrop-filter: blur(4px);
}

.course-card__badge--free {
  background: var(--success);
  color: #fff;
}

.course-card__badge--paid {
  background: var(--accent);
  color: #fff;
}

.course-card__badge--owned {
  top: auto;
  bottom: 10px;
  left: 10px;
  background: var(--success);
  color: #fff;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.course-card__body {
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
}

.course-card__category {
  font-size: 11px;
  font-weight: var(--fw-semibold);
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: var(--accent-text);
}

.course-card__title {
  font-size: var(--text-base);
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
  line-height: var(--leading-tight);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.course-card__desc {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: var(--leading-base);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.course-card__meta {
  display: flex;
  gap: 12px;
  margin-top: auto;
  padding-top: 8px;
  font-size: var(--text-xs);
  color: var(--text-muted);
}

.course-card__meta-item {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.course-card__meta-item i {
  font-size: 11px;
}
</style>
