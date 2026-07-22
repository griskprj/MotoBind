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
        EditMotoModal,
        DeleteMotoModal,
    },

    data() {
        return {
            maintenances_count: 0,
            plan_maintenances_count: 0,
            total_maintenances: 0,
            month_maintenances: 0,
            all_cost: 0,
            total_cost: 0,
            max_cost: 0,
            average_cost: 0,
            motorcycles: [],
            selectedMoto:null,
            motoData: null,
            nodes: [],
            plannedMaintenances: [],
            selectedMaintenance: null,
            selectedDeleteMaintenanceId: null,
            markPlanMaintenanceId: null,
            money_chart_data: [],
            freq_chart_data: [],
            loading: false,

            showUpdateMileageModal: false,
            showEditMotoModal: false,
            showDeleteMotoModal: false,
            showAddMaintenanceModal: false,
            showPlanMaintenanceModal: false,
            showEditPlanMaintenanceModal: false,
            showMarkPlanMaintenanceModal: false,
            showDeletePlanMaintenanceModal: false,
            activeNodeIndex: 0,
            showNodeMaintenances: true,
            welcomeDropdownActive: false,
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
            return this.activeNode ? [this.activeNode] : [];
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
                this.nodes = response.data.nodes
                this.plannedMaintenances = response.data.planned_maintenances
                this.total_cost = response.data.total_cost
                this.max_cost = response.data.max_cost
                this.average_cost = response.data.average_cost
                this.money_chart_data = response.data.money_chart_data
                this.total_maintenances = response.data.total_maintenances
                this.month_maintenances = response.data.month_maintenances
                this.freq_chart_data = response.data.freq_chart_data
                this.activeNodeIndex = 0
                this.showNodeMaintenances = true
            } catch (err) {
                console.error(err)
            } finally {
                this.loading = false
            }
        },
        async updateMotoMileage(formData) {
            try {
                this.loading = true
                const response = await api.patch(`/motorcycle/${formData.id}`, { newMileage: formData.newMileage })
                const updatedMoto = response.data
                if (this.motoData && this.motoData.id === formData.id) {
                    this.motoData.mileage = updatedMoto.mileage
                }
                const motoIndex = this.motorcycles.findIndex(m => m.id === formData.id)
                if (motoIndex !== -1) {
                    this.motorcycles[motoIndex].mileage = updatedMoto.mileage
                }
                this.showUpdateMileageModal = false
                alert(`Пробег обновлен до ${updatedMoto.mileage} км`)
            } catch(err) {
                console.error('Failed update moto mileage', err)
            } finally {
                this.loading = false
            }
        },
        async updateMoto(formData) {
            try {
                this.loading = true
                const { data } = await api.put(`/motorcycle/${formData.id}`, formData)
                const index = this.motorcycles.findIndex(m => m.id === formData.id)
                if (index !== -1) this.motorcycles[index] = data
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
        async addMaintenance(formData) {
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
            try {
                this.loading = true
                await api.post('/maintenance/plan', formData)
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
            try {
                this.loading = true
                const { data } = await api.put(`/maintenance/plan`, formData)
                const maintenanceIndex = this.plannedMaintenances.findIndex(m => m.id === formData.maintenanceId)
                if (maintenanceIndex !== -1) this.plannedMaintenances[maintenanceIndex] = data
                this.closeEditPlanMaintenanceModal()
                this.loadData()
                alert(`Обслуживание обновлено`)
            } catch (err) {
                console.error(`Failed update plan maintenance: ${err}`)
            } finally {
                this.loading = false
            }
        },
        async deletePlanMaintenance(maintenenceId) {
            try {
                this.loading = true
                await api.delete(`/maintenance/plan/${maintenenceId}`)
                const maintnenanceIndex = this.plannedMaintenances.findIndex(m => m.id === maintenenceId)
                if (maintnenanceIndex !== -1) this.plannedMaintenances.splice(maintnenanceIndex, 1)
                this.showDeletePlanMaintenanceModal = false
                this.selectedDeleteMaintenanceId = null
                this.loadData()
                alert("Обслуживание удалено!")
            } catch (err) {
                console.error(`Failed delete plan maintenance: ${err}`)
            } finally {
                this.loading = false
            }
        },
        async markPlanMaintenance(formData) {
            try {
                this.loading = true
                await api.post(`/maintenance/plan/mark`, formData)
                this.loadData()
                this.showMarkPlanMaintenanceModal = false
                alert("Обслуживание отмечено выполненным")
            } catch (err) {
                console.error(`Failed mark plan maintenance: ${err}`)
            } finally {
                this.loading = false
            }
        },
        removeMotoData() {
            this.motoData = null
            this.nodes = []
            this.activeNodeIndex = 0
        },
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
        openUpdateMileageModal() { this.showUpdateMileageModal = true },
        openEditMotoModal() { this.showEditMotoModal = true },
        openDeleteMotoModal() { this.showDeleteMotoModal = true },
        openAddMaintenanceModal() { this.showAddMaintenanceModal = true },
        openPlanMaintenanceModal() { this.showPlanMaintenanceModal = true },
        openEditPlanMaintenanceModal(maintenance) {
            this.selectedMaintenance = maintenance
            this.showEditPlanMaintenanceModal = true
        },
        closeEditPlanMaintenanceModal() {
            this.showEditPlanMaintenanceModal = false
            this.selectedMaintenance = null
        },
        openDeletePlanMaintenanceModal(maintenanceId) {
            this.selectedDeleteMaintenanceId = maintenanceId
            this.showDeletePlanMaintenanceModal = true
        },
        closeDeletePlanMaintenanceModal() {
            this.showDeletePlanMaintenanceModal = false
            this.selectedDeleteMaintenanceId = null
        },
        openMarkPlanMaintenance(maintenanceId) {
            this.markPlanMaintenanceId = maintenanceId
            this.showMarkPlanMaintenanceModal = true
        },
        closeMarkPlanMaintenance() {
            this.markPlanMaintenanceId = null
            this.showMarkPlanMaintenanceModal = false
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

<template>
    <div class="garage-container">
        <!-- === HEADER === -->
        <header class="page-header">
            <div class="header-left">
                <h2>Гараж</h2>
                <div class="header-tabs">
                    <button class="tab-btn active">Мои мотоциклы</button>
                    <button class="tab-btn outline">Добавить мотоцикл</button>
                </div>
            </div>

            <div class="header-right">
                <i class="fa fa-bell notification-icon"></i>
                <div class="profile-wrapper">
                    <img src="/BaseAvatar.jpg" alt="avatar" class="profile-img">
                    <button class="dropdown-trigger" @click="welcomeDropdownActive = !welcomeDropdownActive">
                        <i class="fa" :class="welcomeDropdownActive ? 'fa-angle-up' : 'fa-angle-down'"></i>
                    </button>
                    <div v-if="welcomeDropdownActive" class="dropdown-list">
                        <ul>
                            <li><button class="dropdown-item">Профиль</button></li>
                            <li><button class="dropdown-item">Настройки</button></li>
                            <li><button @click="logout" class="dropdown-item">Выйти</button></li>
                        </ul>
                    </div>
                </div>
            </div>
        </header>

        <!-- === MOTORCYCLE SELECTOR (SCROLLABLE) === -->
        <section class="moto-selector-wrapper">
            <div class="moto-scroll-container">
                <div class="moto-card active">
                    <div class="moto-card-icon"><i class="fa fa-motorcycle"></i></div>
                    <div class="moto-card-info">
                        <div class="moto-name">BMW s1000rr</div>
                        <div class="moto-meta">2020 • 7 500 км</div>
                    </div>
                    <div class="moto-active-badge"><i class="fa fa-check"></i></div>
                </div>
                
                <div class="moto-card">
                    <div class="moto-card-icon"><i class="fa fa-motorcycle"></i></div>
                    <div class="moto-card-info">
                        <div class="moto-name">Yamaha R6</div>
                        <div class="moto-meta">2018 • 14 200 км</div>
                    </div>
                </div>

                <div class="moto-card">
                    <div class="moto-card-icon"><i class="fa fa-motorcycle"></i></div>
                    <div class="moto-card-info">
                        <div class="moto-name">Kawasaki ZX-6R</div>
                        <div class="moto-meta">2019 • 8 100 км</div>
                    </div>
                </div>

                <div class="moto-card add-card">
                    <i class="fa fa-plus"></i>
                    <span>Добавить</span>
                </div>
            </div>
        </section>

        <!-- === MAIN GRID (2 Columns) === -->
        <div class="main-grid">
            <!-- LEFT COLUMN: Moto Info -->
            <aside class="moto-details-col">
                <div class="big-moto-card">
                    <div class="big-card-header">
                        <span class="big-title">BMW S1000RR</span>
                        <button class="icon-btn"><i class="fa fa-pen"></i></button>
                    </div>
                    <div class="big-card-img">
                        <img src="../../public/bmw1000.webp" alt="Фото">
                    </div>
                    <div class="big-card-grid">
                        <div class="spec-item"><span class="label">Год выпуска</span><span class="value">2020</span></div>
                        <div class="spec-item"><span class="label">Двигатель</span><span class="value">999 см³</span></div>
                        <div class="spec-item"><span class="label">Пробег</span><span class="value">20 700 км</span></div>
                        <div class="spec-item"><span class="label">Цвет</span><div class="color-dot" style="background:#fff990;"></div></div>
                        <div class="spec-item full-width"><span class="label">VIN</span><span class="value">WB10D01033LZR12345</span></div>
                        <div class="spec-item full-width"><span class="label">Гос. номер</span><span class="value">0123AB23</span></div>
                    </div>
                    <div class="notes-block">
                        <div class="notes-header">
                            <span>Заметки</span>
                            <button class="icon-btn"><i class="fa fa-pen"></i></button>
                        </div>
                        <p class="notes-text">Мотоцикл пригнан из Германии в 2023 году. Отличное состояние</p>
                    </div>
                </div>
            </aside>

            <!-- RIGHT COLUMN: Stats & Table -->
            <main class="stats-col">
                <!-- 4 Stats Cards -->
                <div class="stats-grid-4">
                    <div class="stat-box">
                        <div class="stat-head"><i class="fa fa-tachometer"></i> Пробег</div>
                        <div class="stat-val">7 500 км</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-head"><i class="fa fa-wrench"></i> Обслуживаний</div>
                        <div class="stat-val">12</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-head"><i class="fa fa-calendar"></i> До следующего ТО</div>
                        <div class="stat-val">1 250 км</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-head"><i class="fa fa-ruble"></i> Общие расходы</div>
                        <div class="stat-val">86 320 ₽</div>
                    </div>
                </div>

                <!-- Table -->
                <div class="maintenance-table-wrapper">
                    <div class="table-header">
                        <span class="th">Дата</span>
                        <span class="th">Обслуживание</span>
                        <span class="th">Пробег</span>
                        <span class="th">Стоимость</span>
                        <span class="th">Статус</span>
                        <span class="th"></span>
                    </div>
                    <div class="table-body">
                        <!-- Row 1 -->
                        <div class="tr">
                            <div class="td date-cell">
                                <div class="icon-square purple"><i class="fa fa-wrench"></i></div>
                                <span>12 мая 2025</span>
                            </div>
                            <div class="td service-cell">
                                <div class="s-title">Замена масла</div>
                                <div class="s-desc">Масло Motul 7100, масляный фильтр</div>
                            </div>
                            <div class="td">7 500 км</div>
                            <div class="td">4 250 ₽</div>
                            <div class="td"><span class="badge-green">Выполнено</span></div>
                            <div class="td action-cell"><i class="fa fa-chevron-right"></i></div>
                        </div>
                        <!-- Row 2 -->
                        <div class="tr">
                            <div class="td date-cell">
                                <div class="icon-square green"><i class="fa fa-trash"></i></div>
                                <span>08 апр 2025</span>
                            </div>
                            <div class="td service-cell">
                                <div class="s-title">Замена воздушного фильтра</div>
                                <div class="s-desc">Воздушный фильтр K&N</div>
                            </div>
                            <div class="td">6 850 км</div>
                            <div class="td">2 350 ₽</div>
                            <div class="td"><span class="badge-green">Выполнено</span></div>
                            <div class="td action-cell"><i class="fa fa-chevron-right"></i></div>
                        </div>
                        <!-- Row 3 -->
                        <div class="tr">
                            <div class="td date-cell">
                                <div class="icon-square blue"><i class="fa fa-shield-alt"></i></div>
                                <span>15 мар 2025</span>
                            </div>
                            <div class="td service-cell">
                                <div class="s-title">Замена передних колодок</div>
                                <div class="s-desc">Тормозные колодки Brembo</div>
                            </div>
                            <div class="td">6 300 км</div>
                            <div class="td">6 800 ₽</div>
                            <div class="td"><span class="badge-green">Выполнено</span></div>
                            <div class="td action-cell"><i class="fa fa-chevron-right"></i></div>
                        </div>
                    </div>
                    <div class="table-footer">
                        <button class="outline-btn" style="width: 100%;">Все записи <i class="fa fa-chevron-right"></i></button>
                    </div>
                </div>
            </main>
        </div>
    </div>

    <!-- Modals (оставляем без изменений) -->
    <EditMotoModal :isOpen="showEditMotoModal" :motorcycle="motoData" @submit="updateMoto" @close="showEditMotoModal=false" />
    <DeleteMotoModal :isOpen="showDeleteMotoModal" :motoId="selectedMoto" @submit="deleteMoto" @close="showDeleteMotoModal=false" />
</template>

<style scoped>
.garage-container {
    padding: 24px 32px;
    background-color: #0f0f1a;
    min-height: 100vh;
    color: #fff;
    font-family: sans-serif;
}

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
    margin: 0 0 12px 0;
    font-size: 24px;
}
.header-tabs {
    display: flex;
    gap: 8px;
}
.tab-btn {
    padding: 8px 20px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    background: transparent;
    color: #8b8b9e;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: 0.2s;
}
.tab-btn.active {
    background: rgba(124, 58, 237, 0.2);
    border-color: #7c3aed;
    color: #a78bfa;
}
.tab-btn.outline:hover {
    background: rgba(124, 58, 237, 0.1);
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
}
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
}
.dropdown-trigger {
    background: transparent;
    border: none;
    color: #8b8b9e;
    cursor: pointer;
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
}
.dropdown-item:hover {
    background: rgba(255,255,255,0.05);
}

/* ===== MOTORCYCLE SELECTOR ===== */
.moto-selector-wrapper {
    margin-bottom: 24px;
}
.moto-scroll-container {
    display: flex;
    gap: 12px;
    overflow-x: auto;
    padding: 4px 0 8px 0;
    scrollbar-width: thin;
    scrollbar-color: #2d2d3d transparent;
}
.moto-scroll-container::-webkit-scrollbar {
    height: 4px;
}
.moto-scroll-container::-webkit-scrollbar-thumb {
    background: #2d2d3d;
    border-radius: 4px;
}
.moto-card {
    flex: 0 0 220px;
    background: #181824;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 14px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    transition: 0.2s;
}
.moto-card:hover {
    background: #202036;
}
.moto-card.active {
    border-color: #7c3aed;
    background: rgba(124, 58, 237, 0.1);
}
.moto-card.add-card {
    border: 2px dashed rgba(255,255,255,0.1);
    background: transparent;
    justify-content: center;
    color: #7c3aed;
}
.moto-card-icon {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    background: rgba(124, 58, 237, 0.15);
    color: #a78bfa;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.moto-card-info {
    flex: 1;
    overflow: hidden;
}
.moto-name {
    font-size: 14px;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.moto-meta {
    font-size: 12px;
    color: #8b8b9e;
}
.moto-active-badge {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #7c3aed;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    color: #fff;
}

/* ===== MAIN GRID (Adaptive) ===== */
.main-grid {
    display: grid;
    grid-template-columns: 320px 1fr;
    gap: 24px;
    align-items: start;
}

/* LEFT COLUMN */
.big-moto-card {
    background: #181824;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 16px;
    padding: 20px;
}
.big-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}
.big-title {
    font-size: 20px;
    font-weight: 600;
}
.icon-btn {
    background: rgba(255,255,255,0.05);
    border: none;
    color: #8b8b9e;
    width: 32px;
    height: 32px;
    border-radius: 8px;
    cursor: pointer;
    transition: 0.2s;
}
.icon-btn:hover {
    background: rgba(255,255,255,0.1);
    color: #fff;
}
.big-card-img img {
    width: 100%;
    height: auto;
    border-radius: 12px;
    margin-bottom: 16px;
    object-fit: cover;
}
.big-card-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px 16px;
    margin-bottom: 16px;
}
.spec-item {
    display: flex;
    flex-direction: column;
    gap: 2px;
}
.spec-item.full-width {
    grid-column: 1 / -1;
}
.spec-item .label {
    font-size: 12px;
    color: #8b8b9e;
}
.spec-item .value {
    font-size: 14px;
    font-weight: 500;
}
.color-dot {
    width: 40px;
    height: 14px;
    border-radius: 4px;
}
.notes-block {
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    padding: 14px;
}
.notes-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 500;
    font-size: 14px;
    margin-bottom: 6px;
}
.notes-text {
    font-size: 13px;
    color: #8b8b9e;
    margin: 0;
}

