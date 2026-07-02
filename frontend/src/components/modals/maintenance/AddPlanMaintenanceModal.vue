<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Запланировать обслуживание"
        @close="$emit('close')"
    >
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
                <option value="">Выберите категорию обслуживания</option>
                <option value="engine">Двигатель</option>
                <option value="drive">Привод</option>
                <option value="steering">Рулевое управление</option>
                <option value="suspension">Подвеска</option>
                <option value="electronics">Электроника</option>
                <option value="wheel">Колеса/Шины</option>
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
                category: '',
                description: '',
                mileage: null,
            },
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
            if (!this.form.id) {
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

            this.$emit('submit', this.form)
            this.resetForm()
        },

        resetForm() {
            this.form = {
                id: null,
                title: '',
                category: '',
                description: '',
                mileage: null,
            }
        }
    }
}
</script>