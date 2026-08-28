<template>
    <div class="container">
        <LoadingOverlay :isLoading="loading" text="Загрузка мануала..." />

        <!-- ХЕДЕР -->
        <Header
            title="Инструкция"
            subtitle="Пошаговое руководство по выполнению процедуры"
        />

        <!-- МАНУАЛ -->
        <section v-if="manual" class="manual-section">
            <!-- ===== НАВИГАЦИЯ ===== -->
            <div class="manual-nav">
                <button class="btn btn-secondary btn-sm" @click="goBack">
                    <i class="fa fa-arrow-left"></i> Назад
                </button>
                <div class="manual-nav-right">
                    <span class="manual-status" :class="statusClass">
                        <i :class="statusIcon"></i>
                        {{ getStatusLabel(manual.status) }}
                    </span>
                </div>
            </div>

            <!-- ===== БЛОК 1: О МАНУАЛЕ ===== -->
            <div class="block block-about">
                <h1 class="manual-title">{{ manual.title }}</h1>
                
                <p v-if="manual.description" class="manual-description">
                    {{ manual.description }}
                </p>

                <div class="about-meta">
                    <div v-if="manual.motorcycle" class="about-item">
                        <i class="fa fa-motorcycle"></i>
                        <span><strong>Мотоцикл:</strong> {{ manual.motorcycle }}</span>
                    </div>
                    <div v-if="manual.time_estimate" class="about-item">
                        <i class="fa fa-clock"></i>
                        <span><strong>Время:</strong> {{ manual.time_estimate }}</span>
                    </div>
                    <div v-if="manual.interval" class="about-item">
                        <i class="fa fa-repeat"></i>
                        <span><strong>Периодичность:</strong> {{ manual.interval }}</span>
                    </div>
                    <div v-if="manual.difficult" class="about-item">
                        <i class="fa fa-signal"></i>
                        <span><strong>Сложность:</strong> 
                            <span class="difficulty-dots">
                                <span class="dot" :class="{ filled: ['easy', 'medium', 'hard'].includes(manual.difficult) }"></span>
                                <span class="dot" :class="{ filled: ['medium', 'hard'].includes(manual.difficult) }"></span>
                                <span class="dot" :class="{ filled: manual.difficult === 'hard' }"></span>
                            </span>
                            {{ getDifficulty(manual.difficult) }}
                        </span>
                    </div>
                    <div v-if="manual.category" class="about-item">
                        <i class="fa fa-tags"></i>
                        <span><strong>Категория:</strong> {{ getCategory(manual.category) }}</span>
                    </div>
                    <div v-if="manual.author?.username" class="about-item">
                        <i class="fa fa-user"></i>
                        <span><strong>Автор:</strong> {{ manual.author.username }}</span>
                    </div>
                    <div v-if="manual.created_at" class="about-item">
                        <i class="fa fa-calendar"></i>
                        <span><strong>Создан:</strong> {{ formatDate(manual.created_at) }}</span>
                    </div>
                </div>
            </div>

            <!-- ===== БЛОК 2: БЕЗОПАСНОСТЬ ===== -->
            <div v-if="manual.safety_tip || manual.warnings || manual.conditions" class="block block-safety">
                <h3 class="block-title">
                    <i class="fa fa-shield"></i> Безопасность и подготовка
                </h3>
                
                <div v-if="manual.safety_tip" class="safety-item safety-tip">
                    <i class="fa fa-lightbulb"></i>
                    <span>{{ manual.safety_tip }}</span>
                </div>
                
                <div v-if="manual.warnings" class="safety-item safety-warning">
                    <i class="fa fa-exclamation-triangle"></i>
                    <span>{{ manual.warnings }}</span>
                </div>
                
                <div v-if="manual.conditions" class="safety-item safety-condition">
                    <i class="fa fa-check-circle"></i>
                    <span>{{ manual.conditions }}</span>
                </div>
            </div>

            <!-- ===== БЛОК 3: ИНСТРУМЕНТЫ И МАТЕРИАЛЫ ===== -->
            <div v-if="manual.instruments || manual.parts" class="block block-tools">
                <h3 class="block-title">
                    <i class="fa fa-wrench"></i> Инструменты и материалы
                </h3>
                
                <div class="tools-grid">
                    <div v-if="manual.instruments" class="tools-item">
                        <i class="fa fa-wrench"></i>
                        <div>
                            <span class="tools-label">Инструменты</span>
                            <span class="tools-value">{{ manual.instruments }}</span>
                        </div>
                    </div>
                    
                    <div v-if="manual.parts" class="tools-item">
                        <i class="fa fa-cogs"></i>
                        <div>
                            <span class="tools-label">Материалы и запчасти</span>
                            <span class="tools-value">{{ manual.parts }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ===== БЛОК 4: ССЫЛКИ НА ДОКУМЕНТАЦИЮ ===== -->
            <div v-if="manual.docs_links && manual.docs_links.length > 0" class="block block-docs">
                <h3 class="block-title">
                    <i class="fa fa-link"></i> Ссылки на документацию
                </h3>
                
                <div class="docs-list">
                    <a 
                        v-for="(link, index) in manual.docs_links" 
                        :key="index"
                        :href="link"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="docs-link"
                    >
                        <i class="fa fa-file-pdf"></i>
                        <span>Документация {{ index + 1 }}</span>
                        <i class="fa fa-external-link"></i>
                    </a>
                </div>
            </div>

            <!-- ===== БЛОК 5: ТЕХНИЧЕСКИЕ ДАННЫЕ ===== -->
            <div v-if="manual.specs && hasSpecs(manual.specs)" class="block block-specs">
                <h3 class="block-title">
                    <i class="fa fa-table"></i> Технические данные
                </h3>

                <!-- Моменты затяжки -->
                <div v-if="manual.specs.torque && manual.specs.torque.length > 0" class="specs-section">
                    <h4 class="specs-subtitle">Моменты затяжки</h4>
                    <div class="torque-table">
                        <div class="torque-header">
                            <span>Название</span>
                            <span>Момент (Н·м)</span>
                            <span>Примечание</span>
                        </div>
                        <div 
                            v-for="(item, index) in manual.specs.torque" 
                            :key="index"
                            class="torque-row"
                        >
                            <span>{{ item.name || '—' }}</span>
                            <span>{{ item.nm || '—' }}</span>
                            <span>{{ item.note || '—' }}</span>
                        </div>
                    </div>
                </div>

                <!-- Объёмы жидкостей -->
                <div v-if="manual.specs.fluids" class="specs-section">
                    <h4 class="specs-subtitle">Объёмы жидкостей</h4>
                    <div class="fluids-grid">
                        <div 
                            v-for="(value, key) in manual.specs.fluids" 
                            :key="key"
                            class="fluid-item"
                        >
                            <span class="fluid-label">{{ getFluidLabel(key) }}</span>
                            <span class="fluid-value">{{ value }}</span>
                        </div>
                    </div>
                </div>

                <!-- Допуски и зазоры -->
                <div v-if="manual.specs.tolerances" class="specs-section">
                    <h4 class="specs-subtitle">Допуски и зазоры</h4>
                    <div class="tolerances-grid">
                        <div 
                            v-for="(value, key) in manual.specs.tolerances" 
                            :key="key"
                            class="tolerance-item"
                        >
                            <span class="tolerance-label">{{ getToleranceLabel(key) }}</span>
                            <span class="tolerance-value">{{ value }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ===== БЛОК 6: ШАГИ ===== -->
            <div v-if="manual.steps && manual.steps.length > 0" class="block block-steps">
                <div class="steps-header">
                    <h3 class="block-title" style="margin: 0;">
                        <i class="fa fa-list-ol"></i> Шаги выполнения
                    </h3>
                    <span class="steps-count">{{ manual.steps.length }} шаг{{ manual.steps.length > 1 ? 'а' : '' }}</span>
                </div>

                <div class="steps-list">
                    <div 
                        v-for="(step, index) in manual.steps" 
                        :key="index"
                        class="step-item"
                        :class="{ 'step-completed': step.completed }"
                    >
                        <div class="step-marker">
                            <span class="step-number">{{ step.order || index + 1 }}</span>
                            <div class="step-line" v-if="index < manual.steps.length - 1"></div>
                        </div>
                        
                        <div class="step-body">
                            <div class="step-header-inner">
                                <span class="step-title">{{ step.title }}</span>
                            </div>
                            
                            <p v-if="step.text" class="step-text">{{ step.text }}</p>
                            
                            <div v-if="step.image" class="step-image">
                                <img :src="getImageUrl(step.image)" :alt="step.title" loading="lazy" />
                            </div>
                            
                            <div class="step-meta">
                                <div v-if="step.warning" class="step-warning">
                                    <i class="fa fa-exclamation-triangle"></i>
                                    <span>{{ step.warning }}</span>
                                </div>
                                <div v-if="step.tip" class="step-tip">
                                    <i class="fa fa-lightbulb"></i>
                                    <span>{{ step.tip }}</span>
                                </div>
                                <div v-if="step.result" class="step-result">
                                    <i class="fa fa-check-circle"></i>
                                    <span>{{ step.result }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ===== БЛОК 7: ПОСЛЕ ЗАВЕРШЕНИЯ ===== -->
            <div v-if="manual.aftercare" class="block block-aftercare">
                <h3 class="block-title">
                    <i class="fa fa-check-circle"></i> После завершения
                </h3>
                
                <div class="aftercare-content">
                    <i class="fa fa-info-circle"></i>
                    <span>{{ manual.aftercare }}</span>
                </div>
            </div>

            <!-- ===== СОВЕТ ===== -->
            <div v-if="manual.tip" class="block block-tip">
                <h3 class="block-title">
                    <i class="fa fa-lightbulb"></i> Совет
                </h3>
                
                <div class="tip-content">
                    <i class="fa fa-quote-left"></i>
                    <span>{{ manual.tip }}</span>
                </div>
            </div>

            <!-- ===== ПУСТОЕ СОСТОЯНИЕ ===== -->
            <div v-if="!manual.steps || manual.steps.length === 0" class="empty-steps">
                <i class="fa fa-file-text"></i>
                <p>Нет шагов для отображения</p>
            </div>
        </section>

        <!-- === ЗАГРУЗКА === -->
        <section v-else-if="loading" class="empty-section">
            <div class="empty-state">
                <div class="empty-icon">
                    <i class="fa fa-spinner fa-spin"></i>
                </div>
                <h3>Загрузка...</h3>
            </div>
        </section>

        <!-- === НЕ НАЙДЕН === -->
        <section v-else class="empty-section">
            <div class="empty-state">
                <div class="empty-icon warning">
                    <i class="fa fa-file-text"></i>
                </div>
                <h3>Мануал не найден</h3>
                <p>Запрашиваемый мануал не существует или был удалён</p>
                <button class="outline-btn" @click="goBack">
                    <i class="fa fa-arrow-left"></i> Вернуться назад
                </button>
            </div>
        </section>
    </div>
</template>

<script>
import api from '../api/api';
import Header from '../components/Header.vue';
import LoadingOverlay from '../components/LoadingOverlay.vue';

export default {
    name: 'ManualView',
    components: { Header, LoadingOverlay },

    data() {
        return {
            loading: true,
            manual: null,
            error: null
        };
    },

    computed: {
        statusClass() {
            if (!this.manual) return '';
            const classes = {
                'approved': 'status-approved',
                'moderate': 'status-moderate',
                'rejected': 'status-rejected',
                'draft': 'status-draft'
            };
            return classes[this.manual.status] || '';
        },

        statusIcon() {
            if (!this.manual) return 'fa-circle';
            const icons = {
                'approved': 'fa fa-check-circle',
                'moderate': 'fa fa-hourglass-half',
                'rejected': 'fa fa-times-circle',
                'draft': 'fa fa-pencil'
            };
            return icons[this.manual.status] || 'fa-circle';
        }
    },

    mounted() {
        const manualId = this.$route.params.id;
        if (manualId) {
            this.loadManual(manualId);
        } else {
            this.loading = false;
            this.error = 'ID мануала не указан';
        }
    },

    methods: {
        async loadManual(id) {
            this.loading = true;
            try {
                const response = await api.get(`/manual/${id}`);
                this.manual = response.data;
                
                // Сортируем шаги
                if (this.manual.steps) {
                    this.manual.steps = [...this.manual.steps].sort((a, b) => (a.order || 0) - (b.order || 0));
                }
            } catch (error) {
                console.error('Ошибка загрузки мануала:', error);
                this.error = error.response?.data?.message || 'Мануал не найден';
                if (error.response?.status === 401) {
                    this.$router.push('/login');
                }
            } finally {
                this.loading = false;
            }
        },

        goBack() {
            this.$router.back();
        },

        formatDate(dateString) {
            if (!dateString) return '—';
            try {
                const date = new Date(dateString);
                if (isNaN(date.getTime())) return '—';
                return date.toLocaleDateString('ru-RU', {
                    day: '2-digit',
                    month: 'long',
                    year: 'numeric'
                });
            } catch {
                return '—';
            }
        },

        getStatusLabel(status) {
            const labels = {
                'approved': 'Одобрен',
                'moderate': 'На проверке',
                'rejected': 'Отклонён',
                'draft': 'Черновик'
            };
            return labels[status] || status || '—';
        },

        getCategory(category) {
            const categories = {
                'engine': 'Двигатель',
                'drive': 'Привод',
                'steering': 'Рулевое управление',
                'suspension': 'Подвеска',
                'electronics': 'Электроника',
                'wheel': 'Колеса / Шины',
                'brakes': 'Тормозная система',
                'fuel': 'Топливная система',
                'cooling': 'Система охлаждения'
            };
            return categories[category] || category;
        },

        getDifficulty(difficult) {
            const difficulties = {
                'easy': 'Лёгкая',
                'medium': 'Средняя',
                'hard': 'Сложная'
            };
            return difficulties[difficult] || difficult;
        },

        hasSpecs(specs) {
            if (!specs) return false;
            return !!(specs.torque?.length > 0 || specs.fluids || specs.tolerances);
        },

        getFluidLabel(key) {
            const labels = {
                'oil': 'Моторное масло',
                'coolant': 'Охлаждающая жидкость',
                'brake': 'Тормозная жидкость',
                'fork': 'Масло в вилке',
                'gear': 'Масло в КПП',
                'chain': 'Смазка цепи'
            };
            return labels[key] || key;
        },

        getToleranceLabel(key) {
            const labels = {
                'chain': 'Зазор цепи',
                'valve': 'Зазор клапанов',
                'spark': 'Зазор свечи',
                'brake': 'Толщина колодок',
                'tire': 'Давление в шинах'
            };
            return labels[key] || key;
        },

        getImageUrl(path) {
            if (!path) return '';
            if (path.startsWith('http://') || path.startsWith('https://')) {
                return path;
            }
            if (path.startsWith('/')) {
                return path;
            }
            return `/uploads/${path}`;
        }
    }
};
</script>

<style scoped>
.container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 0 20px 40px;
}

/* ===== НАВИГАЦИЯ ===== */
.manual-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    padding: 12px 0;
    border-bottom: 1px solid var(--border-color);
    flex-wrap: wrap;
    gap: 10px;
}

.manual-nav-right {
    display: flex;
    align-items: center;
    gap: 10px;
}

.manual-status {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}

.status-approved {
    background: var(--success-trans);
    color: var(--success-text);
}

.status-moderate {
    background: var(--warning-trans);
    color: var(--warning-text);
}

.status-rejected {
    background: var(--danger-trans);
    color: var(--danger-text);
}

.status-draft {
    background: var(--accent-trans);
    color: var(--accent-text);
}

/* ===== КНОПКИ ===== */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 8px 18px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    border: none;
    cursor: pointer;
    transition: all 0.2s ease;
    text-decoration: none;
}

