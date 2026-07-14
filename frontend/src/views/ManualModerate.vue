<template>
    <div class="container">
        <!-- Статистика модерации -->
        <div class="section">
            <div class="section-title-wrapper">
                <i class="fa fa-gavel"></i>
                <h2>Модерация мануалов</h2>
            </div>
            <p class="subtitle">Проверяйте и принимайте решения по мануалам, предложенным пользователями</p>

            <div class="statistics-cards">
                <div class="stat-card">
                    <p class="stat-card-title">На проверке</p>
                    <p class="stat-card-value">{{ pendingCount }}</p>
                </div>
                <div class="stat-card">
                    <p class="stat-card-title">Одобрено</p>
                    <p class="stat-card-value">{{ approvedCount }}</p>
                </div>
                <div class="stat-card">
                    <p class="stat-card-title">Отклонено</p>
                    <p class="stat-card-value">{{ rejectedCount }}</p>
                </div>
                <div class="stat-card">
                    <p class="stat-card-title">Всего мануалов</p>
                    <p class="stat-card-value">{{ totalCount }}</p>
                </div>
            </div>
        </div>

        <!-- Фильтры и список -->
        <div class="section">
            <div class="section-title-wrapper">
                <i class="fa fa-list"></i>
                <h2>Список мануалов на модерацию</h2>
            </div>

            <!-- Фильтры -->
            <div class="filters">
                <div class="filter-group">
                    <select v-model="filterStatus" class="filter-select">
                        <option value="all">Все статусы</option>
                        <option value="pending">На проверке</option>
                        <option value="approved">Одобрено</option>
                        <option value="rejected">Отклонено</option>
                    </select>
                    <select v-model="filterMoto" class="filter-select">
                        <option value="all">Все мотоциклы</option>
                        <option v-for="moto in motorcycles" :key="moto.id" :value="moto.id">
                            {{ moto.name }}
                        </option>
                    </select>
                    <input 
                        type="text" 
                        v-model="searchQuery" 
                        placeholder="Поиск по названию..." 
                        class="filter-input"
                    />
                </div>
            </div>

            <!-- Список мануалов -->
            <div v-if="filteredManuals.length === 0" class="empty-state">
                <i class="fa fa-file-text-o"></i>
                <p>Нет мануалов для отображения</p>
            </div>

            <div v-else class="manuals-list">
                <div 
                    v-for="manual in filteredManuals" 
                    :key="manual.id" 
                    class="manual-card"
                    :class="{
                        'status-pending': manual.status === 'pending',
                        'status-approved': manual.status === 'approved',
                        'status-rejected': manual.status === 'rejected'
                    }"
                >
                    <div class="manual-card-header">
                        <div class="manual-card-info">
                            <div class="manual-icon">
                                <i class="fa fa-file-pdf-o"></i>
                            </div>
                            <div class="manual-meta">
                                <h3 class="manual-title">{{ manual.title }}</h3>
                                <div class="manual-tags">
                                    <span class="tag moto-tag">
                                        <i class="fa fa-motorcycle"></i>
                                        {{ manual.moto_name }}
                                    </span>
                                    <span class="tag author-tag">
                                        <i class="fa fa-user"></i>
                                        {{ manual.author }}
                                    </span>
                                    <span class="tag date-tag">
                                        <i class="fa fa-clock-o"></i>
                                        {{ formatDate(manual.created_at) }}
                                    </span>
                                </div>
                            </div>
                        </div>
                        <span class="status-badge" :class="'status-' + manual.status">
                            {{ getStatusLabel(manual.status) }}
                        </span>
                    </div>

                    <div class="manual-card-body">
                        <div class="manual-description">
                            <i class="fa fa-align-left"></i>
                            <p>{{ manual.description || 'Описание отсутствует' }}</p>
                        </div>

                        <div class="manual-stats">
                            <span class="stat-item">
                                <i class="fa fa-list-ol"></i>
                                {{ manual.steps_count || 0 }} шагов
                            </span>
                            <span class="stat-item">
                                <i class="fa fa-eye"></i>
                                {{ manual.views || 0 }} просмотров
                            </span>
                            <span class="stat-item">
                                <i class="fa fa-thumbs-up"></i>
                                {{ manual.likes || 0 }} лайков
                            </span>
                            <span class="stat-item" v-if="manual.maintenance_title">
                                <i class="fa fa-wrench"></i>
                                {{ manual.maintenance_title }}
                            </span>
                        </div>
                    </div>

                    <div class="manual-card-actions">
                        <button 
                            class="btn-action btn-view" 
                            @click="openManualModal(manual)"
                        >
                            <i class="fa fa-eye"></i> Просмотр
                        </button>
                        <button 
                            v-if="manual.status === 'pending'"
                            class="btn-action btn-approve" 
                            @click="approveManual(manual.id)"
                        >
                            <i class="fa fa-check"></i> Одобрить
                        </button>
                        <button 
                            v-if="manual.status === 'pending'"
                            class="btn-action btn-reject" 
                            @click="openRejectModal(manual.id)"
                        >
                            <i class="fa fa-times"></i> Отклонить
                        </button>
                        <button 
                            v-if="manual.status === 'rejected'"
                            class="btn-action btn-undo" 
                            @click="reconsiderManual(manual.id)"
                        >
                            <i class="fa fa-undo"></i> Пересмотреть
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Модальное окно просмотра мануала -->
    <div v-if="showManualModal" class="modal-wrapper" @click.self="closeManualModal">
        <div class="modal-container modal-large">
            <div class="modal-header">
                <div class="modal-header-info">
                    <i class="fa fa-file-text"></i>
                    <h3 class="modal-title">{{ selectedManual?.title }}</h3>
                </div>
                <button class="modal-close" @click="closeManualModal">
                    <i class="fa fa-times"></i>
                </button>
            </div>

            <div class="modal-body">
                <div class="manual-detail-meta">
                    <span class="detail-item">
                        <i class="fa fa-motorcycle"></i>
                        {{ selectedManual?.moto_name }}
                    </span>
                    <span class="detail-item">
                        <i class="fa fa-user"></i>
                        {{ selectedManual?.author }}
                    </span>
                    <span class="detail-item">
                        <i class="fa fa-clock-o"></i>
                        {{ formatDate(selectedManual?.created_at) }}
                    </span>
                    <span class="detail-item status-badge" :class="'status-' + selectedManual?.status">
                        {{ getStatusLabel(selectedManual?.status) }}
                    </span>
                </div>

                <div class="manual-detail-description">
                    <h4>Описание</h4>
                    <p>{{ selectedManual?.description || 'Описание отсутствует' }}</p>
                </div>

                <div class="manual-detail-steps">
                    <h4>Шаги выполнения ({{ selectedManual?.steps?.length || 0 }})</h4>
                    <div class="steps-list">
                        <div 
                            v-for="(step, index) in selectedManual?.steps" 
                            :key="step.id" 
                            class="step-item"
                        >
                            <div class="step-number">{{ index + 1 }}</div>
                            <div class="step-content">
                                <p class="step-text">{{ step.text }}</p>
                                <div v-if="step.image" class="step-image-wrapper">
                                    <img :src="step.image" :alt="'Шаг ' + (index + 1)" class="step-image" />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="modal-actions">
                    <button v-if="selectedManual?.status === 'pending'" class="btn-approve" @click="approveManualFromModal">
                        <i class="fa fa-check"></i> Одобрить
                    </button>
                    <button v-if="selectedManual?.status === 'pending'" class="btn-reject" @click="openRejectModalFromModal">
                        <i class="fa fa-times"></i> Отклонить
                    </button>
                    <button v-if="selectedManual?.status === 'rejected'" class="btn-undo" @click="reconsiderManualFromModal">
                        <i class="fa fa-undo"></i> Пересмотреть
                    </button>
                    <button class="btn-secondary" @click="closeManualModal">
                        Закрыть
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Модальное окно отклонения -->
    <div v-if="showRejectModal" class="modal-wrapper" @click.self="closeRejectModal">
        <div class="modal-container">
            <div class="modal-header">
                <i class="fa fa-times-circle" style="color: var(--danger);"></i>
                <h3 class="modal-title">Отклонить мануал</h3>
            </div>

            <div class="modal-body">
                <p class="modal-text">Укажите причину отклонения мануала:</p>
                <textarea 
                    v-model="rejectReason" 
                    class="modal-textarea" 
                    placeholder="Опишите причину отклонения..."
                    rows="4"
                ></textarea>
            </div>

            <div class="modal-actions">
                <button class="btn-danger" @click="confirmReject">
                    <i class="fa fa-times"></i> Отклонить
                </button>
                <button class="btn-secondary" @click="closeRejectModal">
                    Отмена
                </button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ModerateManual',
    data() {
        return {
            // Статистика
            pendingCount: 12,
            approvedCount: 84,
            rejectedCount: 23,
            totalCount: 119,

            // Список мануалов (заглушка)
            manuals: [
                {
                    id: 1,
                    title: 'Замена масла на Bajaj Pulsar NS 125',
                    description: 'Подробная инструкция по замене масла на мотоцикле Bajaj Pulsar NS 125. Включает все необходимые шаги и рекомендации.',
                    moto_name: 'Bajaj Pulsar NS 125',
                    moto_id: 1,
                    author: 'Grisky',
                    created_at: '2026-07-14T10:00:00',
                    status: 'pending',
                    steps_count: 5,
                    views: 0,
                    likes: 0,
                    maintenance_title: 'Замена масла',
                    steps: [
                        { id: 1, text: 'Прогрейте двигатель до рабочей температуры' },
                        { id: 2, text: 'Слейте старое масло через сливную пробку' },
                        { id: 3, text: 'Замените масляный фильтр' },
                        { id: 4, text: 'Залейте новое масло через заливную горловину' },
                        { id: 5, text: 'Проверьте уровень масла и запустите двигатель' }
                    ]
                },
                {
                    id: 2,
                    title: 'Регулировка клапанов Yamaha YZF-R3',
                    description: 'Пошаговая инструкция по регулировке клапанов на Yamaha YZF-R3.',
                    moto_name: 'Yamaha YZF-R3',
                    moto_id: 2,
                    author: 'MotoMaster',
                    created_at: '2026-07-13T15:30:00',
                    status: 'pending',
                    steps_count: 8,
                    views: 0,
                    likes: 0,
                    maintenance_title: 'Регулировка клапанов',
                    steps: [
                        { id: 1, text: 'Снимите пластиковый кожух двигателя' },
                        { id: 2, text: 'Открутите крышку головки блока цилиндров' },
                        { id: 3, text: 'Установите поршень в ВМТ такта сжатия' },
                        { id: 4, text: 'Проверьте зазоры щупом' },
                        { id: 5, text: 'При необходимости отрегулируйте зазоры' },
                        { id: 6, text: 'Установите новые прокладки' },
                        { id: 7, text: 'Соберите все в обратном порядке' },
                        { id: 8, text: 'Проверьте работу двигателя' }
                    ]
                },
                {
                    id: 3,
                    title: 'Замена тормозных колодок Honda CB500F',
                    description: 'Инструкция по замене передних тормозных колодок на Honda CB500F.',
                    moto_name: 'Honda CB500F',
                    moto_id: 3,
                    author: 'HondaRider',
                    created_at: '2026-07-12T09:15:00',
                    status: 'approved',
                    steps_count: 6,
                    views: 45,
                    likes: 12,
                    maintenance_title: 'Замена тормозов',
                    steps: [
                        { id: 1, text: 'Поднимите переднюю часть мотоцикла' },
                        { id: 2, text: 'Снимите суппорт с тормозного диска' },
                        { id: 3, text: 'Извлеките старые колодки' },
                        { id: 4, text: 'Установите новые колодки' },
                        { id: 5, text: 'Установите суппорт обратно' },
                        { id: 6, text: 'Проверьте работу тормозов' }
                    ]
                },
                {
                    id: 4,
                    title: 'Замена воздушного фильтра KTM Duke 390',
                    description: 'Как заменить воздушный фильтр на KTM Duke 390.',
                    moto_name: 'KTM Duke 390',
                    moto_id: 4,
                    author: 'DukeRider',
                    created_at: '2026-07-11T18:45:00',
                    status: 'rejected',
                    steps_count: 4,
                    views: 12,
                    likes: 2,
                    maintenance_title: 'Замена фильтра',
                    steps: [
                        { id: 1, text: 'Откройте крышку воздушного фильтра' },
                        { id: 2, text: 'Извлеките старый фильтр' },
                        { id: 3, text: 'Установите новый фильтр' },
                        { id: 4, text: 'Закройте крышку' }
                    ]
                }
            ],

            motorcycles: [
                { id: 1, name: 'Bajaj Pulsar NS 125' },
                { id: 2, name: 'Yamaha YZF-R3' },
                { id: 3, name: 'Honda CB500F' },
                { id: 4, name: 'KTM Duke 390' }
            ],

            // Фильтры
            filterStatus: 'all',
            filterMoto: 'all',
            searchQuery: '',

            // Модальные окна
            showManualModal: false,
            showRejectModal: false,
            selectedManual: null,
            selectedManualId: null,
            rejectReason: ''
        };
    },

    computed: {
        filteredManuals() {
            return this.manuals.filter(manual => {
                const matchStatus = this.filterStatus === 'all' || manual.status === this.filterStatus;
                const matchMoto = this.filterMoto === 'all' || manual.moto_id === Number(this.filterMoto);
                const matchSearch = manual.title.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                                  manual.author.toLowerCase().includes(this.searchQuery.toLowerCase());
                return matchStatus && matchMoto && matchSearch;
            });
        }
    },

    methods: {
        formatDate(dateString) {
            if (!dateString) return '—';
            const date = new Date(dateString);
            return date.toLocaleString('ru-RU', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        },

        getStatusLabel(status) {
            const labels = {
                pending: 'На проверке',
                approved: 'Одобрено',
                rejected: 'Отклонено'
            };
            return labels[status] || status;
        },

        // Просмотр мануала
        openManualModal(manual) {
            this.selectedManual = manual;
            this.showManualModal = true;
            document.body.style.overflow = 'hidden';
        },

        closeManualModal() {
            this.showManualModal = false;
            this.selectedManual = null;
            document.body.style.overflow = '';
        },

        // Одобрение
        approveManual(manualId) {
            if (confirm('Вы уверены, что хотите одобрить этот мануал?')) {
                const manual = this.manuals.find(m => m.id === manualId);
                if (manual) {
                    manual.status = 'approved';
                    this.updateCounts();
                    alert('Мануал успешно одобрен!');
                }
            }
        },

        approveManualFromModal() {
            if (this.selectedManual) {
                this.approveManual(this.selectedManual.id);
                this.closeManualModal();
            }
        },

        // Отклонение
        openRejectModal(manualId) {
            this.selectedManualId = manualId;
            this.rejectReason = '';
            this.showRejectModal = true;
            document.body.style.overflow = 'hidden';
        },

        openRejectModalFromModal() {
            if (this.selectedManual) {
                this.openRejectModal(this.selectedManual.id);
                this.closeManualModal();
            }
        },

        closeRejectModal() {
            this.showRejectModal = false;
            this.selectedManualId = null;
            this.rejectReason = '';
            document.body.style.overflow = '';
        },

        confirmReject() {
            const manual = this.manuals.find(m => m.id === this.selectedManualId);
            if (manual) {
                manual.status = 'rejected';
                this.updateCounts();
                alert(`Мануал отклонен${this.rejectReason ? ': ' + this.rejectReason : ''}`);
            }
            this.closeRejectModal();
        },

        // Пересмотр
        reconsiderManual(manualId) {
            if (confirm('Вернуть мануал на повторную проверку?')) {
                const manual = this.manuals.find(m => m.id === manualId);
                if (manual) {
                    manual.status = 'pending';
                    this.updateCounts();
                    alert('Мануал возвращен на проверку!');
                }
            }
        },

        reconsiderManualFromModal() {
            if (this.selectedManual) {
                this.reconsiderManual(this.selectedManual.id);
                this.closeManualModal();
            }
        },

        updateCounts() {
            this.pendingCount = this.manuals.filter(m => m.status === 'pending').length;
            this.approvedCount = this.manuals.filter(m => m.status === 'approved').length;
            this.rejectedCount = this.manuals.filter(m => m.status === 'rejected').length;
            this.totalCount = this.manuals.length;
        }
    },

    mounted() {
        this.updateCounts();
    }
};
</script>

