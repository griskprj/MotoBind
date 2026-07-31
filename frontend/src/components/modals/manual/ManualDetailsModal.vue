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

        <div class="modal-actions">
            <button @click="$emit('close')" class="btn-close">Закрыть</button>
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

    emits: ['close'],

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
    }
}
</script>

<style scoped>
/* Контейнер с прокруткой */
.modal-scroll {
    max-height: 60vh;
    overflow-y: auto;
    padding-right: 4px;
}

/* Стилизация скроллбара */
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

/* Firefox */
.modal-scroll {
    scrollbar-width: thin;
    scrollbar-color: #7c3aed rgba(255, 255, 255, 0.03);
}

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

.badge-green {
    background: rgba(74, 222, 128, 0.12);
    color: #4ade80;
}

.badge-warning {
    background: rgba(251, 191, 36, 0.12);
    color: #fbbf24;
}

.badge-danger {
    background: rgba(239, 68, 68, 0.12);
    color: #ef4444;
}

.badge-gray {
    background: rgba(107, 114, 128, 0.12);
    color: #9ca3af;
}

.header-date {
    font-size: 13px;
    color: #8b8b9e;
}

.header-date i {
    margin-right: 4px;
}

.header-subtitle {
    font-size: 14px;
    color: #8b8b9e;
    margin: 0;
    line-height: 1.5;
}

.modal-card {
    background: #0f0f1a;
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 12px;
}

.steps-card {
    margin-bottom: 16px;
}

.modal-card-title {
    font-size: 13px;
    font-weight: 600;
    color: #8b8b9e;
    margin: 0 0 14px 0;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}

.modal-card-title i {
    margin-right: 6px;
}

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

.card-item:hover {
    background: #1e1e2e;
}

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

/* Steps */
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

.step-item:hover {
    background: #1e1e2e;
}

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

.step-content {
    flex: 1;
    min-width: 0;
}

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

/* Actions */
.modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.btn-close {
    padding: 8px 24px;
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

.btn-edit {
    padding: 8px 24px;
    background: #7c3aed;
    border: none;
    border-radius: 8px;
    color: #fff;
    cursor: pointer;
    transition: 0.2s;
    font-size: 14px;
}

.btn-edit:hover {
    background: #6d28d9;
}

.btn-edit i {
    margin-right: 6px;
}

/* Responsive */
@media (max-width: 480px) {
    .modal-scroll {
        max-height: 50vh;
    }

    .header-top {
        flex-direction: column;
        align-items: flex-start;
    }

    .card-item {
        flex-direction: column;
        align-items: flex-start;
        gap: 4px;
    }

    .item-value {
        text-align: left;
        max-width: 100%;
    }

    .step-item {
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
    }

    .modal-actions {
        flex-direction: column;
    }

    .btn-close,
    .btn-edit {
        width: 100%;
        text-align: center;
    }
}
</style>