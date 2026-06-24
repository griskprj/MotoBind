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
                    <p class="stat-card-value">12</p>
                </div>
                <div class="stat-card">
                    <p class="stat-card-title">Кол-во плановых обслуживаний</p>
                    <p class="stat-card-value">12</p>
                </div>
                <div class="stat-card">
                    <p class="stat-card-title">Сумма затрат на обслуживание</p>
                    <p class="stat-card-value">12 $</p>
                </div>
            </div>
        </div>
        <!-- === --- === -->
        
        <div class="section-sep"><hr></div>

        <!-- === FILTERS SECTION === -->
        <div class="filters">
            <div class="filter">
                <select>
                    <option value="">Выберите мотоцикл</option>
                </select>
            </div>
        </div>
        <!-- === --- === -->

        <!-- === MAINTENANCE SECTION === -->
        <div class="section">
            <div class="section-wrapper">
                <div class="section-title-wrapper">
                    <i class="fa fa-rocket"></i> <h2>Быстрые действия</h2>
                </div>

                <div class="fast-actions-wrapper">
                    <button><i class="fa fa-pen"></i> Добавить заметку</button>
                    <button><i class="fa fa-tachometer"></i> Обновить пробег</button>
                    <button><i class="fa fa-wrench"></i> Добавить обслуживание</button>
                    <button><i class="fa fa-calendar"></i> Планировать обслуживание</button>
                </div>
            </div>

            <div class="section-sep"><hr></div>

            <div class="section-wrapper">
                <div class="section-title-wrapper">
                    <i class="fa fa-motorcycle"></i> <h2>Ваш мотоцикл</h2>
                </div>
                <MotoCard
                    :moto="{
                        'id': 1,
                        'name': 'moto'
                    }"
                />
            </div>

            <div class="section-sep"><hr></div>

            <div class="section-wrapper">
                <div class="section-title-wrapper">
                    <i class="fa fa-wrench"></i> <h2>Предстоящее обслуживание</h2>
                </div>
                <div class="pending-maintenances">
                    <MaintenanceCard
                        :maintenance="{
                            'id': 1,
                            'title': 'title'
                        }"
                    />
                </div>
            </div>

            <div class="section-wrapper">
                <div class="section-title-wrapper">
                    <i class="fa fa-line-chart"></i> <h2>Статистика</h2>
                </div>

                <div class="charts-wrapper">
                    <div class="chart-wrapper">
                        <div class="chart-wrapper-title">
                            <i class="fa fa-rub"></i> <p>Затраты</p>
                        </div>
    
                        <MaintenanceCostChart/>
                    </div>
    
                    <div class="chart-wrapper">
                        <div class="chart-wrapper-title">
                            <i class="fa fa-wrench"></i> <p>Обслуживание</p>
                        </div>
    
                        <MaintenanceCountChart />
                    </div>
                </div>
            </div>

            <!-- === MAINTENANCE NODES === -->
            <div class="section-wrapper">
                <div class="section-title-wrapper">
                    <i class="fa fa-gear"></i> 
                    <h2>Узлы обслуживания</h2>
                    <button class="toggle-all-btn" @click="toggleAllNodes">
                        <i class="fa" :class="allNodesExpanded ? 'fa-compress' : 'fa-expand'"></i>
                        {{ allNodesExpanded ? 'Свернуть все' : 'Развернуть все' }}
                    </button>
                </div>

                <div class="maintenance-nodes">
                    <!-- Двигатель -->
                    <MaintenanceNodeCard
                        ref="nodeCards"
                        :collapsed="getNodeState('engine')"
                        title="Двигатель"
                        maintenanceCount="12"
                        cost="25000"
                        :maintenances="[
                            {
                                'id': 1,
                                'title': 'Замена масла',
                                'planned_mileage': '21000'
                            },
                            {
                                'id': 2,
                                'title': 'Замена фильтра',
                                'planned_mileage': '22000'
                            }
                        ]"
                        recomendation="Следите за уровнем масла!"
                        @toggle-collapse="onToggleCollapse('engine', $event)"
                        @edit-node="editNode('engine')"
                        @add-maintenance="addNodeMaintenance('engine')"
                        @delete-node="deleteNode('engine')"
                        @view-maintenance="viewMaintenance"
                    />
                    
                    <!-- Привод -->
                    <MaintenanceNodeCard
                        ref="nodeCards"
                        :collapsed="getNodeState('drive')"
                        title="Привод"
                        maintenanceCount="8"
                        cost="15000"
                        :maintenances="[
                            {
                                'id': 3,
                                'title': 'Натянуть цепь',
                                'planned_mileage': '21000'
                            },
                            {
                                'id': 4,
                                'title': 'Смазка цепи',
                                'planned_mileage': '21500'
                            }
                        ]"
                        recomendation="Регулярно смазывайте цепь!"
                        @toggle-collapse="onToggleCollapse('drive', $event)"
                        @edit-node="editNode('drive')"
                        @add-maintenance="addNodeMaintenance('drive')"
                        @delete-node="deleteNode('drive')"
                        @view-maintenance="viewMaintenance"
                    />
                    
                    <!-- Рулевое управление -->
                    <MaintenanceNodeCard
                        ref="nodeCards"
                        :collapsed="getNodeState('steering')"
                        title="Рулевое управление"
                        maintenanceCount="5"
                        cost="8000"
                        :maintenances="[
                            {
                                'id': 5,
                                'title': 'Проверка вилки',
                                'planned_mileage': '21000'
                            }
                        ]"
                        recomendation="Проверьте вилку на предмет утечки масла"
                        @toggle-collapse="onToggleCollapse('steering', $event)"
                        @edit-node="editNode('steering')"
                        @add-maintenance="addNodeMaintenance('steering')"
                        @delete-node="deleteNode('steering')"
                        @view-maintenance="viewMaintenance"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import MaintenanceCostChart from '../components/charts/MaintenanceCostChart.vue';
