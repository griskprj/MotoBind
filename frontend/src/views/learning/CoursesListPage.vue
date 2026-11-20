<template>
  <div class="courses-list">
    <div class="courses-list__head">
      <h3>Курсы</h3>
      <p>Структурированные курсы для уверенного владения мотоциклом</p>
    </div>

    <CourseFilters
      :filters="learningStore.courseFilters"
      @change="onFiltersChange"
    />

    <div v-if="learningStore.coursesLoading" class="courses-list__loading">
      <i class="fa fa-spinner fa-spin" /> Загрузка...
    </div>

    <div
      v-else-if="!learningStore.hasCourses"
      class="empty-state"
    >
      <i class="fa fa-graduation-cap" />
      <p class="empty-text">Курсов пока нет</p>
    </div>

    <div v-else class="courses-list__grid">
      <CourseCard
        v-for="c in learningStore.courses"
        :key="c.id"
        :course="c"
      />
    </div>

    <BasePagination
      v-if="learningStore.coursesPagination?.pages > 1"
      :pagination="learningStore.coursesPagination"
      @change="onPageChange"
    />
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import CourseCard from '@/components/learning/CourseCard.vue'
import CourseFilters from '@/components/learning/CourseFilters.vue'
import BasePagination from '@/components/learning/BasePagination.vue'
import { useLearningStore } from '@/stores'

const learningStore = useLearningStore()
const page = ref(1)

onMounted(() => {
  load()
})

watch(
  () => learningStore.courseFilters,
  () => {
    page.value = 1
    load()
  },
  { deep: true }
)

function load() {
  learningStore.loadCourses({ page: page.value, per_page: 12 }).catch(() => {})
}

function onFiltersChange(newFilters) {
  learningStore.courseFilters = { ...learningStore.courseFilters, ...newFilters }
}

function onPageChange(newPage) {
  page.value = newPage
  load()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<style scoped>
.courses-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.courses-list__head h3 {
  margin: 0 0 4px;
  font-size: var(--text-lg);
}

.courses-list__head p {
  margin: 0;
  font-size: var(--text-sm);
  color: var(--text-muted);
}

.courses-list__loading {
  padding: 40px;
  text-align: center;
  color: var(--text-muted);
  font-size: var(--text-sm);
}

.courses-list__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: var(--space-3);
}

@media (max-width: 640px) {
  .courses-list__grid {
    grid-template-columns: 1fr;
  }
}
</style>
