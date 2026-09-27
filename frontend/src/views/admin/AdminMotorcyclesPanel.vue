<template>
  <div class="container">
    <LoadingOverlay :isLoading="loading" text="Загрузка мотоциклов..." />

    <Header
      title="Мотоциклы пользователей"
      subtitle="Управление мотоциклами всех пользователей"
    />

    <section>
      <div class="stat-cards">
        <div class="stat-card">
          <div class="card-icon">
            <i class="fa fa-motorcycle"></i>
          </div>
          <div class="card-body">
            <p class="card-title">Всего мотоциклов</p>
            <p class="card-value">{{ stats.total || 0 }}</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="card-icon success">
            <i class="fa fa-check-circle"></i>
          </div>
          <div class="card-body">
            <p class="card-title">С обслуживанием</p>
            <p class="card-value">{{ stats.with_maintenance || 0 }}</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="card-icon warning">
            <i class="fa fa-clock"></i>
          </div>
          <div class="card-body">
            <p class="card-title">Без обслуживания</p>
            <p class="card-value">{{ stats.without_maintenance || 0 }}</p>
          </div>
        </div>
      </div>
    </section>

    <section>
      <div class="table-filters">
        <div class="filters-row">
          <div class="filter-group">
            <input
              type="text"
              v-model="filters.search"
              @input="debouncedSearch"
              placeholder="Поиск по названию, VIN, номеру..."
              class="search-input"
            />
          </div>

          <select v-model="filters.status" @change="applyFilters" class="filter-select">
            <option value="">Все мотоциклы</option>
            <option value="has_maintenance">С обслуживанием</option>
            <option value="no_maintenance">Без обслуживания</option>
          </select>

          <select v-model="filters.owner_id" @change="applyFilters" class="filter-select">
            <option value="">Все владельцы</option>
            <option v-for="user in users" :key="user.id" :value="user.id">
              {{ user.username }}
            </option>
          </select>

          <select v-model="filters.sort_by" @change="applyFilters" class="filter-select">
            <option value="created_at">По дате (новые)</option>
            <option value="name">По названию</option>
            <option value="mileage">По пробегу</option>
          </select>
        </div>

        <div class="filters-actions">
          <button class="btn-outline" @click="resetFilters">
            <i class="fa fa-refresh"></i> Сбросить
          </button>
        </div>
      </div>

      <div class="filter-results" v-if="filteredCount > 0">
        <span>Найдено: {{ filteredCount }} мотоциклов</span>
        <button class="clear-filters" @click="resetFilters" v-if="hasActiveFilters">
          <i class="fa fa-times"></i> Очистить фильтры
        </button>
      </div>
    </section>

    <section class="table-section">
      <div v-if="loading" class="loading-state">
        <i class="fa fa-spinner fa-spin"></i> Загрузка...
      </div>

      <div v-else class="motorcycles-table-wrapper">
        <div class="table-header">
          <span class="th">Мотоцикл</span>
          <span class="th">Владелец</span>
          <span class="th">Пробег</span>
          <span class="th">Обслуживаний</span>
          <span class="th">Дата добавления</span>
          <span class="th"></span>
        </div>

        <div class="table-body">
          <div v-if="motorcycles.length === 0" class="tr empty-state">
            <div class="td">Мотоциклы не найдены</div>
          </div>

          <div
            v-for="moto in motorcycles"
            :key="moto.id"
            class="tr"
          >
            <div class="td moto-cell">
              <img
                v-if="moto.photo_url"
                :src="getMotoPhotoUrl(moto.photo_url)"
                alt="Фото"
                class="moto-thumb"
                @error="(e) => e.target.src = '/moto_default.webp'"
              />
              <div class="moto-placeholder" v-else>
                <i class="fa fa-motorcycle"></i>
              </div>
              <div class="moto-info">
                <p class="moto-name">{{ moto.name }}</p>
                <span class="moto-meta">{{ moto.years || '—' }} • {{ moto.volume || '—' }} см³</span>
              </div>
            </div>

            <div class="td owner-cell">
              <div class="owner-info">
                <span class="owner-name">{{ moto.owner?.username || '—' }}</span>
                <span class="owner-email">{{ moto.owner?.email || '—' }}</span>
              </div>
            </div>

            <div class="td mileage-cell">
              <span class="mileage-value">{{ moto.mileage || 0 }} км</span>
            </div>

            <div class="td maintenance-cell">
              <span
                class="maintenance-badge"
                :class="{
                  'badge-success': moto.maintenances_count > 0,
                  'badge-gray': moto.maintenances_count === 0
                }"
              >
                {{ moto.maintenances_count || 0 }}
              </span>
            </div>

            <div class="td date-cell">
              <span class="date-value">{{ formatDate(moto.created_at) }}</span>
            </div>

            <div class="td actions-cell">
              <button
                class="btn-small danger"
                @click="openDeleteModal(moto)"
                title="Удалить мотоцикл"
              >
                <i class="fa fa-trash"></i>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="!loading && motorcycles.length > 0" class="table-paginate">
        <p class="paginate-show">
          Показано {{ (pagination.current_page - 1) * pagination.per_page + 1 }}-
          {{ Math.min(pagination.current_page * pagination.per_page, pagination.total) }}
          из {{ pagination.total }}
        </p>

        <div class="paginate-ui">
          <button
            class="paginate-arrow"
            @click="goToPage(pagination.current_page - 1)"
            :disabled="!pagination.has_prev"
            aria-label="Предыдущая страница"
          >
            <i class="fa fa-angle-left"></i>
          </button>

          <div class="paginate-btns">
            <button
              v-for="(page, idx) in visiblePages"
              :key="`p-${idx}-${page}`"
              class="paginate-num"
              :class="{ active: page === pagination.current_page, dots: page === '...' }"
              :disabled="page === '...'"
              @click="page !== '...' && goToPage(page)"
            >
              {{ page }}
            </button>
          </div>

          <button
            class="paginate-arrow"
            @click="goToPage(pagination.current_page + 1)"
            :disabled="!pagination.has_next"
            aria-label="Следующая страница"
          >
            <i class="fa fa-angle-right"></i>
          </button>
        </div>

        <div class="show-per-page">
          <select v-model="pagination.per_page" @change="changePerPage">
            <option :value="10">10</option>
            <option :value="20">20</option>
            <option :value="50">50</option>
            <option :value="100">100</option>
          </select>
        </div>
      </div>
    </section>
  </div>

  <DeleteMotoAdminModal
    :isOpen="showDeleteModal"
    :motorcycle="selectedMotorcycle"
    @submit="deleteMotorcycle"
    @close="closeDeleteModal"
  />
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import Header from '@/components/Header.vue'
import LoadingOverlay from '@/components/LoadingOverlay.vue'
import DeleteMotoAdminModal from '@/components/modals/admin/DeleteMotoAdminModal.vue'
import { useToast } from '@/composables/useToast'
import { getMotoPhotoUrl } from '@/utils/mediaUrl'
import formatDate from '@/utils/DateFormatter.js'
import api from '@/api/api'

