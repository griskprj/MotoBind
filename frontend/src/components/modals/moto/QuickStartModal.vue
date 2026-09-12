<template>
    <ModalWrapper
        :isOpen="isOpen"
        :title="stepTitle"
        :subtitle="stepSubtitle"
        :icon="stepIcon"
        size="md"
        @close="close"
    >
        <!-- ===== ШАГ 1: ВВОДНЫЙ ===== -->
        <template v-if="step === 1">
            <div class="welcome">
                <div class="welcome-icon">
                    <i class="fa fa-rocket"></i>
                </div>
                <h3>Быстрый старт</h3>
                <p>
                    Мы автоматически создадим базовое расписание обслуживания
                    для вашего мотоцикла, чтобы вы не пропустили важные работы.
                </p>
                <ul class="welcome-features">
                    <li><i class="fa fa-check-circle"></i> Замена масла и фильтров</li>
                    <li><i class="fa fa-check-circle"></i> Проверка тормозов и шин</li>
                    <li><i class="fa fa-check-circle"></i> Обслуживание привода</li>
                </ul>
                <div class="info-box info">
                    <i class="fa fa-info-circle"></i>
                    <span>Все работы можно будет изменить или удалить</span>
                </div>
            </div>
        </template>

        <!-- ===== ШАГ 2: ПАРАМЕТРЫ ===== -->
        <template v-if="step === 2">
            <!-- Пробег -->
            <div class="field">
                <label>Текущий пробег <span>*</span></label>
                <div class="input-with-unit">
                    <input 
                        v-model.number="form.currentMileage" 
                        type="number" 
                        min="0"
                        placeholder="0"
                        required
                    />
                    <span class="unit">км</span>
                </div>
                <p class="field-hint">Можно изменить, если значение неточное</p>
            </div>

            <!-- Тип привода -->
            <div class="field">
                <label>Тип привода <span>*</span></label>
                <div class="radio-group">
                    <button 
                        v-for="d in driveOptions" 
                        :key="d.value"
                        class="radio-card"
                        :class="{ active: form.driveType === d.value }"
                        @click="form.driveType = d.value"
                        type="button"
                    >
                        <i :class="d.icon"></i>
                        <span>{{ d.label }}</span>
                    </button>
                </div>
            </div>

            <!-- Стиль езды -->
            <div class="field">
                <label>Стиль езды</label>
                <div class="radio-group">
                    <button 
                        v-for="s in styleOptions" 
                        :key="s.value"
                        class="radio-card"
                        :class="{ active: form.style === s.value }"
                        @click="form.style = s.value"
                        type="button"
                    >
                        <i :class="s.icon"></i>
                        <span>{{ s.label }}</span>
                    </button>
                </div>
            </div>

            <!-- Местность -->
            <div class="field">
                <label>Условия эксплуатации</label>
                <div class="radio-group vertical">
                    <button 
                        v-for="t in terrainOptions" 
                        :key="t.value"
                        class="radio-card"
                        :class="{ active: form.terrain === t.value }"
                        @click="form.terrain = t.value"
                        type="button"
                    >
                        <i :class="t.icon"></i>
                        <div class="radio-info">
                            <span class="radio-title">{{ t.label }}</span>
                            <span class="radio-desc">{{ t.desc }}</span>
                        </div>
                    </button>
                </div>
            </div>
        </template>

        <!-- ===== ШАГ 3: ПРЕДПРОСМОТР ===== -->
        <template v-if="step === 3">
            <div class="preview">
                <p class="preview-intro">
                    Мы создадим следующие работы:
                </p>
                
                <div class="preview-list">
                    <div 
                        v-for="item in previewItems" 
                        :key="item.code"
                        class="preview-item"
                    >
                        <div class="preview-icon" :class="item.category">
                            <i :class="getCategoryIcon(item.category)"></i>
                        </div>
                        <div class="preview-content">
                            <div class="preview-title">{{ item.title }}</div>
                            <div class="preview-meta">
                                <span>
                                    <i class="fa fa-road"></i>
                                    через {{ item.interval_km.toLocaleString() }} км
                                </span>
                                <span>
                                    <i class="fa fa-calendar"></i>
                                    через {{ item.interval_days }} дн
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="info-box info">
                    <i class="fa fa-lightbulb"></i>
                    <span>
                        Интервалы рассчитаны с учётом ваших условий эксплуатации.
                        Вы можете изменить их позже.
                    </span>
                </div>
            </div>
        </template>

        <!-- ===== ШАГ 4: ГОТОВО ===== -->
        <template v-if="step === 4">
            <div class="success">
                <div class="success-icon">
                    <i class="fa fa-check-circle"></i>
                </div>
                <h3>Готово!</h3>
                <p>Мы создали базовое расписание обслуживания</p>
                
                <div class="success-stats">
                    <div class="success-stat">
                        <span class="stat-value">{{ createdCount }}</span>
                        <span class="stat-label">работ</span>
                    </div>
                    <div class="success-stat">
                        <span class="stat-value">{{ form.currentMileage.toLocaleString() }}</span>
                        <span class="stat-label">км</span>
                    </div>
                </div>

                <p class="success-hint">
                    Все работы вы найдёте в разделе "Обслуживание"
                </p>
            </div>
        </template>

        <!-- ===== КНОПКИ ===== -->
        <template #actions>
            <div class="actions">
                <button 
                    v-if="step > 1 && step < 4" 
                    class="btn btn-secondary" 
                    @click="step--"
                >
                    <i class="fa fa-arrow-left"></i> Назад
                </button>
                <button 
                    v-if="step === 1" 
                    class="btn btn-secondary" 
                    @click="close"
                >
                    Позже
                </button>

                <button 
                    v-if="step < 3" 
                    class="btn btn-primary" 
                    :disabled="!canProceed"
                    @click="step++"
                >
                    Далее <i class="fa fa-arrow-right"></i>
                </button>

                <button 
                    v-if="step === 3" 
                    class="btn btn-primary" 
                    :disabled="loading"
                    @click="submit"
                >
                    <span v-if="!loading">
                        <i class="fa fa-check"></i> Создать
                    </span>
                    <span v-else>
                        <i class="fa fa-spinner fa-spin"></i> Создание...
                    </span>
                </button>

                <button 
                    v-if="step === 4" 
                    class="btn btn-success" 
                    @click="finish"
                >
                    <i class="fa fa-check"></i> Перейти в гараж
                </button>
            </div>
        </template>
    </ModalWrapper>
