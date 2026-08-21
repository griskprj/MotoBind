<template>
    <div class="container">
        <LoadingOverlay :isLoading="loading" text="Загрузка данных ремонта..."/>

        <!-- === HEADER === -->
        <Header
            title="Ремонт"
            subtitle="Проводите обслуживание мотоцикла с нашими мануалами"
        />

        <!-- === STATISTIC SECTION === -->
        <section class="section-block">
            <p class="section-title" v-if="manual">
                Обслуживание: {{ manual.title }}
            </p>
            <p class="section-title" v-else>
                Выберите мотоцикл и обслуживание для отображения инструкции
            </p>

            <div class="stat-cards">
                <div class="stat-card">
                    <div class="stat-body">
                        <p class="stat-label">Пробег мотоцикла</p>
                        <p class="stat-value">{{ selectedMotoData ? selectedMotoData.mileage + ' км' : '—' }}</p>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-body">
                        <p class="stat-label">Следующее ТО</p>
                        <p class="stat-value warning-text" v-if="selectedMaintenanceData && selectedMaintenanceData.planned_mileage - selectedMotoData?.mileage > 0">
                            через {{ selectedMaintenanceData.planned_mileage - (selectedMotoData?.mileage || 0) }} км
                        </p>
                        <p class="stat-value danger-text" v-else-if="selectedMaintenanceData && selectedMaintenanceData.planned_mileage - selectedMotoData?.mileage <= 0"">
                            Пора обслуживать
                        </p>
                        <p class="stat-value warning-text" v-else>—</p>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-body">
                        <p class="stat-label">Статус</p>
                        <div class="stat-badge success" v-if="selectedMaintenanceData">Выполняется</div>
                        <div class="stat-badge" v-else style="background: rgba(107,114,128,0.2); color: #9ca3af;">Ожидание</div>
                    </div>
                </div>
            </div>
        </section>

        <!-- === SELECT SECTION === -->
        <section class="section-block">
            <div class="select-cards">
                <div class="select-card">
                    <div class="select-header">
                        <div class="step-badge">1</div>
                        <p>Выберите мотоцикл</p>
                    </div>
                    <select class="styled-select" v-model="selectedMoto" @change="onMotoChange">
                        <option value="">Выберите мотоцикл</option>
                        <option v-for="moto in motorcycles" :key="moto.id" :value="moto.id">
                            {{ moto.name }}
                        </option>
                    </select>
                </div>

                <div class="select-card">
                    <div class="select-header">
                        <div class="step-badge">2</div>
                        <p>Выберите обслуживание</p>
                    </div>
                    <select class="styled-select" v-model="selectedMaintenance" @change="onMaintenanceChange" :disabled="!selectedMoto">
                        <option value="">Выберите обслуживание</option>
                        <option v-for="m in filteredMaintenances" :key="m.id" :value="m.id">
                            {{ m.title }}
                        </option>
                    </select>
                </div>

                <div class="manual-find-card" :class="{ 'not-found': !manual && selectedMoto && selectedMaintenance }">
                    <div class="find-header">
                        <div class="find-badge" v-if="manual"><i class="fa fa-check"></i></div>
                        <div class="find-badge empty" v-else><i class="fa fa-search"></i></div>
                        <div class="find-header-wrapper">
                            <p class="find-title" v-if="manual">Мануал найден</p>
                            <p class="find-title empty-title" v-else>Поиск мануала</p>
                            <p class="find-subtitle" v-if="manual">Подобран автоматически</p>
                            <p class="find-subtitle" v-else>Выберите параметры выше</p>
                        </div>
                    </div>
                    <button @click="removeRepairData" class="outline-btn" v-if="manual">Сменить</button>
                    <button class="outline-btn" disabled v-else>
                        <p v-if="selectedMaintenance && selectedMoto && !manual">
                            Не нашли
                        </p>
                        <p v-if="!selectedMaintenance || !selectedMoto">
                            Ожидание данных
                        </p>
                    </button>
                </div>
            </div>
        </section>

        <!-- === MANUAL INSTRUCTION === -->
        <section class="section-block" v-if="manual">
            <div class="manual-wrapper">
                <div class="manual">
                    <p class="manual-title">Инструкция по ремонту</p>

                    <div class="steps-list">
                        <div class="step" v-for="step in manual.steps" :key="step.order">
                            <div class="step-left">
                                <div class="step-number">{{ step.order }}</div>
                                <div class="step-img" v-if="step.image">
                                    <img :src="step.image" alt="">
                                </div>
                            </div>

                            <div class="step-body">
                                <p class="step-title">{{ step.title }}</p>
                                <p class="step-text">{{ step.text }}</p>
                                <div v-if="step.tip" class="step-tip info">
                                    <i class="fa fa-info-circle"></i>
                                    <p>{{ step.tip }}</p>
                                </div>
                                <div v-if="step.warning" class="step-tip warning">
                                    <i class="fa fa-exclamation-triangle"></i>
                                    <p>{{ step.warning }}</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="manual-tips" v-if="manual.tip">
                        <i class="fa fa-lightbulb"></i>
                        <p class="tip-text"><strong>Совет:</strong> {{ manual.tip }}</p>
                    </div>
                    <div class="manual-tips" v-else>
                        <i class="fa fa-lightbulb"></i>
                        <p class="tip-text"><strong>Совет:</strong> Всегда проверяйте затяжку болтов после обслуживания.</p>
                    </div>
                </div>

                <div class="manual-meta">
                    <div class="meta-card">
                        <p class="meta-title">Необходимые инструменты</p>
                        <ul class="meta-items" v-if="manual.instruments">
                            <li class="meta-item" v-for="item in splitList(manual.instruments)" :key="item">
                                <i class="fa fa-wrench"></i> {{ item }}
                            </li>
                        </ul>
                        <p class="meta-item empty-text" v-else>Не указаны</p>
                    </div>

                    <div class="meta-card">
                        <p class="meta-title">Материалы</p>
                        <ul class="meta-items" v-if="manual.parts">
                            <li class="meta-item" v-for="part in splitList(manual.parts)" :key="part">
                                <i class="fa fa-gear"></i> {{ part }}
                            </li>
                        </ul>
                        <p class="meta-item empty-text" v-else>Не указаны</p>
                    </div>

                    <div class="mark-card">
                        <p class="mark-title">Завершить обслуживание</p>
                        <p class="mark-text">После завершения:</p>
                        <div class="mark-items">
                            <div class="mark-item"><i class="fa fa-check-circle"></i> Запись в историю</div>
                            <div class="mark-item"><i class="fa fa-check-circle"></i> Новое плановое ТО</div>
                        </div>
                        <button class="accept-btn" @click="openMarkModal"><i class="fa fa-check"></i> Завершить</button>
                    </div>
                </div>
            </div>
        </section>
        <section v-if="!selectedMoto || !selectedMaintenance" class="empty-state">
            <div class="empty-header">
                <i class="fa fa-gear"></i>
                <p class="empty-title">Заполните информацию выше</p>
            </div>

            <div class="empty-body">
                <p class="empty-text">
                    Для получения мануала вам необходимо выбрать мотоцикл и небоходимое обслуживание.
                </p>
                <p class="empty-text">
                    Система автоматически подберет для вас мануал, при его наличии в базе.
                </p>
            </div>
        </section>
        <section v-if="selectedMoto && selectedMaintenance && !manual" class="empty-state">
            <div class="empty-header">
                <i class="fa fa-file"></i>
                <p class="empty-title">Мануал не найден</p>
            </div>

            <div class="empty-body">
                <p class="empty-text" style="margin-bottom: 8px;">
                    К сожалению, мы не нашли в нашей базе подходящего для вас мануала. Вы можете нам помочь, создав этот мануал на основе официальной документации. Подробнее ознакомиться с правилами заполнения мануала вы можете <a href="#">здесь</a>.
                </p>
                <button @click="openMarkModal" class="outline-btn">Отметить обслуживание</button>
            </div>
        </section>
    </div>

    <!-- === MODALS === -->
    <MarkPlanMaintenanceModal
        :is-open="showMarkMaintenanceModal"
        :motorcycle="selectedMotoData"
        :maintenance="selectedMaintenanceData"
        @close="showMarkMaintenanceModal=false"
        @submit="markMaintenance"
    />
