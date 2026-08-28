<template>
    <ModalWrapper
        :isOpen="isOpen"
        :title="manual?.title || 'Мануал'"
        :subtitle="manual?.motorcycle || 'Мотоцикл'"
        icon="book"
        bg-icon-color="var(--accent-trans)"
        icon-color="var(--accent-text)"
        size="lg"
        @close="$emit('close')"
    >
        <!-- ===== СТАТУС И МЕТА ===== -->
        <div class="manual-meta">
            <div class="manual-meta-left">
                <span
                    class="status-badge"
                    :class="{
                        'status-approved': manual?.status === 'approved',
                        'status-moderate': manual?.status === 'moderate',
                        'status-rejected': manual?.status === 'rejected',
                        'status-draft': manual?.status === 'draft'
                    }"
                >
                    <i :class="statusIcon"></i>
                    {{ getStatusLabel(manual?.status) }}
                </span>
                <span v-if="manual?.created_at" class="meta-date">
                    <i class="fa fa-calendar"></i> {{ formatDate(manual.created_at) }}
                </span>
            </div>
            <div v-if="manual?.views" class="manual-meta-right">
                <span class="meta-views">
                    <i class="fa fa-eye"></i> {{ manual.views }}
                </span>
            </div>
        </div>

        <!-- ===== БЛОК 1: ОПИСАНИЕ И МЕТА ===== -->
        <div class="block block-about">
            <p v-if="manual?.description" class="manual-description">
                {{ manual.description }}
            </p>

            <div class="about-meta">
                <div v-if="manual?.time_estimate" class="about-item">
                    <i class="fa fa-clock"></i>
                    <span><strong>Время:</strong> {{ manual.time_estimate }}</span>
                </div>
                <div v-if="manual?.interval" class="about-item">
                    <i class="fa fa-repeat"></i>
                    <span><strong>Периодичность:</strong> {{ manual.interval }}</span>
                </div>
                <div v-if="manual?.difficult" class="about-item">
                    <i class="fa fa-signal"></i>
                    <span><strong>Сложность:</strong> {{ getDifficulty(manual.difficult) }}</span>
                </div>
                <div v-if="manual?.category" class="about-item">
                    <i class="fa fa-tags"></i>
                    <span><strong>Категория:</strong> {{ getCategory(manual.category) }}</span>
                </div>
            </div>
        </div>

        <!-- ===== БЛОК 2: БЕЗОПАСНОСТЬ ===== -->
        <div v-if="manual?.safety_tip || manual?.warnings || manual?.conditions" class="block block-safety">
            <h4 class="block-title">
                <i class="fa fa-shield"></i> Безопасность и подготовка
            </h4>
            
            <div v-if="manual?.safety_tip" class="safety-item safety-tip">
                <i class="fa fa-lightbulb"></i>
                <span>{{ manual.safety_tip }}</span>
            </div>
            
            <div v-if="manual?.warnings" class="safety-item safety-warning">
                <i class="fa fa-exclamation-triangle"></i>
                <span>{{ manual.warnings }}</span>
            </div>
            
            <div v-if="manual?.conditions" class="safety-item safety-condition">
                <i class="fa fa-check-circle"></i>
                <span>{{ manual.conditions }}</span>
            </div>
        </div>

        <!-- ===== БЛОК 3: ИНСТРУМЕНТЫ И МАТЕРИАЛЫ ===== -->
        <div v-if="manual?.instruments || manual?.parts" class="block block-tools">
            <h4 class="block-title">
                <i class="fa fa-wrench"></i> Инструменты и материалы
            </h4>
            
            <div class="tools-grid">
                <div v-if="manual?.instruments" class="tools-item">
                    <i class="fa fa-wrench"></i>
                    <div>
                        <span class="tools-label">Инструменты</span>
                        <span class="tools-value">{{ manual.instruments }}</span>
                    </div>
                </div>
                
                <div v-if="manual?.parts" class="tools-item">
                    <i class="fa fa-cogs"></i>
                    <div>
                        <span class="tools-label">Материалы и запчасти</span>
                        <span class="tools-value">{{ manual.parts }}</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- ===== БЛОК 4: ССЫЛКИ НА ДОКУМЕНТАЦИЮ ===== -->
        <div v-if="manual?.docs_links && manual.docs_links.length > 0" class="block block-docs">
            <h4 class="block-title">
                <i class="fa fa-link"></i> Ссылки на документацию
            </h4>
            
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
        <div v-if="manual?.specs && hasSpecs(manual.specs)" class="block block-specs">
            <h4 class="block-title">
                <i class="fa fa-table"></i> Технические данные
            </h4>

            <!-- Моменты затяжки -->
            <div v-if="manual.specs.torque && manual.specs.torque.length > 0" class="specs-section">
                <h5 class="specs-subtitle">Моменты затяжки</h5>
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
                <h5 class="specs-subtitle">Объёмы жидкостей</h5>
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
                <h5 class="specs-subtitle">Допуски и зазоры</h5>
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
        <div v-if="manual?.steps && manual.steps.length > 0" class="block block-steps">
            <div class="steps-header">
                <h4 class="block-title" style="margin: 0;">
                    <i class="fa fa-list-ol"></i> Шаги выполнения
                </h4>
                <span class="steps-count">{{ manual.steps.length }} шаг{{ manual.steps.length > 1 ? 'а' : '' }}</span>
            </div>

            <div class="steps-list">
                <div 
                    v-for="(step, index) in manual.steps" 
                    :key="index"
                    class="step-item"
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
        <div v-if="manual?.aftercare" class="block block-aftercare">
            <h4 class="block-title">
                <i class="fa fa-check-circle"></i> После завершения
            </h4>
            
            <div class="aftercare-content">
                <i class="fa fa-info-circle"></i>
                <span>{{ manual.aftercare }}</span>
            </div>
        </div>

        <!-- ===== ПУСТОЕ СОСТОЯНИЕ ===== -->
        <div v-if="!manual?.steps || manual.steps.length === 0" class="empty-steps">
            <i class="fa fa-file-text"></i>
            <p>Нет шагов для отображения</p>
        </div>

        <!-- ===== ДЕЙСТВИЯ ===== -->
        <template #actions>
            <div class="modal-actions">
                <button class="btn btn-primary" @click="openFullManual">
                    <i class="fa fa-book"></i> Открыть инструкцию
                </button>
                <button class="btn btn-secondary" @click="$emit('close')">
                    <i class="fa fa-times"></i> Закрыть
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
        },
        manual: {
            type: Object,
            required: true,
            default: null
        },
        canEdit: {
            type: Boolean,
            default: false
        }
    },

    emits: ['close', 'edit'],

    computed: {
        statusIcon() {
            const icons = {
                'approved': 'fa fa-check-circle',
                'moderate': 'fa fa-hourglass-half',
                'rejected': 'fa fa-times-circle',
                'draft': 'fa fa-pencil'
            }
            return icons[this.manual?.status] || 'fa-circle'
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
                    month: 'long',
                    year: 'numeric'
                })
            } catch {
                return '—'
            }
        },

        getStatusLabel(status) {
            const labels = {
                'approved': 'Одобрен',
                'moderate': 'На проверке',
                'rejected': 'Отклонён',
                'draft': 'Черновик'
            }
            return labels[status] || status || '—'
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
            }
            return categories[category] || category
        },

        getDifficulty(difficult) {
            const difficulties = {
                'easy': 'Лёгкая',
                'medium': 'Средняя',
                'hard': 'Сложная'
            }
            return difficulties[difficult] || difficult
        },

        hasSpecs(specs) {
            if (!specs) return false
            return !!(specs.torque?.length > 0 || specs.fluids || specs.tolerances)
        },

        getFluidLabel(key) {
            const labels = {
                'oil': 'Моторное масло',
                'coolant': 'Охлаждающая жидкость',
                'brake': 'Тормозная жидкость',
                'fork': 'Масло в вилке',
                'gear': 'Масло в КПП',
                'chain': 'Смазка цепи'
            }
            return labels[key] || key
        },

        getToleranceLabel(key) {
            const labels = {
                'chain': 'Зазор цепи',
                'valve': 'Зазор клапанов',
                'spark': 'Зазор свечи',
                'brake': 'Толщина колодок',
                'tire': 'Давление в шинах'
            }
            return labels[key] || key
        },

        // ===== РАБОТА С ИЗОБРАЖЕНИЯМИ =====
        getImageUrl(path) {
            if (!path) return ''
            if (path.startsWith('http://') || path.startsWith('https://')) {
                return path
            }
            // Для локальных файлов из папки uploads
            if (path.startsWith('/')) {
                return path
            }
            return `/uploads/${path}`
        },

        openFullManual() {
           if (this.manual?.id) {
                this.$router.push(`/manual/${this.manual.id}`);
                this.$emit('close');
            }
        }
    }
}
</script>

