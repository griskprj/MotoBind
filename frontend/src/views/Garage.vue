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
        <!-- === WELCOME SECTION === -->
        <section>
            <div class="welcome-wrapper">
                <div>
                    <h2>Гараж</h2>

                    <div class="welcome-buttons">
                        <button class="welcome-btn-tab">Мои мотоциклы</button>
                        <button class="welcome-btn">Добавить мотоцикл</button>
                    </div>
                </div>

                <div class="welcome-actions">
                    <i class="fa fa-bell"></i>
                    
                    <div class="profile-link">
                        <router-link
                            to="/profile"
                            class="nav-link"
                            :class="{ active: $route.path === '/profile' }"
                        >
                            <img src="/BaseAvatar.jpg" alt="avatar" class="profile-img">
                        </router-link>

                        <div class="dropdown-menu">
                            <button @click="welcomeDropdownActive = !welcomeDropdownActive" class="dropdown-btn">
                                <i class="fa" :class="welcomeDropdownActive ? 'fa-angle-up' : 'fa-angle-down'"></i>
                            </button>

                            <div v-if="welcomeDropdownActive" class="dropdown-list">
                                <ul>
                                    <li><button class="dropdown-item-btn">Профиль</button></li>
                                    <li><button class="dropdown-item-btn">Настройки</button></li>
                                    <li><button @click="logout()" class="dropdown-item-btn">Выйти</button></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- === MOTORCYCLE SELECTOR === -->
        <section>
            <div class="cards-wrapper">
                <div class="moto-card active">
                    <div class="card-icon">
                        <i class="fa fa-motorcycle"></i>
                    </div>
                    <div class="card-info">
                        <p class="card-title">BMW s1000rr</p>
                        <p class="card-info-item">2020</p>
                        <p class="card-info-item">7500 км</p>
                    </div>
                    <div class="active-icon">
                        <i class="fa fa-check"></i>
                    </div>
                </div>
                <div class="moto-card">
                    <div class="card-icon">
                        <i class="fa fa-motorcycle"></i>
                    </div>
                    <div class="card-info">
                        <p class="card-title">Kawasaki Ninja 400</p>
                        <p class="card-info-item">2022</p>
                        <p class="card-info-item">5600 км</p>
                    </div>
                </div>
                <div class="moto-card add">
                    <i class="fa fa-plus"></i>
                    <p class="add-moto-card-text">Добавить мотоцикл</p>
                </div>
            </div>
        </section>

        <!-- === MOTORCYCLE INFO SECTION === -->
        <section>
            <div class="motorcycle-info-wrapper">
                <div class="big-moto-card">
                    <div class="big-card-header">
                        <p class="big-card-title">BMW s1000rr</p>
                        <button class="btn-small"><i class="fa fa-pen"></i></button>
                    </div>
                    <div class="big-card-img">
                        <img src="../../public/bmw1000.webp" alt="Фото мотоцикла">
                    </div>
                    <div class="big-card-body">
                        <div class="big-body-item">
                            <p class="big-body-item-title">Год выпуска</p>
                            <p class="big-body-item-value">2020</p>
                        </div>
                        <div class="big-body-item">
                            <p class="big-body-item-title">Двигатель</p>
                            <p class="big-body-item-value">999 cm³</p>
                        </div>
                        <div class="big-body-item">
                            <p class="big-body-item-title">Пробег</p>
                            <p class="big-body-item-value">20700 км</p>
                        </div>
                        <div class="big-body-item">
                            <p class="big-body-item-title">Цвет</p>
                            <div class="big-body-item-value color" style="background-color: #fff990;"></div>
                        </div>
                        <div class="big-body-item">
                            <p class="big-body-item-title">VIN</p>
                            <p class="big-body-item-value">WB10D01033LZR12345</p>
                        </div>
                        <div class="big-body-item">
                            <p class="big-body-item-title">Гос. номер</p>
                            <p class="big-body-item-value">0123AB23</p>
                        </div>
                    </div>
                    <div class="big-card-notes">
                        <div class="notes-header">
                            <p class="notes-title">Заметки</p>
                            <div class="notes-header-icon">
                                <button class="btn-small"><i class="fa fa-pen"></i></button>
                            </div>
                        </div>
                        <div class="notes-body">
                            <p class="notes-text">
                                Мотоцикл пригнан из Германии в 2023 году. Отличное состояние
                            </p>
                        </div>
                    </div>
                </div>

                <div class="maintenance-tab">
                    <div class="maintenance-stat">
                        <div class="stat-card">
                            <div class="stat-card-header">
                                <div class="stat-card-icon">
                                    <i class="fa fa-tachometer"></i>
                                </div>
                                <p class="stat-card-title">Пробег</p>
                            </div>
                            <p class="stat-card-value">7500 км</p>
                        </div>
                        <div class="stat-card">
                            <div class="stat-card-header">
                                <div class="stat-card-icon">
                                    <i class="fa fa-wrench"></i>
                                </div>
                                <p class="stat-card-title">Обслуживаний</p>
                            </div>
                            <p class="stat-card-value">12</p>
                        </div>
                        <div class="stat-card">
                            <div class="stat-card-header">
                                <div class="stat-card-icon">
                                    <i class="fa fa-calendar"></i>
                                </div>
                                <p class="stat-card-title">Следующее ТО</p>
                            </div>
                            <p class="stat-card-value">1250 км</p>
                        </div>
                        <div class="stat-card">
                            <div class="stat-card-header">
                                <div class="stat-card-icon">
                                    <i class="fa fa-ruble"></i>
                                </div>
                                <p class="stat-card-title">Общие расходы</p>
                            </div>
                            <p class="stat-card-value">12000 ₽</p>
                        </div>
                    </div>
                    <div class="maintenance-table-wrapper">
                        <div class="table-header-row">
                            <div class="th th-date">Дата</div>
                            <div class="th th-service">Обслуживание</div>
                            <div class="th th-mileage">Пробег</div>
                            <div class="th th-cost">Стоимость</div>
                            <div class="th th-status">Статус</div>
                            <div class="th th-action"></div>
                        </div>

                        <div class="table-body">
                            <div class="table-row">
                                <div class="td td-date">
                                    <div class="td-icon-wrapper purple-bg">
                                        <i class="fa fa-wrench"></i>
                                    </div>
                                    <span class="td-date-text">12 мая 2025</span>
                                </div>
                                <div class="td td-service">
                                    <div class="service-title">Замена масла</div>
                                    <div class="service-desc">Масло Motul 7100 10W-40, масляный фильтр</div>
                                </div>
                                <div class="td td-mileage">7 500 км</div>
                                <div class="td td-cost">4 250 ₽</div>
                                <div class="td td-status">
                                    <span class="status-badge done">Выполнено</span>
                                </div>
                                <div class="td td-action">
                                    <i class="fa fa-chevron-right"></i>
                                </div>
                            </div>

                            <div class="table-row">
                                <div class="td td-date">
                                    <div class="td-icon-wrapper green-bg">
                                        <i class="fa fa-trash"></i>
                                    </div>
                                    <span class="td-date-text">08 апр 2025</span>
                                </div>
                                <div class="td td-service">
                                    <div class="service-title">Замена воздушного фильтра</div>
                                    <div class="service-desc">Воздушный фильтр K&N</div>
                                </div>
                                <div class="td td-mileage">6 850 км</div>
                                <div class="td td-cost">2 350 ₽</div>
                                <div class="td td-status">
                                    <span class="status-badge done">Выполнено</span>
                                </div>
                                <div class="td td-action">
                                    <i class="fa fa-chevron-right"></i>
                                </div>
                            </div>

                            <div class="table-row">
                                <div class="td td-date">
                                    <div class="td-icon-wrapper blue-bg">
                                        <i class="fa fa-shield-alt"></i>
                                    </div>
                                    <span class="td-date-text">15 мар 2025</span>
                                </div>
                                <div class="td td-service">
                                    <div class="service-title">Замена передних колодок</div>
                                    <div class="service-desc">Тормозные колодки Brembo</div>
                                </div>
                                <div class="td td-mileage">6 300 км</div>
                                <div class="td td-cost">6 800 ₽</div>
                                <div class="td td-status">
                                    <span class="status-badge done">Выполнено</span>
                                </div>
                                <div class="td td-action">
                                    <i class="fa fa-chevron-right"></i>
                                </div>
                            </div>
                            
                            <div class="table-footer-btn">
                                <button class="outline-btn">Подробнее <i class="fa fa-chevron-right"></i></button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
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

