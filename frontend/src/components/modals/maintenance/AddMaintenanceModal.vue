<template>
    <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
            <!-- Шаг 1: Выбор типа -->
            <template v-if="currentStep === 1">
                <div class="modal-header">
                    <div class="header-top">
                        <div class="header-icon" :style="{background: 'var(--accent-trans)', color: 'var(--accent)'}">
                            <i class="fa fa-wrench"></i>
                        </div>
                        <button @click="closeModal" class="close-btn">
                            <i class="fa fa-times"></i>
                        </button>
                    </div>
                    <h2 class="modal-title">Добавить обслуживание</h2>
                    <p class="modal-subtitle">Выберите, что хотите сделать</p>
                </div>

                <div class="step-body">
                    <div 
                        class="choice-card"
                        :class="{ selected: selectedType === 'history' }"
                        @click="selectType('history')"
                    >
                        <div class="choice-icon" style="background: var(--success-trans); color: var(--success);">
                            <i class="fa fa-clock"></i>
                        </div>
                        <div class="choice-info">
                            <div class="choice-title">Добавить в историю</div>
                            <div class="choice-subtitle">Уже выполненное обслуживание</div>
                        </div>
                        <div class="choice-arrow">
                            <i class="fa fa-angle-right"></i>
                        </div>
                    </div>

                    <div 
                        class="choice-card"
                        :class="{ selected: selectedType === 'planned' }"
                        @click="selectType('planned')"
                    >
                        <div class="choice-icon" style="background: var(--warning-trans); color: var(--warning);">
                            <i class="fa fa-calendar"></i>
                        </div>
                        <div class="choice-info">
                            <div class="choice-title">Запланировать</div>
                            <div class="choice-subtitle">Плановое обслуживание</div>
                        </div>
                        <div class="choice-arrow">
                            <i class="fa fa-angle-right"></i>
                        </div>
                    </div>
                </div>

                <div class="step-actions">
                    <button class="btn btn-secondary" @click="closeModal">Отменить</button>
                    <button 
                        class="btn btn-primary" 
                        :disabled="!selectedType"
                        @click="nextStep"
                    >
                        Продолжить <i class="fa fa-arrow-right"></i>
                    </button>
                </div>
            </template>

            <!-- Шаг 2: Выбор мотоцикла -->
            <template v-if="currentStep === 2">
                <div class="modal-header">
                    <div class="header-top">
                        <div class="header-icon" :style="{background: 'var(--accent-trans)', color: 'var(--accent)'}">
                            <i class="fa fa-motorcycle"></i>
                        </div>
                        <button @click="closeModal" class="close-btn">
                            <i class="fa fa-times"></i>
                        </button>
                    </div>
                    <h2 class="modal-title">Выберите мотоцикл</h2>
                    <p class="modal-subtitle">Для какого мотоцикла добавить обслуживание</p>
                </div>

                <div class="step-body">
                    <div 
                        v-for="moto in motorcycles" 
                        :key="moto.id"
                        class="moto-choice-card"
                        :class="{ selected: form.motorcycleId === moto.id }"
                        @click="form.motorcycleId = moto.id"
                    >
                        <div class="moto-choice-icon">
                            <img v-if="moto.photo_url" :src="getPhotoUrl(moto.photo_url)" alt="Фото" />
                            <i v-else class="fa fa-motorcycle"></i>
                        </div>
                        <div class="moto-choice-info">
                            <div class="moto-choice-name">{{ moto.name }}</div>
                            <div class="moto-choice-meta">{{ moto.years || '—' }} • {{ moto.mileage || 0 }} км</div>
                        </div>
                        <div v-if="form.motorcycleId === moto.id" class="moto-choice-check">
                            <i class="fa fa-check-circle"></i>
                        </div>
                    </div>
                </div>

                <div class="step-actions">
                    <button class="btn btn-secondary" @click="prevStep">
                        <i class="fa fa-arrow-left"></i> Назад
                    </button>
                    <button 
                        class="btn btn-primary" 
                        :disabled="!form.motorcycleId"
                        @click="nextStep"
                    >
                        Продолжить <i class="fa fa-arrow-right"></i>
                    </button>
                </div>
            </template>

            <!-- Шаг 3: Выбор обслуживания -->
            <template v-if="currentStep === 3">
                <div class="modal-header">
                    <div class="header-top">
                        <div class="header-icon" :style="{background: 'var(--accent-trans)', color: 'var(--accent)'}">
                            <i class="fa fa-tools"></i>
                        </div>
                        <button @click="closeModal" class="close-btn">
                            <i class="fa fa-times"></i>
                        </button>
                    </div>
                    <h2 class="modal-title">Выберите обслуживание</h2>
                    <p class="modal-subtitle">Выберите узел и тип работ</p>
                </div>

                <div class="step-body">
                    <div class="form-group">
                        <label for="categorySelect">Узел / Система</label>
                        <select id="categorySelect" v-model="form.category" @change="onCategoryChange">
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
                    </div>

                    <div class="form-group" v-if="templates.length > 0">
                        <label for="templateSelect">Тип обслуживания</label>
                        <select id="templateSelect" v-model="form.templateId" @change="onTemplateChange">
                            <option value="">Выберите тип обслуживания</option>
                            <option v-for="tpl in templates" :key="tpl.id" :value="tpl.id">
                                {{ tpl.label }}
                            </option>
                        </select>
                    </div>

                    <div v-if="!form.category" class="info-block">
                        <div class="block-icon">
                            <i class="fa fa-info-circle"></i>
                        </div>
                        <p class="block-text">Выберите категорию, чтобы увидеть доступные типы обслуживания</p>
                    </div>
                </div>

                <div class="step-actions">
                    <button class="btn btn-secondary" @click="prevStep">
                        <i class="fa fa-arrow-left"></i> Назад
                    </button>
                    <button 
                        class="btn btn-primary" 
                        :disabled="!form.category || !form.title"
                        @click="nextStep"
                    >
                        Продолжить <i class="fa fa-arrow-right"></i>
                    </button>
                </div>
            </template>

            <!-- Шаг 4: Описание -->
            <template v-if="currentStep === 4">
                <div class="modal-header">
                    <div class="header-top">
                        <div class="header-icon" :style="{background: 'var(--accent-trans)', color: 'var(--accent)'}">
                            <i class="fa fa-align-left"></i>
                        </div>
                        <button @click="closeModal" class="close-btn">
                            <i class="fa fa-times"></i>
                        </button>
                    </div>
                    <h2 class="modal-title">Добавьте описание</h2>
                    <p class="modal-subtitle">Расскажите подробнее о работе</p>
                </div>

                <div class="step-body">
                    <div class="form-group">
                        <label for="description">Описание работы</label>
                        <textarea 
                            id="description"
                            v-model="form.description"
                            rows="4"
                            placeholder="Опишите, что было сделано..."
                            class="textarea-input"
                        ></textarea>
                    </div>

                    <div class="info-block">
                        <div class="block-icon">
                            <i class="fa fa-lightbulb"></i>
                        </div>
                        <p class="block-text">Чем подробнее описание, тем легче будет анализировать историю обслуживания</p>
                    </div>
                </div>

                <div class="step-actions">
                    <button class="btn btn-secondary" @click="prevStep">
                        <i class="fa fa-arrow-left"></i> Назад
                    </button>
                    <button class="btn btn-primary" @click="nextStep">
                        Продолжить <i class="fa fa-arrow-right"></i>
                    </button>
                </div>
            </template>

            <!-- Шаг 5: Дополнительная информация (история) -->
            <template v-if="currentStep === 5 && selectedType === 'history'">
                <div class="modal-header">
                    <div class="header-top">
                        <div class="header-icon" :style="{background: 'var(--success-trans)', color: 'var(--success)'}">
                            <i class="fa fa-clipboard-list"></i>
                        </div>
                        <button @click="closeModal" class="close-btn">
                            <i class="fa fa-times"></i>
                        </button>
                    </div>
                    <h2 class="modal-title">Детали выполнения</h2>
                    <p class="modal-subtitle">Укажите детали выполненной работы</p>
                </div>

                <div class="step-body">
                    <div class="form-group">
                        <label for="cost">Стоимость (₽)</label>
                        <input
                            id="cost"
                            v-model.number="form.cost"
                            type="number"
                            placeholder="0"
                            min="0"
                            class="form-input"
                        />
                    </div>

                    <div class="form-group">
                        <label for="mileage">Пробег (км) <span class="required">*</span></label>
                        <input
                            id="mileage"
                            v-model.number="form.mileage"
                            type="number"
                            placeholder="0"
                            min="0"
                            class="form-input"
                            required
                        />
                    </div>

                    <div class="form-group">
                        <label for="date">Дата выполнения</label>
                        <input
                            id="date"
                            v-model="form.date"
                            type="date"
                            :max="currentDate"
                            class="form-input"
                        />
                    </div>
                </div>

                <div class="step-actions">
                    <button class="btn btn-secondary" @click="prevStep">
                        <i class="fa fa-arrow-left"></i> Назад
                    </button>
                    <button 
                        class="btn btn-primary" 
                        :disabled="!form.mileage || form.mileage <= 0"
                        @click="nextStep"
                    >
                        Продолжить <i class="fa fa-arrow-right"></i>
                    </button>
                </div>
            </template>

            <!-- Шаг 5: Дополнительная информация (плановое) -->
            <template v-if="currentStep === 5 && selectedType === 'planned'">
                <div class="modal-header">
                    <div class="header-top">
                        <div class="header-icon" :style="{background: 'var(--warning-trans)', color: 'var(--warning)'}">
                            <i class="fa fa-calendar-plus"></i>
                        </div>
                        <button @click="closeModal" class="close-btn">
                            <i class="fa fa-times"></i>
                        </button>
                    </div>
                    <h2 class="modal-title">Планирование</h2>
                    <p class="modal-subtitle">Укажите, когда планируете выполнить работу</p>
                </div>

                <div class="step-body">
                    <div class="form-group">
                        <label for="plannedMileage">Плановый пробег (км) <span class="required">*</span></label>
                        <input
                            id="plannedMileage"
                            v-model.number="form.planned_mileage"
                            type="number"
                            placeholder="0"
                            min="0"
                            class="form-input"
                            required
                        />
                    </div>

                    <div class="info-block">
                        <div class="block-icon">
                            <i class="fa fa-bell"></i>
                        </div>
                        <p class="block-text">Мы напомним вам, когда мотоцикл достигнет указанного пробега</p>
                    </div>
                </div>

                <div class="step-actions">
                    <button class="btn btn-secondary" @click="prevStep">
                        <i class="fa fa-arrow-left"></i> Назад
                    </button>
                    <button 
                        class="btn btn-primary" 
                        :disabled="!form.planned_mileage || form.planned_mileage <= 0"
                        @click="nextStep"
                    >
                        Продолжить <i class="fa fa-arrow-right"></i>
                    </button>
                </div>
            </template>

            <!-- Шаг 6: Финальный -->
            <template v-if="currentStep === 6">
                <div class="completion-step">
                    <div class="completion-glow"></div>
                    
                    <div class="particles-container">
                        <div
                            v-for="i in 30"
                            :key="i"
                            class="particle"
                            :style="getParticleStyle(i)"
                        ></div>
                    </div>

                    <div class="blur-blobs">
                        <div class="blob blob-1"></div>
                        <div class="blob blob-2"></div>
                        <div class="blob blob-3"></div>
                    </div>

                    <div class="completion-icon">
                        <i class="fa fa-check-circle"></i>
                    </div>
                    <h2 class="step-title">Всё готово!</h2>
                    <p class="step-subtitle">
                        {{ selectedType === 'history' 
                            ? 'Обслуживание успешно добавлено в историю' 
                            : 'Обслуживание успешно запланировано' 
                        }}
                    </p>

                    <div class="summary-card">
                        <div class="summary-item">
                            <span class="summary-label">Мотоцикл</span>
                            <span class="summary-value">{{ getMotoName(form.motorcycleId) }}</span>
                        </div>
                        <div class="summary-item">
                            <span class="summary-label">Обслуживание</span>
                            <span class="summary-value">{{ form.title }}</span>
                        </div>
                        <div class="summary-item" v-if="form.description">
                            <span class="summary-label">Описание</span>
                            <span class="summary-value">{{ form.description }}</span>
                        </div>
                        <div class="summary-item" v-if="selectedType === 'history' && form.cost">
                            <span class="summary-label">Стоимость</span>
                            <span class="summary-value">{{ form.cost }} ₽</span>
                        </div>
                        <div class="summary-item" v-if="selectedType === 'history' && form.mileage">
                            <span class="summary-label">Пробег</span>
                            <span class="summary-value">{{ form.mileage }} км</span>
                        </div>
                        <div class="summary-item" v-if="selectedType === 'planned' && form.planned_mileage">
                            <span class="summary-label">Плановый пробег</span>
                            <span class="summary-value">{{ form.planned_mileage }} км</span>
                        </div>
                    </div>

                    <div class="step-actions">
                        <button 
                            class="btn btn-primary submit-btn" 
                            :disabled="loading"
                            @click="submit"
                        >
                            <span v-if="!loading"><i class="fa fa-save"></i> Сохранить</span>
                            <span v-else>Сохранение...</span>
                        </button>
                    </div>
                </div>
            </template>
        </div>
    </div>
