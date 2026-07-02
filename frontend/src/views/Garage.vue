<script>
import MaintenanceCostChart from '../components/charts/MaintenanceCostChart.vue';
import MaintenanceCountChart from '../components/charts/MaintenanceCountChart.vue';
import MaintenanceNodeCard from '../components/maintenance/MaintenanceNodeCard.vue'
import MaintenanceCard from '../components/maintenance/MaintenanceCard.vue';
import MotoCard from '../components/moto/MotoCard.vue';

import api from '../api/api.js'

export default {
    components: { 
        MotoCard,
        MaintenanceCard,

        MaintenanceCostChart,
        MaintenanceCountChart,

        MaintenanceNodeCard
    },

    data() {
        return {
            maintenances_count: 0,
            plan_maintenances_count: 0,
            all_cost: 0,
            motorcycles: [],
            selectedMoto:null,

            motoData: null,
            nodes: [],
            plannedMaintenances: [],

            total_cost: 0,
            max_cost: 0,
            average_cost: 0,
            chart_data: [],

            loading: false
        }
    },

    methods: {
        async loadData() {
            try {
                const response = await api.get('/statistic/garage')

                this.maintenances_count = response.data.maintenances_count
                this.plan_maintenances_count = response.data.plan_maintenances_count
                this.motorcycles = response.data.motorcycles
                this.all_cost = response.data.cost
            } catch (err) {
                console.error(err)
            }
        },

        async getMotoData() {
            try {
                this.loading = true

                const response = await api.get(`/statistic/garage/${this.selectedMoto}`)

                this.motoData = response.data.motorcycle
                console.log(this.motoData)
                this.nodes = response.data.nodes
                this.plannedMaintenances = response.data.planned_maintenances

                this.total_cost = response.data.total_cost
                this.max_cost = response.data.max_cost
                this.average_cost = response.data.average_cost
                this.chart_data = response.data.chart_data
            } catch (err) {
                console.error(err)
            } finally {
                this.loading = false
            }
        }
    },

    mounted() {
        this.loadData()
    }
}
</script>

<template>
    <div class="container">
        <!-- === STATISTICS SECTION === -->
        <div class="section">
            <div class="section-title-wrapper">
                <i class="fa fa-wrench"></i> <h2>Управляйте обслуживанием своего мотоцикла</h2>
            </div>
            <div class="statistics-cards">
                <div class="stat-card">
                    <p class="stat-card-title">Кол-во выполненных обслуживаний</p>
                    <p class="stat-card-value">{{ maintenances_count }}</p>
                </div>
                <div class="stat-card">
                    <p class="stat-card-title">Кол-во плановых обслуживаний</p>
                    <p class="stat-card-value">{{ plan_maintenances_count }}</p>
                </div>
                <div class="stat-card">
                    <p class="stat-card-title">Сумма затрат на обслуживание</p>
                    <p class="stat-card-value">{{ all_cost }} ₽</p>
                </div>
            </div>
        </div>

        <!-- === SELECT MOTO === -->
        <div class="section">
            <div class="section-title-wrapper">
                <i class="fa fa-motorcycle"></i> <h2>Выберите мотоцикл для анализа</h2>
            </div>
            
            <div class="actions-wrapper">
                <select v-model="selectedMoto" class="select-action">
                    <option value="">Выберите мотоцикл</option>
                    <option v-for="m in motorcycles" :key="m.id" :value="m.id">{{ m.name }}</option>
                </select>
                <button @click="getMotoData()" :disabled="selectedMoto === null || selectedMoto === ''" class="select-action">Анализ</button>
            </div>
        </div>
        
        <!-- === MAINTENANCE SECTION === -->
        <div v-if="motoData" class="moto-section">
            <div class="section-wrapper">
                <div class="section-title-wrapper">
                    <i class="fa fa-bolt"></i> <h2>Быстрые действия</h2>
                </div>


                <div class="fast-actions-wrapper">
                    <button><i class="fa fa-tachometer"></i> Обновить пробег</button>
                    <button><i class="fa fa-wrench"></i> Добавить обслуживание</button>
                    <button><i class="fa fa-calendar"></i> Планировать обслуживание</button>
                </div>
            </div>


            <div class="section-wrapper">
                <div class="section-title-wrapper">
                    <i class="fa fa-motorcycle"></i> <h2>Ваш мотоцикл</h2>
                </div>
                <MotoCard
                    :moto="motoData"
                />
            </div>

            <div class="section-wrapper">
                <div class="section-title-wrapper">
                    <i class="fa fa-wrench"></i> <h2>Предстоящее обслуживание</h2>
                </div>
                <div class="pending-maintenances">
                    <MaintenanceCard
                        v-for="maintenance in plannedMaintenances"
                        :maintenance="maintenance"
                    />
                </div>
            </div>

            <div class="section-wrapper">
                <div class="section-title-wrapper">
                    <i class="fa fa-line-chart"></i> <h2>Статистика обслуживаний</h2>
                </div>

                <div class="chart-wrapper">
                    <div class="stat-card">
                        <h3>Стоимость обслуживаний</h3>

                        <div class="stat-card-items">
                            <div class="stat-card-item">
                                <p class="stat-card-title">
                                    Затраты на обслуживание:
                                </p>
                                <p class="stat-card-value">
                                    {{ total_cost }}
                                </p>
                            </div>
    
                            <div class="stat-card-item">
                                <p class="stat-card-title">
                                    Самое дорогое:
                                </p>
                                <p class="stat-card-value">
                                    {{ max_cost }}
                                </p>
                            </div>
    
                            <div class="stat-card-item">
                                <p class="stat-card-title">
                                    Средняя стоимость:
                                </p>
                                <p class="stat-card-value">
                                    {{ average_cost }}
                                </p>
                            </div>
                        </div>
                    </div>

                    <MaintenanceCostChart
                        :chartData="chart_data"
                    />
                </div>

                <hr class="chart-sep">

                <div class="chart-wrapper">
                    <div class="stat-card">
                        <h3>Частота обслуживаний</h3>

                        <div class="stat-card-items">
                            <div class="stat-card-item">
                                <p class="stat-card-title">
                                    Всего проведено обслуживаний:
                                </p>
                                <div class="stat-card-value">
                                    42
                                </div>
                            </div>
    
                            <div class="stat-card-item">
                                <p class="stat-card-title">
                                    Проведено в этом месяце:
                                </p>
                                <div class="stat-card-value">
                                    2
                                </div>
                            </div>
                        </div>
                    </div>

                    <MaintenanceCountChart />
                </div>
            </div>

            <div class="section-wrapper">
                <div class="section-title-wrapper">
                    <i class="fa fa-gear"></i> <h2>Узлы обслуживания</h2>
                </div>

                <div class="node-cards">
                    <MaintenanceNodeCard
                        v-for="node in nodes"
                        :node="node"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
