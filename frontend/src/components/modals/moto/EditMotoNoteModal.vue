<template>
    <ModalWrapper
        :isOpen="isOpen"
        title="Редактирование заметок"
        subtitle="Добавьте важную информацию о мотоцикле"
        icon="file"
        bg-icon-color="var(--accent-trans)"
        icon-color="var(--accent-text)"
        @close="$emit('close')"
    >
        <div class="modal-form-group">
            <label>
                Заметки
                <textarea
                    v-model="form.note"
                    maxlength="512"
                    rows="5"
                    placeholder="Введите заметки о мотоцикле..."
                ></textarea>
            </label>
            <div class="char-counter">
                {{ form.note?.length || 0 }} / 512
            </div>
        </div>

        <div class="modal-info-block info">
            <div class="modal-info-icon">
                <i class="fa fa-lightbulb"></i>
            </div>
            <p class="modal-info-text">
                Здесь можно хранить любую полезную информацию: особенности модели, 
                выполненные доработки, личные наблюдения, планы по обслуживанию и другое.
            </p>
        </div>

        <template #actions>
            <div class="modal-actions">
                <button class="btn btn-secondary" @click="$emit('close')">
                    Отменить
                </button>
                <button class="btn btn-primary" @click="submit" :disabled="loading">
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
            default: false,
            required: true
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
                note: ''
            },
            loading: false
        }
    },

    watch: {
        isOpen(newVal) {
            if (newVal && this.motorcycle) {
                this.loadFormData()
            }
            if (!newVal) {
                this.loading = false
            }
        },
        motorcycle: {
            handler(newVal) {
                if (this.isOpen && newVal) {
                    this.loadFormData()
                }
            },
            deep: true
        }
    },

    methods: {
        loadFormData() {
            if (!this.motorcycle) return
            this.form = {
                id: this.motorcycle.id,
                note: this.motorcycle.note || ''
            }
        },

        resetForm() {
            this.form = {
                id: null,
                note: ''
            }
            this.loading = false
        },

        async submit() {
            this.loading = true
            try {
                await this.$emit('submit', this.form)
                this.resetForm()
                this.$emit('close')
            } catch (error) {
                console.error('Submit error:', error)
                alert('Ошибка при сохранении заметки')
            } finally {
                this.loading = false
            }
        }
    }
}
</script>

<style scoped>
/* ===== TEXTAREA ===== */
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

.modal-form-group textarea {
    width: 100%;
    padding: 0.6rem 0.8rem;
    border-radius: 10px;
    border: 2px solid var(--border-color);
    background-color: var(--bg-input);
    color: var(--text-primary);
    font-size: 0.95rem;
    transition: all 0.2s;
    box-sizing: border-box;
    font-family: inherit;
    resize: vertical;
    min-height: 120px;
    line-height: 1.6;
}

.modal-form-group textarea:focus {
    border-color: var(--accent);
    outline: none;
    box-shadow: 0 0 0 3px var(--accent-trans);
}

.modal-form-group textarea::placeholder {
    color: var(--text-muted);
}

.char-counter {
    text-align: right;
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 4px;
    font-weight: 500;
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

    .modal-form-group textarea {
        font-size: 0.9rem;
        padding: 0.5rem 0.7rem;
        min-height: 100px;
    }

    .char-counter {
        font-size: 11px;
    }
}

@media (max-width: 400px) {
    .modal-form-group textarea {
        min-height: 80px;
        font-size: 0.85rem;
    }

    .modal-info-text {
        font-size: 13px;
    }
}
</style>