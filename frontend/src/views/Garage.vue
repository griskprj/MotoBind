<script>
import MaintenanceCostChart from '../components/charts/MaintenanceCostChart.vue';
import MaintenanceCountChart from '../components/charts/MaintenanceCountChart.vue';
import MaintenanceNodeCard from '../components/maintenance/MaintenanceNodeCard.vue'
import MaintenanceCard from '../components/maintenance/MaintenanceCard.vue';
import MotoCard from '../components/moto/MotoCard.vue';

import UpdateMileageModal from '../components/modals/moto/UpdateMileageModal.vue';
import AddMaintenanceModal from '../components/modals/maintenance/AddMaintenanceModal.vue';
import AddPlanMaintenanceModal from '../components/modals/maintenance/AddPlanMaintenanceModal.vue';
import EditPlanMaintenanceModal from '../components/modals/maintenance/EditPlanMaintenanceModal.vue';
import DeletePlanMaintenanceModal from '../components/modals/maintenance/DeletePlanMaintenanceModal.vue';
import MarkPlanMaintenanceModal from '../components/modals/maintenance/MarkPlanMaintenanceModal.vue';

import EditMotoModal from '../components/modals/moto/EditMotoModal.vue';
import DeleteMotoModal from '../components/modals/moto/DeleteMotoModal.vue';

import api from '../api/api.js'

