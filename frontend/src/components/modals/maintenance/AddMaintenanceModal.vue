<template>
    <ModalWrapper
        :isOpen="isOpen"
        :title="currentStepTitle"
        :subtitle="currentStepSubtitle"
        :icon="currentStepIcon"
        :bg-icon-color="currentStepIconBg"
        :icon-color="currentStepIconColor"
        size="md"
        @close="closeModal"
    >
        <!-- Шаг 1: Выбор типа -->
        <template v-if="currentStep === 1">
            <div 
                class="choice-card"
                :class="{ selected: selectedType === 'history' }"
                @click="selectType('history')"
            >
                <div class="choice-icon success">
                    <i class="fa fa-clock"></i>
                </div>
                <div class="choice-info">
                    <div class="choice-title">Добавить в историю</div>
                    <div class="choice-subtitle">Уже выполненное обслуживание</div>
                </div>
                <div class="choice-arrow">
                    <i class="fa fa-chevron-right"></i>
                </div>
            </div>

            <div 
                class="choice-card"
                :class="{ selected: selectedType === 'planned' }"
                @click="selectType('planned')"
            >
                <div class="choice-icon warning">
                    <i class="fa fa-calendar"></i>
                </div>
                <div class="choice-info">
                    <div class="choice-title">Запланировать</div>
                    <div class="choice-subtitle">Плановое обслуживание</div>
                </div>
                <div class="choice-arrow">
                    <i class="fa fa-chevron-right"></i>
                </div>
            </div>

            <div class="modal-info-block info">
                <div class="modal-info-icon">
                    <i class="fa fa-info-circle"></i>
                </div>
                <p class="modal-info-text">
                    Выберите тип обслуживания, которое хотите добавить
                </p>
            </div>
        </template>

        <!-- Шаг 2: Информация об обслуживании -->
        <template v-if="currentStep === 2">
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

            <!-- Ручной ввод названия (если нет шаблонов) -->
            <div v-if="!form.category || templates.length === 0" class="modal-form-group">
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
                <label>
                    Описание работы
                    <textarea 
                        v-model="form.description"
                        rows="2"
                        :placeholder="selectedType === 'history' 
                            ? 'Опишите, что было сделано...' 
                            : 'Опишите, что необходимо сделать...'"
                    ></textarea>
                </label>
            </div>

            <!-- Разделитель -->
            <hr class="form-divider" />

            <!-- Поля в зависимости от типа -->
            <template v-if="selectedType === 'history'">
                <div class="modal-form-group">
                    <label>
                        Пробег (км) <span class="required">*</span>
                        <input
                            v-model.number="form.mileage"
                            type="number"
                            placeholder="0"
                            min="0"
                            required
                        />
                    </label>
                </div>

                <div class="modal-form-row">
                    <div class="modal-form-group">
                        <label>
                            Стоимость (₽)
                            <input
                                v-model.number="form.cost"
                                type="number"
                                placeholder="0"
                                min="0"
                            />
                        </label>
                    </div>

                    <div class="modal-form-group">
                        <label>
                            Дата выполнения
                            <input
                                v-model="form.date"
                                type="date"
                                :max="currentDate"
                            />
                        </label>
                    </div>
                </div>

                <div class="modal-info-block success">
                    <div class="modal-info-icon">
                        <i class="fa fa-check-circle"></i>
                    </div>
                    <p class="modal-info-text">
                        Обслуживание будет добавлено в историю с указанными данными
                    </p>
                </div>
            </template>

            <template v-if="selectedType === 'planned'">
                <div class="modal-info-block info" style="margin-bottom: 14px;">
                    <div class="modal-info-icon">
                        <i class="fa fa-info-circle"></i>
                    </div>
                    <p class="modal-info-text">
                        Вы можете запланировать обслуживание по <strong>пробегу</strong> или по <strong>дате</strong>.
                        Заполните хотя бы одно поле.
                    </p>
                </div>

                <!-- Планирование по пробегу -->
                <div class="modal-form-group">
                    <label>
                        Плановый пробег (км)
                        <input
                            v-model.number="form.planned_mileage"
                            type="number"
                            placeholder="Например: 15000"
                            min="0"
                        />
                    </label>
                </div>

                <!-- ИЛИ -->
                <div class="or-divider">
                    <span>или</span>
                </div>

                <!-- Планирование по дате -->
                <div class="modal-form-group">
                    <label>
                        Плановая дата
                        <input
                            v-model="form.planned_date"
                            type="date"
                            :min="today"
                        />
                    </label>
                </div>

                <div class="modal-info-block info">
                    <div class="modal-info-icon">
                        <i class="fa fa-bell"></i>
                    </div>
                    <p class="modal-info-text">
                        Вы получите уведомление, когда наступит указанная дата или мотоцикл достигнет указанного пробега.
                    </p>
                </div>
            </template>
        </template>

        <!-- Шаг 3: Успех -->
        <template v-if="currentStep === 3">
            <div class="completion-step">
                <div class="completion-icon">
                    <i class="fa fa-check-circle"></i>
                </div>
                <h2 class="step-title">Готово!</h2>
                <p class="step-subtitle">
                    {{ selectedType === 'history' 
                        ? 'Обслуживание добавлено в историю' 
                        : 'Обслуживание запланировано' 
                    }}
                </p>

                <div class="summary-card">
                    <div class="summary-item">
                        <span class="summary-label">Мотоцикл</span>
                        <span class="summary-value">{{ getMotoName(form.motorcycleId) }}</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-label">Обслуживание</span>
                        <span class="summary-value">{{ form.title || '—' }}</span>
                    </div>
                    <div v-if="form.description" class="summary-item">
                        <span class="summary-label">Описание</span>
                        <span class="summary-value">{{ form.description }}</span>
                    </div>
                    <div v-if="selectedType === 'history' && form.mileage" class="summary-item">
                        <span class="summary-label">Пробег</span>
                        <span class="summary-value">{{ form.mileage }} км</span>
                    </div>
                    <div v-if="selectedType === 'history' && form.cost" class="summary-item">
                        <span class="summary-label">Стоимость</span>
                        <span class="summary-value">{{ form.cost }} ₽</span>
                    </div>
                    <div v-if="selectedType === 'planned' && form.planned_mileage" class="summary-item">
                        <span class="summary-label">Плановый пробег</span>
                        <span class="summary-value">{{ form.planned_mileage }} км</span>
                    </div>
                    <div v-if="selectedType === 'planned' && form.planned_date" class="summary-item">
                        <span class="summary-label">Плановая дата</span>
                        <span class="summary-value">{{ formatDate(form.planned_date) }}</span>
                    </div>
                </div>
            </div>
        </template>

        <!-- Действия -->
        <template #actions>
            <div class="step-actions">
                <button 
                    v-if="currentStep === 2"
                    class="btn btn-secondary" 
                    @click="prevStep"
                >
                    <i class="fa fa-arrow-left"></i> Назад
                </button>

                <button 
                    v-if="currentStep === 1"
                    class="btn btn-secondary" 
                    @click="closeModal"
                >
                    Отменить
                </button>

                <button 
                    v-if="currentStep === 1"
                    class="btn btn-primary" 
                    :disabled="!selectedType"
                    @click="nextStep"
                >
                    Продолжить <i class="fa fa-arrow-right"></i>
                </button>

                <button 
                    v-if="currentStep === 2"
                    class="btn btn-primary" 
                    :disabled="!isFormValid || loading"
                    @click="submit"
                >
                    <span v-if="!loading">
                        <i class="fa fa-save"></i> Сохранить
                    </span>
                    <span v-else>
                        <i class="fa fa-spinner fa-spin"></i> Сохранение...
                    </span>
                </button>

                <button 
                    v-if="currentStep === 3"
                    class="btn btn-success" 
                    @click="closeModal"
                >
                    <i class="fa fa-check"></i> Закрыть
                </button>
            </div>
        </template>
    </ModalWrapper>
