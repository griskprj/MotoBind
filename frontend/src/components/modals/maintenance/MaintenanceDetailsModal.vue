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
                        'badge-green': maintenance?.status === 'ok' || maintenance?.status === 'completed',
                        'badge-warning': maintenance?.status === 'soon',
                        'badge-danger': maintenance?.status === 'overdue',
                        'badge-gray': !maintenance?.status || maintenance?.status === 'planned'
                    }"
                >
                    <span class="badge-dot"></span>
                    {{ getStatusLabel(maintenance?.status) }}
                </span>
                <span v-if="maintenance?.date" class="header-date">
                    <i class="fa fa-calendar"></i>
                    {{ formatDate(maintenance.date) }}
                </span>
            </div>

            <p v-if="maintenance?.description" class="header-subtitle">
                <i class="fa fa-message"></i>
                {{ maintenance.description }}
            </p>
        </div>

        <div class="modal-card">
            <p class="modal-card-title">
                <i class="fa fa-receipt"></i>
                Детали обслуживания
            </p>
            <div class="card-items">
                <div v-if="maintenance?.date" class="card-item">
                    <span class="item-title">
                        <i class="fa fa-calendar"></i> Дата
                    </span>
                    <span class="item-value">{{ formatDate(maintenance.date) }}</span>
                </div>

                <div v-if="maintenance?.mileage" class="card-item">
                    <span class="item-title">
                        <i class="fa fa-gauge-high"></i> Пробег выполнения
                    </span>
                    <span class="item-value">{{ maintenance.mileage }} <span class="unit">км</span></span>
                </div>
                
                <div v-if="maintenance?.planned_mileage" class="card-item">
                    <span class="item-title">
                        <i class="fa fa-clock"></i> Плановый пробег
                    </span>
                    <span class="item-value">{{ maintenance.planned_mileage }} <span class="unit">км</span></span>
                </div>
                
                <div v-if="maintenance?.cost" class="card-item">
                    <span class="item-title">
                        <i class="fa fa-ruble-sign"></i> Стоимость
                    </span>
                    <span class="item-value">{{ maintenance.cost }} <span class="unit">₽</span></span>
                </div>

                <div v-if="maintenance?.category" class="card-item">
                    <span class="item-title">
                        <i class="fa fa-tags"></i> Категория
                    </span>
                    <span class="item-value">
                        <span class="category-tag">{{ getCategory(maintenance.category) }}</span>
                    </span>
                </div>
            </div>
        </div>

        <div class="modal-actions">
            <div class="actions-wrapper">
                <button @click="openDeleteModal" class="btn-close danger"><i class="fa fa-trash"></i> Удалить</button>
                <button @click="openEditModal" class="btn-close edit" disabled><i class="fa fa-pen"></i> Редактировать</button>
            </div>
            <button @click="$emit('close')" class="btn-close">
                <i class="fa fa-xmark"></i> Закрыть
            </button>
        </div>

        <DeleteMaintenanceModal
            :isOpen="showDeleteModal"
            :maintenanceId="maintenance.id"
            :isPlanned="!maintenance.status || maintenance.status !== 'completed'"
            @submit="handleDelete"
            @close="showDeleteModal = false"
        />
    </ModalWrapper>
</template>

<script>
import ModalWrapper from '../ModalWrapper.vue';
import DeleteMaintenanceModal from './DeleteMaintenanceModal.vue';

export default {
    components: {
        ModalWrapper,
        DeleteMaintenanceModal
    },

    data() {
        return {
            showDeleteModal: false,
            showEditModal: false,
        }
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
            return labels[status] || 'Выполнено'
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
        },

        openDeleteModal() {
            this.showDeleteModal = true
        },
        handleDelete(payload) {
            this.$emit('delete', payload)
            this.showDeleteModal = false
        },

        openEditModal() {
            this.showEditModal = true
        }
    }
}
</script>

<style scoped>
/* ===== HEADER ===== */
.modal-header {
    display: flex;
    flex-direction: column;
    margin-bottom: 16px;
}

.header-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    flex-wrap: wrap;
    gap: 8px;
}

.header-subtitle {
    width: 100%;
}

.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 14px 4px 10px;
    border-radius: 50px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}

.badge-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: currentColor;
    flex-shrink: 0;
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
    background: rgba(107, 114, 128, 0.10);
    color: #9ca3af;
}

.header-date {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    color: #8b8b9e;
    background: rgba(255, 255, 255, 0.04);
    padding: 4px 12px;
    border-radius: 50px;
}

.header-date i {
    font-size: 13px;
}

.header-subtitle {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    font-size: 14px;
    color: #b0b0c8;
    margin: 0;
    line-height: 1.6;
    padding: 12px 16px;
    background: rgba(255, 255, 255, 0.02);
    border-radius: 10px;
    border-left: 3px solid rgba(124, 58, 237, 0.3);
}

.header-subtitle i {
    margin-top: 2px;
    color: #7c3aed;
    flex-shrink: 0;
}

/* ===== CARD ===== */
.modal-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 20px;
}

.modal-card-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    font-weight: 700;
    color: #6b6b84;
    margin: 0 0 14px 0;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}

.modal-card-title i {
    font-size: 14px;
    color: #7c3aed;
}

.card-items {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.card-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    background: rgba(255, 255, 255, 0.02);
    border-radius: 10px;
    transition: all 0.2s ease;
}

.card-item:hover {
    background: rgba(255, 255, 255, 0.05);
}

.item-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: #8b8b9e;
}

.item-title i {
    font-size: 14px;
    color: #7c3aed;
    width: 18px;
    text-align: center;
}

.item-value {
    display: flex;
    align-items: baseline;
    gap: 2px;
    font-size: 14px;
    font-weight: 500;
    color: #e8e8f0;
}

.unit {
    font-size: 11px;
    font-weight: 400;
    color: #6b6b84;
    margin-left: 2px;
}

.category-tag {
    display: inline-block;
    padding: 2px 14px;
    border-radius: 50px;
    font-size: 12px;
    font-weight: 500;
    background: rgba(124, 58, 237, 0.10);
    color: #a78bfa;
}

/* ===== ACTIONS ===== */
.modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 4px;
    padding-top: 16px;
    border-top: 1px solid rgba(255, 255, 255, 0.04);
}

.actions-wrapper {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
}

.btn-danger {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 18px;
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.15);
    border-radius: 10px;
    color: #ef4444;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 14px;
    font-weight: 500;
}

.btn-danger:hover {
    background: rgba(239, 68, 68, 0.15);
    border-color: rgba(239, 68, 68, 0.3);
    transform: translateY(-1px);
}

.btn-close {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 24px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
    color: #b0b0c8;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 14px;
    font-weight: 500;
}

.btn-close:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.12);
    color: #e8e8f0;
    transform: translateY(-1px);
}

.btn-close.danger {
    background-color: var(--danger-trans);
    color: var(--danger);
}

.btn-close.edit {
    background-color: var(--warning-trans);
    color: var(--warning);
}

/* ===== RESPONSIVE ===== */
@media (max-width: 480px) {
    .header-top {
        flex-direction: column;
        align-items: flex-start;
    }

    .modal-card {
        padding: 14px 16px;
    }

    .card-item {
        flex-wrap: wrap;
        gap: 4px;
    }

    .modal-actions {
        flex-direction: column-reverse;
    }

    .modal-actions button {
        justify-content: center;
        padding: 10px;
    }
}

@media (max-width: 320px) {
    .actions-wrapper {
        grid-template-columns: repeat(1, 1fr);
        grid-template-rows: repeat(2, 1fr);
    }
}
</style>