<template>
    <div class="container">
        <!-- === HEADER === -->
        <Header
            title="Панель администратора"
            subtitle="Обзор ключевых показателей и активности сайта"
        />

        <!-- === STATISTIC === -->
        <section>
            <div class="stat-cards">
                <div class="stat-card">
                    <div class="card-icon">
                        <i class="fa fa-users"></i>
                    </div>
                    <div class="card-body">
                        <p class="card-title">Пользователи</p>
                        <p class="card-value">{{ usersCount }}</p>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="card-icon">
                        <i class="fa fa-motorcycle"></i>
                    </div>
                    <div class="card-body">
                        <p class="card-title">Мотоциклы</p>
                        <p class="card-value">{{ motosCount }}</p>
                    </div>
                </div>

                <div class="stat-card third">
                    <div class="card-icon">
                        <i class="fa fa-file"></i>
                    </div>
                    <div class="card-body">
                        <p class="card-title">Мануалы</p>
                        <p class="card-value">{{ manualsCount }}</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- === MAIN SECTION === -->
        <section class="main-section-wrapper">
            <div class="chart-wrapper">
                <h3>Регистрация пользователей</h3>
                <UserRegistrationsChart
                    :chart-data="registrationsChartData"
                />
            </div>
            <div class="last-reg-wrapper">
                <h3>Последние регистрации</h3>
                <div class="last-reg-cards">
                    <div 
                        class="last-reg-card"
                        v-for="user in lastRegUserData"    
                    >
                        <div class="user-info">
                            <img class="user-img" src="/BaseAvatar.jpg" alt="">
                            <div class="reg-card-body">
                                <p class="user-name">{{ user.username }}</p>
                                <p class="user-time">26.08.2008, 12:45</p>
                            </div>
                        </div>
                        <div class="user-status" :class="user.role">
                            <p class="user-role">{{getUserRole( user.role) }}</p>
                        </div>
                    </div>
                </div>
                <router-link class="btn outline-btn" style="text-decoration: none; width: 100%;" to="/admin/users">
                    Смотреть всех пользователей <i class="fa fa-angle-right"></i>
                </router-link>
            </div>
        </section>

        <!-- === FAST ACTIONS === -->
        <section class="fast-section-wrapper">
            <h3>Быстрые действия</h3>
            <div class="fast-action-card-wrapper">
                <div @click="showAddUserModal = true" class="fast-action-card">
                    <div class="action-card-icon">
                        <i class="fa fa-user-plus"></i>
                    </div>
                    <p class="fast-action-text">
                        Добавить пользователя
                    </p>
                </div>
    
                <router-link class="fast-action-card link" to="/manual-creator">
                    <div class="action-card-icon">
                        <i class="fa fa-tools"></i>
                    </div>
                    <p class="fast-action-text" to="/manual-creator">
                        Добавить мануал
                    </p>
                </router-link>
    
                <router-link class="fast-action-card link" to="/admin/manuals">
                    <div class="action-card-icon">
                        <i class="fa fa-pen"></i>
                    </div>
                    <p class="fast-action-text">
                        Модерация мануалов
                    </p>
                </router-link>
    
                <div class="fast-action-card">
                    <div class="action-card-icon">
                        <i class="fa fa-file-text"></i>
                    </div>
                    <p class="fast-action-text">
                        Добавить новость
                    </p>
                </div>
            </div>
        </section>
    </div>

    <AddUserModal
        :is-open="showAddUserModal"
        @close="showAddUserModal = false"
        @submit="addUser"
    />
</template>

<script>
import api from '../../api/api'
import UserRegistrationsChart from '../../components/charts/UserRegistrationsChart.vue';
import Header from '../../components/Header.vue';
import AddUserModal from '../../components/modals/admin/AddUserModal.vue';

