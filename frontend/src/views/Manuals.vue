<template>
    <div class="container">
        <LoadingOverlay :isLoading="loading" text="Загрузка мануалов..."/>

        <!-- === HEADER === -->
        <Header
            title="Мануалы"
            subtitle="База инструкций по ремонту и обслуживанию мотоциклов"
        />

        <!-- === FILTERS AND TABS === -->
        <section>
            <div class="tabs">
                <div
                    @click="changeTab('all')"
                    class="tab" 
                    :class="selectedTab === 'all' ? 'active' : ''"
                >
                    <p>Все мануалы</p>
                    <hr v-if="selectedTab === 'all'">
                </div>
                <div 
                    @click="changeTab('my')" 
                    class="tab"
                    :class="selectedTab === 'my' ? 'active' : ''"
                >
                    <p>Мои мануалы</p>
                    <hr v-if="selectedTab === 'my'">
                </div>
                <div 
                    @click="changeTab('myMotos')" 
                    class="tab"
                    :class="selectedTab === 'myMotos' ? 'active' : ''"
                >   
                    <p>Для моих мотоциклов</p>
                    <hr v-if="selectedTab === 'myMotos'">
                </div>
            </div>

            <div class="filters">
                <div class="filters-group">
                    <label>
                        Поиск мануалов
                        <input 
                            type="text" 
                            v-model="filters.search" 
                            @input="debouncedSearch"
                            placeholder="Поиск по названию или мотоциклу"
                            class="search-input"
                        >
                    </label>
    
                    <label>
                        Выберите мотоцикл
                        <select 
                            class="filter-select" 
                            v-model="filters.motorcycle"
                            @change="applyFilters"
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
                    </label>
    
                    <label>
                        Узел / Система
                        <select 
                            class="filter-select" 
                            v-model="filters.category"
                            @change="applyFilters"
                        >
                            <option value="">Все системы</option>
                            <option value="engine">Двигатель</option>
                            <option value="drive">Привод</option>
                            <option value="steering">Рулевое управление</option>
                            <option value="suspension">Подвеска</option>
                            <option value="electronics">Электроника</option>
                            <option value="wheel">Колеса/Шины</option>
                            <option value="brakes">Тормозная система</option>
                            <option value="fuel">Топливная система</option>
                            <option value="cooling">Система охлаждения</option>
                        </select>
                    </label>
    
                    <label>
                        Сортировка
                        <select 
                            class="filter-select" 
                            v-model="filters.sort_by"
                            @change="applyFilters"
                        >
                            <option value="created_at_desc">По дате (новые)</option>
                            <option value="created_at_asc">По дате (старые)</option>
                            <option value="title_asc">По названию (А-Я)</option>
                            <option value="title_desc">По названию (Я-А)</option>
                        </select>
                    </label>
                </div>
                <button class="outline-btn" @click="this.$router.push('/manual-creator')"><i class="fa fa-plus"></i> Добавить мануал</button>
            </div>
        </section>

        <!-- === MANUALS GRID === -->
        <section>
            <!-- Loading state -->
            <div v-if="loading" class="loading-state">
                <i class="fa fa-spinner fa-spin"></i> Загрузка...
            </div>

            <div v-else>
                <div v-if="manuals.length === 0" class="empty-state">
                    <i class="fa fa-book" style="font-size: 48px; color: var(--text-muted);"></i>
                    <p>Мануалы не найдены</p>
                    <button class="outline-btn" @click="this.$router.push('/manual-creator')">Создать первый мануал</button>
                </div>

                <div v-else class="manuals-grid-wrapper">
                    <div 
                        v-for="manual in manuals" 
                        :key="manual.id" 
                        class="manual-card"
                    >
                        <img 
                            :src="manual.image || '/ManualImgDefault.webp'" 
                            alt="" 
                            class="manual-img"
                        >
                        
                        <div class="manual-body">
                            <p class="manual-category">{{ getCategoryName(manual.category) }}</p>
                            <p class="manual-title">{{ manual.title }}</p>
                            <p class="manual-moto"><i class="fa fa-motorcycle"></i> {{ manual.motorcycle }}</p>
                            <button class="outline-btn" @click="viewManual(manual)">
                                Подробнее <i class="fa fa-angle-right"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- === PAGINATION === -->
            <div v-if="!loading && manuals.length > 0" class="table-paginate">
                <p class="paginate-show">
                    Показано {{ (pagination.current_page - 1) * pagination.per_page + 1 }}-
                    {{ Math.min(pagination.current_page * pagination.per_page, pagination.total) }} 
                    из {{ pagination.total }}
                </p>
                
                <div class="paginate-ui">
                    <button 
                        class="outline-btn" 
                        @click="goToPage(pagination.current_page - 1)"
                        :disabled="!pagination.has_prev"
                    >
                        <i class="fa fa-angle-left"></i>
                    </button>
                    <div class="paginate-btns">
                        <button 
                            v-for="page in visiblePages" 
                            :key="page"
                            class="outline-btn paginate" 
                            :class="{ active: page === pagination.current_page }"
                            @click="goToPage(page)"
                        >
                            {{ page }}
                        </button>
                        <p v-if="showEllipsisEnd">...</p>
                        <button 
                            v-if="showLastPage"
                            class="outline-btn paginate" 
                            @click="goToPage(pagination.pages)"
                        >
                            {{ pagination.pages }}
                        </button>
                    </div>
                    <button 
                        class="outline-btn" 
                        @click="goToPage(pagination.current_page + 1)"
                        :disabled="!pagination.has_next"
                    >
                        <i class="fa fa-angle-right"></i>
                    </button>
                </div>

                <div class="show-per-page">
                    <select v-model="pagination.per_page" @change="changePerPage">
                        <option :value="1">1</option>
                        <option :value="6">6</option>
                        <option :value="12">12</option>
                        <option :value="24">24</option>
                        <option :value="48">48</option>
                    </select>
                </div>
            </div>
        </section>
    </div>

    <ManualDetailsModal
        :is-open="showManualDetailsModal"
        :manual="selectedManual"
        @close="showManualDetailsModal = false"
    />
