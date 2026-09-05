<template>
    <div class="maintenance-page">
        <LoadingOverlay :isLoading="loading" text="Загрузка обслуживаний..."/>

        <div class="container">
            <!-- === HEADER === -->
            <Header
                title="Обслуживание"
                subtitle="Управляйте обслуживанием своих мотоциклов"
            />

            <!-- === STATISTIC SECTION === -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon total">
                        <i class="fa fa-wrench"></i>
                    </div>
                    <div class="stat-info">
                        <span class="stat-label">Всего обслуживаний</span>
                        <span class="stat-value">{{ allMaintenancesCount }}</span>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-icon completed">
                        <i class="fa fa-check"></i>
                    </div>
                    <div class="stat-info">
                        <span class="stat-label">Выполнено</span>
                        <span class="stat-value">{{ completedMaintenances.length }}</span>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-icon planned">
                        <i class="fa fa-clock"></i>
                    </div>
                    <div class="stat-info">
                        <span class="stat-label">Запланировано</span>
                        <span class="stat-value">{{ plannedMaintenances.length }}</span>
                    </div>
                </div>

                <div class="stat-card" :class="{ 'stat-danger': overdueMaintenances.length > 0 }">
                    <div class="stat-icon overdue">
                        <i class="fa fa-exclamation-triangle"></i>
                    </div>
                    <div class="stat-info">
                        <span class="stat-label">Просрочено</span>
                        <span class="stat-value" :class="{ 'text-danger': overdueMaintenances.length > 0 }">
                            {{ overdueMaintenances.length }}
                        </span>
                    </div>
                </div>
            </div>

            <!-- === FILTERS === -->
            <div class="filters-section">
                <div class="tabs-wrapper">
                    <div class="tabs">
                        <div class="tabs-btn">
                            <button 
                                v-for="tab in tabs" 
                                :key="tab.value"
                                @click="changeTab(tab.value)" 
                                class="tab"
                                :class="{ active: selectedTab === tab.value }"
                            >
                                <i :class="tab.icon"></i>
                                {{ tab.label }}
                                <span class="tab-count" v-if="tab.value === 'all'">{{ allMaintenancesCount }}</span>
                                <span class="tab-count" v-else-if="tab.value === 'planned'">{{ plannedMaintenances.length + overdueMaintenances.length }}</span>
                                <span class="tab-count" v-else-if="tab.value === 'history'">{{ completedMaintenances.length }}</span>
                            </button>
                        </div>
                        <button 
                            class="outline-btn"
                            style="padding: 10px 24px;"
                            @click="showAddMaintenanceModal = true"
                        >
                            <i class="fa fa-plus" style="min-width: 14px; margin-right: 0px;"></i> Добавить обслуживание
                        </button>
                    </div>

                </div>

                <div class="filters">
                    <div class="filter-group">
                        <div class="search-wrapper">
                            <i class="fa fa-search"></i>
                            <input 
                                type="text" 
                                v-model="searchQuery" 
                                placeholder="Поиск по названию, описанию, мотоциклу..."
                                class="search-input"
                            >
                            <button v-if="searchQuery" @click="searchQuery = ''" class="clear-search">
                                <i class="fa fa-times"></i>
                            </button>
                        </div>
                    </div>
                    <div class="filter-group">
                        <select v-model="filterMotorcycle" class="filter-select">
                            <option value="">Все мотоциклы</option>
                            <option v-for="motorcycle in motorcycles" :key="motorcycle.id" :value="motorcycle.id">
                                {{ motorcycle.name }}
                            </option>
                        </select>
                        <select v-model="filterStatus" class="filter-select">
                            <option value="">Все статусы</option>
                            <option value="completed">✅ Выполнено</option>
                            <option value="planned">⏳ Запланировано</option>
                            <option value="overdue">⚠️ Просрочено</option>
                        </select>
                        <select v-model="sortBy" class="filter-select">
                            <option value="date_desc">📅 По дате (новые)</option>
                            <option value="date_asc">📅 По дате (старые)</option>
                            <option value="mileage_desc">📊 По пробегу (макс)</option>
                            <option value="mileage_asc">📊 По пробегу (мин)</option>
                            <option value="cost_desc">💰 По стоимости (макс)</option>
                            <option value="cost_asc">💰 По стоимости (мин)</option>
                        </select>
                    </div>
                </div>

                <div class="filter-results" v-if="filteredMaintenances.length > 0 && hasActiveFilters">
                    <span>
                        <i class="fa fa-filter"></i>
                        Найдено: {{ filteredMaintenances.length }} записей
                    </span>
                    <button class="clear-filters" @click="clearFilters">
                        <i class="fa fa-times"></i> Очистить фильтры
                    </button>
                </div>
            </div>

            <!-- === MAINTENANCE LIST === -->
            <div v-if="filteredMaintenances && filteredMaintenances.length > 0" class="maintenance-list">
                <div 
                    v-for="maintenance in filteredMaintenances"
                    :key="maintenance.id"
                    class="maintenance-card"
                    @click="openDetailsMaintenance(maintenance)"
                >
                    <div class="card-left">
                        <div class="card-icon" :class="getStatusIconClass(maintenance.status)">
                            <i :class="getStatusIcon(maintenance.status)"></i>
                        </div>
                        <div class="card-content">
                            <div class="card-header-row">
                                <h3 class="card-title">{{ maintenance.title }}</h3>
                                <span class="card-date">
                                    <i class="fa fa-calendar-alt"></i>
                                    {{ getMaintenanceDate(maintenance) }}
                                </span>
                            </div>
                            <div class="card-description" v-if="maintenance.description">
                                {{ maintenance.description }}
                            </div>
                            <div class="card-meta">
                                <span class="meta-item">
                                    <i class="fa fa-motorcycle"></i>
                                    {{ maintenance.moto_name || '—' }}
                                </span>
                                <span class="meta-item">
                                    <i class="fa-solid fa-gauge-high"></i>
                                    {{ getMaintenanceMileage(maintenance) }}
                                </span>
                                <span class="meta-item" v-if="maintenance.cost">
                                    <i class="fa fa-ruble-sign"></i>
                                    {{ formatCost(maintenance.cost) }}
                                </span>
                                <span class="badge" :class="getStatusBadgeClass(maintenance.status)">
                                    {{ getStatusLabel(maintenance.status) }}
                                </span>
                            </div>
                        </div>
                    </div>
                    <div class="card-right">
                        <i class="fa fa-chevron-right"></i>
                    </div>
                </div>
            </div>

            <!-- === EMPTY STATE === -->
            <div v-else class="empty-state">
                <i class="fa fa-wrench"></i>
                <h3 v-if="hasActiveFilters">Ничего не найдено</h3>
                <h3 v-else>Нет записей обслуживания</h3>
                <p class="empty-text" v-if="hasActiveFilters">
                    Попробуйте изменить параметры фильтрации
                </p>
                <p class="empty-text" v-else>
                    Начните вести учёт обслуживания своих мотоциклов
                </p>
                <button v-if="!hasActiveFilters" @click="showAddMaintenanceModal = true" class="btn-primary">
                    <i class="fa fa-plus"></i>
                    Добавить обслуживание
                </button>
                <button v-else @click="clearFilters" class="btn-secondary">
                    Сбросить фильтры
                </button>
            </div>
        </div>

        <!-- MODALS -->
        <AddMaintenanceModal
            :isOpen="showAddMaintenanceModal"
            :motorcycles="motorcycles"
            @submit="addMaintenance"
            @close="showAddMaintenanceModal = false"
        />

        <MaintenanceDetailsModal
            v-if="selectedMaintenance"
            :isOpen="showDetailsMaintenanceModal"
            :motoName="selectedMotorcycle?.name"
            :motorcycle="selectedMotorcycle"
            :motorcycles="motorcycles"
            :maintenance="selectedMaintenance"
            @delete="deleteMaintenance"
            @save="editMaintenance"
            @mark="markMaintenance"
            @updateMaintenance="updateMaintenance"
            @close="closeDetailsMaintenance"
        />
    </div>