export default {
    components: {
        // === CARDS ===
        MotoCard,
        MaintenanceCard,
        MaintenanceNodeCard,

        // === CHARTS ===
        MaintenanceCostChart,
        MaintenanceCountChart,

        // === MODALS ===
        // maintenance modal
        AddMaintenanceModal,
        AddPlanMaintenanceModal,
        EditPlanMaintenanceModal,
        DeletePlanMaintenanceModal,
        MarkPlanMaintenanceModal,

        // motorcycle modals
        EditMotoModal,
        DeleteMotoModal,
        UpdateMileageModal,
    },

    data() {
        return {
            // === STATISTICS VARS ===  
            // maintenance
            maintenances_count: 0,
            plan_maintenances_count: 0,
            total_maintenances: 0,
            month_maintenances: 0,
            
            // money
            all_cost: 0,
            total_cost: 0,
            max_cost: 0,
            average_cost: 0,

            // === MOTORCYCLE ===
            motorcycles: [],
            selectedMoto:null,
            motoData: null,

            // === MAINTENANCES ===
            nodes: [],
            plannedMaintenances: [],
            selectedMaintenance: null,
            selectedDeleteMaintenanceId: null,
            markPlanMaintenanceId: null,

            // === CHARTS ===
            money_chart_data: [],
            freq_chart_data: [],

            loading: false,

            // === MODALS ===
            // motorcycles
            showUpdateMileageModal: false,
            showEditMotoModal: false,
            showDeleteMotoModal: false,

            // maintenances
            showAddMaintenanceModal: false,
            showPlanMaintenanceModal: false,
            showEditPlanMaintenanceModal: false,
            showMarkPlanMaintenanceModal: false,
            showDeletePlanMaintenanceModal: false,

            // === NODES TABS ===
            activeNodeIndex: 0,
            showNodeMaintenances: true,
        }
    },

    computed: {
        activeNode() {
            return this.nodes[this.activeNodeIndex] || null;
        },
        healthColor() {
            if (!this.activeNode) return 'var(--health-green, #4CAF50)';
            const health = this.activeNode.health;
            if (health >= 80) return 'var(--health-green, #4CAF50)';
            if (health >= 50) return 'var(--health-yellow, #FFC107)';
            return 'var(--health-red, #F44336)';
        },
        filteredNodes() {
            // Если есть активный узел, показываем только его
            return this.activeNode ? [this.activeNode] : [];
        }
    },

    methods: {
        // === ASYNC FUNC ===
        async loadData() {
            // load garage base data
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
            // load more garage data
            try {
                this.loading = true

                const response = await api.get(`/statistic/garage/${this.selectedMoto}`)

                this.motoData = response.data.motorcycle
                this.nodes = response.data.nodes
                this.plannedMaintenances = response.data.planned_maintenances

                this.total_cost = response.data.total_cost
                this.max_cost = response.data.max_cost
                this.average_cost = response.data.average_cost
                this.money_chart_data = response.data.money_chart_data

                this.total_maintenances = response.data.total_maintenances
                this.month_maintenances = response.data.month_maintenances
                this.freq_chart_data = response.data.freq_chart_data

                // Сбрасываем индекс при загрузке новых данных
                this.activeNodeIndex = 0
                this.showNodeMaintenances = true
            } catch (err) {
                console.error(err)
            } finally {
                this.loading = false
            }
        },

        // --- motorcycles ---
        async updateMotoMileage(formData) {
            // update moto mileage
            try {
                this.loading = true

                const response = await api.patch(`/motorcycle/${formData.id}`, {
                    newMileage: formData.newMileage
                })

                const updatedMoto = response.data

                if (this.motoData && this.motoData.id === formData.id) {
                    this.motoData.mileage = updatedMoto.mileage
                }

                const motoIndex = this.motorcycles.findIndex(m => m.id === formData.id)
                if (motoIndex !== -1) {
                    this.motorcycles[motoIndex].mileage = updatedMoto.mileage
                }

                this.showUpdateMileageModal = false
                alert(`Пробег мотоцикла ${this.motoData?.name || 'Мотоцикл'} обновлен до ${updatedMoto.mileage} км`)
            } catch(err) {
                console.error('Failed update moto mileage', err)
            } finally {
                this.loading = false
            }
        },

        async updateMoto(formData) {
            // update moto
            try {
                this.loading = true

                const { data } = await api.put(`/motorcycle/${formData.id}`, formData)
                const index = this.motorcycles.findIndex(m => m.id === formData.id)

                if (index !== -1) {
                    this.motorcycles[index] = data
                }
                this.motoData = data

                this.showEditMotoModal = false
                alert("Мотоцикл обновлен")
            } catch (err) {
                console.error(`Failed update moto: ${err}`)
            } finally {
                this.loading = false
            }
        },

        async deleteMoto() {
            // delete moto
            try {
                this.loading = true

                await api.delete(`/motorcycle/${this.selectedMoto}`)
                
                alert("Мотоцикл удален")
                this.$router.push('/home')
            } catch (err) {
                console.error(`Failed delete moto: ${err}`)
            } finally {
                this.loading = false
            }
        },

        // --- maintenances ---
        async addMaintenance(formData) {
            // add maintenance
            try {
                this.loading = true
                
                await api.post('/maintenance/create-new', formData)
                this.loadData()
                this.showAddMaintenanceModal = false
                alert("Обслуживание добавлено в историю")
            } catch (err) {

                console.error(`Failed add maintenance: ${err}`)
            } finally {
                this.loading = false
            }
        },

        async addPlanMaintenance(formData) {
            // plan maintenance
            try {
                this.loading = true

                const response = await api.post('/maintenance/plan', formData)
                this.loadData()
                this.showPlanMaintenanceModal = false
                alert("Обслуживание запланированно")
            } catch (err) {
                console.error(`Failed plan maintenance: ${err}`)
            } finally {
                this.loading = false
            }
        },

        async editPlanMaintenance(formData) {
            // edit plan maintenance
            try {
                this.loading = true

                const { data } = await api.put(`/maintenance/plan`, formData)

                const maintenanceIndex = this.plannedMaintenances.findIndex(m => m.id === formData.maintenanceId)
                if (maintenanceIndex !== -1) {
                    this.plannedMaintenances[maintenanceIndex] = data
                }   
                this.closeEditPlanMaintenanceModal() 
                this.loadData()   
                alert(`Плановое обслуживание "${formData.title}" обновлено`)
            } catch (err) {
                console.error(`Failed update plan maintenance: ${err}`)
            } finally {
                this.loading = false
            }
        },

        async deletePlanMaintenance(maintenenceId) {
            // delete plan maintenance
            try {
                this.loading = true

                const response = await api.delete(`/maintenance/plan/${maintenenceId}`)
                
                const maintnenanceIndex = this.plannedMaintenances.findIndex(m => m.id === maintenenceId)
                if (maintnenanceIndex !== -1) {
                    this.plannedMaintenances.splice(maintnenanceIndex, 1)
                }
                
                this.showDeletePlanMaintenanceModal = false
                this.selectedDeleteMaintenanceId = null
                this.loadData()
                alert("Обслуживание успешно удалено!")
            } catch (err) {
                console.error(`Failed delete plan maintenance: ${err}`)
            } finally {
                this.loading = false
            }
        },

        async markPlanMaintenance(formData) {
            // mark plan maintenance
            try {
                this.loading = true

                const response = await api.post(`/maintenance/plan/mark`, formData)

                this.loadData()
                this.showMarkPlanMaintenanceModal = false
                alert("Обслуживание отмечено выполненным")
            } catch (err) {
                console.error(`Failed mark plan maintenance: ${err}`)
            } finally {
                this.loading = false
            }
        },

        // --- other ---
        removeMotoData() {
            // remove moto data
            this.motoData = null
            this.nodes = []
            this.activeNodeIndex = 0
        },

        // === NODE TABS METHODS ===
        selectNode(index) {
            this.activeNodeIndex = index
            this.showNodeMaintenances = true
        },

        prevNode() {
            if (this.activeNodeIndex > 0) {
                this.activeNodeIndex--
                this.showNodeMaintenances = true
            }
        },

        nextNode() {
            if (this.activeNodeIndex < this.nodes.length - 1) {
                this.activeNodeIndex++
                this.showNodeMaintenances = true
            }
        },

        toggleNodeMaintenances() {
            this.showNodeMaintenances = !this.showNodeMaintenances
        },

        // === MODALS FUNC ===

        // --- motorcycles ---
        // update mileage
        openUpdateMileageModal() {
            this.showUpdateMileageModal = true
        },

        // edit motorcycle
        openEditMotoModal() {
            this.showEditMotoModal = true
        },

        // delete motorcycle
        openDeleteMotoModal() {
            this.showDeleteMotoModal = true
        },

        // --- maintenances ---
        // add maintenance
        openAddMaintenanceModal() {
            this.showAddMaintenanceModal = true
        },

        // add plan maintenance
        openPlanMaintenanceModal() {
            this.showPlanMaintenanceModal = true
        },

        // update plan maintenance
        openEditPlanMaintenanceModal(maintenance) {
            this.selectedMaintenance = maintenance
            this.showEditPlanMaintenanceModal = true
        },
        closeEditPlanMaintenanceModal() {
            this.showEditPlanMaintenanceModal = false
            this.selectedMaintenance = null
        },
        
        // delete plan maintenance
        openDeletePlanMaintenanceModal(maintenanceId) {
            this.selectedDeleteMaintenanceId = maintenanceId
            this.showDeletePlanMaintenanceModal = true
        },
        closeDeletePlanMaintenanceModal() {
            this.showDeletePlanMaintenanceModal = false
            this.selectedDeleteMaintenanceId = null
        },

        // mark plan maintenance
        openMarkPlanMaintenance(maintenanceId) {
            this.markPlanMaintenanceId = maintenanceId
            this.showMarkPlanMaintenanceModal = true
        },
        closeMarkPlanMaintenance() {
            this.markPlanMaintenanceId = null
            this.showMarkPlanMaintenanceModal = false
        },
    },

    mounted() {
        this.loadData()
    }
}
</script>