p {
    margin-bottom: 0;
}


/* === Sections === */
.section-wrapper {
    display: flex;
    flex-direction: column;
    gap: 12px;

    padding: 18px;

    background-color: var(--bg-primary);
    border: 2px solid var(--border-color);
    border-radius: 25px;
}

.chart-sep {
    margin: 12px;
    color: var(--accent);
}

/* === Statistics === */
.statistics-cards {
    display: flex;
    flex-direction: row;
    gap: 24px;
    justify-content: center;
}

.stat-card {
    display: flex;
    flex-direction: column;
    gap: 12px;
    justify-content: space-evenly;

    padding: 16px;
    max-width: 370px;

    background-color: var(--bg-secondary);
    border: 2px solid var(--border-color);
    border-radius: 24px;

    text-align: center;

    transition: all 0.3s;
}

.stat-card:hover {
    border-bottom: 2px solid var(--accent);
    transform: translateY(-2px);
}

.stat-card-title {
    font-weight: 500;
    font-size: 18px;
}

.stat-card-value  {
    font-weight: 600;
    color: var(--accent);
    font-size: 24px;
}

.stat-card-items {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.stat-card-item {
    padding: 8px;
    background-color: var(--bg-primary);
    border-radius: 18px;
}

@media (max-width: 720px) {
    .statistics-cards {
        flex-direction: column;
        gap: 8px;
    }
}


/* === Select moto === */
.actions-wrapper {
    min-width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    max-width: 320px;
}

.select-action {
    width: 250px;
}


/* === Fast actions === */
.fast-actions-wrapper {
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
    gap: 8px;
}

.fast-actions-wrapper button {
    width: 100%;
    min-width: 220px;
}

@media (max-width: 1240px) {
    .fast-actions-wrapper {
        flex-direction: column;
    }
}


/* === Stat. section === */
.chart-wrapper {
    display: flex;
    flex-direction: row;
    gap: 8px;
    justify-content: center;
}

@media (max-width: 1220px) {
    .chart-wrapper {
        flex-direction: column;
    }

    .stat-card {
        min-width: 100%;
    }
    
    .statistics-cards {
        flex-direction: column;
    }
}


/* === Node maintenance === */
.node-cards {
    display: flex;
    flex-direction: column;
    gap: 21px;
}
</style>