</template>

<script>
import api from '../api/api';
import formatDate from '../utils/DateFormatter.js';
import AddMaintenanceModal from '../components/modals/maintenance/AddMaintenanceModal.vue'
import MaintenanceDetailsModal from '../components/modals/maintenance/MaintenanceDetailsModal.vue';
import Header from '../components/Header.vue'
import LoadingOverlay from '../components/LoadingOverlay.vue';

export default {
    components: {
        AddMaintenanceModal,
        MaintenanceDetailsModal,
        Header,
        LoadingOverlay
    },

    data() {
        return {
            motorcycles: [],
            allMaintenances: [],
            
            selectedMaintenance: null,
            selectedMotorcycle: null,
            
            // Фильтры
            searchQuery: '',
            filterMotorcycle: '',
            filterStatus: '',
            sortBy: 'date_desc',
            
            // Статистика
            allMaintenancesCount: 0,
            selectedTab: 'all',

            // Модалки
            showAddMaintenanceModal: false,
            showDetailsMaintenanceModal: false,

            loading: false,
        }
    },

    computed: {
        tabs() {
            return [
                { value: 'all', label: 'Все записи', icon: 'fa fa-list' },
                { value: 'planned', label: 'Плановые', icon: 'fa fa-clock' },
                { value: 'history', label: 'История', icon: 'fa fa-history' },
            ]
        },

        completedMaintenances() {
            return this.allMaintenances.filter(m => m.status === 'completed')
        },
        plannedMaintenances() {
            return this.allMaintenances.filter(m => m.status === 'planned')
        },
        overdueMaintenances() {
            return this.allMaintenances.filter(m => m.status === 'overdue')
        },

        filteredMaintenances() {
            let items = [...this.allMaintenances]
            
            // Поиск
            if (this.searchQuery.trim()) {
                const query = this.searchQuery.toLowerCase().trim()
                items = items.filter(m => 
                    m.title?.toLowerCase().includes(query) ||
                    m.description?.toLowerCase().includes(query) ||
                    m.moto_name?.toLowerCase().includes(query)
                )
            }

            // Табы
            if (this.selectedTab === 'planned') {
                items = items.filter(m => m.status === 'planned' || m.status === 'overdue')
            } else if (this.selectedTab === 'history') {
                items = items.filter(m => m.status === 'completed')
            }
            
            // Фильтры
            if (this.filterMotorcycle) {
                items = items.filter(m => m.moto_id === this.filterMotorcycle)
            }
            
            if (this.filterStatus) {
                items = items.filter(m => m.status === this.filterStatus)
            }
            
            // Сортировка
            items = this.sortItems(items)
            
            return items
        },
        
        hasActiveFilters() {
            return this.searchQuery || this.filterMotorcycle || this.filterStatus || this.selectedTab !== 'all'
        }
    },

    methods: {
        async loadData() {
            try {
                this.loading = true

                const response = await api.get('/statistic/maintenance')
                
                this.motorcycles = response.data.motorcycles || []
                
                const history = response.data.history_maintenances || []
                const planned = response.data.planned_maintenances || []
                this.allMaintenances = [...history, ...planned]
                
                this.allMaintenancesCount = response.data.all_maintenances_count || 0
                
            } catch (err) {
                console.error('Failed load maintenance data:', err)
                alert('Ошибка загрузки данных')
            } finally {
                this.loading = false
            }
        },

        async addMaintenance(formData) {
            try {
                await api.post('/maintenance/', formData)
                await this.loadData()
                this.showAddMaintenanceModal = false
                this.$toast?.success('Обслуживание добавлено')
            } catch (err) {
                console.error('Failed create maintenance:', err)
                alert(err.response?.data?.error || 'Ошибка при добавлении обслуживания')
            }
        },

        editMaintenance() {
            this.loadData()
        },

        async deleteMaintenance(id) {
            try {
                await api.delete(`/maintenance/${id}`)
                await this.loadData()
                this.showDetailsMaintenanceModal = false
                this.$toast?.success('Обслуживание удалено')
            } catch (err) {
                console.error('Failed delete maintenance:', err)
                alert(err.response?.data?.error || 'Ошибка удаления обслуживания')
            }
        },

        async markMaintenance(formData) {
            try {
                if (!formData || !formData.id) {
                    console.error('No maintenance ID provided');
                    this.$toast?.error('Ошибка: отсутствует ID обслуживания');
                    return;
                }

                const payload = {
                    completed_mileage: formData.completed_mileage || formData.mileage || 0,
                    completed_date: formData.completed_date || new Date().toISOString().split('T')[0],
                    cost: formData.cost || 0,
                    is_repeat: formData.isRepeat || false,
                    interval: formData.interval || null,
                    interval_days: formData.interval_days || null
                };

                await api.post(`/maintenance/${formData.id}/complete`, payload);
                
                this.$toast?.success('Обслуживание успешно завершено!');
                await this.loadData();
                
                this.selectedMaintenance = null;
                this.selectedMotorcycle = null;
            } catch (err) {
                console.error('Failed to complete maintenance:', err);
                const errorMsg = err.response?.data?.error || 'Ошибка при завершении обслуживания';
                this.$toast?.error(errorMsg);
            }
        },

        updateMaintenance() {
            this.loadData()
        },

        changeTab(tabName) {
            this.selectedTab = tabName
        },

        openDetailsMaintenance(maintenance) {
            this.selectedMaintenance = maintenance
            this.selectedMotorcycle = this.motorcycles.find(m => m.id === maintenance.moto_id)
            this.showDetailsMaintenanceModal = true
        },

        closeDetailsMaintenance() {
            this.selectedMaintenance = null
            this.selectedMotorcycle = null
            this.showDetailsMaintenanceModal = false
        },

        getMaintenanceDate(maintenance) {
            return formatDate(maintenance.completed_date || maintenance.planned_date || maintenance.created_at)
        },

        getMaintenanceMileage(maintenance) {
            if (maintenance.completed_mileage) {
                return `${maintenance.completed_mileage} км`
            }
            if (maintenance.planned_mileage) {
                return `(план) ${maintenance.planned_mileage} км`
            }
            return '—'
        },

        formatCost(value) {
            if (!value) return '0 ₽'
            if (value >= 1000) {
                return (value / 1000).toFixed(1) + ' тыс. ₽'
            }
            return Math.round(value) + ' ₽'
        },

        sortItems(items) {
            const sortFunctions = {
                'date_desc': (a, b) => {
                    const dateA = new Date(a.completed_date || a.planned_date || a.created_at)
                    const dateB = new Date(b.completed_date || b.planned_date || b.created_at)
                    return dateB - dateA
                },
                'date_asc': (a, b) => {
                    const dateA = new Date(a.completed_date || a.planned_date || a.created_at)
                    const dateB = new Date(b.completed_date || b.planned_date || b.created_at)
                    return dateA - dateB
                },
                'mileage_desc': (a, b) => (b.completed_mileage || b.planned_mileage || 0) - (a.completed_mileage || a.planned_mileage || 0),
                'mileage_asc': (a, b) => (a.completed_mileage || a.planned_mileage || 0) - (b.completed_mileage || b.planned_mileage || 0),
                'cost_desc': (a, b) => (b.cost || 0) - (a.cost || 0),
                'cost_asc': (a, b) => (a.cost || 0) - (b.cost || 0),
            }
            return items.sort(sortFunctions[this.sortBy] || sortFunctions['date_desc'])
        },

        clearFilters() {
            this.searchQuery = ''
            this.filterMotorcycle = ''
            this.filterStatus = ''
            this.sortBy = 'date_desc'
            this.selectedTab = 'all'
        },

        getStatusLabel(status) {
            const labels = {
                'completed': 'Выполнено',
                'planned': 'Запланировано',
                'overdue': 'Просрочено'
            }
            return labels[status] || '—'
        },

        getStatusBadgeClass(status) {
            const classes = {
                'completed': 'badge-success',
                'planned': 'badge-warning',
                'overdue': 'badge-danger'
            }
            return classes[status] || 'badge-gray'
        },

        getStatusIconClass(status) {
            const classes = {
                'completed': 'icon-completed',
                'planned': 'icon-planned',
                'overdue': 'icon-overdue'
            }
            return classes[status] || 'icon-gray'
        },

        getStatusIcon(status) {
            const icons = {
                'completed': 'fa fa-check',
                'planned': 'fa fa-clock',
                'overdue': 'fa fa-exclamation-triangle'
            }
            return icons[status] || 'fa fa-circle'
        },

        formatDate(dateString) {
            return formatDate(dateString)
        }
    },

    mounted() {
        this.loadData()
    }
}
</script>

