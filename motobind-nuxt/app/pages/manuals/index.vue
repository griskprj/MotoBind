<script setup lang="ts">
import type { Manual } from '~/types'

useSeoMeta({
  title: 'Мануалы по ремонту мотоциклов',
  description: 'Пошаговые инструкции по обслуживанию и ремонту мотоциклов. Бесплатные руководства от сообщества.',
  ogType: 'website',
})

const api = useApi()
const route = useRoute()
const router = useRouter()

// --- Состояние фильтров ---
const searchQuery = ref(String(route.query.search || ''))
const debouncedSearch = useDebounce(searchQuery, 500)
const selectedCategory = ref(String(route.query.category || 'all'))
const selectedDifficulty = ref(String(route.query.difficult || 'all'))
const selectedDuration = ref(String(route.query.duration || 'all'))
const selectedModel = ref(String(route.query.model || 'all'))
const page = ref(Number(route.query.page) || 1)

const manuals = ref<Manual[]>([])
const totalPages = ref(1)
const pending = ref(false)
const error = ref<any>(null)

// --- Загрузка данных ---
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
      // Если на бэкенде есть фильтры по длительности или модели — раскомментируйте:
      // duration: selectedDuration.value !== 'all' ? selectedDuration.value : undefined,
      // model: selectedModel.value !== 'all' ? selectedModel.value : undefined,
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

// Следим за изменениями (дебаунс для поиска)
watch([debouncedSearch, page, selectedCategory, selectedDifficulty, selectedDuration, selectedModel], () => {
  page.value = 1 // Сбрасываем страницу при смене фильтров
  loadManuals()
})

// Синхронизация с URL
watch([debouncedSearch, selectedCategory, selectedDifficulty, selectedDuration, selectedModel, page], () => {
  router.replace({
    query: {
      ...route.query,
      search: debouncedSearch.value || undefined,
      category: selectedCategory.value !== 'all' ? selectedCategory.value : undefined,
      difficult: selectedDifficulty.value !== 'all' ? selectedDifficulty.value : undefined,
      duration: selectedDuration.value !== 'all' ? selectedDuration.value : undefined,
      model: selectedModel.value !== 'all' ? selectedModel.value : undefined,
      page: page.value > 1 ? page.value : undefined,
    }
  })
})

// --- Константы ---
const tabs = [
  { id: 'all', label: 'Все мануалы', icon: 'fa-solid fa-border-all' },
  { id: 'engine', label: 'Двигатель', icon: 'fa-solid fa-gear' },
  { id: 'drive', label: 'Трансмиссия', icon: 'fa-solid fa-link' },
  { id: 'brakes', label: 'Тормоза', icon: 'fa-solid fa-hand' },
  { id: 'electronics', label: 'Электрика', icon: 'fa-solid fa-bolt' },
  { id: 'maintenance', label: 'ТО', icon: 'fa-solid fa-wrench' },
]

const difficultyMap = {
  easy: { label: 'Легко', color: 'var(--color-success)', icon: 'fa-solid fa-signal' },
  medium: { label: 'Средне', color: 'var(--color-warning)', icon: 'fa-solid fa-signal' },
  hard: { label: 'Сложно', color: 'var(--color-danger)', icon: 'fa-solid fa-signal' },
}

const modelOptions = [
  { value: 'all', label: 'Модель мотоцикла' },
  { value: 'bajaj', label: 'Bajaj Pulsar NS 125' },
  { value: 'yamaha', label: 'Yamaha MT-07' },
]

const durationOptions = [
  { value: 'all', label: 'Длительность' },
  { value: '15', label: 'До 15 мин' },
  { value: '30', label: 'До 30 мин' },
  { value: '60', label: 'До 1 часа' },
]
</script>

