<template>
    <div class="container">
        <!-- === WELCOME SECTION === -->
        <Header
            v-if="user"
            :title="`Добро пожаловать, ${user.username} 👋`"
            subtitle="Ваша статистика"
        />

        <!-- === STATISTICS SECTION === -->
        <section>
            <div class="statistic-cards-grid">
                <div class="stat-card">
                    <div class="card-icon">
                        <i class="fa fa-motorcycle"></i>
                    </div>
                    <div class="card-body">
                        <p class="card-title">Мотоциклов в гараже</p>
                        <p class="stat-value">{{ motorcycleCount }}</p>
                        <div class="stat-meta-wrapper">
                            <p class="stat-meta-value positive">+{{ dynamicMotorcycleCount }}</p> 
                            <p class="stat-meta"> за последний месяц</p>
                        </div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="card-icon">
                        <i class="fa fa-calendar"></i>
                    </div>
                    <div class="card-body">
                        <p class="card-title">Плановых ТО</p>
                        <p class="stat-value">{{ planMaintenanceCount }}</p>
                        <div class="stat-meta-wrapper">
                            <p class="stat-meta maintenance">{{ pendingMaintenanceCount }} скоро нужно выполнить</p>
                        </div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="card-icon">
                        <i class="fa fa-wrench"></i>
                    </div>
                    <div class="card-body">
                        <p class="card-title">Обслуживаний</p>
                        <p class="stat-value">{{ maintenanceCount }}</p>
                        <div class="stat-meta-wrapper">
                            <p class="stat-meta-value positive">+{{ dynamicMaintenanceCount }}</p> 
                            <p class="stat-meta"> за последний месяц</p>
                        </div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="card-icon">
                        <i class="fa fa-ruble"></i>
                    </div>
                    <div class="card-body">
                        <p class="card-title">Общие расходы</p>
                        <p class="stat-value">{{ totalSpends }} ₽</p>
                        <div class="stat-meta-wrapper">
                            <p 
                                class="stat-meta-value" 
                                :class="dynamicTotalSpendsCount >= 0 ? 'negative' : 'positive'"
                            >
                                {{ dynamicTotalSpendsCount >= 0 ? '+' : '' }}{{ dynamicTotalSpendsCount }}%
                            </p> 
                            <p class="stat-meta"> за последний месяц</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- === CHARTS SECTION === -->
        <div class="charts-grid-wrapper">
            <MaintenanceCostChart :chartData="costChartData" />
            <MaintenanceCountChart :chartData="countChartData" />
        </div>

        <!-- === PENDING MAINTENANCE SECTION === -->
        <section class="pending-maintenance-section">
            <h3>Ближайшие обслуживания</h3>
            <div v-if="pendingMaintenances.length > 0" class="cards-wrapper">
                <MaintenanceCard
                    v-for="maintenance in pendingMaintenances"
                    :key="maintenance.id"
                    :maintenance="{
                        ...maintenance,
                        moto_name: getMotorcycleName(maintenance.moto_id),
                        moto_mileage: getMotorcycleMileage(maintenance.moto_id)
                    }"
                />
            </div>
            <div v-else class="empty-state" style="margin-bottom: 14px;">
                <div class="empty-header">
                    <i class="fa fa-wrench"></i>
                    <p class="empty-title">У вас нет запланированных ТО</p>
                </div>

                <div class="empty-body">
                    <p class="empty-text">Запланируйте первое ТО на странице <a href="/maintenance">"Обслуживание"</a></p>
                </div>
            </div>
            <button @click="this.$router.push('/maintenance')" class="outline-btn">Все обслуживания <i class="fa fa-angle-right"></i></button>
        </section>
    </div>
</template>

<script>
import api from '../api/api';
import { getUser } from '../api/auth';
import { removeTokens } from '../api/auth';

import Header from '../components/Header.vue';
import MaintenanceCard from '../components/maintenance/MaintenanceCard.vue';
import MaintenanceCostChart from '../components/charts/MaintenanceCostChart.vue'
import MaintenanceCountChart from '../components/charts/MaintenanceCountChart.vue'

