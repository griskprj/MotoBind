<template>
    <ModalWrapper
        :isOpen="isOpen"
        title="Удаление обслуживания"
        subtitle="Вы уверены, что хотите удалить эту запись?"
        icon="trash"
        bg-icon-color="var(--danger-trans)"
        icon-color="var(--danger-text)"
        @close="$emit('close')"
    >
        <div class="modal-info-block danger">
            <div class="modal-info-icon">
                <i class="fa fa-exclamation-triangle"></i>
            </div>
            <div>
                <p class="modal-info-text" style="font-weight: 600; color: var(--danger-text);">
                    Это действие нельзя отменить!
                </p>
                <p class="modal-info-text">
                    Запись об обслуживании будет удалена безвозвратно. 
                    Все связанные данные будут потеряны.
                </p>
            </div>
        </div>

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
        maintenanceId: {
            type: Number,
            default: null
        }
    },

    methods: {
        submit() {
            this.$emit('submit', this.maintenanceId)
        }
    }
}
</script>

<style scoped>
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
    .modal-info-text {
        font-size: 13px;
    }

    .modal-actions .btn {
        font-size: 0.85rem;
        padding: 0.7rem;
    }
}
</style>