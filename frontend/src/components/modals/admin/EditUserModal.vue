<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Редактирование пользователя"
        subtitle="Отредактируйте данные пользователя"
        icon="pen"
        @close="$emit('close')"
    >
        <div v-if="user" class="user-card">
            <img :src="getAvatarUrl(user.avatar)" alt="" class="user-img">

            <div class="user-card-body">
                <div class="user-top">
                    <p class="user-name">{{ user.username }}</p>
                    <p class="user-id">ID: {{ user.id }}</p>
                </div>
                <div class="user-bottom">
                    <p class="user-date">Пользователь с {{ formatDate(user.created_at) }}</p>
                </div>
            </div>
        </div>

        <div class="input-groups">
            <div class="inputs-wrapper">
                <label>
                    Имя пользователя
                    <input v-model="form.username" type="text">
                </label>
                <label>
                    Email
                    <input v-model="form.email" type="email">
                </label>
            </div>
            
            <div class="inputs-wrapper">
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
                        <option value="banned">Заблокирован</option>
                    </select>
                </label>
            </div>
        </div>

        <div class="info-block">
            <div class="block-icon">
                <i class="fa fa-info"></i>
            </div>
            <p class="block-text">
                Данные пользователя будут обновлены.
            </p>
        </div>

        <div class="modal-actions">
            <button @click="$emit('close')" class="cancel-btn">Отменить</button>
            <button @click="$emit('submit', this.form)"><i class="fa fa-check"></i> Сохранить изменения</button>
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
        },

        user: {
            type: Object,
            required: true,
            default: null
        }
    },

    data() {
        return {
            form: {
                id: null,
                username: null,
                email: null,
                role: null,
                status: null
            }
        }
    },

    watch: {
        isOpen(newVal) {
            if (newVal && this.user) {
                this.form = {
                    id: this.user.id,
                    username: this.user.username,
                    email: this.user.email,
                    role: this.user.role,
                    status: this.user.status
                }
            }
        },

        user: {
            handler(newVal) {
                if (this.isOpen && newVal) {
                    this.form = {
                        id: newVal.id,
                        username: newVal.username,
                        email: newVal.email,
                        role: newVal.role,
                        status: newVal.status
                    }
                }
            },
            deep: true
        }
    },

    methods: {
        resetForm() {
            this.form = {
                id: null,
                username: null,
                email: null,
                role: null,
                status: null
            }
        },

        submit(id) {
            this.$emit('submit', this.form)
            this.resetForm()
        },

        formatDate(dateString) {
            if (!dateString) return '--'
            
            try {
                if (dateString instanceof Date) {
                    return dateString.toLocaleDateString('ru-RU', {
                        day: '2-digit',
                        month: 'short',
                        year: 'numeric'
                    })
                }
                
                const date = new Date(dateString)
                
                if (isNaN(date.getTime())) {
                    return '--'
                }
                
                return date.toLocaleDateString('ru-RU', {
                    day: '2-digit',
                    month: 'short',
                    year: 'numeric'
                })
            } catch (error) {
                console.error('Error formatting date:', dateString, error)
                return '--'
            }
        },
        getAvatarUrl(avatarPath) {
            if (!avatarPath || typeof avatarPath !== 'string') {
                return '/BaseAvatar.jpg';
            }
            if (avatarPath.startsWith('http')) {
                return avatarPath;
            }
            return `/uploads/${avatarPath}`;
        }
    }
}
</script>

<style scoped>
.inputs-group {
    display: grid;
    grid-template-columns: repeat(1, 1fr);
    grid-template-rows: repeat(3, 1fr);
    gap: 8px;
}

.inputs-wrapper {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(1, 1fr);
    gap: 8px;
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

.user-card {
    padding: 14px 16px;
    display: flex;
    align-items: center;
    gap: 14px;
}

.user-top {
    display: flex;
    align-items: center;
    gap: 12px;
}

.user-name {
    font-weight: 600;
    font-size: 18px;
}

.user-id {
    padding: 2px 10px;
    font-size: 14px;
    font-weight: 600;
    background-color: var(--accent-trans);
    color: var(--accent);
    border-radius: 8px;
}

.user-date {
    font-size: 14px;
    color: var(--text-muted);
}

.user-img {
    width: 52px;
    height: 52px;
    border-radius: 50%;
}

.info-block {
    display: flex;
    align-items: center;
    padding: 12px;
    background-color: var(--accent-trans);
    border-radius: 10px;
    border: 1px solid var(--accent-light);
}

.block-icon {
    color: var(--accent);
    font-size: 24px;
    margin-right: 12px;
}

.block-text {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 0;
}
</style>