.btn-sm {
    padding: 6px 14px;
    font-size: 13px;
}

.btn-secondary {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}

.btn-secondary:hover {
    background: var(--border-color);
}

/* ===== БЛОКИ ===== */
.block {
    margin-bottom: 24px;
    padding: 24px 28px;
    background: var(--bg-card);
    border-radius: 16px;
    border: 1px solid var(--border-color);
}

.block:last-child {
    margin-bottom: 0;
}

.block-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0 0 16px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}

.block-title i {
    color: var(--accent-text);
}

/* ===== БЛОК 1: О МАНУАЛЕ ===== */
.manual-title {
    font-size: 28px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 12px 0;
}

.manual-description {
    font-size: 16px;
    color: var(--text-secondary);
    margin: 0 0 16px 0;
    line-height: 1.7;
}

.about-meta {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 8px 24px;
}

.about-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    color: var(--text-secondary);
}

.about-item i {
    color: var(--accent-text);
    width: 18px;
    text-align: center;
}

.difficulty-dots {
    display: inline-flex;
    gap: 4px;
    margin-right: 6px;
    vertical-align: middle;
}

.dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--border-color);
    transition: background 0.3s;
}

.dot.filled {
    background: var(--warning-text);
}

/* ===== БЛОК 2: БЕЗОПАСНОСТЬ ===== */
.safety-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
    border-radius: 10px;
    margin-bottom: 10px;
    font-size: 15px;
    line-height: 1.6;
}

