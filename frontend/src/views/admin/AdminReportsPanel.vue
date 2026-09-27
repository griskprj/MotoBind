<template>
  <div class="container">
    <LoadingOverlay :isLoading="loading" text="Загрузка жалоб..." />

    <Header title="Жалобы на посты" subtitle="Модерация контента и пользователей" />

    <section>
      <div class="stat-cards">
        <div class="stat-card">
          <div class="card-icon warning"><i class="fa fa-clock"></i></div>
          <div class="card-body">
            <p class="card-title">На рассмотрении</p>
            <p class="card-value">{{ stats.pending || 0 }}</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="card-icon success"><i class="fa fa-check"></i></div>
          <div class="card-body">
            <p class="card-title">Рассмотрено</p>
            <p class="card-value">{{ stats.resolved || 0 }}</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="card-icon danger"><i class="fa fa-times"></i></div>
          <div class="card-body">
            <p class="card-title">Отклонено</p>
            <p class="card-value">{{ stats.rejected || 0 }}</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="card-icon"><i class="fa fa-flag"></i></div>
          <div class="card-body">
            <p class="card-title">Всего</p>
            <p class="card-value">{{ stats.total || 0 }}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="filters-section">
      <div class="filters-row">
        <select v-model="filters.status" @change="applyFilters" class="filter-select">
          <option value="">Все статусы</option>
          <option value="pending">На рассмотрении</option>
          <option value="resolved">Рассмотрено</option>
          <option value="rejected">Отклонено</option>
        </select>
        <select v-model="filters.category" @change="applyFilters" class="filter-select">
          <option value="">Все категории</option>
          <option v-for="cat in categories" :key="cat.value" :value="cat.value">
            {{ cat.label }}
          </option>
        </select>
        <button class="btn-outline" @click="resetFilters">
          <i class="fa fa-refresh"></i> Сбросить
        </button>
      </div>
    </section>

    <section class="reports-list">
      <div v-if="reports.length === 0 && !loading" class="empty-state">
        <i class="fa fa-flag-o"></i>
        <h3>Жалоб нет</h3>
        <p class="empty-text">Все чисто — новых жалоб на посты пока нет</p>
      </div>

      <div
        v-for="report in reports"
        :key="report.id"
        class="report-card"
        @click="openDetails(report)"
      >
        <div class="report-main">
          <div class="report-badge" :class="'status-' + report.status">
            {{ statusLabel(report.status) }}
          </div>
          <div class="report-info">
            <div class="report-category">
              <i class="fa fa-exclamation-circle"></i>
              {{ report.category_label }}
            </div>
            <div class="report-meta">
              <span><i class="fa fa-user"></i> {{ report.reporter || '—' }}</span>
              <span class="dot">•</span>
              <span><i class="fa fa-calendar"></i> {{ formatDate(report.created_at) }}</span>
            </div>
          </div>
        </div>

        <div class="report-post-preview">
          <span class="preview-author">
            <i class="fa fa-motorcycle"></i>
            {{ report.post?.author || report.post_snapshot?.author || 'Автор удалён' }}
          </span>
          <p class="preview-text">
            {{ truncate(report.post?.content || report.post_snapshot?.content || '—', 90) }}
          </p>
        </div>

        <div class="report-right">
          <i class="fa fa-chevron-right"></i>
        </div>
      </div>
    </section>

    <!-- === PAGINATION === -->
    <div
      v-if="!loading && pagination.total > 0"
      class="table-paginate"
    >
      <p class="paginate-show">
        Показано
        {{ (pagination.current_page - 1) * pagination.per_page + 1 }}-
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
            @click="goToPage(page)"
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
        <select v-model.number="pagination.per_page" @change="changePerPage">
          <option :value="10">10</option>
          <option :value="20">20</option>
          <option :value="50">50</option>
          <option :value="100">100</option>
        </select>
      </div>
    </div>
  </div>

  <ReportDetailsModal
    v-if="selectedReport"
    :isOpen="showDetailsModal"
    :report="selectedReport"
    @close="closeDetails"
    @resolved="onResolved"
  />
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import Header from '@/components/Header.vue'
import LoadingOverlay from '@/components/LoadingOverlay.vue'
import ReportDetailsModal from '@/components/modals/admin/ReportDetailsModal.vue'
import { useToast } from '@/composables/useToast'
import api from '@/api/api'

const toast = useToast()