const toast = useToast()

const loading = ref(false)
const motorcycles = ref([])
const users = ref([])
const stats = ref({
  total: 0,
  with_maintenance: 0,
  without_maintenance: 0,
})
const pagination = ref({
  current_page: 1,
  per_page: 10,
  total: 0,
  pages: 0,
  has_prev: false,
  has_next: false,
})
const filters = ref({
  search: '',
  status: '',
  owner_id: '',
  sort_by: 'created_at',
  sort_order: 'desc',
})
const showDeleteModal = ref(false)
const selectedMotorcycle = ref(null)

let searchTimeout = null

const filteredCount = computed(() => pagination.value.total || 0)

const visiblePages = computed(() => {
    const current = pagination.value.current_page
    const total = pagination.value.pages
    const delta = 2
    const pages = []

    if (total <= 7) {
        for (let i = 1; i <= total; i++) pages.push(i)
        return pages
    }

    pages.push(1)
    if (current - delta > 2) pages.push('...')

    const start = Math.max(2, current - delta)
    const end = Math.min(total - 1, current + delta)
    for (let i = start; i <= end; i++) pages.push(i)

    if (current + delta < total - 1) pages.push('...')
    pages.push(total)

    return pages
})

const hasActiveFilters = computed(() => {
  return filters.value.search || filters.value.status || filters.value.owner_id
})