<style scoped>
/* ===== Общие стили ===== */
.subtitle {
    text-align: center;
    color: var(--text-muted);
    max-width: 600px;
    margin: 0 auto 28px;
    font-size: 1.05rem;
}

.section {
    background-color: var(--bg-primary);
    border: 2px solid var(--border-color);
    border-radius: 25px;
    padding: 28px;
    margin-bottom: 32px;
    transition: border-color 0.3s ease;
}

.section:hover {
    border-color: var(--accent-light);
}

.section-title-wrapper {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 18px;
    margin-bottom: 28px;
    flex-wrap: wrap;
}

.section-title-wrapper i {
    font-size: 32px;
    color: var(--accent);
}

.section-title-wrapper h2 {
    margin-bottom: 0;
    font-size: 1.6rem;
}

/* ===== Статистика ===== */
.statistics-cards {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
}

.stat-card {
    display: flex;
    flex-direction: column;
    gap: 8px;
    justify-content: center;
    padding: 20px 24px;
    background-color: var(--bg-secondary);
    border: 2px solid var(--border-color);
    border-radius: 20px;
    text-align: center;
    transition: all 0.3s;
}

.stat-card:hover {
    border-bottom: 3px solid var(--accent);
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}

.stat-card-title {
    font-weight: 500;
    font-size: 0.9rem;
    color: var(--text-secondary);
    margin-bottom: 0;
}