const loading = ref(false)
const reports = ref([])
const stats = ref({ total: 0, pending: 0, resolved: 0, rejected: 0 })
const pagination = ref({
  current_page: 1,
  per_page: 20,
  total: 0,
  pages: 0,
  has_prev: false,
  has_next: false,
})

const filters = ref({ status: 'pending', category: '' })
const categories = [
  { value: 'sexual_content', label: 'Контент сексуального характера' },
  { value: 'hate_speech', label: 'Разжигание межнациональной розни' },
  { value: 'extremism', label: 'Экстремистская символика' },
  { value: 'violence', label: 'Насилие' },
  { value: 'drugs', label: 'Пропаганда наркотиков' },
  { value: 'spam', label: 'Спам и мошенничество' },
  { value: 'other', label: 'Другое' },
]
const selectedReport = ref(null)
const showDetailsModal = ref(false)

let currentAbort = null
let isUnmounted = false

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

onMounted(() => {
  loadReports()
})

onBeforeUnmount(() => {
  isUnmounted = true
  if (currentAbort) currentAbort.abort()
})

async function loadReports() {
  if (currentAbort) currentAbort.abort()
  currentAbort = new AbortController()

  loading.value = true
  try {
    const params = {
      page: pagination.value.current_page,
      per_page: pagination.value.per_page,
      status: filters.value.status || undefined,
      category: filters.value.category || undefined,
    }

    const { data } = await api.get('/admin/reports', {
      params,
      signal: currentAbort.signal,
    })

    if (isUnmounted) return

    reports.value = data.reports || []
    Object.assign(stats.value, data.stats || {})

    pagination.value.current_page = data.current_page
    pagination.value.per_page = data.per_page
    pagination.value.total = data.total
    pagination.value.pages = data.pages
    pagination.value.has_prev = data.has_prev
    pagination.value.has_next = data.has_next
  } catch (err) {
    if (err?.name === 'CanceledError' || err?.code === 'ERR_CANCELED') return
    if (isUnmounted) return

    console.error(err)
    toast.error('Ошибка загрузки жалоб')
  } finally {
    if (!isUnmounted) loading.value = false
    currentAbort = null
  }
}

function applyFilters() {
  pagination.value.current_page = 1
  loadReports()
}

function resetFilters() {
  filters.value = { status: 'pending', category: '' }
  applyFilters()
}

function changePerPage() {
  pagination.value.current_page = 1
  loadReports()
}

function goToPage(page) {
  if (typeof page !== 'number') return
  if (page < 1 || page > pagination.value.pages) return
  if (page === pagination.value.current_page) return
  pagination.value.current_page = page
  loadReports()
}

function openDetails(report) {
  selectedReport.value = report
  showDetailsModal.value = true
}

function closeDetails() {
  showDetailsModal.value = false
  selectedReport.value = null
}

function onResolved() {
  closeDetails()
  loadReports()
}

function statusLabel(status) {
  return { pending: 'На рассмотрении', resolved: 'Рассмотрено', rejected: 'Отклонено' }[status] || status
}

function formatDate(date) {
  if (!date) return '—'
  return new Date(date).toLocaleString('ru-RU', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function truncate(text, len) {
  if (!text) return ''
  return text.length > len ? text.slice(0, len) + '...' : text
}

</script>
<style scoped>
/* ============================================
   STATISTIC CARDS
   ============================================ */
.stat-cards {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}

.stat-card {
    display: flex;
    gap: 16px;
    align-items: center;
    padding: 12px 14px;
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    transition: all var(--transition-base);
    min-width: 0;
}
.stat-card:hover {
    background: var(--accent-trans);
    border-color: var(--accent);
}

.card-icon {
    width: 48px;
    height: 48px;
    min-height: 48px; /* перебиваем reset.scss */
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--radius-md);
    background: var(--accent-trans);
    color: var(--accent-text);
    font-size: 18px;
    flex-shrink: 0;
}
.card-icon.warning { background: var(--warning-trans); color: var(--warning-text); }
.card-icon.success { background: var(--success-trans); color: var(--success-text); }
.card-icon.danger  { background: var(--danger-trans);  color: var(--danger-text); }

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
.filters-section { margin-bottom: 16px; }

.filters-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
}

.filter-select {
    padding: 8px 14px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: var(--radius-md);
    color: var(--text-primary);
    font-size: 14px;
    outline: none;
    min-width: 180px;
    cursor: pointer;
    transition: border var(--transition-fast), box-shadow var(--transition-fast);
    min-height: 40px;
}
.filter-select:focus {
    border-color: var(--accent);
    box-shadow: var(--shadow-focus);
}
.filter-select option { background: var(--bg-input); color: var(--text-primary); }