onMounted(() => {
  loadMotorcycles()
  loadUsers()
})

async function loadMotorcycles() {
  loading.value = true
  try {
    const params = {
      page: pagination.value.current_page,
      per_page: pagination.value.per_page,
      ...filters.value,
    }

    Object.keys(params).forEach(key => {
      if (!params[key]) delete params[key]
    })

    const response = await api.get('/admin/motorcycles', { params })
    const data = response.data

    motorcycles.value = data.motorcycles || []
    pagination.value = {
      current_page: data.current_page,
      per_page: data.per_page,
      total: data.total,
      pages: data.pages,
      has_prev: data.has_prev,
      has_next: data.has_next,
    }
    stats.value = data.stats || {
      total: 0,
      with_maintenance: 0,
      without_maintenance: 0,
    }
  } catch (error) {
    console.error('Error loading motorcycles:', error)
  } finally {
    loading.value = false
  }
}

async function loadUsers() {
  try {
    const response = await api.get('/admin/users', {
      params: { per_page: 1000 },
    })
    users.value = response.data.users || []
  } catch (error) {
    console.error('Error loading users:', error)
  }
}

function goToPage(page) {
  if (page < 1 || page > pagination.value.pages) return
  pagination.value.current_page = page
  loadMotorcycles()
}

function changePerPage() {
  pagination.value.current_page = 1
  loadMotorcycles()
}

function applyFilters() {
  pagination.value.current_page = 1
  loadMotorcycles()
}

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    applyFilters()
  }, 500)
}

function resetFilters() {
  filters.value = {
    search: '',
    status: '',
    owner_id: '',
    sort_by: 'created_at',
    sort_order: 'desc',
  }
  pagination.value.current_page = 1
  loadMotorcycles()
}

function openDeleteModal(moto) {
  selectedMotorcycle.value = moto
  showDeleteModal.value = true
}

function closeDeleteModal() {
  selectedMotorcycle.value = null
  showDeleteModal.value = false
}

async function deleteMotorcycle(motoId) {
  try {
    await api.delete(`/admin/motorcycle/${motoId}`)
    await loadMotorcycles()
    closeDeleteModal()
    toast.success('Мотоцикл удалён')
  } catch (error) {
    console.error('Error deleting motorcycle:', error)
    toast.error(
      error.response?.data?.error || 'Ошибка при удалении мотоцикла'
    )
  }
}
</script>

<style scoped>
/* ============================================
   STATISTIC CARDS
   ============================================ */
.stat-cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}

.stat-card {
    display: flex;
    gap: 16px;
    align-items: center;
    padding: 12px 14px;
    background-color: var(--bg-card);
    border-radius: var(--radius-md);
    border: 1px solid var(--border-light);
    transition: all var(--transition-base);
    min-width: 0;
}
.stat-card:hover {
    background-color: var(--accent-trans);
    border-color: var(--accent);
}

.card-icon {
    width: 48px;
    height: 48px;
    min-height: 48px; /* перебиваем reset.scss */
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: var(--radius-md);
    background-color: var(--accent-trans);
    color: var(--accent-text);
    font-size: 18px;
    flex-shrink: 0;
}
.card-icon.success { background-color: var(--success-trans); color: var(--success-text); }
.card-icon.warning { background-color: var(--warning-trans); color: var(--warning-text); }

.card-body { min-width: 0; }
.card-title {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.card-value {
    font-size: 21px;
    font-weight: var(--fw-semibold);
    color: var(--text-primary);
    margin: 0;
}

/* ============================================
   FILTERS
   ============================================ */
.table-filters {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 12px;
}

.filters-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    flex: 1;
    min-width: 0;
}

.filter-group {
    min-width: 200px;
    flex: 1;
}

.search-input {
    width: 100%;
    padding: 8px 14px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: var(--radius-md);
    color: var(--text-primary);
    font-size: 14px;
    outline: none;
    transition: border var(--transition-fast), box-shadow var(--transition-fast);
}
.search-input:focus {
    border-color: var(--accent);
    box-shadow: var(--shadow-focus);
}
.search-input::placeholder { color: var(--text-muted); }

