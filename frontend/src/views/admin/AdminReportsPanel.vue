<template>
    <div class="container">
        <LoadingOverlay :isLoading="loading" text="Загрузка жалоб..." />

        <Header title="Жалобы на посты" subtitle="Модерация контента и пользователей" />

        <!-- Статистика -->
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

        <!-- Фильтры -->
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

        <!-- Список жалоб -->
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

        <!-- Пагинация -->
        <div v-if="pagination.pages > 1" class="pagination">
            <button class="btn-outline" :disabled="!pagination.has_prev" @click="goToPage(pagination.current_page - 1)">
                <i class="fa fa-angle-left"></i>
            </button>
            <span>Стр. {{ pagination.current_page }} из {{ pagination.pages }}</span>
            <button class="btn-outline" :disabled="!pagination.has_next" @click="goToPage(pagination.current_page + 1)">
                <i class="fa fa-angle-right"></i>
            </button>
        </div>
    </div>

    <!-- Модалка рассмотрения -->
    <ReportDetailsModal
        v-if="selectedReport"
        :isOpen="showDetailsModal"
        :report="selectedReport"
        @close="closeDetails"
        @resolved="onResolved"
    />
</template>

<script>
import api from '../../api/api'
import Header from '../../components/Header.vue'
import LoadingOverlay from '../../components/LoadingOverlay.vue'
import ReportDetailsModal from '../../components/modals/admin/ReportDetailsModal.vue'

export default {
    name: 'AdminReportsPanel',
    components: { Header, LoadingOverlay, ReportDetailsModal },

    data() {
        return {
            loading: false,
            reports: [],
            stats: { total: 0, pending: 0, resolved: 0, rejected: 0 },
            pagination: {
                current_page: 1, per_page: 20, total: 0, pages: 0,
                has_prev: false, has_next: false,
            },
            filters: { status: 'pending', category: '' },
            categories: [
                { value: 'sexual_content', label: 'Контент сексуального характера' },
                { value: 'hate_speech', label: 'Разжигание межнациональной розни' },
                { value: 'extremism', label: 'Экстремистская символика' },
                { value: 'violence', label: 'Насилие' },
                { value: 'drugs', label: 'Пропаганда наркотиков' },
                { value: 'spam', label: 'Спам и мошенничество' },
                { value: 'other', label: 'Другое' },
            ],
            selectedReport: null,
            showDetailsModal: false,
        }
    },

    mounted() { this.loadReports() },

    methods: {
        async loadReports() {
            this.loading = true
            try {
                const params = {
                    page: this.pagination.current_page,
                    per_page: this.pagination.per_page,
                    status: this.filters.status || undefined,
                    category: this.filters.category || undefined,
                }
                const { data } = await api.get('/admin/reports', { params })
                this.reports = data.reports || []
                this.stats = data.stats || this.stats
                this.pagination = {
                    current_page: data.current_page,
                    per_page: data.per_page,
                    total: data.total,
                    pages: data.pages,
                    has_prev: data.has_prev,
                    has_next: data.has_next,
                }
            } catch (err) {
                console.error(err)
                alert('Ошибка загрузки жалоб')
            } finally {
                this.loading = false
            }
        },

        applyFilters() {
            this.pagination.current_page = 1
            this.loadReports()
        },

        resetFilters() {
            this.filters = { status: 'pending', category: '' }
            this.applyFilters()
        },

        goToPage(page) {
            if (page < 1 || page > this.pagination.pages) return
            this.pagination.current_page = page
            this.loadReports()
        },

        openDetails(report) {
            this.selectedReport = report
            this.showDetailsModal = true
        },

        closeDetails() {
            this.showDetailsModal = false
            this.selectedReport = null
        },

        onResolved() {
            this.closeDetails()
            this.loadReports()
        },

        statusLabel(status) {
            return { pending: 'На рассмотрении', resolved: 'Рассмотрено', rejected: 'Отклонено' }[status] || status
        },

        formatDate(date) {
            if (!date) return '—'
            return new Date(date).toLocaleString('ru-RU', {
                day: '2-digit', month: 'short', year: 'numeric',
                hour: '2-digit', minute: '2-digit',
            })
        },

        truncate(text, len) {
            if (!text) return ''
            return text.length > len ? text.slice(0, len) + '...' : text
        },
    },
}
</script>