.btn-outline {
    padding: 8px 16px;
    background: transparent;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    color: var(--text-secondary);
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    font-size: 14px;
    transition: all var(--transition-base);
    min-height: 40px;
}
.btn-outline:hover {
    background: var(--border-light);
    border-color: var(--text-muted);
    color: var(--text-primary);
}
.btn-outline:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* ============================================
   REPORTS LIST
   ============================================ */
.reports-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.report-card {
    display: grid;
    grid-template-columns: 1fr 1.2fr 20px;
    gap: 16px;
    align-items: center;
    padding: 14px 18px;
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-lg);
    cursor: pointer;
    transition: all var(--transition-base);
    min-width: 0;
}
.report-card:hover {
    border-color: var(--accent);
    transform: translateX(4px);
}

.report-main {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    min-width: 0;
}

.report-badge {
    padding: 3px 10px;
    border-radius: var(--radius-full);
    font-size: 11px;
    font-weight: var(--fw-semibold);
    white-space: nowrap;
    flex-shrink: 0;
}
.status-pending  { background: var(--warning-trans); color: var(--warning-text); }
.status-resolved { background: var(--success-trans); color: var(--success-text); }
.status-rejected { background: var(--danger-trans);  color: var(--danger-text); }

.report-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
    min-width: 0;
}
.report-category {
    font-weight: var(--fw-semibold);
    font-size: 14px;
    color: var(--text-primary);
    display: flex;
    gap: 6px;
    align-items: center;
    overflow: hidden;
    text-overflow: ellipsis;
}
.report-category i { color: var(--danger-text); flex-shrink: 0; }

.report-meta {
    font-size: 12px;
    color: var(--text-muted);
    display: flex;
    gap: 6px;
    align-items: center;
    flex-wrap: wrap;
}
.report-meta .dot { opacity: 0.4; }

.report-post-preview { min-width: 0; }
.preview-author {
    font-size: 12px;
    color: var(--text-muted);
    display: inline-flex;
    gap: 4px;
    align-items: center;
    margin-bottom: 4px;
}
.preview-text {
    font-size: 13px;
    color: var(--text-secondary);
    margin: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    line-clamp: 2;
}

.report-right {
    color: var(--text-muted);
    transition: color var(--transition-base);
}
.report-card:hover .report-right { color: var(--accent-text); }

/* ============================================
   PAGINATION
   ============================================ */
.table-paginate {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
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
   EMPTY STATE
   ============================================ */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    border: 2px dashed var(--border-color);
    border-radius: var(--radius-lg);
}
.empty-state i {
    font-size: 40px;
    color: var(--accent);
    margin-bottom: 12px;
}
.empty-state h3 {
    color: var(--text-primary);
    margin: 0 0 6px;
    font-size: 20px;
}
.empty-text { color: var(--text-muted); font-size: 14px; margin: 0; }

/* ============================================
   АДАПТИВ
   Шкала: 1024 → 820 → 640 → 480 → 400
   ============================================ */

/* --- Планшет --- */
@media (max-width: 1024px) {
    .stat-cards { grid-template-columns: repeat(2, 1fr); }

    .report-card {
        grid-template-columns: 1fr;
        gap: 10px;
    }
    .report-right { display: none; }
}

/* --- Мобильный планшет --- */
@media (max-width: 820px) {
    .filters-row { flex-direction: column; align-items: stretch; }
    .filter-select,
    .btn-outline { width: 100%; min-width: 0; }

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
    .report-card { padding: 12px 14px; }
    .report-main { flex-direction: column; gap: 6px; }

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

/* --- Очень узкие --- */
@media (max-width: 480px) {
    .stat-cards { grid-template-columns: 1fr; gap: 10px; }
    .stat-card { padding: 10px 12px; gap: 12px; }
    .card-icon {
        width: 40px;
        height: 40px;
        min-height: 40px;
        font-size: 16px;
    }
    .card-title { font-size: 12px; }
    .card-value { font-size: 18px; }

    /* Оставляем только активную страницу + стрелки */
    .paginate-num:not(.active):not(.dots) { display: none; }
    .paginate-num.dots { display: none; }

    .empty-state { padding: 40px 16px; }
    .empty-state i { font-size: 32px; }
    .empty-state h3 { font-size: 17px; }
}
</style>
