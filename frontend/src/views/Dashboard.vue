<script>
import api from '../api/api';
import { getUser } from '../api/auth';
import AddMotoModal from '../components/modals/moto/AddMotoModal.vue';
import DeleteMotoModal from '../components/modals/moto/DeleteMotoModal.vue';
import EditMotoModal from '../components/modals/moto/EditMotoModal.vue';
import UpdateMileageModal from '../components/modals/moto/UpdateMileageModal.vue';

import AddMaintenanceModal from '../components/modals/maintenance/AddMaintenanceModal.vue';
import AddPlanMaintenanceModal from '../components/modals/maintenance/AddPlanMaintenanceModal.vue';
import EditPlanMaintenanceModal from '../components/modals/maintenance/EditPlanMaintenanceModal.vue';
import DeletePlanMaintenanceModal from '../components/modals/maintenance/DeletePlanMaintenanceModal.vue';
import MarkPlanMaintenanceModal from '../components/modals/maintenance/MarkPlanMaintenanceModal.vue';


export default {
    components: {
        AddMotoModal,
        EditMotoModal,
        DeleteMotoModal,
        UpdateMileageModal,

        AddMaintenanceModal,
        AddPlanMaintenanceModal,
        EditPlanMaintenanceModal,
        DeletePlanMaintenanceModal,
        MarkPlanMaintenanceModal
    },

    data() {
        return {
            user: null,
            loading: false,

            // === Motorcycle vars ===
            // moto list
            motorcycles: [],

            // modals vars
            showEditMotoModal: false,
            showDeleteMotoModal: false,
            showCreateMotoModal: false,
            showUpdateMileageModal: false,

            // other vars
            deleteMotoId: null,
            selectedMoto: null,
            // === --- ===



            // === History maintenances vars ===
            // maintenances list
            maintenances: [],

            // modals vars
            showAddMaintenanceModal: false,
            showAddPlanMaintenanceModal: false,
            showEditPlanMaintenanceModal: false,
            showDeletePlanMaintenanceModal: false,
            showMarkPlanMaintenanceModal: false,


            // other vars
            selectedPlanMaintenance: null,
            deletePlanMaintenanceId: null,
            markPlanMaintenanceId: null,
            // === --- ===
        }
    },

    methods: {
        async loadData() {
            try {
                this.loading = true
                const response = await api.get('/statistic/dashboard-data')

                this.user = getUser()
                this.motorcycles = response.data.motorcycles
                this.maintenances = response.data.maintenance.flat(Infinity)
            } catch(err) {
                console.error(err)
            } finally {
                this.loading = false
            }
        },



        // ===== MOTORCYCLES =====

        // --> Async functions
        async handleMotoCreated(formData) {
            // create moto
            try {
                this.loading = true
                this.loadData()

                const { data } = await api.post('/motorcycle/new', formData)

                this.motorcycles.push(data)
                this.showCreateMotoModal = false

                alert('Мотоцикл добавлен!')
            } catch(err) {
                console.error('Failed create moto:', err)
            } finally {
                this.loading = false
            }
        },

        async handleMotoUpdated(formData) {
            // update moto
            try {
                this.loading = true
                const { data } = await api.put(`/motorcycle/${formData.id}`, formData)

                const index = this.motorcycles.findIndex(m => m.id === formData.id)
                
                if (index !== -1) {
                    this.motorcycles[index] = data
                }

                this.showEditMotoModal = false
                alert('Мотоцикл обновлен!')
            } catch(err) {
                console.error('Failed update moto:', err)
            } finally {
                this.loading = false
            }
        },

        async handleMotoMileageUpdated(formData) {
            // update moto mileage
            try {
                this.loading = true

                const { data } = await api.patch(`motorcycle/${formData.id}`, formData)

                const index = this.motorcycles.findIndex(m => m.id === formData.id)
                
                if (index !== -1) {
                    this.motorcycles[index] = data
                }

                this.showUpdateMileageModal = false
                alert('Пробег мотоцикла обновлен!')
            } catch(err) {
                console.error('Failed update moto mileage', err)
            } finally {
                this.loading = false
            }
        },

        async handleMotoDeleted(motoId) {
            // delete moto
            try {
                this.loading = true
                await api.delete(`/motorcycle/${motoId}`)

                const index = this.motorcycles.findIndex(m => m.id === motoId)
                
                if (index !== -1) {
                    this.motorcycles.splice(index, 1)
                }

                this.showDeleteMotoModal = false
                alert('Мотоцикл удален!')
            } catch(err) {
                console.error('Failed delete moto:', err)
            } finally {
                this.loading = false
            }
        },


        // ---> Modals function
        
        // create moto
        openCreateMotoModal() {
            this.showCreateMotoModal = true
        },

        // edit moto
        openEditMotoModal(moto) {
            this.selectedMoto = moto
            this.showEditMotoModal = true
        },
        closeEditMotoModal() {
            this.showEditMotoModal = false
            this.selectedMoto = null
        },

        // update moto mileage
        openUpdateMileageModal() {
            this.showUpdateMileageModal = true
        },

        // delete moto
        openDeleteMotoModal(motoId) {
            this.deleteMotoId = motoId
            this.showDeleteMotoModal = true
        },
        closeDeleteMotoModal() {
            this.showDeleteMotoModal = false
            this.deleteMotoId = null
        },
        // ===== --- =====



        // === MAINTENANCES ===

        // ---> Async functions
        async handleMaintenanceCreated(formData) {
            // create history maintenance record
            try {
                this.loading = true

                const { data } = await api.post('/maintenance/create-new', formData)

                this.showAddMaintenanceModal = false

                alert('Запись обслуживания добавлена в историю!')
            } catch (err) {
                console.error('Failed add maintenence:', err)
            } finally {
                this.loading = false
            }
        },

        async handlePlanMaintenanceCreated(formData) {
            // create plan maintenance record
            try {
                this.loading = true

                const { data } = await api.post('/maintenance/plan', formData)

                this.maintenances.push(data)
                this.showAddPlanMaintenanceModal = false

                alert('Обслуживание запланировано')
            } catch(err) {
                console.error('Failed plan maintenance', err)
            } finally {
                this.loading = false
            }
        },

        async handlePlanMaintenanceUpdated(formData) {
            // update plan maintenance
            try {
                this.loading = true

                const { data } = await api.put(`/maintenance/plan`, formData)

                const index = this.maintenances.findIndex(m => m.id === formData.maintenanceId)
                if (index !== -1) {
                    this.maintenances[index] = data
                }

                this.showEditPlanMaintenanceModal = false
                alert('Запланированное обслуживание обновлено!')
            } catch(err) {
                console.error('Failed edit plan maintenance', err)
            } finally {
                this.loading = false
            }
        },

        async handlePlanMaintenanceDeleted(maintenanceId) {
            // delete plan maintenance
            try {
                this.loading = true

                await api.delete(`/maintenance/plan/${maintenanceId}`)
                
                const index = this.maintenances.findIndex(m => m.id === maintenanceId)
                if (index !== -1) {
                    this.maintenances.splice(index, 1)
                }

                this.showDeletePlanMaintenanceModal = false
                this.selectedPlanMaintenance = null
                alert('Запланированное обслуживание удалено!')
            } catch(err) {
                alert('Ошибка удаления обслуживания')
                console.error('Failed delete plan maintenance', err)
            } finally {
                this.loading = false
            }
        },

        async handlePlanMaintenanceMarked(formData) {
            // mark plan maintenance
            try {
                this.loading = true

                const response = await api.post('/maintenance/plan/mark', formData)
                
                if (response.maintenance) {
                    this.maintenances.push(response.maintenance)
                }

                const index = this.maintenances.findIndex(m => m.id === formData.id)
                if (index !== -1) {
                    this.maintenances.splice(index, 1)
                }

                this.showMarkPlanMaintenanceModal = false
                this.markPlanMaintenanceId = null
                alert('Запланированное обслуживание отмечено!')
            } catch(err) {
                alert('Ошибка отметки обслуживания')
                console.error('Failed mark plan maintenance', err)
            } finally {
                this.loading = false
            }
        },


        // ---> Modals functions

        // create history maintenance
        openAddMaintenanceModal() {
            this.showAddMaintenanceModal = true
        },

        // create plan maintenance
        openAddPlanMaintenanceModal() {
            this.showAddPlanMaintenanceModal = true
        },

        // edit plan maintenance
        openEditPlanMaintenanceModal(maintenance) {
            this.selectedPlanMaintenance = maintenance
            this.showEditPlanMaintenanceModal = true
        },
        closeEditPlanMaintenanceModal() {
            this.selectedPlanMaintenance = null
            this.showEditPlanMaintenanceModal = false
        },

        // delete plan maintenance
        openDeletePlanMaintenanceModal(maintenanceId) {
            this.deletePlanMaintenanceId = maintenanceId
            this.showDeletePlanMaintenanceModal = true
        },
        closeDeletePlanMaintenanceModal() {
            this.showDeletePlanMaintenanceModal = false
            this.deletePlanMaintenanceId = null
        },

        // mark plan maintenance
        openMarkPlanMaintenanceModal(maintenanceId) {
            this.showMarkPlanMaintenanceModal = true
            this.markPlanMaintenanceId = maintenanceId
        },
        closeMarkPlanMaintenanceModal() {
            this.showMarkPlanMaintenanceModal = false
            this.markPlanMaintenanceId = null
        }
    },

        
    mounted() {
        this.loadData()
    }
}
</script>