.stat-card-value {
    font-weight: 700;
    color: var(--accent);
    font-size: 2rem;
    margin-bottom: 0;
}

/* ===== Фильтры ===== */
.filters {
    margin-bottom: 28px;
}

.filter-group {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    justify-content: center;
}

.filter-select,
.filter-input {
    padding: 10px 16px;
    font-size: 0.9rem;
    background-color: var(--bg-secondary);
    border: 2px solid var(--border-color);
    border-radius: 14px;
    color: var(--text-primary);
    transition: all 0.3s;
    min-width: 180px;
    flex: 1;
    max-width: 250px;
}

.filter-select:focus,
.filter-input:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15);
}

.filter-select option {
    background-color: var(--bg-primary);
}

/* ===== Список мануалов ===== */
.manuals-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.manual-card {
    background: var(--bg-secondary);
    border: 2px solid var(--border-color);
    border-radius: 20px;
    padding: 20px 24px;
    transition: all 0.3s ease;
}

.manual-card:hover {
    transform: translateY(-2px);
}

.manual-card.status-pending {
    border-left: 4px solid var(--warning);
}

.manual-card.status-approved {
    border-left: 4px solid var(--success);
}

.manual-card.status-rejected {
    border-left: 4px solid var(--danger);
}

.manual-card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 16px;
    flex-wrap: wrap;
    margin-bottom: 14px;
}

