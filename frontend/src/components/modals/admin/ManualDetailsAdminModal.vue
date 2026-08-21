<template>
    <ModalWrapper
        :isOpen="isOpen"
        :title="manual?.title || 'Мануал'"
        :subtitle="manual?.motorcycle || 'Мотоцикл'"
        icon="book"
        @close="$emit('close')"
    >
        <div class="modal-content">
            <!-- Хедер с информацией -->
            <div class="modal-header">
                <div class="header-row">
                    <div class="header-left">
                        <span
                            class="badge"
                            :class="{
                                'badge-success': manual?.status === 'approved',
                                'badge-warning': manual?.status === 'moderate',
                                'badge-danger': manual?.status === 'rejected',
                                'badge-info': manual?.status === 'draft'
                            }"
                        >
                            <i class="fa" :class="{
                                'fa-check-circle': manual?.status === 'approved',
                                'fa-hourglass-half': manual?.status === 'moderate',
                                'fa-times-circle': manual?.status === 'rejected',
                                'fa-pencil': manual?.status === 'draft'
                            }"></i>
                            {{ getStatusLabel(manual?.status) }}
                        </span>
                        <span v-if="manual?.created_at" class="header-date">
                            <i class="fa fa-calendar"></i> {{ formatDate(manual.created_at) }}
                        </span>
                    </div>
                    <div class="header-right">
                        <span v-if="manual?.views" class="view-count">
                            <i class="fa fa-eye"></i> {{ manual.views }}
                        </span>
                    </div>
                </div>

                <p v-if="manual?.description" class="header-description">
                    {{ manual.description }}
                </p>

                <!-- Админ-статус индикатор -->
                <div v-if="manual?.status === 'moderate'" class="moderation-banner">
                    <i class="fa fa-clock-o"></i>
                    <span>Этот мануал ожидает модерации</span>
                </div>
                <div v-else-if="manual?.status === 'rejected' && manual?.reject_reason" class="rejection-banner">
                    <i class="fa fa-exclamation-triangle"></i>
                    <span>Причина отклонения: {{ manual.reject_reason }}</span>
                </div>
            </div>

            <!-- Информационная сетка -->
            <div class="info-grid">
                <div class="info-card" v-if="manual?.category">
                    <div class="info-icon">
                        <i class="fa fa-tags"></i>
                    </div>
                    <div class="info-content">
                        <span class="info-label">Категория</span>
                        <span class="info-value">{{ getCategory(manual.category) }}</span>
                    </div>
                </div>

                <div class="info-card" v-if="manual?.difficult">
                    <div class="info-icon">
                        <i class="fa fa-signal"></i>
                    </div>
                    <div class="info-content">
                        <span class="info-label">Сложность</span>
                        <span class="info-value">
                            <span class="difficulty-dots">
                                <span class="dot" :class="{ filled: manual.difficult === 'easy' || manual.difficult === 'medium' || manual.difficult === 'hard' }"></span>
                                <span class="dot" :class="{ filled: manual.difficult === 'medium' || manual.difficult === 'hard' }"></span>
                                <span class="dot" :class="{ filled: manual.difficult === 'hard' }"></span>
                            </span>
                            {{ getDifficulty(manual.difficult) }}
                        </span>
                    </div>
                </div>

                <div class="info-card" v-if="manual?.author">
                    <div class="info-icon">
                        <i class="fa fa-user"></i>
                    </div>
                    <div class="info-content">
                        <span class="info-label">Автор</span>
                        <span class="info-value">{{ manual.author?.username || '—' }}</span>
                    </div>
                </div>

                <div class="info-card" v-if="manual?.instruments">
                    <div class="info-icon">
                        <i class="fa fa-wrench"></i>
                    </div>
                    <div class="info-content">
                        <span class="info-label">Инструменты</span>
                        <span class="info-value">{{ manual.instruments }}</span>
                    </div>
                </div>

                <div class="info-card" v-if="manual?.parts">
                    <div class="info-icon">
                        <i class="fa fa-cogs"></i>
                    </div>
                    <div class="info-content">
                        <span class="info-label">Запчасти</span>
                        <span class="info-value">{{ manual.parts }}</span>
                    </div>
                </div>

                <div class="info-card" v-if="manual?.updated_at && manual?.updated_at !== manual?.created_at">
                    <div class="info-icon">
                        <i class="fa fa-pencil-square-o"></i>
                    </div>
                    <div class="info-content">
                        <span class="info-label">Обновлён</span>
                        <span class="info-value">{{ formatDate(manual.updated_at) }}</span>
                    </div>
                </div>
            </div>

            <!-- Шаги -->
            <div v-if="manual?.steps && manual.steps.length > 0" class="steps-section">
                <div class="steps-header">
                    <h4 class="steps-title">
                        <i class="fa fa-list-ol"></i> Шаги выполнения
                    </h4>
                    <span class="steps-count">{{ manual.steps.length }} шаг{{ manual.steps.length > 1 ? 'а' : '' }}</span>
                </div>

                <div class="steps-list">
                    <div 
                        v-for="(step, index) in manual.steps" 
                        :key="index"
                        class="step-item"
                    >
                        <div class="step-marker">
                            <span class="step-number">{{ step.order || index + 1 }}</span>
                            <div class="step-line" v-if="index < manual.steps.length - 1"></div>
                        </div>
                        <div class="step-body">
                            <div class="step-header">
                                <span class="step-title">{{ step.title }}</span>
                            </div>
                            <p v-if="step.text" class="step-text">{{ step.text }}</p>
                            <div v-if="step.image" class="step-image">
                                <img :src="step.image" :alt="step.title" loading="lazy" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Пустое состояние -->
            <div v-else class="empty-steps">
                <i class="fa fa-file-text-o"></i>
                <p>Нет шагов для отображения</p>
            </div>
        </div>

        <!-- Админ-действия -->
        <div class="modal-footer admin-footer">
            <div class="admin-actions">
                <!-- Одобрить -->
                <button 
                    v-if="manual?.status === 'moderate'" 
                    @click="$emit('approve', manual.id)" 
                    class="btn btn-success"
                >
                    <i class="fa fa-check"></i> Одобрить
                </button>

                <!-- Отклонить -->
                <button 
                    v-if="manual?.status === 'moderate'" 
                    @click="openRejectModal" 
                    class="btn btn-danger"
                >
                    <i class="fa fa-times"></i> Отклонить
                </button>

                <!-- Удалить -->
                <button 
                    @click="confirmDelete" 
                    class="btn btn-delete"
                >
                    <i class="fa fa-trash"></i> Удалить
                </button>
            </div>

            <button @click="$emit('close')" class="btn btn-outline">
                <i class="fa fa-times"></i> Закрыть
            </button>
        </div>

        <!-- Модалка для причины отклонения -->
        <div v-if="showRejectModal" class="reject-overlay" @click.self="closeRejectModal">
            <div class="reject-box">
                <div class="reject-header">
                    <h4 class="reject-title">Отклонить мануал</h4>
                    <button class="reject-close" @click="closeRejectModal">
                        <i class="fa fa-times"></i>
                    </button>
                </div>
                <p class="reject-sub">Укажите причину отклонения, чтобы автор мог исправить ошибки</p>
                <textarea 
                    v-model="rejectReason" 
                    class="reject-input" 
                    placeholder="Например: Не хватает шагов, ошибки в тексте, неверная категория..."
                    rows="4"
                ></textarea>
                <div class="reject-actions">
                    <button class="btn btn-cancel" @click="closeRejectModal">Отмена</button>
                    <button class="btn btn-confirm-reject" @click="submitReject">
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
                    month: 'long',
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

        openRejectModal() {
            this.rejectReason = '';
            this.showRejectModal = true;
        },

        closeRejectModal() {
            this.showRejectModal = false;
        },

        submitReject() {
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
/* ===== CSS Переменные (для консистентности) ===== */
:root {
    --bg-primary: #0a0a12;
    --bg-secondary: #0f0f1a;
    --bg-card-hover: #181824;
    --bg-tertiary: #181824;
    --text-primary: #e8e8f0;
    --text-secondary: #b0b0c8;
    --text-muted: #7a7a94;
    --border-color: rgba(255, 255, 255, 0.06);
    --accent: #7c3aed;
    --accent-hover: #6d28d9;
    --accent-trans: rgba(124, 58, 237, 0.12);
    --success: #4ade80;
    --success-trans: rgba(74, 222, 128, 0.12);
    --warning: #fbbf24;
    --warning-trans: rgba(251, 191, 36, 0.12);
    --danger: #ef4444;
    --danger-trans: rgba(239, 68, 68, 0.12);
    --shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

/* ===== ОСНОВНОЙ КОНТЕЙНЕР ===== */
.modal-content {
    padding: 0 4px;
    max-height: 55vh;
    overflow-y: auto;
    scroll-behavior: smooth;
}

/* Стилизация скроллбара */
.modal-content::-webkit-scrollbar {
    width: 5px;
}

.modal-content::-webkit-scrollbar-track {
    background: var(--bg-secondary);
    border-radius: 10px;
}

.modal-content::-webkit-scrollbar-thumb {
    background: var(--accent);
    border-radius: 10px;
    transition: background 0.3s;
}

.modal-content::-webkit-scrollbar-thumb:hover {
    background: var(--accent-hover);
}

.modal-content {
    scrollbar-width: thin;
    scrollbar-color: var(--accent) var(--bg-secondary);
}

/* ===== ХЕДЕР ===== */
.modal-header {
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--border-color);
}

.header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 12px;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
}

