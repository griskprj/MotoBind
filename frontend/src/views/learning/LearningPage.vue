<template>
  <div class="learning-page">
    <div class="container">
      <Header
        title="Обучение"
        subtitle="Курсы, статьи и материалы для мотоциклистов"
      />

      <LearningTabs
        v-if="!hideTabs"
        v-model="activeTab"
        :counts="tabCounts"
      />

      <router-view v-slot="{ Component }">
        <KeepAlive>
          <component :is="Component" />
        </KeepAlive>
      </router-view>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import Header from '@/components/Header.vue'
import LearningTabs from '@/components/learning/LearningTabs.vue'
import { useLearningStore } from '@/stores'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const learningStore = useLearningStore()
const authStore = useAuthStore()

const activeTab = computed({
  get() {
    if (route.name === 'learning-courses' || route.name === 'learning-course' || route.name === 'learning-lesson') {
      return 'courses'
    }
    if (route.name === 'learning-articles' || route.name === 'learning-article') {
      return 'articles'
    }
    if (route.name === 'learning-my') {
      return 'my'
    }
    return 'courses'
  },
  set(value) {
    if (value === 'courses') router.push({ name: 'learning-courses' })
    else if (value === 'articles') router.push({ name: 'learning-articles' })
    else if (value === 'my') router.push({ name: 'learning-my' })
  },
})

const hideTabs = computed(() => {
  return route.meta?.hideParentTabs === true
})

const tabCounts = computed(() => ({
  courses: 0, // можно грузить из store
  articles: 0,
  my: authStore.isAuthenticated ? learningStore.myLearningCounts.inProgress : 0,
}))

onMounted(() => {
  if (authStore.isAuthenticated) {
    learningStore.loadMyLearning().catch(() => {})
  }
})
</script>

<style scoped>
.learning-page {
  width: 100%;
  overflow-x: hidden;
}

.container {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  width: 100%;
  max-width: 100%;
  min-width: 0;
  overflow-x: clip;
}
</style>