<template>
    <div class="container">
        <!-- Статистика -->
        <div class="section statistics-section">
            <div class="section-title-wrapper">
                <i class="fa fa-gear"></i>
                <h2>Управляйте обслуживанием своего мотоцикла</h2>
            </div>
            <div class="statistics-cards">
                <div class="stat-card">
                    <p class="stat-card-title">Выполнено обслуживаний</p>
                    <p class="stat-card-value">{{ maintenances_count }}</p>
                </div>
                <div class="stat-card">
                    <p class="stat-card-title">Запланировано</p>
                    <p class="stat-card-value">{{ plan_maintenances_count }}</p>
                </div>
                <div class="stat-card">
                    <p class="stat-card-title">Общие затраты</p>
                    <p class="stat-card-value">{{ all_cost }} ₽</p>
                </div>
            </div>
        </div>

        <!-- Выбор мотоцикла -->
        <div class="section select-moto-section">
            <div class="section-title-wrapper">
                <i class="fa fa-motorcycle"></i>
                <h2>Выберите мотоцикл для анализа</h2>
            </div>
            <div class="actions-wrapper">
                <select v-model="selectedMoto" class="select-action">
                <option value="">Выберите мотоцикл</option>
                <option v-for="m in motorcycles" :key="m.id" :value="m.id">{{ m.name }}</option>
                </select>
                <button
                    @click="getMotoData()"
                    :disabled="selectedMoto === null || selectedMoto === ''"
                    class="select-action"
                    :style="{ display: motoData ? 'none' : '' }"
                >
                    Анализ
                </button>
                <button
                    @click="removeMotoData()"
                    :disabled="motoData === null || motoData === ''"
                    class="select-action"
                    :style="{ display: !motoData ? 'none' : '' }"
                    >
                    Закрыть
                </button>
            </div>
        </div>

        <!-- Детальная информация по мотоциклу -->
        <div v-if="motoData" class="moto-section">
            <!-- Быстрые действия -->
            <div class="section-wrapper actions-wrapper-block">
                <div class="section-title-wrapper small">
                <i class="fa fa-bolt"></i>
                    <h3>Быстрые действия</h3>
                </div>
                <div class="fast-actions-wrapper">
                    <button @click="openUpdateMileageModal()"><i class="fa fa-tachometer"></i> Обновить пробег</button>
                    <button @click="openAddMaintenanceModal()"><i class="fa fa-wrench"></i> Добавить обслуживание</button>
                    <button @click="openPlanMaintenanceModal()"><i class="fa fa-calendar"></i> Планировать обслуживание</button>
                </div>
            </div>

            <!-- Карточка мотоцикла -->
            <div class="section-wrapper moto-card-wrapper">
                <div class="section-title-wrapper small">
                    <i class="fa fa-motorcycle"></i>
                    <h3>Ваш мотоцикл</h3>
                </div>
                <MotoCard
                    :moto="motoData"
                    @editMoto="openEditMotoModal"
                    @deleteMoto="openDeleteMotoModal"
                />
            </div>

            <!-- Предстоящее обслуживание -->
            <div class="section-wrapper planned-wrapper">
                <div class="section-title-wrapper small">
                <i class="fa fa-wrench"></i>
                <h3>Предстоящее обслуживание</h3>
                </div>
                <div v-if="plannedMaintenances.length === 0" class="empty-state small">
                <i class="fa fa-calendar-check-o"></i>
                <p>Нет запланированных обслуживаний</p>
                </div>
                <div v-else class="pending-maintenances">
                <MaintenanceCard
                    v-for="maintenance in plannedMaintenances"
                    :key="maintenance.id"
                    :maintenance="maintenance"
                    style="margin-bottom: 8px;"
                    @edit="openEditPlanMaintenanceModal"
                    @delete="openDeletePlanMaintenanceModal"
                    @mark="openMarkPlanMaintenance"
                />
                </div>
            </div>

            <!-- Статистика обслуживаний -->
            <div class="section-wrapper stats-wrapper">
                <div class="section-title-wrapper small">
                <i class="fa fa-line-chart"></i>
                <h3>Статистика обслуживаний</h3>
                </div>

                <!-- Стоимость -->
                <div class="chart-block">
                <div class="stat-card horizontal">
                    <h4>Стоимость обслуживаний</h4>
                    <div class="stat-card-items">
                    <div class="stat-card-item">
                        <p class="stat-card-title">Затраты</p>
                        <p class="stat-card-value">{{ total_cost }} ₽</p>
                    </div>
                    <div class="stat-card-item">
                        <p class="stat-card-title">Самое дорогое</p>
                        <p class="stat-card-value">{{ max_cost }} ₽</p>
                    </div>
                    <div class="stat-card-item">
                        <p class="stat-card-title">Средняя стоимость</p>
                        <p class="stat-card-value">{{ average_cost }} ₽</p>
                    </div>
                    </div>
                </div>
                <MaintenanceCostChart :chartData="money_chart_data" />
                </div>

                <hr class="chart-sep" />

                <!-- Частота -->
                <div class="chart-block">
                <div class="stat-card horizontal">
                    <h4>Частота обслуживаний</h4>
                    <div class="stat-card-items">
                    <div class="stat-card-item">
                        <p class="stat-card-title">Всего</p>
                        <p class="stat-card-value">{{ total_maintenances }}</p>
                    </div>
                    <div class="stat-card-item">
                        <p class="stat-card-title">За этот месяц</p>
                        <p class="stat-card-value">{{ month_maintenances }}</p>
                    </div>
                    </div>
                </div>
                <MaintenanceCountChart :chartData="freq_chart_data" />
                </div>
            </div>

            <!-- Узлы обслуживания с вкладками -->
            <div class="section-wrapper nodes-wrapper">
                <div class="section-title-wrapper small">
                    <i class="fa fa-gear"></i>
                    <h3>Узлы обслуживания</h3>
                    <span class="nodes-count">{{ nodes.length }}</span>
                </div>

                <!-- Вкладки узлов -->
                <div v-if="nodes.length > 0" class="node-tabs-wrapper">
                    <div class="node-tabs">
                        <button 
                            class="node-tab-prev"
                            @click="prevNode"
                            :disabled="activeNodeIndex === 0"
                        >
                            <i class="fa fa-chevron-left"></i>
                        </button>
                        
                        <div class="node-tabs-container">
                            <div class="node-tabs-scroll" ref="tabsScroll">
                                <button
                                    v-for="(node, index) in nodes"
                                    :key="node.id || index"
                                    class="node-tab"
                                    :class="{ 'active': activeNodeIndex === index }"
                                    @click="selectNode(index)"
                                >
                                    <span class="node-tab-name">{{ node.title }}</span>
                                    <span class="node-tab-badge">{{ node.maintenances_count }}</span>
                                    <span 
                                        class="node-tab-health"
                                        :style="{ 
                                            background: node.health >= 80 ? 'var(--health-green, #4CAF50)' : 
                                                       node.health >= 50 ? 'var(--health-yellow, #FFC107)' : 
                                                       'var(--health-red, #F44336)'
                                        }"
                                    >
                                        {{ node.health }}%
                                    </span>
                                </button>
                            </div>
                        </div>

                        <button 
                            class="node-tab-next"
                            @click="nextNode"
                            :disabled="activeNodeIndex === nodes.length - 1"
                        >
                            <i class="fa fa-chevron-right"></i>
                        </button>
                    </div>

                    <!-- Индикатор -->
                    <div class="node-indicator">
                        <span class="node-indicator-text">
                            {{ activeNodeIndex + 1 }} / {{ nodes.length }}
                        </span>
                    </div>
                </div>

                <!-- Карточка активного узла -->
                <div v-if="activeNode" class="active-node-card">
                    <div class="node-card-header">
                        <div class="node-card-title-wrapper">
                            <h4 class="node-card-title">{{ activeNode.title }}</h4>
                            <span class="node-card-count">{{ activeNode.maintenances_count }}</span>
                        </div>
                        <button 
                            class="node-card-toggle"
                            @click="toggleNodeMaintenances"
                        >
                            <i class="fa" :class="showNodeMaintenances ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
                            <span>{{ showNodeMaintenances ? 'Скрыть' : 'Показать' }}</span>
                        </button>
                    </div>

                    <div class="node-card-body">
                        <!-- Здоровье узла -->
                        <div class="node-health">
                            <div class="node-health-header">
                                <span class="node-health-label">Здоровье узла</span>
                                <span class="node-health-value" :style="{ color: healthColor }">
                                    {{ activeNode.health }}%
                                </span>
                            </div>
                            <div class="node-health-bar">
                                <div 
                                    class="node-health-progress"
                                    :style="{ 
                                        width: activeNode.health + '%', 
                                        background: healthColor 
                                    }"
                                ></div>
                            </div>
                        </div>

                        <!-- Список обслуживаний -->
                        <div v-if="showNodeMaintenances" class="node-maintenances">
                            <div v-if="!activeNode.planned_maintenances || activeNode.planned_maintenances.length === 0" 
                                 class="empty-state small"
                            >
                                <i class="fa fa-wrench"></i>
                                <p>Нет запланированного обслуживания для этого узла</p>
                            </div>
                            
                            <MaintenanceCard
                                v-for="(maintenance, index) in activeNode.planned_maintenances"
                                :key="maintenance.id || index"
                                :maintenance="maintenance"
                                class="maintenance-card-item"
                                @edit="openEditPlanMaintenanceModal"
                                @delete="openDeletePlanMaintenanceModal"
                                @mark="openMarkPlanMaintenance"
                            />
                        </div>
                    </div>
                </div>

                <div v-else-if="nodes.length === 0" class="empty-state small">
                    <i class="fa fa-cogs"></i>
                    <p>Нет данных по узлам обслуживания</p>
                </div>
            </div>
        </div>
    </div>
    <!-- Модальные окна -->
    <UpdateMileageModal
        :isOpen="showUpdateMileageModal"
        :motorcycles="[motoData]"
        @close="showUpdateMileageModal=false"
        @submit="updateMotoMileage"
    />
    <EditMotoModal
        :isOpen="showEditMotoModal"
        :motorcycle="motoData"
        @submit="updateMoto"
        @close="showEditMotoModal=false"
    />
    <DeleteMotoModal
        :isOpen="showDeleteMotoModal"
        :motoId="selectedMoto"
        @submit="deleteMoto"
        @close="showDeleteMotoModal=false"
    />

    <AddMaintenanceModal
        :isOpen="showAddMaintenanceModal"
        :motorcycles="motorcycles"
        @close="showAddMaintenanceModal=false"
        @submit="addMaintenance"
    />
    <AddPlanMaintenanceModal
        :isOpen="showPlanMaintenanceModal"
        :motorcycles="motorcycles"
        @close="showPlanMaintenanceModal=false"
        @submit="addPlanMaintenance"
    />
    <EditPlanMaintenanceModal
        :isOpen="showEditPlanMaintenanceModal"
        :motorcycles="motorcycles"
        :maintenance="selectedMaintenance"
        @close="closeEditPlanMaintenanceModal"
        @submit="editPlanMaintenance"
    />
    <DeletePlanMaintenanceModal
        :isOpen="showDeletePlanMaintenanceModal"
        :maintenanceId="selectedDeleteMaintenanceId"
        @submit="deletePlanMaintenance"
        @close="closeDeletePlanMaintenanceModal"
    />
    <MarkPlanMaintenanceModal
        :isOpen="showMarkPlanMaintenanceModal"
        :id="markPlanMaintenanceId"
        @submit="markPlanMaintenance"
        @close="closeMarkPlanMaintenance"
    />