<style scoped>
/* ===== BASE ===== */
.maintenance-page {
    padding: 20px 0 40px;
    max-width: 100%;
    overflow-x: hidden;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 16px;
    overflow-x: hidden;
}

/* ===== HEADER ===== */
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--border-light);
}

.header-content {
    flex: 1;
    min-width: 150px;
}

.page-title {
    font-size: 28px;
    font-weight: 700;
    margin: 0;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 12px;
}

.page-title i {
    color: var(--accent-text);
    font-size: 28px;
}

.page-subtitle {
    font-size: 14px;
    color: var(--text-muted);
    margin: 4px 0 0;
}


/* ===== STATS ===== */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 28px;
}

.stat-card {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 16px 20px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: 14px;
    transition: all 0.25s ease;
}

.stat-card:hover {
    border-color: var(--border-color);
    transform: translateY(-2px);
    box-shadow: var(--shadow-sm);
}

.stat-card.stat-danger {
    border-color: var(--danger-trans);
    background: var(--danger-trans);
}

.stat-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}

.stat-icon.total {
    background: var(--accent-trans);
    color: var(--accent-text);
}

.stat-icon.completed {
    background: var(--success-trans);
    color: var(--success-text);
}

.stat-icon.planned {
    background: var(--warning-trans);
    color: var(--warning-text);
}

