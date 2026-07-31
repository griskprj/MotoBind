<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Удаление аккаунта"
        subtitle="Это действие нельзя отменить. Все ваши данные, мотоциклы, записи об обслуживании и активность будут безвозвратно удалены"
        icon="lock"
        bg-icon-color="var(--danger-trans)"
        icon-color="var(--danger)"
        @close="$emit('close')"
    >
        <div class="danger-input">
            <label>
                Введите пароль для подтверждения
                <input v-model="password" type="password" required>
            </label>
        </div>

        <div class="modal-actions">
            <button class="outline-btn" @click="$emit('close')">Отменить</button>
            <button class="btn-danger" @click="$emit('submit', this.password)"><i class="fa fa-user-time"></i> Удалить аккаунт</button>
        </div>
    </ModalWrapper>
</template>

<script>
import ModalWrapper from '../ModalWrapper.vue';

export default {
    components: { ModalWrapper },

    data() {
        return {
            password: null
        }
    },
}
</script>

<style scoped>
.danger-input {
    padding: 10px 12px;
    background-color: var(--danger-trans);
    border: 2px solid var(--danger);
    border-radius: 10px;
}

label {
    color: var(--text-secondary);
}

input {
    background-color: rgba(0, 0, 0, 0.4);
}
input:focus {
    border-color: var(--danger);
    box-shadow: 0 0 0 3px var(--danger-trans);
}

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