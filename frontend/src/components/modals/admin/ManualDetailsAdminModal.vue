<template>
    <ModalWrapper
        :isOpen="isOpen"
        :title="manual?.title || 'Мануал'"
        :subtitle="manual?.motorcycle || 'Мотоцикл'"
        icon="book"
        @close="$emit('close')"
    >
        <div class="modal-scroll">
            <div class="modal-header">
                <div class="header-top">
                    <span
                        class="badge"
                        :class="{
                            'badge-green': manual?.status === 'approved',
                            'badge-warning': manual?.status === 'moderate',
                            'badge-danger': manual?.status === 'rejected'
                        }"
                    >
                        {{ getStatusLabel(manual?.status) }}
                    </span>
                    <span v-if="manual?.created_at" class="header-date">
                        <i class="fa fa-clock-o"></i> {{ formatDate(manual.created_at) }}
                    </span>
                </div>

                <p v-if="manual?.description" class="header-subtitle">
                    {{ manual.description }}
                </p>
            </div>

            <div class="modal-card">
                <p class="modal-card-title">Информация о мануале</p>
                <div class="card-items">
                    <div v-if="manual?.category" class="card-item">
                        <span class="item-title">
                            <i class="fa fa-tags"></i> Категория
                        </span>
                        <span class="item-value">{{ getCategory(manual.category) }}</span>
                    </div>

                    <div v-if="manual?.difficult" class="card-item">
                        <span class="item-title">
                            <i class="fa fa-signal"></i> Сложность
                        </span>
                        <span class="item-value">{{ getDifficulty(manual.difficult) }}</span>
                    </div>

                    <div v-if="manual?.instruments" class="card-item">
                        <span class="item-title">
                            <i class="fa fa-wrench"></i> Инструменты
                        </span>
                        <span class="item-value">{{ manual.instruments }}</span>
                    </div>

                    <div v-if="manual?.parts" class="card-item">
                        <span class="item-title">
                            <i class="fa fa-cogs"></i> Запчасти
                        </span>
                        <span class="item-value">{{ manual.parts }}</span>
                    </div>

                    <div v-if="manual?.author" class="card-item">
                        <span class="item-title">
                            <i class="fa fa-user"></i> Автор
                        </span>
                        <span class="item-value">{{ manual.author?.username || '—' }}</span>
                    </div>
                </div>
            </div>

            <!-- Steps -->
            <div v-if="manual?.steps && manual.steps.length > 0" class="modal-card steps-card">
                <p class="modal-card-title">
                    <i class="fa fa-list-ol"></i> Шаги выполнения
                </p>
                <div class="steps-list">
                    <div 
                        v-for="(step, index) in manual.steps" 
                        :key="index"
                        class="step-item"
                    >
                        <div class="step-number">{{ step.order || index + 1 }}</div>
                        <div class="step-content">
                            <p class="step-title">{{ step.title }}</p>
                            <p v-if="step.text" class="step-text">{{ step.text }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- === ADMIN ACTIONS (для модерации) === -->
        <div class="admin-actions-wrapper">
            <div class="admin-buttons">
                <!-- Одобрить (Только если на проверке) -->
                <button 
                    v-if="manual?.status === 'moderate'" 
                    @click="$emit('approve', manual.id)" 
                    class="btn-action btn-success"
                >
                    <i class="fa fa-check"></i> Одобрить
                </button>

                <!-- Отклонить (Только если на проверке) -->
                <button 
                    v-if="manual?.status === 'moderate'" 
                    @click="openRejectModal" 
                    class="btn-action btn-danger"
                >
                    <i class="fa fa-times"></i> Отклонить
                </button>

                <!-- Удалить (Всегда доступно) -->
                <button 
                    @click="confirmDelete" 
                    class="btn-action btn-delete"
                >
                    <i class="fa fa-trash"></i> Удалить
                </button>
            </div>
            
            <!-- Кнопка закрытия -->
            <button @click="$emit('close')" class="btn-close">Закрыть</button>
        </div>

        <!-- === ВСТРОЕННАЯ МОДАЛКА ДЛЯ ПРИЧИНЫ ОТКЛОНЕНИЯ === -->
        <div v-if="showRejectModal" class="reject-overlay" @click.self="closeRejectModal">
            <div class="reject-box">
                <h4 class="reject-title">Причина отклонения</h4>
                <p class="reject-sub">Укажите причину, чтобы автор мог исправить ошибки</p>
                <textarea 
                    v-model="rejectReason" 
                    class="reject-input" 
                    placeholder="Например: Не хватает шагов, ошибки в тексте..."
                    rows="4"
                ></textarea>
                <div class="reject-actions">
                    <button class="btn-cancel" @click="closeRejectModal">Отмена</button>
                    <button class="btn-confirm-reject" @click="submitReject">
                        <i class="fa fa-times"></i> Отклонить
                    </button>
                </div>
            </div>
        </div>
    </ModalWrapper>
</template>

<script>
import ModalWrapper from '../ModalWrapper.vue';

export default {
    components: {
        ModalWrapper
    },

    props: {
        isOpen: {
            type: Boolean,
            required: true,
            default: false
        },
        manual: {
            type: Object,
            required: true,
            default: null
        },
    },

    emits: ['close', 'approve', 'reject', 'delete'],

    data() {
        return {
            showRejectModal: false,
            rejectReason: '',
        }
    },

    methods: {
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

        getStatusLabel(status) {
            const labels = {
                'approved': 'Одобрен',
                'moderate': 'На проверке',
                'rejected': 'Отклонён',
                'draft': 'Черновик'
            }
            return labels[status] || status || '—'
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

        getDifficulty(difficult) {
            const difficulties = {
                'easy': 'Лёгкая',
                'medium': 'Средняя',
                'hard': 'Сложная'
            }
            return difficulties[difficult] || difficult
        },

        // === Логика модерации ===
        openRejectModal() {
            this.rejectReason = '';
            this.showRejectModal = true;
        },
        closeRejectModal() {
            this.showRejectModal = false;
        },
        submitReject() {
            // Передаем ID мануала и причину на родительский компонент
            this.$emit('reject', { 
                id: this.manual.id, 
                reason: this.rejectReason.trim() || 'Без указания причины' 
            });
            this.closeRejectModal();
        },
        confirmDelete() {
            if (confirm('Вы уверены, что хотите удалить этот мануал?')) {
                this.$emit('delete', this.manual.id);
            }
        }
    }
}
</script>

<style scoped>
/* ===== Основной скролл ===== */
.modal-scroll {
    max-height: 60vh;
    overflow-y: auto;
    padding-right: 4px;
}
.modal-scroll::-webkit-scrollbar {
    width: 4px;
}
.modal-scroll::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 4px;
}
.modal-scroll::-webkit-scrollbar-thumb {
    background: #7c3aed;
    border-radius: 4px;
}
.modal-scroll::-webkit-scrollbar-thumb:hover {
    background: #6d28d9;
}
.modal-scroll {
    scrollbar-width: thin;
    scrollbar-color: #7c3aed rgba(255, 255, 255, 0.03);
}

/* ===== Header ===== */
.modal-header {
    margin-bottom: 20px;
}
.header-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    flex-wrap: wrap;
    gap: 8px;
}
.badge {
    display: inline-block;
    padding: 3px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.3px;
}
.badge-green { background: rgba(74, 222, 128, 0.12); color: #4ade80; }
.badge-warning { background: rgba(251, 191, 36, 0.12); color: #fbbf24; }
.badge-danger { background: rgba(239, 68, 68, 0.12); color: #ef4444; }
.badge-gray { background: rgba(107, 114, 128, 0.12); color: #9ca3af; }

.header-date {
    font-size: 13px;
    color: #8b8b9e;
}
.header-date i { margin-right: 4px; }

.header-subtitle {
    font-size: 14px;
    color: #8b8b9e;
    margin: 0;
    line-height: 1.5;
}

/* ===== Карточки информации ===== */
.modal-card {
    background: #0f0f1a;
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 12px;
}
.steps-card { margin-bottom: 16px; }
.modal-card-title {
    font-size: 13px;
    font-weight: 600;
    color: #8b8b9e;
    margin: 0 0 14px 0;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}
.modal-card-title i { margin-right: 6px; }

.card-items {
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.card-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 12px;
    background: #181824;
    border-radius: 8px;
    transition: background 0.2s;
}
.card-item:hover { background: #1e1e2e; }
.item-title {
    font-size: 13px;
    color: #8b8b9e;
}
.item-title i {
    margin-right: 6px;
    font-size: 13px;
    color: #7c3aed;
    width: 16px;
    text-align: center;
}
.item-value {
    font-size: 14px;
    font-weight: 500;
    color: #e0e0e0;
    text-align: right;
    max-width: 60%;
    word-break: break-word;
}

/* ===== Steps ===== */
.steps-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.step-item {
    display: flex;
    gap: 14px;
    padding: 12px 14px;
    background: #181824;
    border-radius: 8px;
    transition: background 0.2s;
}
.step-item:hover { background: #1e1e2e; }
.step-number {
    flex-shrink: 0;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #7c3aed;
    border-radius: 50%;
    font-size: 13px;
    font-weight: 600;
    color: #fff;
}
.step-content { flex: 1; min-width: 0; }
.step-title {
    font-size: 14px;
    font-weight: 500;
    color: #e0e0e0;
    margin: 0 0 4px 0;
}
.step-text {
    font-size: 13px;
    color: #8b8b9e;
    margin: 0;
    line-height: 1.5;
}

/* ===== ADMIN ACTIONS (Нижняя панель) ===== */
.admin-actions-wrapper {
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
}

.admin-buttons {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.btn-action {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 8px 18px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    border: none;
    cursor: pointer;
    transition: all 0.2s ease;
    color: #fff;
}
.btn-action i { font-size: 14px; }

.btn-success {
    background: #22c55e;
}
.btn-success:hover {
    background: #16a34a;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(34, 197, 94, 0.25);
}

.btn-danger {
    background: #ef4444;
}
.btn-danger:hover {
    background: #dc2626;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.25);
}

.btn-delete {
    background: transparent;
    border: 1px solid rgba(239, 68, 68, 0.2);
    color: #f87171;
}
.btn-delete:hover {
    background: rgba(239, 68, 68, 0.1);
    border-color: rgba(239, 68, 68, 0.4);
}

.btn-close {
    padding: 8px 20px;
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    color: #b0b0c8;
    cursor: pointer;
    transition: 0.2s;
    font-size: 14px;
}
.btn-close:hover {
    background: rgba(255, 255, 255, 0.04);
    border-color: rgba(255, 255, 255, 0.15);
    color: #e0e0e0;
}

/* ===== ВСТРОЕННАЯ МОДАЛКА ОТКЛОНЕНИЯ ===== */
.reject-overlay {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2000;
}
.reject-box {
    background: #181824;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 24px;
    max-width: 420px;
    width: 90%;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}
.reject-title {
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 4px 0;
}
.reject-sub {
    font-size: 14px;
    color: #8b8b9e;
    margin: 0 0 16px 0;
}
.reject-input {
    width: 100%;
    padding: 12px;
    background: #0f0f1a;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    color: #e0e0e0;
    font-size: 14px;
    font-family: inherit;
    resize: vertical;
    outline: none;
    transition: border 0.2s;
}
.reject-input:focus {
    border-color: #7c3aed;
}
.reject-actions {
    display: flex;
    gap: 10px;
    margin-top: 16px;
    justify-content: flex-end;
}
.btn-cancel {
    padding: 8px 20px;
    background: transparent;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    color: #b0b0c8;
    cursor: pointer;
    font-size: 14px;
}
.btn-cancel:hover {
    background: rgba(255,255,255,0.05);
}
.btn-confirm-reject {
    padding: 8px 20px;
    background: #ef4444;
    border: none;
    border-radius: 8px;
    color: #fff;
    cursor: pointer;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: 0.2s;
}
.btn-confirm-reject:hover {
    background: #dc2626;
}

/* ===== Responsive ===== */
@media (max-width: 480px) {
    .modal-scroll { max-height: 50vh; }
    .header-top { flex-direction: column; align-items: flex-start; }
    .card-item { flex-direction: column; align-items: flex-start; gap: 4px; }
    .item-value { text-align: left; max-width: 100%; }
    .step-item { flex-direction: column; align-items: flex-start; gap: 8px; }
    .admin-actions-wrapper { flex-direction: column-reverse; align-items: stretch; }
    .admin-buttons { flex-direction: column; }
    .btn-action, .btn-close { width: 100%; text-align: center; justify-content: center; }
    .reject-actions { flex-direction: column; }
    .btn-cancel, .btn-confirm-reject { width: 100%; justify-content: center; }
}
</style>