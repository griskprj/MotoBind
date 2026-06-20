<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Обновить пробег"
        @close="$emit('close')"
    >
        <label>
            <i class="fa fa-motorcycle"></i> Мотоцикл
            <select v-model="form.id">
                <option value="">Выберите мотоцикл</option>
                <option v-for="moto in motorcycles" :value="moto.id">
                    {{ moto.name }}
                </option>
            </select>
        </label>
        <label>
            <i class="fa fa-tachometer"></i> Новый пробег
            <input v-model="form.newMileage" type="number">
        </label>

        <div class="modal-actions">
            <button @click="submit">Сохранить</button>
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
                newMileage: null
            }
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

            if (!this.form.newMileage || this.form.newMileage <= 0) {
                alert('Укажите корректный пробег')
                return
            }

            this.$emit('submit', this.form)
            this.resetForm()
        },

        resetForm() {
            this.form = {
                id: null,
                newMileage: null
            }
        }
    }
}
</script>