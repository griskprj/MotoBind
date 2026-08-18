<template>
    <div class="container">
        <!-- === HEADER === -->
        <Header
            title="Обслуживание"
            subtitle="Управляйте обслуживанием своих мотоциклов"
        />

        <!-- === ACTIONS BUTTONS === -->
        <section>
            <div class="actions-wrapper">
                <button @click="showAddMaintenanceModal = true" class="btn-primary">
                    <i class="fa fa-plus"></i> Добавить обслуживание
                </button>
            </div>
        </section>

        <!-- === STATISTIC SECTION === -->
        <section>
            <div class="cards-wrapper">
                <div class="stat-card">
                    <div class="card-header">
                        <i class="fa fa-wrench"></i>
                    </div>
                    <div class="card-body">
                        <p class="card-title">Всего обслуживаний</p>
                        <p class="card-value">{{ allMaintenancesCount }}</p>
                        <p class="card-subtitle">для всех мотоциклов</p>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="card-header">
                        <i class="fa fa-check" style="color: var(--success); background-color: var(--success-trans);"></i>
                    </div>
                    <div class="card-body">
                        <p class="card-title">Выполнено</p>
                        <p class="card-value">{{ completedMaintenances.length }}</p>
                        <p class="card-subtitle">за все время</p>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="card-header">
                        <i class="fa fa-clock" style="color: var(--warning); background-color: var(--warning-trans);"></i>
                    </div>
                    <div class="card-body">
                        <p class="card-title">Запланировано</p>
                        <p class="card-value">{{ plannedMaintenances.length }}</p>
                        <p class="card-subtitle">ожидают выполнения</p>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="card-header">
                        <i class="fa fa-calendar" style="color: var(--danger); background-color: var(--danger-trans);"></i>
                    </div>
                    <div class="card-body">
                        <p class="card-title">Просрочено</p>
                        <p class="card-value">{{ overdueMaintenances.length }}</p>
                        <p class="card-subtitle">требует внимания</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- === MAINTENANCE TABLE === -->
        <div class="table-filter-wrap">
            <div class="tabs">
                <div 
                    @click="changeTab('all')" 
                    class="tab"
                    :class="selectedTab === 'all' ? 'active' : ''"
                >   
                    <p>Все записи</p>
                    <hr v-if="selectedTab === 'all'">
                </div>
                <div
                    @click="changeTab('planned')"
                    class="tab" 
                    :class="selectedTab === 'planned' ? 'active' : ''"
                >
                    <p>Плановые</p>
                    <hr v-if="selectedTab === 'planned'">
                </div>
                <div 
                    @click="changeTab('history')" 
                    class="tab"
                    :class="selectedTab === 'history' ? 'active' : ''"
                >
                    <p>История</p>
                    <hr v-if="selectedTab === 'history'">
                </div>
            </div>

            <div class="filters">
                <div class="filter-group">
                    <input 
                        type="text" 
                        v-model="searchQuery" 
                        placeholder="Поиск по названию..."
                        class="search-input"
                    >
                </div>
                <select v-model="filterMotorcycle" class="filter-select">
                    <option value="">Все мотоциклы</option>
                    <option v-for="motorcycle in motorcycles" :key="motorcycle.id" :value="motorcycle.id">
                        {{ motorcycle.name }}
                    </option>
                </select>
                <select v-model="filterStatus" class="filter-select">
                    <option value="">Все статусы</option>
                    <option value="completed">Выполнено</option>
                    <option value="planned">Запланировано</option>
                    <option value="overdue">Просрочено</option>
                </select>
                <select v-model="sortBy" class="filter-select">
                    <option value="date_desc">По дате (новые)</option>
                    <option value="date_asc">По дате (старые)</option>
                    <option value="mileage_desc">По пробегу (макс)</option>
                    <option value="mileage_asc">По пробегу (мин)</option>
                    <option value="cost_desc">По стоимости (макс)</option>
                    <option value="cost_asc">По стоимости (мин)</option>
                </select>
            </div>
        </div>

        <div class="filter-results" v-if="filteredMaintenances.length > 0">
            <span>Найдено: {{ filteredMaintenances.length }} записей</span>
            <button class="clear-filters" @click="clearFilters" v-if="hasActiveFilters">
                <i class="fa fa-times"></i> Очистить фильтры
            </button>
        </div>

        <div v-if="filteredMaintenances && filteredMaintenances.length > 0" class="maintenance-table-wrapper">
            <div class="table-header">
                <span class="th">Дата</span>
                <span class="th">Обслуживание</span>
                <span class="th">Мотоцикл</span>
                <span class="th">Пробег</span>
                <span class="th">Стоимость</span>
                <span class="th">Статус</span>
                <span class="th"></span>
            </div>
            <div class="table-body">
                <div class="tr"
                    v-for="maintenance in filteredMaintenances"
                    :key="maintenance.id"
                    @click="openDetailsMaintenance(maintenance)"
                >
                    <div class="td date-cell">
                        <div class="icon-square purple"><i class="fa fa-wrench"></i></div>
                        <span>{{ getMaintenanceDate(maintenance) }}</span>
                    </div>
                    <div class="td service-cell">
                        <div class="s-title">{{ maintenance.title }}</div>
                        <div class="s-desc">{{ maintenance.description ? maintenance.description.slice(0, 60) + '...' : '—' }}</div>
                    </div>
                    <div class="td moto-name">{{ maintenance.moto_name || '—' }}</div>
                    <div class="td">
                        <span>
                            {{ getMaintenanceMileage(maintenance) }}
                        </span>
                    </div>
                    <div class="td">{{ maintenance.cost || '—' }} ₽</div>
                    <div class="td">
                        <span class="badge" :class="getStatusBadgeClass(maintenance.status)">
                            {{ getStatusLabel(maintenance.status) }}
                        </span>
                    </div>
                    <div class="td action-cell">
                        <i class="fa fa-angle-right"></i>
                    </div>
                </div>
            </div>
        </div>
        <div v-else class="empty-state">
            <div class="empty-header">
                <i class="fa fa-wrench"></i>
                <p class="empty-title">Записей не найдено</p>
            </div>
            <div class="empty-body">
                <p class="empty-text" v-if="hasActiveFilters">
                    Попробуйте изменить параметры фильтрации
                </p>
                <p class="empty-text" v-else>
                    Начните вести обслуживание своего мотоцикла
                </p>
                <p class="empty-text">
                    Добавьте запись о выполненном или запланируйте ТО
                </p>
            </div>
        </div>
    </div>

    <AddMaintenanceModal
        :isOpen="showAddMaintenanceModal"
        :motorcycles="motorcycles"
        @submit="addMaintenance"
        @close="showAddMaintenanceModal = false"
    />

    <MaintenanceDetailsModal
        v-if="selectedMaintenance"
        :isOpen="showDetailsMaintenanceModal"
        :motoName="selectedMaintenanceMotoName"
        :maintenance="selectedMaintenance"
        @delete="deleteMaintenance"
        @close="closeDetailsMaintenance"
    />
