<script setup lang="ts">
import type { CourseShort, ArticleShort } from '~/types'

useSeoMeta({
  title: 'Обучение мотоциклистов',
  description: 'Курсы и статьи по ремонту, обслуживанию и вождению мотоциклов.',
  ogType: 'website',
})

const api = useApi()
const activeTab = ref<'courses' | 'articles'>('courses')
const searchQuery = ref('')
const debouncedSearch = useDebounce(searchQuery, 500)

const coursesData = ref<{ courses: CourseShort[] } | null>(null)
const articlesData = ref<{ articles: ArticleShort[] } | null>(null)
const pending = ref(false)

async function loadData() {
  pending.value = true
  try {
    if (activeTab.value === 'courses') {
      coursesData.value = await api.training.listCourses({ search: debouncedSearch.value || undefined })
    } else {
      articlesData.value = await api.training.listArticles({ search: debouncedSearch.value || undefined })
    }
  } catch (e) {
    console.error(e)
  } finally {
    pending.value = false
  }
}

onMounted(loadData)
watch([activeTab, debouncedSearch], loadData)

const courses = computed(() => coursesData.value?.courses || [])
const articles = computed(() => articlesData.value?.articles || [])
</script>

<template>
  <div class="page-training">
    <header class="page-header">
      <h1 class="page-title">Обучение</h1>
      <p class="page-subtitle">Курсы и статьи для мотоциклистов.</p>
    </header>

    <div class="filters">
      <div class="search-wrap">
        <i class="fa-solid fa-magnifying-glass search-icon"></i>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Поиск..."
          class="search-input"
        />
      </div>

      <div class="tabs">
        <button
          class="tab-btn"
          :class="{ 'tab-btn--active': activeTab === 'courses' }"
          @click="activeTab = 'courses'"
        >
          Курсы
        </button>
        <button
          class="tab-btn"
          :class="{ 'tab-btn--active': activeTab === 'articles' }"
          @click="activeTab = 'articles'"
        >
          Статьи
        </button>
      </div>
    </div>

    <div v-if="pending" class="loading">
      <BaseSkeleton height="200px" rounded v-for="i in 4" :key="i" />
    </div>

    <div v-else-if="activeTab === 'courses'" class="grid">
      <div v-if="courses.length === 0" class="empty">Курсы не найдены.</div>
      <BaseCard
        v-for="course in courses"
        :key="course.id"
        hoverable
        clickable
        :to="`/training/courses/${course.slug}`"
        class="card"
      >
        <div
          class="card-cover"
          :style="course.cover_url ? { backgroundImage: `url(${useMediaUrl()(course.cover_url)})` } : {}"
        />
        <div class="card-content">
          <span v-if="course.level" class="badge">{{ course.level }}</span>
          <h2 class="card-title">{{ course.title }}</h2>
          <p class="card-desc">{{ course.short_description }}</p>
          <div class="card-footer">
            <span v-if="course.lessons_count"><i class="fa-solid fa-book-open"></i> {{ course.lessons_count }} уроков</span>
            <span v-if="course.is_free" class="free">Бесплатно</span>
          </div>
        </div>
      </BaseCard>
    </div>

    <div v-else class="grid">
      <div v-if="articles.length === 0" class="empty">Статьи не найдены.</div>
      <BaseCard
        v-for="article in articles"
        :key="article.id"
        hoverable
        clickable
        :to="`/training/articles/${article.slug}`"
        class="card"
      >
        <div class="card-content">
          <h2 class="card-title">{{ article.title }}</h2>
          <p class="card-desc">{{ article.short_description }}</p>
          <div class="card-footer">
            <span>{{ new Date(article.created_at || '').toLocaleDateString('ru-RU') }}</span>
          </div>
        </div>
      </BaseCard>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.page-training { display: flex; flex-direction: column; gap: var(--space-6); }
.page-title { font-size: var(--text-3xl); font-weight: var(--fw-bold); }
.page-subtitle { color: var(--color-text-secondary); margin-top: var(--space-2); }

.filters {
  display: flex; flex-direction: column; gap: var(--space-4);
  background: var(--color-surface); padding: var(--space-4);
  border-radius: var(--radius-md); border: 1px solid var(--color-border);
  @include md-up { flex-direction: row; align-items: center; justify-content: space-between; }
}

.search-wrap { position: relative; width: 100%; max-width: 400px; }
.search-icon { position: absolute; left: var(--space-3); top: 50%; transform: translateY(-50%); color: var(--color-text-tertiary); }
.search-input {
  width: 100%; padding: var(--space-2) var(--space-3) var(--space-2) var(--space-8);
  border: 1px solid var(--color-border); border-radius: var(--radius-md);
  background: var(--color-surface); color: var(--color-text);
  &:focus { outline: none; border-color: var(--color-brand); box-shadow: var(--shadow-focus); }
}

.tabs { display: flex; gap: var(--space-2); background: var(--color-surface-secondary); padding: 4px; border-radius: var(--radius-md); }
.tab-btn {
  padding: var(--space-2) var(--space-4); border-radius: var(--radius-sm);
  font-size: var(--text-sm); font-weight: var(--fw-medium);
  color: var(--color-text-secondary); transition: all var(--transition-fast);
  border: none; background: transparent; cursor: pointer;
  &--active { background: var(--color-surface); color: var(--color-brand); box-shadow: var(--shadow-sm); }
}

.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: var(--space-4); }
.empty { grid-column: 1 / -1; text-align: center; padding: var(--space-8); color: var(--color-text-secondary); }

.card { display: flex; flex-direction: column; height: 100%; overflow: hidden; }
.card-cover { height: 160px; background: var(--color-surface-secondary); background-size: cover; background-position: center; }
.card-content { padding: var(--space-4); display: flex; flex-direction: column; flex: 1; }
.card-title { font-size: var(--text-lg); font-weight: var(--fw-bold); margin-bottom: var(--space-2); }
.card-desc { font-size: var(--text-sm); color: var(--color-text-secondary); flex: 1; margin-bottom: var(--space-3); }
.card-footer { font-size: var(--text-xs); color: var(--color-text-tertiary); display: flex; gap: var(--space-3); }
.badge { font-size: var(--text-xs); font-weight: var(--fw-semibold); color: var(--color-brand); text-transform: uppercase; margin-bottom: var(--space-2); }
.free { color: var(--color-success); font-weight: var(--fw-semibold); }
.loading { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: var(--space-4); }
</style>