.header-right {
    display: flex;
    align-items: center;
    gap: 8px;
}

.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}

.badge i {
    font-size: 13px;
}

.badge-success {
    background: var(--success-trans);
    color: var(--success);
}

.badge-warning {
    background: var(--warning-trans);
    color: var(--warning);
}

.badge-danger {
    background: var(--danger-trans);
    color: var(--danger);
}

.badge-info {
    background: var(--accent-trans);
    color: var(--accent);
}

.header-date {
    font-size: 13px;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 4px;
}

.header-date i {
    font-size: 13px;
}

.view-count {
    font-size: 13px;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 4px;
}

.header-description {
    width: 100%;
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.6;
    padding: 10px 14px;
    background: var(--bg-secondary);
    border-radius: 8px;
    border-left: 3px solid var(--accent);
}

/* ===== Баннеры модерации ===== */
.moderation-banner,
.rejection-banner {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 10px;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 500;
}

.moderation-banner {
    background: var(--warning-trans);
    color: var(--warning);
    border: 1px solid rgba(251, 191, 36, 0.15);
}

.rejection-banner {
    background: var(--danger-trans);
    color: var(--danger);
    border: 1px solid rgba(239, 68, 68, 0.15);
}

.moderation-banner i,
.rejection-banner i {
    font-size: 16px;
    flex-shrink: 0;
}

