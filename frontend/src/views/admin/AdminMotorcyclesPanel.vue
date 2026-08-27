<template>
    <div class="container">
        <LoadingOverlay :isLoading="loading" text="Загрузка мотоциклов..." />

        <!-- === HEADER === -->
        <Header
            title="Мотоциклы пользователей"
            subtitle="Управление мотоциклами всех пользователей"
        />

        <!-- === СТАТИСТИКА === -->
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

        <!-- === ФИЛЬТРЫ === -->
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

            <!-- Результаты -->
            <div class="filter-results" v-if="filteredCount > 0">
                <span>Найдено: {{ filteredCount }} мотоциклов</span>
                <button class="clear-filters" @click="resetFilters" v-if="hasActiveFilters">
                    <i class="fa fa-times"></i> Очистить фильтры
                </button>
            </div>
        </section>

        <!-- === ТАБЛИЦА === -->
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
                        <div class="td" style="grid-column: 1 / -1; text-align: center; color: var(--text-secondary);">
                            Мотоциклы не найдены
                        </div>
                    </div>

                    <div
                        v-for="moto in motorcycles"
                        :key="moto.id"
                        class="tr"
                    >
                        <div class="td moto-cell">
                            <img
                                v-if="moto.photo_url"
                                :src="getPhotoUrl(moto.photo_url)"
                                alt="Фото"
                                class="moto-thumb"
                                @error="(e) => e.target.src = '/moto_default.jpg'"
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

                        <div class="td">
                            <span class="mileage-value">{{ moto.mileage || 0 }} км</span>
                        </div>

                        <div class="td">
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

                        <div class="td">
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

            <!-- === ПАГИНАЦИЯ === -->
            <div v-if="!loading && motorcycles.length > 0" class="table-paginate">
                <p class="paginate-show">
                    Показано {{ (pagination.current_page - 1) * pagination.per_page + 1 }}-
                    {{ Math.min(pagination.current_page * pagination.per_page, pagination.total) }}
                    из {{ pagination.total }}
                </p>

                <div class="paginate-ui">
                    <button
                        class="btn-outline"
                        @click="goToPage(pagination.current_page - 1)"
                        :disabled="!pagination.has_prev"
                    >
                        <i class="fa fa-angle-left"></i>
                    </button>

                    <div class="paginate-btns">
                        <button
                            v-for="page in visiblePages"
                            :key="page"
                            class="btn-outline paginate"
                            :class="{ active: page === pagination.current_page }"
                            @click="goToPage(page)"
                        >
                            {{ page }}
                        </button>
                    </div>

                    <button
                        class="btn-outline"
                        @click="goToPage(pagination.current_page + 1)"
                        :disabled="!pagination.has_next"
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

    <!-- Модалка удаления -->
    <DeleteMotoAdminModal
        :isOpen="showDeleteModal"
        :motorcycle="selectedMotorcycle"
        @submit="deleteMotorcycle"
        @close="closeDeleteModal"
    />
</template>

<script>
import api from '../../api/api.js'
import Header from '../../components/Header.vue'
import LoadingOverlay from '../../components/LoadingOverlay.vue'
import DeleteMotoAdminModal from '../../components/modals/admin/DeleteMotoAdminModal.vue'

