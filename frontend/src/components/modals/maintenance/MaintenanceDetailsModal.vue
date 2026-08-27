<template>
    <ModalWrapper
        :isOpen="isOpen"
        :title="maintenance?.title || 'Детали обслуживания'"
        :subtitle="motoName"
        icon="wrench"
        bg-icon-color="var(--accent-trans)"
        icon-color="var(--accent-text)"
        size="md"
        @close="$emit('close')"
    >
        <!-- Статус и дата -->
        <div class="maintenance-meta">
            <span
                class="status-badge"
                :class="{
                    'status-completed': maintenance?.status === 'completed',
                    'status-planned': maintenance?.status === 'planned',
                    'status-overdue': maintenance?.status === 'overdue'
                }"
            >
                <span class="status-dot"></span>
                {{ getStatusLabel(maintenance?.status) }}
            </span>
            <span v-if="maintenance?.completed_date || maintenance?.planned_date" class="meta-date">
                <i class="fa fa-calendar"></i>
                {{ formatDate(maintenance.completed_date || maintenance.planned_date) }}
            </span>
        </div>

        <!-- Описание -->
        <p v-if="maintenance?.description" class="maintenance-description">
            <i class="fa fa-message"></i>
            {{ maintenance.description }}
        </p>

        <!-- Детали -->
        <div class="details-card">
            <div class="details-title">
                <i class="fa fa-receipt"></i>
                Детали обслуживания
            </div>
            <div class="details-list">
                <div v-if="maintenance?.completed_date || maintenance?.planned_date" class="detail-item">
                    <span class="detail-label">
                        <i class="fa fa-calendar"></i> Дата
                    </span>
                    <span class="detail-value">{{ formatDate(maintenance.completed_date || maintenance.planned_date) }}</span>
                </div>

                <div v-if="maintenance?.completed_mileage" class="detail-item">
                    <span class="detail-label">
                        <i class="fa fa-gauge-high"></i> Пробег выполнения
                    </span>
                    <span class="detail-value">{{ maintenance.completed_mileage }} <span class="unit">км</span></span>
                </div>
                
                <div v-if="maintenance?.planned_mileage" class="detail-item">
                    <span class="detail-label">
                        <i class="fa fa-clock"></i> Плановый пробег
                    </span>
                    <span class="detail-value">{{ maintenance.planned_mileage }} <span class="unit">км</span></span>
                </div>
                
                <div v-if="maintenance?.cost" class="detail-item">
                    <span class="detail-label">
                        <i class="fa fa-ruble-sign"></i> Стоимость
                    </span>
                    <span class="detail-value">{{ maintenance.cost }} <span class="unit">₽</span></span>
                </div>

                <div v-if="maintenance?.category" class="detail-item">
                    <span class="detail-label">
                        <i class="fa fa-tags"></i> Категория
                    </span>
                    <span class="detail-value">
                        <span class="category-tag">{{ getCategory(maintenance.category) }}</span>
                    </span>
                </div>
            </div>
        </div>

        <!-- Действия -->
        <template #actions>
            <div class="modal-actions">
                <button class="btn btn-secondary" @click="$emit('close')">
                    <i class="fa fa-times"></i> Закрыть
                </button>
                <button class="btn btn-danger" @click="openDeleteModal">
                    <i class="fa fa-trash"></i> Удалить
                </button>
            </div>
        </template>

        <!-- Модалка подтверждения удаления -->
        <DeleteMaintenanceModal
            :isOpen="showDeleteModal"
            :maintenanceId="maintenance?.id"
            @submit="handleDelete"
            @close="showDeleteModal = false"
        />
    </ModalWrapper>
</template>

<script>
import ModalWrapper from '../ModalWrapper.vue'
import DeleteMaintenanceModal from './DeleteMaintenanceModal.vue'

