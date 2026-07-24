<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Отметить обслуживание"
        subtitle="Вы уверены, что хотите завершить это обслуживание?"
        icon="check"
        bgIconColor="var(--success-trans)"
        iconColor="var(--success)"
        @close="$emit('close')"
    >   

        <div class="moto-card">
            <div class="card-info">
                <p class="card-title">{{ motorcycle.name }}</p>

                <div class="maintenance-card">
                    <i class="fa fa-wrench"></i>
                    <p class="maintenance-title">{{ maintenance.title }}</p>
                </div>
            </div>
        </div>

        <div class="inputs-group">
            <label>
                Пробег выполнения
                <input v-model="form.mileage" type="number" max="1000000">
            </label>
            <label>
                Дата
                <input v-model="form.date" type="date" :max="new Date().toISOString().split('T')">
            </label>
        </div>
        <label>
            <i class="fa fa-ruble"></i>
            <input v-model="form.cost" type="number">
        </label>
        <label class="checkbox-group">
            Запланировать следующее обслуживание?
            <input v-model="form.isRepeat" type="checkbox">
        </label>
        <label v-if="form.isRepeat">
            Интервал
            <input v-model="form.interval" type="number" max="100000">
        </label>

        <div class="info-block">
            <div class="info-icon"><i class="fa fa-info"></i></div>

            <p class="info-text">Это действие нельзя отменить. Вы всегда сможете посмотреть записи в истории обслуживания.</p>
        </div>

        <div class="modal-actions">
            <button @click="$emit('close')" class="cancel-btn">Отменить</button>
            <button @click="submit()" class="accept-btn"><i class="fa fa-check"></i> Завершить обслуживание</button>
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
            default: null
        },
        maintenance: {
            type: Object,
            default: null
        }
    },

    data() {
        return {
            form: {
                id: null,
                mileage: null,
                date: null,
                cost: null,
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
            if (newVal && this.maintenance) {
                this.form = {
                    id: this.maintenance.id,
                    mileage: null,
                    date: this.today,
                    cost: null,
                    isRepeat: false,
                    interval: null
                }
            }
        }
    },

    methods: {
        submit() {
            if (!this.maintenance) {
                console.error('No maintenance data')
                return
            }
            
            const submitData = {
                ...this.form,
                id: this.maintenance.id
            }
            
            this.$emit('submit', submitData)
            this.resetForm()
        },

        resetForm() {
            this.form = {
                id: null,
                mileage: null,
                date: this.today,
                cost: null,
                isRepeat: false,
                interval: null
            }
        }
    }
}
</script>

<style scoped>
.inputs-group {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
}

.moto-card {
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 12px;
    border-radius: 14px;
    align-items: center;
    text-align: center;
    background-color: var(--bg-card);
}

.card-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 14px;
}

.maintenance-card {
    background-color: var(--accent-trans);
    border-radius: 10px;
    padding: 8px 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    color: var(--accent);
}

.modal-actions {
    display: flex;
    flex-direction: row;
}

.modal-actions button {
    width: 100%;
}

.info-block {
    display: flex;
    padding: 12px;
    background-color: var(--accent-trans);
    border-radius: 10px;
    border: 1px solid var(--accent-light);
}

.info-icon {
    color: var(--accent);
    font-size: 24px;
    margin-right: 12px;
}

.info-text {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 0;
}
</style>