</template>


<style scoped>
p {
  margin-bottom: 0;
}

.section {
  background-color: var(--bg-primary);
  border: 2px solid var(--border-color);
  border-radius: 25px;
  padding: 28px;
  margin-bottom: 32px;
}

.section-title-wrapper {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 24px;
  margin-bottom: 28px;
}
.section-title-wrapper i {
  font-size: 32px;
  color: var(--accent);
}
.section-title-wrapper.small i {
  font-size: 24px;
}
.section-title-wrapper.small h3 {
  font-size: 1.3rem;
  margin-bottom: 0;
}

.nodes-count {
    background: var(--accent-light);
    color: var(--accent);
    border-radius: 20px;
    padding: 2px 14px;
    font-size: 14px;
    font-weight: 600;
    border: 1px solid var(--border-color);
    margin-left: 8px;
}

/* Статистика */
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
  padding: 20px 24px;
  min-width: 180px;
  flex: 1;
  background-color: var(--bg-secondary);
  border: 2px solid var(--border-color);
  border-radius: 24px;
  text-align: center;
  transition: all 0.3s;
}
.stat-card:hover {
  border-bottom: 3px solid var(--accent);
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}
.stat-card-title {
  font-weight: 500;
  font-size: 18px;
  color: var(--text-secondary);
}
.stat-card-value {
  font-weight: 700;
  color: var(--accent);
  font-size: 28px;
}
.stat-card.horizontal {
  flex-direction: column;
  align-items: stretch;
  min-width: unset;
  padding: 16px 20px;
}
.stat-card.horizontal h4 {
  margin-bottom: 8px;
  color: var(--text-primary);
}
.stat-card-items {
  display: flex;
  flex-direction: row;
  gap: 16px;
  justify-content: space-around;
  flex-wrap: wrap;
}
.stat-card-item {
  padding: 8px 16px;
  background-color: var(--bg-primary);
  border-radius: 18px;
  min-width: 100px;
}
.stat-card-item .stat-card-title {
  font-size: 14px;
}
.stat-card-item .stat-card-value {
  font-size: 20px;
}

