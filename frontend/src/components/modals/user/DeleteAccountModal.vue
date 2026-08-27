<template>
    <ModalWrapper
        :isOpen="isOpen"
        title="Удаление аккаунта"
        subtitle="Это действие нельзя отменить. Все данные будут удалены безвозвратно"
        icon="user-slash"
        bg-icon-color="var(--danger-trans)"
        icon-color="var(--danger-text)"
        @close="$emit('close')"
    >
        <!-- Предупреждение -->
        <div class="modal-info-block danger">
            <div class="modal-info-icon">
                <i class="fa fa-exclamation-triangle"></i>
            </div>
            <div>
                <p class="modal-info-text" style="font-weight: 600; color: var(--danger-text);">
                    Вы уверены, что хотите удалить аккаунт?
                </p>
                <p class="modal-info-text">
                    Будут удалены все ваши данные: мотоциклы, записи об обслуживании, 
                    мануалы, фотографии и личная информация. Восстановление невозможно.
                </p>
            </div>
        </div>

        <!-- Поле для пароля -->
        <div class="modal-form-group danger-input">
            <label>
                Введите пароль для подтверждения <span class="required">*</span>
                <input
                    v-model="password"
                    type="password"
                    placeholder="Введите текущий пароль"
                    required
                    @keydown.enter="submit"
                />
            </label>
        </div>

        <template #actions>
            <div class="modal-actions">
                <button class="btn btn-secondary" @click="$emit('close')">
                    Отменить
                </button>
                <button 
                    class="btn btn-danger" 
                    :disabled="!password || password.length < 6 || loading"
                    @click="submit"
                >
                    <span v-if="!loading">
                        <i class="fa fa-trash"></i> Удалить аккаунт
                    </span>
                    <span v-else>
                        <i class="fa fa-spinner fa-spin"></i> Удаление...
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
            default: false,
            required: true
        }
    },

    data() {
        return {
            password: '',
            loading: false
        }
    },

    watch: {
        isOpen(newVal) {
            if (!newVal) {
                this.password = ''
                this.loading = false
            }
        }
    },

    methods: {
        resetForm() {
            this.password = ''
            this.loading = false
        },

        async submit() {
            if (!this.password || this.password.length < 6) {
                alert('Введите корректный пароль (минимум 6 символов)')
                return
            }

            if (!confirm('Вы действительно хотите удалить аккаунт? Это действие нельзя отменить!')) {
                return
            }

            this.loading = true

            try {
                await this.$emit('submit', this.password)
                this.resetForm()
                this.$emit('close')
            } catch (error) {
                console.error('Submit error:', error)
                alert('Ошибка при удалении аккаунта. Проверьте пароль.')
            } finally {
                this.loading = false
            }
        }
    }
}
</script>

<style scoped>
/* ===== ИНФО-БЛОК ===== */
.modal-info-block {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 14px 16px;
    border-radius: 10px;
    margin-bottom: 16px;
}

.modal-info-block.danger {
    background: var(--danger-trans);
    border: 1px solid rgba(239, 68, 68, 0.2);
}

.modal-info-icon {
    font-size: 20px;
    color: var(--danger-text);
    flex-shrink: 0;
    margin-top: 2px;
}

.modal-info-text {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.5;
}

/* ===== ПОЛЕ ПАРОЛЯ ===== */
.modal-form-group {
    margin-bottom: 14px;
}

.modal-form-group.danger-input {
    padding: 14px 16px;
    background-color: var(--danger-trans);
    border: 2px solid rgba(239, 68, 68, 0.3);
    border-radius: 10px;
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
    border-color: var(--danger);
    outline: none;
    box-shadow: 0 0 0 3px var(--danger-trans);
}

.modal-form-group input::placeholder {
    color: var(--text-muted);
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

.btn-danger {
    background: var(--danger);
    color: #fff;
}

.btn-danger:hover:not(:disabled) {
    background: var(--danger-hover);
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(239, 68, 68, 0.3);
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

    .modal-form-group.danger-input {
        padding: 12px 14px;
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