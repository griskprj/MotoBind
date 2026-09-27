<template>
    <div class="container">
        <LoadingOverlay :isLoading="loading" text="Загрузка мануалов..."/>

        <!-- === HEADER === -->
        <Header
            title="Мануалы"
            subtitle="Управление мануалами и модерация"
        />

        <!-- === TABS & FILTERS === -->
        <div class="controls-wrapper">
            <div class="tabs">
                <div
                    @click="changeTab('all')"
                    class="tab"
                    :class="selectedTab === 'all' ? 'active' : ''"
                >
                    <p>Все <span class="tab-count">{{ getTabCount('all') }}</span></p>
                </div>
                <div
                    @click="changeTab('moderate')"
                    class="tab"
                    :class="selectedTab === 'moderate' ? 'active' : ''"
                >
                    <p>На проверке <span class="tab-count">{{ getTabCount('moderate') }}</span></p>
                </div>
                <div
                    @click="changeTab('approved')"
                    class="tab"
                    :class="selectedTab === 'approved' ? 'active' : ''"
                >
                    <p>Одобренные <span class="tab-count">{{ getTabCount('approved') }}</span></p>
                </div>
                <div
                    @click="changeTab('rejected')"
                    class="tab"
                    :class="selectedTab === 'rejected' ? 'active' : ''"
                >
                    <p>Отклонённые <span class="tab-count">{{ getTabCount('rejected') }}</span></p>
                </div>
            </div>

            <div class="filters">
                <div class="filter-group">
                    <input
                        type="text"
                        v-model="searchQuery"
                        placeholder="Поиск по названию, автору..."
                        class="search-input"
                        @input="debouncedSearch"
                    >
                </div>

                <select v-model="filterCategory" class="filter-select" @change="applyFilters">
                    <option value="">Все категории</option>
                    <option value="engine">Двигатель</option>
                    <option value="drive">Привод</option>
                    <option value="steering">Рулевое управление</option>
                    <option value="suspension">Подвеска</option>
                    <option value="electronics">Электроника</option>
                    <option value="wheel">Колеса / Шины</option>
                    <option value="brakes">Тормозная система</option>
                    <option value="fuel">Топливная система</option>
                    <option value="cooling">Система охлаждения</option>
                </select>

                <select v-model="filterMotorcycle" class="filter-select" @change="applyFilters">
                    <option value="">Все мотоциклы</option>
                    <option v-for="moto in motorcycles" :key="moto.id" :value="moto.name">
                        {{ moto.name }}
                    </option>
                </select>

                <select v-model="filterDifficulty" class="filter-select" @change="applyFilters">
                    <option value="">Все сложности</option>
                    <option value="easy">Легко</option>
                    <option value="medium">Средне</option>
                    <option value="hard">Сложно</option>
                </select>

                <select v-model="sortBy" class="filter-select" @change="applyFilters">
                    <option value="created_at_desc">По дате (новые)</option>
                    <option value="created_at_asc">По дате (старые)</option>
                    <option value="title_asc">По названию (А-Я)</option>
                    <option value="title_desc">По названию (Я-А)</option>
                </select>
            </div>
        </div>

        <!-- Результаты фильтрации -->
        <div class="filter-results" v-if="pagination.total > 0">
        <span>Найдено: {{ pagination.total }} мануалов</span>
        <button class="clear-filters" @click="clearFilters" v-if="hasActiveFilters">
            <i class="fa fa-times"></i> Очистить фильтры
        </button>
        </div>

        <!-- === GRID OF MANUALS === -->
        <div v-if="manuals && manuals.length > 0" class="manuals-grid">
            <div
                class="manual-card"
                v-for="manual in manuals"
                :key="manual.id"
                @click="openDetailsModal(manual)"
            >
                <div class="card-header">
                    <span class="card-title">{{ manual.title }}</span>
                    <span
                        class="status-badge"
                        :class="{
                            'badge-green': manual.status === 'approved',
                            'badge-warning': manual.status === 'moderate',
                            'badge-danger': manual.status === 'rejected'
                        }"
                    >
                        {{ getStatusLabel(manual.status) }}
                    </span>
                </div>

                <div class="card-body">
                    <div class="card-meta">
                        <div class="meta-item">
                            <i class="fa fa-motorcycle"></i> {{ manual.motorcycle }}
                        </div>
                        <div class="meta-item">
                            <i class="fa fa-tags"></i> {{ getCategory(manual.category) }}
                        </div>
                        <div class="meta-item">
                            <i class="fa fa-signal"></i> {{ getDifficulty(manual.difficult) }}
                        </div>
                        <div class="meta-item">
                            <i class="fa fa-user"></i> {{ manual.author?.username || 'Неизвестно' }}
                        </div>
                        <div class="meta-item" v-if="manual.time_estimate">
                            <i class="fa fa-clock-o"></i> {{ manual.time_estimate }}
                        </div>
                        <div class="meta-item" v-if="manual.interval">
                            <i class="fa fa-repeat"></i> {{ manual.interval }}
                        </div>
                        <div class="meta-item">
                            <i class="fa fa-calendar"></i> {{ formatDate(manual.created_at) }}
                        </div>
                    </div>
                </div>

                <div class="card-footer">
                    <span class="steps-count">
                        <i class="fa fa-list-ol"></i> {{ manual.steps?.length || 0 }} шагов
                    </span>
                    <div class="card-actions">
                        <span class="click-hint">Подробнее <i class="fa fa-chevron-right"></i></span>
                    </div>
                </div>
            </div>
        </div>

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
            <option :value="6">6</option>
            <option :value="12">12</option>
            <option :value="24">24</option>
            <option :value="48">48</option>
            </select>
        </div>
        </div>

        <!-- Empty State -->
        <div v-else class="empty-state">
            <div class="empty-header">
                <i class="fa fa-book"></i>
                <p class="empty-title">Мануалы не найдены</p>
            </div>
            <div class="empty-body">
                <p class="empty-text" v-if="hasActiveFilters">
                    Попробуйте изменить параметры фильтрации
                </p>
                <p class="empty-text" v-else>
                    Список мануалов пуст
                </p>
            </div>
        </div>
    </div>

    <!-- === MODAL (Details + Actions) === -->
    <ManualDetailsAdminModal
        v-if="selectedManual"
        :isOpen="showDetailsModal"
        :manual="selectedManual"
        @close="closeDetailsModal"
        @approve="handleApprove"
        @reject="handleReject"
        @reconsider="handleReconsider"
        @delete="handleDelete"
    />
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import api from '@/api/api'
import Header from '@/components/Header.vue'
import LoadingOverlay from '@/components/LoadingOverlay.vue'
import ManualDetailsAdminModal from '@/components/modals/admin/ManualDetailsAdminModal.vue'
import { useToast } from '@/composables/useToast'

