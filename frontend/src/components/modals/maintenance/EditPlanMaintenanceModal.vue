<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Редактировать обслуживание"
        @close="$emit('close')"
    >
        <label>
            <input v-model="form.maintenanceId" type="hidden">

            <i class="fa fa-motorcycle"></i> Мотоцикл
            <select v-model="form.motorcycleId">
                <option v-for="moto in motorcycles" :value="moto.id">{{ moto.name }}</option>
            </select>
        </label>
        <label>
            <i class="fa fa-font"></i> Название
            <input v-model="form.title" type="text">
        </label>
        <label>
            <i class="fa fa-align-justify"></i> Описание
            <input v-model="form.description" type="text">
        </label>
        <label>
            <i class="fa fa-tachometer"></i> Пробег
            <input v-model="form.mileage" type="number" max="1000000" min="0">
        </label>

        <div class="modal-actions">
            <button @click="submit">Добавить</button>
            <button @click="$emit('close')" class="cancel-btn">Отменить</button>
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
        },
        motorcycles: {
            type: Array,
            default: []
        },
        maintenance: {
            type: Object,
            default: null
        }
    },

    data() {
        return {
            form: {
                motorcycleId: null,
                maintenanceId: null,
                title: '',
                description: '',
                mileage: null
            }
        }
    },

    watch: {
        isOpen(newVal) {
            if (newVal && this.maintenance) {
                this.form = {
                maintenanceId: this.maintenance.id,
                motorcycleId: this.maintenance.moto_id,
                title: this.maintenance.title || '',
                description: this.maintenance.description || '',
                mileage: this.maintenance.planned_mileage || null
                }
            }
        },

        maintenance: {
            handler(newVal) {
                if (this.isOpen && newVal) {
                    this.form = {
                        maintenanceId: newVal.id,
                        motorcycleId: newVal.moto_id,
                        title: newVal.title,
                        description: newVal.description,
                        mileage: newVal.planned_mileage
                    }
                }
            },
            deep: true
        }
    },

    methods: {
        submit() {
            this.$emit('submit', this.form)
            this.resetForm()
        },

        resetForm() {
            this.form = {
                motorcycleId: null,
                maintenanceId: null,
                title: '',
                description: '',
                mileage: null
            }
        }
    }
}
</script>