import MaintenanceCountChart from '../components/charts/MaintenanceCountChart.vue';
import NodeCountChart from '../components/charts/NodeCountChart.vue';
import MaintenanceCard from '../components/maintenance/MaintenanceCard.vue';
import MaintenanceNodeCard from '../components/maintenance/MaintenanceNodeCard.vue';
import MotoCard from '../components/moto/MotoCard.vue';

export default {
    components: { 
        MotoCard,
        MaintenanceCard,
        MaintenanceCostChart,
        MaintenanceCountChart,
        NodeCountChart,
        MaintenanceNodeCard
    },
    data() {
        return {
            // Состояние сворачивания для каждого узла
            nodeStates: {
                engine: false,    // false - развернуто, true - свернуто
                drive: false,
                steering: false
            }
        }
    },
    computed: {
        allNodesExpanded() {
            // ⭐ ПРОВЕРЯЕМ, ЧТО nodeStates СУЩЕСТВУЕТ И НЕ ПУСТОЙ ⭐
            if (!this.nodeStates || typeof this.nodeStates !== 'object') {
                return true
            }
            
            // Проверяем, все ли узлы развернуты
            const values = Object.values(this.nodeStates)
            if (values.length === 0) return true
            
            return !values.some(state => state === true)
        }
    },
    methods: {
        // ⭐ БЕЗОПАСНОЕ ПОЛУЧЕНИЕ СОСТОЯНИЯ УЗЛА ⭐
        getNodeState(nodeKey) {
            if (!this.nodeStates) return false
            return this.nodeStates[nodeKey] || false
        },
        
        // Переключение состояния конкретного узла
        onToggleCollapse(nodeKey, isCollapsed) {
            if (this.nodeStates) {
                this.nodeStates[nodeKey] = isCollapsed
            }
        },
        
        // Переключение всех узлов
        toggleAllNodes() {
            if (!this.nodeStates) return
            
            const newState = !this.allNodesExpanded
            Object.keys(this.nodeStates).forEach(key => {
                this.nodeStates[key] = !newState
            })
        },
        
        // Обработчики действий
        editNode(nodeKey) {
            console.log('Редактирование узла:', nodeKey)
        },
        
        addNodeMaintenance(nodeKey) {
            console.log('Добавление обслуживания для узла:', nodeKey)
        },
        
        deleteNode(nodeKey) {
            console.log('Удаление узла:', nodeKey)
        },
        
        viewMaintenance(maintenance) {
            console.log('Просмотр обслуживания:', maintenance)
        }
    }
}
</script>

<style scoped>
p {
    margin-bottom: 0;
}

/* Кнопка переключения всех */
.toggle-all-btn {
    margin-left: auto;
    padding: 6px 16px;
    background-color: var(--bg-secondary, #f8f9fa);
    border: 2px solid var(--border-color, #e0e0e0);
    border-radius: 20px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    color: #666;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    gap: 8px;
}

.toggle-all-btn:hover {
    background-color: var(--accent, #FF6B35);
    color: white;
    border-color: var(--accent, #FF6B35);
    transform: translateY(-1px);
}

.toggle-all-btn i {
    font-size: 14px;
}

@media (max-width: 768px) {
    .section-title-wrapper {
        flex-wrap: wrap;
    }
    
    .toggle-all-btn {
        margin-left: 0;
        width: 100%;
        justify-content: center;
    }
}


/* === Statistics === */
.statistics-cards {
    display: flex;
    flex-direction: row;
    gap: 24px;
    justify-content: center;
}

.stat-card {
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
    margin-bottom: 12px;
    font-size: 18px;
}

.stat-card-value  {
    font-weight: 600;
    color: var(--accent);
    font-size: 24px;
}

@media (max-width: 720px) {
    .statistics-cards {
        flex-direction: column;
        gap: 8px;
    }
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
.charts-wrapper {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.chart-wrapper {
    padding: 12px;
    border: 2px solid var(--border-color);
    border-radius: 25px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    align-items: center;
}

.stat-chart-wrapper {
    display: flex;
    flex-direction: column;
    width: 100%;
    gap: 8px;
}

.chart-wrapper-title {
    display: flex;
    flex-direction: row;
    gap: 12px;
    align-items: center;

    font-size: 20px;
}

.chart-wrapper-title i {
    color: var(--accent-hover)
}

.stat-chart-card {
    padding: 16px;
    width: 100%;

    background-color: var(--bg-secondary);
    border: 2px solid var(--border-color);
    border-radius: 24px;

    text-align: center;

    transition: all 0.3s;
}

.stat-chart-card:hover {
    border-bottom: 2px solid var(--accent);
    transform: translateY(-2px);
}

/* === Maintenance nodes === */
.maintenance-nodes {
    margin-bottom: 12px;
}


</style>