</template>

<script>
import api from '../api/api';
import formatDate from '../utils/DateFormatter.js';
import AddMaintenanceModal from '../components/modals/maintenance/AddMaintenanceModal.vue'
import MaintenanceDetailsModal from '../components/modals/maintenance/MaintenanceDetailsModal.vue';
import Header from '../components/Header.vue'

export default {
    components: {
        AddMaintenanceModal,
        MaintenanceDetailsModal,
        Header
    },

    data() {
        return {
            motorcycles: [],
            allMaintenances: [],
            
            selectedMaintenance: null,
            selectedMaintenanceMotoName: '',
            
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
        }
    },

    computed: {
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
            
            if (this.searchQuery.trim()) {
                const query = this.searchQuery.toLowerCase().trim()
                items = items.filter(m => 
                    m.title?.toLowerCase().includes(query) ||
                    m.description?.toLowerCase().includes(query) ||
                    m.moto_name?.toLowerCase().includes(query)
                )
            }

            if (this.selectedTab === 'planned') {
                items = items.filter(m => m.status === 'planned' || m.status === 'overdue')
            } else if (this.selectedTab === 'history') {
                items = items.filter(m => m.status === 'completed')
            }
            
            if (this.filterMotorcycle) {
                items = items.filter(m => m.moto_id === this.filterMotorcycle)
            }
            
            if (this.filterStatus) {
                items = items.filter(m => m.status === this.filterStatus)
            }
            
            items = this.sortItems(items)
            
            return items
        },
        
        hasActiveFilters() {
            return this.searchQuery || this.filterMotorcycle || this.filterStatus
        }
    },

    methods: {
        async loadData() {
            try {
                const response = await api.get('/statistic/maintenance')
                
                this.motorcycles = response.data.motorcycles || []
                
                const history = response.data.history_maintenances || []
                const planned = response.data.planned_maintenances || []
                this.allMaintenances = [...history, ...planned]
                
                this.allMaintenancesCount = response.data.all_maintenances_count || 0
                
                this.changeTab(this.selectedTab || 'all')
            } catch (err) {
                console.error('Failed load maintenance data:', err)
                alert('Ошибка загрузки данных')
            }
        },

        async addMaintenance(formData) {
            try {
                const { data } = await api.post('/maintenance/', formData)
                
                await this.loadData()
                this.showAddMaintenanceModal = false
                
                alert('Обслуживание успешно добавлено!')
            } catch (err) {
                console.error('Failed create maintenance:', err)
                alert(err.response?.data?.error || 'Ошибка при добавлении обслуживания')
            }
        },

        async deleteMaintenance(id) {
            try {
                await api.delete(`/maintenance/${id}`)
                
                await this.loadData()
                this.showDetailsMaintenanceModal = false
                alert('Обслуживание успешно удалено')
            } catch (err) {
                console.error('Failed delete maintenance:', err)
                alert(err.response?.data?.error || 'Ошибка удаления обслуживания')
            }
        },

        changeTab(tabName) {
            this.selectedTab = tabName
            this.clearFilters()
        },

        openDetailsMaintenance(maintenance) {
            this.selectedMaintenance = maintenance
            const moto = this.motorcycles.find(m => m.id === maintenance.moto_id)
            this.selectedMaintenanceMotoName = moto ? moto.name : maintenance.moto_name || 'Мотоцикл'
            this.showDetailsMaintenanceModal = true
        },

        closeDetailsMaintenance() {
            this.selectedMaintenance = null
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
                'completed': 'badge-green',
                'planned': 'badge-warning',
                'overdue': 'badge-danger'
            }
            return classes[status] || 'badge-gray'
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
/* === ACTIONS WRAPPER === */
.actions-wrapper {
    display: flex;
    gap: 15px;
}

/* === STATISTIC SECTION === */
.cards-wrapper {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(1, 1fr);
    gap: 8px;
    margin-bottom: 24px;
}

.stat-card {
    display: flex;
    gap: 14px;
    padding: 12px;
    background: #181824;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
}

.card-header i {
    padding: 14px;
    background-color: var(--accent-trans);
    color: var(--accent);
    border-radius: 10px;
}

.card-title {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
}

.card-value {
    font-size: 24px;
    font-weight: 600;
    margin: 0;
}

.card-subtitle {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
}

/* === TABLE FILTERS === */
.table-filter-wrap {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 16px;
}

.filters {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    align-items: center;
}

.filter-group {
    flex: 1;
    min-width: 200px;
}

.search-input {
    width: 100%;
    padding: 8px 14px;
    background: #0f0f1a;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    color: #e0e0e0;
    font-size: 14px;
    outline: none;
    transition: border 0.2s;
}

.search-input:focus {
    border-color: #7c3aed;
}

.search-input::placeholder {
    color: #5a5a72;
}

.filter-select {
    padding: 8px 14px;
    background: #0f0f1a;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    color: #e0e0e0;
    font-size: 14px;
    outline: none;
    cursor: pointer;
    transition: border 0.2s;
    min-width: 140px;
}

.filter-select:focus {
    border-color: #7c3aed;
}

.filter-select option {
    background: #0f0f1a;
}

.tabs {
    display: flex;
    gap: 16px;
    color: var(--text-secondary);
}

.tab {
    transition: all 0.3s ease;
    cursor: pointer;
}

.tab:hover {
    color: var(--accent);
}

.tab.active {
    color: var(--accent);
}

.tab p {
    margin-bottom: 4px;
}

.tab hr {
    border: none;
    border-top: 2px solid var(--accent);
    margin: 0;
}

.filter-results {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    background: rgba(124, 58, 237, 0.05);
    border-radius: 8px;
    font-size: 13px;
    color: #8b8b9e;
}

.clear-filters {
    background: transparent;
    border: none;
    color: #a78bfa;
    cursor: pointer;
    font-size: 13px;
    transition: color 0.2s;
}

.clear-filters:hover {
    color: #7c3aed;
}

/* ===== TABLE ===== */
.maintenance-table-wrapper {
    background: #181824;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 16px;
    overflow-x: auto;
}

.table-header {
    display: grid;
    grid-template-columns: 180px 0.5fr 0.5fr 110px 110px 130px 80px;
    padding: 12px 16px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 13px;
    color: #8b8b9e;
    font-weight: 500;
    min-width: 700px;
}

.table-body {
    display: flex;
    flex-direction: column;
}

.tr {
    display: grid;
    grid-template-columns: 180px 0.5fr 0.5fr 110px 110px 130px 80px;
    padding: 14px 16px;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.03);
    transition: background 0.2s;
    cursor: pointer;
    min-width: 700px;
}

