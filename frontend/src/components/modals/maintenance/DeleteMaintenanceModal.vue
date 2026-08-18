<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Удаление обслуживания"
        icon="trash"
        icon-color="var(--danger)"
        bg-icon-color="var(--danger-trans)"
        @close="$emit('close')"
    >
        <p class="modal-text">
            Вы уверены, что хотите удалить запись об обслуживании?
            Отменить это действие невозможно.
        </p>
        <div class="modal-actions">
            <button @click="submit" class="btn-danger">Удалить</button>
            <button @click="$emit('close')" class="cancel-btn">Отменить</button>
        </div>
    </ModalWrapper>
</template>

<script>
import ModalWrapper from '../ModalWrapper.vue';

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