.manual-card-info {
    display: flex;
    gap: 14px;
    flex: 1;
    min-width: 0;
}

.manual-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: var(--accent-light);
    border: 2px solid var(--border-color);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.manual-icon i {
    font-size: 20px;
    color: var(--warning);
}

.manual-meta {
    flex: 1;
    min-width: 0;
}

.manual-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 6px;
}

.manual-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.tag {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 0.75rem;
    padding: 3px 10px;
    border-radius: 12px;
    background: var(--bg-primary);
    border: 1px solid var(--border-color);
    color: var(--text-muted);
}

.tag i {
    font-size: 0.7rem;
}

.status-badge {
    font-size: 0.7rem;
    font-weight: 600;
    padding: 4px 14px;
    border-radius: 12px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    flex-shrink: 0;
    white-space: nowrap;
}

.status-pending {
    color: var(--warning);
    background: rgba(245, 158, 11, 0.15);
    border: 1px solid rgba(245, 158, 11, 0.2);
}

.status-approved {
    color: var(--success);
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.2);
}

.status-rejected {
    color: var(--danger);
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.2);
}

/* Тело карточки */
.manual-card-body {
    margin-bottom: 16px;
    padding-bottom: 14px;
    border-bottom: 1px solid var(--border-color);
}

.manual-description {
    display: flex;
    gap: 10px;
    align-items: flex-start;
    margin-bottom: 12px;
}