.stat-icon.overdue {
    background: var(--danger-trans);
    color: var(--danger-text);
}

.stat-info {
    display: flex;
    flex-direction: column;
    min-width: 0;
}

.stat-label {
    font-size: 12px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.4px;
    font-weight: 600;
}

.stat-value {
    font-size: 22px;
    font-weight: 700;
    color: var(--text-primary);
}

.stat-value.text-danger {
    color: var(--danger);
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
    justify-content: space-between;
    background: var(--bg-secondary);
    padding: 4px;
    border-radius: 12px;
    border: 1px solid var(--border-light);
}

.tabs button {
    width: 100%;
}

.tabs-btn {
    display: flex;
    gap: 4px;
    width: 100%;
    margin-bottom: 8px;
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

.filter-group {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.filter-group:first-child {
    flex: 1;
    min-width: 200px;
}

.search-wrapper {
    display: flex;
    align-items: center;
    position: relative;
    width: 100%;
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
    margin-top: 8px;
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

/* ===== MAINTENANCE LIST ===== */
.maintenance-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.maintenance-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: 14px;
    cursor: pointer;
    transition: all 0.25s ease;
}

.maintenance-card:hover {
    background: var(--bg-card-hover);
    border-color: var(--border-color);
    transform: translateX(4px);
}

.card-left {
    display: flex;
    gap: 16px;
    flex: 1;
    min-width: 0;
}

.card-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}

.icon-completed {
    background: var(--success-trans);
    color: var(--success-text);
}

.icon-planned {
    background: var(--warning-trans);
    color: var(--warning-text);
}

.icon-overdue {
    background: var(--danger-trans);
    color: var(--danger-text);
}

.icon-gray {
    background: rgba(107, 114, 128, 0.15);
    color: #9ca3af;
}

.card-content {
    flex: 1;
    min-width: 0;
}

.card-header-row {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
}

.card-title {
    font-size: 15px;
    font-weight: 600;
    margin: 0;
    color: var(--text-primary);
}

.card-date {
    font-size: 13px;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 4px;
}

.card-date i {
    font-size: 12px;
}

.card-description {
    font-size: 13px;
    color: var(--text-secondary);
    margin-top: 2px;
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.card-meta {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-top: 4px;
    flex-wrap: wrap;
}

.meta-item {
    font-size: 13px;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 4px;
}

.meta-item i {
    font-size: 12px;
    color: var(--text-muted);
}

.card-right {
    color: var(--text-muted);
    padding-left: 12px;
    transition: all 0.25s ease;
}

.maintenance-card:hover .card-right {
    color: var(--accent-text);
    transform: translateX(4px);
}

.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 500;
}

.badge-success {
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

.badge-gray {
    background: rgba(107, 114, 128, 0.15);
    color: #9ca3af;
}


/* ===== RESPONSIVE ===== */
@media (max-width: 1024px) {
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
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
    
    .filters {
        flex-direction: column;
    }

    .filter-group {
        flex-direction: column;
        width: 100%;
    }

    .filter-group:first-child {
        min-width: unset;
    }

    .filter-select {
        width: 100%;
        min-width: unset;
    }

    .tabs {
        flex-wrap: wrap;
    }

    .tab {
        flex: 1;
        justify-content: center;
        min-width: 80px;
    }
}

@media (max-width: 600px) {
    .container {
        padding: 0 12px;
    }
    
    .maintenance-page {
        padding: 12px 0 24px;
    }
    
    .page-title {
        font-size: 20px;
    }
    
    .page-subtitle {
        font-size: 13px;
    }

    .stats-grid {
        grid-template-columns: 1fr 1fr;
        gap: 8px;
    }

    .stat-card {
        padding: 12px 14px;
        gap: 10px;
    }

    .stat-icon {
        width: 36px;
        height: 36px;
        font-size: 15px;
    }

    .stat-value {
        font-size: 18px;
    }

    .stat-label {
        font-size: 10px;
    }

    .maintenance-card {
        padding: 14px 16px;
        flex-direction: column;
        align-items: stretch;
        gap: 10px;
    }

    .card-left {
        gap: 12px;
    }

    .card-icon {
        width: 36px;
        height: 36px;
        font-size: 14px;
    }

    .card-title {
        font-size: 14px;
    }

    .card-header-row {
        flex-direction: column;
        align-items: flex-start;
        gap: 2px;
    }

    .card-meta {
        gap: 8px;
        font-size: 12px;
    }

    .card-right {
        display: none;
    }

    .empty-state {
        padding: 40px 16px;
    }

    .empty-icon {
        width: 60px;
        height: 60px;
        font-size: 26px;
    }

    .empty-state h3 {
        font-size: 18px;
    }

    .tabs {
        gap: 2px;
        padding: 3px;
    }

    .tab {
        padding: 6px 10px;
        font-size: 12px;
    }

    .tab-count {
        font-size: 10px;
        height: 18px;
        min-width: 18px;
        padding: 0 6px;
    }

    .filter-results {
        flex-direction: column;
        gap: 6px;
        text-align: center;
    }
}

@media (max-width: 400px) {
    .stats-grid {
        grid-template-columns: 1fr;
    }

    .tab {
        font-size: 11px;
        padding: 4px 8px;
    }

    .tab-count {
        display: none;
    }
}
</style>