</template>

<script>
import ModalWrapper from '../ModalWrapper.vue'
import { getTemplatesByCategory } from '../../../constants/maintenanceTemplates'

export default {
    components: { ModalWrapper },

    props: {
        isOpen: {
            type: Boolean,
            default: false
        },
        motorcycles: {
            type: Array,
            default: () => []
        }
    },

    data() {
        return {
            currentStep: 1,
            selectedType: null,
            form: {
                motorcycleId: null,
                category: '',
                templateId: '',
                title: '',
                description: '',
                cost: null,
                mileage: null,
                date: null,
                planned_mileage: null,
                planned_date: null
            },
            templates: [],
            currentDate: new Date().toISOString().split('T')[0],
            loading: false
        }
    },

    computed: {
        today() {
            return new Date().toISOString().split('T')[0]
        },

        currentStepTitle() {
            const titles = {
                1: 'Добавить обслуживание',
                2: this.selectedType === 'history' ? 'Добавить в историю' : 'Запланировать обслуживание',
                3: 'Готово!'
            }
            return titles[this.currentStep] || 'Добавить обслуживание'
        },

        currentStepSubtitle() {
            const subtitles = {
                1: 'Выберите, что хотите сделать',
                2: this.selectedType === 'history' 
                    ? 'Заполните информацию о выполненной работе' 
                    : 'Заполните информацию о плановом обслуживании',
                3: ''
            }
            return subtitles[this.currentStep] || ''
        },

        currentStepIcon() {
            const icons = {
                1: 'wrench',
                2: this.selectedType === 'history' ? 'clipboard-list' : 'calendar-plus',
                3: 'check-circle'
            }
            return icons[this.currentStep] || 'wrench'
        },

        currentStepIconBg() {
            if (this.currentStep === 3) return 'var(--success-trans)'
            if (this.currentStep === 2 && this.selectedType === 'history') return 'var(--success-trans)'
            if (this.currentStep === 2 && this.selectedType === 'planned') return 'var(--warning-trans)'
            return 'var(--accent-trans)'
        },

        currentStepIconColor() {
            if (this.currentStep === 3) return 'var(--success-text)'
            if (this.currentStep === 2 && this.selectedType === 'history') return 'var(--success-text)'
            if (this.currentStep === 2 && this.selectedType === 'planned') return 'var(--warning-text)'
            return 'var(--accent-text)'
        },

        isFormValid() {
            const baseValid = this.form.motorcycleId && 
                             this.form.category && 
                             this.form.title

            if (this.selectedType === 'history') {
                return baseValid && this.form.mileage && this.form.mileage > 0
            }

            if (this.selectedType === 'planned') {
                const hasPlanned = (this.form.planned_mileage && this.form.planned_mileage > 0) ||
                                   this.form.planned_date
                return baseValid && hasPlanned
            }

            return false
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
        formatDate(dateString) {
            if (!dateString) return '—'
            try {
                const date = new Date(dateString)
                if (isNaN(date.getTime())) return '—'
                return date.toLocaleDateString('ru-RU', {
                    day: '2-digit',
                    month: 'short',
                    year: 'numeric'
                })
            } catch {
                return '—'
            }
        },

        getMotoName(id) {
            const moto = this.motorcycles.find(m => m.id === id)
            return moto ? moto.name : '—'
        },

        selectType(type) {
            this.selectedType = type
        },

        onCategoryChange() {
            this.form.templateId = ''
            this.form.title = ''
            this.templates = this.form.category ? getTemplatesByCategory(this.form.category) : []
        },

        onTemplateChange() {
            const found = this.templates.find(t => t.id === this.form.templateId)
            this.form.title = found ? found.label : ''
        },

        nextStep() {
            if (this.currentStep < 3) {
                this.currentStep++
            }
        },

        prevStep() {
            if (this.currentStep > 1) {
                this.currentStep--
            }
        },

        closeModal() {
            this.$emit('close')
        },

        resetForm() {
            this.currentStep = 1
            this.selectedType = null
            this.form = {
                motorcycleId: null,
                category: '',
                templateId: '',
                title: '',
                description: '',
                cost: null,
                mileage: null,
                date: null,
                planned_mileage: null,
                planned_date: null
            }
            this.templates = []
            this.loading = false
        },

        async submit() {
            this.loading = true
            try {
                let payload = {
                    motorcycleId: this.form.motorcycleId,
                    title: this.form.title,
                    category: this.form.category,
                    description: this.form.description || ''
                }

                if (this.selectedType === 'history') {
                    payload = {
                        ...payload,
                        cost: this.form.cost || null,
                        completed_mileage: this.form.mileage,
                        completed_date: this.form.date || null
                    }
                } else {
                    payload = {
                        ...payload,
                        planned_mileage: this.form.planned_mileage || null,
                        planned_date: this.form.planned_date || null
                    }
                }

                await this.$emit('submit', payload)
                this.nextStep()
            } catch (error) {
                console.error('Submit error:', error)
                alert('Ошибка при сохранении')
            } finally {
                this.loading = false
            }
        }
    }
}
</script>

<style scoped>
/* ===== КАРТОЧКИ ВЫБОРА ===== */
.choice-card {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px 20px;
    background: var(--bg-secondary);
    border: 2px solid transparent;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s;
    margin-bottom: 12px;
}

.choice-card:hover {
    background: var(--bg-card-hover);
    transform: translateY(-2px);
}

.choice-card.selected {
    border-color: var(--accent);
    background: var(--accent-trans);
    box-shadow: 0 0 0 2px var(--accent-trans);
}

.choice-icon {
    width: 44px;
    height: 44px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}

.choice-icon.success {
    background: var(--success-trans);
    color: var(--success-text);
}

.choice-icon.warning {
    background: var(--warning-trans);
    color: var(--warning-text);
}

.choice-info {
    flex: 1;
}

.choice-title {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
}

.choice-subtitle {
    font-size: 13px;
    color: var(--text-secondary);
}

.choice-arrow {
    color: var(--text-muted);
    font-size: 16px;
}

/* ===== РАЗДЕЛИТЕЛЬ "ИЛИ" ===== */
.or-divider {
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 8px 0 12px;
    color: var(--text-muted);
}

.or-divider::before,
.or-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border-color);
}

