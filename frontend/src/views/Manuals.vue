<template>
  <div class="manuals-page">
    <LoadingOverlay :isLoading="loading" text="Загрузка мануалов..." />

    <div class="container">
      <!-- === HEADER === -->
      <Header
        title="Мануалы"
        subtitle="База инструкций по ремонту и обслуживанию мотоциклов"
      />

      <!-- === FILTERS AND TABS === -->
      <div class="filters-section">
        <div class="tabs-wrapper">
          <div class="tabs">
            <div class="tabs-btn">
              <button
                v-for="tabItem in tabs"
                :key="tabItem.value"
                class="tab"
                :class="{ active: tab === tabItem.value }"
                @click="changeTab(tabItem.value)"
              >
                <i :class="tabItem.icon"></i>
                {{ tabItem.label }}
                <span class="tab-count" v-if="tabItem.value === 'all'">
                  {{ pagination.total }}
                </span>
              </button>
            </div>

            <button @click="$router.push('/manual-creator')" class="outline-btn">
              <i class="fa fa-plus"></i>
              <span>Создать мануал</span>
            </button>
          </div>
        </div>

        <div class="filters">
          <div class="filters-group">
            <div class="search-wrapper">
              <i class="fa fa-search"></i>
              <input
                type="text"
                :value="filters.search"
                @input="debouncedSearch"
                placeholder="Поиск по названию или мотоциклу..."
                class="search-input"
              >
              <button v-if="filters.search" @click="clearSearch" class="clear-search">
                <i class="fa fa-times"></i>
              </button>
            </div>

            <select
              class="filter-select"
              :value="filters.motorcycle"
              @change="onMotorcycleChange($event.target.value)"
            >
              <option value="">Все мотоциклы</option>
              <option
                v-for="moto in motorcycles"
                :key="moto.id"
                :value="moto.name"
              >
                {{ moto.name }}
              </option>
            </select>

            <select
              class="filter-select"
              :value="filters.category"
              @change="onCategoryChange($event.target.value)"
            >
              <option value="">Все системы</option>
              <option value="engine">⚙️ Двигатель</option>
              <option value="drive">🔗 Привод</option>
              <option value="steering">🔄 Рулевое управление</option>
              <option value="suspension">🛞 Подвеска</option>
              <option value="electronics">💡 Электроника</option>
              <option value="wheel">⚡ Колеса/Шины</option>
              <option value="brakes">🛑 Тормозная система</option>
              <option value="fuel">⛽ Топливная система</option>
              <option value="cooling">❄️ Система охлаждения</option>
            </select>

            <select
              class="filter-select"
              :value="filters.sort_by"
              @change="onSortChange($event.target.value)"
            >
              <option value="created_at_desc">📅 По дате (новые)</option>
              <option value="created_at_asc">📅 По дате (старые)</option>
              <option value="title_asc">🔤 По названию (А-Я)</option>
              <option value="title_desc">🔤 По названию (Я-А)</option>
            </select>
          </div>
        </div>

        <div class="filter-results" v-if="items.length > 0 && hasActiveFilters">
          <span>
            <i class="fa fa-filter"></i>
            Найдено: {{ items.length }} мануалов
          </span>
          <button class="clear-filters" @click="clearAllFilters">
            <i class="fa fa-times"></i> Очистить фильтры
          </button>
        </div>
      </div>

      <!-- === MANUALS GRID === -->
      <div class="manuals-section">
        <div v-if="loading" class="loading-state">
          <i class="fa fa-spinner fa-spin"></i>
          <span>Загрузка мануалов...</span>
        </div>

        <div v-else-if="items.length === 0" class="empty-state-wrapper">
          <div class="empty-state">
            <div class="empty-icon" :class="{ warning: hasActiveFilters }">
              <i :class="hasActiveFilters ? 'fa fa-search' : 'fa fa-book'"></i>
            </div>
            <h3 v-if="hasActiveFilters">Мануалы не найдены</h3>
            <h3 v-else>Мануалов пока нет</h3>
            <p class="empty-text" v-if="hasActiveFilters">
              Попробуйте изменить параметры фильтрации
            </p>
            <p class="empty-text" v-else>
              Создайте свой первый мануал и помогите сообществу
            </p>
            <div class="empty-actions">
              <button v-if="hasActiveFilters" @click="clearAllFilters" class="btn-secondary">
                Сбросить фильтры
              </button>
              <button v-else @click="$router.push('/manual-creator')" class="btn-primary">
                Создать мануал
              </button>
            </div>
          </div>
        </div>

        <div v-else class="manuals-grid">
          <div
            v-for="manual in items"
            :key="manual.id"
            class="manual-card"
            @click="viewManual(manual)"
          >
            <div class="manual-image-wrapper">
              <img
                :src="getManualImage(manual)"
                :alt="manual.title"
                class="manual-img"
                @error="handleImageError"
                loading="lazy"
              >
              <div class="manual-badge" v-if="manual.difficult">
                {{ getDifficultyLabel(manual.difficult) }}
              </div>
            </div>

            <div class="manual-body">
              <span class="manual-category">{{ getCategoryLabel(manual.category) }}</span>
              <h3 class="manual-title">{{ manual.title }}</h3>
              <p class="manual-moto">
                <i class="fa fa-motorcycle"></i>
                {{ manual.motorcycle }}
              </p>

              <div class="manual-meta">
                <span v-if="manual.time_estimate" class="meta-tag">
                  <i class="fa fa-clock"></i> {{ manual.time_estimate }}
                </span>
                <span v-if="manual.steps?.length" class="meta-tag">
                  <i class="fa fa-list-ol"></i> {{ manual.steps.length }} шаг{{ manual.steps.length > 1 ? 'а' : '' }}
                </span>
              </div>

              <button class="btn-outline view-btn">
                Подробнее <i class="fa fa-arrow-right"></i>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- === PAGINATION === -->
      <div v-if="!loading && items.length > 0 && pagination.pages > 1" class="pagination-section">
        <div class="pagination-info">
          <span>
            Показано {{ (pagination.current_page - 1) * pagination.per_page + 1 }}—
            {{ Math.min(pagination.current_page * pagination.per_page, pagination.total) }}
            из {{ pagination.total }}
          </span>
        </div>

        <div class="pagination-controls">
          <button
            class="pagination-btn"
            @click="goToPage(pagination.current_page - 1)"
            :disabled="!pagination.has_prev"
          >
            <i class="fa fa-chevron-left"></i>
          </button>

          <div class="pagination-pages">
            <template v-for="page in visiblePages" :key="page">
              <button
                v-if="page !== '...'"
                class="pagination-btn page-btn"
                :class="{ active: page === pagination.current_page }"
                @click="goToPage(page)"
              >
                {{ page }}
              </button>
              <span v-else class="pagination-ellipsis">…</span>
            </template>
          </div>

          <button
            class="pagination-btn"
            @click="goToPage(pagination.current_page + 1)"
            :disabled="!pagination.has_next"
          >
            <i class="fa fa-chevron-right"></i>
          </button>
        </div>

        <div class="pagination-per-page">
          <select :value="pagination.per_page" @change="onPerPageChange($event.target.value)">
            <option :value="6">6</option>
            <option :value="12">12</option>
            <option :value="24">24</option>
            <option :value="48">48</option>
          </select>
          <span>на странице</span>
        </div>
      </div>
    </div>
  </div>

  <ManualDetailsModal
    :is-open="showManualDetailsModal"
    :manual="selectedManual"
    @close="showManualDetailsModal = false"
  />
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useManualsStore, useMotorcyclesStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import { getCategoryLabel, getDifficultyLabel } from '@/utils/formatters'
import { getManualImageUrl } from '@/utils/mediaUrl'