</template>

<head>
  <title>MotoBind — Мануалы по ремонту мотоциклов | База инструкций</title>
  <meta name="description" content="База инструкций по ремонту и обслуживанию мотоциклов от сообщества. Находите мануалы для своего мотоцикла и делитесь своим опытом.">
</head>

<script>
import api from '../api/api'
import ManualDetailsModal from '../components/modals/manual/ManualDetailsModal.vue';
import Header from '../components/Header.vue'
import LoadingOverlay from '../components/LoadingOverlay.vue';

export default {
    components: {
        ManualDetailsModal,
        Header,
        LoadingOverlay
    },
    data() {
        return {
            loading: false,
            
            selectedTab: 'all',
            selectedManual: null,
            manuals: [],
            motorcycles: [],
            
            filters: {
                search: '',
                motorcycle: '',
                category: '',
                sort_by: 'created_at_desc'
            },
            
            pagination: {
                current_page: 1,
                per_page: 6,
                total: 0,
                pages: 0,
                has_prev: false,
                has_next: false
            },
            
            searchTimeout: null,

            showManualDetailsModal: false
        }
    },
    
    computed: {
        visiblePages() {
            const current = this.pagination.current_page
            const total = this.pagination.pages
            const delta = 2
            const range = []
            
            for (let i = Math.max(2, current - delta); i <= Math.min(total - 1, current + delta); i++) {
                range.push(i)
            }
            
            if (current - delta > 2) {
                range.unshift('...')
            }
            
            if (current + delta < total - 1) {
                range.push('...')
            }
            
            range.unshift(1)
            
            if (total > 1) {
                range.push(total)
            }
            
            return range.filter((v, i, a) => a.indexOf(v) === i)
        },
        
        showEllipsisEnd() {
            const current = this.pagination.current_page
            const total = this.pagination.pages
            return total > 1 && current + 2 < total - 1
        },
        
        showLastPage() {
            const total = this.pagination.pages
            return total > 1 && this.pagination.current_page + 2 < total
        }
    },
    
    created() {
        this.loadManuals()
        this.loadMotorcycles()
    },
    
    methods: {
        async loadManuals() {
            this.loading = true
            try {
                const params = {
                    page: this.pagination.current_page,
                    per_page: this.pagination.per_page,
                    tab: this.selectedTab,
                    ...this.filters
                }
                
                Object.keys(params).forEach(key => {
                    if (!params[key]) delete params[key]
                })
                
                const response = await api.get('/manual/list', { params })
                const data = response.data
                
                this.manuals = data.manuals || []
                this.pagination = {
                    current_page: data.current_page,
                    per_page: data.per_page,
                    total: data.total,
                    pages: data.pages,
                    has_prev: data.has_prev,
                    has_next: data.has_next
                }
            } catch (error) {
                console.error('Error loading manuals:', error)
                if (error.response?.status === 401) {
                    this.$router.push('/login')
                }
            } finally {
                this.loading = false
            }
        },
        
        async loadMotorcycles() {
            try {
                const response = await api.get('/motorcycle')
                this.motorcycles = response.data || []
            } catch (error) {
                console.error('Error loading motorcycles:', error)
            }
        },
        
        changeTab(tabName) {
            this.selectedTab = tabName
            this.pagination.current_page = 1
            this.loadManuals()
        },
        
        applyFilters() {
            this.pagination.current_page = 1
            this.loadManuals()
        },
        
        debouncedSearch() {
            clearTimeout(this.searchTimeout)
            this.searchTimeout = setTimeout(() => {
                this.applyFilters()
            }, 500)
        },
        
        goToPage(page) {
            if (page < 1 || page > this.pagination.pages) return
            this.pagination.current_page = page
            this.loadManuals()
        },
        
        changePerPage() {
            this.pagination.current_page = 1
            this.loadManuals()
        },
        
        getCategoryName(category) {
            const categories = {
                'engine': 'ДВИГАТЕЛЬ',
                'drive': 'ПРИВОД',
                'steering': 'РУЛЕВОЕ УПРАВЛЕНИЕ',
                'suspension': 'ПОДВЕСКА',
                'electronics': 'ЭЛЕКТРОНИКА',
                'wheel': 'КОЛЕСА/ШИНЫ',
                'brakes': 'ТОРМОЗНАЯ СИСТЕМА',
                'fuel': 'ТОПЛИВНАЯ СИСТЕМА',
                'cooling': 'СИСТЕМА ОХЛАЖДЕНИЯ'
            }
            return categories[category] || category.toUpperCase()
        },
        
        getStatusClass(status) {
            const classes = {
                'moderate': 'status-moderate',
                'approved': 'status-approved',
                'rejected': 'status-rejected'
            }
            return classes[status] || ''
        },
        
        viewManual(manual) {
            this.selectedManual = manual
            this.showManualDetailsModal = true
        },
        
        openCreateModal() {
            // TODO: Открыть модалку создания
            console.log('Open create manual modal')
        },
        
        logout() {
            // TODO: Реализовать выход
            console.log('Logout')
        }
    }
}
</script>