</template>

<script>
import api from '../api/api'
import MarkPlanMaintenanceModal from '../components/modals/maintenance/MarkPlanMaintenanceModal.vue';
import Header from '../components/Header.vue'
import LoadingOverlay from '../components/LoadingOverlay.vue';

export default {
    components: { MarkPlanMaintenanceModal, Header, LoadingOverlay },
    data() {
        return {
            loading: false,
            overdue_maintenances_count: 0,
            pending_maintenances_count: 0,
            planned_maintenances_count: 0,
            motorcycles: [],
            maintenances: [],
            manual: null,
            selectedMoto: null,
            selectedMaintenance: null,
            selectedMotoData: null,
            selectedMaintenanceData: null,
            dataLoad: false,
            showMarkMaintenanceModal: false,
            welcomeDropdownActive: false,
            lastMaintenanceDate: null,
        }
    },
    computed: {
        filteredMaintenances() {
            if (!this.selectedMoto) return []
            return this.maintenances.filter(m => 
                m.moto_id === this.selectedMoto &&
                (m.status === 'planned' || m.status === 'overdue')
            )
        }
    },
    watch: {
        selectedMoto() {
            this.selectedMaintenance = ''
            this.manual = null
            this.selectedMotoData = this.motorcycles.find(m => m.id === this.selectedMoto) || null
        }
    },
    methods: {
        async loadData() {
            try {
                this.loading = true
                const response = await api.get('/statistic/repair')
                this.motorcycles = response.data.motorcycles
                this.maintenances = response.data.maintenances
                this.overdue_maintenances_count = response.data.overdue
                this.pending_maintenances_count = response.data.soon || 0
                this.planned_maintenances_count = response.data.planned
            } catch (err) {
                console.error('Failed load repair data: ', err)
            } finally {
                this.loading = false
            }
        },
        onMotoChange() {
            this.selectedMaintenance = '';
            this.manual = null;
            this.selectedMaintenanceData = null;
            this.lastMaintenanceDate = null;
        },
        onMaintenanceChange() {
            if (this.selectedMoto && this.selectedMaintenance) {
                this.selectedMaintenanceData = this.maintenances.find(
                    m => m.id === this.selectedMaintenance
                ) || null
                this.getManual();
            } else {
                this.manual = null;
                this.selectedMaintenanceData = null
            }
        },
        async getManual() {
            try {
                const response = await api.get(`/manual/?maintenance_id=${this.selectedMaintenance}&moto_id=${this.selectedMoto}`)
                if (Array.isArray(response.data) && response.data.length > 0) {
                    this.manual = response.data[0];
                } else if (!Array.isArray(response.data) && response.data.id) {
                    this.manual = response.data;
                } else {
                    this.manual = null;
                }
            } catch (err) {
                console.error('Failed get manual: ', err)
                this.manual = null;
            }
        },
        openMarkModal() {
            if (!this.selectedMaintenanceData) {
                alert('Выберите обслуживание')
                return
            }
            this.showMarkMaintenanceModal = true;
        },
        async markMaintenance(formData) {
            try {
                await api.post(`/maintenance/${formData.id}/complete`, {
                    completed_mileage: formData.mileage,
                    completed_date: formData.date,
                    cost: formData.cost,
                    is_repeat: formData.isRepeat,
                    interval: formData.interval
                })
                
                this.showMarkMaintenanceModal = false
                alert('Обслуживание успешно завершено!')

                await this.loadData()

                this.selectedMaintenance = null
                this.selectedMaintenanceData = null
                this.manual = null
            } catch (err) {
                console.log('Failed mark maintenance: ', err)
                alert(err.response?.data?.error || 'Ошибка при завершении обслуживания')
            }
        },
        removeRepairData() {
            this.selectedMaintenance = null
            this.selectedMoto = null
            this.manual = null
        },
        splitList(str) {
            if (!str) return [];
            return str.split(/[,;]\s*/).filter(s => s.trim() !== '');
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
        },
    },
    mounted() {
        this.loadData()
    }
}
</script>

