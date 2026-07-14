<template>
    <div class="container">
        <section class="section">
            <div class="section-header">
                <div class="section-title-wrapper">
                    <i class="fa fa-wrench"></i>
                    <h2>Создайте мануал по обслуживанию</h2>
                </div>
                <p class="subtitle">Мануал должен соответствовать стандарту сервиса. Подробнее о правилах написания мануала вы можете узнать <a href="#">здесь</a></p>
            </div>
        </section>

        <section class="section">
            <div class="section-title-wrapper">
                <i class="fa fa-pen"></i>
                <h2>Конструктор</h2>
            </div>

            <div class="section-body">
                <form @submit.prevent="submitManual">
                    <!-- Основная информация -->
                    <div class="form-group">
                        <label>
                            Название*
                            <input 
                                type="text" 
                                v-model="form.title" 
                                required
                                placeholder="Например: Замена масла в двигателе"
                                :class="{ 'error': errors.title }"
                            >
                            <span v-if="errors.title" class="error-message">{{ errors.title }}</span>
                        </label>
                    </div>

                    <div class="form-group">
                        <label>
                            Описание*
                            <input 
                                type="text" 
                                v-model="form.description" 
                                required
                                placeholder="Краткое описание процедуры"
                                :class="{ 'error': errors.description }"
                            >
                            <span v-if="errors.description" class="error-message">{{ errors.description }}</span>
                        </label>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label>
                                Категория
                                <select v-model="form.category">
                                    <option value="">Выберите категорию</option>
                                    <option value="engine">Двигатель</option>
                                    <option value="drive">Привод</option>
                                    <option value="steering">Рулевое управление</option>
                                    <option value="suspension">Подвеска</option>
                                    <option value="electronics">Электроника</option>
                                    <option value="wheel">Колеса/Шины</option>
                                    <option value="brakes">Тормозная система</option>
                                    <option value="fuel">Топливная система</option>
                                    <option value="cooling">Система охлаждения</option>
                                </select>
                            </label>
                        </div>

                        <div class="form-group">
                            <label>
                                Сложность
                                <select v-model="form.difficult">
                                    <option value="">Выберите сложность</option>
                                    <option value="easy">Легко</option>
                                    <option value="medium">Средне</option>
                                    <option value="hard">Сложно</option>
                                </select>
                            </label>
                        </div>
                    </div>

                    <div class="form-group">
                        <label>
                            Модель мотоцикла*
                            <input 
                                type="text" 
                                v-model="form.motorcycle" 
                                required
                                placeholder="Например: BMW S1000RR"
                                :class="{ 'error': errors.motorcycle }"
                            >
                            <span v-if="errors.motorcycle" class="error-message">{{ errors.motorcycle }}</span>
                        </label>
                    </div>

                    <div class="form-group">
                        <label>
                            Инструменты (через запятую)
                            <input 
                                type="text" 
                                v-model="form.instruments" 
                                placeholder="Ключ на 18мм, ветошь, динамометрический ключ"
                            >
                        </label>
                    </div>

                    <div class="form-group">
                        <label>
                            Материалы и запчасти (через запятую)
                            <input 
                                type="text" 
                                v-model="form.parts" 
                                placeholder="Масло моторное 10W-40, масляный фильтр, прокладка"
                            >
                        </label>
                    </div>

                    <div class="section-sep">
                        <hr>
                    </div>

                    <!-- Шаги -->
                    <div class="steps-header">
                        <div class="steps-header-left">
                            <i class="fa fa-list-ol"></i>
                            <h3>Шаги инструкции</h3>
                            <span class="steps-count">{{ form.steps.length }} шаг(ов)</span>
                        </div>
                        <button type="button" class="btn-add-step" @click="addStep">
                            <i class="fa fa-plus"></i> Добавить шаг
                        </button>
                    </div>

                    <div v-if="form.steps.length === 0" class="empty-state">
                        <i class="fa fa-hand-pointer"></i>
                        <p>Нажмите "Добавить шаг", чтобы создать инструкцию</p>
                    </div>

                    <div v-for="(step, index) in form.steps" :key="step.id" class="step-card">
                        <div class="step-header">
                            <span class="step-number">Шаг {{ index + 1 }}</span>
                            <button type="button" class="btn-remove-step" @click="removeStep(index)">
                                <i class="fa fa-times"></i>
                            </button>
                        </div>
                        <div class="step-content">
                            <div class="form-group">
                                <label>
                                    Заголовок шага*
                                    <input 
                                        type="text" 
                                        v-model="step.title" 
                                        required
                                        :placeholder="`Что нужно сделать на шаге ${index + 1}?`"
                                        :class="{ 'error': step.errors && step.errors.title }"
                                    >
                                    <span v-if="step.errors && step.errors.title" class="error-message">{{ step.errors.title }}</span>
                                </label>
                            </div>
                            <div class="form-group">
                                <label>
                                    Описание шага
                                    <textarea 
                                        v-model="step.text" 
                                        rows="3"
                                        :placeholder="`Подробное описание шага ${index + 1}`"
                                    ></textarea>
                                </label>
                            </div>
                        </div>
                    </div>

                    <!-- Кнопки отправки -->
                    <div class="form-actions">
                        <button type="button" class="btn btn-secondary" @click="resetForm">Отменить</button>
                        <button type="submit" class="btn" :disabled="isSubmitting">
                            <i v-if="isSubmitting" class="fa fa-spinner fa-spin"></i>
                            <span v-else><i class="fa fa-check"></i> Создать мануал</span>
                        </button>
                    </div>
                </form>
            </div>
        </section>
    </div>