const toast = useToast()

// ===== State =====
const loading = ref(false)
const manuals = ref([])
const motorcycles = ref([])

const selectedManual = ref(null)
const showDetailsModal = ref(false)

// Фильтры
const searchQuery = ref('')
const filterCategory = ref('')
const filterMotorcycle = ref('')
const filterDifficulty = ref('')
const sortBy = ref('created_at_desc')
const selectedTab = ref('moderate')

// Пагинация
const pagination = ref({
    current_page: 1,
    per_page: 12,
    total: 0,
    pages: 0,
    has_prev: false,
    has_next: false,
})

// Счётчики вкладок
const tabCounts = ref({
    all: 0,
    moderate: 0,
    approved: 0,
    rejected: 0,
})

let searchTimeout = null

// ===== Computed =====
const hasActiveFilters = computed(() =>
    !!searchQuery.value ||
    !!filterCategory.value ||
    !!filterMotorcycle.value ||
    !!filterDifficulty.value ||
    sortBy.value !== 'created_at_desc'
)

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

// ===== Lifecycle =====
onMounted(async () => {
    await Promise.all([
        loadManuals(),
        loadMotorcycles(),
        loadTabCounts(),
    ])
})

// ===== Загрузка данных =====
async function loadManuals() {
    loading.value = true
    try {
        const params = {
            page: pagination.value.current_page,
            per_page: pagination.value.per_page,
            tab: 'all',
            search: searchQuery.value || '',
            motorcycle: filterMotorcycle.value || '',
            category: filterCategory.value || '',
            difficult: filterDifficulty.value || '',
            sort_by: sortBy.value,
            status: selectedTab.value === 'all' ? '' : selectedTab.value,
        }

        // Убираем пустые
        Object.keys(params).forEach(k => {
            if (!params[k]) delete params[k]
        })

        const { data } = await api.get('/manual/list', { params })

        manuals.value = data.manuals || []
        pagination.value = {
            current_page: data.current_page,
            per_page: data.per_page,
            total: data.total,
            pages: data.pages,
            has_prev: data.has_prev,
            has_next: data.has_next,
        }
    } catch (err) {
        console.error('Failed load manuals:', err)
        toast.error('Не удалось загрузить мануалы')
    } finally {
        loading.value = false
    }
}