<style scoped>
/* ===== HEADER ===== */
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    flex-wrap: wrap;
    gap: 16px;
}
.header-left h2 {
    margin: 0;
    font-size: 24px;
    font-weight: 600;
}
.header-subtitle {
    font-size: 14px;
    color: var(--text-secondary);
}
.header-right {
    display: flex;
    align-items: center;
    gap: 16px;
}
.notification-icon {
    font-size: 20px;
    color: #8b8b9e;
    cursor: pointer;
    transition: color 0.2s;
}
.notification-icon:hover { color: #fff; }

.profile-wrapper {
    display: flex;
    align-items: center;
    gap: 6px;
    position: relative;
}
.profile-img {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    border: 2px solid #7c3aed;
    object-fit: cover;
}
.dropdown-trigger {
    background: transparent;
    border: none;
    color: #8b8b9e;
    cursor: pointer;
    padding: 4px;
}
.dropdown-list {
    position: absolute;
    top: 48px;
    right: 0;
    background: #181824;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 8px;
    min-width: 140px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    z-index: 100;
}
.dropdown-list ul {
    list-style: none;
    margin: 0;
    padding: 0;
}
.dropdown-item {
    width: 100%;
    padding: 8px 12px;
    background: transparent;
    border: none;
    color: #ccc;
    text-align: left;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    transition: 0.2s;
}
.dropdown-item:hover {
    background: rgba(255,255,255,0.05);
    color: #fff;
}

@media (max-width: 720px) {
    .header-right {
        display: none;
    }
}

/* ===== COMMON ===== */
.section-block {
    margin-bottom: 24px;
}
.section-title {
    font-size: 16px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 16px;
}

/* ===== STATS ===== */
.stat-cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
}
.stat-card {
    padding: 18px 16px;
    background-color: #181824;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    transition: border-color 0.2s;
}
.stat-card:hover { border-color: rgba(255,255,255,0.1); }

