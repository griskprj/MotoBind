<script>
import api from '../api/api';
import { getUser } from '../api/auth';
import { removeTokens } from '../api/auth';

import AddMotoModal from '../components/modals/moto/AddMotoModal.vue';
import DeleteMotoModal from '../components/modals/moto/DeleteMotoModal.vue';
import EditMotoModal from '../components/modals/moto/EditMotoModal.vue';
import UpdateMileageModal from '../components/modals/moto/UpdateMileageModal.vue';

import AddMaintenanceModal from '../components/modals/maintenance/AddMaintenanceModal.vue';
import AddPlanMaintenanceModal from '../components/modals/maintenance/AddPlanMaintenanceModal.vue';
import EditPlanMaintenanceModal from '../components/modals/maintenance/EditPlanMaintenanceModal.vue';
import DeletePlanMaintenanceModal from '../components/modals/maintenance/DeletePlanMaintenanceModal.vue';
import MarkPlanMaintenanceModal from '../components/modals/maintenance/MarkPlanMaintenanceModal.vue';
import MotoCard from '../components/moto/MotoCard.vue';
import MaintenanceCard from '../components/maintenance/MaintenanceCard.vue';

import MaintenanceCostChart from '../components/charts/MaintenanceCostChart.vue'
import MaintenanceCountChart from '../components/charts/MaintenanceCountChart.vue'


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
        MarkPlanMaintenanceModal,

        MotoCard,
        MaintenanceCard,

        MaintenanceCostChart,
        MaintenanceCountChart,
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

            // === Other vars ===
            // bool
            welcomeDropdownActive: false,
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

        async logout() {
            try {
                await api.post('/auth/logout');
            } catch(err) {
                console.error('Logout failed:', err);
            } finally {
                removeTokens();
                this.$router.push('/login');
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
        <section>
            <div class="welcome-wrapper">
                <h2>Добро пожаловать, {{ user?.username }} 👋</h2>

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

        <!-- === STATISTICS SECTION === -->
        <section>
            <div class="statistic-cards-grid">
                <div class="stat-card">
                    <div class="card-icon">
                        <i class="fa fa-motorcycle"></i>
                    </div>
                    <div class="card-body">
                        <p class="card-title">Мотоциклов в гараже</p>
                        <p class="stat-value">2</p>
                        <div class="stat-meta-wrapper">
                            <p class="stat-meta-value positive">+1</p> 
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
                        <p class="stat-value">3</p>
                        <div class="stat-meta-wrapper">
                            <p class="stat-meta maintenance">2 скоро нужно выполнить</p>
                        </div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="card-icon">
                        <i class="fa fa-wrench"></i>
                    </div>
                    <div class="card-body">
                        <p class="card-title">Обслуживаний</p>
                        <p class="stat-value">12</p>
                        <div class="stat-meta-wrapper">
                            <p class="stat-meta-value positive">+3</p> <p class="stat-meta"> за последний месяц</p>
                        </div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="card-icon">
                        <i class="fa fa-ruble"></i>
                    </div>
                    <div class="card-body">
                        <p class="card-title">Общие расходы</p>
                        <p class="stat-value">142570 ₽</p>
                        <div class="stat-meta-wrapper">
                            <p class="stat-meta-value negative">+12%</p> <p class="stat-meta"> за последний месяц</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <div class="grid-sections-wrapper">
            <!-- === MAINTENANCE COST CHART === -->
            <MaintenanceCostChart />

            <!-- === MAINTENANCE COUNT CHART === -->
            <MaintenanceCountChart />

            <!-- === PENDING MAINTENANCE SECTION === -->
            <section class="pending-maintenance-section">
                <h3>Ближайшие обслуживания</h3>
                <div class="cards-wrapper">
                    <MaintenanceCard
                        :maintenance="
                            {
                                'id': 1,
                                'title': 'Замена масла',
                                'moto_name': 'Bajaj Pulsar NS 125',
                                'planned_mileage': '22100',
                            }
                        "
                    />
                    <MaintenanceCard
                        :maintenance="
                            {
                                'id': 2,
                                'title': 'Замена цепи и звезд',
                                'moto_name': 'BMW s1000rr',
                                'planned_mileage': '20100',
                            }
                        "
                    />
                </div>
                <button class="outline-btn">Все обслуживания <i class="fa fa-angle-right"></i></button>
            </section>

            <!-- === UPCOMING EVENTS SECTION === -->
            <section class="pending-event-section">
                <h3>Мероприятия</h3>

                <div class="cards-wrapper">
                    <div class="event-card">
                        <div class="event-icon-wrapper blue-bg">
                            <i class="fa fa-flag-checkered"></i>
                        </div>
                        
                        <div class="event-info">
                            <p class="event-title">Открытие MotoBind</p>
                            <p class="event-desc">Мотофестиваль и презентация сезона</p>
                        </div>

                        <div class="event-meta">
                            <span class="event-date">26.08.2026</span>
                            <span class="event-status future">Скоро</span>
                        </div>

                        <div class="card-action">
                            <i class="fa fa-chevron-right"></i>
                        </div>
                    </div>

                    <div class="event-card">
                        <div class="event-icon-wrapper green-bg">
                            <i class="fa fa-road"></i>
                        </div>
                        
                        <div class="event-info">
                            <p class="event-title">Мотопробег "Золотое кольцо"</p>
                            <p class="event-desc">Сбор в 09:00 у парка Горького</p>
                        </div>

                        <div class="event-meta">
                            <span class="event-date">15.09.2026</span>
                            <span class="event-status future">Скоро</span>
                        </div>

                        <div class="card-action">
                            <i class="fa fa-chevron-right"></i>
                        </div>
                    </div>

                    <div class="event-card past-event">
                        <div class="event-icon-wrapper purple-bg">
                            <i class="fa fa-users"></i>
                        </div>
                        
                        <div class="event-info">
                            <p class="event-title">Открытая тренировка</p>
                            <p class="event-desc">Трек "Маяк", 15 участников</p>
                        </div>

                        <div class="event-meta">
                            <span class="event-date">15.07.2026</span>
                            <span class="event-status past">Прошло</span>
                        </div>

                        <div class="card-action">
                            <i class="fa fa-chevron-right"></i>
                        </div>
                    </div>
                </div>
                <button class="outline-btn">Все мероприятия <i class="fa fa-angle-right"></i></button>
            </section>  
        </div>
        
    </div>
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

@media (max-width: 728px) {
    .statistic-cards-grid {
        grid-template-columns: repeat(1, 1fr);
        grid-template-rows: repeat(4, 1fr);
    }

    .stat-card {
        align-items: center;
        justify-content: space-evenly;
    }
}

/*  === MOTORCYCLE SECTION ===  */
.motorcycle-section {
    background-color: var(--bg-primary);
    border: 2px solid var(--border-color);
    border-radius: 25px;

    margin-bottom: 32px;
    padding: 28px;
}

@media (max-width: 728px) {
    .motorcycle-section {
        padding: 16px;
    }
}


/* === CHART SECTION === */
.grid-sections-wrapper {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: 12px;
}

@media (max-width: 728px) {
    .grid-sections-wrapper {
        grid-template-columns: repeat(1, 1fr);
        grid-template-rows: repeat(4, 1fr);
    }
}

/*  === PENDING MAINTENANCE SECTION ===  */
.pending-maintenance-section {
    background-color: var(--bg-secondary);
    padding: 12px;
    border-radius: 20px;

    display: flex;
    flex-direction: column;
    justify-content: space-around;
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


/* === UPCOMING EVENTS SECTION === */
.pending-event-section h3 {
    margin-bottom: 16px;
    font-size: 18px;
}

.pending-event-section {
    background-color: var(--bg-secondary);
    padding: 16px;
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.section-header h3 {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
}

.header-link {
    color: #7c3aed;
    font-size: 13px;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 4px;
    transition: opacity 0.2s;
}

.header-link:hover {
    opacity: 0.8;
}

.cards-wrapper {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

/* Сама карточка мероприятия */
.event-card {
    display: flex;
    align-items: center;
    padding: 12px 16px;
    background-color: var(--bg-card);
    border-radius: 12px;
    gap: 16px;
    transition: background 0.2s ease, opacity 0.2s;
    cursor: pointer;
    border: 1px solid transparent;
}

.event-card:hover {
    background-color: #202036;
}

/* Если мероприятие прошло - делаем чуть тусклее */
.event-card.past-event {
    opacity: 0.6;
}
.event-card.past-event:hover {
    opacity: 1;
}

/* Квадрат с иконкой */
.event-icon-wrapper {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}

/* Цвета фона для иконок */
.purple-bg { background: rgba(124, 58, 237, 0.2); color: #a78bfa; }
.blue-bg { background: rgba(59, 130, 246, 0.2); color: #93c5fd; }
.green-bg { background: rgba(34, 197, 94, 0.2); color: #4ade80; }
.yellow-bg { background: rgba(234, 179, 8, 0.2); color: #fde047; }

/* Текстовая часть */
.event-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.event-title {
    font-size: 14px;
    font-weight: 500;
    color: #ffffff;
    margin: 0;
}

.event-desc {
    font-size: 13px;
    color: #8b8b9e;
    margin: 0;
}

/* Дата и статус справа */
.event-meta {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 4px;
}

.event-date {
    font-size: 12px;
    color: #8b8b9e;
}

.event-status {
    font-size: 11px;
    font-weight: 600;
    padding: 2px 10px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.event-status.future {
    background: rgba(34, 197, 94, 0.15);
    color: #4ade80;
}

.event-status.past {
    background: rgba(107, 114, 128, 0.2);
    color: #9ca3af;
}

/* Стрелка перехода */
.card-action {
    color: #4b4b5e;
    font-size: 14px;
    transition: color 0.2s ease;
    margin-left: 4px;
}

.event-card:hover .card-action {
    color: #a78bfa;
}

/* Адаптив для маленьких экранов */
@media (max-width: 600px) {
    .section-header {
        flex-direction: row;
        flex-wrap: wrap;
    }
    
    .event-card {
        flex-wrap: wrap;
    }
    
    .event-meta {
        flex-direction: row;
        align-items: center;
        gap: 12px;
        width: 100%;
        padding-left: 56px; /* Отступ под иконку, чтобы выровнять */
        margin-top: 4px;
    }
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