.or-divider span {
    font-size: 13px;
    font-weight: 500;
    padding: 0 8px;
    color: var(--text-muted);
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

.modal-form-group input,
.modal-form-group select,
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
}

.form-divider {
    border: none;
    border-top: 1px solid var(--border-light);
    margin: 16px 0;
}

/* ===== ИНФО-БЛОКИ ===== */
.modal-info-block {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
    border-radius: 10px;
    margin: 12px 0;
}

.modal-info-block.info {
    background: var(--accent-trans);
    border: 1px solid var(--accent-light);
}

.modal-info-block.success {
    background: var(--success-trans);
    border: 1px solid rgba(16, 185, 129, 0.2);
}

.modal-info-block.warning {
    background: var(--warning-trans);
    border: 1px solid rgba(245, 158, 11, 0.2);
}

.modal-info-block .modal-info-icon {
    font-size: 18px;
    flex-shrink: 0;
    margin-top: 2px;
}

.modal-info-block.info .modal-info-icon {
    color: var(--accent-text);
}

.modal-info-block.success .modal-info-icon {
    color: var(--success-text);
}

.modal-info-block.warning .modal-info-icon {
    color: var(--warning-text);
}

.modal-info-text {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.5;
}

/* ===== КНОПКИ ===== */
.step-actions {
    display: flex;
    gap: 10px;
}

