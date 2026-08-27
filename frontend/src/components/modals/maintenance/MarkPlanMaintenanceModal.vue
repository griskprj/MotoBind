<template>
    <ModalWrapper
        :isOpen="isOpen"
        title="Завершить обслуживание"
        subtitle="Подтвердите завершение обслуживания"
        icon="check"
        bg-icon-color="var(--success-trans)"
        icon-color="var(--success-text)"
        size="md"
        @close="$emit('close')"
    >
        <!-- Информация о мотоцикле и обслуживании -->
        <div class="info-card">
            <div class="info-card-row">
                <span class="info-label">Мотоцикл</span>
                <span class="info-value">{{ motorcycle?.name || '—' }}</span>
            </div>
            <div class="info-card-row">
                <span class="info-label">Обслуживание</span>
                <span class="info-value">
                    <span class="maintenance-tag">
                        <i class="fa fa-wrench"></i>
                        {{ maintenance?.title || '—' }}
                    </span>
                </span>
            </div>
            <div v-if="maintenance?.planned_mileage" class="info-card-row">
                <span class="info-label">Плановый пробег</span>
                <span class="info-value">
                    <span class="planned-badge">
                        <i class="fa fa-clock"></i>
                        {{ maintenance.planned_mileage }} км
                    </span>
                </span>
            </div>
        </div>

        <!-- Форма -->
        <div class="modal-form-group">
            <label>
                Пробег выполнения <span class="required">*</span>
                <input
                    v-model.number="form.mileage"
                    type="number"
                    min="0"
                    max="1000000"
                    placeholder="Введите пробег"
                    required
                />
            </label>
        </div>

        <div class="modal-form-row">
            <div class="modal-form-group">
                <label>
                    Дата выполнения
                    <input
                        v-model="form.date"
                        type="date"
                        :max="today"
                    />
                </label>
            </div>

            <div class="modal-form-group">
                <label>
                    Стоимость (₽)
                    <input
                        v-model.number="form.cost"
                        type="number"
                        min="0"
                        placeholder="0"
                    />
                </label>
            </div>
        </div>

        <!-- Чекбокс: следующее обслуживание -->
        <label class="checkbox-group">
            <input v-model="form.isRepeat" type="checkbox" />
            <span>Запланировать следующее обслуживание</span>
        </label>

        <!-- Интервал (показывается если isRepeat = true) -->
        <div v-if="form.isRepeat" class="modal-form-group">
            <label>
                Интервал (км)
                <input
                    v-model.number="form.interval"
                    type="number"
                    min="1"
                    max="100000"
                    placeholder="Например: 5000"
                />
            </label>
        </div>

        <!-- Инфо-блок -->
        <div class="modal-info-block warning">
            <div class="modal-info-icon">
                <i class="fa fa-exclamation-triangle"></i>
            </div>
            <div>
                <p class="modal-info-text" style="font-weight: 600; color: var(--warning-text);">
                    Это действие нельзя отменить!
                </p>
                <p class="modal-info-text">
                    Запись будет добавлена в историю обслуживания. Вы всегда сможете её просмотреть.
                </p>
            </div>
        </div>

        <!-- Действия -->
        <template #actions>
            <div class="modal-actions">
                <button class="btn btn-secondary" @click="$emit('close')">
                    Отменить
                </button>
                <button
                    class="btn btn-success"
                    :disabled="!form.mileage || form.mileage < 0 || loading"
                    @click="submit"
                >
                    <span v-if="!loading">
                        <i class="fa fa-check"></i> Завершить
                    </span>
                    <span v-else>
                        <i class="fa fa-spinner fa-spin"></i> Завершение...
                    </span>
                </button>
            </div>
        </template>
    </ModalWrapper>
</template>

<script>
import ModalWrapper from '../ModalWrapper.vue'

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
            },
            loading: false
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
                this.resetForm()
            }
        }
    },

    methods: {
        resetForm() {
            this.form = {
                id: this.maintenance?.id || null,
                moto_id: this.motorcycle?.id || null,
                mileage: null,
                date: this.today,
                cost: null,
                isRepeat: false,
                interval: null
            }
            this.loading = false
        },

        async submit() {
            if (!this.maintenance) {
                console.error('No maintenance data')
                return
            }

            if (!this.form.mileage || this.form.mileage < 0) {
                alert('Укажите пробег выполнения')
                return
            }

            if (this.form.isRepeat && (!this.form.interval || this.form.interval <= 0)) {
                alert('Укажите интервал для следующего обслуживания')
                return
            }

            this.loading = true

            try {
                const submitData = {
                    id: this.maintenance.id,
                    moto_id: this.motorcycle.id,
                    mileage: this.form.mileage,
                    date: this.form.date || this.today,
                    cost: this.form.cost || 0,
                    isRepeat: this.form.isRepeat,
                    interval: this.form.interval
                }

                await this.$emit('submit', submitData)
                this.$emit('close')
            } catch (error) {
                console.error('Submit error:', error)
                alert('Ошибка при завершении обслуживания')
            } finally {
                this.loading = false
            }
        }
    }
}
</script>

