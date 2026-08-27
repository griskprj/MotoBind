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
        <div class="moto-info-card">
            <img
                v-if="motorcycle.photo_url"
                :src="getPhotoUrl(motorcycle.photo_url)"
                alt="Фото"
                class="moto-thumb"
            />
            <div class="moto-placeholder" v-else>
                <i class="fa fa-motorcycle"></i>
            </div>
            <div class="moto-info">
                <div class="moto-name">{{ motorcycle.name }}</div>
                <div class="moto-meta">
                    <span>{{ motorcycle.years || '—' }}</span>
                    <span>•</span>
                    <span>{{ motorcycle.mileage || 0 }} км</span>
                    <span>•</span>
                    <span>Владелец: {{ motorcycle.owner?.username || '—' }}</span>
                </div>
            </div>
        </div>

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
                    обслуживание, фотографии и статистика.
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
        motorcycle: {
            type: Object,
            default: null
        }
    },

    methods: {
        getPhotoUrl(photoPath) {
            if (!photoPath) return null
            if (photoPath.startsWith('http')) return photoPath
            const baseUrl = import.meta.env.VITE_API_URL || ''
            return `${baseUrl}/uploads/${photoPath}`
        },

        submit() {
            this.$emit('submit', this.motorcycle.id)
        }
    }
}
</script>

<style scoped>
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

.moto-thumb {
    width: 48px;
    height: 48px;
    border-radius: 8px;
    object-fit: cover;
    flex-shrink: 0;
}

.moto-placeholder {
    width: 48px;
    height: 48px;
    border-radius: 8px;
    background: var(--bg-card);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    flex-shrink: 0;
    font-size: 20px;
}

.moto-info {
    flex: 1;
    min-width: 0;
}

.moto-name {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
}

.moto-meta {
    font-size: 13px;
    color: var(--text-muted);
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
}

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

@media (max-width: 640px) {
    .moto-info-card {
        flex-direction: column;
        text-align: center;
    }

    .modal-actions {
        flex-direction: column;
    }

    .modal-actions .btn {
        width: 100%;
    }

    .modal-info-block {
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
}
</style>