/* ===== ИНФО-СЕТКА ===== */
.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 10px;
    margin-bottom: 20px;
}

.info-card {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: var(--bg-secondary);
    border-radius: 10px;
    border: 1px solid var(--border-color);
    transition: all 0.2s ease;
}

.info-card:hover {
    border-color: var(--accent);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.info-icon {
    flex-shrink: 0;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--accent-trans);
    border-radius: 8px;
    color: var(--accent);
    font-size: 16px;
}

.info-content {
    flex: 1;
    min-width: 0;
}

.info-label {
    display: block;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-muted);
    margin-bottom: 2px;
}

.info-value {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-primary);
    word-break: break-word;
}

/* Индикатор сложности */
.difficulty-dots {
    display: inline-flex;
    gap: 4px;
    margin-right: 8px;
    vertical-align: middle;
}

.dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--border-color);
    transition: background 0.3s;
}

.dot.filled {
    background: var(--warning);
}

/* ===== ШАГИ ===== */
.steps-section {
    margin-top: 4px;
}

.steps-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
}

.steps-title {
    font-size: 15px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.steps-title i {
    color: var(--accent);
}

.steps-count {
    font-size: 12px;
    color: var(--text-muted);
    background: var(--bg-secondary);
    padding: 2px 12px;
    border-radius: 12px;
}

.steps-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.step-item {
    display: flex;
    gap: 16px;
    padding: 16px 18px;
    background: var(--bg-secondary);
    border-radius: 12px;
    border: 1px solid var(--border-color);
    transition: all 0.2s ease;
    position: relative;
}

.step-item:hover {
    border-color: var(--accent);
    background: var(--bg-card-hover);
}

.step-marker {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-shrink: 0;
}

.step-number {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--accent);
    border-radius: 50%;
    font-size: 13px;
    font-weight: 700;
    color: #fff;
    flex-shrink: 0;
    transition: all 0.3s;
}

