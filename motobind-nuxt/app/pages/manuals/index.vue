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

const searchQuery = ref(String(route.query.search || ''))
const debouncedSearch = useDebounce(searchQuery, 500)
const selectedCategory = ref(String(route.query.category || 'all'))
const selectedDifficulty = ref(String(route.query.difficult || 'all'))
const page = ref(Math.max(1, Number(route.query.page) || 1))

const manuals = ref<Manual[]>([])
const totalPages = ref(1)
const pending = ref(false)
const error = ref<unknown>(null)

let requestId = 0

const tabs = [
  { id: 'all', label: 'Все мануалы', icon: 'fa-solid fa-border-all' },
  { id: 'engine', label: 'Двигатель', icon: 'fa-solid fa-gear' },
  { id: 'drive', label: 'Трансмиссия', icon: 'fa-solid fa-link' },
  { id: 'brakes', label: 'Тормоза', icon: 'fa-solid fa-hand' },
  { id: 'electronics', label: 'Электрика', icon: 'fa-solid fa-bolt' },
  { id: 'maintenance', label: 'ТО', icon: 'fa-solid fa-wrench' },
]

const difficultyOptions = [
  { value: 'all', label: 'Любая сложность' },
  { value: 'easy', label: 'Лёгкая' },
  { value: 'medium', label: 'Средняя' },
  { value: 'hard', label: 'Высокая' },
]

const difficultyMap = {
  easy: { label: 'Лёгкая', variant: 'success' as const },
  medium: { label: 'Средняя', variant: 'warning' as const },
  hard: { label: 'Высокая', variant: 'danger' as const },
}

const activeFiltersCount = computed(() => [
  selectedCategory.value !== 'all',
  selectedDifficulty.value !== 'all',
  Boolean(debouncedSearch.value),
].filter(Boolean).length)

async function loadManuals() {
  const currentRequest = ++requestId
  pending.value = true
  error.value = null

  try {
    const response = await api.manuals.list({
      page: page.value,
      per_page: 12,
      search: debouncedSearch.value || undefined,
      category: selectedCategory.value !== 'all' ? selectedCategory.value : undefined,
      difficult: selectedDifficulty.value !== 'all' ? selectedDifficulty.value : undefined,
      tab: 'all',
      status: 'approved',
    })

    if (currentRequest !== requestId) return
    manuals.value = response.manuals || []
    totalPages.value = response.pages || 1
  } catch (err) {
    if (currentRequest !== requestId) return
    error.value = err
    console.error('Ошибка загрузки мануалов:', err)
  } finally {
    if (currentRequest === requestId) pending.value = false
  }
}

function resetFilters() {
  searchQuery.value = ''
  selectedCategory.value = 'all'
  selectedDifficulty.value = 'all'
  page.value = 1
}

function selectCategory(category: string) {
  if (selectedCategory.value === category) return
  selectedCategory.value = category
}

function openManual(manual: Manual) {
  router.push(`/manuals/${manual.id}`)
}

watch([debouncedSearch, selectedCategory, selectedDifficulty], () => {
  if (page.value !== 1) {
    page.value = 1
    return
  }
  loadManuals()
})

watch(page, () => loadManuals())

watch(
  [debouncedSearch, selectedCategory, selectedDifficulty, page],
  () => {
    router.replace({
      query: {
        ...route.query,
        search: debouncedSearch.value || undefined,
        category: selectedCategory.value !== 'all' ? selectedCategory.value : undefined,
        difficult: selectedDifficulty.value !== 'all' ? selectedDifficulty.value : undefined,
        page: page.value > 1 ? String(page.value) : undefined,
      },
    })
  },
)

onMounted(loadManuals)
</script>