<template>
  <div class="manuals-page">
    <!-- Заголовок -->
    <header class="page-header">
      <div>
        <h1 class="page-title">Мануалы по ремонту</h1>
        <p class="page-subtitle">Пошаговые руководства для самостоятельного обслуживания мотоциклов.</p>
      </div>
      <BaseButton size="md" variant="primary" to="/manuals/new">
        <template #icon><i class="fa-solid fa-plus"></i></template>
        Добавить мануал
      </BaseButton>
    </header>

    <!-- Табы категорий -->
    <div class="category-tabs">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        class="cat-tab"
        :class="{ 'cat-tab--active': selectedCategory === tab.id }"
        @click="selectedCategory = tab.id"
      >
        <i :class="tab.icon"></i>
        {{ tab.label }}
      </button>
    </div>

    <!-- Панель фильтров -->
    <div class="filters-panel">
      <div class="search-wrap">
        <i class="fa-solid fa-magnifying-glass search-icon"></i>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Поиск по названию, описанию..."
          class="search-input"
        />
      </div>

      <div class="filters-group">
        <select v-model="selectedModel" class="filter-select">
          <option v-for="opt in modelOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
        </select>

        <select v-model="selectedDifficulty" class="filter-select">
          <option value="all">Сложность</option>
          <option value="easy">Легко</option>
          <option value="medium">Средне</option>
          <option value="hard">Сложно</option>
        </select>

        <select v-model="selectedDuration" class="filter-select">
          <option v-for="opt in durationOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
        </select>
      </div>
    </div>

    <!-- Состояния -->
    <div v-if="pending" class="loading-grid">
      <BaseSkeleton height="320px" rounded v-for="i in 4" :key="i" />
    </div>
    <div v-else-if="error" class="error-state">
      <i class="fa-solid fa-triangle-exclamation"></i>
      <p>Не удалось загрузить мануалы.</p>
      <BaseButton @click="loadManuals()">Повторить</BaseButton>
    </div>
    <div v-else-if="manuals.length === 0" class="empty-state">
      <i class="fa-solid fa-book-open"></i>
      <p>Ничего не найдено. Попробуйте изменить запрос.</p>
    </div>

    <!-- Сетка карточек -->
    <div v-else class="manuals-grid">
      <div
        v-for="manual in manuals"
        :key="manual.id"
        class="manual-card"
        @click="router.push(`/manuals/${manual.id}`)"
      >
        <!-- Обложка карточки -->
        <div class="card-cover">
          <span class="cover-badge">{{ manual.category }}</span>
          <img
            v-if="manual.image_url"
            :src="manual.image_url"
            :alt="manual.title"
            class="cover-img"
          />
          <div v-else class="cover-placeholder">
            <i class="fa-solid fa-motorcycle"></i>
          </div>
        </div>

        <!-- Контент карточки -->
        <div class="card-content">
          <h2 class="card-title">{{ manual.title }}</h2>
          <p class="card-desc">{{ manual.description || 'Без описания' }}</p>

          <!-- Мета-данные -->
          <div class="card-meta">
            <span class="meta-item difficulty" :style="{ color: difficultyMap[manual.difficult as keyof typeof difficultyMap]?.color || 'var(--color-text-secondary)' }">
              <i :class="difficultyMap[manual.difficult as keyof typeof difficultyMap]?.icon || 'fa-solid fa-signal'"></i>
              {{ difficultyMap[manual.difficult as keyof typeof difficultyMap]?.label || 'Любая' }}
            </span>
            <span class="meta-item" v-if="manual.time_estimate">
              <i class="fa-regular fa-clock"></i> {{ manual.time_estimate }}
            </span>
            <span class="meta-item" v-if="manual.steps">
              <i class="fa-solid fa-list-ol"></i> {{ manual.steps.length }} шагов
            </span>
          </div>

          <!-- Кнопка -->
          <div class="card-footer">
            <BaseButton class="open-btn" variant="secondary" @click.stop="router.push(`/manuals/${manual.id}`)">
              Открыть руководство <i class="fa-solid fa-arrow-right"></i>
            </BaseButton>
          </div>
        </div>
      </div>
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