export default {
    components: {
        Header,
        MaintenanceCard,
        MaintenanceCostChart,
        MaintenanceCountChart,
    },

    data() {
        return {
            user: null,
            loading: false,

            // === Arrays ===
            motorcycles: [],
            maintenances: [],

            // === Statistic vars ===
            motorcycleCount: 0,
            planMaintenanceCount: 0,
            pendingMaintenanceCount: 0,
            maintenanceCount: 0,
            totalSpends: 0,
            // dynamic stat vars
            dynamicMotorcycleCount: 0,
            dynamicMaintenanceCount: 0,
            dynamicTotalSpendsCount: 0,

            // === Chart data ===
            costChartData: [],
            countChartData: [],
        }
    },

    computed: {
        pendingMaintenances() {
            // check pending maintenances
            if (!this.maintenances) return []
            return this.maintenances
                .filter(m => m.status === 'overdue' || m.status === 'soon')
                .slice(0, 2)
        }
    },

    methods: {
        async loadData() {
            // load page data. First - dashboard stat and obj. Second - charts data
            try {
                this.loading = true
                
                const dashboardResponse = await api.get('/statistic/dashboard-data')
                
                this.user = getUser()
                this.motorcycles = dashboardResponse.data.motorcycles || []
                this.maintenances = dashboardResponse.data.maintenance || []
                this.motorcycleCount = dashboardResponse.data.motorcycles_count || 0
                this.planMaintenanceCount = dashboardResponse.data.plan_maintenances_count || 0
                this.maintenanceCount = dashboardResponse.data.maintenances_count || 0
                this.totalSpends = dashboardResponse.data.total_spends || 0
                
                this.dynamicMotorcycleCount = dashboardResponse.data.new_motorcycles_count || 0
                this.dynamicMaintenanceCount = dashboardResponse.data.month_maintenances_count || 0
                this.dynamicTotalSpendsCount = dashboardResponse.data.spends_change_percent || 0
                
                this.pendingMaintenanceCount = this.maintenances
                    .filter(m => m.status === 'overdue' || m.status === 'soon')
                    .length

                const chartsResponse = await api.get('/statistic/dashboard-charts')
                this.costChartData = chartsResponse.data.cost_chart || []
                this.countChartData = chartsResponse.data.count_chart || []

            } catch(err) {
                alert("Не удалось загрузить данные")
                console.error('Failed to load dashboard data:', err)
            } finally {
                this.loading = false
            }
        },

        getMotorcycleName(motoId) {
            // Get motorcycle name
            const moto = this.motorcycles.find(m => m.id === motoId)
            return moto ? moto.name : `Мотоцикл #${motoId}`
        },

        getMotorcycleMileage(motoId) {
            // Get motorcycle mileage
            const moto = this.motorcycles.find(m => m.id === motoId)
            return moto ? moto.mileage : '0'
        },

        async logout() {
            // Logout
            try {
                await api.post('/auth/logout');
            } catch(err) {
                console.error('Logout failed:', err);
            } finally {
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
/*  === WELCOME SECTION ===  */
.welcome-section {
    background-color: var(--bg-primary);
    border: 2px solid var(--border-color);
    border-radius: 25px;
    padding: 28px;
    margin-bottom: 32px;

}

.welcome-wrapper {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    position: relative;
}

.welcome-actions {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 24px;
}

.profile-img {
    border-radius: 50%;
    overflow: hidden;
    border: 2px solid var(--accent);
    max-width: 40px;
    max-height: 40px;
}

.profile-link {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 8px;
    color: var(--text-muted);
    cursor: pointer;
}

.dropdown-wrapper {
    position: relative;
}

.dropdown-list {
    position: absolute;
    top: calc(100% + 8px);
    right: 0;
    min-width: 150px;
    padding: 8px;
    background-color: var(--bg-primary);
    border: 2px solid var(--border-color);
    border-radius: 16px;
    box-shadow: var(--shadow-lg);
    z-index: 100;
    animation: slideInUp 0.2s ease;
}

.dropdown-list ul {
    margin: 0;
    padding: 0;
}

.dropdown-list li {
    list-style-type: none;
}

.dropdown-item-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    width: 100%;
    padding: 8px 12px;
    background-color: transparent;
    border: none;
    border-radius: 10px;
    color: var(--text-primary);
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.dropdown-item-btn:hover {
    background-color: var(--bg-secondary);
}

@media (max-width: 720px) {
    .welcome-actions {
        display: none;
    }
}


/* === STATISTICS SECTION === */
.statistic-cards-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(1, 1fr);
    gap: 8px;
}

.stat-card {
    padding: 16px;
    background-color: var(--bg-secondary);
    border-radius: 20px;

    display: flex;
    flex-direction: row;
}

.card-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--accent-trans);
    color: var(--accent);
    height: 48px;
    width: 48px;
    text-align: center;
    border-radius: 12px;

    margin-right: 12px;
}

.card-title {
    font-size: 14px;
    color: var(--text-muted);
    margin-bottom: 8px;
}

.stat-value {
    font-size: 28px;
    font-weight: 600;
    margin-bottom: 8px;
}

.stat-meta-wrapper {
    display: flex;
    flex-direction: row;
    gap: 8px;
    font-size: 14px;
    margin-bottom: 8px;
}

.stat-meta {
    color: var(--text-muted);
    margin-bottom: 8px;
}

.stat-meta-value.positive {
    color: var(--success);
    margin-bottom: 8px;
}

.stat-meta-value.negative {
    color: var(--danger);
    margin-bottom: 8px;
}

.stat-meta.maintenance {
    color: var(--warning);
}

@media (max-width: 728px) {
    .statistic-cards-grid {
        grid-template-columns: repeat(1, 1fr) !important;
        grid-template-rows: repeat(4, 1fr) !important;
    }

    .stat-card {
        align-items: center;
        justify-content: space-evenly;
    }
}

@media (max-width: 1220px) {
    .statistic-cards-grid {
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(2, 1fr);
    }

    .stat-card {
        align-items: center;
        justify-content: space-evenly;
    }
}


/* === CHART SECTION === */
.charts-grid-wrapper {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    margin: 24px 0;
}

@media (max-width: 768px) {
    .charts-grid-wrapper {
        grid-template-columns: 1fr;
        gap: 12px;
    }
}

@media (max-width: 1220px) {
    .charts-grid-wrapper {
        grid-template-columns: 1fr;
        gap: 12px;
    }
}

@media (max-width: 1220px) {
    .stat-card {
        align-items: center;
        justify-content: space-evenly;
    }
}


/*  === PENDING MAINTENANCE SECTION ===  */
.pending-maintenance-section {
    background-color: var(--bg-secondary);
    padding: 12px;
    border-radius: 20px;

    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.pending-maintenance-section h3 {
    margin-bottom: 16px;
    font-size: 18px;
}

.pending-maintenance-section button {
    width: 100%;
}

.cards-wrapper {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 16px;
}


/* === EMPTY STATE === */
.empty-text {
    color: #5a5a72;
    font-size: 14px;
    margin: 0;
}


/* === ANIMATIONS === */

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
</style>