.safety-item:last-child {
    margin-bottom: 0;
}

.safety-item i {
    font-size: 18px;
    margin-top: 2px;
    flex-shrink: 0;
}

.safety-tip {
    background: var(--accent-trans);
    border-left: 4px solid var(--accent);
}

.safety-tip i {
    color: var(--accent-text);
}

.safety-warning {
    background: var(--danger-trans);
    border-left: 4px solid var(--danger);
}

.safety-warning i {
    color: var(--danger);
}

.safety-condition {
    background: var(--success-trans);
    border-left: 4px solid var(--success);
}

.safety-condition i {
    color: var(--success-text);
}

/* ===== БЛОК 3: ИНСТРУМЕНТЫ ===== */
.tools-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}

.tools-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
    background: var(--bg-secondary);
    border-radius: 10px;
    border: 1px solid var(--border-color);
}

.tools-item i {
    font-size: 20px;
    color: var(--accent-text);
    margin-top: 2px;
}

.tools-item div {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.tools-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-muted);
}

.tools-value {
    font-size: 14px;
    color: var(--text-primary);
}

/* ===== БЛОК 4: ССЫЛКИ ===== */
.docs-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.docs-link {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    color: var(--accent-text);
    text-decoration: none;
    transition: all 0.2s;
}

.docs-link:hover {
    border-color: var(--accent);
    background: var(--accent-trans);
}