.manuals-page {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

/* Заголовок */
.page-header {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);

  @include sm-up {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}

.page-title {
  font-size: var(--text-3xl);
  font-weight: var(--fw-bold);
}

.page-subtitle {
  font-size: var(--text-base);
  color: var(--color-text-secondary);
  margin-top: var(--space-1);
}

/* Баннер */
.promo-banner {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  padding: var(--space-6);
  background: linear-gradient(135deg, rgba(112, 0, 255, 0.15) 0%, rgba(30, 30, 40, 0.6) 100%);
  border: 1px solid rgba(112, 0, 255, 0.3);
  border-radius: var(--radius-lg);
  overflow: hidden;

  @include md-up {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}

.promo-content {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  position: relative;
  z-index: 2;
}

.promo-icon {
  width: 56px;
  height: 56px;
  background: rgba(112, 0, 255, 0.2);
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-brand);
  font-size: 24px;
  flex-shrink: 0;
}

.promo-label {
  display: inline-block;
  font-size: 10px;
  font-weight: var(--fw-bold);
  color: var(--color-brand);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: var(--space-1);
}

.promo-title {
  font-size: var(--text-xl);
  font-weight: var(--fw-bold);
  color: var(--color-text);
  margin-bottom: var(--space-1);
}

.promo-desc {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  max-width: 600px;
}

.promo-actions {
  position: relative;
  z-index: 2;
  flex-shrink: 0;
}

.promo-bg {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 50%;
  background-image: url('https://www.transparentpng.com/thumb/motorcycle/Pulse-Motorcycle-PNG-Image.png');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: right center;
  opacity: 0.1;
  pointer-events: none;
  z-index: 1;
}

/* Табы */
.category-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  padding: var(--space-2);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow-x: auto;

  @include md-up {
    flex-wrap: nowrap;
  }
}

.cat-tab {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  color: var(--color-text-secondary);
  background: transparent;
  border: none;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;

  i {
    color: var(--color-text-tertiary);
    transition: color 0.2s;
  }

  &:hover {
    background: var(--color-surface-secondary);
    color: var(--color-text);
  }

  &--active {
    background: rgba(112, 0, 255, 0.15);
    color: var(--color-brand);

    i {
      color: var(--color-brand);
    }
  }
}

/* Фильтры */
.filters-panel {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  background: var(--color-surface);
  padding: var(--space-3);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);

  @include lg-up {
    flex-direction: row;
    align-items: center;
  }
}

.search-wrap {
  position: relative;
  flex: 1;
  min-width: 250px;
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
  background: var(--color-surface-secondary);
  color: var(--color-text);
  font-size: var(--text-sm);
  transition: border-color 0.2s;

  &:focus {
    outline: none;
    border-color: var(--color-brand);
  }
}

.filters-group {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);

  @include lg-up {
    flex-wrap: nowrap;
  }
}

.filter-select {
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface-secondary);
  color: var(--color-text);
  font-size: var(--text-sm);
  cursor: pointer;
  min-width: 140px;

  &:focus {
    outline: none;
    border-color: var(--color-brand);
  }
}

/* Сетка */
.manuals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-4);
}

.loading-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-4);
}

/* Карточка */
.manual-card {
  display: flex;
  flex-direction: column;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;

  .open-btn {
    width: 100%;
  }

  &:hover {
    border-color: rgba(112, 0, 255, 0.4);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  }
}

/* Обложка */
.card-cover {
  position: relative;
  height: 160px;
  background: linear-gradient(135deg, rgba(112, 0, 255, 0.1), rgba(30, 30, 40, 0.8));
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.cover-badge {
  position: absolute;
  top: var(--space-3);
  left: var(--space-3);
  font-size: 10px;
  font-weight: var(--fw-bold);
  text-transform: uppercase;
  color: #fff;
  background: rgba(112, 0, 255, 0.8);
  padding: 4px 10px;
  border-radius: var(--radius-full);
  z-index: 2;
}

.cover-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-placeholder {
  font-size: 48px;
  color: rgba(255, 255, 255, 0.1);
}

/* Контент карточки */
.card-content {
  display: flex;
  flex-direction: column;
  padding: var(--space-4);
  flex: 1;
}

.card-title {
  font-size: var(--text-lg);
  font-weight: var(--fw-bold);
  color: var(--color-text);
  margin-bottom: var(--space-2);
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-desc {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-4);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

/* Мета-данные */
.card-meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);

  i {
    font-size: 12px;
  }
}

.meta-item.difficulty {
  font-weight: var(--fw-medium);
}

/* Футер */
.card-footer {
  margin-top: auto;
}

/* Состояния */
.error-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-10);
  text-align: center;
  color: var(--color-text-tertiary);

  i { font-size: 48px; opacity: 0.5; }
}

/* Пагинация */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--space-4);
  margin-top: var(--space-4);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}
</style>
