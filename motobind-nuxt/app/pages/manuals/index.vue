<script setup lang="ts">
import type { Manual, ManualsListResponse } from '~/types'

useSeoMeta({
  title: 'Мануалы по ремонту мотоциклов',
  description: 'Пошаговые инструкции по обслуживанию и ремонту мотоциклов. Бесплатные руководства от сообщества.',
  ogType: 'website',
})

const api = useApi()
const route = useRoute()
const router = useRouter()

const searchQuery = ref('')
const debouncedSearch = useDebounce(searchQuery, 1000)
const selectedCategory = ref(String(route.query.category || 'all'))
const selectedDifficulty = ref(String(route.query.difficult || 'all'))
const page = ref(Number(route.query.page) || 1)

const manuals = ref<Manual[]>([])
const totalPages = ref(1)
const pending = ref(false)
const error = ref<any>(null)

async function loadManuals() {
  pending.value = true
  error.value = null
  try {
    const res = await api.manuals.list({
      page: page.value,
      per_page: 12,
      search: debouncedSearch.value || undefined,
      category: selectedCategory.value !== 'all' ? selectedCategory.value : undefined,
      difficult: selectedDifficulty.value !== 'all' ? selectedDifficulty.value : undefined,
      tab: 'all',
      status: 'approved',
    })
    manuals.value = res.manuals || []
    totalPages.value = res.pages || 1
  } catch (e) {
    error.value = e
    console.error('Ошибка загрузки мануалов:', e)
  } finally {
    pending.value = false
  }
}

onMounted(loadManuals)
watch([debouncedSearch, page, selectedCategory, selectedDifficulty], loadManuals)

watch([searchQuery, selectedCategory, selectedDifficulty, page], () => {
  router.replace({
    query: {
      ...route.query,
      search: debouncedSearch.value || undefined,
      category: selectedCategory.value !== 'all' ? selectedCategory.value : undefined,
      difficult: selectedDifficulty.value !== 'all' ? selectedDifficulty.value : undefined,
      page: page.value > 1 ? page.value : undefined,
    }
  })
})

const difficultyMap = {
  easy: { label: 'Легко', color: 'var(--color-success)' },
  medium: { label: 'Средне', color: 'var(--color-warning)' },
  hard: { label: 'Сложно', color: 'var(--color-danger)' },
}

const categories = ['all', 'engine', 'drive', 'brakes', 'wheel', 'suspension', 'electronics', 'steering', 'fuel', 'cooling']
</script>

<template>
  <div class="page-manuals">
    <header class="page-header">
      <h1 class="page-title">Мануалы по ремонту</h1>
      <p class="page-subtitle">Пошаговые руководства для самостоятельного обслуживания мотоциклов.</p>

      <div class="header-wrapper">
        <NuxtLink class="link" to="/manual-rules">Правила оформления мануалов</NuxtLink>

        <BaseButton
          size="sm"
          variant="primary"
          to="/manuals/new"
        >
          Добавить мануал
        </BaseButton>
      </div>
    </header>

    <!-- Фильтры -->
    <div class="filters">
      <div class="search-wrap">
        <i class="fa-solid fa-magnifying-glass search-icon"></i>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Поиск по названию, мотоциклу..."
          class="search-input"
        />
      </div>

      <div class="filter-group">
        <select v-model="selectedCategory" class="filter-select">
          <option value="all">Все категории</option>
          <option v-for="cat in categories.filter(c => c !== 'all')" :key="cat" :value="cat">{{ cat }}</option>
        </select>

        <select v-model="selectedDifficulty" class="filter-select">
          <option value="all">Любая сложность</option>
          <option value="easy">Легко</option>
          <option value="medium">Средне</option>
          <option value="hard">Сложно</option>
        </select>
      </div>
    </div>

    <!-- Загрузка / ошибка / пустота -->
    <div v-if="pending" class="loading">
      <BaseSkeleton height="200px" rounded v-for="i in 4" :key="i" />
    </div>
    <div v-else-if="error" class="error">
      <p>Не удалось загрузить мануалы.</p>
      <BaseButton @click="loadManuals()">Повторить</BaseButton>
    </div>
    <div v-else-if="manuals.length === 0" class="empty-state">
      <i class="fa-solid fa-book-open"></i>
      <p>Ничего не найдено. Попробуйте изменить запрос.</p>
    </div>

    <!-- Сетка -->
    <div v-else class="manuals-grid">
      <BaseCard
        v-for="manual in manuals"
        :key="manual.id"
        hoverable
        clickable
        :to="`/manuals/${manual.id}`"
        class="manual-card"
      >
        <div class="card-header">
          <span class="category-badge">{{ manual.category }}</span>
          <span v-if="manual.difficult" class="difficulty" :style="{ color: difficultyMap[manual.difficult as keyof typeof difficultyMap]?.color }">
            <i class="fa-solid fa-signal"></i> {{ difficultyMap[manual.difficult as keyof typeof difficultyMap]?.label }}
          </span>
        </div>
        <h2 class="card-title">{{ manual.title }}</h2>
        <p class="card-desc">{{ manual.description || 'Без описания' }}</p>
        <div class="card-footer">
          <span v-if="manual.time_estimate"><i class="fa-regular fa-clock"></i> {{ manual.time_estimate }}</span>
          <span v-if="manual.steps"><i class="fa-solid fa-list-ol"></i> {{ manual.steps.length }} шагов</span>
          <span v-if="manual.motorcycle"><i class="fa-solid fa-motorcycle"></i> {{ manual.motorcycle }}</span>
        </div>
      </BaseCard>
    </div>

    <!-- Пагинация -->
    <div v-if="totalPages > 1" class="pagination">
      <BaseButton variant="secondary" :disabled="page <= 1" @click="page--">
        <i class="fa-solid fa-chevron-left"></i>
      </BaseButton>
      <span>Страница {{ page }} из {{ totalPages }}</span>
      <BaseButton variant="secondary" :disabled="page >= totalPages" @click="page++">
        <i class="fa-solid fa-chevron-right"></i>
      </BaseButton>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.link {
  color: var(--color-brand);
}