/* Выбор мотоцикла */
.actions-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  max-width: 320px;
  margin: 0 auto;
}
.select-action {
  width: 250px;
}

/* Блоки внутри moto-section */
.moto-section {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.section-wrapper {
  background-color: var(--bg-secondary);
  border: 2px solid var(--border-color);
  border-radius: 25px;
  padding: 24px 28px;
  transition: background 0.2s;
}
.section-wrapper.actions-wrapper-block {
  background-color: var(--bg-primary);
}
.section-wrapper.moto-card-wrapper {
  background-color: var(--bg-card);
}
.section-wrapper.planned-wrapper {
  background-color: var(--bg-secondary);
}
.section-wrapper.stats-wrapper {
  background-color: var(--bg-primary);
}
.section-wrapper.nodes-wrapper {
  background-color: var(--bg-secondary);
}

/* Быстрые действия */
.fast-actions-wrapper {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  gap: 12px;
  flex-wrap: wrap;
}
.fast-actions-wrapper button {
  flex: 1;
  min-width: 200px;
  padding: 0.75rem 1.25rem;
  font-size: 0.95rem;
}

/* Пустые состояния внутри */
.empty-state.small {
  padding: 24px 16px;
  background-color: var(--bg-primary);
  border-radius: 18px;
  border: 2px dashed var(--border-color);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}
.empty-state.small i {
  font-size: 28px;
  color: var(--accent);
}
.empty-state.small p {
  color: var(--text-secondary);
  font-size: 16px;
  margin: 0;
}

/* Графики */
.chart-block {
  display: flex;
  flex-direction: row;
  gap: 20px;
  align-items: stretch;
  margin-bottom: 8px;
}
.chart-block > * {
  flex: 1;
}
.chart-sep {
  margin: 20px 0;
  border: 0;
  height: 2px;
  background: var(--border-color);
}

/* ===== NODE TABS ===== */
.node-tabs-wrapper {
    margin-top: 16px;
}

.node-tabs {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 16px;
}

.node-tabs-container {
    flex: 1;
    overflow: hidden;
    position: relative;
}

.node-tabs-scroll {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding: 4px 2px;
    scroll-behavior: smooth;
    -webkit-overflow-scrolling: touch;
}

.node-tabs-scroll::-webkit-scrollbar {
    height: 3px;
}

.node-tabs-scroll::-webkit-scrollbar-track {
    background: var(--bg-primary);
    border-radius: 10px;
}

.node-tabs-scroll::-webkit-scrollbar-thumb {
    background: var(--accent);
    border-radius: 10px;
}

.node-tab {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    background: var(--bg-primary);
    border: 2px solid var(--border-color);
    border-radius: 12px;
    color: var(--text-secondary);
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.25s ease;
    flex-shrink: 0;
    font-size: 0.85rem;
    font-weight: 500;
}

.node-tab:hover {
    background: var(--bg-card);
    border-color: var(--accent);
    transform: translateY(-2px);
}

.node-tab.active {
    background: var(--accent-light);
    border-color: var(--accent);
    color: var(--text-primary);
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.15);
}