<style scoped>
.stat-cards {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}
.stat-card {
    display: flex;
    gap: 16px;
    padding: 12px 14px;
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: 10px;
    transition: all 0.3s;
}
.stat-card:hover { background: var(--accent-trans); border-color: var(--accent); }
.card-icon {
    width: 48px; height: 48px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 10px;
    background: var(--accent-trans);
    color: var(--accent);
}
.card-icon.warning { background: var(--warning-trans); color: var(--warning-text); }
.card-icon.success { background: var(--success-trans); color: var(--success-text); }
.card-icon.danger { background: var(--danger-trans); color: var(--danger-text); }
.card-title { font-size: 14px; color: var(--text-secondary); }
.card-value { font-size: 21px; font-weight: 600; color: var(--text-primary); }

.filters-section { margin-bottom: 16px; }
.filters-row { display: flex; flex-wrap: wrap; gap: 10px; }
.filter-select {
    padding: 8px 14px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: 10px;
    color: var(--text-primary);
    font-size: 14px;
    outline: none;
    min-width: 180px;
}
.btn-outline {
    padding: 8px 16px;
    background: transparent;
    border: 1px solid var(--border-color);
    border-radius: 10px;
    color: var(--text-secondary);
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}
.btn-outline:hover { background: var(--border-light); }

.reports-list { display: flex; flex-direction: column; gap: 10px; }

.report-card {
    display: grid;
    grid-template-columns: 1fr 1.2fr 20px;
    gap: 16px;
    align-items: center;
    padding: 14px 18px;
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: 14px;
    cursor: pointer;
    transition: all 0.2s;
}
.report-card:hover {
    border-color: var(--accent);
    transform: translateX(4px);
}

.report-main { display: flex; gap: 12px; align-items: flex-start; }
.report-badge {
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    white-space: nowrap;
    flex-shrink: 0;
}
.status-pending { background: var(--warning-trans); color: var(--warning-text); }
.status-resolved { background: var(--success-trans); color: var(--success-text); }
.status-rejected { background: var(--danger-trans); color: var(--danger-text); }

.report-info { display: flex; flex-direction: column; gap: 4px; min-width: 0; }
.report-category { font-weight: 600; font-size: 14px; color: var(--text-primary); display: flex; gap: 6px; align-items: center; }
.report-category i { color: var(--danger-text); }
.report-meta { font-size: 12px; color: var(--text-muted); display: flex; gap: 6px; align-items: center; flex-wrap: wrap; }
.report-meta .dot { opacity: 0.4; }

.report-post-preview { min-width: 0; }
.preview-author { font-size: 12px; color: var(--text-muted); display: inline-flex; gap: 4px; align-items: center; margin-bottom: 4px; }
.preview-text { font-size: 13px; color: var(--text-secondary); margin: 0; overflow: hidden; text-overflow: ellipsis; }

.report-right { color: var(--text-muted); }
.report-card:hover .report-right { color: var(--accent-text); }

.pagination { display: flex; justify-content: center; align-items: center; gap: 12px; margin-top: 20px; }

.empty-state { text-align: center; padding: 60px 20px; border: 2px dashed var(--border-color); border-radius: 16px; }
.empty-state i { font-size: 40px; color: var(--accent); margin-bottom: 12px; }
.empty-state h3 { color: var(--text-primary); margin: 0 0 6px; }
.empty-text { color: var(--text-muted); }

@media (max-width: 1024px) {
    .stat-cards { grid-template-columns: repeat(2, 1fr); }
    .report-card { grid-template-columns: 1fr; }
    .report-right { display: none; }
}
@media (max-width: 520px) {
    .stat-cards { grid-template-columns: 1fr; }
    .filter-select { width: 100%; }
}
</style>