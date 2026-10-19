<template>
  <div class="my-learning">
    <div class="my-learning__head">
      <h3>Моё обучение</h3>
      <p>Курсы, которые вы проходите или уже завершили</p>
    </div>

    <div v-if="learningStore.myLearningLoading" class="my-learning__loading">
      <i class="fa fa-spinner fa-spin" /> Загрузка...
    </div>

    <template v-else-if="my">
      <!-- В процессе -->
      <section v-if="my.in_progress?.length" class="my-section">
        <h4 class="my-section__title">
          В процессе
          <span class="my-section__badge">{{ my.in_progress.length }}</span>
        </h4>
        <div class="my-list">
          <MyCourseRow
            v-for="item in my.in_progress"
            :key="item.course.id"
            :item="item"
          />
        </div>
      </section>

      <!-- Завершено -->
      <section v-if="my.completed?.length" class="my-section">
        <h4 class="my-section__title">
          Завершено
          <span class="my-section__badge my-section__badge--success">
            {{ my.completed.length }}
          </span>
        </h4>
        <div class="my-list">
          <MyCourseRow
            v-for="item in my.completed"
            :key="item.course.id"
            :item="item"
          />
        </div>
      </section>

      <!-- Не начато -->
      <section v-if="my.not_started?.length" class="my-section">
        <h4 class="my-section__title">
          Доступно
          <span class="my-section__badge my-section__badge--muted">
            {{ my.not_started.length }}
          </span>
        </h4>
        <div class="my-list">
          <MyCourseRow
            v-for="item in my.not_started"
            :key="item.course.id"
            :item="item"
          />
        </div>
      </section>

      <!-- Совсем пусто -->
      <div
        v-if="!my.in_progress?.length && !my.completed?.length && !my.not_started?.length"
        class="empty-state"
      >
        <i class="fa fa-book-open" />
        <p class="empty-text">Пока нет доступных курсов</p>
        <router-link :to="{ name: 'learning-courses' }" class="btn btn-primary">
          Перейти к курсам
        </router-link>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import MyCourseRow from '@/components/learning/MyCourseRow.vue'
import { useLearningStore } from '@/stores'

const learningStore = useLearningStore()
const my = computed(() => learningStore.myLearning)

onMounted(() => {
  learningStore.loadMyLearning().catch(() => {})
})
</script>

<style scoped>
.my-learning {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.my-learning__head h3 {
  margin: 0 0 4px;
  font-size: var(--text-lg);
}

.my-learning__head p {
  margin: 0;
  font-size: var(--text-sm);
  color: var(--text-muted);
}

.my-learning__loading {
  padding: 40px;
  text-align: center;
  color: var(--text-muted);
  font-size: var(--text-sm);
}

.my-section__title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 var(--space-2);
  font-size: var(--text-base);
}

.my-section__badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 22px;
  height: 22px;
  padding: 0 6px;
  border-radius: var(--radius-full);
  background: var(--accent-trans);
  color: var(--accent-text);
  font-size: 11px;
  font-weight: 700;
}

.my-section__badge--success {
  background: var(--success-trans);
  color: var(--success-text);
}

.my-section__badge--muted {
  background: var(--border-light);
  color: var(--text-muted);
}

.my-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
</style>
