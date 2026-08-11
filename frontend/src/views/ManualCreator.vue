<template>
    <div class="container">
        <!-- === HEADER === -->
        <Header
            title="Конструктор мануалов"
            subtitle="Конструктор для создания мануалов"
        />

        <!-- === FORM === -->
        <section class="form-section">
            <p>Правила оформления мануалов <a href='/manual/rules' target='_blank'>здесь</a>.</p>
            <form @submit.prevent="submitManual">
                <!-- Основная информация -->
                <div class="form-card">
                    <div class="form-card-header">
                        <i class="fa fa-info-circle"></i>
                        <h3>Основная информация</h3>
                    </div>

                    <div class="form-card-body">
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

                        <div class="form-group">
                            <label>
                                Совет к мануалу
                                <input
                                    type="text"
                                    v-model="form.tip"
                                    placeholder="Напишите совет по выполнению мануала"    
                                >
                            </label>
                        </div>
                    </div>
                </div>

                <!-- Шаги -->
                <div class="form-card">
                    <div class="form-card-header">
                        <i class="fa fa-list-ol"></i>
                        <h3>Шаги инструкции</h3>
                        <span class="steps-count">{{ form.steps.length }} шаг(ов)</span>
                    </div>

                    <div class="form-card-body">
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
                                <div class="form-group">
                                    <label>
                                        Предупреждение
                                        <input 
                                            type="text"
                                            v-model="step.warning"
                                            placeholder="Предупреждение к шагу"
                                        >
                                    </label>
                                </div>
                                <div class="form-group">
                                    <label>
                                        Совет
                                        <input 
                                            type="text"
                                            v-model="step.tip"
                                            placeholder="Совет к шагу"
                                        >
                                    </label>
                                </div>
                            </div>
                        </div>

                        <button type="button" class="btn-add-step" @click="addStep">
                            <i class="fa fa-plus"></i> Добавить шаг
                        </button>
                    </div>
                </div>

                <!-- Кнопки отправки -->
                <div class="form-actions">
                    <button type="button" class="btn btn-secondary" @click="resetForm">Отменить</button>
                    <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
                        <i v-if="isSubmitting" class="fa fa-spinner fa-spin"></i>
                        <span v-else><i class="fa fa-check"></i> Создать мануал</span>
                    </button>
                </div>
            </form>
        </section>
    </div>
</template>

<script>
import api from '../api/api';
import Header from '../components/Header.vue';

export default {
    name: 'ManualCreator',
    components: { Header },
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
                tip: '',
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
                    tip: this.form.tip.trim() || null,
                    steps: this.form.steps.map((step, index) => ({
                        order: index + 1,
                        title: step.title.trim(),
                        warning: step.warning.trim() || null,
                        tip: step.tip.trim() || null,
                        text: step.text.trim() || null
                    }))
                };

                const response = await api.post('/manual/new-manual', payload);

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
        },

        async logout() {
            try {
                await api.post('/auth/logout');
            } catch(err) { console.error(err) }
            finally {
                const { removeTokens } = await import('../api/auth');
                removeTokens();
                this.$router.push('/login');
            }
        }
    },
    mounted() {
        this.addStep();
    }
};
</script>

<style scoped>
/* ===== FORM SECTION ===== */
.form-section {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

/* ===== FORM CARD ===== */
.form-card {
    background: var(--bg-card);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 16px;
}

.form-card-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 20px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    background: rgba(255,255,255,0.02);
}

.form-card-header i {
    font-size: 18px;
    color: var(--accent);
}

.form-card-header h3 {
    font-size: 16px;
    font-weight: 600;
    margin: 0;
}

.steps-count {
    margin-left: auto;
    font-size: 13px;
    color: var(--text-secondary);
    background: rgba(255,255,255,0.05);
    padding: 2px 12px;
    border-radius: 20px;
}

.form-card-body {
    padding: 20px;
}

/* ===== FORM ELEMENTS ===== */
.form-group {
    margin-bottom: 16px;
}

