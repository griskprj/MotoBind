<template>
    <ModalWrapper
        :isOpen="isOpen"
        title="Редактирование обслуживания"
        subtitle="Измените данные о обслуживании"
        icon="wrench"
        size="md"
        @close="$emit('close')"
    >
        <form @submit.prevent="submit" class="edit-form">
            <!-- Выбор мотоцикла -->
            <div class="modal-form-group">
                <label>
                    Мотоцикл <span class="required">*</span>
                    <select v-model="form.motorcycleId">
                        <option value="">Выберите мотоцикл</option>
                        <option 
                            v-for="moto in motorcycles" 
                            :key="moto.id" 
                            :value="moto.id"
                        >
                            {{ moto.name }} ({{ moto.mileage || 0 }} км)
                        </option>
                    </select>
                </label>
            </div>

            <!-- Категория -->
            <div class="modal-form-group">
                <label>
                    Узел / Система <span class="required">*</span>
                    <select v-model="form.category" @change="onCategoryChange">
                        <option value="">Выберите категорию</option>
                        <option value="engine">Двигатель</option>
                        <option value="drive">Привод</option>
                        <option value="steering">Рулевое управление</option>
                        <option value="suspension">Подвеска</option>
                        <option value="electronics">Электроника</option>
                        <option value="wheel">Колеса / Шины</option>
                        <option value="brakes">Тормозная система</option>
                        <option value="fuel">Топливная система</option>
                        <option value="cooling">Система охлаждения</option>
                        <option value="other">Другое</option>
                    </select>
                </label>
            </div>

            <!-- Тип обслуживания (из шаблонов) -->
            <div v-if="templates.length > 0" class="modal-form-group">
                <label>
                    Тип обслуживания <span class="required">*</span>
                    <select v-model="form.templateId" @change="onTemplateChange">
                        <option value="">Выберите тип обслуживания</option>
                        <option v-for="tpl in templates" :key="tpl.id" :value="tpl.id">
                            {{ tpl.label }}
                        </option>
                    </select>
                </label>
            </div>

            <div v-if="!form.category || templates.length === 0 || form.category === 'other'" class="modal-form-group">
                <label>
                    Название обслуживания <span class="required">*</span>
                    <input
                        v-model="form.title"
                        type="text"
                        placeholder="Например: Замена масла"
                    />
                </label>
            </div>

            <!-- Описание -->
            <div class="modal-form-group">
                <label>Описание работы</label>
                <textarea 
                    v-model="form.description"
                    rows="2"
                    placeholder="Подробное описание работы"
                ></textarea>
            </div>

            <hr class="form-divider" />

            <!-- Плановые поля -->
            <div class="modal-form-row">
                <div class="modal-form-group">
                    <label>Плановый пробег (км)</label>
                    <input
                        v-model.number="form.planned_mileage"
                        type="number"
                        placeholder="15000"
                        min="0"
                    />
                </div>
                <div class="modal-form-group">
                    <label>Плановая дата</label>
                    <input
                        v-model="form.planned_date"
                        type="date"
                    />
                </div>
            </div>

            <!-- Выполненные поля -->
            <div class="modal-form-row">
                <div class="modal-form-group">
                    <label>Выполненный пробег (км)</label>
                    <input
                        v-model.number="form.completed_mileage"
                        type="number"
                        placeholder="15000"
                        min="0"
                    />
                </div>
                <div class="modal-form-group">
                    <label>Дата выполнения</label>
                    <input
                        v-model="form.completed_date"
                        type="date"
                    />
                </div>
            </div>

            <!-- Стоимость -->
            <div class="modal-form-group">
                <label>Стоимость (₽)</label>
                <input
                    v-model.number="form.cost"
                    type="number"
                    placeholder="5000"
                    min="0"
                />
            </div>

            <div class="modal-info-block info" style="margin-top: 12px;">
                <div class="modal-info-icon">
                    <i class="fa fa-info-circle"></i>
                </div>
                <p class="modal-info-text">
                    Если заполнены выполненные поля, статус изменится на "Выполнено".
                    Если заполнены плановые поля — статус будет "Запланировано".
                </p>
            </div>

            <!-- Действия -->
            <div class="modal-actions">
                <button type="button" class="btn btn-secondary" @click="$emit('close')">
                    Отмена
                </button>
                <button type="submit" class="btn btn-primary" :disabled="isSubmitting || !isFormValid">
                    <i v-if="isSubmitting" class="fa fa-spinner fa-spin"></i>
                    <span v-else><i class="fa fa-save"></i> Сохранить</span>
                </button>
            </div>
        </form>
    </ModalWrapper>
</template>

<script>
import api from '../../../api/api'
import ModalWrapper from '../ModalWrapper.vue'
import { getTemplatesByCategory } from '../../../constants/maintenanceTemplates'

