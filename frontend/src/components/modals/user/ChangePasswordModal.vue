<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Смена пароля"
        subtitle="Для безопасности используйте надежный пароль"
        icon="lock"
        @close="$emit('close')"
    >
        <div class="inputs-group">
            <label>
                Текущий пароль
                <input v-model="form.currentPassword" type="password" required>
            </label>

            <label>
                Новый пароль
                <input v-model="form.newPassword" type="password" required>
            </label>
            <label>
                Повторите новый пароль
                <input v-model="form.repeatPassword" type="password" required>
            </label>
        </div>

        <div class="modal-actions">
            <button @click="$emit('close')" class="outline-btn">Отменить</button>
            <button @click="$emit('submit', this.form)"><i class="fa fa-lock"></i> Изменить пароль</button>
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
            required: true,
            default: false
        }
    },

    data() {
        return {
            form: {
                currentPassword: null,
                newPassword: null,
                repeatPassword: null
            }
        }
    },

    methods: {
        submit() {
            if (newPassword !== repeatPassword) {
                alert('Пароли не совпадают')
                return
            }

            this.resetForm()
        },

        resetForm() {
            form = {
                currentPassword: null,
                newPassword: null,
                repeatPassword: null
            }
        }
    }
}
</script>

<style scoped>
.modal-actions {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(1, 1fr);
    gap: 8px;
}
.modal-actions button {
    width: 100%;
}
</style>