<style scoped>
/* ===== ИНФО-КАРТОЧКА ===== */
.info-card {
    background: var(--bg-secondary);
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 16px;
    border: 1px solid var(--border-light);
}

.info-card-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid var(--border-light);
}

.info-card-row:last-child {
    border-bottom: none;
}

.info-label {
    font-size: 13px;
    color: var(--text-muted);
}

.info-value {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-primary);
}

.maintenance-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 2px 12px;
    background: var(--accent-trans);
    border-radius: 12px;
    color: var(--accent-text);
    font-size: 13px;
}

.planned-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 2px 12px;
    background: var(--warning-trans);
    border-radius: 12px;
    color: var(--warning-text);
    font-size: 13px;
}

/* ===== ФОРМА ===== */
.modal-form-group {
    margin-bottom: 14px;
}

.modal-form-group:last-child {
    margin-bottom: 0;
}

.modal-form-group label {
    display: block;
    font-weight: 600;
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-bottom: 4px;
}

.modal-form-group label .required {
    color: var(--danger-text);
    font-weight: 700;
}

.modal-form-group input {
    width: 100%;
    padding: 0.6rem 0.8rem;
    border-radius: 10px;
    border: 2px solid var(--border-color);
    background-color: var(--bg-input);
    color: var(--text-primary);
    font-size: 0.95rem;
    transition: all 0.2s;
    box-sizing: border-box;
}

.modal-form-group input:focus {
    border-color: var(--accent);
    outline: none;
    box-shadow: 0 0 0 3px var(--accent-trans);
}

.modal-form-group input::placeholder {
    color: var(--text-muted);
}

.modal-form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}

/* ===== ЧЕКБОКС ===== */
.checkbox-group {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 4px 0 10px 0;
    cursor: pointer;
    font-size: 14px;
    color: var(--text-secondary);
}

.checkbox-group input[type="checkbox"] {
    width: 18px;
    height: 18px;
    accent-color: var(--accent);
    cursor: pointer;
    flex-shrink: 0;
}

.checkbox-group span {
    user-select: none;
}

/* ===== ИНФО-БЛОК ===== */
.modal-info-block {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
    border-radius: 10px;
    margin: 12px 0;
}

.modal-info-block.warning {
    background: var(--warning-trans);
    border: 1px solid rgba(245, 158, 11, 0.2);
}

.modal-info-icon {
    font-size: 18px;
    color: var(--warning-text);
    flex-shrink: 0;
    margin-top: 2px;
}

.modal-info-text {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.5;
}

/* ===== КНОПКИ ===== */
.modal-actions {
    display: flex;
    gap: 10px;
}

.modal-actions .btn {
    flex: 1;
    padding: 0.7rem 1rem;
    border-radius: 40px;
    font-weight: 600;
    font-size: 0.9rem;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.modal-actions .btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.btn-secondary {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}

.btn-secondary:hover:not(:disabled) {
    background: var(--border-color);
}

.btn-success {
    background: linear-gradient(135deg, var(--success), var(--success-hover));
    color: #fff;
}

.btn-success:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
}

/* ============================================ */
/* ===== АДАПТИВНОСТЬ ===== */
/* ============================================ */

@media (max-width: 640px) {
    .modal-form-row {
        grid-template-columns: 1fr;
        gap: 0;
    }

    .info-card-row {
        flex-direction: column;
        align-items: flex-start;
        gap: 2px;
        padding: 8px 0;
    }

    .modal-actions {
        flex-direction: column-reverse;
    }

    .modal-actions .btn {
        width: 100%;
        padding: 0.8rem;
    }

    .modal-info-block {
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .modal-info-icon {
        margin-top: 0;
    }
}

@media (max-width: 400px) {
    .info-card {
        padding: 12px 14px;
    }

    .info-value {
        font-size: 13px;
    }

    .modal-form-group input {
        font-size: 0.9rem;
        padding: 0.5rem 0.7rem;
    }

    .maintenance-tag,
    .planned-badge {
        font-size: 12px;
        padding: 2px 10px;
    }
}
</style>