.step-item:hover .step-number {
    transform: scale(1.05);
    box-shadow: 0 0 20px var(--accent-trans);
}

.step-line {
    width: 2px;
    flex: 1;
    min-height: 20px;
    background: var(--border-color);
    margin: 6px 0;
    position: relative;
}

.step-item:last-child .step-line {
    display: none;
}

.step-body {
    flex: 1;
    min-width: 0;
}

.step-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 8px;
    margin-bottom: 4px;
}

.step-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
}

.step-text {
    font-size: 13.5px;
    color: var(--text-secondary);
    margin: 4px 0 0 0;
    line-height: 1.6;
}

.step-image {
    margin-top: 10px;
    border-radius: 8px;
    overflow: hidden;
    max-width: 100%;
}

.step-image img {
    width: 100%;
    max-height: 200px;
    object-fit: cover;
    border-radius: 8px;
    border: 1px solid var(--border-color);
}

/* ===== ПУСТОЕ СОСТОЯНИЕ ===== */
.empty-steps {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    background: var(--bg-secondary);
    border-radius: 12px;
    border: 2px dashed var(--border-color);
    text-align: center;
}

.empty-steps i {
    font-size: 32px;
    color: var(--text-muted);
    margin-bottom: 12px;
    opacity: 0.5;
}

.empty-steps p {
    color: var(--text-muted);
    font-size: 14px;
    margin: 0;
}

/* ===== ФУТЕР С АДМИН-ДЕЙСТВИЯМИ ===== */
.modal-footer {
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
}

.admin-footer {
    padding-top: 16px;
}

.admin-actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

/* ===== КНОПКИ ===== */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 9px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    border: none;
    cursor: pointer;
    transition: all 0.2s ease;
    color: #fff;
    text-decoration: none;
}

.btn i {
    font-size: 14px;
}

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
    border: 1px solid rgba(239, 68, 68, 0.25);
    color: #f87171;
}

.btn-delete:hover {
    background: rgba(239, 68, 68, 0.08);
    border-color: rgba(239, 68, 68, 0.4);
    transform: translateY(-1px);
}

.btn-outline {
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-secondary);
}

.btn-outline:hover {
    background: var(--bg-secondary);
    border-color: rgba(255, 255, 255, 0.15);
    color: var(--text-primary);
}

.btn-cancel {
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-secondary);
}

.btn-cancel:hover {
    background: var(--bg-secondary);
    border-color: rgba(255, 255, 255, 0.15);
}

.btn-confirm-reject {
    background: #ef4444;
}

.btn-confirm-reject:hover {
    background: #dc2626;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.25);
}

/* ===== МОДАЛКА ОТКЛОНЕНИЯ ===== */
.reject-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(6px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2000;
    animation: fadeIn 0.2s ease;
}