<template>
  <main class="manuals-page">
    <header class="page-header">
      <div class="page-heading">
        <div class="eyebrow">
          <i class="fa-solid fa-book-open" aria-hidden="true" />
          БАЗА ЗНАНИЙ MOTOBIND
        </div>
        <h1 class="page-title">Мануалы</h1>
        <p class="page-subtitle">
          Проверенные руководства по обслуживанию, диагностике и ремонту мотоциклов.
        </p>
      </div>

      <BaseButton to="/manuals/new" size="md">
        <template #icon><i class="fa-solid fa-plus" aria-hidden="true" /></template>
        Предложить мануал
      </BaseButton>
    </header>

    <section class="bike-panel" aria-labelledby="bike-panel-title">
      <div class="bike-panel__copy">
        <BaseBadge variant="brand" size="sm">ПЕРСОНАЛЬНЫЙ ПОДБОР</BaseBadge>
        <h2 id="bike-panel-title">Мануалы для твоего мотоцикла</h2>
        <p>Найди руководства, подходящие именно для твоей модели.</p>
        <BaseButton to="/garage" variant="secondary" size="sm">
          <template #icon><i class="fa-solid fa-motorcycle" aria-hidden="true" /></template>
          Открыть гараж
          <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true" />
        </BaseButton>
      </div>
      <div class="bike-panel__art" aria-hidden="true">
        <i class="fa-solid fa-motorcycle" />
      </div>
      <div class="bike-panel__glow" aria-hidden="true" />
    </section>

    <nav class="category-tabs" aria-label="Категории мануалов">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        type="button"
        class="category-tab"
        :class="{ 'category-tab--active': selectedCategory === tab.id }"
        :aria-pressed="selectedCategory === tab.id"
        @click="selectCategory(tab.id)"
      >
        <i :class="tab.icon" aria-hidden="true" />
        <span>{{ tab.label }}</span>
      </button>
    </nav>

    <section class="catalog-section" aria-labelledby="catalog-title">
      <div class="catalog-heading">
        <div>
          <div class="section-title">
            <span class="section-title__icon"><i class="fa-solid fa-layer-group" aria-hidden="true" /></span>
            <h2 id="catalog-title">Все руководства</h2>
          </div>
          <p class="section-description">
            Практические инструкции, которые помогут разобраться и выполнить работу самостоятельно.
          </p>
        </div>
        <BaseButton
          v-if="activeFiltersCount"
          variant="ghost"
          size="sm"
          @click="resetFilters"
        >
          <template #icon><i class="fa-solid fa-rotate-left" aria-hidden="true" /></template>
          Сбросить
          <BaseBadge variant="brand" size="sm">{{ activeFiltersCount }}</BaseBadge>
        </BaseButton>
      </div>

      <div class="filters-panel">
        <div class="search-control">
          <i class="fa-solid fa-magnifying-glass" aria-hidden="true" />
          <BaseInput
            v-model="searchQuery"
            type="search"
            placeholder="Поиск по названию или описанию..."
            aria-label="Поиск мануалов"
          />
        </div>
        <div class="difficulty-control">
          <BaseSelect
            v-model="selectedDifficulty"
            :options="difficultyOptions"
            aria-label="Фильтр по сложности"
          />
        </div>
      </div>

      <div v-if="pending" class="manuals-grid" aria-label="Загрузка мануалов">
        <article v-for="item in 8" :key="item" class="manual-card manual-card--skeleton">
          <BaseSkeleton height="176px" rounded />
          <div class="manual-card__body">
            <BaseSkeleton height="20px" width="78%" />
            <BaseSkeleton height="14px" width="100%" />
            <BaseSkeleton height="14px" width="64%" />
            <BaseSkeleton height="36px" width="100%" rounded />
          </div>
        </article>
      </div>

      <div v-else-if="error" class="state-panel">
        <BaseEmptyState
          title="Не удалось загрузить мануалы"
          description="Проверь соединение и попробуй загрузить каталог ещё раз."
        >
          <template #icon><i class="fa-solid fa-triangle-exclamation" /></template>
          <template #action>
            <BaseButton @click="loadManuals">
              <template #icon><i class="fa-solid fa-rotate-right" /></template>
              Повторить
            </BaseButton>
          </template>
        </BaseEmptyState>
      </div>

      <div v-else-if="manuals.length === 0" class="state-panel">
        <BaseEmptyState
          title="Ничего не найдено"
          description="Попробуй изменить поисковый запрос или сбросить фильтры."
        >
          <template #icon><i class="fa-solid fa-book-open" /></template>
          <template #action>
            <BaseButton variant="secondary" @click="resetFilters">Сбросить фильтры</BaseButton>
          </template>
        </BaseEmptyState>
      </div>

      <div v-else class="manuals-grid">
        <article
          v-for="manual in manuals"
          :key="manual.id"
          class="manual-card"
          role="link"
          tabindex="0"
          @click="openManual(manual)"
          @keydown.enter="openManual(manual)"
          @keydown.space.prevent="openManual(manual)"
        >
          <div class="manual-card__cover">
            <img
              v-if="manual.image_url"
              :src="manual.image_url"
              :alt="manual.title"
              class="manual-card__image"
              loading="lazy"
            />
            <div v-else class="manual-card__placeholder">
              <i class="fa-solid fa-motorcycle" aria-hidden="true" />
              <span>Изображение не добавлено</span>
            </div>
            <div class="manual-card__badges">
              <BaseBadge variant="brand" size="sm">{{ manual.category }}</BaseBadge>
              <BaseBadge variant="success" size="sm" dot>Проверен</BaseBadge>
            </div>
          </div>

          <div class="manual-card__body">
            <h3 class="manual-card__title">{{ manual.title }}</h3>
            <p class="manual-card__description">
              {{ manual.description || 'Подробное руководство по выполнению процедуры.' }}
            </p>

            <div class="manual-card__meta">
              <BaseBadge
                v-if="difficultyMap[manual.difficult as keyof typeof difficultyMap]"
                :variant="difficultyMap[manual.difficult as keyof typeof difficultyMap].variant"
                size="sm"
              >
                {{ difficultyMap[manual.difficult as keyof typeof difficultyMap].label }}
              </BaseBadge>
              <span v-else class="meta-item">Сложность не указана</span>
              <span v-if="manual.time_estimate" class="meta-item">
                <i class="fa-regular fa-clock" aria-hidden="true" />
                {{ manual.time_estimate }}
              </span>
              <span v-if="manual.steps?.length" class="meta-item">
                <i class="fa-solid fa-list-ol" aria-hidden="true" />
                {{ manual.steps.length }} этапов
              </span>
            </div>

            <div class="manual-card__footer">
              <span>Открыть руководство</span>
              <i class="fa-solid fa-arrow-right" aria-hidden="true" />
            </div>
          </div>
        </article>
      </div>

      <div v-if="!pending && !error && manuals.length > 0 && totalPages > 1" class="pagination">
        <BaseButton
          variant="secondary"
          size="sm"
          :disabled="page <= 1"
          aria-label="Предыдущая страница"
          @click="page--"
        >
          <i class="fa-solid fa-chevron-left" aria-hidden="true" />
        </BaseButton>
        <span>Страница <strong>{{ page }}</strong> из {{ totalPages }}</span>
        <BaseButton
          variant="secondary"
          size="sm"
          :disabled="page >= totalPages"
          aria-label="Следующая страница"
          @click="page++"
        >
          <i class="fa-solid fa-chevron-right" aria-hidden="true" />
        </BaseButton>
      </div>
    </section>
  </main>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.manuals-page {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
  width: 100%;
  max-width: 1400px;
  min-width: 0;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: var(--space-4);
  flex-wrap: wrap;
}