.form-group:last-child {
    margin-bottom: 0;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}

.form-group label {
    display: block;
    font-weight: 500;
    color: var(--text-secondary);
    margin-bottom: 6px;
    font-size: 14px;
}

.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 10px 14px;
    font-size: 14px;
    font-family: inherit;
    background: var(--bg-secondary);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    color: var(--text-primary);
    transition: all 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.15);
}

.form-group input::placeholder,
.form-group textarea::placeholder {
    color: var(--text-muted);
}

.form-group input.error,
.form-group textarea.error {
    border-color: var(--danger);
}

.form-group input.error:focus,
.form-group textarea.error:focus {
    box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.15);
}

.form-group textarea {
    resize: vertical;
    min-height: 60px;
}

.error-message {
    display: block;
    color: var(--danger);
    font-size: 13px;
    margin-top: 4px;
}

/* ===== STEPS ===== */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px;
    background: var(--bg-secondary);
    border-radius: 12px;
    border: 2px dashed rgba(255,255,255,0.06);
    text-align: center;
    margin-bottom: 16px;
}

.empty-state i {
    font-size: 32px;
    color: var(--accent);
    margin-bottom: 12px;
}

.empty-state p {
    font-size: 16px;
    color: var(--text-secondary);
    margin: 0;
}

.step-card {
    background: var(--bg-secondary);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    transition: border-color 0.2s;
}

.step-card:hover {
    border-color: rgba(124, 58, 237, 0.3);
}

.step-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}

.step-number {
    font-weight: 600;
    font-size: 14px;
    color: var(--accent);
    background: rgba(124, 58, 237, 0.12);
    padding: 2px 14px;
    border-radius: 20px;
}

.btn-remove-step {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 6px;
    transition: all 0.2s;
    font-size: 16px;
}

.btn-remove-step:hover {
    background: rgba(239, 68, 68, 0.1);
    color: var(--danger);
}

.step-content .form-group {
    margin-bottom: 12px;
}

.step-content .form-group:last-child {
    margin-bottom: 0;
}

/* ===== BUTTONS ===== */
.btn-add-step {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 500;
    border-radius: 10px;
    border: 1px dashed rgba(124, 58, 237, 0.4);
    background: transparent;
    color: var(--accent);
    cursor: pointer;
    transition: all 0.2s;
    width: 100%;
    justify-content: center;
}

.btn-add-step:hover {
    background: rgba(124, 58, 237, 0.08);
    border-color: var(--accent);
}

.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 10px 24px;
    font-size: 14px;
    font-weight: 500;
    border-radius: 10px;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.btn-primary {
    background: var(--accent);
    color: #fff;
}

.btn-primary:hover:not(:disabled) {
    background: #6d28d9;
    transform: translateY(-2px);
}

.btn-secondary {
    background: transparent;
    color: var(--text-secondary);
    border: 1px solid rgba(255,255,255,0.08);
}

.btn-secondary:hover:not(:disabled) {
    background: rgba(255,255,255,0.05);
}

/* ===== FORM ACTIONS ===== */
.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    padding-top: 20px;
    border-top: 1px solid rgba(255,255,255,0.06);
}

/* ===== ANIMATIONS ===== */
@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fa-spin {
    animation: fa-spin 1s linear infinite;
}

@keyframes fa-spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
    .form-row {
        grid-template-columns: 1fr;
        gap: 0;
    }

    .form-card-header {
        flex-wrap: wrap;
    }

    .steps-count {
        margin-left: 0;
        width: 100%;
    }

    .form-actions {
        flex-direction: column-reverse;
    }

    .form-actions .btn {
        width: 100%;
        justify-content: center;
    }

    .step-card {
        padding: 12px;
    }
}

@media (max-width: 480px) {
    .form-card-body {
        padding: 16px;
    }

    .empty-state {
        padding: 24px;
    }

    .empty-state i {
        font-size: 24px;
    }

    .empty-state p {
        font-size: 14px;
    }
}
</style>