.filter-select {
    padding: 8px 14px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: var(--radius-md);
    color: var(--text-primary);
    font-size: 14px;
    outline: none;
    cursor: pointer;
    transition: border var(--transition-fast), box-shadow var(--transition-fast);
    min-width: 150px;
}
.filter-select:focus {
    border-color: var(--accent);
    box-shadow: var(--shadow-focus);
}
.filter-select option { background: var(--bg-input); }

.filters-actions { display: flex; gap: 8px; flex-shrink: 0; }

.btn-outline {
    padding: 8px 16px;
    background: transparent;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    color: var(--text-secondary);
    cursor: pointer;
    transition: all var(--transition-base);
    font-size: 14px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    min-height: 40px; /* не 44px из reset */
}
.btn-outline:hover {
    background: var(--border-light);
    border-color: var(--text-muted);
}
.btn-outline:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.filter-results {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    padding: 8px 12px;
    background: var(--accent-trans);
    border-radius: var(--radius-md);
    font-size: 13px;
    color: var(--text-muted);
    margin-bottom: 16px;
    flex-wrap: wrap;
}

.clear-filters {
    background: transparent;
    border: none;
    color: var(--accent-text);
    cursor: pointer;
    font-size: 13px;
    transition: color var(--transition-fast);
    display: inline-flex;
    align-items: center;
    gap: 6px;
    min-height: 32px;
}
.clear-filters:hover { color: var(--accent); }

/* ============================================
   TABLE
   ============================================ */
.table-section {
    background: var(--bg-card);
    border-radius: var(--radius-md);
    border: 1px solid var(--border-light);
    padding: 14px 16px;
    margin-bottom: 0;
}

.loading-state {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 40px 0;
    color: var(--text-secondary);
    gap: 12px;
}
.loading-state .fa-spinner { font-size: 24px; color: var(--accent); }

.motorcycles-table-wrapper {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}

.table-header {
    display: grid;
    grid-template-columns: 2fr 1.2fr 0.9fr 1fr 1fr 60px;
    gap: 8px;
    padding: 10px 12px;
    border-bottom: 1px solid var(--border-light);
    font-size: 13px;
    color: var(--text-muted);
    font-weight: var(--fw-medium);
    min-width: 720px;
}

.table-body { display: flex; flex-direction: column; }

.tr {
    display: grid;
    grid-template-columns: 2fr 1.2fr 0.9fr 1fr 1fr 60px;
    gap: 8px;
    padding: 10px 12px;
    align-items: center;
    border-bottom: 1px solid var(--border-light);
    transition: background var(--transition-fast);
    min-width: 720px;
}
.tr:hover { background: var(--border-light); }
.tr:last-child { border-bottom: none; }

.tr.empty-state { cursor: default; }
.tr.empty-state:hover { background: transparent; }
.tr.empty-state .td {
    grid-column: 1 / -1;
    text-align: center;
    color: var(--text-secondary);
}

