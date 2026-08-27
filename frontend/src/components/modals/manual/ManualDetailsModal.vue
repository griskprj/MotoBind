<template>
    <ModalWrapper
        :isOpen="isOpen"
        :title="manual?.title || 'Мануал'"
        :subtitle="manual?.motorcycle || 'Мотоцикл'"
        icon="book"
        bg-icon-color="var(--accent-trans)"
        icon-color="var(--accent-text)"
        size="lg"
        @close="$emit('close')"
    >
        <!-- Статус и мета-информация -->
        <div class="manual-meta">
            <div class="manual-meta-left">
                <span
                    class="status-badge"
                    :class="{
                        'status-approved': manual?.status === 'approved',
                        'status-moderate': manual?.status === 'moderate',
                        'status-rejected': manual?.status === 'rejected',
                        'status-draft': manual?.status === 'draft'
                    }"
                >
                    <i :class="statusIcon"></i>
                    {{ getStatusLabel(manual?.status) }}
                </span>
                <span v-if="manual?.created_at" class="meta-date">
                    <i class="fa fa-calendar"></i> {{ formatDate(manual.created_at) }}
                </span>
            </div>
            <div v-if="manual?.views" class="manual-meta-right">
                <span class="meta-views">
                    <i class="fa fa-eye"></i> {{ manual.views }}
                </span>
            </div>
        </div>

        <!-- Описание -->
        <p v-if="manual?.description" class="manual-description">
            {{ manual.description }}
        </p>

        <!-- Информационная сетка -->
        <div class="info-grid">
            <div v-if="manual?.category" class="info-card">
                <div class="info-icon"><i class="fa fa-tags"></i></div>
                <div class="info-content">
                    <span class="info-label">Категория</span>
                    <span class="info-value">{{ getCategory(manual.category) }}</span>
                </div>
            </div>

            <div v-if="manual?.difficult" class="info-card">
                <div class="info-icon"><i class="fa fa-signal"></i></div>
                <div class="info-content">
                    <span class="info-label">Сложность</span>
                    <span class="info-value">
                        <span class="difficulty-dots">
                            <span class="dot" :class="{ filled: ['easy', 'medium', 'hard'].includes(manual.difficult) }"></span>
                            <span class="dot" :class="{ filled: ['medium', 'hard'].includes(manual.difficult) }"></span>
                            <span class="dot" :class="{ filled: manual.difficult === 'hard' }"></span>
                        </span>
                        {{ getDifficulty(manual.difficult) }}
                    </span>
                </div>
            </div>

            <div v-if="manual?.author" class="info-card">
                <div class="info-icon"><i class="fa fa-user"></i></div>
                <div class="info-content">
                    <span class="info-label">Автор</span>
                    <span class="info-value">{{ manual.author?.username || '—' }}</span>
                </div>
            </div>

            <div v-if="manual?.instruments" class="info-card">
                <div class="info-icon"><i class="fa fa-wrench"></i></div>
                <div class="info-content">
                    <span class="info-label">Инструменты</span>
                    <span class="info-value">{{ manual.instruments }}</span>
                </div>
            </div>

            <div v-if="manual?.parts" class="info-card">
                <div class="info-icon"><i class="fa fa-cogs"></i></div>
                <div class="info-content">
                    <span class="info-label">Запчасти</span>
                    <span class="info-value">{{ manual.parts }}</span>
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
                    :class="{ 'step-completed': step.completed }"
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

        <!-- Действия -->
        <template #actions>
            <div class="modal-actions">
                <button class="btn btn-secondary" @click="$emit('close')">
                    <i class="fa fa-times"></i> Закрыть
                </button>
            </div>
        </template>
    </ModalWrapper>
</template>

<script>
import ModalWrapper from '../ModalWrapper.vue'

export default {
    components: { ModalWrapper },

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
        canEdit: {
            type: Boolean,
            default: false
        }
    },

    emits: ['close', 'edit'],

    computed: {
        statusIcon() {
            const icons = {
                'approved': 'fa fa-check-circle',
                'moderate': 'fa fa-hourglass-half',
                'rejected': 'fa fa-times-circle',
                'draft': 'fa fa-pencil'
            }
            return icons[this.manual?.status] || 'fa-circle'
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
        }
    }
}
</script>

<style scoped>
/* ===== СТАТУС И МЕТА ===== */
.manual-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 12px;
}

.manual-meta-left {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}

.manual-meta-right {
    display: flex;
    align-items: center;
    gap: 10px;
}