.manual-description i {
    color: var(--text-muted);
    margin-top: 2px;
    flex-shrink: 0;
}

.manual-description p {
    color: var(--text-secondary);
    font-size: 0.9rem;
    margin-bottom: 0;
    line-height: 1.4;
}

.manual-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
}

.stat-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.8rem;
    color: var(--text-muted);
}

.stat-item i {
    font-size: 0.75rem;
}

/* Действия */
.manual-card-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.btn-action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 8px 18px;
    font-size: 0.8rem;
    font-weight: 500;
    border-radius: 12px;
    border: 2px solid var(--border-color);
    background: var(--bg-primary);
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.25s ease;
}

.btn-action:hover {
    transform: translateY(-2px);
}

.btn-action:active {
    transform: translateY(0);
}

.btn-view:hover {
    border-color: var(--accent);
    color: var(--accent);
    background: var(--accent-light);
}

.btn-approve:hover {
    border-color: var(--success);
    color: var(--success);
    background: rgba(16, 185, 129, 0.15);
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
}

.btn-reject:hover {
    border-color: var(--danger);
    color: var(--danger);
    background: rgba(239, 68, 68, 0.15);
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.2);
}

.btn-undo:hover {
    border-color: var(--accent);
    color: var(--accent);
    background: var(--accent-light);
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.2);
}