export default {
    name: 'AdminMotorcyclesPanel',

    components: {
        Header,
        LoadingOverlay,
        DeleteMotoAdminModal
    },

    data() {
        return {
            loading: false,
            motorcycles: [],
            users: [],
            stats: {
                total: 0,
                with_maintenance: 0,
                without_maintenance: 0
            },
            pagination: {
                current_page: 1,
                per_page: 10,
                total: 0,
                pages: 0,
                has_prev: false,
                has_next: false
            },
            filters: {
                search: '',
                status: '',
                owner_id: '',
                sort_by: 'created_at',
                sort_order: 'desc'
            },
            searchTimeout: null,
            showDeleteModal: false,
            selectedMotorcycle: null
        }
    },

    computed: {
        filteredCount() {
            return this.pagination.total || 0
        },

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

        hasActiveFilters() {
            return this.filters.search || this.filters.status || this.filters.owner_id
        }
    },

    created() {
        this.loadMotorcycles()
        this.loadUsers()
    },

    methods: {
        getPhotoUrl(photoPath) {
            if (!photoPath) return null
            if (photoPath.startsWith('http')) return photoPath
            const baseUrl = import.meta.env.VITE_API_URL || ''
            return `${baseUrl}/uploads/${photoPath}`
        },

        async loadMotorcycles() {
            this.loading = true
            try {
                const params = {
                    page: this.pagination.current_page,
                    per_page: this.pagination.per_page,
                    ...this.filters
                }

                // Убираем пустые параметры
                Object.keys(params).forEach(key => {
                    if (!params[key]) delete params[key]
                })

                const response = await api.get('/admin/motorcycles', { params })
                const data = response.data

                this.motorcycles = data.motorcycles || []
                this.pagination = {
                    current_page: data.current_page,
                    per_page: data.per_page,
                    total: data.total,
                    pages: data.pages,
                    has_prev: data.has_prev,
                    has_next: data.has_next
                }
                this.stats = data.stats || {
                    total: 0,
                    with_maintenance: 0,
                    without_maintenance: 0
                }
            } catch (error) {
                console.error('Error loading motorcycles:', error)
                if (error.response?.status === 401) {
                    this.$router.push('/login')
                }
            } finally {
                this.loading = false
            }
        },

        async loadUsers() {
            try {
                const response = await api.get('/admin/users', {
                    params: { per_page: 1000 }
                })
                this.users = response.data.users || []
            } catch (error) {
                console.error('Error loading users:', error)
            }
        },

        goToPage(page) {
            if (page < 1 || page > this.pagination.pages) return
            this.pagination.current_page = page
            this.loadMotorcycles()
        },

        changePerPage() {
            this.pagination.current_page = 1
            this.loadMotorcycles()
        },

        applyFilters() {
            this.pagination.current_page = 1
            this.loadMotorcycles()
        },

        debouncedSearch() {
            clearTimeout(this.searchTimeout)
            this.searchTimeout = setTimeout(() => {
                this.applyFilters()
            }, 500)
        },

        resetFilters() {
            this.filters = {
                search: '',
                status: '',
                owner_id: '',
                sort_by: 'created_at',
                sort_order: 'desc'
            }
            this.pagination.current_page = 1
            this.loadMotorcycles()
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
            } catch {
                return '—'
            }
        },

        openDeleteModal(moto) {
            this.selectedMotorcycle = moto
            this.showDeleteModal = true
        },

        closeDeleteModal() {
            this.selectedMotorcycle = null
            this.showDeleteModal = false
        },

        async deleteMotorcycle(motoId) {
            try {
                await api.delete(`/admin/motorcycle/${motoId}`)
                await this.loadMotorcycles()
                this.closeDeleteModal()
            } catch (error) {
                console.error('Error deleting motorcycle:', error)
                alert(error.response?.data?.error || 'Ошибка при удалении мотоцикла')
            }
        }
    }
}
</script>

<style scoped>
/* ===== СТАТИСТИКА ===== */
.stat-cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}

.stat-card {
    display: flex;
    gap: 16px;
    justify-content: center;
    padding: 12px 14px;
    background-color: var(--bg-card);
    border-radius: 10px;
    border: 1px solid var(--border-light);
    transition: all 0.3s ease;
}

.stat-card:hover {
    background-color: var(--accent-trans);
    border-color: var(--accent);
}

.card-icon {
    width: 48px;
    height: 48px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 10px;
    background-color: var(--accent-trans);
    color: var(--accent-text);
}

.card-icon.success {
    background-color: var(--success-trans);
    color: var(--success-text);
}

.card-icon.warning {
    background-color: var(--warning-trans);
    color: var(--warning-text);
}

.card-title {
    font-size: 14px;
    color: var(--text-secondary);
}

.card-value {
    font-size: 21px;
    font-weight: 600;
    color: var(--text-primary);
}

/* ===== ФИЛЬТРЫ ===== */
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
    min-width: 150px;
}

.filter-select:focus {
    border-color: var(--accent);
}

.filter-select option {
    background: var(--bg-input);
}

.filters-actions {
    display: flex;
    gap: 8px;
}