.docs-link i:first-child {
    font-size: 22px;
    color: var(--danger-text);
}

.docs-link span {
    flex: 1;
    font-size: 14px;
}

.docs-link i:last-child {
    font-size: 14px;
    color: var(--text-muted);
}

/* ===== БЛОК 5: ТЕХНИЧЕСКИЕ ДАННЫЕ ===== */
.specs-section {
    margin-top: 16px;
}

.specs-section:first-child {
    margin-top: 0;
}

.specs-subtitle {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-secondary);
    margin: 0 0 10px 0;
}

.torque-table {
    display: flex;
    flex-direction: column;
    border: 1px solid var(--border-color);
    border-radius: 10px;
    overflow: hidden;
}

.torque-header {
    display: grid;
    grid-template-columns: 2fr 1fr 2fr;
    padding: 10px 16px;
    background: var(--bg-secondary);
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    color: var(--text-muted);
    letter-spacing: 0.5px;
}

.torque-row {
    display: grid;
    grid-template-columns: 2fr 1fr 2fr;
    padding: 10px 16px;
    border-top: 1px solid var(--border-color);
    font-size: 14px;
    color: var(--text-primary);
}

.torque-row:nth-child(even) {
    background: var(--bg-secondary);
}

.fluids-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 10px;
}

.fluid-item {
    display: flex;
    justify-content: space-between;
    padding: 10px 16px;
    background: var(--bg-secondary);
    border-radius: 10px;
    border: 1px solid var(--border-color);
}