async function loadMotorcycles() {
    try {
        const { data } = await api.get('/motorcycle/')
        motorcycles.value = data || []
    } catch (err) {
        console.error('Failed load motorcycles:', err)
    }
}

async function loadTabCounts() {
    const statuses = ['', 'moderate', 'approved', 'rejected']
    try {
        const results = await Promise.all(
            statuses.map(status =>
                api.get('/manual/list', {
                    params: { per_page: 1, status, tab: 'all' },
                })
            )
        )
        tabCounts.value = {
            all: results[0].data.total || 0,
            moderate: results[1].data.total || 0,
            approved: results[2].data.total || 0,
            rejected: results[3].data.total || 0,
        }
    } catch (err) {
        console.error('Failed load tab counts:', err)
    }
}

// ===== Управление вкладками =====
function changeTab(tabName) {
    if (selectedTab.value === tabName) return
    selectedTab.value = tabName
    pagination.value.current_page = 1
    loadManuals()
}

function getTabCount(status) {
    return tabCounts.value[status] ?? 0
}

// ===== Фильтры =====
function applyFilters() {
    pagination.value.current_page = 1
    loadManuals()
}

function debouncedSearch() {
    clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => {
        applyFilters()
    }, 400)
}

function clearFilters() {
    searchQuery.value = ''
    filterCategory.value = ''
    filterMotorcycle.value = ''
    filterDifficulty.value = ''
    sortBy.value = 'created_at_desc'
    pagination.value.current_page = 1
    loadManuals()
}

// ===== Пагинация =====
function goToPage(page) {
    if (typeof page !== 'number') return
    if (page < 1 || page > pagination.value.pages) return
    if (page === pagination.value.current_page) return
    pagination.value.current_page = page
    loadManuals()
}

function changePerPage() {
    pagination.value.current_page = 1
    loadManuals()
}

// ===== Модалка =====
function openDetailsModal(manual) {
    selectedManual.value = manual
    showDetailsModal.value = true
}

function closeDetailsModal() {
    showDetailsModal.value = false
    selectedManual.value = null
}

// ===== Действия =====
async function handleApprove(manualId) {
    try {
        await api.post(`/admin/manual/${manualId}/approve`)
        closeDetailsModal()
        toast.success('Мануал успешно одобрен!')
        await Promise.all([loadManuals(), loadTabCounts()])
    } catch (err) {
        console.error('Failed approve manual:', err)
        toast.error('Ошибка при одобрении мануала')
    }
}