</template>

<script>
import api from '../api/api';

export default {
    name: 'ManualCreator',
    data() {
        return {
            form: {
                title: '',
                description: '',
                category: '',
                difficult: '',
                motorcycle: '',
                instruments: '',
                parts: '',
                steps: []
            },
            errors: {},
            isSubmitting: false,
            stepIdCounter: 0
        };
    },
    methods: {
        addStep() {
            this.form.steps.push({
                id: ++this.stepIdCounter,
                title: '',
                text: '',
                errors: {}
            });
        },
        removeStep(index) {
            if (this.form.steps.length <= 1) {
                alert('Мануал должен содержать хотя бы один шаг');
                return;
            }
            this.form.steps.splice(index, 1);
            this.form.steps.forEach((step, idx) => {
                step.id = idx + 1;
            });
        },
        validateForm() {
            this.errors = {};
            let isValid = true;

            if (!this.form.title || this.form.title.trim().length < 3) {
                this.errors.title = 'Название должно содержать минимум 3 символа';
                isValid = false;
            }

            if (!this.form.description || this.form.description.trim().length < 10) {
                this.errors.description = 'Описание должно содержать минимум 10 символов';
                isValid = false;
            }

            if (!this.form.motorcycle || this.form.motorcycle.trim().length < 2) {
                this.errors.motorcycle = 'Укажите модель мотоцикла';
                isValid = false;
            }

            this.form.steps.forEach((step, index) => {
                step.errors = {};
                if (!step.title || step.title.trim().length < 2) {
                    step.errors.title = 'Заголовок шага обязателен';
                    isValid = false;
                }
            });

            if (this.form.steps.length === 0) {
                isValid = false;
            }

            return isValid;
        },
        async submitManual() {
            if (!this.validateForm()) {
                const firstError = document.querySelector('.error');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstError.focus();
                }
                return;
            }

            this.isSubmitting = true;

            try {
                const payload = {
                    title: this.form.title.trim(),
                    description: this.form.description.trim(),
                    category: this.form.category || 'general',
                    difficult: this.form.difficult || 'easy',
                    motorcycle: this.form.motorcycle.trim(),
                    instruments: this.form.instruments.trim() || null,
                    parts: this.form.parts.trim() || null,
                    steps: this.form.steps.map((step, index) => ({
                        order: index + 1,
                        title: step.title.trim(),
                        text: step.text.trim() || null
                    }))
                };

                const response = await api.post('/manual/new-manual', payload, {
                });

                if (response.status === 201) {
                    this.$emit('manual-created', response.data);
                    alert('Мануал успешно создан!');
                    this.resetForm();
                }
            } catch (error) {
                console.error('Ошибка создания мануала:', error);
                
                let errorMessage = 'Произошла ошибка при создании мануала';
                if (error.response?.data?.message) {
                    errorMessage = error.response.data.message;
                } else if (error.response?.data?.error) {
                    errorMessage = error.response.data.error;
                } else if (error.message) {
                    errorMessage = error.message;
                }
                
                alert(`Ошибка: ${errorMessage}`);
            } finally {
                this.isSubmitting = false;
            }
        },
        resetForm() {
            this.form = {
                title: '',
                description: '',
                category: '',
                difficult: '',
                motorcycle: '',
                instruments: '',
                parts: '',
                steps: []
            };
            this.errors = {};
            this.stepIdCounter = 0;
            this.addStep();
        }
    },
    mounted() {
        this.addStep();
    }
};
</script>

<style scoped>
/* Контейнер использует глобальный стиль .container */
/* Настройки секции */
.section {
    background-color: var(--bg-primary);
    border: 2px solid var(--border-color);
    border-radius: 25px;
    padding: 28px;
    margin-bottom: 32px;
}

.section-header {
    text-align: center;
}

.section-title-wrapper {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 24px;
    margin-bottom: 16px;
}

.section-title-wrapper i {
    font-size: 32px;
    color: var(--accent);
}

.section-title-wrapper h2 {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
}

.subtitle {
    color: var(--text-secondary);
    font-size: 0.95rem;
    margin: 0;
    text-align: center;
}

.subtitle a {
    color: var(--accent);
    text-decoration: none;
}

.subtitle a:hover {
    color: var(--accent-hover);
    text-decoration: underline;
}

.section-body {
    margin-top: 24px;
}

/* Форма */
.form-group {
    margin-bottom: 20px;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.form-group label {
    display: block;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 6px;
    font-size: 0.875rem;
}

.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 0.625rem 0.75rem;
    font-size: 0.875rem;
    font-family: inherit;
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius);
    color: var(--text-primary);
    transition: border 0.2s, box-shadow 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2);
}

