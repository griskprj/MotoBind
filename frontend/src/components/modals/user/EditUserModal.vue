<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Редактирование профиля"
        subtitle="Измените информацию о себе. Эти данные будут видны пользователям."
        icon="pen"
        @close="$emit('close')"
    >   
        <div class="inputs-group">
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