async function handleReject(data) {
    try {
        await api.post(`/admin/manual/${data.id}/reject`, { reason: data.reason })
        closeDetailsModal()
        toast.warning('Мануал отклонён')
        await Promise.all([loadManuals(), loadTabCounts()])
    } catch (err) {
        console.error('Failed reject manual:', err)
        toast.error('Ошибка при отклонении мануала')
    }
}

async function handleReconsider(manualId) {
    try {
        await api.post(`/admin/manual/${manualId}/reconsider`)
        closeDetailsModal()
        toast.info('Мануал возвращён на проверку')
        await Promise.all([loadManuals(), loadTabCounts()])
    } catch (err) {
        console.error('Failed reconsider manual:', err)
        toast.error('Ошибка при возврате мануала на проверку')
    }
}

async function handleDelete(manualId) {
    if (!confirm('Вы уверены, что хотите удалить этот мануал?')) return

    try {
        await api.delete(`/admin/manual/${manualId}`)
        closeDetailsModal()
        toast.success('Мануал удалён')

        if (manuals.value.length === 1 && pagination.value.current_page > 1) {
            pagination.value.current_page -= 1
        }

        await Promise.all([loadManuals(), loadTabCounts()])
    } catch (err) {
        console.error('Failed delete manual:', err)
        toast.error('Ошибка при удалении мануала')
    }
}

// ===== Хелперы =====
function formatDate(dateString) {
    if (!dateString) return '—'
    try {
        const date = new Date(dateString)
        if (isNaN(date.getTime())) return '—'
        return date.toLocaleDateString('ru-RU', {
            day: '2-digit',
            month: 'short',
            year: 'numeric',
        })
    } catch {
        return '—'
    }
}

function getStatusLabel(status) {
    const labels = {
        approved: 'Одобрен',
        moderate: 'На проверке',
        rejected: 'Отклонён',
    }
    return labels[status] || status
}

function getCategory(category) {
    const categories = {
        engine: 'Двигатель',
        drive: 'Привод',
        steering: 'Рулевое управление',
        suspension: 'Подвеска',
        electronics: 'Электроника',
        wheel: 'Колеса / Шины',
        brakes: 'Тормозная система',
        fuel: 'Топливная система',
        cooling: 'Система охлаждения',
    }
    return categories[category] || category
}

function getDifficulty(difficult) {
    const difficulties = {
        easy: 'Легко',
        medium: 'Средне',
        hard: 'Сложно',
    }
    return difficulties[difficult] || difficult
}
</script>

<style scoped>
.controls-wrapper {
    margin-bottom: 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 16px;
}

.tabs {
    display: flex;
    gap: 24px;
    border-bottom: 1px solid var(--border-light);
    padding-bottom: 12px;
    flex-wrap: wrap;
}

.tab {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-muted);
    cursor: pointer;
    position: relative;
    padding-bottom: 12px;
    transition: 0.2s;
}

.tab:hover {
    color: var(--text-primary);
}

.tab.active {
    color: var(--accent-text);
}

.tab.active::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    right: 0;
    height: 2px;
    background: var(--accent);
    border-radius: 2px;
}

.tab-count {
    display: inline-block;
    background: var(--bg-secondary);
    padding: 0 8px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
    color: var(--text-muted);
    margin-left: 4px;
}

.tab.active .tab-count {
    background: var(--accent-trans);
    color: var(--accent-text);
}

.filters {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    align-items: center;
    flex: 1;
}

.filter-group {
    flex: 1;
    min-width: 160px;
}

.search-input {
    width: 100%;
    padding: 8px 14px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: 10px;
    color: var(--text-primary);
    font-size: 14px;
    outline: none;
    transition: border 0.2s;
}

.search-input:focus {
    border-color: var(--accent);
}

.search-input::placeholder {
    color: var(--text-muted);
}

.filter-select {
    padding: 8px 14px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: 10px;
    color: var(--text-primary);
    font-size: 14px;
    outline: none;
    cursor: pointer;
    transition: border 0.2s;
    min-width: 140px;
    appearance: none;
    background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2364748B' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: right 10px center;
    background-size: 14px;
    padding-right: 36px;
}