<style scoped>
/* ===== БЛОКИ ===== */
.block {
    margin-bottom: 20px;
    padding: 16px 18px;
    background: var(--bg-secondary);
    border-radius: 12px;
    border: 1px solid var(--border-color);
}

.block:last-child {
    margin-bottom: 0;
}

.block-title {
    font-size: 15px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0 0 12px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.block-title i {
    color: var(--accent-text);
}

/* ===== БЛОК 1: О МАНУАЛЕ ===== */
.manual-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 12px;
}

.manual-meta-left {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}

.manual-meta-right {
    display: flex;
    align-items: center;
    gap: 10px;
}

.status-badge {
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

.meta-date,
.meta-views {
    font-size: 13px;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 4px;
}

.manual-description {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0 0 12px 0;
    line-height: 1.6;
}

.about-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
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
    width: 16px;
}

/* ===== БЛОК 2: БЕЗОПАСНОСТЬ ===== */
.safety-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 10px 14px;
    border-radius: 8px;
    margin-bottom: 8px;
    font-size: 14px;
    line-height: 1.5;
}

.safety-item:last-child {
    margin-bottom: 0;
}

.safety-item i {
    font-size: 16px;
    margin-top: 1px;
    flex-shrink: 0;
}

.safety-tip {
    background: var(--accent-trans);
    border-left: 3px solid var(--accent);
}

