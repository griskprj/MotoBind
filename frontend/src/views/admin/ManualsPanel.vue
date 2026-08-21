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
                    <p>Все</p>
                </div>
                <div
                    @click="changeTab('moderate')"
                    class="tab" 
                    :class="selectedTab === 'moderate' ? 'active' : ''"
                >
                    <p>На проверке</p>
                </div>
                <div 
                    @click="changeTab('approved')" 
                    class="tab"
                    :class="selectedTab === 'approved' ? 'active' : ''"
                >
                    <p>Одобренные</p>
                </div>
                <div 
                    @click="changeTab('rejected')" 
                    class="tab"
                    :class="selectedTab === 'rejected' ? 'active' : ''"
                >
                    <p>Отклонённые</p>
                </div>
            </div>

            <div class="filters">
                <div class="filter-group">
                    <input 
                        type="text" 
                        v-model="searchQuery" 
                        placeholder="Поиск по названию, автору..."
                        class="search-input"
                    >
                </div>
                
                <select v-model="filterCategory" class="filter-select">
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

                <select v-model="filterMotorcycle" class="filter-select">
                    <option value="">Все мотоциклы</option>
                    <option v-for="moto in motorcycles" :key="moto.id" :value="moto.name">
                        {{ moto.name }}
                    </option>
                </select>

                <select v-model="sortBy" class="filter-select">
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
                            <i class="fa fa-user"></i> {{ manual.author?.username || 'Неизвестно' }}
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
        @close="showDetailsModal = false"
        @approve="handleApprove"
        @reject="handleReject"
        @delete="handleDelete"
    />
</template>

<head>
  <title>MotoBind — Управление мануалами | Админ-панель</title>
  <meta name="description" content="Модерация и управление мануалами MotoBind. Просмотр, одобрение, отклонение и удаление инструкций.">
</head>

<script>
import api from '../../api/api';
import Header from '../../components/Header.vue';
import LoadingOverlay from '../../components/LoadingOverlay.vue';
import ManualDetailsAdminModal from '../../components/modals/admin/ManualDetailsAdminModal.vue';

export default {
    name: 'AdminManuals',
    components: {
        ManualDetailsAdminModal,
        Header,
        LoadingOverlay
    },

    data() {
        return {
            loading: false,
            manuals: [],
            motorcycles: [],
            
            selectedManual: null,
            showDetailsModal: false,

            // Фильтры
            searchQuery: '',
            filterCategory: '',
            filterMotorcycle: '',
            sortBy: 'created_at_desc',
            selectedTab: 'moderate', // По умолчанию показываем "На проверке"
        }
    },

    computed: {
        filteredManuals() {
            let items = [...this.manuals]
            
            if (this.selectedTab === 'moderate') {
                items = items.filter(m => m.status === 'moderate')
            } else if (this.selectedTab === 'approved') {
                items = items.filter(m => m.status === 'approved')
            } else if (this.selectedTab === 'rejected') {
                items = items.filter(m => m.status === 'rejected')
            }
            
            if (this.searchQuery.trim()) {
                const query = this.searchQuery.toLowerCase().trim()
                items = items.filter(m => 
                    m.title?.toLowerCase().includes(query) ||
                    m.motorcycle?.toLowerCase().includes(query) ||
                    m.author?.username?.toLowerCase().includes(query)
                )
            }
            
            if (this.filterCategory) {
                items = items.filter(m => m.category === this.filterCategory)
            }
            
            if (this.filterMotorcycle) {
                items = items.filter(m => m.motorcycle === this.filterMotorcycle)
            }
            
            items = this.sortItems(items)
            
            return items
        },
        
        hasActiveFilters() {
            return this.searchQuery || this.filterCategory || this.filterMotorcycle || this.sortBy !== 'created_at_desc'
        }
    },

    methods: {
        async loadData() {
            try {
                this.loading = true
                const manualsRes = await api.get('/manual/list?per_page=100')
                this.manuals = manualsRes.data.manuals

                const motoRes = await api.get('/motorcycle/')
                this.motorcycles = motoRes.data
            } catch (err) {
                console.error('Failed load admin manuals data:', err)
            } finally {
                this.loading = false
            }
        },

        changeTab(tabName) {
            this.selectedTab = tabName
            this.clearFilters()
        },

        openDetailsModal(manual) {
            this.selectedManual = manual
            this.showDetailsModal = true
        },

        async handleApprove(manualId) {
            try {
                await api.post(`/admin/manual/${manualId}/approve`)
                const manual = this.manuals.find(m => m.id === manualId)
                if (manual) manual.status = 'approved'
                this.showDetailsModal = false
                this.selectedManual = null
                alert('Мануал успешно одобрен!')
            } catch (err) {
                console.error('Failed approve manual:', err)
                alert('Ошибка при одобрении мануала')
            }
        },

        async handleReject(data) {
            try {
                await api.post(`/admin/manual/${data.id}/reject`, { reason: data.reason })
                const manual = this.manuals.find(m => m.id === data.id)
                if (manual) manual.status = 'rejected'
                this.showDetailsModal = false
                this.selectedManual = null
                alert('Мануал отклонён')
            } catch (err) {
                console.error('Failed reject manual:', err)
                alert('Ошибка при отклонении мануала')
            }
        },

        async handleDelete(manualId) {
            if (!confirm('Вы уверены, что хотите удалить этот мануал?')) return
            
            try {
                await api.delete(`/admin/manual/${manualId}`)
                this.manuals = this.manuals.filter(m => m.id !== manualId)
                this.showDetailsModal = false
                this.selectedManual = null
                alert('Мануал удалён')
            } catch (err) {
                console.error('Failed delete manual:', err)
                alert('Ошибка при удалении мануала')
            }
        },

        sortItems(items) {
            const sortFunctions = {
                'created_at_desc': (a, b) => new Date(b.created_at) - new Date(a.created_at),
                'created_at_asc': (a, b) => new Date(a.created_at) - new Date(b.created_at),
                'title_asc': (a, b) => a.title.localeCompare(b.title),
                'title_desc': (a, b) => b.title.localeCompare(a.title),
            }
            return items.sort(sortFunctions[this.sortBy] || sortFunctions['created_at_desc'])
        },

        clearFilters() {
            this.searchQuery = ''
            this.filterCategory = ''
            this.filterMotorcycle = ''
            this.sortBy = 'created_at_desc'
        },

        formatDate(dateString) {
            if (!dateString) return '—'
            try {
                const date = new Date(dateString)
                if (isNaN(date.getTime())) return '—'
                return date.toLocaleDateString('ru-RU', {
                    day: '2-digit',
                    month: 'short',
                    year: 'numeric'
                })
            } catch { return '—' }
        },

        getStatusLabel(status) {
            const labels = {
                'approved': 'Одобрен',
                'moderate': 'На проверке',
                'rejected': 'Отклонён'
            }
            return labels[status] || status
        },

        getCategory(category) {
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
        },

        async logout() {
            try {
                await api.post('/auth/logout');
            } catch(err) { console.error(err) }
            finally {
                const { removeTokens } = await import('../../api/auth');
                removeTokens();
                this.$router.push('/login');
            }
        },
    },

    mounted() {
        this.loadData()
    }
}
</script>

