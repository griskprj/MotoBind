<script>
import api from '../api/api';
import { getUser } from '../api/auth';
import AddMotoModal from '../components/modals/moto/AddMotoModal.vue';
import DeleteMotoModal from '../components/modals/moto/DeleteMotoModal.vue';
import EditMotoModal from '../components/modals/moto/EditMotoModal.vue';

export default {
    components: {
        AddMotoModal,
        EditMotoModal,
        DeleteMotoModal
    },

    data() {
        return {
            user: null,
            motorcycles: [],
            maintenances: [],
            loading: false,

            showEditMotoModal: false,
            showDeleteMotoModal: false,
            showCreateMotoModal: false,
            showUpdateMileageModal: false,
            showAddMaintenanceModal: false,
            showPlanMaintenanceModal: false,
            showMarkPlanMaintenanceModal: false,
            showEditPlanMaintenanceModal: false,
            showDeletePlanMaintenanceModal: false,

            // Motorcycle vars
            deleteMotoId: null,
            selectedMoto: null,
            // === --- ===

            addMaintenanceModal: {
                motorcycleId: null,
                title: '',
                description: '',
                mileage: null,
                date: null
            },

            planMaintenanceModal: {
                motorcycleId: null,
                title: '',
                description: '',
                mileage: null,
            },

            editPlanMaintenanceModal: {
                maintenanceId: null,
                motorcycleId: null,
                title: '',
                description: '',
                mileage: null,
            },

            deleteMaintenanceId: null,

            markPlanMaintenanceModal: {
                maintenanceId: null,
                mileage: null,
                date: null,
                isRepeat: false,
                interval: null
            },

            updateMileageModal: {
                newMileage: null,
                motoId: null
            }
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
            try {
                this.loading = true

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

        async handleMotoEdited(formData) {
            try {
                this.loading = true

                const { data } = await api.put(`/motorcycle/${formData.motoId}`, formData)

                this.motorcycles.push(data)
                this.showEditMotoModal = false
                
                alert('Изменения сохранены!')
            } catch(err) {
                console.error('Failed edit moto:', err)
            } finally {
                this.loading = false
            }
        },

        async handleMotoUpdated(formData) {
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

        async handleMotoDeleted(motoId) {
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
            console.log(this.selectedMoto)
            this.showEditMotoModal = true
        },
        closeEditMotoModal() {
            this.showEditMotoModal = false
            this.selectedMoto = null
        },

        // delete moto
        openDeleteMotoModal(motoId) {
            this.deleteMotoId = motoId
            this.showDeleteMotoModal = true
        },
        // ===== --- =====

        

        async deleteMoto() {
            try {
                this.loading = true
                const response = await api.delete(`/motorcycle/${this.deleteMotoId}`)

                this.showDeleteMotoModal = false
                this.loadData()
            } catch (err) {
                console.error(err)
            } finally {
                this.loading = false
            }
        },

        async updateMileage() {
            try {
                this.loading = true

                const response = await api.patch(`motorcycle/${this.updateMileageModal.motoId}`, this.updateMileageModal)

                this.showUpdateMileageModal = false
                this.loadData()
            } catch(err) {
                console.error('Failed update mileage', err)
            } finally {
                this.loading = false
            }
        },

        async addMaintenance() {
            try {
                this.loading = true

                const response = await api.post('/maintenance/create-new', this.addMaintenanceModal)

                this.showAddMaintenanceModal = false
                this.loadData()
            } catch (err) {
                console.error('Failed add maintenence:', err)
            } finally {
                this.loading = false
            }
        },

        async planMaintenance() {
            try {
                this.loading = true

                const response = await api.post('/maintenance/plan', this.planMaintenanceModal)

                this.showPlanMaintenanceModal = false
                this.loadData()
            } catch(err) {
                console.error('Failed plan maintenance', err)
            } finally {
                this.loading = false
            }
        },
        

        async editPlanMaintenance() {
            try {
                this.loading = true

                const response = await api.put(`/maintenance/plan`, this.editPlanMaintenanceModal)

                this.showEditPlanMaintenanceModal = false
                this.loadData()
            } catch(err) {
                console.error('Failed plan maintenance', err)
            } finally {
                this.loading = false
            }
        },

        async deletePlanMaintenance() {
            try {
                this.loading = true

                const response = await api.delete(`/maintenance/plan/${this.deleteMaintenanceId}`)
                
                this.showDeleteMaintenanceModal = false
                this.loadData()
            } catch(err) {
                console.error('Failed delete plan maintenance', err)
            } finally {
                this.loading = false
            }
        },

        async markPlanMaintenance(maintenanceId) {
            try {
                this.loading = true

                const response = await api.post('/maintenance/plan/mark', this.markPlanMaintenanceModal)

                this.showMarkPlanMaintenanceModal = false
                this.loadData()
            } catch (err) {
                console.error('Failed mark plan maintenance', err)
            } finally {
                this.loading = false
            }
        },


        

        

        

        openUpdateMileageModal() {
            this.showUpdateMileageModal = true
        },

        closeUpdateMileageModal() {
            this.showUpdateMileageModal = false
            this.updateMileageModal = {
                newMileage: null,
                motoId: null
            }
        },

        

        openAddMaintenanceModal() {
            this.showAddMaintenanceModal = true
        },

        closeAddMaintenanceModal() {
            this.showAddMaintenanceModal = false

            this.addMaintenanceModal = {
                motorcycleId: null,
                title: '',
                description: '',
                mileage: null,
                date: null
            }
        },

        openPlanMaintenanceModal() {
            this.showPlanMaintenanceModal = true
        },

        closePlanMaintenanceModal() {
            this.showPlanMaintenanceModal = false

            this.planMaintenanceModal = {
                motorcycleId: null,
                title: '',
                description: '',
                mileage: null,
            }
        },

        openEditPlanMaintenanceModal(maintenance) {
            this.showEditPlanMaintenanceModal = true

            this.editPlanMaintenanceModal = {
                maintenanceId: maintenance.id,
                motorcycleId: maintenance.moto_id,
                title: maintenance.title,
                description: maintenance.description,
                mileage: maintenance.planned_mileage,
            }
        },

        closeEditPlanMaintenanceModal() {
            this.showEditPlanMaintenanceModal = false

            this.editPlanMaintenanceModal = {
                maintenanceId: null,
                motorcycleId: null,
                title: '',
                description: '',
                mileage: null,
            }
        },

        openDeletePlanMaintenanceModal(maintenanceId) {
            this.showDeletePlanMaintenanceModal = true
            this.deleteMaintenanceId = maintenanceId
        },

        closeDeleteMaintenanceModal() {
            this.showDeletePlanMaintenanceModal = false

            this.maintenanceId = null
        },

        openMarkPlanMaintenanceModal(maintenanceId) {
            this.showMarkPlanMaintenanceModal = true
            this.markPlanMaintenanceModal.maintenanceId = maintenanceId
        },

        closeMarkPlanMaintenanceModal() {
            this.showMarkPlanMaintenanceModal = false
            this.markPlanMaintenanceModal = {
                maintenanceId: null,
                mileage: null,
                date: null,
                isRepeat: false,
                interval: null
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
                <button @click="openPlanMaintenanceModal()" :disabled="motorcycles.length === 0"><i class="fa fa-calendar"></i> Планировать обслуживание</button>
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
                                <p class="meta-text">Объем:</p> <p>{{ moto.volume }}</p>
                            </div>
                            <div class="meta-item">
                                <p class="meta-text">Год выпуска:</p> <p>{{ moto.years }}</p>
                            </div>
                            <div class="meta-item">
                                <p class="meta-text">Пробег:</p> <p>{{ moto.mileage ? moto.mileage : 0 }} км</p>
                            </div>
                            <div class="meta-item">
                                <p class="meta-text">Здоровье:</p> <p>{{ moto.health }}%</p>
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
                    <button @click="openPlanMaintenanceModal()" :disabled="motorcycles.length === 0" class="btn add-maintenance">
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

    <div v-if="showUpdateMileageModal" class="modal-wrapper">
        <div class="modal-container">
            <div class="modal-header">
                <p class="modal-title">Обновить пробег</p>
                <button @click="closeUpdateMileageModal()" class="close-btn btn"><i class="fa fa-close"></i></button>
            </div>
            <div class="modal-group">
                <label>
                    <i class="fa fa-motorcycle"></i> Мотоцикл
                    <select v-model="updateMileageModal.motoId">
                        <option value="">Выберите мотоцикл</option>
                        <option v-for="moto in motorcycles" :value="moto.id">{{ moto.name }}</option>
                    </select>
                </label>
                <label>
                    <i class="fa fa-tachometer"></i> Новый пробег
                    <input v-model="updateMileageModal.newMileage" type="number">
                </label>

                <div class="modal-actions">
                    <button @click="updateMileage()">Сохранить</button>
                    <button @click="closeUpdateMileageModal()" class="cancel-btn">Отменить</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Delete moto modal -->
    <DeleteMotoModal
        :is-open="showDeleteMotoModal"
        :motoId="deleteMotoId"
        @submit="handleMotoDeleted"
        @close="showDeleteMotoModal = false"
    />

    <!-- Add maintenance -->
    <div v-if="showAddMaintenanceModal" class="modal-wrapper">
        <div class="modal-container">
            <div class="modal-header">
                <p class="modal-title">Добавить обслуживание</p>
                <button @click="closeAddMaintenanceModal()" class="close-btn btn"><i class="fa fa-close"></i></button>
            </div>
            <div class="modal-group">
                <label>
                    <i class="fa fa-motorcycle"></i> Мотоцикл
                    <select v-model="addMaintenanceModal.motorcycleId">
                        <option value="">Выберите мотоцикл</option>
                        <option v-for="moto in motorcycles" :value="moto.id">{{ moto.name }}</option>
                    </select>
                </label>
                <label>
                    <i class="fa fa-font"></i> Название
                    <input v-model="addMaintenanceModal.title" type="text">
                </label>
                <label>
                    <i class="fa fa-align-justify"></i> Описание
                    <input v-model="addMaintenanceModal.description" type="text">
                </label>
                <label>
                    <i class="fa fa-tachometer"></i> Пробег
                    <input v-model="addMaintenanceModal.mileage" type="number" max="1000000" min="0">
                </label>
                <label>
                    <i class="fa fa-calendar"></i> Дата
                    <input v-model="addMaintenanceModal.date" type="date" :max="new Date().toISOString().split('T')[0]">
                </label>

                <div class="modal-actions">
                    <button @click="addMaintenance()">Добавить</button>
                    <button @click="closeAddMaintenanceModal()" class="cancel-btn">Отменить</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Plan maintenance -->
    <div v-if="showPlanMaintenanceModal" class="modal-wrapper">
        <div class="modal-container">
            <div class="modal-header">
                <p class="modal-title">Добавить обслуживание</p>
                <button @click="closePlanMaintenanceModal()" class="close-btn btn"><i class="fa fa-close"></i></button>
            </div>
            <div class="modal-group">
                <label>
                    <i class="fa fa-motorcycle"></i> Мотоцикл
                    <select v-model="planMaintenanceModal.motorcycleId">
                        <option value="">Выберите мотоцикл</option>
                        <option v-for="moto in motorcycles" :value="moto.id">{{ moto.name }}</option>
                    </select>
                </label>
                <label>
                    <i class="fa fa-font"></i> Название
                    <input v-model="planMaintenanceModal.title" type="text">
                </label>
                <label>
                    <i class="fa fa-align-justify"></i> Описание
                    <input v-model="planMaintenanceModal.description" type="text">
                </label>
                <label>
                    <i class="fa fa-tachometer"></i> Пробег
                    <input v-model="planMaintenanceModal.mileage" type="number" max="1000000" min="0">
                </label>

                <div class="modal-actions">
                    <button @click="planMaintenance()">Добавить</button>
                    <button @click="closePlanMaintenanceModal()" class="cancel-btn">Отменить</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Edit plan maintenance -->
    <div v-if="showEditPlanMaintenanceModal" class="modal-wrapper">
        <div class="modal-container">
            <div class="modal-header">
                <p class="modal-title">Редактировать запланированное обслуживание</p>
                <button @click="closeEditPlanMaintenanceModal()" class="close-btn btn"><i class="fa fa-close"></i></button>
            </div>
            <div class="modal-group">
                <label>
                    <i class="fa fa-motorcycle"></i> Мотоцикл
                    <select v-model="editPlanMaintenanceModal.motorcycleId">
                        <option v-for="moto in motorcycles" :value="moto.id">{{ moto.name }}</option>
                    </select>
                </label>
                <label>
                    <i class="fa fa-font"></i> Название
                    <input v-model="editPlanMaintenanceModal.title" type="text">
                </label>
                <label>
                    <i class="fa fa-align-justify"></i> Описание
                    <input v-model="editPlanMaintenanceModal.description" type="text">
                </label>
                <label>
                    <i class="fa fa-tachometer"></i> Пробег
                    <input v-model="editPlanMaintenanceModal.mileage" type="number" max="1000000" min="0">
                </label>

                <div class="modal-actions">
                    <button @click="editPlanMaintenance()">Добавить</button>
                    <button @click="closeEditPlanMaintenanceModal()" class="cancel-btn">Отменить</button>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Delete maintenance -->
    <div v-if="showDeletePlanMaintenanceModal" class="modal-wrapper">
        <div class="modal-container">
            <div class="modal-header">
                <p class="modal-title">Удалить обслуживание</p>
                <button @click="closeDeleteMaintenanceModal()" class="close-btn btn"><i class="fa fa-close"></i></button>
            </div>
            <div class="modal-group">
                <p class="modal-text">Вы уверены, что хотите удалить запланированное обслуживание? Отменить это действие невозможно.</p>
                <div class="modal-actions">
                    <button @click="deletePlanMaintenance()" class="btn-danger">Удалить</button>
                    <button @click="closeDeleteMaintenanceModal()" class="cancel-btn">Отменить</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Mark maintenance -->
    <div v-if="showMarkPlanMaintenanceModal" class="modal-wrapper">
        <div class="modal-container">
            <div class="modal-header">
                <p class="modal-title">Отметить обслуживание</p>
                <button @click="closeMarkPlanMaintenanceModal()" class="close-btn btn"><i class="fa fa-close"></i></button>
            </div>
            <div class="modal-group">
                <label>
                    Пробег выполнения
                    <input v-model="markPlanMaintenanceModal.mileage" type="number" max="1000000">
                </label>
                <label>
                    Дата
                    <input v-model="markPlanMaintenanceModal.date" type="date" :max="new Date().toISOString().split('T')">
                </label>
                <label class="checkbox-group">
                    Запланировать следующее обслуживание?
                    <input v-model="markPlanMaintenanceModal.isRepeat" type="checkbox">
                </label>
                <label v-if="markPlanMaintenanceModal.isRepeat">
                    Интервал
                    <input v-model="markPlanMaintenanceModal.interval" type="number" max="100000">
                </label>

                <div class="modal-actions">
                    <button @click="markPlanMaintenance()">Сохранить</button>
                    <button @click="closeMarkPlanMaintenanceModal()" class="cancel-btn">Отменить</button>
                </div>
            </div>
        </div>
    </div>
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