</template>

<script>
import { getTemplatesByCategory } from '../../../constants/maintenanceTemplates';

export default {
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
            },
            templates: [],
            currentDate: new Date().toISOString().split('T')[0],
            loading: false,
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
        getPhotoUrl(photoPath) {
            if (!photoPath) return null
            if (photoPath.startsWith('http')) return photoPath
            const baseUrl = import.meta.env.VITE_API_URL || ''
            return `${baseUrl}/uploads/${photoPath}`
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
            if (this.currentStep < 6) {
                this.currentStep++
            }
        },

        prevStep() {
            if (this.currentStep > 1) {
                this.currentStep--
            }
        },

        getParticleStyle(index) {
            const size = Math.random() * 6 + 2
            const x = Math.random() * 100
            const y = Math.random() * 100
            const duration = Math.random() * 20 + 15
            const delay = Math.random() * 10
            const opacity = Math.random() * 0.4 + 0.1
            
            return {
                width: size + 'px',
                height: size + 'px',
                left: x + '%',
                top: y + '%',
                animationDuration: duration + 's',
                animationDelay: delay + 's',
                opacity: opacity,
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
                    description: this.form.description || '',
                }

                if (this.selectedType === 'history') {
                    payload = {
                        ...payload,
                        cost: this.form.cost || null,
                        completed_mileage: this.form.mileage,
                        completed_date: this.form.date || null,
                    }
                } else {
                    payload = {
                        ...payload,
                        planned_mileage: this.form.planned_mileage,
                    }
                }

                await this.$emit('submit', payload)
                this.closeModal()
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
/* ===== ОВЕРЛЕЙ ===== */
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 16px;
    animation: fadeIn 0.25s ease;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.modal-content {
    background: var(--bg-primary);
    border-radius: 16px;
    max-width: 560px;
    width: 100%;
    max-height: 90vh;
    display: flex;
    flex-direction: column;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.05);
    animation: slideUp 0.3s ease;
    overflow: hidden;
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px) scale(0.98);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

