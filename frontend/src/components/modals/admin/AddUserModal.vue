<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Добавить пользователя"
        subtitle="Заполните информацию о новом пользователе"
        icon="user"
        bg-icon-color="var(--success-trans)"
        icon-color="var(--success-text)"
        @close="$emit('close')"
    >
        <div class="modal-form-group">
            <label>
                Имя <span class="required">*</span>
                <input 
                    v-model="form.username" 
                    type="text" 
                    placeholder="Введите имя пользователя"
                    required
                />
            </label>
        </div>

        <div class="modal-form-group">
            <label>
                Email <span class="required">*</span>
                <input 
                    v-model="form.email" 
                    type="email" 
                    placeholder="user@example.com"
                    required
                />
            </label>
        </div>

        <div class="modal-form-row">
            <div class="modal-form-group">
                <label>Роль</label>
                <select v-model="form.role">
                    <option value="motorcyclist">Мотоциклист</option>
                    <option value="club_member">Член мотоклуба</option>
                    <option value="admin">Админ</option>
                </select>
            </div>

            <div class="modal-form-group">
                <label>Статус</label>
                <select v-model="form.status">
                    <option value="active">Активен</option>
                    <option value="banned">Заблокирован</option>
                </select>
            </div>
        </div>

        <div class="modal-form-group">
            <label>
                Пароль
                <input 
                    v-model="form.password" 
                    type="password" 
                    placeholder="Оставьте пустым для генерации"
                />
            </label>
        </div>

        <div class="modal-info-block success">
            <div class="modal-info-icon">
                <i class="fa fa-info-circle"></i>
            </div>
            <p class="modal-info-text">
                Пользователь будет добавлен в систему и получит доступ ко всем функциям.
            </p>
        </div>

        <template #actions>
            <div class="modal-actions">
                <button class="btn btn-secondary" @click="$emit('close')">
                    Отменить
                </button>
                <button class="btn btn-primary" @click="$emit('submit', form)">
                    <i class="fa fa-plus"></i> Добавить
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

    watch: {
        isOpen(val) {
            if (!val) {
                this.resetForm()
            }
        }
    },

    methods: {
        resetForm() {
            this.form = {
                username: '',
                email: '',
                password: '',
                role: 'motorcyclist',
                status: 'active'
            }
        }
    }
}
</script>