import ManualDetailsModal from '../components/modals/manual/ManualDetailsModal.vue'
import Header from '../components/Header.vue'
import LoadingOverlay from '../components/LoadingOverlay.vue'

const toast = useToast()
const manualsStore = useManualsStore()
const motorcyclesStore = useMotorcyclesStore()

const {
  items,
  loading,
  filters,
  tab,
  pagination,
  hasActiveFilters,
  visiblePages,
} = storeToRefs(manualsStore)

const {
  loadList,
  setFilter,
  setTab,
  setSortBy,
  setPage,
  setPerPage,
  clearAll,
} = manualsStore

const motorcycles = storeToRefs(motorcyclesStore).items

// ===== Local UI state =====
const selectedManual = ref(null)
const showManualDetailsModal = ref(false)
let searchTimeout = null

// ===== Tabs =====
const tabs = [
  { value: 'all', label: 'Все мануалы', icon: 'fa fa-book' },
  { value: 'my', label: 'Мои мануалы', icon: 'fa fa-user' },
  { value: 'myMotos', label: 'Для моих мотоциклов', icon: 'fa fa-motorcycle' },
]

// ===== Lifecycle =====
onMounted(async () => {
  const promises = [loadList()]
  if (!motorcycles.value.length) {
    promises.push(motorcyclesStore.loadAll())
  }
  await Promise.all(promises).catch((err) => {
    console.error('Failed to load manuals:', err)
    toast.error('Не удалось загрузить мануалы')
  })
})

// ===== Filters / tabs / pagination =====
function changeTab(value) {
  setTab(value)
  loadList().catch(() => {})
}

function debouncedSearch(event) {
  setFilter('search', event.target.value)
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    loadList().catch(() => {})
  }, 500)
}

