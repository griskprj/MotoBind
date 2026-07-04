<template>
    <ModalWrapper
        :isOpen="isOpen"
        title="Создать базовое обслуживание"
        @close="$emit('close')"
    >
        <p class="modal-text">Запланировать автоматически базовое обслуживание?</p>
        <p class="modal-subtitle">Система автоматически запланирует базовое обслуживание вашего мотоцикла на основе введенного вами пробега для каждого из обслуживаний. Вы можете сделать это вручную через кнопку "Запланировать обслуживание".</p>

        <div class="modal-actions">
            <button @click="submit" class="accept-btn">Создать</button>
            <button @click="$emit('close')">Отменить</button>
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
        motoId: {
            type: Number,
            default: null
        }
    },

    methods: {
        submit() {
            this.$emit('submit', this.motoId)
        }
    }
}
</script>