export default {
    components: {
        ModalWrapper,
        DeleteMaintenanceModal
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

    data() {
        return {
            showDeleteModal: false
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
                'completed': 'Выполнено',
                'planned': 'Запланировано',
                'overdue': 'Просрочено'
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
                'cooling': 'Система охлаждения'
            }
            return categories[category] || category
        },

        openDeleteModal() {
            this.showDeleteModal = true
        },

        handleDelete(id) {
            this.$emit('delete', id)
            this.showDeleteModal = false
        }
    }
}
</script>

<style scoped>
/* ===== СТАТУС И МЕТА ===== */
.maintenance-meta {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 12px;
}

.status-badge {
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

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: currentColor;
    flex-shrink: 0;
}

.status-completed {
    background: var(--success-trans);
    color: var(--success-text);
}

.status-planned {
    background: var(--warning-trans);
    color: var(--warning-text);
}

.status-overdue {
    background: var(--danger-trans);
    color: var(--danger-text);
}

.meta-date {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    color: var(--text-muted);
    padding: 4px 12px;
    background: var(--bg-secondary);
    border-radius: 50px;
}

.meta-date i {
    font-size: 13px;
}

/* ===== ОПИСАНИЕ ===== */
.maintenance-description {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0 0 16px 0;
    line-height: 1.6;
    padding: 12px 16px;
    background: var(--bg-secondary);
    border-radius: 10px;
    border-left: 3px solid var(--accent);
}

.maintenance-description i {
    margin-top: 2px;
    color: var(--accent-text);
    flex-shrink: 0;
}

/* ===== ДЕТАЛИ ===== */
.details-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: 12px;
    padding: 16px 18px;
}

.details-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    font-weight: 700;
    color: var(--text-muted);
    margin-bottom: 12px;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}

.details-title i {
    font-size: 14px;
    color: var(--accent-text);
}

.details-list {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.detail-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    padding: 8px 12px;
    background: var(--bg-card);
    border-radius: 8px;
    transition: background 0.2s;
}

.detail-item:hover {
    background: var(--bg-card-hover);
}

.detail-label {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: var(--text-muted);
}

.detail-label i {
    font-size: 14px;
    color: var(--accent-text);
    width: 18px;
    text-align: center;
}

.detail-value {
    display: flex;
    align-items: baseline;
    gap: 2px;
    font-size: 14px;
    font-weight: 500;
    color: var(--text-primary);
}

.unit {
    font-size: 11px;
    font-weight: 400;
    color: var(--text-muted);
    margin-left: 2px;
}

.category-tag {
    display: inline-block;
    padding: 2px 12px;
    border-radius: 50px;
    font-size: 12px;
    font-weight: 500;
    background: var(--accent-trans);
    color: var(--accent-text);
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

.btn-danger {
    background: var(--danger);
    color: #fff;
}

.btn-danger:hover {
    background: var(--danger-hover);
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(239, 68, 68, 0.3);
}

/* ============================================ */
/* ===== АДАПТИВНОСТЬ ===== */
/* ============================================ */

@media (max-width: 640px) {
    .maintenance-meta {
        flex-direction: column;
        align-items: flex-start;
    }

    .detail-item {
        flex-wrap: wrap;
        gap: 4px;
    }

    .detail-value {
        width: 100%;
        padding-left: 26px;
    }

    .modal-actions {
        flex-direction: column-reverse;
    }

    .modal-actions .btn {
        width: 100%;
        padding: 0.8rem;
    }

    .maintenance-description {
        font-size: 13px;
        padding: 10px 14px;
    }
}

@media (max-width: 400px) {
    .details-card {
        padding: 12px 14px;
    }

    .detail-item {
        padding: 6px 10px;
    }

    .detail-label {
        font-size: 12px;
    }

    .detail-value {
        font-size: 13px;
    }

    .status-badge {
        font-size: 11px;
        padding: 3px 10px 3px 8px;
    }

    .meta-date {
        font-size: 12px;
        padding: 3px 10px;
    }
}
</style>