.reject-box {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 28px;
    max-width: 440px;
    width: 92%;
    box-shadow: var(--shadow);
    animation: slideUp 0.3s ease;
}

.reject-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
}

.reject-close {
    background: none;
    border: none;
    color: var(--text-muted);
    font-size: 20px;
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 6px;
    transition: all 0.2s;
}

.reject-close:hover {
    background: var(--bg-card-hover);
    color: var(--text-primary);
}

.reject-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
}

.reject-sub {
    font-size: 14px;
    color: var(--text-muted);
    margin: 6px 0 16px 0;
}

.reject-input {
    width: 100%;
    padding: 12px 14px;
    background: var(--bg-primary);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    color: var(--text-primary);
    font-size: 14px;
    font-family: inherit;
    resize: vertical;
    outline: none;
    transition: border 0.2s;
    min-height: 100px;
}

.reject-input:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-trans);
}

.reject-input::placeholder {
    color: var(--text-muted);
}

.reject-actions {
    display: flex;
    gap: 10px;
    margin-top: 16px;
    justify-content: flex-end;
}

.reject-actions .btn {
    padding: 9px 24px;
}

/* ===== АНИМАЦИИ ===== */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px) scale(0.98);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

.step-item {
    animation: fadeInUp 0.3s ease forwards;
    opacity: 0;
}

.step-item:nth-child(1) { animation-delay: 0.05s; }
.step-item:nth-child(2) { animation-delay: 0.10s; }
.step-item:nth-child(3) { animation-delay: 0.15s; }
.step-item:nth-child(4) { animation-delay: 0.20s; }
.step-item:nth-child(5) { animation-delay: 0.25s; }
.step-item:nth-child(6) { animation-delay: 0.30s; }

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.info-card {
    animation: fadeInUp 0.3s ease forwards;
    opacity: 0;
}

.info-card:nth-child(1) { animation-delay: 0.05s; }
.info-card:nth-child(2) { animation-delay: 0.10s; }
.info-card:nth-child(3) { animation-delay: 0.15s; }
.info-card:nth-child(4) { animation-delay: 0.20s; }
.info-card:nth-child(5) { animation-delay: 0.25s; }
.info-card:nth-child(6) { animation-delay: 0.30s; }

/* ===== АДАПТИВНОСТЬ ===== */
@media (max-width: 768px) {
    .info-grid {
        grid-template-columns: 1fr 1fr;
        gap: 8px;
    }
}

@media (max-width: 640px) {
    .modal-content {
        max-height: 50vh;
        padding-right: 2px;
    }

    .header-row {
        flex-direction: column;
        align-items: flex-start;
    }

    .header-left {
        width: 100%;
        flex-wrap: wrap;
    }

    .header-right {
        width: 100%;
        justify-content: flex-start;
    }

    .info-grid {
        grid-template-columns: 1fr;
    }

    .info-card {
        padding: 10px 14px;
    }

    .info-icon {
        width: 32px;
        height: 32px;
        font-size: 14px;
    }

    .step-item {
        padding: 14px;
        gap: 12px;
    }

    .step-number {
        width: 28px;
        height: 28px;
        font-size: 12px;
    }

    .modal-footer {
        flex-direction: column-reverse;
        align-items: stretch;
    }

    .admin-actions {
        flex-direction: column;
        width: 100%;
    }

    .admin-actions .btn {
        width: 100%;
        justify-content: center;
    }

    .btn-outline {
        width: 100%;
        justify-content: center;
    }

    .reject-box {
        padding: 20px;
        width: 95%;
    }

    .reject-actions {
        flex-direction: column;
    }

    .reject-actions .btn {
        width: 100%;
        justify-content: center;
    }
}

@media (max-width: 420px) {
    .header-description {
        font-size: 13px;
        padding: 8px 12px;
    }

    .step-title {
        font-size: 13px;
    }

    .step-text {
        font-size: 12.5px;
    }

    .badge {
        font-size: 11px;
        padding: 3px 10px;
    }
}
</style>