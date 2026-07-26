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
                                :class="dynamicTotalSpendsCount >= 0 ? 'positive' : 'negative'"
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

        <!-- === PENDING MAINTENANCE & EVENTS SECTION === -->
        <div class="grid-sections-wrapper">
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
                        <p class="empty-text">Запланируйте первое ТО на странице <a href="#">"Обслуживание"</a></p>
                    </div>
                </div>
                <button class="outline-btn">Все обслуживания <i class="fa fa-angle-right"></i></button>
            </section>
        </div>
    </div>
</template>

<script>
import api from '../api/api';
import { getUser } from '../api/auth';
import { removeTokens } from '../api/auth';
import MaintenanceCard from '../components/maintenance/MaintenanceCard.vue';
import MaintenanceCostChart from '../components/charts/MaintenanceCostChart.vue'
import MaintenanceCountChart from '../components/charts/MaintenanceCountChart.vue'

export default {
    components: {
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
            events: [],

            // === Statistic vars ===
            motorcycleCount: 0,
            planMaintenanceCount: 0,
            pendingMaintenanceCount: 0,
            maintenanceCount: 0,
            totalSpends: 0,

            // dynamic vars
            dynamicMotorcycleCount: 0,
            dynamicMaintenanceCount: 0,
            dynamicTotalSpendsCount: 0,

            // === Chart data ===
            costChartData: [],
            countChartData: [],

            // === Other vars ===
            welcomeDropdownActive: false,
        }
    },

    computed: {
        pendingMaintenances() {
            if (!this.maintenances) return []
            return this.maintenances
                .filter(m => m.status === 'overdue' || m.status === 'soon')
                .slice(0, 2)
        }
    },

    methods: {
        async loadData() {
            try {
                this.loading = true
                
                // Загружаем основные данные
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

                // Загружаем данные для графиков
                const chartsResponse = await api.get('/statistic/dashboard-charts')
                this.costChartData = chartsResponse.data.cost_chart || []
                this.countChartData = chartsResponse.data.count_chart || []

                const eventsResponse = await api.get('/event/')
                this.events = eventsResponse.data.filter(
                    e => e.status === 'planned' || e.status === 'active'
                ).slice(0, 3) // Ограничиваем тремя первыми
                
            } catch(err) {
                console.error('Failed to load dashboard data:', err)
            } finally {
                this.loading = false
            }
        },

        getMotorcycleName(motoId) {
            const moto = this.motorcycles.find(m => m.id === motoId)
            return moto ? moto.name : `Мотоцикл #${motoId}`
        },

        getMotorcycleMileage(motoId) {
            const moto = this.motorcycles.find(m => m.id === motoId)
            return moto ? moto.mileage : '0'
        },

        // === Event formatting methods ===
        formatEventDate(dateString) {
            if (!dateString) return 'Дата не указана'
            
            const date = new Date(dateString)
            const now = new Date()
            
            // Проверяем, что дата валидна
            if (isNaN(date.getTime())) return 'Неверная дата'
            
            // Форматируем дату: "15 января 2024"
            const months = ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 
                           'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
            
            const day = date.getDate()
            const month = months[date.getMonth()]
            const year = date.getFullYear()
            
            // Проверяем, сколько дней осталось
            const today = new Date()
            today.setHours(0, 0, 0, 0)
            const eventDate = new Date(date)
            eventDate.setHours(0, 0, 0, 0)
            
            const diffTime = eventDate.getTime() - today.getTime()
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
            
            // Если мероприятие уже прошло
            if (diffDays < 0) {
                return `${day} ${month} ${year}`
            }
            
            // Если сегодня
            if (diffDays === 0) {
                return `Сегодня, ${day} ${month}`
            }
            
            // Если завтра
            if (diffDays === 1) {
                return `Завтра, ${day} ${month}`
            }
            
            // Если в ближайшие 3 дня
            if (diffDays <= 3) {
                return `Через ${diffDays} дня, ${day} ${month}`
            }
            
            // Если в ближайшую неделю
            if (diffDays <= 7) {
                const weekDays = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 
                                 'Четверг', 'Пятница', 'Суббота']
                const weekDay = weekDays[date.getDay()]
                return `${weekDay}, ${day} ${month}`
            }
            
            // Иначе обычная дата
            return `${day} ${month} ${year}`
        },

        getStatusLabel(status) {
            const labels = {
                'planned': 'Запланировано',
                'active': 'Активно',
                'moderate': 'На модерации',
                'decline': 'Отклонено'
            }
            return labels[status] || status
        },

        getStatusClass(status) {
            const classes = {
                'planned': 'status-planned',
                'active': 'status-active',
                'moderate': 'status-moderate',
                'decline': 'status-decline'
            }
            return classes[status] || ''
        },

        getEventIcon(status) {
            const icons = {
                'planned': 'fa-calendar-plus',
                'active': 'fa-calendar-check',
                'moderate': 'fa-clock',
                'decline': 'fa-calendar-times'
            }
            return icons[status] || 'fa-calendar'
        },

        getEventIconClass(status) {
            const classes = {
                'planned': 'blue-bg',
                'active': 'green-bg',
                'moderate': 'yellow-bg',
                'decline': 'red-bg'
            }
            return classes[status] || 'blue-bg'
        },

        truncateDescription(description) {
            if (!description) return ''
            if (description.length > 60) {
                return description.substring(0, 60) + '...'
            }
            return description
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

@media (max-width: 1220px) {
    .grid-sections-wrapper {
        grid-template-columns: repeat(1, 1fr);
        grid-template-rows: repeat(4, 1fr);
    }

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