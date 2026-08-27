<template>
    <ModalWrapper
        v-if="motorcycle"
        :isOpen="isOpen"
        title="Обновить пробег"
        :subtitle="`Текущий пробег: ${motorcycle.mileage || 0} км`"
        icon="tachometer"
        bg-icon-color="var(--accent-trans)"
        icon-color="var(--accent-text)"
        @close="$emit('close')"
    >
        <div class="modal-form-group">
            <label>
                Новый пробег (км) <span class="required">*</span>
                <input
                    v-model.number="form.mileage"
                    type="number"
                    min="0"
                    max="1000000"
                    placeholder="Введите новый пробег"
                    required
                />
            </label>
        </div>

        <div class="modal-info-block info">
            <div class="modal-info-icon">
                <i class="fa fa-info-circle"></i>
            </div>
            <p class="modal-info-text">
                Пробег используется для расчёта интервалов обслуживания и статистики вашего мотоцикла.
                Убедитесь, что значение корректно.
            </p>
        </div>

        <template #actions>
            <div class="modal-actions">
                <button class="btn btn-secondary" @click="$emit('close')">
                    Отменить
                </button>
                <button class="btn btn-primary" :disabled="!isFormValid || loading" @click="submit">
                    <span v-if="!loading">
                        <i class="fa fa-save"></i> Сохранить
                    </span>
                    <span v-else>
                        <i class="fa fa-spinner fa-spin"></i> Сохранение...
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
        }
    },

    data() {
        return {
            form: {
                id: null,
                mileage: null
            },
            loading: false
        }
    },

    computed: {
        isFormValid() {
            return this.form.mileage !== null &&
                   this.form.mileage !== '' &&
                   this.form.mileage >= 0 &&
                   this.form.mileage <= 1000000
        }
    },

    watch: {
        isOpen(newVal) {
            if (newVal) {
                this.resetForm()
            }
            if (!newVal) {
                this.loading = false
            }
        }
    },

    methods: {
        resetForm() {
            this.form = {
                id: this.motorcycle?.id || null,
                mileage: null
            }
            this.loading = false
        },

        async submit() {
            if (!this.isFormValid) {
                alert('Укажите корректный пробег (от 0 до 1 000 000 км)')
                return
            }

            if (this.motorcycle && this.form.mileage < (this.motorcycle.mileage || 0)) {
                if (!confirm('Внимание! Новый пробег меньше текущего. Это может повлиять на историю обслуживания. Продолжить?')) {
                    return
                }
            }

            this.loading = true

            try {
                const submitData = {
                    id: this.motorcycle.id,
                    mileage: this.form.mileage
                }

                await this.$emit('submit', submitData)
                this.resetForm()
                this.$emit('close')
            } catch (error) {
                console.error('Submit error:', error)
                alert('Ошибка при обновлении пробега')
            } finally {
                this.loading = false
            }
        }
    }
}
</script>

<style scoped>
/* ===== ПОЛЯ ВВОДА ===== */
.modal-form-group {
    margin-bottom: 14px;
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

/* ===== ИНФО-БЛОК ===== */
.modal-info-block {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
    border-radius: 10px;
}

.modal-info-block.info {
    background: var(--accent-trans);
    border: 1px solid var(--accent-light);
}

.modal-info-icon {
    font-size: 18px;
    color: var(--accent-text);
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

.btn-primary {
    background: linear-gradient(135deg, var(--accent), var(--accent-hover));
    color: #fff;
}

.btn-primary:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px var(--accent-trans);
}

.btn-secondary {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}

.btn-secondary:hover:not(:disabled) {
    background: var(--border-color);
}

/* ============================================ */
/* ===== АДАПТИВНОСТЬ ===== */
/* ============================================ */

@media (max-width: 640px) {
    .modal-actions {
        flex-direction: column;
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

    .modal-form-group input {
        font-size: 0.9rem;
        padding: 0.5rem 0.7rem;
    }
}

@media (max-width: 400px) {
    .modal-info-text {
        font-size: 13px;
    }

    .modal-actions .btn {
        font-size: 0.85rem;
        padding: 0.7rem;
    }
}
</style>