/* ===== Модальное окно просмотра ===== */
.modal-large {
    max-width: 700px;
}

.modal-header-info {
    display: flex;
    align-items: center;
    gap: 12px;
}

.modal-header-info i {
    font-size: 24px;
    color: var(--accent);
}

.modal-close {
    background: var(--bg-secondary);
    border: 2px solid var(--border-color);
    border-radius: 50%;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: var(--text-secondary);
    transition: all 0.3s;
}

.modal-close:hover {
    border-color: var(--danger);
    color: var(--danger);
    background: rgba(239, 68, 68, 0.1);
}

.modal-body {
    max-height: 70vh;
    overflow-y: auto;
    padding-right: 4px;
}

.modal-body::-webkit-scrollbar {
    width: 4px;
}

.modal-body::-webkit-scrollbar-track {
    background: var(--bg-primary);
    border-radius: 10px;
}

.modal-body::-webkit-scrollbar-thumb {
    background: var(--accent);
    border-radius: 10px;
}

.manual-detail-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 2px solid var(--border-color);
}

.detail-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.85rem;
    color: var(--text-secondary);
}

.detail-item i {
    color: var(--text-muted);
}

.manual-detail-description {
    margin-bottom: 20px;
}

.manual-detail-description h4 {
    font-size: 0.9rem;
    color: var(--text-secondary);
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

.manual-detail-description p {
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.5;
    margin-bottom: 0;
}

.manual-detail-steps h4 {
    font-size: 0.9rem;
    color: var(--text-secondary);
    margin-bottom: 12px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

.steps-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.step-item {
    display: flex;
    gap: 14px;
    padding: 14px 16px;
    background: var(--bg-primary);
    border-radius: 14px;
    border: 1px solid var(--border-color);
}

.step-number {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--accent-light);
    border: 2px solid var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 14px;
    color: var(--accent);
    flex-shrink: 0;
}

.step-content {
    flex: 1;
    min-width: 0;
}

.step-text {
    font-size: 0.9rem;
    color: var(--text-primary);
    margin-bottom: 0;
    line-height: 1.4;
}

.step-image-wrapper {
    margin-top: 10px;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid var(--border-color);
}

.step-image {
    width: 100%;
    height: auto;
    max-height: 250px;
    object-fit: cover;
    display: block;
}

/* Модальное окно отклонения */
.modal-text {
    color: var(--text-secondary);
    margin-bottom: 12px;
}

.modal-textarea {
    width: 100%;
    padding: 12px 16px;
    background: var(--bg-secondary);
    border: 2px solid var(--border-color);
    border-radius: 14px;
    color: var(--text-primary);
    font-size: 0.9rem;
    font-family: inherit;
    resize: vertical;
    transition: all 0.3s;
}

.modal-textarea:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15);
}