.page-heading { min-width: 0; }

.eyebrow {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-2);
  color: var(--color-brand);
  font-size: var(--text-xs);
  font-weight: var(--fw-bold);
  letter-spacing: .08em;
}

.page-title {
  margin: 0;
  color: var(--color-text);
  font-size: var(--text-3xl);
  font-weight: var(--fw-bold);
  line-height: var(--leading-tight);
}

.page-subtitle {
  max-width: 680px;
  margin: var(--space-2) 0 0;
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  line-height: var(--leading-relaxed);
}

/* Персональный блок */
.bike-panel {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 174px;
  padding: var(--space-5) var(--space-6);
  overflow: hidden;
  isolation: isolate;
  border: 1px solid color-mix(in srgb, var(--color-brand) 30%, var(--color-border));
  border-radius: var(--radius-xl);
  background: var(--color-surface);
}

.bike-panel__copy {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--space-2);
  max-width: 560px;
}

.bike-panel__copy h2 {
  margin: var(--space-1) 0 0;
  color: var(--color-text);
  font-size: var(--text-xl);
  font-weight: var(--fw-bold);
}

.bike-panel__copy p {
  margin: 0 0 var(--space-2);
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  line-height: var(--leading-base);
}

.bike-panel__art {
  position: absolute;
  z-index: 1;
  top: 50%;
  right: 9%;
  transform: translateY(-50%) rotate(-12deg);
  color: color-mix(in srgb, var(--color-brand) 22%, transparent);
  font-size: clamp(88px, 11vw, 144px);
  pointer-events: none;
}

.bike-panel__glow {
  position: absolute;
  z-index: 0;
  top: -90px;
  right: 4%;
  width: 360px;
  height: 320px;
  border-radius: 50%;
  background: color-mix(in srgb, var(--color-brand) 12%, transparent);
  filter: blur(65px);
  pointer-events: none;
}

/* Категории */
.category-tabs {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-2);
  overflow-x: auto;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  scrollbar-width: thin;
}

.category-tab {
  display: inline-flex;
  flex: 0 0 auto;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  min-height: 40px;
  padding: 0 var(--space-4);
  border: 0;
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--color-text-secondary);
  font: inherit;
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  white-space: nowrap;
  cursor: pointer;
  transition: background-color var(--transition-fast), color var(--transition-fast);
}

.category-tab i { color: var(--color-text-tertiary); }
.category-tab:hover { background: var(--color-surface-hover); color: var(--color-text); }
.category-tab--active { background: var(--color-brand-soft); color: var(--color-brand); }
.category-tab--active i { color: var(--color-brand); }
.category-tab:focus-visible { outline: none; box-shadow: var(--shadow-focus); }

/* Каталог и фильтры */
.catalog-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.catalog-heading {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: var(--space-3);
}