.step-actions .btn {
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
    gap: 6px;
}

.step-actions .btn:disabled {
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

.btn-success {
    background: linear-gradient(135deg, var(--success), var(--success-hover));
    color: #fff;
}

.btn-success:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px var(--success-trans);
}

/* ===== ФИНАЛЬНЫЙ ШАГ ===== */
.completion-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 16px 4px;
    text-align: center;
}

.completion-icon {
    font-size: 56px;
    color: var(--success-text);
    margin-bottom: 12px;
}

.completion-step .step-title {
    font-size: 22px;
    font-weight: 700;
    margin: 0 0 4px 0;
    color: var(--text-primary);
}

.completion-step .step-subtitle {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0 0 16px 0;
}

.summary-card {
    background: var(--bg-secondary);
    border-radius: 12px;
    padding: 16px;
    width: 100%;
    border: 1px solid var(--border-light);
}

.summary-item {
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    border-bottom: 1px solid var(--border-light);
}

.summary-item:last-child {
    border-bottom: none;
}

.summary-label {
    font-size: 13px;
    color: var(--text-muted);
}

.summary-value {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-primary);
    text-align: right;
    max-width: 60%;
    word-break: break-word;
}

/* ============================================ */
/* ===== АДАПТИВНОСТЬ ===== */
/* ============================================ */

@media (max-width: 640px) {
    .choice-card {
        padding: 14px 16px;
    }

    .choice-icon {
        width: 38px;
        height: 38px;
        font-size: 16px;
    }

    .modal-form-row {
        grid-template-columns: 1fr;
        gap: 0;
    }

    .step-actions {
        flex-direction: column;
    }

    .step-actions .btn {
        width: 100%;
        padding: 0.8rem;
    }

    .summary-item {
        flex-direction: column;
        align-items: center;
        gap: 2px;
        text-align: center;
    }

    .summary-value {
        max-width: 100%;
        text-align: center;
    }

    .completion-icon {
        font-size: 44px;
    }

    .completion-step .step-title {
        font-size: 20px;
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
    .choice-card {
        padding: 12px 14px;
    }

    .choice-icon {
        width: 34px;
        height: 34px;
        font-size: 14px;
    }

    .modal-form-group input,
    .modal-form-group select,
    .modal-form-group textarea {
        font-size: 0.9rem;
        padding: 0.5rem 0.7rem;
    }

    .completion-icon {
        font-size: 38px;
    }

    .completion-step .step-title {
        font-size: 18px;
    }
}
</style>