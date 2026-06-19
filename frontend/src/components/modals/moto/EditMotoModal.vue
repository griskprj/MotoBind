<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Редактировать мотоцикл"
        @close="$emit('close')"
    >
        <input v-model="form.id" type="hidden">
        <label>
            Имя
            <input v-model="form.name" type="text" class="modal-input">
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
            <button @click="submit" class="save-btn">Сохранить</button>
            <button @click="this.$emit('close')" class="cancel-btn">Отменить</button>
        </div>
    </ModalWrapper>
</template>

<script>
import ModalWrapper from '../ModalWrapper.vue';

export default {
    components: { ModalWrapper },

    props: {
        isOpen: Boolean,
        motorcycle: {
            type: Object,
            default: null
        }
    },

    data() {
        return {
            form: {
                id: null,
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
            if (newVal && this.motorcycle) {
                this.form = {
                    id: this.motorcycle.id,
                    name: this.motorcycle.name || '',
                    volume: this.motorcycle.volume || null,
                    years: this.motorcycle.years || null,
                    mileage: this.motorcycle.mileage || null
                }
            }
        },

        motorcycle: {
            handler(newVal) {
                if (this.isOpen && newVal) {
                    this.form = {
                        id: newVal.id,
                        name: newVal.name || '',
                        volume: newVal.volume || null,
                        years: newVal.years || null,
                        mileage: newVal.mileage || null
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
                name: '',
                volume: null,
                years: null,
                mileage: null
            }
        },

        submit(id) {
            this.$emit('submit', this.form)
            this.resetForm()
        }
    }
}
</script>