.safety-tip i {
    color: var(--accent-text);
}

.safety-warning {
    background: var(--danger-trans);
    border-left: 3px solid var(--danger);
}

.safety-warning i {
    color: var(--danger);
}

.safety-condition {
    background: var(--success-trans);
    border-left: 3px solid var(--success);
}

.safety-condition i {
    color: var(--success-text);
}

/* ===== БЛОК 3: ИНСТРУМЕНТЫ ===== */
.tools-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}

.tools-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 10px 14px;
    background: var(--bg-card);
    border-radius: 8px;
    border: 1px solid var(--border-color);
}

.tools-item i {
    font-size: 18px;
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
    gap: 8px;
}

.docs-link {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    color: var(--accent-text);
    text-decoration: none;
    transition: all 0.2s;
}

.docs-link:hover {
    border-color: var(--accent);
    background: var(--accent-trans);
}

.docs-link i:first-child {
    font-size: 20px;
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
    margin-top: 12px;
}

.specs-section:first-child {
    margin-top: 0;
}

.specs-subtitle {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-secondary);
    margin: 0 0 8px 0;
}

.torque-table {
    display: flex;
    flex-direction: column;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    overflow: hidden;
}

.torque-header {
    display: grid;
    grid-template-columns: 2fr 1fr 2fr;
    padding: 8px 14px;
    background: var(--bg-card);
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    color: var(--text-muted);
    letter-spacing: 0.5px;
}

.torque-row {
    display: grid;
    grid-template-columns: 2fr 1fr 2fr;
    padding: 8px 14px;
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
    gap: 8px;
}

