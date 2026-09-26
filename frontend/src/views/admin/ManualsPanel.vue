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
        <div class="filter-results" v-if="filteredManuals.length > 0">
            <span>Найдено: {{ filteredManuals.length }} мануалов</span>
            <button class="clear-filters" @click="clearFilters" v-if="hasActiveFilters">
                <i class="fa fa-times"></i> Очистить фильтры
            </button>
        </div>

        <!-- === GRID OF MANUALS === -->
        <div v-if="filteredManuals && filteredManuals.length > 0" class="manuals-grid">
            <div
                class="manual-card"
                v-for="manual in filteredManuals"
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
import { computed, onMounted, ref } from 'vue'
import api from '@/api/api'
import Header from '@/components/Header.vue'
import LoadingOverlay from '@/components/LoadingOverlay.vue'
import ManualDetailsAdminModal from '@/components/modals/admin/ManualDetailsAdminModal.vue'
import { useToast } from '@/composables/useToast'

// ===== Composable =====
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

let searchTimeout = null

// ===== Computed =====
const filteredManuals = computed(() => {
    let items = [...manuals.value]

    // Таб фильтр
    if (selectedTab.value === 'moderate') {
        items = items.filter(m => m.status === 'moderate')
    } else if (selectedTab.value === 'approved') {
        items = items.filter(m => m.status === 'approved')
    } else if (selectedTab.value === 'rejected') {
        items = items.filter(m => m.status === 'rejected')
    }

    // Поиск
    if (searchQuery.value.trim()) {
        const query = searchQuery.value.toLowerCase().trim()
        items = items.filter(m =>
            m.title?.toLowerCase().includes(query) ||
            m.motorcycle?.toLowerCase().includes(query) ||
            m.author?.username?.toLowerCase().includes(query) ||
            m.description?.toLowerCase().includes(query)
        )
    }

    // Категория
    if (filterCategory.value) {
        items = items.filter(m => m.category === filterCategory.value)
    }

    // Мотоцикл
    if (filterMotorcycle.value) {
        items = items.filter(m => m.motorcycle === filterMotorcycle.value)
    }

    // Сложность
    if (filterDifficulty.value) {
        items = items.filter(m => m.difficult === filterDifficulty.value)
    }

    // Сортировка
    items = sortItems(items)

    return items
})

const hasActiveFilters = computed(() => {
    return searchQuery.value ||
        filterCategory.value ||
        filterMotorcycle.value ||
        filterDifficulty.value ||
        sortBy.value !== 'created_at_desc'
})

// ===== Lifecycle =====
onMounted(() => {
    loadData()
})

// ===== Methods =====
async function loadData() {
    try {
        loading.value = true

        // Загружаем все мануалы (без пагинации для админки)
        const manualsRes = await api.get('/manual/list?per_page=1000')
        manuals.value = manualsRes.data.manuals || []

        // Загружаем мотоциклы
        const motoRes = await api.get('/motorcycle/')
        motorcycles.value = motoRes.data || []
    } catch (err) {
        console.error('Failed load admin manuals data:', err)
        // 401 обрабатывается глобальным интерцептором
    } finally {
        loading.value = false
    }
}

function getTabCount(status) {
    if (status === 'all') return manuals.value.length
    return manuals.value.filter(m => m.status === status).length
}

function changeTab(tabName) {
    selectedTab.value = tabName
    // Не очищаем фильтры при смене таба
}

function applyFilters() {
    // Применяем фильтры (пересчёт computed)
}

function debouncedSearch() {
    clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => {
        // Применяем поиск (пересчёт computed)
    }, 400)
}

function openDetailsModal(manual) {
    selectedManual.value = manual
    showDetailsModal.value = true
}

function closeDetailsModal() {
    showDetailsModal.value = false
    selectedManual.value = null
}

async function handleApprove(manualId) {
    try {
        await api.post(`/admin/manual/${manualId}/approve`)
        const manual = manuals.value.find(m => m.id === manualId)
        if (manual) {
            manual.status = 'approved'
            manual.rejection_reason = null
        }
        closeDetailsModal()
        toast.success('Мануал успешно одобрен!')
    } catch (err) {
        console.error('Failed approve manual:', err)
        toast.error('Ошибка при одобрении мануала')
    }
}

async function handleReject(data) {
    try {
        await api.post(`/admin/manual/${data.id}/reject`, { reason: data.reason })
        const manual = manuals.value.find(m => m.id === data.id)
        if (manual) {
            manual.status = 'rejected'
            manual.rejection_reason = data.reason
        }
        closeDetailsModal()
        toast.warning('Мануал отклонён')
    } catch (err) {
        console.error('Failed reject manual:', err)
        toast.error('Ошибка при отклонении мануала')
    }
}

async function handleReconsider(manualId) {
    try {
        await api.post(`/admin/manual/${manualId}/reconsider`)
        const manual = manuals.value.find(m => m.id === manualId)
        if (manual) {
            manual.status = 'moderate'
            manual.rejection_reason = null
        }
        closeDetailsModal()
        toast.info('Мануал возвращён на проверку')
    } catch (err) {
        console.error('Failed reconsider manual:', err)
        toast.error('Ошибка при возврате мануала на проверку')
    }
}

async function handleDelete(manualId) {
    if (!confirm('Вы уверены, что хотите удалить этот мануал?')) return

    try {
        await api.delete(`/admin/manual/${manualId}`)
        manuals.value = manuals.value.filter(m => m.id !== manualId)
        closeDetailsModal()
        toast.success('Мануал удалён')
    } catch (err) {
        console.error('Failed delete manual:', err)
        toast.error('Ошибка при удалении мануала')
    }
}

function sortItems(items) {
    const sortFunctions = {
        'created_at_desc': (a, b) => new Date(b.created_at) - new Date(a.created_at),
        'created_at_asc': (a, b) => new Date(a.created_at) - new Date(b.created_at),
        'title_asc': (a, b) => a.title.localeCompare(b.title),
        'title_desc': (a, b) => b.title.localeCompare(a.title),
    }
    return items.sort(sortFunctions[sortBy.value] || sortFunctions['created_at_desc'])
}

function clearFilters() {
    searchQuery.value = ''
    filterCategory.value = ''
    filterMotorcycle.value = ''
    filterDifficulty.value = ''
    sortBy.value = 'created_at_desc'
}

function formatDate(dateString) {
    if (!dateString) return '—'
    try {
        const date = new Date(dateString)
        if (isNaN(date.getTime())) return '—'
        return date.toLocaleDateString('ru-RU', {
            day: '2-digit',
            month: 'short',
            year: 'numeric'
        })
    } catch {
        return '—'
    }
}

function getStatusLabel(status) {
    const labels = {
        'approved': 'Одобрен',
        'moderate': 'На проверке',
        'rejected': 'Отклонён'
    }
    return labels[status] || status
}

function getCategory(category) {
    const categories = {
        'engine': 'Двигатель',
        'drive': 'Привод',
        'steering': 'Рулевое управление',
        'suspension': 'Подвеска',
        'electronics': 'Электроника',
        'wheel': 'Колеса / Шины',
        'brakes': 'Тормозная система',
        'fuel': 'Топливная система',
        'cooling': 'Система охлаждения'
    }
    return categories[category] || category
}

function getDifficulty(difficult) {
    const difficulties = {
        'easy': 'Легко',
        'medium': 'Средне',
        'hard': 'Сложно'
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
}
</style>