.section-title {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.section-title h2 {
  margin: 0;
  color: var(--color-text);
  font-size: var(--text-xl);
  font-weight: var(--fw-bold);
}

.section-title__icon {
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
  background: var(--color-brand-soft);
  color: var(--color-brand);
}

.section-description {
  margin: var(--space-1) 0 0 40px;
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  line-height: var(--leading-base);
}

.filters-panel {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
}

.search-control {
  position: relative;
  flex: 1;
  min-width: 0;
}

.search-control > i {
  position: absolute;
  z-index: 2;
  top: 50%;
  left: var(--space-3);
  transform: translateY(-50%);
  color: var(--color-text-tertiary);
  pointer-events: none;
}

.search-control :deep(.field) { width: 100%; }
.search-control :deep(.field__input) {
  min-height: 42px;
  padding-left: 40px;
  background: var(--color-surface-secondary);
}

.difficulty-control { flex: 0 0 220px; }
.difficulty-control :deep(.field__select) {
  min-height: 42px;
  background: var(--color-surface-secondary);
}

/* Карточки — локальная разметка, чтобы scoped CSS применялся предсказуемо */
.manuals-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--space-4);
}

.manual-card {
  display: flex;
  min-width: 0;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  cursor: pointer;
  transition:
    transform var(--transition-fast),
    border-color var(--transition-fast),
    box-shadow var(--transition-fast);
}

.manual-card:hover {
  transform: translateY(-2px);
  border-color: color-mix(in srgb, var(--color-brand) 45%, var(--color-border));
  box-shadow: var(--shadow-md);
}

.manual-card:focus-visible {
  outline: none;
  box-shadow: var(--shadow-focus);
}

.manual-card__cover {
  position: relative;
  height: 176px;
  overflow: hidden;
  background:
    linear-gradient(135deg, var(--color-brand-soft), var(--color-surface-secondary));
}

.manual-card__image {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-base);
}

.manual-card:hover .manual-card__image { transform: scale(1.035); }

.manual-card__placeholder {
  display: flex;
  width: 100%;
  height: 100%;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  color: var(--color-text-tertiary);
}

.manual-card__placeholder i { color: var(--color-brand); font-size: 38px; opacity: .55; }
.manual-card__placeholder span { font-size: var(--text-xs); }

.manual-card__badges {
  position: absolute;
  z-index: 2;
  top: var(--space-3);
  left: var(--space-3);
  right: var(--space-3);
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-2);
}

.manual-card__body {
  display: flex;
  flex: 1;
  min-height: 206px;
  flex-direction: column;
  padding: var(--space-4);
}

.manual-card__title {
  display: -webkit-box;
  overflow: hidden;
  margin: 0;
  color: var(--color-text);
  font-size: var(--text-base);
  font-weight: var(--fw-bold);
  line-height: var(--leading-tight);
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.manual-card__description {
  display: -webkit-box;
  overflow: hidden;
  min-height: 42px;
  margin: var(--space-2) 0 var(--space-3);
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  line-height: var(--leading-base);
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.manual-card__meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-top: auto;
  padding-top: var(--space-3);
  border-top: 1px solid var(--color-border-light);
}

.meta-item {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  color: var(--color-text-tertiary);
  font-size: var(--text-xs);
  white-space: nowrap;
}

.manual-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: var(--space-3);
  padding-top: var(--space-3);
  border-top: 1px solid var(--color-border-light);
  color: var(--color-text);
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
}

.manual-card__footer i {
  color: var(--color-brand);
  transition: transform var(--transition-fast);
}

.manual-card:hover .manual-card__footer i { transform: translateX(4px); }

.manual-card--skeleton {
  padding: 0;
  cursor: default;
}

.manual-card__body :deep(.skeleton) { flex-shrink: 0; }
.state-panel {
  overflow: hidden;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
}

/* Пагинация */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-4);
  margin-top: var(--space-2);
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
}

.pagination strong { color: var(--color-text); }

@media (max-width: 1200px) {
  .manuals-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}

@media (max-width: 900px) {
  .manuals-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .bike-panel__art { right: 4%; }
}

@media (max-width: 640px) {
  .page-header { align-items: stretch; flex-direction: column; }
  .page-title { font-size: var(--text-2xl); }
  .bike-panel { min-height: 0; padding: var(--space-4); }
  .bike-panel__art, .bike-panel__glow { display: none; }
  .category-tabs { margin-right: calc(var(--space-3) * -1); }
  .category-tab { padding: 0 var(--space-3); }
  .catalog-heading { align-items: flex-start; flex-direction: column; }
  .section-description { margin-left: 0; }
  .filters-panel { align-items: stretch; flex-direction: column; }
  .difficulty-control { flex-basis: auto; }
  .manuals-grid { grid-template-columns: 1fr; }
  .manual-card__cover { height: 200px; }
}
</style>