.modal-textarea::placeholder {
    color: var(--text-muted);
}

/* ===== Адаптивность ===== */

/* Планшеты */
@media (max-width: 1024px) {
    .statistics-cards {
        grid-template-columns: repeat(2, 1fr);
    }

    .modal-large {
        max-width: 90%;
        margin: 20px;
    }
}

/* Планшеты вертикальные */
@media (max-width: 768px) {
    .container {
        padding: 0 16px;
    }

    .section {
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 24px;
    }

    .section-title-wrapper {
        gap: 12px;
    }

    .section-title-wrapper i {
        font-size: 26px;
    }

    .section-title-wrapper h2 {
        font-size: 1.3rem;
    }

    .subtitle {
        font-size: 0.95rem;
    }

    .statistics-cards {
        grid-template-columns: repeat(2, 1fr);
        gap: 14px;
    }

    .stat-card {
        padding: 16px;
    }

    .stat-card-value {
        font-size: 1.5rem;
    }

    .stat-card-title {
        font-size: 0.8rem;
    }

    .filter-group {
        flex-direction: column;
        align-items: stretch;
    }

    .filter-select,
    .filter-input {
        max-width: 100%;
        min-width: unset;
    }

    .manual-card {
        padding: 16px;
    }

    .manual-card-header {
        flex-direction: column;
    }

    .manual-title {
        font-size: 1rem;
    }

    .manual-card-actions {
        justify-content: stretch;
    }

    .manual-card-actions .btn-action {
        flex: 1;
        justify-content: center;
    }

    .modal-large {
        max-width: 95%;
        margin: 12px;
        padding: 16px;
    }

    .modal-body {
        max-height: 60vh;
    }

    .step-item {
        flex-direction: column;
        align-items: stretch;
        padding: 12px;
    }

    .step-number {
        align-self: flex-start;
    }
}

/* Мобильные */
@media (max-width: 480px) {
    .container {
        padding: 0 10px;
    }

    .section {
        padding: 14px;
        border-radius: 16px;
        margin-bottom: 18px;
    }

    .section-title-wrapper {
        gap: 10px;
    }

    .section-title-wrapper i {
        font-size: 20px;
    }

    .section-title-wrapper h2 {
        font-size: 1.1rem;
    }

    .subtitle {
        font-size: 0.85rem;
    }

    .statistics-cards {
        grid-template-columns: 1fr 1fr;
        gap: 10px;
    }

    .stat-card {
        padding: 12px 14px;
        border-radius: 16px;
    }

    .stat-card-value {
        font-size: 1.3rem;
    }

    .stat-card-title {
        font-size: 0.7rem;
    }

    .manual-card {
        padding: 12px;
        border-radius: 16px;
    }

    .manual-icon {
        width: 36px;
        height: 36px;
    }

    .manual-icon i {
        font-size: 16px;
    }

    .manual-title {
        font-size: 0.9rem;
    }

    .manual-tags {
        gap: 4px;
    }

    .tag {
        font-size: 0.65rem;
        padding: 2px 8px;
    }

    .manual-description p {
        font-size: 0.8rem;
    }

    .stat-item {
        font-size: 0.7rem;
        gap: 4px;
    }

    .btn-action {
        font-size: 0.7rem;
        padding: 6px 12px;
    }

    .modal-container {
        padding: 14px;
        border-radius: 16px;
    }

    .modal-header-info i {
        font-size: 18px;
    }

    .modal-title {
        font-size: 1rem;
    }

    .detail-item {
        font-size: 0.75rem;
    }

    .step-text {
        font-size: 0.8rem;
    }

    .step-number {
        width: 28px;
        height: 28px;
        font-size: 12px;
    }
}

/* Очень маленькие экраны */
@media (max-width: 360px) {
    .statistics-cards {
        grid-template-columns: 1fr;
    }

    .manual-card-actions {
        flex-direction: column;
    }

    .manual-card-actions .btn-action {
        width: 100%;
    }

    .modal-actions {
        flex-direction: column;
    }

    .modal-actions button {
        width: 100%;
    }
}
</style>