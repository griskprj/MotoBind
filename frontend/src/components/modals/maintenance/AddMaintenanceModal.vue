<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Добавление в историю"
        subtitle="Обслуживание будет добавлено в историю"
        icon="check"
        bgIconColor="var(--success-trans)"
        iconColor="var(--success)"
        @close="$emit('close')"
    >
        <div class="modal-group">
            <div class="inputs-wrapper">
                <label>
                    <i class="fa fa-motorcycle"></i> Мотоцикл
                    <select v-model="form.motorcycleId">
                        <option value="">Выберите мотоцикл</option>
                        <option v-for="moto in motorcycles" :value="moto.id">{{ moto.name }}</option>
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

            <!-- === ШАБЛОНЫ ТО === -->
            <label v-if="templates.length > 0">
                <i class="fa fa-list"></i> Тип обслуживания
                <select v-model="form.templateId" @change="onTemplateChange">
                    <option value="">Выберите тип обслуживания</option>
                    <option v-for="tpl in templates" :key="tpl.id" :value="tpl.id">
                        {{ tpl.label }}
                    </option>
                </select>
            </label>
            <input v-model="form.title" type="hidden" required>

            <label>
                <i class="fa fa-align-justify"></i> Описание
                <input v-model="form.description" type="text">
            </label>
            <label>
                <i class="fa fa-tachometer"></i> Пробег *
                <input v-model="form.mileage" type="number" max="1000000" min="0" required>
            </label>
            <div class="inputs-wrapper">
                <label>
                    <i class="fa fa-ruble"></i> Стоимость
                    <input v-model="form.cost" type="number">
                </label>
                <label>
                    <i class="fa fa-calendar"></i> Дата
                    <input v-model="form.date" type="date" :max="currentDate">
                </label>
            </div>
        </div>

        <div class="info-block">
            <div class="block-icon">
                <i class="fa fa-info-circle"></i>
            </div>
            <p class="block-text">
                Эта запись будет добавлена в историю обслуживания мотоцикла.
            </p>
        </div>

        <div class="modal-actions">
            <button @click="$emit('close')" class="cancel-btn">Отменить</button>
            <button @click="submit" class="accept-btn"><i class="fa fa-check"></i> Добавить</button>
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
            default: []
        }
    },

    data() {
        return {
            form: {
                motorcycleId: null,
                title: '',
                description: '',
                category: '',
                templateId: '', // ID шаблона
                cost: null,
                mileage: null,
                date: null
            },
            templates: [],
            currentDate: new Date().toISOString().split('T')[0]
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
        // При смене категории — подгружаем шаблоны
        onCategoryChange() {
            this.form.templateId = '';
            this.form.title = '';
            this.templates = this.form.category ? getTemplatesByCategory(this.form.category) : [];
        },

        // При выборе шаблона — заполняем название
        onTemplateChange() {
            const found = this.templates.find(t => t.id === this.form.templateId);
            this.form.title = found ? found.label : '';
        },

        submit() {
            if (!this.form.motorcycleId) {
                alert('Выберите мотоцикл')
                return
            }

            if (!this.form.title) {
                alert('Введите название обслуживания')
                return
            }

            if (!this.form.mileage || this.form.mileage <= 0) {
                alert('Введите корректный пробег')
                return
            }

            // Отправляем только нужные поля (без templateId)
            const payload = {
                motorcycleId: this.form.motorcycleId,
                title: this.form.title,
                description: this.form.description,
                category: this.form.category,
                cost: this.form.cost,
                mileage: this.form.mileage,
                date: this.form.date
            }

            this.$emit('submit', payload)
            this.resetForm()
        },

        resetForm() {
            this.form = {
                motorcycleId: null,
                title: '',
                description: '',
                category: '',
                templateId: '',
                cost: null,
                mileage: null,
                date: null
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
    background-color: var(--success-trans);
    border-radius: 10px;
    border: 1px solid var(--success-light);
}

.block-icon {
    color: var(--success);
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