<template>
    <div class="container">
        <!-- === WELCOME SECTION === -->
        <div class="welcome-section">
            <div class="welcome-wrapper">
                <h2>Здравствуйте,</h2> <h2 class="welcome-title">{{ user?.username }}</h2>
            </div>
            <p class="welcome-subtitle">Ваш мотоцикл в отличной форме <span v-if="maintenances.length > 0"> , но есть пару моментов, на которые стоит обратить внимание</span></p>
        </div>

        <!-- === FAST ACTIONS === -->
        <div class="fast-actions-section">
            <h2 class="section-title">Быстрые действия</h2>
            <div class="fast-actions-wrapper">
                <button @click="openCreateMotoModal()"><i class="fa fa-motorcycle"></i> Добавить мотоцикл</button>
                <button @click="openUpdateMileageModal()"><i class="fa fa-tachometer"></i> Обновить пробег</button>
                <button @click="openAddMaintenanceModal()" :disabled="motorcycles.length === 0"><i class="fa fa-wrench"></i> Добавить обслуживание</button>
                <button @click="openAddPlanMaintenanceModal()" :disabled="motorcycles.length === 0"><i class="fa fa-calendar"></i> Планировать обслуживание</button>
            </div>
        </div>
      
        <!-- === MOTORCYCLE SECTION === -->
        <div class="motorcycle-section">
            <h2 class="section-title"><i class="fa fa-motorcycle"></i> Мои мотоциклы</h2>
            <div v-if="motorcycles.length === 0" class="empty-state">
                <i class="fa fa-motorcycle"></i>
                <p class="empty-state-p">У вас нет мотоциклов</p>
                <button @click="openCreateMotoModal()" class="btn add-maintenance">
                    Добавить
                </button>
            </div>
            <div v-else v-for="moto in motorcycles" class="moto-card">
                <div class="moto-card-header">
                    <p>{{ moto.name }}</p>
                    <div class="moto-actions">
                        <button @click="openEditMotoModal(moto)" class="moto-action"><i class="fa fa-pen"></i></button>
                        <button @click="openDeleteMotoModal(moto.id)" class="moto-action"><i class="fa fa-trash"></i></button>
                    </div>
                </div>
                <div class="moto-card-body">
                    <div class="moto-card-meta">
                        <div class="meta-items">
                            <div class="meta-item">
                                <p class="meta-text">Объем:</p> <p>{{ moto.volume }} см3</p>
                            </div>
                            <div class="meta-item">
                                <p class="meta-text">Год выпуска:</p> <p>{{ moto.years }} г.</p>
                            </div>
                            <div class="meta-item">
                                <p class="meta-text">Пробег:</p> <p>{{ moto.mileage ? moto.mileage : 0 }} км</p>
                            </div>
                        </div>
      
                        <button class="follow-btn btn">Подробнее</button>
                    </div>
                    <div class="img-wrapper">
                        <img src="/moto_default.jpg" alt="Motorcycle" class="moto-img">
                    </div>
                </div>
            </div>
        </div>
        
        <!-- === PENDING MAINTENANCE SECTION === -->
        <div class="maintenance-section">
            <h2 class="maintenance-section-title"><i class="fa fa-wrench"></i> Предстоящее обслуживание</h2>
            <div class="maintenance-cards">
                <div v-if="maintenances.length === 0" class="empty-state">
                    <i class="fa fa-wrench"></i>
                    <p class="empty-state-p">У вас нет запланированного обслуживания</p>
                    <button @click="openAddPlanMaintenanceModal()" :disabled="motorcycles.length === 0" class="btn add-maintenance">
                        Добавить
                    </button>
                </div>
                <div v-else v-for="maintenance in maintenances" class="maintenance-card">
                    <div class="maintenance-header">
                        <div class="maintenance-icon">
                            <i class="fa fa-wrench"></i>
                        </div>
                        <p class="maintenance-title">{{ maintenance.title }}</p>
                    </div>
                    <div class="maintenance-body">
                        <div class="maintenance-meta">
                            <p v-if="maintenance.planned_date" class="maintenance-meta-item">Дата: {{ maintenance.planned_date }}</p>
                            <p v-if="maintenance.planned_mileage" class="maintenance-meta-item">Пробег: {{ maintenance.planned_mileage}}</p>
                        </div>
                        <div class="maintenance-actions">
                            <div class="actions-wrapper">
                                <button @click="openEditPlanMaintenanceModal(maintenance)" class="maintenance-action"><i class="fa fa-pen"></i></button>
                                <button @click="openDeletePlanMaintenanceModal(maintenance.id)" class="maintenance-action"><i class="fa fa-trash"></i></button>
                            </div>
                            <button @click="openMarkPlanMaintenanceModal(maintenance.id)" class="accept-btn"><i class="fa fa-check"></i></button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Add motorcycle -->
    <AddMotoModal 
        :is-open="showCreateMotoModal"
        @submit="handleMotoCreated"
        @close="showCreateMotoModal = false"
    />

    <!-- Edit Motorcycle -->
    <EditMotoModal
        :is-open="showEditMotoModal"
        :motorcycle="selectedMoto"
        @submit="handleMotoUpdated"
        @close="showEditMotoModal = false"
    />

    <!-- Update moto mileage -->
    <UpdateMileageModal
        :is-open="showUpdateMileageModal"
        :motorcycles="motorcycles"
        @submit="handleMotoMileageUpdated"
        @close="showUpdateMileageModal = false"
    />

    <!-- Delete moto modal -->
    <DeleteMotoModal
        :is-open="showDeleteMotoModal"
        :motoId="deleteMotoId"
        @submit="handleMotoDeleted"
        @close="closeDeleteMotoModal"
    />

    <!-- Add maintenance -->
    <AddMaintenanceModal
        :is-open="showAddMaintenanceModal"
        :motorcycles="motorcycles"
        @submit="handleMaintenanceCreated"
        @close="showAddMaintenanceModal = false"
    />

    <!-- Plan maintenance -->
    <AddPlanMaintenanceModal
        :is-open="showAddPlanMaintenanceModal"
        :motorcycles="motorcycles"
        @submit="handlePlanMaintenanceCreated"
        @close="showAddPlanMaintenanceModal = false"
    />


    <!-- Edit plan maintenance -->
    <EditPlanMaintenanceModal
        :is-open="showEditPlanMaintenanceModal"
        :motorcycles="motorcycles"
        :maintenance="selectedPlanMaintenance"
        @submit="handlePlanMaintenanceUpdated"
        @close="closeEditPlanMaintenanceModal"
    />

    <!-- Delete plan maintenance -->
    <DeletePlanMaintenanceModal
        :is-open="showDeletePlanMaintenanceModal"
        :maintenance-id="deletePlanMaintenanceId"
        @submit="handlePlanMaintenanceDeleted"
        @close="closeDeletePlanMaintenanceModal"
    />

    <!-- Mark maintenance -->
    <MarkPlanMaintenanceModal
        :is-open="showMarkPlanMaintenanceModal"
        :id="markPlanMaintenanceId"
        @submit="handlePlanMaintenanceMarked"
        @close="closeMarkPlanMaintenanceModal"
    />