export default {
    components: { ModalWrapper },

    props: {
        isOpen: {
            type: Boolean,
            required: true,
            default: false
        },
        maintenance: {
            type: Object,
            required: true,
            default: null
        },
        motorcycles: {
            type: Array,
            default: () => []
        }
    },

    emits: ['close', 'saved'],

    data() {
        return {
            form: {
                motorcycleId: null,
                category: '',
                templateId: '',
                title: '',
                description: '',
                planned_mileage: null,
                planned_date: null,
                completed_mileage: null,
                completed_date: null,
                cost: null
            },
            templates: [],
            isSubmitting: false,
            errors: {}
        }
    },

    computed: {
        isFormValid() {
            return this.form.motorcycleId && 
                   this.form.category && 
                   this.form.title &&
                   this.form.title.trim().length > 0
        }
    },

    watch: {
        maintenance: {
            immediate: true,
            handler(val) {
                if (val) {
                    this.fillForm(val)
                }
            }
        },
        'form.category'(newVal) {
            if (newVal) {
                this.templates = getTemplatesByCategory(newVal)
                if (this.form.templateId) {
                    const found = this.templates.find(t => t.id === this.form.templateId)
                    if (!found) {
                        this.form.templateId = ''
                    }
                }
            } else {
                this.templates = []
            }
        }
    },

    methods: {
        fillForm(maintenance) {
            this.form = {
                motorcycleId: maintenance.moto_id || maintenance.motorcycle_id || null,
                category: maintenance.category || '',
                templateId: '',
                title: maintenance.title || '',
                description: maintenance.description || '',
                planned_mileage: maintenance.planned_mileage || null,
                planned_date: maintenance.planned_date || null,
                completed_mileage: maintenance.completed_mileage || null,
                completed_date: maintenance.completed_date || null,
                cost: maintenance.cost || null
            }

            if (this.form.category) {
                this.templates = getTemplatesByCategory(this.form.category)
                
                const found = this.templates.find(t => t.label === this.form.title)
                if (found) {
                    this.form.templateId = found.id
                }
            }
        },

        onCategoryChange() {
            this.form.templateId = ''
            if (this.form.category) {
                this.templates = getTemplatesByCategory(this.form.category)
            } else {
                this.templates = []
            }
        },

        onTemplateChange() {
            const found = this.templates.find(t => t.id === this.form.templateId)
            if (found) {
                this.form.title = found.label
            }
        },

        async submit() {
            if (!this.isFormValid) {
                this.$toast?.warning('Заполните все обязательные поля')
                return
            }

            this.isSubmitting = true
            this.errors = {}

            try {
                if (this.form.completed_mileage && !this.form.completed_date) {
                    alert('Укажите дату выполнения')
                    return
                }
                const payload = {
                    maintenanceId: this.maintenance.id,
                    motorcycleId: this.form.motorcycleId,
                    category: this.form.category,
                    title: this.form.title.trim(),
                    description: this.form.description?.trim() || null,
                    planned_mileage: this.form.planned_mileage || null,
                    planned_date: this.form.planned_date || null,
                    completed_mileage: this.form.completed_mileage || null,
                    completed_date: this.form.completed_date || null,
                    cost: this.form.cost || null
                }

                await api.put(`/maintenance/${this.maintenance.id}`, payload)
                
                this.$emit('saved')
                this.$emit('close')
                this.$toast?.success('Обслуживание обновлено!')
            } catch (error) {
                console.error('Ошибка обновления:', error)
                this.errors = error
                const msg = error.response?.data?.message || 'Ошибка при обновлении'
                this.$toast?.error(msg)
            } finally {
                this.isSubmitting = false
            }
        }
    }
}
</script>

<style scoped>
.edit-form {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.modal-form-group {
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin-bottom: 14px;
}

.modal-form-group:last-child {
    margin-bottom: 0;
}

.modal-form-group label {
    display: flex;
    flex-direction: column;
    align-items: center;
    font-weight: 600;
    font-size: 0.85rem;
    color: var(--text-secondary);
}

.modal-form-group label .required {
    color: var(--danger-text);
    font-weight: 700;
}

.modal-form-group input,
.modal-form-group select,
.modal-form-group textarea {
    padding: 0.6rem 0.8rem;
    border-radius: 10px;
    border: 2px solid var(--border-color);
    background-color: var(--bg-input);
    color: var(--text-primary);
    font-size: 0.95rem;
    transition: all 0.2s;
    width: 100%;
    font-family: inherit;
    box-sizing: border-box;
}

.modal-form-group input:focus,
.modal-form-group select:focus,
.modal-form-group textarea:focus {
    border-color: var(--accent);
    outline: none;
    box-shadow: 0 0 0 3px var(--accent-trans);
}

.modal-form-group input::placeholder,
.modal-form-group textarea::placeholder {
    color: var(--text-muted);
}

.modal-form-group textarea {
    resize: vertical;
    min-height: 60px;
}

.modal-form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 14px;
}

.modal-form-row:last-child {
    margin-bottom: 0;
}

/* ===== РАЗДЕЛИТЕЛЬ ===== */
.form-divider {
    border: none;
    border-top: 1px solid var(--border-light);
    margin: 8px 0 14px;
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

.modal-info-block .modal-info-icon {
    font-size: 18px;
    flex-shrink: 0;
    margin-top: 2px;
    color: var(--accent-text);
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
    margin-top: 16px;
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
    opacity: 0.6;
    cursor: not-allowed;
}

.btn-primary {
    background: var(--accent);
    color: #fff;
}

.btn-primary:hover:not(:disabled) {
    background: var(--accent-hover);
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

.fa-spin {
    animation: fa-spin 1s linear infinite;
}

@keyframes fa-spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* ============================================ */
/* ===== АДАПТИВНОСТЬ ===== */
/* ============================================ */

@media (max-width: 640px) {
    .modal-form-row {
        grid-template-columns: 1fr;
        gap: 0;
    }

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
}

@media (max-width: 400px) {
    .modal-form-group input,
    .modal-form-group select,
    .modal-form-group textarea {
        font-size: 0.9rem;
        padding: 0.5rem 0.7rem;
    }
}
</style>