<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Добавить мотоцикл"
        @close="$emit('close')"
    >
        <div class="modal-group">
            <div class="modal-group">
                <input v-model="form.id" type="hidden">
                <label>
                    Название *
                    <input v-model="form.name" type="text" class="modal-input" required>
                </label>
                <label>
                    Объем
                    <input v-model="form.volume" type="number" min="49" max="4000" class="modal-input">
                </label>
                <label>
                    Год выпуска
                    <input v-model="form.years" type="number" min="1950" :max="currentYear" class="modal-input">
                </label>
                <label>
                    Пробег
                    <input v-model="form.mileage" type="number" min="0" max="1000000" class="modal-input">
                </label>

                <div class="modal-actions">
                    <button @click="submit" class="save-btn">Добавить</button>
                    <button @click="$emit('close')" class="cancel-btn">Отменить</button>
                </div>
            </div>
        </div>
    </ModalWrapper>
</template>

<script>
import ModalWrapper from '../ModalWrapper.vue';

export default {
    components: { ModalWrapper },

    props: {
        isOpen: Boolean
    },

    data() {
        return {
            form: {
                name: '',
                volume: null,
                years: null,
                mileage: null
            },
            currentYear: new Date().getFullYear()
        }
    },

    watch: {
        isOpen(newVal) {
            if (newVal) {
                this.resetForm()
            }
        }
    },

    methods: {
        resetForm() {
            this.form = {
                name: '',
                volume: null,
                years: null,
                mileage: null
            }
        },

        submit() {
            if (!this.form.name) {
                alert('Введите название мотоцикла')
                return
            }

            if (!this.form.mileage || this.form.mileage <= 0) {
                alert('Введите корректный пробег')
                return
            }

            if (this.form.years > this.currentYear) {
                alert('Год выпуска не может быть в будущем')
                return
            }

            this.$emit('submit', this.form)
            this.resetForm()
        }
    }
}
</script>