.fluid-label {
    font-size: 13px;
    color: var(--text-secondary);
}

.fluid-value {
    font-weight: 600;
    font-size: 14px;
    color: var(--text-primary);
}

.tolerances-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 10px;
}

.tolerance-item {
    display: flex;
    justify-content: space-between;
    padding: 10px 16px;
    background: var(--bg-secondary);
    border-radius: 10px;
    border: 1px solid var(--border-color);
}

.tolerance-label {
    font-size: 13px;
    color: var(--text-secondary);
}

.tolerance-value {
    font-weight: 600;
    font-size: 14px;
    color: var(--text-primary);
}

/* ===== БЛОК 6: ШАГИ ===== */
.steps-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.steps-count {
    font-size: 13px;
    color: var(--text-secondary);
    background: var(--bg-secondary);
    padding: 2px 14px;
    border-radius: 20px;
    border: 1px solid var(--border-color);
}

.steps-list {
    display: flex;
    flex-direction: column;
    gap: 14px;
}

.step-item {
    display: flex;
    gap: 16px;
    padding: 18px 20px;
    background: var(--bg-secondary);
    border-radius: 12px;
    border: 1px solid var(--border-color);
    transition: all 0.2s ease;
}

.step-item:hover {
    border-color: var(--accent-trans);
}