.node-tab-name {
    max-width: 120px;
    overflow: hidden;
    text-overflow: ellipsis;
}

.node-tab-badge {
    background: var(--bg-secondary);
    padding: 1px 8px;
    border-radius: 10px;
    font-size: 0.7rem;
    color: var(--text-muted);
    border: 1px solid var(--border-color);
}

.node-tab.active .node-tab-badge {
    border-color: var(--accent);
    color: var(--text-primary);
}

.node-tab-health {
    font-size: 0.65rem;
    font-weight: 700;
    padding: 1px 8px;
    border-radius: 10px;
    color: white;
    min-width: 36px;
    text-align: center;
}

.node-tab-prev,
.node-tab-next {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    border: 2px solid var(--border-color);
    background: var(--bg-primary);
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.25s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.node-tab-prev:hover:not(:disabled),
.node-tab-next:hover:not(:disabled) {
    background: var(--accent-light);
    border-color: var(--accent);
    color: var(--text-primary);
    transform: scale(1.05);
}

.node-tab-prev:disabled,
.node-tab-next:disabled {
    opacity: 0.3;
    cursor: not-allowed;
    transform: none;
}

.node-indicator {
    text-align: center;
    margin-bottom: 16px;
}

.node-indicator-text {
    font-size: 0.75rem;
    color: var(--text-muted);
    background: var(--bg-primary);
    padding: 2px 14px;
    border-radius: 12px;
    border: 1px solid var(--border-color);
}

/* ===== ACTIVE NODE CARD ===== */
.active-node-card {
    background: var(--bg-primary);
    border-radius: 16px;
    padding: 20px 24px;
    border: 1px solid var(--border-color);
    transition: all 0.3s ease;
}

.active-node-card:hover {
    border-color: var(--accent);
}

.node-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 2px solid var(--border-color);
}