</template>

<style scoped>
p {
    margin-bottom: 0;
}

/* Welcome Section */
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
    gap: 12px;
}

.welcome-title {
    color: var(--accent);
}


/* Fast actions section */
.fast-actions-section {
    background-color: var(--bg-primary);
    border: 2px solid var(--border-color);
    border-radius: 25px;

    padding: 28px;
    margin-bottom: 32px;
}

.section-title {
    margin-bottom: 24px;
}

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


/* Motorcycle Section */
.motorcycle-section {
    background-color: var(--bg-primary);
    border: 2px solid var(--border-color);
    border-radius: 25px;

    margin-bottom: 32px;
    padding: 28px;
}

.moto-card {
    padding: 15px;
    background-color: var(--bg-secondary);
    margin-bottom: 24px;
    border-radius: 18px;

    border: 2px solid var(--accent-light);

    transition: all 0.3s;
}

.moto-card:hover {
    transform: translateY(-5px);
}

.moto-card-header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-bottom: 24px;
}

.moto-card-header p {
    font-size: 24px;
    color: var(--accent);
    font-weight: 600;
}

.moto-actions {
    display: flex;
    flex-direction: row;
    gap: 12px;
}

.moto-actions button {
    max-height: 32px;
    max-width: 32px;
}

.moto-card-body {
    display: flex;
    width: 100%;
    justify-content: space-between;
    gap: 24px;

    overflow: hidden;
}