export default {
    components: {
        UserRegistrationsChart,
        AddUserModal,
        Header
    },
    data() {
        return {
            registrationsChartData: [],
            usersCount: 0,
            motosCount: 0,
            manualsCount: 0,
            lastRegUserData: [],

            showAddUserModal: false
        }
    },

    methods: {
        async getRegChartData() {
            try {
                const response = await api.get('statistic/registrations-chart')
                this.registrationsChartData = response.data.registrations || []
                this.usersCount = response.data.users_count
                this.motosCount = response.data.motos_count
                this.manualsCount = response.data.manuals_count
                this.lastRegUserData = response.data.last_reg
            } catch (err) {
                console.error('Failed load registrations data:', err)
            }
        },

        async addUser(formData) {
            try {
                const response = await api.post('/admin/user', formData)
                this.showAddUserModal = false
                this.getRegChartData()
            } catch (err) {
                console.error(`Failed add user: ${err}`)
            }
        },

        getUserRole(status) {
            const labels = {
                admin: 'Администратор',
                motorcyclist: 'Мотоциклист',
                club_member: 'Член клуба'
            }
            return labels[status]
        }
    },

    mounted() {
        this.getRegChartData()
    }
}
</script>

<style scoped>
/* === STATISTIC === */
.stat-cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(1, 1fr);
    gap: 16px;
}

.stat-card {
    display: flex;
    gap: 16px;
    justify-content: center;
    padding: 12px 14px;
    background-color: var(--bg-card);
    border-radius: 10px;
    transition: all 0.3s ease;
}
.stat-card:hover {
    background-color: var(--accent-trans);
}

.card-icon {
    width: 48px;
    height: 48px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 10px;
    background-color: var(--accent-trans);
    color: var(--accent);
}

.card-title {
    font-size: 14px;
    color: var(--text-secondary);
}

.card-value {
    font-size: 21px;
    font-weight: 600;
}

@media (max-width: 1000px) {
    .stat-cards {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(2, 1fr);
    }

    .stat-card.third {
        grid-column: span 2 / span 2;
    }
}

@media (max-width: 520px) {
    .stat-cards {
        grid-template-columns: repeat(1, 1fr);
        grid-template-rows: repeat(3, 1fr);
    }

    .stat-card.third {
        grid-column: span 1 / span 1;
    }
}


/* === MAIN SECTION === */
.main-section-wrapper {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(1, 1fr);
    gap: 16px;
}

.chart-wrapper {
    grid-column: span 2 / span 2;
    padding: 12px 14px;
    background-color: var(--bg-card);
    border-radius: 10px;
}

/* --- last reg */
.last-reg-wrapper {
    padding: 12px 14px;
    background-color: var(--bg-card);
    border-radius: 10px;
}

.last-reg-cards {
    display: flex;
    flex-direction: column;
}

.last-reg-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 8px;
}

.user-info {
    display: flex;
    gap: 14px;
    align-items: center;
    margin-bottom: 8px;
}

.user-img {
    width: 38px;
    height: 38px;
    border-radius: 50%;
}

.user-time {
    font-size: 14px;
    color: var(--text-muted);
}

.user-status {
    padding: 4px 10px;
    background-color: var(--bg-secondary);
    border-radius: 6px;
    color: var(--text-secondary);
}

.user-status.admin {
    color: var(--accent);
    font-weight: 600;
}
.user-status.club_member {
    color: var(--success);
    font-weight: 600;
}

.last-reg-wrapper button {
    width: 100%;
}

@media (max-width: 1300px) {
    .main-section-wrapper {
        display: flex;
        flex-direction: column;
    }
}


/* === FAST ACTIONS === */
.fast-section-wrapper {
    padding: 14px 14px;
    background-color: var(--bg-card);
    border-radius: 10px;
}

.fast-action-card-wrapper {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(1, 1fr);
    gap: 16px;  
}

.fast-action-card {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 14px;
    padding: 12px 14px;
    background-color: var(--bg-card);
    border-radius: 10px;
    border: 2px solid var(--border-color);
    transition: all 0.3s ease;
    cursor: pointer;
}
.fast-action-card:hover {
    background-color: var(--accent-trans);
    border-color: var(--accent);
}

.fast-action-card.link {
    text-decoration: none;
}

.action-card-icon {
    font-size: 24px;
    color: var(--accent);
}

.fast-action-text {
    color: var(--text-secondary);
}

@media (max-width: 800px) {
    .fast-action-card-wrapper {
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(2, 1fr);
    }
}

@media (max-width: 620px) {
    .fast-action-card-wrapper {
        grid-template-columns: repeat(1, 1fr);
        grid-template-rows: repeat(4, 1fr);
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