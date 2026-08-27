<template>
    <ModalWrapper
        :isOpen="isOpen"
        title="Смена пароля"
        subtitle="Для безопасности используйте надёжный пароль"
        icon="lock"
        bg-icon-color="var(--accent-trans)"
        icon-color="var(--accent-text)"
        @close="$emit('close')"
    >
        <div class="modal-form-group">
            <label>
                Текущий пароль <span class="required">*</span>
                <input
                    v-model="form.currentPassword"
                    type="password"
                    placeholder="Введите текущий пароль"
                    required
                />
            </label>
        </div>

        <div class="modal-form-group">
            <label>
                Новый пароль <span class="required">*</span>
                <input
                    v-model="form.newPassword"
                    type="password"
                    placeholder="Введите новый пароль"
                    required
                />
            </label>
        </div>

        <div class="modal-form-group">
            <label>
                Повторите новый пароль <span class="required">*</span>
                <input
                    v-model="form.repeatPassword"
                    type="password"
                    placeholder="Повторите новый пароль"
                    required
                />
            </label>
        </div>

        <div class="modal-info-block info">
            <div class="modal-info-icon">
                <i class="fa fa-shield-alt"></i>
            </div>
            <div>
                <p class="modal-info-text">
                    <strong>Рекомендации по созданию надёжного пароля:</strong>
                </p>
                <ul class="password-tips">
                    <li>Минимум 8 символов</li>
                    <li>Используйте буквы в разных регистрах</li>
                    <li>Добавьте цифры и специальные символы</li>
                    <li>Не используйте личную информацию</li>
                </ul>
            </div>
        </div>

        <template #actions>
            <div class="modal-actions">
                <button class="btn btn-secondary" @click="$emit('close')">
                    Отменить
                </button>
                <button class="btn btn-primary" :disabled="!isFormValid || loading" @click="submit">
                    <span v-if="!loading">
                        <i class="fa fa-key"></i> Изменить пароль
                    </span>
                    <span v-else>
                        <i class="fa fa-spinner fa-spin"></i> Изменение...
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
            required: true,
            default: false
        }
    },

    data() {
        return {
            form: {
                currentPassword: '',
                newPassword: '',
                repeatPassword: ''
            },
            loading: false
        }
    },

    computed: {
        isFormValid() {
            return this.form.currentPassword &&
                   this.form.currentPassword.length >= 6 &&
                   this.form.newPassword &&
                   this.form.newPassword.length >= 6 &&
                   this.form.repeatPassword &&
                   this.form.newPassword === this.form.repeatPassword
        }
    },

    watch: {
        isOpen(newVal) {
            if (!newVal) {
                this.resetForm()
                this.loading = false
            }
        }
    },

    methods: {
        resetForm() {
            this.form = {
                currentPassword: '',
                newPassword: '',
                repeatPassword: ''
            }
            this.loading = false
        },

        async submit() {
            // Проверка: заполнены ли все поля
            if (!this.form.currentPassword) {
                alert('Введите текущий пароль')
                return
            }

            if (!this.form.newPassword || this.form.newPassword.length < 6) {
                alert('Новый пароль должен содержать минимум 6 символов')
                return
            }

            if (this.form.newPassword !== this.form.repeatPassword) {
                alert('Новые пароли не совпадают')
                return
            }

            if (this.form.newPassword === this.form.currentPassword) {
                alert('Новый пароль должен отличаться от текущего')
                return
            }

            this.loading = true

            try {
                await this.$emit('submit', this.form)
                this.resetForm()
                this.$emit('close')
            } catch (error) {
                console.error('Submit error:', error)
                alert('Ошибка при смене пароля')
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

/* ===== ИНФО-БЛОК ===== */
.modal-info-block {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
    border-radius: 10px;
    margin: 4px 0 12px;
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
    margin: 0 0 4px 0;
    line-height: 1.5;
}

.password-tips {
    margin: 4px 0 0 0;
    padding-left: 20px;
    color: var(--text-muted);
    font-size: 13px;
    line-height: 1.8;
}

.password-tips li {
    list-style-type: disc;
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

    .password-tips {
        text-align: left;
        padding-left: 16px;
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

    .password-tips {
        font-size: 12px;
    }

    .modal-actions .btn {
        font-size: 0.85rem;
        padding: 0.7rem;
    }
}
</style>