.welcome-buttons {
    display: flex;
    flex-direction: row;
    gap: 8px;
}

.welcome-btn {
    background-color: var(--bg-card);
}
.welcome-btn:hover {
    background-color: var(--accent);
}

.welcome-btn-tab {
    background-color: var(--accent-light);
    cursor: default;
}
.welcome-btn-tab:hover {
    transform: translateY(0px);
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


/* === MOTORCYCLE SELECTOR === */
.motorcycle-info-wrapper {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(1, 1fr);
    gap: 16px;
}
.maintenance-tab {
    grid-column: span 3 / span 3;
}

.cards-wrapper {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(1, 1fr);
    gap: 8px;
}

.moto-card {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    min-width: 256px;
    padding: 12px;
    background-color: var(--bg-card);
    border-radius: 14px;
    cursor: pointer;

    transition: all 0.3s ease;
}

.moto-card:hover {
    transform: translateY(-2px);
}

.moto-card.active {
    background-color: var(--accent-trans);
    border: 1px solid var(--accent);
}

.moto-card.add {
    display: flex;
    flex-direction: column;
    gap: 8px;
    color: var(--accent);
    background-color: transparent;
    border: 2px dashed var(--accent-light);
}

.card-icon {
    width: 48px;
    height: 48px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
    background-color: rgba(124, 58, 237, 0.2);
    color: #a78bfa;
}

.active-icon {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 24px;
    height: 24px;
    background-color: var(--accent);
    border-radius: 50%;
}

.card-title {
    margin-bottom: 4px;
    font-weight: 600;
}

.card-info-item {
    color: var(--text-secondary);
    font-size: 12px;
    margin-bottom: 8px;
}

@media (max-width: 1220px) {
    .cards-wrapper {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(1, 1fr);
        gap: 8px;
    }
}

@media (max-width: 820px) {
    .cards-wrapper {
        display: grid;
        grid-template-columns: repeat(1, 1fr);
        grid-template-rows: repeat(1, 1fr);
        gap: 8px;
    }
}


.big-moto-card {
    padding: 18px;
    background-color: var(--bg-card);
    border-radius: 16px;
}

.big-card-img {
    margin-bottom: 12px;
}

.big-card-img img {
    width: 256px;
    height: 128px;
    border-radius: 16px;
}

.big-card-header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-bottom: 8px;
}