.tr:hover {
    background: rgba(255,255,255,0.02);
}

.td {
    font-size: 14px;
}

.moto-name {
    color: #a78bfa;
    font-weight: 500;
}

.date-cell {
    display: flex;
    align-items: center;
    gap: 10px;
}

.icon-square {
    width: 30px;
    height: 30px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
}

.icon-square.purple { background: rgba(124, 58, 237, 0.15); color: #a78bfa; }
.icon-square.green { background: rgba(34, 197, 94, 0.15); color: #4ade80; }
.icon-square.blue { background: rgba(59, 130, 246, 0.15); color: #93c5fd; }

.service-cell {
    display: flex;
    flex-direction: column;
}

.s-title { font-weight: 500; }
.s-desc { font-size: 13px; color: #8b8b9e; }

.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
}

.badge-green {
    background: rgba(34, 197, 94, 0.15);
    color: #4ade80;
}

.badge-warning {
    background: rgba(251, 191, 36, 0.15);
    color: #fbbf24;
}

.badge-danger {
    background: rgba(239, 68, 68, 0.15);
    color: #ef4444;
}

.badge-gray {
    background: rgba(107, 114, 128, 0.15);
    color: #9ca3af;
}

.action-cell {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    color: #4b4b5e;
    transition: color 0.2s;
}

.tr:hover .action-cell { color: #a78bfa; }

.outline-btn {
    padding: 10px 20px;
    background: transparent;
    border: 1px solid rgba(124, 58, 237, 0.3);
    border-radius: 10px;
    color: #a78bfa;
    font-weight: 500;
    cursor: pointer;
    transition: 0.2s;
}

.outline-btn:hover {
    background: rgba(124, 58, 237, 0.1);
    border-color: #7c3aed;
}

/* === EMPTY STATE === */
.empty-state {
    background: #181824;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 16px;
    padding: 60px 20px;
    text-align: center;
}

.empty-header i {
    font-size: 48px;
    color: #2d2d3d;
    margin-bottom: 16px;
}

.empty-title {
    font-size: 20px;
    font-weight: 600;
    margin: 0 0 8px 0;
}

.empty-text {
    color: #8b8b9e;
    font-size: 14px;
    margin: 4px 0;
}

.empty-text a {
    color: #a78bfa;
    text-decoration: none;
}

.empty-text a:hover {
    text-decoration: underline;
}

/* === MEDIA QUERIES === */
@media (max-width: 1200px) {
    .table-header {
        grid-template-columns: 140px 1fr 120px 70px 80px 90px 36px;
        font-size: 12px;
        padding: 10px 14px;
    }
    .tr {
        grid-template-columns: 140px 1fr 120px 70px 80px 90px 36px;
        padding: 10px 14px;
        font-size: 13px;
    }
}

@media (max-width: 1024px) {
    .cards-wrapper {
        grid-template-columns: repeat(2, 1fr);
    }
    .filters {
        flex-wrap: wrap;
    }
    .filter-select {
        min-width: 120px;
        flex: 1;
    }
}

@media (max-width: 820px) {
    .header-right {
        display: none;
    }
    .actions-wrapper {
        flex-direction: column;
    }
    
    .table-header { display: none; }
    .tr {
        grid-template-columns: 1fr;
        gap: 4px;
        padding: 16px;
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px;
        margin-bottom: 8px;
        background: #0f0f1a;
        position: relative;
        min-width: unset;
    }
    .tr:hover { background: #0f0f1a; }
    
    .date-cell {
        order: 1;
        margin-bottom: 4px;
    }
    .service-cell {
        order: 2;
        padding-left: 40px;
    }
    .td:nth-child(3) { /* Мотоцикл */
        order: 3;
        padding-left: 40px;
        font-size: 13px;
    }
    .td:nth-child(4) { /* Пробег */
        order: 4;
        padding-left: 40px;
        font-size: 13px;
    }
    .td:nth-child(5) { /* Стоимость */
        order: 5;
        padding-left: 40px;
        font-size: 13px;
    }
    .td:nth-child(6) { /* Статус */
        order: 6;
        padding-left: 40px;
    }
    .td.action-cell {
        order: 7;
        position: absolute;
        right: 16px;
        top: 20px;
    }
    .td.action-cell i { font-size: 16px; }
    
    .td:not(.date-cell):not(.service-cell):not(.action-cell)::before {
        content: attr(data-label);
        color: #8b8b9e;
        font-weight: 400;
        margin-right: 8px;
    }
    
    .td:nth-child(3)::before {
        content: "Мотоцикл: ";
    }
    .td:nth-child(4)::before {
        content: "Пробег: ";
    }
    .td:nth-child(5)::before {
        content: "Стоимость: ";
    }
}

@media (max-width: 480px) {
    .cards-wrapper {
        grid-template-columns: 1fr;
    }
    
    .filters {
        flex-direction: column;
    }
    .filter-select {
        width: 100%;
    }
}
</style>