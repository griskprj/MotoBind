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
                <div
                    class="badge"
                    :class="{
                        'badge-green': maintenance?.status === 'ok',
                        'badge-warning': maintenance?.status === 'soon',
                        'badge-danger': maintenance?.status === 'overdue',
                        'badge-gray': !maintenance?.status
                    }"
                >
                    {{ getStatusLabel(maintenance?.status) }}
                </div>
                <div v-if="maintenance?.date" class="header-date">
                    {{ formatDate(maintenance.date) }}
                </div>
            </div>

            <p v-if="maintenance?.description" class="header-subtitle">
                {{ maintenance.description }}
            </p>
        </div>

        <div class="modal-card">
            <p class="modal-card-title">Детали обслуживания</p>
            <div class="card-items">
                <div v-if="maintenance?.date" class="card-item">
                    <p class="item-title"><i class="fa fa-calendar"></i> Дата</p>
                    <p class="item-value">{{ formatDate(maintenance.date) }}</p>
                </div>

                <div v-if="maintenance?.mileage" class="card-item">
                    <p class="item-title"><i class="fa fa-tachometer"></i> Пробег выполнения</p>
                    <p class="item-value">{{ maintenance.mileage }} км</p>
                </div>
                
                <div v-if="maintenance?.planned_mileage" class="card-item">
                    <p class="item-title"><i class="fa fa-tachometer"></i> Плановый пробег</p>
                    <p class="item-value">{{ maintenance.planned_mileage }} км</p>
                </div>
                
                <div v-if="maintenance?.cost" class="card-item">
                    <p class="item-title"><i class="fa fa-ruble"></i> Стоимость</p>
                    <p class="item-value">{{ maintenance.cost }} ₽</p>
                </div>

                <div v-if="maintenance?.category" class="card-item">
                    <p class="item-title"><i class="fa fa-tags"></i> Категория</p>
                    <p class="item-value">{{ getCategory(maintenance.category) }}</p>
                </div>
            </div>
        </div>

        <div class="modal-actions">
            <button @click="$emit('close')" class="cancel-btn">Закрыть</button>
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
            } catch (error) {
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

        getCategory(category){
            const categories = {
                'engine': 'Двигатель',
                'drive': 'Привод',
                'steering': 'Рулевое управление',
                'suspension' : 'Подвеска',
                'electronics': 'Электроника',
                'wheel': 'Колеса/Шины',
                'brakes': 'Тормозная система',
                'fuel': 'Топливная система',
                'cooling': 'Система охлаждения',
            }
            return categories[category]
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
    margin-bottom: 12px;
    flex-wrap: wrap;
    gap: 8px;
}

.badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
}

.badge-green {
    background: rgba(34, 197, 94, 0.15);
    color: #4ade80;
}

.badge-warning {
    background: rgba(251, 191, 36, 0.15);
    color: #fbbf24;
}

.badge-danger {
    background: rgba(239, 68, 68, 0.15);
    color: #ef4444;
}

.badge-gray {
    background: rgba(107, 114, 128, 0.15);
    color: #9ca3af;
}

.header-date {
    font-size: 14px;
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
    padding: 16px;
    margin-bottom: 16px;
}

.modal-card-title {
    font-size: 14px;
    font-weight: 600;
    color: #8b8b9e;
    margin: 0 0 12px 0;
}

.card-items {
    width: 256px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.card-item {
    display: flex;
    justify-content: space-between;
    background: #181824;
    padding: 12px;
    border-radius: 10px;
}

.card-item.full-width {
    grid-column: 1 / -1;
}

.item-title {
    font-size: 12px;
    color: var(--accent);
    margin: 0 0 4px 0;
}

.item-title i {
    margin-right: 4px;
}

.item-value {
    font-size: 16px;
    font-weight: 600;
    margin: 0;
}

.item-value i {
    margin-right: 4px;
    color: #a78bfa;
}

.modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 8px;
}

.cancel-btn {
    padding: 10px 24px;
    background: transparent;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    color: #e0e0e0;
    cursor: pointer;
    transition: 0.2s;
    font-size: 14px;
}

.cancel-btn:hover {
    background: rgba(255,255,255,0.05);
}

@media (max-width: 480px) {
    .card-items {
        grid-template-columns: 1fr;
    }
}
</style>