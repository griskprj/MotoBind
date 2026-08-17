<template>
    <ModalWrapper
        v-if="motorcycle"
        :is-open="isOpen"
        title="Обновить пробег"
        @close="$emit('close')"
        icon="tachometer"
        :subtitle="`Текущий пробег: ${motorcycle.mileage}`"
    >
        <label>
            Новый пробег
            <input v-model="form.mileage" type="number" max="1000000" min="0" required>
        </label>

        <div class="info-block">
            <div class="block-icon">
                <i class="fa fa-info"></i>
            </div>
            <p class="block-text">
                Пробег используется для расчета инетрвалов обслуживания и статистики вашего мотоцикла
            </p>
        </div>

        <div class="modal-actions">
            <button @click="$emit('close')" class="cancel-btn">Отменить</button>
            <button @click="submit"><i class="fa fa-check"></i> Сохранить</button>
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
        motorcycle: {
            type: Object,
            default: []
        }
    },

    data() {
        return {
            form: {
                id: null,
                mileage: null
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
            if (!this.form.mileage || this.form.mileage < 0 || this.form.mileage > 1000000) {
                alert(`Укажите корректный пробег: ${this.form.mileage}`)
                return
            }

            this.form.id = this.motorcycle.id

            this.$emit('submit', this.form)
            this.resetForm()
        },

        resetForm() {
            this.form = {
                id: null,
                mileage: null
            }
        }
    }
}
</script>

<style scoped>
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
    display: flex;
    flex-direction: row;
}

.modal-actions button {
    width: 100%;
}
</style>