/* RIGHT COLUMN */
.stats-grid-4 {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 20px;
}
.stat-box {
    background: #181824;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 16px;
}
.stat-head {
    font-size: 13px;
    color: #8b8b9e;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
}
.stat-head i {
    font-size: 16px;
    color: #a78bfa;
}
.stat-val {
    font-size: 22px;
    font-weight: 700;
}

/* ===== TABLE (Fully Responsive) ===== */
.maintenance-table-wrapper {
    background: #181824;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 16px;
    overflow: hidden;
}
.table-header {
    display: grid;
    grid-template-columns: 160px 1fr 90px 100px 120px 40px;
    padding: 12px 16px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 13px;
    color: #8b8b9e;
    font-weight: 500;
}
.table-body {
    display: flex;
    flex-direction: column;
}
.tr {
    display: grid;
    grid-template-columns: 160px 1fr 90px 100px 120px 40px;
    padding: 14px 16px;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.03);
    transition: background 0.2s;
    cursor: pointer;
}
.tr:hover {
    background: rgba(255,255,255,0.02);
}
.td {
    font-size: 14px;
}
.date-cell {
    display: flex;
    align-items: center;
    gap: 10px;
}
.icon-square {
    width: 30px;
    height: 30px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
}
.icon-square.purple { background: rgba(124, 58, 237, 0.15); color: #a78bfa; }
.icon-square.green { background: rgba(34, 197, 94, 0.15); color: #4ade80; }
.icon-square.blue { background: rgba(59, 130, 246, 0.15); color: #93c5fd; }
.service-cell {
    display: flex;
    flex-direction: column;
}
.s-title { font-weight: 500; }
.s-desc { font-size: 13px; color: #8b8b9e; }
.badge-green {
    display: inline-block;
    padding: 3px 12px;
    background: rgba(34, 197, 94, 0.15);
    color: #4ade80;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
}
.action-cell {
    display: flex;
    justify-content: flex-end;
    color: #4b4b5e;
    transition: color 0.2s;
}
.tr:hover .action-cell { color: #a78bfa; }
.table-footer {
    padding: 16px;
    text-align: center;
}
.show-more {
    background: transparent;
    border: none;
    color: #7c3aed;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}
.show-more:hover { opacity: 0.8; }

/* ===== MEDIA QUERIES ===== */

/* Планшеты и небольшие ноутбуки (до 1220px) - превращаем в 1 колонку */
@media (max-width: 1220px) {
    .main-grid {
        grid-template-columns: 1fr;
    }
    .moto-details-col {
        max-width: 100%;
    }
    .big-moto-card {
        display: grid;
        grid-template-columns: 240px 1fr;
        gap: 20px;
    }
    .big-card-img {
        grid-row: span 2;
    }
    .big-card-img img {
        height: 100%;
        object-fit: cover;
        margin-bottom: 0;
    }
    .big-card-grid {
        margin-bottom: 0;
    }
    .notes-block {
        grid-column: 1 / -1;
    }
    .stats-grid-4 {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* Телефоны (до 820px) */
@media (max-width: 820px) {
    .header-right {
        display: none;
    }

    .garage-container { padding: 16px; }
    .page-header {
        flex-direction: column;
        align-items: stretch;
        gap: 12px;
    }
    .header-left h2 { margin-bottom: 8px; }
    .header-tabs { flex-wrap: wrap; }
    .header-right {
        justify-content: flex-end;
    }
    .moto-card {
        flex: 0 0 160px;
        padding: 10px 12px;
    }
    .moto-card-icon { display: none; }
    .moto-name { font-size: 13px; }
    
    .big-moto-card {
        grid-template-columns: 1fr;
    }
    .big-card-img {
        grid-row: auto;
    }
    .big-card-img img {
        height: 160px;
        width: 100%;
    }
    .stats-grid-4 {
        grid-template-columns: 1fr 1fr;
    }
    
    /* Мобильная таблица (превращается в карточки) */
    .table-header { display: none; }
    .tr {
        grid-template-columns: 1fr;
        gap: 4px;
        padding: 16px;
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px;
        margin-bottom: 8px;
        background: #0f0f1a;
        position: relative;
    }
    .tr:hover { background: #0f0f1a; }
    .date-cell {
        order: 1;
        margin-bottom: 4px;
    }
    .service-cell {
        order: 2;
        padding-left: 40px;
    }
    .td:not(.date-cell):not(.service-cell):not(.action-cell) {
        order: 3;
        padding-left: 40px;
        font-size: 13px;
    }
    .td:not(.date-cell):not(.service-cell):not(.action-cell)::before {
        content: attr(data-label);
        color: #8b8b9e;
        font-weight: 400;
        margin-right: 4px;
    }
    .td.action-cell {
        order: 4;
        position: absolute;
        right: 16px;
        top: 20px;
    }
    .td.action-cell i { font-size: 16px; }
}

/* Очень маленькие экраны (до 480px) */
@media (max-width: 480px) {
    .stats-grid-4 { grid-template-columns: 1fr; }
    .moto-scroll-container { gap: 8px; }
    .moto-card { flex: 0 0 140px; }
}
</style>