.page-manuals {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.page-header {
  margin-bottom: var(--space-2);
}
.header-wrapper {
  display: flex;
  justify-content: space-between;
  margin-top: var(--space-4);
  flex-wrap: wrap;
  gap: 8px;
}
.page-title {
  font-size: var(--text-3xl);
  font-weight: var(--fw-bold);
}
.page-subtitle {
  font-size: var(--text-base);
  color: var(--color-text-secondary);
  margin-top: var(--space-2);
}

/* Фильтры */
.filters {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  background: var(--color-surface);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);

  @include md-up {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}
.filter-group {
  display: flex;
  gap: var(--space-2);
}
.filter-select {
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text);
}

.search-wrap {
  position: relative;
  width: 100%;
  max-width: 400px;
}
.search-icon {
  position: absolute;
  left: var(--space-3);
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-tertiary);
}
.search-input {
  width: 100%;
  padding: var(--space-2) var(--space-3) var(--space-2) var(--space-8);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text);
  font-size: var(--text-sm);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);

  &:focus {
    outline: none;
    border-color: var(--color-brand);
    box-shadow: var(--shadow-focus);
  }
}

.categories {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}
.cat-btn {
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  background: var(--color-surface-secondary);
  color: var(--color-text-secondary);
  border: 1px solid transparent;
  cursor: pointer;
  transition: all var(--transition-fast);

  &:hover { background: var(--color-surface-hover); }
  &--active {
    background: var(--color-brand-soft);
    color: var(--color-brand);
    border-color: var(--color-brand);
  }
}

/* Сетка */
.manuals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--space-4);
}

.manual-card {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-3);
}
.category-badge {
  font-size: var(--text-xs);
  font-weight: var(--fw-semibold);
  color: var(--color-brand);
  text-transform: uppercase;
}
.difficulty {
  font-size: var(--text-xs);
  font-weight: var(--fw-medium);
  display: flex;
  align-items: center;
  gap: 4px;
}

.card-title {
  font-size: var(--text-lg);
  font-weight: var(--fw-bold);
  color: var(--color-text);
  margin-bottom: var(--space-2);
  line-height: var(--leading-tight);
}
.card-desc {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-4);
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  gap: var(--space-4);
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
  border-top: 1px solid var(--color-border-light);
  padding-top: var(--space-3);

  span {
    display: flex;
    align-items: center;
    gap: 4px;
  }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-10);
  color: var(--color-text-tertiary);

  i { font-size: 48px; opacity: 0.5; }
}

@media (max-width: 380px) {
  .filter-group {
    flex-direction: column;
  }
}
</style>
