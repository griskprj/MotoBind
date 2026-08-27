<template>
    <ModalWrapper
        v-if="motorcycle"
        :isOpen="isOpen"
        title="Удалить мотоцикл"
        subtitle="Вы уверены, что хотите удалить этот мотоцикл?"
        icon="trash"
        bg-icon-color="var(--danger-trans)"
        icon-color="var(--danger-text)"
        @close="$emit('close')"
    >
        <!-- Информация о мотоцикле -->
        <div class="moto-info-card">
            <div class="moto-info-icon">
                <i class="fa fa-motorcycle"></i>
            </div>
            <div class="moto-info-content">
                <div class="moto-info-name">{{ motorcycle.name || '—' }}</div>
                <div class="moto-info-meta">
                    <span v-if="motorcycle.years">{{ motorcycle.years }}</span>
                    <span v-if="motorcycle.years && motorcycle.mileage !== undefined">•</span>
                    <span v-if="motorcycle.mileage !== undefined">{{ motorcycle.mileage }} км</span>
                    <span v-if="!motorcycle.years && motorcycle.mileage === undefined">Нет данных</span>
                </div>
            </div>
        </div>

        <!-- Предупреждение -->
        <div class="modal-info-block danger">
            <div class="modal-info-icon">
                <i class="fa fa-exclamation-triangle"></i>
            </div>
            <div>
                <p class="modal-info-text" style="font-weight: 600; color: var(--danger-text);">
                    Это действие нельзя отменить!
                </p>
                <p class="modal-info-text">
                    Будут удалены все данные, связанные с этим мотоциклом:
                    обслуживание, файлы, статистика и история.
                </p>
            </div>
        </div>

        <!-- Действия -->
        <template #actions>
            <div class="modal-actions">
                <button class="btn btn-secondary" @click="$emit('close')">
                    Отменить
                </button>
                <button class="btn btn-danger" @click="submit">
                    <i class="fa fa-trash"></i> Удалить
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
            default: false
        },
        motorcycle: {
            type: Object,
            default: null
        }
    },

    methods: {
        submit() {
            this.$emit('submit', this.motorcycle.id)
        }
    }
}
</script>

<style scoped>
/* ===== ИНФО О МОТОЦИКЛЕ ===== */
.moto-info-card {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 14px 16px;
    background: var(--bg-secondary);
    border-radius: 12px;
    border: 1px solid var(--border-light);
    margin-bottom: 16px;
}

.moto-info-icon {
    width: 44px;
    height: 44px;
    min-width: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background: var(--accent-trans);
    color: var(--accent-text);
    font-size: 20px;
}

.moto-info-content {
    flex: 1;
    min-width: 0;
}

.moto-info-name {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 2px;
}

.moto-info-meta {
    font-size: 13px;
    color: var(--text-muted);
}

.moto-info-meta span {
    margin: 0 2px;
}

/* ===== ИНФО-БЛОК ===== */
.modal-info-block {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 14px 16px;
    border-radius: 10px;
}

.modal-info-block.danger {
    background: var(--danger-trans);
    border: 1px solid rgba(239, 68, 68, 0.2);
}

.modal-info-icon {
    font-size: 20px;
    color: var(--danger-text);
    flex-shrink: 0;
    margin-top: 2px;
}

.modal-info-text {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.5;
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
    .moto-info-card {
        flex-direction: column;
        text-align: center;
        padding: 16px;
    }

    .moto-info-icon {
        width: 48px;
        height: 48px;
        min-width: 48px;
        font-size: 22px;
    }

    .modal-actions {
        flex-direction: column;
    }

    .modal-actions .btn {
        width: 100%;
        padding: 0.8rem;
    }

    .modal-info-block {
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .modal-info-icon {
        margin-top: 0;
    }
}

@media (max-width: 400px) {
    .moto-info-name {
        font-size: 14px;
    }

    .moto-info-meta {
        font-size: 12px;
    }

    .modal-info-text {
        font-size: 13px;
    }

    .modal-actions .btn {
        font-size: 0.85rem;
        padding: 0.7rem;
    }
}
</style>