.form-group input.error,
.form-group textarea.error {
    border-color: var(--danger);
}

.form-group input.error:focus,
.form-group textarea.error:focus {
    box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.2);
}

.form-group textarea {
    resize: vertical;
    min-height: 60px;
}

.error-message {
    display: block;
    color: var(--danger);
    font-size: 0.8rem;
    margin-top: 4px;
}

/* Разделитель */
.section-sep {
    width: 100%;
    display: flex;
    justify-content: center;
    margin: 24px 0;
}

.section-sep hr {
    width: 60%;
    border: none;
    border-top: 1px solid var(--border-color);
}

/* Шаги */
.steps-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding: 12px 16px;
    background-color: var(--bg-secondary);
    border-radius: var(--radius);
    border: 1px solid var(--border-color);
}

.steps-header-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.steps-header-left i {
    font-size: 20px;
    color: var(--accent);
}

.steps-header-left h3 {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
}

.steps-count {
    font-size: 0.8rem;
    color: var(--text-muted);
    background-color: var(--bg-card);
    padding: 2px 10px;
    border-radius: 20px;
    border: 1px solid var(--border-color);
}

.btn-add-step {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
    font-weight: 500;
    line-height: 1;
    border-radius: var(--radius);
    border: 1px solid transparent;
    cursor: pointer;
    transition: all 0.3s;
    background-color: var(--accent);
    color: white;
    white-space: nowrap;
}

.btn-add-step:hover {
    background-color: var(--accent-hover);
    transform: translateY(-2px);
}

.btn-add-step:active {
    transform: translateY(0);
}

/* Пустое состояние */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 48px;
    background-color: var(--bg-secondary);
    border-radius: 24px;
    border: 2px dashed var(--border-color);
    text-align: center;
}

.empty-state i {
    font-size: 32px;
    color: var(--accent);
    margin-bottom: 12px;
}

.empty-state p {
    font-size: 18px;
    color: var(--text-secondary);
    font-style: italic;
    margin-bottom: 0;
}

/* Карточка шага */
.step-card {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius);
    padding: 20px;
    margin-bottom: 16px;
    transition: border-color 0.2s;
}

.step-card:hover {
    border-color: var(--accent);
}

.step-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.step-number {
    font-weight: 600;
    font-size: 0.9rem;
    color: var(--accent);
    background-color: var(--accent-light);
    padding: 4px 14px;
    border-radius: 20px;
    border: 1px solid var(--border-color);
}

.btn-remove-step {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 6px 10px;
    border-radius: 6px;
    transition: all 0.2s ease;
    font-size: 16px;
}

.btn-remove-step:hover {
    background-color: rgba(239, 68, 68, 0.1);
    color: var(--danger);
}

.step-content .form-group {
    margin-bottom: 12px;
}

.step-content .form-group:last-child {
    margin-bottom: 0;
}

/* Кнопки действий */
.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 28px;
    padding-top: 20px;
    border-top: 1px solid var(--border-color);
}

/* Глобальные кнопки переопределены через .btn */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.625rem 1.25rem;
    font-size: 0.875rem;
    font-weight: 500;
    line-height: 1;
    border-radius: var(--radius);
    border: 1px solid transparent;
    cursor: pointer;
    transition: all 0.3s;
    background-color: var(--accent);
    color: white;
    white-space: nowrap;
}

.btn:hover:not(:disabled) {
    background-color: var(--accent-hover);
    transform: translateY(-2px);
}

.btn:active:not(:disabled) {
    transform: translateY(0);
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
}

.btn-secondary {
    background-color: var(--bg-secondary);
    border-color: var(--border-color);
    color: var(--text-primary);
}

.btn-secondary:hover:not(:disabled) {
    background-color: var(--border-color);
}

/* Анимация спиннера */
.fa-spin {
    animation: fa-spin 1s linear infinite;
}

@keyframes fa-spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Адаптивность */
@media (max-width: 768px) {
    .section {
        padding: 20px;
    }

    .section-title-wrapper {
        flex-direction: column;
        text-align: center;
        gap: 12px;
    }

    .section-title-wrapper i {
        font-size: 28px;
    }

    .section-title-wrapper h2 {
        font-size: 1.25rem;
    }

    .form-row {
        grid-template-columns: 1fr;
        gap: 0;
    }

    .steps-header {
        flex-direction: column;
        gap: 12px;
        align-items: stretch;
        text-align: center;
    }

    .steps-header-left {
        justify-content: center;
    }

    .form-actions {
        flex-direction: column-reverse;
    }

    .form-actions .btn {
        width: 100%;
        justify-content: center;
    }

    .step-card {
        padding: 16px;
    }
}

@media (max-width: 480px) {
    .section {
        padding: 16px;
    }

    .empty-state {
        padding: 32px 20px;
    }

    .empty-state i {
        font-size: 28px;
    }

    .empty-state p {
        font-size: 16px;
    }

    .btn-add-step {
        font-size: 0.8rem;
        padding: 0.4rem 0.8rem;
    }
}
</style>