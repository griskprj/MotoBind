<template>
  <router-link
    :to="{ name: 'learning-course', params: { slug: item.course.slug } }"
    class="my-course"
  >
    <div class="my-course__cover">
      <img
        v-if="item.course.cover_url"
        :src="resolveMedia(item.course.cover_url)"
        :alt="item.course.title"
      />
      <div v-else class="my-course__cover-placeholder">
        <i class="fa fa-graduation-cap" />
      </div>
    </div>

    <div class="my-course__body">
      <div class="my-course__title">{{ item.course.title }}</div>
      <div class="my-course__progress-text">
        {{ item.progress.completed }} из {{ item.progress.total }} уроков
        <template v-if="item.last_viewed_lesson_title">
          · Последний: {{ item.last_viewed_lesson_title }}
        </template>
      </div>
      <div class="my-course__progress-bar">
        <div
          class="my-course__progress-fill"
          :style="{ width: `${percent}%` }"
        />
      </div>
    </div>

    <div class="my-course__pct">{{ percent }}%</div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'
import { resolveMedia } from '@/utils/mediaUrl'

const props = defineProps({
  item: { type: Object, required: true },
})

const percent = computed(() => {
  const p = props.item.progress
  if (!p || !p.total) return 0
  return Math.round((p.completed / p.total) * 100)
})
</script>

<style scoped>
.my-course {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  text-decoration: none;
  color: inherit;
  transition: all var(--transition-base);
}

.my-course:hover {
  border-color: var(--accent);
  background: var(--bg-card-hover);
}

.my-course__cover {
  width: 80px;
  height: 56px;
  flex-shrink: 0;
  border-radius: var(--radius-sm);
  overflow: hidden;
  background: var(--bg-primary);
}

.my-course__cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.my-course__cover-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
  opacity: 0.4;
  font-size: 20px;
}

.my-course__body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.my-course__title {
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
  overflow: hidden;
}

.my-course__progress-text {
  font-size: var(--text-xs);
  color: var(--text-muted);
  overflow: hidden;
}

.my-course__progress-bar {
  height: 4px;
  background: var(--border-light);
  border-radius: 2px;
  overflow: hidden;
  margin-top: 4px;
}

.my-course__progress-fill {
  height: 100%;
  background: var(--accent);
  transition: width var(--transition-base);
}

.my-course__pct {
  font-size: var(--text-sm);
  font-weight: var(--fw-bold);
  color: var(--accent-text);
  flex-shrink: 0;
  min-width: 44px;
  text-align: right;
}

@media (max-width: 640px) {
  .my-course__pct {
    font-size: var(--text-xs);
  }
}

@media (max-width: 420px) {
  .my-course {
    flex-direction: column
  }

  .my-course__cover {
    display: block;
    margin: 0 auto;
    width: 100%;
    height: 128px;
  }
}
</style>