.btn-outline {
    padding: 8px 16px;
    background: transparent;
    border: 1px solid var(--border-color);
    border-radius: 10px;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s;
    font-size: 14px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.btn-outline:hover {
    background: var(--border-light);
    border-color: var(--text-muted);
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

/* ===== ТАБЛИЦА ===== */
.table-section {
    background: var(--bg-card);
    border-radius: 10px;
    border: 1px solid var(--border-light);
    padding: 14px 16px;
}

.loading-state {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 40px 0;
    color: var(--text-secondary);
    gap: 12px;
}

.motorcycles-table-wrapper {
    overflow-x: auto;
}

.table-header {
    display: grid;
    grid-template-columns: 1.5fr 1fr 0.8fr 0.8fr 1fr 60px;
    padding: 10px 12px;
    border-bottom: 1px solid var(--border-light);
    font-size: 13px;
    color: var(--text-muted);
    font-weight: 500;
    min-width: 700px;
}

.table-body {
    display: flex;
    flex-direction: column;
}

.tr {
    display: grid;
    grid-template-columns: 1.5fr 1fr 0.8fr 0.8fr 1fr 60px;
    padding: 10px 12px;
    align-items: center;
    border-bottom: 1px solid var(--border-light);
    transition: background 0.2s;
    min-width: 700px;
}

.tr:hover {
    background: var(--border-light);
}

.tr.empty-state {
    cursor: default;
}

.tr.empty-state:hover {
    background: transparent;
}

.td {
    font-size: 14px;
    color: var(--text-primary);
}

/* Moto cell */
.moto-cell {
    display: flex;
    align-items: center;
    gap: 12px;
}

.moto-thumb {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    object-fit: cover;
    flex-shrink: 0;
}

.moto-placeholder {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    background: var(--bg-secondary);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    flex-shrink: 0;
}

.moto-info {
    display: flex;
    flex-direction: column;
}

.moto-name {
    font-weight: 600;
    margin: 0;
    color: var(--text-primary);
}

.moto-meta {
    font-size: 12px;
    color: var(--text-muted);
}

/* Owner cell */
.owner-cell {
    display: flex;
    align-items: center;
}

.owner-info {
    display: flex;
    flex-direction: column;
}

.owner-name {
    font-weight: 500;
    color: var(--text-primary);
}

.owner-email {
    font-size: 12px;
    color: var(--text-muted);
}

/* Mileage */
.mileage-value {
    font-weight: 500;
    color: var(--text-primary);
}

/* Maintenance badge */
.maintenance-badge {
    display: inline-block;
    padding: 2px 12px;
    border-radius: 12px;
    font-size: 13px;
    font-weight: 600;
    text-align: center;
    min-width: 30px;
}

.badge-success {
    background: var(--success-trans);
    color: var(--success-text);
}

.badge-gray {
    background: var(--bg-secondary);
    color: var(--text-muted);
}

.date-value {
    font-size: 13px;
    color: var(--text-secondary);
}

/* Actions */
.actions-cell {
    display: flex;
    gap: 6px;
}

.btn-small {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.btn-small.danger {
    background: var(--danger-trans);
    color: var(--danger-text);
}

.btn-small.danger:hover {
    background: var(--danger-trans);
    opacity: 0.8;
}

/* ===== ПАГИНАЦИЯ ===== */
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
}

.paginate-ui {
    display: flex;
    align-items: center;
    gap: 10px;
}

.paginate-btns {
    display: flex;
    gap: 6px;
    align-items: center;
}

.btn-outline.paginate {
    border: none;
    min-width: 34px;
    height: 34px;
    padding: 0 8px;
    justify-content: center;
}

.btn-outline.paginate.active {
    background-color: var(--accent-trans);
    color: var(--accent-text);
}

.btn-outline.paginate:hover:not(.active) {
    background-color: var(--border-light);
}

.show-per-page select {
    padding: 6px 12px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: 8px;
    color: var(--text-primary);
    font-size: 14px;
    outline: none;
    cursor: pointer;
}

/* ===== АДАПТИВНОСТЬ ===== */
@media (max-width: 1024px) {
    .stat-cards {
        grid-template-columns: repeat(3, 1fr);
    }
}

@media (max-width: 820px) {
    .table-filters {
        flex-direction: column;
        align-items: stretch;
    }

    .filters-row {
        flex-direction: column;
    }

    .filter-group {
        min-width: unset;
    }

    .filter-select {
        width: 100%;
    }

    .stat-cards {
        grid-template-columns: 1fr;
    }

    .table-header {
        display: none;
    }

    .tr {
        grid-template-columns: 1fr;
        gap: 6px;
        padding: 14px;
        border: 1px solid var(--border-light);
        border-radius: 12px;
        margin-bottom: 8px;
        background: var(--bg-primary);
        min-width: unset;
        position: relative;
    }

    .tr:hover {
        background: var(--bg-primary);
    }

    .moto-cell {
        order: 1;
    }

    .td:nth-child(2) {
        order: 2;
        padding-left: 52px;
    }

    .td:nth-child(3) {
        order: 3;
        padding-left: 52px;
    }

    .td:nth-child(4) {
        order: 4;
        padding-left: 52px;
    }

    .td:nth-child(5) {
        order: 5;
        padding-left: 52px;
    }

    .td:nth-child(6) {
        order: 6;
        position: absolute;
        right: 14px;
        top: 14px;
    }

    .td:not(.moto-cell):not(.actions-cell)::before {
        content: attr(data-label);
        color: var(--text-muted);
        font-weight: 400;
        margin-right: 8px;
        font-size: 12px;
    }

    .td:nth-child(2)::before {
        content: "Владелец: ";
    }
    .td:nth-child(3)::before {
        content: "Пробег: ";
    }
    .td:nth-child(4)::before {
        content: "Обслуживаний: ";
    }
    .td:nth-child(5)::before {
        content: "Дата: ";
    }

    .paginate-ui {
        flex-wrap: wrap;
        justify-content: center;
    }

    .table-paginate {
        flex-direction: column;
        align-items: stretch;
    }

    .paginate-show {
        text-align: center;
    }

    .show-per-page {
        display: flex;
        justify-content: center;
    }
}

@media (max-width: 480px) {
    .moto-thumb {
        width: 32px;
        height: 32px;
    }

    .moto-placeholder {
        width: 32px;
        height: 32px;
        font-size: 14px;
    }

    .moto-name {
        font-size: 13px;
    }
}
</style>