</template>

<script>
import ModalWrapper from '../ModalWrapper.vue'
import api from '../../../api/api'

export default {
    components: { ModalWrapper },
    
    props: {
        isOpen: Boolean,
        motorcycle: {
            type: Object,
            default: null
        }
    },
    
    emits: ['close', 'created'],
    
    data() {
        return {
            step: 1,
            loading: false,
            createdCount: 0,
            
            form: {
                currentMileage: 0,
                driveType: 'chain',
                style: 'normal',
                terrain: 'mixed'
            },
            
            driveOptions: [
                { value: 'chain', label: 'Цепь', icon: 'fa fa-link' },
                { value: 'belt', label: 'Ремень', icon: 'fa fa-circle-notch' },
                { value: 'shaft', label: 'Кардан', icon: 'fa fa-cog' },
            ],
            
            styleOptions: [
                { value: 'calm', label: 'Спокойный', icon: 'fa fa-leaf' },
                { value: 'normal', label: 'Обычный', icon: 'fa fa-motorcycle' },
                { value: 'aggressive', label: 'Агрессивный', icon: 'fa fa-bolt' },
            ],
            
            terrainOptions: [
                { 
                    value: 'city', 
                    label: 'Город', 
                    desc: 'Ежедневные поездки по асфальту',
                    icon: 'fa fa-city'
                },
                { 
                    value: 'highway', 
                    label: 'Трасса', 
                    desc: 'Дальние поездки, ровный асфальт',
                    icon: 'fa fa-road'
                },
                { 
                    value: 'mixed', 
                    label: 'Смешанный', 
                    desc: 'И город, и трасса',
                    icon: 'fa fa-random'
                },
                { 
                    value: 'dusty', 
                    label: 'Пыльная местность', 
                    desc: 'Много пыли, грунтовки',
                    icon: 'fa fa-wind'
                },
                { 
                    value: 'offroad', 
                    label: 'Бездорожье', 
                    desc: 'Грязь, камни, бездорожье',
                    icon: 'fa fa-mountain'
                },
            ]
        }
    },
    
    computed: {
        stepTitle() {
            return {
                1: 'Быстрый старт',
                2: 'Параметры эксплуатации',
                3: 'Предпросмотр',
                4: 'Готово!'
            }[this.step] || 'Быстрый старт'
        },
        
        stepSubtitle() {
            return {
                1: 'Настроим базовое обслуживание за 30 секунд',
                2: 'Это поможет точнее рассчитать интервалы',
                3: 'Проверьте, что мы вам предлагаем',
                4: ''
            }[this.step] || ''
        },
        
        stepIcon() {
            return {
                1: 'rocket',
                2: 'sliders',
                3: 'list-check',
                4: 'check-circle'
            }[this.step] || 'rocket'
        },
        
        canProceed() {
            if (this.step === 1) return true
            if (this.step === 2) {
                return this.form.currentMileage >= 0 && this.form.driveType
            }
            return true
        },
        
        previewItems() {
            // Локальный расчёт для предпросмотра
            // Дублирует логику backend для UX
            const basePresets = [
                { code: 'engine_oil', title: 'Замена масла', category: 'engine', km: 5000, days: 365, affects: ['style', 'terrain'] },
                { code: 'air_filter', title: 'Замена воздушного фильтра', category: 'engine', km: 10000, days: 365, affects: ['terrain'] },
                { code: 'tire_pressure', title: 'Проверка давления в шинах', category: 'wheel', km: 1000, days: 30, affects: [] },
                { code: 'brake_check', title: 'Проверка тормозов', category: 'brakes', km: 10000, days: 180, affects: ['style'] },
            ]
            
            const drivePresets = {
                chain: [
                    { code: 'chain_lube', title: 'Смазка цепи', category: 'drive', km: 500, days: 14, affects: ['terrain'] },
                    { code: 'chain_adjust', title: 'Регулировка цепи', category: 'drive', km: 1000, days: 30, affects: ['style'] },
                ],
                belt: [
                    { code: 'belt_check', title: 'Проверка ремня', category: 'drive', km: 5000, days: 90, affects: ['style'] },
                ],
                shaft: [
                    { code: 'shaft_oil', title: 'Замена масла в редукторе', category: 'drive', km: 20000, days: 730, affects: [] },
                ]
            }
            
            const presets = [...basePresets, ...(drivePresets[this.form.driveType] || [])]
            
            const styleMult = { calm: 1.2, normal: 1.0, aggressive: 0.8 }[this.form.style] || 1.0
            const terrainMult = { city: 1.0, highway: 1.1, mixed: 1.0, dusty: 0.7, offroad: 0.6 }[this.form.terrain] || 1.0
            
            return presets.map(p => {
                let mult = 1.0
                if (p.affects.includes('style')) mult *= styleMult
                if (p.affects.includes('terrain')) mult *= terrainMult
                
                return {
                    ...p,
                    interval_km: Math.max(Math.round(p.km * mult / 100) * 100, 100),
                    interval_days: Math.max(Math.round(p.days * mult), 7)
                }
            })
        }
    },
    
    watch: {
        isOpen(val) {
            if (val) {
                this.step = 1
                this.loading = false
                this.createdCount = 0
                this.form = {
                    currentMileage: this.motorcycle?.mileage || 0,
                    driveType: 'chain',
                    style: 'normal',
                    terrain: 'mixed'
                }
            }
        }
    },
    
    methods: {
        getCategoryIcon(category) {
            const icons = {
                engine: 'fa fa-cog',
                drive: 'fa fa-link',
                wheel: 'fa fa-circle',
                brakes: 'fa fa-stop-circle',
                fuel: 'fa fa-gas-pump',
                cooling: 'fa fa-snowflake',
                electronics: 'fa fa-bolt',
                suspension: 'fa fa-arrows-alt-v',
                steering: 'fa fa-crosshairs'
            }
            return icons[category] || 'fa fa-wrench'
        },
        
        async submit() {
            if (!this.motorcycle) {
                this.$toast?.error('Мотоцикл не выбран')
                return
            }
            
            this.loading = true
            try {
                const { data } = await api.post('/maintenance/quick-start', {
                    moto_id: this.motorcycle.id,
                    current_mileage: this.form.currentMileage,
                    drive_type: this.form.driveType,
                    style: this.form.style,
                    terrain: this.form.terrain
                })
                
                this.createdCount = data.created?.length || 0
                this.step = 4
                this.$emit('created', data)
                this.$toast?.success('Расписание создано!')
            } catch (err) {
                console.error('Quick start failed:', err)
                this.$toast?.error(err.response?.data?.error || 'Ошибка создания')
            } finally {
                this.loading = false
            }
        },
        
        finish() {
            this.$emit('close')
        },
        
        close() {
            this.$emit('close')
        }
    }
}
</script>