/* ===== ЗАГОЛОВОК ===== */
.modal-header {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 20px 24px 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.header-top {
    display: flex;
    gap: 16px;
    align-items: center;
    margin-bottom: 12px;
}

.header-icon {
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    font-size: 20px;
}

.close-btn {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: none;
    background: var(--bg-secondary);
    color: var(--text-secondary);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    transition: all 0.2s;
}

.close-btn:hover {
    background: var(--danger-trans);
    color: var(--danger);
}

.modal-title {
    font-size: 20px;
    font-weight: 700;
    margin: 0 0 4px 0;
    color: var(--text-primary);
}

.modal-subtitle {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
}

/* ===== ТЕЛО ШАГА ===== */
.step-body {
    flex: 1;
    overflow-y: auto;
    padding: 16px 24px;
}

.step-body::-webkit-scrollbar {
    width: 4px;
}

.step-body::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
}

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
    background: var(--accent-light);
    box-shadow: 0 0 0 2px rgba(138, 92, 246, 0.2);
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

.choice-info {
    flex: 1;
}

.choice-title {
    font-size: 16px;
    font-weight: 600;
}

.choice-subtitle {
    font-size: 13px;
    color: var(--text-secondary);
}

.choice-arrow {
    color: var(--text-muted);
    font-size: 18px;
}

