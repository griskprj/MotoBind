<template>
    <ModalWrapper
        :isOpen="isOpen"
        :title="maintenance?.title || 'Детали обслуживания'"
        :subtitle="motoName"
        icon="wrench"
        @close="$emit('close')"
    >
        <div class="modal-header">
            <div class="header-top">
                <span
                    class="badge"
                    :class="{
                        'badge-green': maintenance?.status === 'ok',
                        'badge-warning': maintenance?.status === 'soon',
                        'badge-danger': maintenance?.status === 'overdue',
                        'badge-gray': !maintenance?.status || maintenance?.status === 'planned'
                    }"
                >
                    {{ getStatusLabel(maintenance?.status) }}
                </span>
                <span v-if="maintenance?.date" class="header-date">
                    {{ formatDate(maintenance.date) }}
                </span>
            </div>

            <p v-if="maintenance?.description" class="header-subtitle">
                {{ maintenance.description }}
            </p>
        </div>

        <div class="modal-card">
            <p class="modal-card-title">Детали обслуживания</p>
            <div class="card-items">
                <div v-if="maintenance?.date" class="card-item">
                    <span class="item-title">
                        <i class="fa fa-calendar"></i> Дата
                    </span>
                    <span class="item-value">{{ formatDate(maintenance.date) }}</span>
                </div>

                <div v-if="maintenance?.mileage" class="card-item">
                    <span class="item-title">
                        <i class="fa fa-tachometer"></i> Пробег выполнения
                    </span>
                    <span class="item-value">{{ maintenance.mileage }} км</span>
                </div>
                
                <div v-if="maintenance?.planned_mileage" class="card-item">
                    <span class="item-title">
                        <i class="fa fa-tachometer"></i> Плановый пробег
                    </span>
                    <span class="item-value">{{ maintenance.planned_mileage }} км</span>
                </div>
                
                <div v-if="maintenance?.cost" class="card-item">
                    <span class="item-title">
                        <i class="fa fa-ruble"></i> Стоимость
                    </span>
                    <span class="item-value">{{ maintenance.cost }} ₽</span>
                </div>

                <div v-if="maintenance?.category" class="card-item">
                    <span class="item-title">
                        <i class="fa fa-tags"></i> Категория
                    </span>
                    <span class="item-value">{{ getCategory(maintenance.category) }}</span>
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
        motoName: {
            type: String,
            required: true,
            default: 'Мотоцикл'
        },
        maintenance: {
            type: Object,
            required: true,
            default: null
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
                'ok': 'Выполнено',
                'soon': 'Скоро',
                'overdue': 'Просрочено',
                'planned': 'Запланировано'
            }
            return labels[status] || '—'
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
                'cooling': 'Система охлаждения',
            }
            return categories[category] || category
        }
    }
}
</script>

<style scoped>
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
}

.modal-actions {
    display: flex;
    justify-content: flex-end;
    margin-top: 4px;
}

.btn-close {
    padding: 8px 28px;
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
</style>