<style scoped>
/* ===== ШАГ 1: WELCOME ===== */
.welcome {
    text-align: center;
}

.welcome-icon {
    width: 72px;
    height: 72px;
    margin: 0 auto 16px;
    border-radius: 50%;
    background: var(--accent-trans);
    color: var(--accent-text);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
}

.welcome h3 {
    margin: 0 0 8px;
    font-size: 22px;
    color: var(--text-primary);
}

.welcome p {
    margin: 0 0 20px;
    font-size: 14px;
    color: var(--text-secondary);
    line-height: 1.6;
}

.welcome-features {
    list-style: none;
    padding: 0;
    margin: 0 0 20px;
    text-align: left;
}

.welcome-features li {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 12px;
    font-size: 14px;
    color: var(--text-secondary);
}

.welcome-features li i {
    color: var(--success-text);
    font-size: 16px;
}

/* ===== ШАГ 2: ФОРМА ===== */
.field {
    margin-bottom: 18px;
}

.field:last-child {
    margin-bottom: 0;
}

.field > label {
    display: block;
    font-size: 13px;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 8px;
}

.field > label span {
    color: var(--danger);
}

.input-with-unit {
    position: relative;
    display: flex;
    align-items: center;
}

.input-with-unit input {
    width: 100%;
    padding: 10px 50px 10px 14px;
    background: var(--bg-input);
    border: 2px solid var(--border-color);
    border-radius: 10px;
    color: var(--text-primary);
    font-size: 15px;
    font-weight: 600;
    transition: all 0.2s;
}