/* ===== КАРТОЧКИ МОТОЦИКЛА ===== */
.moto-choice-card {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 16px;
    background: var(--bg-secondary);
    border: 2px solid transparent;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s;
    margin-bottom: 10px;
}

.moto-choice-card:hover {
    background: var(--bg-card-hover);
    transform: translateY(-2px);
}

.moto-choice-card.selected {
    border-color: var(--accent);
    background: var(--accent-light);
    box-shadow: 0 0 0 2px rgba(138, 92, 246, 0.2);
}

.moto-choice-icon {
    width: 44px;
    height: 44px;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.05);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    color: var(--text-muted);
    flex-shrink: 0;
    overflow: hidden;
}

.moto-choice-icon img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.moto-choice-info {
    flex: 1;
}

.moto-choice-name {
    font-size: 15px;
    font-weight: 600;
}

.moto-choice-meta {
    font-size: 13px;
    color: var(--text-secondary);
}

.moto-choice-check {
    color: var(--accent);
    font-size: 20px;
}

/* ===== ФОРМА ===== */
.form-group {
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin-bottom: 14px;
}

.form-group label {
    font-weight: 600;
    font-size: 0.85rem;
    color: var(--text-secondary);
}

.required {
    color: var(--danger);
}

.form-input,
.form-group select {
    padding: 0.6rem 0.8rem;
    border-radius: 8px;
    border: 2px solid var(--border-color);
    background-color: var(--bg-secondary);
    color: var(--text-primary);
    font-size: 0.95rem;
    transition: border 0.2s;
    width: 100%;
    box-sizing: border-box;
}

