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
                    <select v-model="form.id">
                        <option value="">Выберите мотоцикл</option>
                        <option v-for="moto in motorcycles" :value="moto.id">{{ moto.name }}</option>
                    </select>
                </label>
                <label>
                    <i class="fa fa-wrench"></i>
                    <select v-model="form.category">
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
            <label>
                <i class="fa fa-font"></i> Название *
                <input v-model="form.title" type="text" required>
            </label>
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
                    <i class="fa fa-ruble"></i>
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
                id: null,
                title: '',
                description: '',
                category: '',
                cost: null,
                mileage: null,
                date: null
            },
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
        submit() {
            if (!this.form.title) {
                alert('Введите название')
                return
            }

            if (!this.form.mileage || this.form.mileage <= 0) {
                alert('Введите корректный пробег')
                return
            }

            this.$emit('submit', this.form)
            this.resetForm()
        },

        resetForm() {
            this.form = {
                id: null,
                title: '',
                description: '',
                category: '',
                cost: null,
                mileage: null,
                date: null
            }
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
    padding: 12px;
    background-color: var(--success-trans);
    border-radius: 10px;
    border: 1px solid var(--success);
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

.modal-actions button {
    font-weight: 600;
}
</style>