.stat-label {
    font-size: 13px;
    color: #8b8b9e;
    margin-bottom: 6px;
}
.stat-value {
    font-size: 20px;
    font-weight: 700;
    margin: 0;
}
.warning-text {
    color: var(--warning);
}
.danger-text {
    color: var(--danger);
}
.stat-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
}
.stat-badge.success {
    background: rgba(34, 197, 94, 0.15);
    color: #4ade80;
}

/* ===== SELECT CARDS ===== */
.select-cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
}
.select-card, .manual-find-card {
    padding: 16px;
    background-color: #181824;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.select-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
}
.select-header p {
    font-size: 14px;
    font-weight: 500;
    margin: 0;
}
.step-badge {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 28px;
    height: 28px;
    border-radius: 50%;
    background-color: rgba(124, 58, 237, 0.15);
    color: #a78bfa;
    font-weight: 700;
    font-size: 14px;
}

/* Select styling */
.styled-select {
    width: 100%;
    padding: 10px 12px;
    background-color: #0f0f1a;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    color: #e0e0e0;
    font-size: 14px;
    outline: none;
    cursor: pointer;
    transition: border 0.2s;
    appearance: none;
    background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%238b8b9e' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: right 12px center;
    background-size: 14px;
}
.styled-select:focus { border-color: #7c3aed; }
.styled-select option { background-color: #0f0f1a; }

/* Find card */
.find-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
}
.find-badge {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 28px;
    height: 28px;
    border-radius: 50%;
    background-color: rgba(34, 197, 94, 0.15);
    color: #4ade80;
}
.find-badge.empty {
    background-color: rgba(107, 114, 128, 0.15);
    color: #9ca3af;
}
.find-title {
    color: #4ade80;
    font-weight: 600;
    margin: 0 0 2px 0;
    font-size: 14px;
}
.find-title.empty-title {
    color: #9ca3af;
}
.find-subtitle {
    font-size: 13px;
    color: #8b8b9e;
    margin: 0;
}


/* ===== MANUAL ===== */
.manual-wrapper {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 12px;
}
.manual {
    background-color: #181824;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.05);
}
.manual-title {
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 16px 0;
}

.steps-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 20px;
}
.step {
    display: flex;
    gap: 16px;
    padding: 12px;
    background-color: #0f0f1a;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.03);
}
.step-left {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
}
.step-number {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background-color: #7c3aed;
    color: #fff;
    font-weight: 700;
    font-size: 14px;
}
.step-img img {
    width: 120px;
    height: 80px;
    border-radius: 8px;
    object-fit: cover;
}
.step-body {
    display: flex;
    flex-direction: column;
    gap: 6px;
    width: 100%;
}
.step-title {
    font-weight: 600;
    margin: 0;
    font-size: 16px;
}
.step-text {
    font-size: 14px;
    color: #8b8b9e;
    margin: 0;
}
.step-tip {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 10px 12px;
    border-radius: 10px;
    margin-top: 4px;
}
.step-tip p {
    margin: 0;
    font-size: 13px;
}
.step-tip.info {
    background-color: rgba(124, 58, 237, 0.08);
    color: #a78bfa;
}
.step-tip.warning {
    background-color: rgba(251, 191, 36, 0.08);
    color: #fbbf24;
}
.step-tip i { font-size: 16px; margin-top: 1px;}