.input-with-unit input:focus {
    border-color: var(--accent);
    outline: none;
    box-shadow: 0 0 0 3px var(--accent-trans);
}

.input-with-unit .unit {
    position: absolute;
    right: 14px;
    font-size: 13px;
    color: var(--text-muted);
    pointer-events: none;
}

.field-hint {
    margin: 6px 0 0;
    font-size: 12px;
    color: var(--text-muted);
}

/* ===== RADIO CARDS ===== */
.radio-group {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
}

.radio-group.vertical {
    grid-template-columns: 1fr;
}

.radio-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 12px 10px;
    background: var(--bg-secondary);
    border: 2px solid var(--border-light);
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s;
    color: var(--text-secondary);
    font-size: 13px;
    font-weight: 500;
    text-align: center;
}

.radio-group.vertical .radio-card {
    flex-direction: row;
    justify-content: flex-start;
    text-align: left;
    padding: 12px 16px;
    gap: 14px;
}

.radio-card:hover {
    border-color: var(--border-color);
    background: var(--bg-card-hover);
}

.radio-card.active {
    border-color: var(--accent);
    background: var(--accent-trans);
    color: var(--accent-text);
}

.radio-card i {
    font-size: 18px;
}

.radio-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
    flex: 1;
}

.radio-title {
    font-size: 14px;
    font-weight: 600;
}

