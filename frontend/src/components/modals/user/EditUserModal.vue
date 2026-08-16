<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Редактирование профиля"
        subtitle="Измените информацию о себе. Эти данные будут видны пользователям."
        icon="pen"
        @close="$emit('close')"
    >   
        <div class="inputs-group">
            <div class="profile-avatar-wrapper">
                <img :src="getAvatarUrl(user.avatar)" alt="" class="profile-avatar">
            </div>
            <label>
                Имя
                <input type="text" v-model="form.username">
            </label>
            <label>
                Email
                <input type="email" v-model="form.email">
            </label>
            <label>
                О себе
                <input type="text" v-model="form.bio">
            </label>
        </div>

        <div class="modal-actions">
            <button @click="$emit('close')" class="outline-btn">Отменить</button>
            <button @click="submit"><i class="fa fa-check"></i> Сохранить изменения</button>
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
            default: false,
            required: true
        },

        user: {
            type: Object,
            default: null,
            required: true
        }
    },

    data() {
        return {
            form: {
                username: null,
                email: null,
                bio: null
            }
        }
    },

    watch: {
        isOpen(newVal) {
            if (newVal && this.user) {
                this.form = {
                    username: this.user.username,
                    email: this.user.email,
                    bio: this.user.bio
                }
            }
        },

        user: {
            handler(newVal) {
                if (this.isOpen && newVal) {
                    this.form = {
                        username: newVal.username,
                        email: newVal.email,
                        bio: newVal.bio
                    }
                }
            },
            deep: true
        }
    },

    methods: {
        resetForm() {
            form = {
                username: null,
                email: null,
                bio: null
            }
        },

        submit() {
            this.$emit('submit', this.form)
            this.resetForm()
        },

        getAvatarUrl(avatarPath) {
            if (!avatarPath || typeof avatarPath !== 'string') {
                return '/BaseAvatar.jpg';
            }
            if (avatarPath.startsWith('http')) {
                return avatarPath;
            }
            const baseUrl = import.meta.env.VITE_API_URL || '';
            return `${baseUrl}/uploads/${avatarPath}`;  // ✅
        }
    }
}
</script>

<style scoped>
.profile-avatar-wrapper {
    position: relative;
    width: 120px;
    height: 120px;
    margin: 0 auto 16px;
}

.profile-avatar {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid var(--accent);
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