.fluid-item {
    display: flex;
    justify-content: space-between;
    padding: 8px 14px;
    background: var(--bg-card);
    border-radius: 8px;
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
    gap: 8px;
}

.tolerance-item {
    display: flex;
    justify-content: space-between;
    padding: 8px 14px;
    background: var(--bg-card);
    border-radius: 8px;
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
    margin-bottom: 12px;
}

.steps-count {
    font-size: 13px;
    color: var(--text-secondary);
    background: var(--bg-card);
    padding: 2px 12px;
    border-radius: 20px;
    border: 1px solid var(--border-color);
}

.steps-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.step-item {
    display: flex;
    gap: 14px;
    padding: 16px 18px;
    background: var(--bg-card);
    border-radius: 12px;
    border: 1px solid var(--border-color);
    transition: all 0.2s ease;
}

.step-item:hover {
    border-color: var(--accent-trans);
}

.step-marker {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-shrink: 0;
}

.step-number {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--accent);
    border-radius: 50%;
    font-size: 13px;
    font-weight: 700;
    color: #fff;
    flex-shrink: 0;
}

.step-line {
    width: 2px;
    flex: 1;
    min-height: 16px;
    background: var(--border-color);
    margin: 4px 0;
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
    margin-bottom: 4px;
}

.step-title {
    font-size: 15px;
    font-weight: 600;
    color: var(--text-primary);
}

.step-text {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 4px 0 8px 0;
    line-height: 1.6;
}

.step-image {
    margin: 8px 0;
    border-radius: 8px;
    overflow: hidden;
    max-width: 100%;
}

.step-image img {
    width: 100%;
    max-height: 250px;
    object-fit: cover;
    border-radius: 8px;
    border: 1px solid var(--border-color);
}

.step-meta {
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin-top: 8px;
}

.step-warning,
.step-tip,
.step-result {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 13px;
    line-height: 1.4;
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
    gap: 10px;
    padding: 12px 16px;
    background: var(--bg-card);
    border-radius: 8px;
    border: 1px solid var(--border-color);
    font-size: 14px;
    line-height: 1.6;
    color: var(--text-secondary);
}

.aftercare-content i {
    font-size: 18px;
    color: var(--accent-text);
    margin-top: 1px;
    flex-shrink: 0;
}

/* ===== ПУСТОЕ СОСТОЯНИЕ ===== */
.empty-steps {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 32px 20px;
    background: var(--bg-secondary);
    border-radius: 12px;
    border: 2px dashed var(--border-color);
    text-align: center;
}

.empty-steps i {
    font-size: 28px;
    color: var(--text-muted);
    margin-bottom: 10px;
    opacity: 0.5;
}

.empty-steps p {
    color: var(--text-muted);
    font-size: 14px;
    margin: 0;
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

.btn-secondary {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}

.btn-secondary:hover {
    background: var(--border-color);
}

/* ============================================ */
/* ===== АДАПТИВНОСТЬ ===== */
/* ============================================ */

@media (max-width: 768px) {
    .tools-grid {
        grid-template-columns: 1fr;
    }

    .torque-header,
    .torque-row {
        grid-template-columns: 1fr 1fr 1fr;
        font-size: 12px;
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
        gap: 8px;
        padding: 14px;
    }

    .step-marker {
        flex-direction: row;
        gap: 8px;
    }

    .step-line {
        display: none !important;
    }

    .about-meta {
        flex-direction: column;
        gap: 8px;
    }

    .modal-actions {
        flex-direction: column;
    }

    .modal-actions .btn {
        width: 100%;
        padding: 0.8rem;
    }
}

@media (max-width: 480px) {
    .block {
        padding: 12px 14px;
    }

    .manual-meta {
        flex-direction: column;
        align-items: flex-start;
    }

    .manual-meta-right {
        width: 100%;
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

    .status-badge {
        font-size: 11px;
        padding: 3px 10px;
    }

    .step-title {
        font-size: 14px;
    }

    .step-text {
        font-size: 13px;
    }

    .safety-item {
        font-size: 13px;
        padding: 8px 12px;
    }
}
</style>