function clearSearch() {
  setFilter('search', '')
  loadList().catch(() => {})
}

function onMotorcycleChange(value) {
  setFilter('motorcycle', value)
  loadList().catch(() => {})
}

function onCategoryChange(value) {
  setFilter('category', value)
  loadList().catch(() => {})
}

function onSortChange(value) {
  setSortBy(value)
  loadList().catch(() => {})
}

function onPerPageChange(value) {
  setPerPage(Number(value))
  loadList().catch(() => {})
}

function goToPage(page) {
  setPage(page)
  loadList().catch(() => {})
}

function clearAllFilters() {
  clearAll()
  loadList().catch(() => {})
}

// ===== Cards =====
function viewManual(manual) {
  selectedManual.value = manual
  showManualDetailsModal.value = true
}

function getManualImage(manual) {
  if (manual.image) return getManualImageUrl(manual.image)
  if (manual.steps?.length) {
    const stepWithImage = manual.steps.find((s) => s.image)
    if (stepWithImage?.image) return getManualImageUrl(stepWithImage.image)
  }
  return '/ManualImgDefault.webp'
}

function handleImageError(event) {
  event.target.src = '/ManualImgDefault.webp'
}
</script>

<style scoped>
/* ===== BASE ===== */
.manuals-page {
    padding: 20px 0 40px;
    max-width: 100%;
    overflow-x: hidden;
}

.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 16px;
    overflow-x: hidden;
}

/* ===== FILTERS ===== */
.filters-section {
    margin-bottom: 24px;
}

.tabs-wrapper {
    margin-bottom: 16px;
}

.tabs {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    background: var(--bg-secondary);
    padding: 4px;
    border-radius: 12px;
    border: 1px solid var(--border-light);
}

.tabs-btn {
    display: flex;
    gap: 4px;
}

.tab {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: transparent;
    border: none;
    border-radius: 8px;
    color: var(--text-muted);
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.25s ease;
}

.tab:hover {
    color: var(--text-primary);
    background: var(--border-light);
}

.tab.active {
    background: var(--bg-primary);
    color: var(--accent-text);
    box-shadow: var(--shadow-sm);
}

.tab-count {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0 8px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
    background: var(--bg-primary);
    color: var(--text-muted);
    min-width: 20px;
    height: 20px;
}

.tab.active .tab-count {
    background: var(--accent-trans);
    color: var(--accent-text);
}

.filters {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.filters-group {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
}

.search-wrapper {
    display: flex;
    align-items: center;
    position: relative;
    flex: 1;
    min-width: 200px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: 10px;
    transition: border 0.2s;
}

.search-wrapper:focus-within {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-trans);
}

.search-wrapper i {
    position: absolute;
    left: 12px;
    color: var(--text-muted);
    font-size: 14px;
}

.search-input {
    width: 100%;
    padding: 10px 36px 10px 38px;
    background: transparent;
    border: none;
    color: var(--text-primary);
    font-size: 14px;
    outline: none;
}

.search-input::placeholder {
    color: var(--text-muted);
}

.clear-search {
    position: absolute;
    right: 10px;
    background: transparent;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 6px;
    transition: all 0.2s;
}

.clear-search:hover {
    color: var(--text-primary);
    background: var(--border-light);
}

.filter-select {
    padding: 10px 14px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: 10px;
    color: var(--text-primary);
    font-size: 14px;
    outline: none;
    cursor: pointer;
    transition: all 0.2s;
    min-width: 160px;
    flex: 1;
}

.filter-select:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-trans);
}

.filter-select option {
    background: var(--bg-input);
}

.filter-results {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 16px;
    background: var(--accent-trans);
    border-radius: 10px;
    font-size: 13px;
    color: var(--text-muted);
}

.filter-results i {
    color: var(--accent-text);
}

.clear-filters {
    background: transparent;
    border: none;
    color: var(--accent-text);
    cursor: pointer;
    font-size: 13px;
    transition: all 0.2s;
    padding: 4px 12px;
    border-radius: 6px;
}

.clear-filters:hover {
    background: var(--accent-trans);
    color: var(--accent);
}

/* ===== MANUALS GRID ===== */
.manuals-section {
    min-height: 400px;
}

.manuals-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
}

.manual-card {
    background: var(--bg-secondary);
    border-radius: 16px;
    border: 1px solid var(--border-light);
    overflow: hidden;
    transition: all 0.3s ease;
    cursor: pointer;
}

.manual-card:hover {
    border-color: var(--accent);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.manual-image-wrapper {
    position: relative;
    width: 100%;
    aspect-ratio: 16/10;
    overflow: hidden;
    background: var(--bg-primary);
}

.manual-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.manual-card:hover .manual-img {
    transform: scale(1.05);
}

.manual-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(8px);
    color: #fff;
}

.manual-body {
    padding: 14px 16px 16px;
}

