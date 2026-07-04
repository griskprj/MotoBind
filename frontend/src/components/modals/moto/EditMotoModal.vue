<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Редактировать мотоцикл"
        @close="$emit('close')"
    >
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
            Пробег
            <input v-model="form.mileage" type="number" min="0" max="1000000" class="modal-input">
        </label>
        <label>
            Год выпуска
            <input v-model="form.years" type="number" min="1950" :max="currentYear" class="modal-input">
        </label>
        <label>
            Гос. номер
            <input v-model="form.licensePlate" type="text" min="8" max="9" class="modal-input">
        </label>
        <label>
            VIN
            <input v-model="form.vin" type="text" min="17" max="17" class="modal-input">
        </label>
        <label>
            Цвет
            <input v-model="form.color" type="color">
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
                mileage: null,
                licensePlate: null,
                vin: null,
                color: null,
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
                    mileage: this.motorcycle.mileage || null,
                    licensePlate: this.motorcycle.license_plate || '',
                    vin: this.motorcycle.vin || '',
                    color: this.motorcycle.color || null
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
                        mileage: newVal.mileage || null,
                        licensePlate: newVal.license_plate || '',
                        vin: newVal.vin || '',
                        color: newVal.color || null
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
                mileage: null,
                licensePlate: null,
                vin: null,
                color: null,
            }
        },

        submit(id) {
            this.$emit('submit', this.form)
            this.resetForm()
        }
    }
}
</script>