.manual-tips {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 14px;
    background-color: rgba(251, 191, 36, 0.06);
    border-radius: 10px;
}
.manual-tips i {
    color: #fbbf24;
    font-size: 18px;
    margin-top: 2px;
}
.tip-text {
    font-size: 14px;
    color: #d1d1d1;
    margin: 0;
    line-height: 1.4;
}
.tip-text strong { color: #fff; }

/* ===== MANUAL META (Right column) ===== */
.manual-meta {
    display: flex;
    flex-direction: column;
    gap: 12px;
}
.meta-card {
    padding: 16px;
    background-color: #181824;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
}
.meta-title {
    font-weight: 600;
    margin: 0 0 10px 0;
    font-size: 14px;
}
.meta-items {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 6px;
}
.meta-item {
    color: #8b8b9e;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.meta-item i {
    color: #5a5a72;
    font-size: 14px;
    width: 18px;
    text-align: center;
}
.empty-text {
    color: #5a5a72;
    font-size: 14px;
    margin: 0;
}

/* ===== MARK CARD ===== */
.mark-card {
    padding: 20px 16px;
    background: rgba(124, 58, 237, 0.06);
    border: 1px solid rgba(124, 58, 237, 0.15);
    border-radius: 14px;
}
.mark-title {
    color: #a78bfa;
    font-weight: 600;
    margin: 0 0 4px 0;
    font-size: 15px;
}
.mark-text {
    color: #8b8b9e;
    margin: 0 0 12px 0;
    font-size: 13px;
}
.mark-items {
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin-bottom: 16px;
}
.mark-item {
    color: #d1d1d1;
    font-size: 13px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.mark-item i {
    color: #4ade80;
}
.accept-btn {
    width: 100%;
    padding: 10px;
    background-color: #7c3aed;
    border: none;
    border-radius: 10px;
    color: #fff;
    font-weight: 600;
    font-size: 14px;
    cursor: pointer;
    transition: 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}
.accept-btn:hover {
    background-color: #6d28d9;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

/* ===== MEDIA QUERIES ===== */
@media (max-width: 1220px) {
    .stat-cards { grid-template-columns: repeat(2, 1fr); }
    .select-cards { grid-template-columns: repeat(2, 1fr); }
    .manual-find-card { grid-column: span 2; }
    .manual-wrapper { grid-template-columns: 1fr; }
}

@media (max-width: 820px) {
    .repair-container { padding: 16px; }
    .page-header { flex-direction: column; align-items: stretch; gap: 12px; }
    .header-right { justify-content: flex-end; }
}

@media (max-width: 560px) {
    .header-right { display: none;}
    .stat-cards { grid-template-columns: 1fr; }
    .select-cards { grid-template-columns: 1fr; }
    .manual-find-card { grid-column: span 1; }

    .step {
        flex-direction: column;
        align-items: stretch;
    }
    .step-left {
        flex-direction: row;
        gap: 12px;
    }
    .step-img img {
        width: 80px;
        height: 60px;
    }
    .step-number {
        width: 28px;
        height: 28px;
        font-size: 12px;
    }
    .manual-tips {
        flex-direction: column;
        align-items: flex-start;
    }
}
</style>
