<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Удалить мотоцикл"
        @close="$emit('close')"
    >
        <p class="modal-text">Вы уверены, что хотите удалить мотоцикл? Все связанные данные безвозвратно будут удалены, отменить это действие невозможно.</p>
        <div class="modal-actions">
            <button @click="submit" class="btn-danger">Удалить</button>
            <button @click="$emit('close')" class="close-btn">Отменить</button>
        </div>
    </ModalWrapper>
</template>

<script>
import ModalWrapper from '../ModalWrapper.vue';

export default {
    components: { ModalWrapper },

    props: {
        isOpen: Boolean,
        motoId: {
            type: Number,
            default: null
        }
    },

    methods: {
        submit() {
            this.$emit('submit', this.motoId)
        },
    }
}
</script>