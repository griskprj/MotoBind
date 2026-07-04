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
            } catch (err) {
                console.error(err)
            } finally {
                this.loading = false
            }
        },

        // --- motorcycles ---
        async updateMotoMileage(formData) {
            // update motot mileage
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
                consoler.error(`Failed delete plan maintenance: ${err}`)
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

        <!-- Узлы обслуживания -->
        <div class="section-wrapper nodes-wrapper">
            <div class="section-title-wrapper small">
            <i class="fa fa-gear"></i>
            <h3>Узлы обслуживания</h3>
            </div>
            <div v-if="nodes.length === 0" class="empty-state small">
            <i class="fa fa-cogs"></i>
            <p>Нет данных по узлам</p>
            </div>
            <div v-else class="node-cards">
            <MaintenanceNodeCard
                v-for="node in nodes"
                :key="node.id"
                :node="node"
            />
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

/* Узлы */
.node-cards {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Адаптивность */
@media (max-width: 1024px) {
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
}

@media (max-width: 720px) {
  .section {
    padding: 18px;
  }
  .section-title-wrapper {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }
  .fast-actions-wrapper {
    flex-direction: column;
  }
  .fast-actions-wrapper button {
    min-width: unset;
    width: 100%;
  }
  .select-action {
    width: 100%;
    max-width: 300px;
  }
  .section-wrapper {
    padding: 18px;
  }
}
</style>