.node-card-title-wrapper {
    display: flex;
    align-items: center;
    gap: 12px;
}

.node-card-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--accent);
    margin: 0;
}

.node-card-count {
    background: var(--accent-light);
    color: var(--accent);
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 13px;
    font-weight: 600;
    border: 1px solid var(--border-color);
}

.node-card-toggle {
    display: flex;
    align-items: center;
    gap: 6px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
    color: var(--text-secondary);
    transition: all 0.2s ease;
    cursor: pointer;
}

.node-card-toggle:hover {
    background: var(--accent-light);
    border-color: var(--accent);
    color: var(--text-primary);
}

.node-card-body {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

/* Health */
.node-health {
    padding: 12px 0;
}

.node-health-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
}

.node-health-label {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

.node-health-value {
    font-size: 18px;
    font-weight: 700;
    transition: color 0.3s ease;
}

.node-health-bar {
    width: 100%;
    height: 8px;
    background: var(--bg-secondary);
    border-radius: 12px;
    overflow: hidden;
}

.node-health-progress {
    height: 100%;
    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1), background 0.3s ease;
    border-radius: 12px;
}

/* Maintenances list */
.node-maintenances {
    padding-top: 12px;
    border-top: 1px solid var(--border-color);
}

.maintenance-card-item {
    border-radius: 14px;
    transition: all 0.2s ease;
}