.form-input:focus,
.form-group select:focus {
    border-color: var(--accent);
    outline: none;
    box-shadow: 0 0 0 3px rgba(138, 92, 246, 0.15);
}

.form-input::placeholder {
    color: var(--text-muted);
}

.textarea-input {
    padding: 0.6rem 0.8rem;
    border-radius: 8px;
    border: 2px solid var(--border-color);
    background-color: var(--bg-secondary);
    color: var(--text-primary);
    font-size: 0.95rem;
    transition: border 0.2s;
    width: 100%;
    box-sizing: border-box;
    resize: vertical;
    font-family: inherit;
}

.textarea-input:focus {
    border-color: var(--accent);
    outline: none;
    box-shadow: 0 0 0 3px rgba(138, 92, 246, 0.15);
}

.textarea-input::placeholder {
    color: var(--text-muted);
}

/* ===== ИНФО-БЛОК ===== */
.info-block {
    display: flex;
    padding: 12px;
    background-color: var(--accent-trans);
    border-radius: 10px;
    border: 1px solid var(--accent-light);
    margin-top: 4px;
}

.block-icon {
    color: var(--accent);
    font-size: 20px;
    margin-right: 12px;
    flex-shrink: 0;
}

.block-text {
    font-size: 13px;
    color: var(--text-secondary);
    margin: 0;
}

/* ===== КНОПКИ ===== */
.step-actions {
    display: flex;
    gap: 10px;
    padding: 12px 24px 20px;
    flex-shrink: 0;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    background: var(--bg-primary);
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

.btn-primary {
    background: linear-gradient(135deg, var(--accent), var(--accent-hover));
    color: white;
}

.btn-primary:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(138, 92, 246, 0.3);
}

.btn-primary:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.btn-secondary {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}

.btn-secondary:hover {
    background: var(--border-color);
}

.submit-btn.btn-primary {
    background: linear-gradient(135deg, var(--success), #22c55e);
}

.submit-btn.btn-primary:hover:not(:disabled) {
    box-shadow: 0 4px 16px rgba(34, 197, 94, 0.3);
}

/* ===== ФИНАЛЬНЫЙ ШАГ ===== */
.completion-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 32px 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
    min-height: 420px;
}

.completion-glow {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 80%;
    height: 60%;
    background: radial-gradient(
        ellipse at center,
        rgba(139, 92, 246, 0.25) 0%,
        rgba(139, 92, 246, 0.08) 40%,
        transparent 70%
    );
    animation: pulseGlow 4s ease-in-out infinite;
    pointer-events: none;
}

@keyframes pulseGlow {
    0%, 100% {
        transform: translate(-50%, -50%) scale(1);
        opacity: 0.8;
    }
    50% {
        transform: translate(-50%, -50%) scale(1.2);
        opacity: 1;
    }
}

.blur-blobs {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    overflow: hidden;
}

.blob {
    position: absolute;
    border-radius: 50%;
    filter: blur(60px);
    opacity: 0.08;
}

.blob-1 {
    width: 200px;
    height: 200px;
    background: var(--accent);
    top: 10%;
    right: -10%;
    animation: floatBlob 12s ease-in-out infinite;
}

.blob-2 {
    width: 150px;
    height: 150px;
    background: #a78bfa;
    bottom: 10%;
    left: -10%;
    animation: floatBlob 16s ease-in-out infinite reverse;
}

.blob-3 {
    width: 120px;
    height: 120px;
    background: #7c3aed;
    top: 40%;
    left: 30%;
    animation: floatBlob 14s ease-in-out infinite 2s;
}