<style scoped>
.controls-wrapper {
    margin-bottom: 16px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 16px;
}

.tabs {
    display: flex;
    gap: 24px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    padding-bottom: 12px;
}
.tab {
    font-size: 14px;
    font-weight: 500;
    color: #8b8b9e;
    cursor: pointer;
    position: relative;
    padding-bottom: 12px;
    transition: 0.2s;
}
.tab:hover { color: #fff; }
.tab.active { color: #a78bfa; }
.tab.active::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    right: 0;
    height: 2px;
    background: #7c3aed;
    border-radius: 2px;
}

.filters {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    align-items: center;
}
.filter-group {
    flex: 1;
    min-width: 160px;
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
.search-input:focus { border-color: #7c3aed; }
.search-input::placeholder { color: #5a5a72; }

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
    appearance: none;
    background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%238b8b9e' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: right 10px center;
    background-size: 14px;
    padding-right: 36px;
}
.filter-select:focus { border-color: #7c3aed; }
.filter-select option { background: #0f0f1a; }

.filter-results {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    background: rgba(124, 58, 237, 0.05);
    border-radius: 8px;
    font-size: 13px;
    color: #8b8b9e;
    margin-bottom: 16px;
}
.clear-filters {
    background: transparent;
    border: none;
    color: #a78bfa;
    cursor: pointer;
    font-size: 13px;
    transition: color 0.2s;
}
.clear-filters:hover { color: #7c3aed; }

/* ===== GRID ===== */
.manuals-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 16px;
}

.manual-card {
    background: #181824;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 18px 20px;
    cursor: pointer;
    transition: border-color 0.2s, transform 0.2s;
    display: flex;
    flex-direction: column;
}
.manual-card:hover {
    border-color: #7c3aed;
    transform: translateY(-2px);
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
.badge-green { background: rgba(34, 197, 94, 0.15); color: #4ade80; }
.badge-warning { background: rgba(251, 191, 36, 0.15); color: #fbbf24; }
.badge-danger { background: rgba(239, 68, 68, 0.15); color: #ef4444; }

.card-body {
    flex: 1;
    margin-bottom: 12px;
}
.card-meta {
    display: flex;
    flex-direction: column;
    gap: 4px;
}
.meta-item {
    font-size: 13px;
    color: #8b8b9e;
    display: flex;
    align-items: center;
    gap: 8px;
}
.meta-item i {
    width: 16px;
    text-align: center;
    color: #5a5a72;
}

.card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 12px;
    border-top: 1px solid rgba(255,255,255,0.05);
}
.steps-count {
    font-size: 13px;
    color: #8b8b9e;
}
.steps-count i { margin-right: 6px; }
.click-hint {
    font-size: 13px;
    color: #5a5a72;
    display: flex;
    align-items: center;
    gap: 4px;
    transition: color 0.2s;
}
.manual-card:hover .click-hint { color: #a78bfa; }

/* ===== EMPTY STATE ===== */
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
    .admin-manuals-container { padding: 16px; }
    .header-right { display: none; }
    .tabs {
        overflow-x: auto;
        gap: 16px;
        padding-bottom: 8px;
        white-space: nowrap;
        scrollbar-width: none;
    }
    .tabs::-webkit-scrollbar { display: none; }
}
@media (max-width: 480px) {
    .filters {
        flex-direction: column;
    }
    .filter-select { width: 100%; }
    .manuals-grid {
        grid-template-columns: 1fr;
    }
}
</style>