.maintenance-card-item:hover {
    transform: translateX(4px);
}

/* ===== RESPONSIVE ===== */
@media (max-width: 1024px) {
    .node-tab-name {
        max-width: 80px;
    }
}

@media (max-width: 768px) {
    .section {
        padding: 20px;
    }

    .section-title-wrapper {
        flex-wrap: wrap;
    }

    .statistics-cards {
        flex-direction: column;
        align-items: stretch;
    }

    .chart-block {
        flex-direction: column;
    }

    .stat-card-items {
        flex-direction: column;
        align-items: stretch;
    }

    .stat-card-item {
        min-width: unset;
    }

    .fast-actions-wrapper {
        flex-direction: column;
    }

    .fast-actions-wrapper button {
        min-width: unset;
        width: 100%;
    }

    .node-tabs {
        gap: 4px;
    }

    .node-tab {
        padding: 6px 10px;
        font-size: 0.75rem;
    }

    .node-tab-name {
        max-width: 60px;
    }

    .node-tab-health {
        font-size: 0.55rem;
        min-width: 28px;
        padding: 1px 4px;
    }

    .node-tab-prev,
    .node-tab-next {
        width: 28px;
        height: 28px;
        font-size: 12px;
    }

    .active-node-card {
        padding: 16px;
    }

    .node-card-title {
        font-size: 16px;
    }

    .node-card-toggle span {
        display: none;
    }
}

@media (max-width: 480px) {
    .section {
        padding: 14px;
    }

    .section-wrapper {
        padding: 16px;
    }

    .node-tab {
        padding: 4px 8px;
        font-size: 0.65rem;
        gap: 4px;
    }

    .node-tab-name {
        max-width: 40px;
    }

    .node-tab-badge {
        font-size: 0.6rem;
        padding: 0px 6px;
    }

    .node-tab-health {
        font-size: 0.5rem;
        min-width: 22px;
        padding: 0px 4px;
    }

    .active-node-card {
        padding: 12px;
    }

    .node-card-header {
        flex-wrap: wrap;
        gap: 8px;
    }

    .node-card-title {
        font-size: 14px;
    }

    .node-health-value {
        font-size: 16px;
    }
}
</style>