.big-card-body {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(3, 1fr);
    gap: 8px;
}

.big-body-item-title {
    font-size: 12px;
    color: var(--text-secondary);
    margin-bottom: 4px;
}

.big-body-item-value {
    font-size: 14px;
}

.big-body-item-value.color {
    width: 64px;
    height: 12px;
    border-radius: 25px;
}

.big-card-notes {
    padding: 16px 14px;
    background-color: var(--bg-secondary);
    border-radius: 10px;
}

.notes-header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}

.notes-text {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 0;
}

/* maintenance stat */
.maintenance-stat {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(1, 1fr);
    gap: 8px;
    margin-bottom: 16px;
}

.stat-card {
    padding: 16px;
    background-color: var(--bg-card);
    border-radius: 16px;
}

.stat-card-header {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 8px;

    margin-bottom: 12px;
}

.stat-card-icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--accent-trans);
    color: var(--accent);
    border-radius: 10px;
}

.stat-card-title {
    font-size: 14px;
    color: var(--text-secondary);
}

.stat-card-value {
    font-size: 20px;
    font-weight: 600;
    text-align: center;
}

/* table */
/* === MAINTENANCE TABLE (Flex вместо классической таблицы) === */
.maintenance-table-wrapper {
    background-color: var(--bg-card);
    border-radius: 16px;
    padding: 16px 0;
    margin-top: 16px;
}