.step-item.step-completed {
    border-color: var(--success);
}

.step-marker {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-shrink: 0;
}

.step-number {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--accent);
    border-radius: 50%;
    font-size: 14px;
    font-weight: 700;
    color: #fff;
    flex-shrink: 0;
}

.step-line {
    width: 2px;
    flex: 1;
    min-height: 20px;
    background: var(--border-color);
    margin: 6px 0;
}

.step-item:last-child .step-line {
    display: none;
}

.step-body {
    flex: 1;
    min-width: 0;
}

.step-header-inner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
}

.step-title {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
}

.step-text {
    font-size: 15px;
    color: var(--text-secondary);
    margin: 0 0 10px 0;
    line-height: 1.7;
}

.step-image {
    margin: 10px 0;
    border-radius: 10px;
    overflow: hidden;
    max-width: 100%;
}

.step-image img {
    width: 100%;
    max-height: 300px;
    object-fit: cover;
    border-radius: 10px;
    border: 1px solid var(--border-color);
}

.step-meta {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-top: 10px;
}

.step-warning,
.step-tip,
.step-result {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 14px;
    line-height: 1.5;
}

.step-warning {
    background: var(--danger-trans);
    color: var(--danger-text);
}

.step-warning i {
    color: var(--danger);
}

.step-tip {
    background: var(--accent-trans);
    color: var(--accent-text);
}

.step-tip i {
    color: var(--accent-text);
}

.step-result {
    background: var(--success-trans);
    color: var(--success-text);
}

.step-result i {
    color: var(--success-text);
}

/* ===== БЛОК 7: ПОСЛЕ ЗАВЕРШЕНИЯ ===== */
.aftercare-content {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 14px 18px;
    background: var(--bg-secondary);
    border-radius: 10px;
    border: 1px solid var(--border-color);
    font-size: 15px;
    line-height: 1.7;
    color: var(--text-secondary);
}

.aftercare-content i {
    font-size: 20px;
    color: var(--accent-text);
    margin-top: 2px;
    flex-shrink: 0;
}

/* ===== СОВЕТ ===== */
.tip-content {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 14px 18px;
    background: var(--warning-trans);
    border-radius: 10px;
    border: 1px solid rgba(245, 158, 11, 0.15);
    font-size: 15px;
    line-height: 1.7;
    color: var(--text-secondary);
}

