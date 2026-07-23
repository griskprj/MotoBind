<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Добавление мотоцикла"
        subtitle="Заполните информацию о вашем мотоцикле"
        icon="motorcycle"
        @close="$emit('close')"
    >
        <div class="modal-group">
            <div class="inputs-group">
                <label>
                Название *
                <input v-model="form.name" type="text" class="modal-input" required>
            </label>
            
            <div class="inputs-wrapper">
                <label>
                    Объем
                    <input v-model="form.volume" type="number" min="49" max="4000" class="modal-input">
                </label>
                <label>
                    Пробег
                    <input v-model="form.mileage" type="number" min="0" max="1000000" class="modal-input">
                </label>
            </div>
            <div class="inputs-wrapper">
                <label>
                    Год выпуска
                    <input v-model="form.years" type="number" min="1950" :max="currentYear" class="modal-input">
                </label>
                <label>
                    Гос. номер
                    <input v-model="form.licensePlate" type="text" min="8" max="9" class="modal-input">
                </label>
            </div>
            <label>
                VIN
                <input v-model="form.vin" type="text" min="17" max="17" class="modal-input">
            </label>
            <label>
                Цвет
                <input v-model="form.color" type="color">
            </label>
            </div>

        </div>
        <div class="info-block">
            <div class="block-icon">
                <i class="fa fa-info"></i>
            </div>
            <p class="block-text">
                Эта информацию поможет точнее строить статистику и подбирать мануалы для вашего мотоцикла.
            </p>
        </div>

        <div class="modal-actions">
            <button @click="$emit('close')" class="cancel-btn">Отменить</button>
            <button @click="submit" class="save-btn"><i class="fa fa-plus"></i> Добавить</button>
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
                mileage: null,
                licensePlate: null,
                vin: null,
                color: null,
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

            if (this.form.years && this.form.years > this.currentYear) {
                alert('Год выпуска не может быть в будущем')
                return
            }

            this.$emit('submit', this.form)
            this.resetForm()
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

.info-block {
    display: flex;
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