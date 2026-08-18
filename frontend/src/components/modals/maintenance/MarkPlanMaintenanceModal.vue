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
                <p class="card-title">{{ motorcycle?.name || 'Мотоцикл' }}</p>

                <div class="maintenance-card">
                    <i class="fa fa-wrench"></i>
                    <p class="maintenance-title">{{ maintenance?.title || 'Обслуживание' }}</p>
                </div>
                
                <!-- Показываем плановый пробег -->
                <div v-if="maintenance?.planned_mileage" class="planned-info">
                    <i class="fa fa-clock"></i>
                    <span>Плановый пробег: {{ maintenance.planned_mileage }} км</span>
                </div>
            </div>
        </div>

        <div class="inputs-group">
            <label>
                Пробег выполнения <span class="required">*</span>
                <input 
                    v-model.number="form.mileage" 
                    type="number" 
                    min="0"
                    max="1000000"
                    placeholder="Введите пробег"
                    required
                >
            </label>
            <label>
                Дата выполнения
                <input 
                    v-model="form.date" 
                    type="date" 
                    :max="today"
                >
            </label>
        </div>
        
        <label class="cost-label">
            <i class="fa fa-ruble"></i>
            Стоимость
            <input 
                v-model.number="form.cost" 
                type="number" 
                min="0"
                placeholder="0"
            >
        </label>
        
        <label class="checkbox-group">
            <input v-model="form.isRepeat" type="checkbox">
            <span>Запланировать следующее обслуживание</span>
        </label>
        
        <label v-if="form.isRepeat" class="interval-label">
            Интервал (км)
            <input 
                v-model.number="form.interval" 
                type="number" 
                min="1"
                max="100000"
                placeholder="Например: 5000"
                required
            >
        </label>

        <div class="info-block">
            <div class="info-icon"><i class="fa fa-info-circle"></i></div>
            <p class="info-text">
                Это действие нельзя отменить. Вы всегда сможете посмотреть записи в истории обслуживания.
            </p>
        </div>

        <div class="modal-actions">
            <button @click="$emit('close')" class="cancel-btn">Отменить</button>
            <button 
                @click="submit" 
                class="accept-btn"
                :disabled="!form.mileage || form.mileage < 0"
            >
                <i class="fa fa-check"></i> Завершить обслуживание
            </button>
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
                moto_id: null,
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
                    moto_id: this.motorcycle.id,
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
            
            if (!this.form.mileage || this.form.mileage < 0) {
                alert('Укажите пробег выполнения')
                return
            }
            
            const submitData = {
                id: this.maintenance.id,
                moto_id: this.motorcycle.id,
                mileage: this.form.mileage,
                date: this.form.date || this.today,
                cost: this.form.cost || 0,
                isRepeat: this.form.isRepeat,
                interval: this.form.interval
            }
            
            this.$emit('submit', submitData)
            this.resetForm()
        },

        resetForm() {
            this.form = {
                id: null,
                moto_id: null,
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

.planned-info {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 10px;
    padding: 6px 12px;
    background: rgba(251, 191, 36, 0.08);
    border-radius: 8px;
    color: #fbbf24;
    font-size: 13px;
}

.required {
    color: var(--danger);
    margin-left: 4px;
}

.inputs-group {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin-bottom: 12px;
}

.cost-label {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
    padding: 8px 12px;
    background: rgba(255, 255, 255, 0.02);
    border-radius: 8px;
}

.cost-label input {
    flex: 1;
}

.checkbox-group {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
    cursor: pointer;
    font-size: 14px;
}

.checkbox-group input[type="checkbox"] {
    width: 18px;
    height: 18px;
    accent-color: var(--accent);
    cursor: pointer;
}

.interval-label {
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin-bottom: 12px;
}

/* Остальные стили остаются без изменений */
.moto-card {
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 12px;
    border-radius: 14px;
    align-items: center;
    text-align: center;
    background-color: var(--bg-card);
    margin-bottom: 16px;
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
    gap: 10px;
    margin-top: 16px;
}

.modal-actions button {
    flex: 1;
}

.info-block {
    display: flex;
    padding: 12px;
    background-color: var(--accent-trans);
    border-radius: 10px;
    border: 1px solid var(--accent-light);
    margin-top: 12px;
}

.info-icon {
    color: var(--accent);
    font-size: 20px;
    margin-right: 12px;
    flex-shrink: 0;
}

.info-text {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.4;
}

.accept-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

@media (max-width: 480px) {
    .inputs-group {
        grid-template-columns: 1fr;
    }
}
</style>