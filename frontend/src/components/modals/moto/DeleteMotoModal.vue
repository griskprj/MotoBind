<template>
    <ModalWrapper
        v-if="motorcycle"
        :is-open="isOpen"
        title="Удалить мотоцикл"
        @close="$emit('close')"
        icon="trash"
        iconColor="var(--danger)"
        bgIconColor="var(--danger-trans)"
        subtitle="Вы уверены, что хотите удалить мотоцикл?"
    >
        <div class="moto-card">
            <div class="card-icon">
                <i class="fa fa-motorcycle"></i>
            </div>
            <div class="card-body">
                <p class="card-title">{{ motorcycle.name || '--' }}</p>
                <span class="card-subtitle">{{ motorcycle.years }}</span> • <span class="card-subtitle">{{  motorcycle.mileage }} км</span>
            </div>
        </div>
        <div class="danger-block">
            <div class="block-icon">
                <i class="fa fa-exclamation-triangle"></i>
            </div>
            <div class="block-wrappper">
                <p class="block-title">Это действие нельзя отменить</p>
                <p class="block-text">
                    Будут удалены все данные, связанные с этим мотоциклом: обслуживания, файлы и статистика.
                </p>
            </div>
        </div>
        <div class="modal-actions">
            <button @click="$emit('close')" class="outline-btn">Отменить</button>
            <button @click="submit" class="btn-danger"><i class="fa fa-trash"></i> Удалить</button>
        </div>
    </ModalWrapper>
</template>

<script>
import ModalWrapper from '../ModalWrapper.vue';

export default {
    components: { ModalWrapper },

    props: {
        isOpen: Boolean,
        motorcycle: {
            type: Object,
            default: null
        }
    },

    methods: {
        submit() {
            this.$emit('submit', this.motorcycle.id)
        },
    }
}
</script>

<style scoped>
.moto-card {
    display: flex;
    flex-direction: row;
    gap: 16px;
    padding: 12px;
    border-radius: 14px;
    align-items: center;

    background-color: var(--bg-card);
}

.card-icon {
    height: 48px;
    width: 48px;
    text-align: center;
    border-radius: 10px;

    padding: 8px;
    background-color: var(--accent-trans);
}

.card-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 8px;
}

.card-subtitle {
    font-size: 14px;
    color: var(--text-secondary);
    font-weight: 400;
}

.danger-block {
    display: flex;
    padding: 12px;
    background-color: var(--danger-trans);
    border-radius: 10px;
    border: 1px solid var(--danger);
}

.block-icon {
    color: var(--danger);
    font-size: 24px;
    margin-right: 8px;
}

.block-title {
    color: var(--danger);
    font-weight: 600;
    margin-bottom: 4px;
}

.block-text {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 0;
}

.modal-actions {
    flex-direction: row;
}

.modal-actions button {
    width: 100%;
}
</style>