@keyframes floatBlob {
    0%, 100% {
        transform: translate(0, 0) scale(1);
    }
    33% {
        transform: translate(20px, -30px) scale(1.1);
    }
    66% {
        transform: translate(-20px, 20px) scale(0.9);
    }
}

.particles-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    overflow: hidden;
}

.particle {
    position: absolute;
    border-radius: 50%;
    background: var(--accent);
    animation: floatParticle linear infinite;
    pointer-events: none;
    will-change: transform;
    box-shadow: 0 0 10px rgba(139, 92, 246, 0.3);
}

@keyframes floatParticle {
    0% {
        transform: translate(0, 0) scale(1);
        opacity: 0;
    }
    10% {
        opacity: 1;
    }
    90% {
        opacity: 1;
    }
    100% {
        transform: translate(calc(var(--dx, 30px)), calc(var(--dy, -80px))) scale(0.5);
        opacity: 0;
    }
}

.particle:nth-child(odd) {
    --dx: 40px;
    --dy: -100px;
}

.particle:nth-child(even) {
    --dx: -30px;
    --dy: -70px;
}

.particle:nth-child(3n) {
    --dx: 50px;
    --dy: -60px;
}

.particle:nth-child(5n) {
    --dx: -50px;
    --dy: -90px;
}

.particle:nth-child(7n) {
    --dx: 20px;
    --dy: -120px;
}

.completion-icon {
    font-size: 56px;
    color: var(--success);
    margin-bottom: 12px;
    position: relative;
    z-index: 2;
    filter: drop-shadow(0 0 30px var(--success-trans));
}

.completion-step .step-title {
    font-size: 24px;
    font-weight: 700;
    margin: 0 0 8px 0;
    position: relative;
    z-index: 2;
}

.completion-step .step-subtitle {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0 0 16px 0;
    position: relative;
    z-index: 2;
}

.completion-step .step-actions {
    position: relative;
    z-index: 2;
    width: 100%;
    border-top: none;
    padding: 0;
}

.summary-card {
    background: var(--bg-secondary);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
    width: 100%;
    position: relative;
    z-index: 2;
}

.summary-item {
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.summary-item:last-child {
    border-bottom: none;
}

.summary-label {
    font-size: 0.85rem;
    color: var(--text-secondary);
}

.summary-value {
    font-size: 0.9rem;
    font-weight: 500;
    text-align: right;
    max-width: 60%;
    word-break: break-word;
}

/* ============================================ */
/* ===== АДАПТИВНОСТЬ ===== */
/* ============================================ */

@media (max-width: 640px) {
    .modal-overlay {
        padding: 8px;
        align-items: flex-end;
    }

    .modal-content {
        max-height: 94vh;
        border-radius: 16px 16px 0 0;
        animation: slideUpMobile 0.3s ease;
    }

    @keyframes slideUpMobile {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .modal-header {
        padding: 16px 16px 12px;
    }

    .header-icon {
        width: 40px;
        height: 40px;
        font-size: 18px;
    }

    .modal-title {
        font-size: 18px;
    }

    .step-body {
        padding: 12px 16px;
    }

    .step-actions {
        flex-direction: column;
        padding: 10px 16px 16px;
    }

    .step-actions .btn {
        width: 100%;
        padding: 0.8rem;
    }

    .choice-card {
        padding: 14px 16px;
    }

    .moto-choice-card {
        padding: 12px 14px;
    }

    .completion-step {
        padding: 24px 16px;
        min-height: 360px;
    }

    .completion-icon {
        font-size: 48px;
    }

    .completion-step .step-title {
        font-size: 20px;
    }

    .summary-item {
        flex-direction: column;
        gap: 2px;
        text-align: center;
    }

    .summary-value {
        max-width: 100%;
        text-align: center;
    }

    .close-btn {
        width: 32px;
        height: 32px;
        font-size: 14px;
    }
}

@media (max-width: 400px) {
    .modal-content {
        padding: 0;
    }

    .modal-header {
        padding: 12px 12px 10px;
    }

    .step-body {
        padding: 10px 12px;
    }

    .step-actions {
        padding: 8px 12px 12px;
    }

    .form-input,
    .form-group select,
    .textarea-input {
        font-size: 0.9rem;
        padding: 0.5rem 0.7rem;
    }

    .choice-card {
        padding: 12px 14px;
    }

    .choice-icon {
        width: 36px;
        height: 36px;
        font-size: 16px;
    }

    .moto-choice-icon {
        width: 36px;
        height: 36px;
        font-size: 16px;
    }
}
</style>