.filter-select:focus {
    border-color: var(--accent);
}

.filter-select option {
    background: var(--bg-input);
    color: var(--text-primary);
}

.filter-results {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    background: var(--accent-trans);
    border-radius: 8px;
    font-size: 13px;
    color: var(--text-muted);
    margin-bottom: 16px;
}

.clear-filters {
    background: transparent;
    border: none;
    color: var(--accent-text);
    cursor: pointer;
    font-size: 13px;
    transition: color 0.2s;
}

.clear-filters:hover {
    color: var(--accent);
}

/* ===== GRID ===== */
.manuals-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 16px;
}

.manual-card {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: 14px;
    padding: 18px 20px;
    cursor: pointer;
    transition: border-color 0.2s, transform 0.2s;
    display: flex;
    flex-direction: column;
}

.manual-card:hover {
    border-color: var(--accent);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 12px;
}

.card-title {
    font-size: 16px;
    font-weight: 600;
    line-height: 1.3;
    flex: 1;
    color: var(--text-primary);
}

.status-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    white-space: nowrap;
    flex-shrink: 0;
}

.badge-green {
    background: var(--success-trans);
    color: var(--success-text);
}

.badge-warning {
    background: var(--warning-trans);
    color: var(--warning-text);
}

.badge-danger {
    background: var(--danger-trans);
    color: var(--danger-text);
}

.card-body {
    flex: 1;
    margin-bottom: 12px;
}

.card-meta {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4px 16px;
}

.meta-item {
    font-size: 13px;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 8px;
}

.meta-item i {
    width: 16px;
    text-align: center;
    color: var(--text-muted);
    flex-shrink: 0;
}

.card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 12px;
    border-top: 1px solid var(--border-light);
}

.steps-count {
    font-size: 13px;
    color: var(--text-muted);
}

.steps-count i {
    margin-right: 6px;
}

.click-hint {
    font-size: 13px;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 4px;
    transition: color 0.2s;
}

.manual-card:hover .click-hint {
    color: var(--accent-text);
}

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

/* ===== EMPTY STATE ===== */
.empty-state {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: 16px;
    padding: 60px 20px;
    text-align: center;
}

.empty-header i {
    font-size: 48px;
    color: var(--border-color);
    margin-bottom: 16px;
}

.empty-title {
    font-size: 20px;
    font-weight: 600;
    margin: 0 0 8px 0;
    color: var(--text-primary);
}

.empty-text {
    color: var(--text-muted);
    font-size: 14px;
    margin: 4px 0;
}

/* ===== MEDIA QUERIES ===== */
@media (max-width: 1024px) {
    .controls-wrapper {
        flex-direction: column;
        align-items: stretch;
    }

    .filters {
        flex-wrap: wrap;
    }

    .filter-select {
        flex: 1;
        min-width: 120px;
    }
}

@media (max-width: 820px) {
    .tabs {
        overflow-x: auto;
        gap: 16px;
        padding-bottom: 8px;
        white-space: nowrap;
        scrollbar-width: none;
    }

    .tabs::-webkit-scrollbar {
        display: none;
    }

    .card-meta {
        grid-template-columns: 1fr;
    }

    .table-paginate {
        flex-direction: column;
        align-items: stretch;
        gap: 12px;
    }
    .paginate-show { text-align: center; font-size: 13px; }
    .paginate-ui { justify-content: center; }
    .show-per-page { justify-content: center; }
}

@media (max-width: 640px) {
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

@media (max-width: 480px) {
    .filters {
        flex-direction: column;
    }

    .filter-select {
        width: 100%;
        min-width: unset;
    }

    .manuals-grid {
        grid-template-columns: 1fr;
    }

    .manual-card {
        padding: 14px 16px;
    }

    .paginate-num:not(.active):not(.dots) { display: none; }
    .paginate-num.dots { display: none; }
}
</style>