.radio-desc {
    font-size: 12px;
    color: var(--text-muted);
    font-weight: 400;
}

.radio-card.active .radio-desc {
    color: var(--accent-text);
    opacity: 0.8;
}

/* ===== ШАГ 3: ПРЕДПРОСМОТР ===== */
.preview-intro {
    margin: 0 0 16px;
    font-size: 14px;
    color: var(--text-secondary);
}

.preview-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 16px;
}

.preview-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 14px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: 10px;
}

.preview-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
    background: var(--accent-trans);
    color: var(--accent-text);
}

.preview-icon.engine { background: var(--accent-trans); color: var(--accent-text); }
.preview-icon.drive { background: var(--warning-trans); color: var(--warning-text); }
.preview-icon.wheel { background: var(--success-trans); color: var(--success-text); }
.preview-icon.brakes { background: var(--danger-trans); color: var(--danger-text); }

.preview-content {
    flex: 1;
    min-width: 0;
}

.preview-title {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-primary);
    margin-bottom: 2px;
}

.preview-meta {
    display: flex;
    gap: 12px;
    font-size: 12px;
    color: var(--text-muted);
}

.preview-meta i {
    font-size: 11px;
}

/* ===== ШАГ 4: SUCCESS ===== */
.success {
    text-align: center;
    padding: 8px 0;
}

.success-icon {
    font-size: 64px;
    color: var(--success-text);
    margin-bottom: 12px;
    animation: popIn 0.5s ease;
}

@keyframes popIn {
    0% { transform: scale(0); }
    50% { transform: scale(1.15); }
    100% { transform: scale(1); }
}

.success h3 {
    margin: 0 0 8px;
    font-size: 22px;
    color: var(--text-primary);
}

.success p {
    margin: 0 0 20px;
    font-size: 14px;
    color: var(--text-secondary);
}

.success-stats {
    display: flex;
    justify-content: center;
    gap: 32px;
    margin-bottom: 20px;
    padding: 16px;
    background: var(--bg-secondary);
    border-radius: 12px;
}

.success-stat {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.success-stat .stat-value {
    font-size: 26px;
    font-weight: 700;
    color: var(--accent-text);
}

.success-stat .stat-label {
    font-size: 12px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.success-hint {
    font-size: 13px;
    color: var(--text-muted);
    font-style: italic;
    margin: 0;
}

/* ===== INFO BOX ===== */
.info-box {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 12px 16px;
    border-radius: 10px;
    font-size: 13px;
    line-height: 1.5;
}

.info-box.info {
    background: var(--accent-trans);
    color: var(--text-secondary);
}

.info-box i {
    color: var(--accent-text);
    font-size: 18px;
    flex-shrink: 0;
    margin-top: 1px;
}

/* ===== ACTIONS ===== */
.actions {
    display: flex;
    gap: 10px;
}

.actions .btn {
    flex: 1;
    padding: 10px 16px;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 600;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
}

.actions .btn:disabled {
    opacity: 0.5;
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

.btn-secondary:hover {
    background: var(--border-color);
}

.btn-success {
    background: var(--success);
    color: #fff;
}

.btn-success:hover {
    background: var(--success-hover);
    transform: translateY(-2px);
}

/* ===== АДАПТИВ ===== */
@media (max-width: 640px) {
    .welcome-icon {
        width: 60px;
        height: 60px;
        font-size: 26px;
    }

    .welcome h3 {
        font-size: 19px;
    }

    .radio-group {
        grid-template-columns: repeat(3, 1fr);
        gap: 6px;
    }

    .radio-card {
        padding: 10px 6px;
        font-size: 12px;
    }

    .radio-card i {
        font-size: 16px;
    }

    .actions {
        flex-direction: column-reverse;
    }

    .actions .btn {
        width: 100%;
    }

    .success-icon {
        font-size: 52px;
    }

    .success-stats {
        gap: 20px;
        padding: 12px;
    }

    .success-stat .stat-value {
        font-size: 22px;
    }
}
</style>