/* Заголовки таблицы */
.table-header-row {
    display: grid;
    grid-template-columns: 180px 1fr 100px 100px 130px 40px;
    padding: 12px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    color: var(--text-muted);
    font-size: 13px;
    font-weight: 500;
}

/* Строка данных */
.table-row {
    display: grid;
    grid-template-columns: 180px 1fr 100px 100px 130px 40px;
    padding: 16px 20px;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    transition: background 0.2s ease;
    cursor: pointer;
}

.table-row:hover {
    background-color: rgba(255, 255, 255, 0.02);
}
.table-row:last-child {
    border-bottom: none;
}

/* Ячейка "Дата" */
.td-date {
    display: flex;
    align-items: center;
    gap: 12px;
}
.td-icon-wrapper {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
}
.td-date-text {
    font-size: 14px;
    color: var(--text-primary);
}

/* Ячейка "Обслуживание" */
.td-service {
    display: flex;
    flex-direction: column;
    gap: 2px;
}
.service-title {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-primary);
}
.service-desc {
    font-size: 13px;
    color: var(--text-muted);
}

/* Ячейки "Пробег" и "Стоимость" */
.td-mileage, .td-cost {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-primary);
}

/* Ячейка "Статус" */
.status-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    background: rgba(34, 197, 94, 0.15);
    color: #4ade80;
}

/* Стрелка справа */
.td-action {
    display: flex;
    justify-content: flex-end;
    color: #4b4b5e;
    font-size: 14px;
    transition: color 0.2s ease;
}
.table-row:hover .td-action {
    color: #a78bfa;
}

/* Кнопка "Показать ещё" */
.table-footer-btn {
    display: flex;
    justify-content: center;
    padding: 16px 20px 0;
}
.table-footer-btn button {
    width: 100%;
}

/* Цвета для иконок */
.purple-bg { background: rgba(124, 58, 237, 0.15); color: #a78bfa; }
.green-bg { background: rgba(34, 197, 94, 0.15); color: #4ade80; }
.blue-bg { background: rgba(59, 130, 246, 0.15); color: #93c5fd; }

/* Адаптив для экранов поменьше */
@media (max-width: 1100px) {
    .table-header-row, .table-row {
        grid-template-columns: 150px 1fr 80px 80px 110px 30px;
        padding: 12px 16px;
    }
}

@media (max-width: 820px) {
    /* На планшетах и телефонах превращаем таблицу в карточки */
    .table-header-row {
        display: none;
    }
    .table-row {
        grid-template-columns: 1fr;
        gap: 6px;
        padding: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        margin-bottom: 8px;
        background-color: var(--bg-secondary);
    }
    .table-row:hover {
        background-color: var(--bg-secondary);
    }
    
    .td-date {
        order: 1;
    }
    .td-service {
        order: 2;
        padding-left: 44px; /* Отступ под иконку */
    }
    .td-mileage {
        order: 3;
        padding-left: 44px;
    }
    .td-cost {
        order: 4;
        padding-left: 44px;
    }
    .td-status {
        order: 5;
        padding-left: 44px;
    }
    .td-action {
        order: 6;
        position: absolute;
        right: 16px;
        top: 20px;
    }
    .table-row {
        position: relative;
    }
    
    /* Добавляем подписи к данным на мобилках */
    .td-mileage::before {
        content: "Пробег: ";
        color: var(--text-muted);
        font-weight: 400;
    }
    .td-cost::before {
        content: "Стоимость: ";
        color: var(--text-muted);
        font-weight: 400;
    }
}
</style>