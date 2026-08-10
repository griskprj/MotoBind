<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Запланировать обслуживание"
        subtitle="Запланируйте следующее обслуживание"
        icon="calendar"
        @close="$emit('close')"
    >
        <div class="inputs-wrapper">
            <label>
                <i class="fa fa-motorcycle"></i> Мотоцикл
                <select v-model="form.motorcycleId"> <!-- ИСПРАВЛЕНО: id → motorcycleId -->
                    <option value="">Выберите мотоцикл</option>
                    <option v-for="moto in motorcycles" :key="moto.id" :value="moto.id">{{ moto.name }}</option>
                </select>
            </label>
            <label>
                <i class="fa fa-wrench"></i> Категория
                <select v-model="form.category" @change="onCategoryChange">
                    <option value="">Выберите категорию</option>
                    <option value="engine">Двигатель</option>
                    <option value="drive">Привод</option>
                    <option value="steering">Рулевое управление</option>
                    <option value="suspension">Подвеска</option>
                    <option value="electronics">Электроника</option>
                    <option value="wheel">Колеса/Шины</option>
                    <option value="brakes">Тормозная система</option>
                    <option value="fuel">Топливная система</option>
                    <option value="cooling">Система охлаждения</option>
                </select>
            </label>
        </div>

        <!-- ШАБЛОНЫ -->
        <label v-if="templates.length > 0">
            <i class="fa fa-list"></i> Тип обслуживания
            <select v-model="form.templateId" @change="onTemplateChange">
                <option value="">Выберите тип обслуживания</option>
                <option v-for="tpl in templates" :key="tpl.id" :value="tpl.id">
                    {{ tpl.label }}
                </option>
            </select>
        </label>
        <input v-model="form.title" type="hidden">

        <label>
            <i class="fa fa-align-justify"></i> Описание
            <input v-model="form.description" type="text">
        </label>
        <label>
            <i class="fa fa-tachometer"></i> Плановый пробег
            <input v-model="form.planned_mileage" type="number" max="1000000" min="0">
        </label>

        <div class="info-block">
            <div class="block-icon">
                <i class="fa fa-info"></i>
            </div>
            <p class="block-text">
                Мы напомним, когда придет время обслуживать
            </p>
        </div>

        <div class="modal-actions">
            <button @click="$emit('close')" class="cancel-btn">Отменить</button>
            <button @click="submit"><i class="fa fa-calendar"></i> Запланировать</button>
        </div>
    </ModalWrapper>
</template>

<script>
import ModalWrapper from '../ModalWrapper.vue';
import { getTemplatesByCategory } from '../../../constants/maintenanceTemplates';

export default {
    components: { ModalWrapper },

    props: {
        isOpen: {
            type: Boolean,
            default: false
        },
        motorcycles: {
            type: Array,
            default: () => []
        }
    },
    
    data() {
        return {
            form: {
                motorcycleId: null, // ИСПРАВЛЕНО: id → motorcycleId
                title: '',
                category: '',
                templateId: '',
                description: '',
                planned_mileage: null,
            },
            templates: []
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
        onCategoryChange() {
            this.form.templateId = '';
            this.form.title = '';
            this.templates = this.form.category ? getTemplatesByCategory(this.form.category) : [];
        },

        onTemplateChange() {
            const found = this.templates.find(t => t.id === this.form.templateId);
            this.form.title = found ? found.label : '';
        },

        submit() {
            if (!this.form.motorcycleId) { // ИСПРАВЛЕНО: form.id → form.motorcycleId
                alert('Выберите мотоцикл')
                return
            }

            if (!this.form.title) {
                alert('Введите название обслуживания')
                return
            }
            
            if (!this.form.planned_mileage || this.form.planned_mileage <= 0) {
                alert('Введите корректный пробег')
                return
            }

            const payload = {
                motorcycleId: this.form.motorcycleId, // ИСПРАВЛЕНО: id → motorcycleId
                title: this.form.title,
                category: this.form.category,
                description: this.form.description || '',
                planned_mileage: this.form.planned_mileage
            }

            this.$emit('submit', payload)
            this.resetForm()
        },

        resetForm() {
            this.form = {
                motorcycleId: null, // ИСПРАВЛЕНО: id → motorcycleId
                title: '',
                category: '',
                templateId: '',
                description: '',
                planned_mileage: null,
            }
            this.templates = []
        }
    }
}
</script>

<style scoped>
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
</style>