.status-badge {
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

.status-approved {
    background: var(--success-trans);
    color: var(--success-text);
}

.status-moderate {
    background: var(--warning-trans);
    color: var(--warning-text);
}

.status-rejected {
    background: var(--danger-trans);
    color: var(--danger-text);
}

.status-draft {
    background: var(--accent-trans);
    color: var(--accent-text);
}

.meta-date,
.meta-views {
    font-size: 13px;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 4px;
}

/* ===== ОПИСАНИЕ ===== */
.manual-description {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0 0 16px 0;
    line-height: 1.6;
    padding: 10px 14px;
    background: var(--bg-secondary);
    border-radius: 8px;
    border-left: 3px solid var(--accent);
}

/* ===== ИНФО-СЕТКА ===== */
.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 10px;
    margin-bottom: 18px;
}

.info-card {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 14px;
    background: var(--bg-secondary);
    border-radius: 10px;
    border: 1px solid var(--border-light);
    transition: all 0.2s ease;
}

.info-card:hover {
    border-color: var(--accent);
    transform: translateY(-1px);
}

.info-icon {
    flex-shrink: 0;
    width: 34px;
    height: 34px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--accent-trans);
    border-radius: 8px;
    color: var(--accent-text);
    font-size: 15px;
}

.info-content {
    flex: 1;
    min-width: 0;
}

.info-label {
    display: block;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-muted);
    margin-bottom: 1px;
}

.info-value {
    font-size: 13px;
    font-weight: 500;
    color: var(--text-primary);
    word-break: break-word;
}

/* Индикатор сложности */
.difficulty-dots {
    display: inline-flex;
    gap: 4px;
    margin-right: 6px;
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
    background: var(--warning-text);
}

/* ===== ШАГИ ===== */
.steps-section {
    margin-top: 4px;
}

.steps-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
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
    color: var(--accent-text);
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
    gap: 10px;
}

.step-item {
    display: flex;
    gap: 14px;
    padding: 14px 16px;
    background: var(--bg-secondary);
    border-radius: 12px;
    border: 1px solid var(--border-light);
    transition: all 0.2s ease;
}

.step-item:hover {
    border-color: var(--accent-trans);
    background: var(--bg-card-hover);
}

.step-item.step-completed {
    border-color: var(--success);
}

.step-marker {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-shrink: 0;
}

.step-number {
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--accent);
    border-radius: 50%;
    font-size: 12px;
    font-weight: 700;
    color: #fff;
    flex-shrink: 0;
}

.step-line {
    width: 2px;
    flex: 1;
    min-height: 16px;
    background: var(--border-color);
    margin: 4px 0;
}

.step-item:last-child .step-line {
    display: none;
}

.step-body {
    flex: 1;
    min-width: 0;
}

.step-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
}

.step-text {
    font-size: 13px;
    color: var(--text-secondary);
    margin: 4px 0 0 0;
    line-height: 1.6;
}

.step-image {
    margin-top: 8px;
    border-radius: 8px;
    overflow: hidden;
    max-width: 100%;
}

.step-image img {
    width: 100%;
    max-height: 180px;
    object-fit: cover;
    border-radius: 8px;
    border: 1px solid var(--border-light);
}

/* ===== ПУСТОЕ СОСТОЯНИЕ ===== */
.empty-steps {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 32px 20px;
    background: var(--bg-secondary);
    border-radius: 12px;
    border: 2px dashed var(--border-color);
    text-align: center;
}

.empty-steps i {
    font-size: 28px;
    color: var(--text-muted);
    margin-bottom: 10px;
    opacity: 0.5;
}

.empty-steps p {
    color: var(--text-muted);
    font-size: 14px;
    margin: 0;
}

/* ===== КНОПКИ ===== */
.modal-actions {
    display: flex;
    gap: 10px;
}

.modal-actions .btn {
    flex: 1;
    padding: 0.7rem 1rem;
    border-radius: 40px;
    font-weight: 600;
    font-size: 0.9rem;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.btn-secondary {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}

.btn-secondary:hover {
    background: var(--border-color);
}

/* ============================================ */
/* ===== АДАПТИВНОСТЬ ===== */
/* ============================================ */

@media (max-width: 768px) {
    .info-grid {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 640px) {
    .manual-meta {
        flex-direction: column;
        align-items: flex-start;
    }

    .manual-meta-right {
        width: 100%;
    }

    .info-grid {
        grid-template-columns: 1fr;
    }

    .step-item {
        flex-direction: column;
        gap: 8px;
    }

    .step-marker {
        flex-direction: row;
        gap: 8px;
    }

    .step-line {
        display: none !important;
    }

    .modal-actions {
        flex-direction: column;
    }

    .modal-actions .btn {
        width: 100%;
        padding: 0.8rem;
    }
}

@media (max-width: 420px) {
    .manual-description {
        font-size: 13px;
        padding: 8px 12px;
    }

    .step-title {
        font-size: 13px;
    }

    .step-text {
        font-size: 12px;
    }

    .status-badge {
        font-size: 11px;
        padding: 3px 10px;
    }

    .info-card {
        padding: 8px 12px;
    }

    .info-icon {
        width: 30px;
        height: 30px;
        font-size: 13px;
    }

    .info-value {
        font-size: 12px;
    }
}
</style>