.manual-category {
    display: inline-block;
    padding: 2px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    background: var(--accent-trans);
    color: var(--accent-text);
    margin-bottom: 8px;
}

.manual-title {
    font-size: 16px;
    font-weight: 600;
    margin: 0 0 4px 0;
    color: var(--text-primary);
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    line-height: 1.3;
}

.manual-moto {
    font-size: 13px;
    color: var(--text-muted);
    margin: 0 0 10px 0;
    display: flex;
    align-items: center;
    gap: 4px;
}

.manual-moto i {
    font-size: 13px;
}

.manual-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 12px;
}

.meta-tag {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
    color: var(--text-secondary);
    background: var(--bg-primary);
    padding: 2px 10px;
    border-radius: 12px;
    border: 1px solid var(--border-light);
}

.meta-tag i {
    font-size: 11px;
    color: var(--text-muted);
}

/* ===== LOADING STATE ===== */
.loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 80px 0;
    gap: 16px;
    color: var(--text-secondary);
}

.loading-state .fa-spinner {
    font-size: 32px;
    color: var(--accent);
}

/* ===== PAGINATION ===== */
.pagination-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
    margin-top: 28px;
    padding-top: 20px;
    border-top: 1px solid var(--border-light);
}

.pagination-info {
    font-size: 14px;
    color: var(--text-muted);
}

.pagination-controls {
    display: flex;
    align-items: center;
    gap: 4px;
}

.pagination-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border: 1px solid var(--border-light);
    border-radius: 8px;
    background: var(--bg-secondary);
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 14px;
}

.pagination-btn:hover:not(:disabled) {
    border-color: var(--accent);
    color: var(--accent-text);
    background: var(--accent-trans);
}

.pagination-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

.pagination-btn.page-btn {
    width: 36px;
    font-weight: 500;
}

.pagination-btn.page-btn.active {
    background: var(--accent);
    color: #fff;
    border-color: var(--accent);
}

.pagination-pages {
    display: flex;
    gap: 4px;
    margin-left: 8px;
    margin-right: 8px;
    overflow-x: auto;
}

.pagination-ellipsis {
    padding: 0 8px;
    color: var(--text-muted);
}

.pagination-per-page {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    color: var(--text-muted);
}

.pagination-per-page select {
    padding: 6px 12px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: 8px;
    color: var(--text-primary);
    font-size: 14px;
    outline: none;
    cursor: pointer;
    transition: border 0.2s;
}

.pagination-per-page select:focus {
    border-color: var(--accent);
}

/* ===== RESPONSIVE ===== */
@media (max-width: 1200px) {
    .manuals-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

@media (max-width: 992px) {
    .manuals-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .filters-group {
        flex-direction: column;
        width: 100%;
    }

    .search-wrapper {
        min-width: unset;
        width: 100%;
    }

    .filter-select {
        min-width: unset;
        width: 100%;
    }
}

@media (max-width: 820px) {
    .page-header {
        flex-direction: column;
        align-items: stretch;
        gap: 12px;
    }

    .page-title {
        font-size: 24px;
    }

    .tabs {
        flex-wrap: wrap;
    }

    .tabs-btn {
        margin-bottom: 8px;
    }

    .tabs button {
        width: 100%;
    }

    .tab {
        flex: 1;
        justify-content: center;
        min-width: 80px;
        padding: 6px 12px;
        font-size: 12px;
    }

    .tab-count {
        display: none;
    }

    .pagination-section {
        flex-direction: column;
        align-items: stretch;
        gap: 12px;
    }

    .pagination-controls {
        justify-content: center;
        flex-wrap: wrap;
    }

    .pagination-info {
        text-align: center;
    }

    .pagination-per-page {
        justify-content: center;
    }
}

@media (max-width: 600px) {
    .manuals-page {
        padding: 12px 0 24px;
    }

    .container {
        padding: 0 12px;
    }

    .page-title {
        font-size: 20px;
    }

    .page-subtitle {
        font-size: 13px;
    }

    .manuals-grid {
        grid-template-columns: 1fr;
        gap: 12px;
    }

    .manual-card {
        border-radius: 12px;
    }

    .manual-image-wrapper {
        aspect-ratio: 16/9;
    }

    .manual-title {
        font-size: 15px;
    }

    .filter-results {
        flex-direction: column;
        gap: 6px;
        text-align: center;
    }

    .pagination-btn {
        width: 32px;
        height: 32px;
        font-size: 12px;
    }

    .pagination-btn.page-btn {
        width: 32px;
    }
}

@media (max-width: 400px) {
    .tab {
        font-size: 11px;
        padding: 4px 8px;
    }

    .tab i {
        display: none;
    }

    .manual-meta {
        flex-direction: column;
        gap: 4px;
    }
}
</style>