<style scoped>
/* === FILTERS AND TABS === */
.tabs {
    display: flex;
    gap: 16px;
    color: var(--text-secondary);
    margin-bottom: 16px;
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

.filters {
    padding: 14px 16px;
    background-color: var(--bg-card);
    border-radius: 10px;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
    align-items: center;
}

.filters-group {
    display: flex;
    flex-direction: row;
    gap: 10px;
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

@media (max-width: 1200px) {
    .filters {
        flex-direction: column;
    }

    .filters button {
        width: 100%;    
    }
}

@media (max-width: 1000px) {
    .filters-group {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(2, 1fr);
    }
}

@media (max-width: 460px) {
    .filters-group {
        display: grid;
        grid-template-columns: repeat(1, 1fr);
        grid-template-rows: repeat(4, 1fr);
        width: 100%;
    }
}


/* === MANUALS GRID === */
.manuals-grid-wrapper {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: 14px;
}

.manual-card {
    background-color: var(--bg-card);
    border-radius: 10px;
}

.manual-img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
}

.manual-body {
    padding: 10px 14px;
}

.manual-category {
    border-radius: 10px;
    font-weight: 600;
    text-align: center;
    background-color: var(--accent-trans);
    color: var(--accent);
    margin-bottom: 8px;
}

.manual-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 4px;
}

.manual-moto {
    font-size: 14px;
    color: var(--text-muted);
    margin-bottom: 12px;
}

.manual-body button {
    width: 100%;
}

@media (max-width: 1200px) {
    .manuals-grid-wrapper {
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(4, 1fr);
    }
}

@media (max-width: 540px) {
    .manuals-grid-wrapper {
        grid-template-columns: repeat(1, 1fr);
        grid-template-rows: repeat(8, 1fr);
    }
}

/* paginate */
.table-paginate {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.paginate-show {
    color: var(--text-secondary);
}

.paginate-ui {
    display: flex;
    align-items: center;
    gap: 14px;
}

.paginate-btns {
    display: flex;
    gap: 8px;
    text-align: center;
}

.paginate-btns button {
    margin-top: 0;
}

.outline-btn.paginate {
    border: none;
}

.outline-btn.paginate.active {
    background-color: var(--accent-trans);
}

.show-per-page {
    display: flex;
    gap: 16px;
}

.loading-state {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 60px 0;
    color: var(--text-secondary);
    gap: 12px;
}

.loading-state .fa-spinner {
    font-size: 24px;
    color: var(--accent);
}

.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 0;
    gap: 16px;
    color: var(--text-secondary);
}

.empty-state p {
    font-size: 18px;
}

/* Пагинация */
.paginate {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
    flex-wrap: wrap;
    gap: 16px;
}

.paginate-show {
    color: var(--text-secondary);
    font-size: 14px;
}

.paginate-ui {
    display: flex;
    align-items: center;
    gap: 14px;
}

.paginate-btns {
    display: flex;
    gap: 8px;
    align-items: center;
}

.outline-btn.paginate {
    border: none;
    min-width: 36px;
    height: 36px;
    padding: 0 8px;
}

.outline-btn.paginate.active {
    background-color: var(--accent-trans);
    color: var(--accent);
}

.outline-btn.paginate:hover:not(.active) {
    background-color: rgba(255,255,255,0.05);
}

.paginate-ui button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.show-per-page select {
    padding: 8px 14px;
    background: #0f0f1a;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    color: #e0e0e0;
    font-size: 14px;
    outline: none;
    cursor: pointer;
    transition: border 0.2s;
}

.show-per-page select:focus {
    border-color: #7c3aed;
}

@media (max-width: 768px) {
    .paginate {
        flex-direction: column;
        align-items: stretch;
        gap: 12px;
    }
    
    .paginate-ui {
        justify-content: center;
    }
    
    .paginate-show {
        text-align: center;
    }
    
    .show-per-page {
        display: flex;
        justify-content: center;
    }
}

/* Анимация */
@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.fa-spin {
    animation: spin 1s linear infinite;
}
</style>