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
                username: '',
                email: '',
                password: '',
                role: 'motorcyclist',
                status: 'active'
            }
        }
    },
}
</script>

<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Добавить пользователя"
        subtitle="Добавьте пользователя в систему."
        icon="user"
        bg-icon-color="var(--success-trans)"
        icon-color="var(--success)"
        @close="this.$emit('close')"
    >
        <div class="modal-group">
            <div class="inputs-group">
                <div class="inputs-wrapper">
                    <label>
                        Имя пользователя *
                        <input v-model="form.username" type="text" required>
                    </label>
                    <label>
                        Email *
                        <input v-model="form.email" type="email" required>
                    </label>
                </div>
            </div>

            <div class="inputs-group">
                <label>
                    Роль
                    <select v-model="form.role">
                        <option value="motorcyclist">Мотоциклист</option>
                        <option value="clubMember">Член мотоклуба</option>
                        <option value="admin">Админ</option>
                    </select>
                </label>

                <label>
                    Статус
                    <select v-model="form.status">
                        <option value="active">Активен</option>
                        <option value="ban">Заблокирован</option>
                    </select>
                </label>
            </div>

            <label>
                Пароль
                <input type="password">
            </label>
        </div>

        <div class="info-block">
            <div class="block-icon">
                <i class="fa fa-info"></i>
            </div>
            <p class="block-text">
                Пользователь будет добавлен в систему.
            </p>
        </div>

        <div class="modal-actions">
            <button @click="$emit('close')" class="cancel-btn">Отменить</button>
            <button @click="$emit('submit', this.form)" class="accept-btn"><i class="fa fa-plus"></i> Добавить</button>
        </div>
    </ModalWrapper>
</template>

<style scoped>
.inputs-group {
    display: grid;
    grid-template-columns: repeat(1, 1fr);
    grid-template-rows: repeat(1, 1fr);
    gap: 8px;
}

.inputs-wrapper {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(1, 1fr);
    gap: 8px;
}

.info-block {
    display: flex;
    align-items: center;
    padding: 12px;
    background-color: var(--success-trans);
    border-radius: 10px;
    border: 1px solid var(--success-light);
}

.block-icon {
    color: var(--success);
    font-size: 24px;
    margin-right: 12px;
}

.block-text {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 0;
}

.modal-actions {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(1, 1fr);
    gap: 8px;
}

.modal-actions button {
    font-weight: 600;
}
</style>