.tip-content i {
    color: var(--warning-text);
    font-size: 20px;
    margin-top: 2px;
    flex-shrink: 0;
}

/* ===== ПУСТЫЕ СОСТОЯНИЯ ===== */
.empty-steps {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    background: var(--bg-secondary);
    border-radius: 12px;
    border: 2px dashed var(--border-color);
    text-align: center;
}

.empty-steps i {
    font-size: 32px;
    color: var(--text-muted);
    margin-bottom: 12px;
    opacity: 0.5;
}

.empty-steps p {
    color: var(--text-muted);
    font-size: 15px;
    margin: 0;
}

.empty-section {
    margin-top: 40px;
}

.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 40px;
    background: var(--bg-card);
    border-radius: 16px;
    border: 2px dashed var(--border-color);
    text-align: center;
}

.empty-icon {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: rgba(59, 130, 246, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 36px;
    color: #3b82f6;
    margin-bottom: 20px;
}

.empty-icon.warning {
    background: var(--warning-trans);
    color: var(--warning-text);
}

.empty-icon .fa-spin {
    color: var(--accent-text);
}

.empty-state h3 {
    margin: 0 0 8px 0;
    font-size: 22px;
    font-weight: 600;
    color: var(--text-primary);
}

.empty-state p {
    margin: 0 0 20px 0;
    font-size: 16px;
    color: var(--text-secondary);
    max-width: 400px;
}

.outline-btn {
    padding: 10px 28px;
    border: 2px solid var(--accent);
    border-radius: 40px;
    background: transparent;
    color: var(--accent-text);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 14px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.outline-btn:hover {
    background: var(--accent);
    color: #fff;
}

/* ============================================ */
/* ===== АДАПТИВНОСТЬ ===== */
/* ============================================ */

@media (max-width: 768px) {
    .container {
        padding: 0 12px 30px;
    }

    .block {
        padding: 18px 16px;
    }

    .manual-title {
        font-size: 22px;
    }

    .about-meta {
        grid-template-columns: 1fr;
        gap: 6px;
    }

    .tools-grid {
        grid-template-columns: 1fr;
    }

    .torque-header,
    .torque-row {
        grid-template-columns: 1fr 1fr 1fr;
        font-size: 12px;
        padding: 8px 12px;
    }

    .torque-row span {
        font-size: 12px;
    }

    .fluids-grid,
    .tolerances-grid {
        grid-template-columns: 1fr;
    }

    .step-item {
        flex-direction: column;
        gap: 10px;
        padding: 14px 16px;
    }

    .step-marker {
        flex-direction: row;
        gap: 10px;
    }

    .step-number {
        width: 30px;
        height: 30px;
        font-size: 13px;
    }

    .step-line {
        display: none !important;
    }

    .manual-nav {
        flex-direction: column;
        align-items: flex-start;
    }

    .manual-nav-right {
        width: 100%;
    }

    .manual-status {
        width: 100%;
        justify-content: center;
    }
}

@media (max-width: 480px) {
    .block {
        padding: 14px 12px;
    }

    .manual-title {
        font-size: 20px;
    }

    .manual-description {
        font-size: 14px;
    }

    .step-title {
        font-size: 15px;
    }

    .step-text {
        font-size: 14px;
    }

    .safety-item {
        font-size: 14px;
        padding: 10px 12px;
    }

    .torque-header,
    .torque-row {
        grid-template-columns: 1fr 1fr 1fr;
        padding: 6px 10px;
        font-size: 11px;
    }

    .torque-row span {
        font-size: 11px;
    }

    .docs-link {
        padding: 10px 12px;
        font-size: 13px;
    }

    .status-badge {
        font-size: 11px;
        padding: 3px 10px;
    }

    .empty-state {
        padding: 40px 20px;
    }

    .empty-icon {
        width: 60px;
        height: 60px;
        font-size: 28px;
    }

    .empty-state h3 {
        font-size: 18px;
    }

    .empty-state p {
        font-size: 14px;
    }
}
</style>