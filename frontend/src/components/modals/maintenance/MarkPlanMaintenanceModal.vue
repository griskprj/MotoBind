<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Отметить обслуживание"
        @close="$emit('close')"
    >   
        <label>
            Пробег выполнения
            <input v-model="form.mileage" type="number" max="1000000">
        </label>
        <label>
            Дата
            <input v-model="form.date" type="date" :max="new Date().toISOString().split('T')">
        </label>
        <label class="checkbox-group">
            Запланировать следующее обслуживание?
            <input v-model="form.isRepeat" type="checkbox">
        </label>
        <label v-if="form.isRepeat">
            Интервал
            <input v-model="form.interval" type="number" max="100000">
        </label>

        <div class="modal-actions">
            <button @click="submit()">Сохранить</button>
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
        id: {
            type: Number,
            default: null
        }
    },

    data() {
        return {
            form: {
                id: null,
                mileage: null,
                date: null,
                isRepeat: false,
                interval: null
            }
        }
    },

    computed: {
        today() {
            return new Date().toISOString().split('T')[0]
        }
    },

    watch: {
        isOpen(newVal) {
            if (newVal && this.id) {
                this.form = {
                    id: this.id,
                    mileage: null,
                    date: this.today,
                    isRepeat: false,
                    interval: null
                }
            }
        }
    },

    methods: {
        submit() {
            this.$emit('submit', this.form)
            this.resetForm()
        },

        resetForm() {
            this.form = {
                id: null,
                mileage: null,
                date: this.today,
                isRepeat: false,
                interval: null
            }
        }
    }
}
</script>