.td {
    font-size: 14px;
    color: var(--text-primary);
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* --- Moto cell --- */
.moto-cell {
    display: flex;
    align-items: center;
    gap: 12px;
    min-width: 0;
}
.moto-thumb {
    width: 40px;
    height: 40px;
    min-height: 40px;
    border-radius: var(--radius-md);
    object-fit: cover;
    flex-shrink: 0;
}
.moto-placeholder {
    width: 40px;
    height: 40px;
    min-height: 40px;
    border-radius: var(--radius-md);
    background: var(--bg-secondary);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    flex-shrink: 0;
    font-size: 16px;
}
.moto-info { display: flex; flex-direction: column; min-width: 0; }
.moto-name {
    font-weight: var(--fw-semibold);
    margin: 0;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.moto-meta {
    font-size: 12px;
    color: var(--text-muted);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* --- Owner cell --- */
.owner-cell { display: flex; align-items: center; min-width: 0; }
.owner-info { display: flex; flex-direction: column; min-width: 0; }
.owner-name {
    font-weight: var(--fw-medium);
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.owner-email {
    font-size: 12px;
    color: var(--text-muted);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* --- Mileage --- */
.mileage-cell { min-width: 0; }
.mileage-value {
    font-weight: var(--fw-medium);
    color: var(--text-primary);
}

/* --- Maintenance --- */
.maintenance-cell { display: flex; }
.maintenance-badge {
    display: inline-block;
    padding: 2px 12px;
    border-radius: var(--radius-full);
    font-size: 13px;
    font-weight: var(--fw-semibold);
    text-align: center;
    min-width: 34px;
}
.badge-success { background: var(--success-trans); color: var(--success-text); }
.badge-gray    { background: var(--bg-secondary);    color: var(--text-muted); }

/* --- Date --- */
.date-cell { min-width: 0; }
.date-value {
    font-size: 13px;
    color: var(--text-secondary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* --- Actions --- */
.actions-cell { display: flex; gap: 6px; justify-content: flex-end; }
.btn-small {
    width: 32px;
    height: 32px;
    min-height: 32px;
    padding: 0;
    border-radius: var(--radius-md);
    border: none;
    cursor: pointer;
    transition: all var(--transition-base);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    flex-shrink: 0;
}
.btn-small.danger { background: var(--danger-trans); color: var(--danger-text); }
.btn-small.danger:hover { background: var(--danger-trans); opacity: 0.8; }

/* ============================================
   PAGINATION
   ============================================ */
.table-paginate {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 16px;
    flex-wrap: wrap;
    gap: 12px;
}

.paginate-show {
    color: var(--text-secondary);
    font-size: 14px;
    margin: 0;
}

.paginate-ui {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
}

.paginate-btns {
    display: flex;
    gap: 4px;
    align-items: center;
    flex-wrap: wrap;
}

/* Стрелки ← → */
.paginate-arrow {
    width: 36px;
    height: 36px;
    min-height: 36px;
    padding: 0;
    border-radius: var(--radius-md);
    border: 1px solid var(--border-color);
    background: transparent;
    color: var(--text-secondary);
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: all var(--transition-base);
    font-size: 15px;
    flex-shrink: 0;
}
.paginate-arrow:hover:not(:disabled) {
    background: var(--border-light);
    border-color: var(--text-muted);
    color: var(--text-primary);
}
.paginate-arrow:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

/* Номера страниц */
.paginate-num {
    min-width: 34px;
    height: 34px;
    min-height: 34px;
    padding: 0 10px;
    border-radius: var(--radius-md);
    border: none;
    background: transparent;
    color: var(--text-secondary);
    cursor: pointer;
    font-size: 14px;
    font-weight: var(--fw-medium);
    transition: all var(--transition-base);
    display: inline-flex;
    align-items: center;
    justify-content: center;
}
.paginate-num:hover:not(:disabled):not(.active) {
    background: var(--border-light);
    color: var(--text-primary);
}
.paginate-num.active {
    background: var(--accent-trans);
    color: var(--accent-text);
    font-weight: var(--fw-semibold);
}
.paginate-num.dots {
    cursor: default;
    color: var(--text-muted);
    pointer-events: none;
}

/* Кол-во на страницу */
.show-per-page {
    display: flex;
    gap: 8px;
    align-items: center;
}
.show-per-page select {
    padding: 6px 12px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: var(--radius-md);
    color: var(--text-primary);
    font-size: 14px;
    outline: none;
    cursor: pointer;
    transition: border var(--transition-fast), box-shadow var(--transition-fast);
    min-height: 36px;
}
.show-per-page select:focus {
    border-color: var(--accent);
    box-shadow: var(--shadow-focus);
}

/* ============================================
   АДАПТИВ
   Шкала: 1024 → 820 → 640 → 480 → 400
   ============================================ */

/* --- Планшет: фильтры в колонку, stat-cards 2×2 --- */
@media (max-width: 1024px) {
    .stat-cards {
        grid-template-columns: repeat(2, 1fr);
    }

    .table-filters {
        flex-direction: column;
        align-items: stretch;
        gap: 10px;
    }
    .filters-row { flex-direction: column; }
    .filter-group { min-width: 0; }
    .filter-select,
    .search-input { width: 100%; }
    .filters-actions { width: 100%; }
    .filters-actions .btn-outline { width: 100%; }
}

/* --- Мобильный планшет: карточки вместо таблицы --- */
@media (max-width: 820px) {
    .table-header { display: none; }

    .tr {
        grid-template-columns: 1fr;
        gap: 0;
        padding: 14px;
        border: 1px solid var(--border-light);
        border-radius: var(--radius-md);
        margin-bottom: 8px;
        background: var(--bg-primary);
        min-width: unset;
    }
    .tr:hover { background: var(--bg-primary); }
    .tr:last-child { border-bottom: 1px solid var(--border-light); }

    /* Moto-cell — шапка карточки */
    .moto-cell {
        order: 1;
        padding-bottom: 12px;
        margin-bottom: 8px;
        border-bottom: 1px solid var(--border-light);
    }

    /* Информационные строки */
    .td.owner-cell,
    .td.mileage-cell,
    .td.maintenance-cell,
    .td.date-cell {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        padding: 6px 0;
        font-size: 13px;
    }

    .td.owner-cell::before       { content: "Владелец";        color: var(--text-muted); font-weight: var(--fw-normal); flex-shrink: 0; }
    .td.mileage-cell::before     { content: "Пробег";           color: var(--text-muted); font-weight: var(--fw-normal); flex-shrink: 0; }
    .td.maintenance-cell::before { content: "Обслуживаний";     color: var(--text-muted); font-weight: var(--fw-normal); flex-shrink: 0; }
    .td.date-cell::before        { content: "Дата добавления";  color: var(--text-muted); font-weight: var(--fw-normal); flex-shrink: 0; }

    .owner-cell       { order: 2; }
    .mileage-cell     { order: 3; }
    .maintenance-cell { order: 4; }
    .date-cell        { order: 5; }

    /* Owner-info теперь горизонтально, т.к. label уже слева */
    .owner-info {
        flex-direction: row;
        align-items: baseline;
        gap: 6px;
        min-width: 0;
    }
    .owner-email { font-size: 11px; }

    /* Actions — отдельной строкой */
    .actions-cell {
        order: 6;
        margin-top: 8px;
        padding-top: 10px;
        border-top: 1px solid var(--border-light);
        justify-content: flex-end;
    }

    /* Пагинация */
    .table-paginate {
        flex-direction: column;
        align-items: stretch;
        gap: 12px;
    }
    .paginate-show { text-align: center; font-size: 13px; }
    .paginate-ui { justify-content: center; }
    .show-per-page { justify-content: center; }
}

/* --- Мобильные --- */
@media (max-width: 640px) {
    .table-section { padding: 12px; }

    .tr { padding: 12px; }

    .paginate-ui { gap: 6px; }
    .paginate-arrow { width: 34px; height: 34px; min-height: 34px; }
    .paginate-num {
        min-width: 32px;
        height: 32px;
        min-height: 32px;
        padding: 0 8px;
        font-size: 13px;
    }

    .show-per-page select { width: 100%; }
}

/* --- Узкие мобильные --- */
@media (max-width: 480px) {
    .moto-thumb {
        width: 34px;
        height: 34px;
        min-height: 34px;
    }
    .moto-placeholder {
        width: 34px;
        height: 34px;
        min-height: 34px;
        font-size: 14px;
    }
    .moto-name { font-size: 14px; }
    .moto-meta { font-size: 11px; }

    .stat-card { padding: 10px 12px; gap: 12px; }
    .card-icon {
        width: 40px;
        height: 40px;
        min-height: 40px;
        font-size: 16px;
    }
    .card-title { font-size: 12px; }
    .card-value { font-size: 18px; }

    /* Пагинация: оставляем только активную страницу + стрелки */
    .paginate-num:not(.active):not(.dots) { display: none; }
    .paginate-num.dots { display: none; }

    /* Owner-info снова вертикально, т.к. места мало */
    .owner-info {
        flex-direction: column;
        align-items: flex-end;
        gap: 0;
    }
    .owner-email { font-size: 11px; }
}

/* --- Экстра-узкие --- */
@media (max-width: 400px) {
    .stat-cards {
        grid-template-columns: 1fr;
        gap: 10px;
    }
    .stat-card { padding: 10px; }

    .actions-cell { justify-content: space-between; }
    .btn-small {
        width: 36px;
        height: 36px;
        min-height: 36px;
    }
}
</style>