.img-wrapper {
    flex: 0 0 40%;
    max-height: 284px;
}
.moto-img {
  width: 100%;
  height: 100%;
  object-fit: cover; 
  border-radius: 25px;
  object-position: center center;
  filter: brightness(0.5);
}

.moto-card-meta {
    flex: 1;
    padding: 20px;

    background-color: var(--bg-secondary);
    border-radius: 25px;
}

.meta-items {
    margin-bottom: 24px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.meta-item {
    display: flex;
    flex-direction: row;
    justify-content: space-between;

    padding: 8px 14px 8px 14px;

    background-color: var(--bg-primary);

    border-radius: 50px;
}

.meta-text {
    color: var(--accent);
    font-weight: 500;
}

.follow-btn {
    width: 100%;
}



@media (max-width: 728px) {
    .moto-card {
        padding: 8px;
    }

    .moto-card-body {
        flex-direction: column-reverse;
    }

    .moto-card-header {
        flex-direction: column;
        gap: 12px;
        align-items: center;
    }

    .moto-actions {
        flex-direction: column;
        width: 100%;
    }

    .moto-action {
        min-width: 100%;    
    }
}



/* Pending Maintenance Section */
.maintenance-section {
    background-color: var(--bg-primary);
    border: 2px solid var(--border-color);
    border-radius: 25px;

    margin-bottom: 32px;
    padding: 28px;
}

.maintenance-cards {
    margin-top: 24px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.maintenance-card {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    padding: 18px;
    background-color: var(--bg-secondary);
    border: 2px solid var(--border-color);
    border-radius: 25px;
}

.maintenance-header {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 8px;
}

.maintenance-icon i {
    text-align: center;
    border-radius: 8px;
    padding: 12px;
    background-color: var(--accent);
    margin-right: 12px;
}

.maintenance-title {
    font-size: 20px;
    font-weight: 500;
    color: var(--text-primary)
}

.maintenance-body {
    display: flex;
    flex-direction: row;
    align-items: center;

    gap: 32px;
}

.maintenance-meta {
    background-color: var(--bg-primary);
    padding: 12px;
    border-radius: 8px;
}

.maintenance-actions {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.actions-wrapper {
    display: flex;
    flex-direction: row;
    gap: 8px;
}

@media (max-width: 728px) {
    .maintenance-card {
        flex-direction: column;
    }

    .maintenance-header {
        margin-bottom: 18px;
    }

    .maintenance-body {
        flex-direction: column;
    }

    .maintenance-meta {
        width: 100%;
        text-align: center;
    }

    .maintenance-actions {
        flex-direction: column;
        width: 100%;
    }

    .maintenance-action {
        width: 100%;
    }
}


/* Empty State */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 48px;
    background-color: var(--bg-secondary);
    border-radius: 24px;
    border: 2px dashed var(--border-color);

    text-align: center;
}

.empty-state i {
    font-size: 32px;
    color: var(--accent);
    margin-bottom: 12px;
}

.empty-state-p {
    font-size: 18px;
    font-weight: 500;
    color: var(--text-secondary);

    margin-bottom: 12px;
}
</style>