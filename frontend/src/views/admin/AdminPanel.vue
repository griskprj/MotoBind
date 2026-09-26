<template>
  <div class="container">
    <LoadingOverlay :isLoading="loading" text="Загрузка панели администратора..."/>

    <Header
      title="Панель администратора"
      subtitle="Обзор ключевых показателей и активности сайта"
    />

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

    <section class="main-section-wrapper">
      <div class="chart-wrapper">
        <h3>Регистрация пользователей</h3>
        <UserRegistrationsChart :chart-data="registrationsChartData" />
      </div>
      <div class="last-reg-wrapper">
        <h3>Последние регистрации</h3>
        <div class="last-reg-cards">
          <div
            class="last-reg-card"
            v-for="user in lastRegUserData"
            :key="user.id"
          >
            <div class="user-info">
              <img class="user-img" :src="getAvatarUrl(user?.avatar)" alt="">
              <div class="reg-card-body">
                <p class="user-name">{{ user.username }}</p>
                <p class="user-time">{{ formatDate(user.last_login) }}</p>
              </div>
            </div>
            <div class="user-status" :class="user.role">
              <p class="user-role">{{ getUserRole(user.role) }}</p>
            </div>
          </div>
        </div>
        <router-link class="btn outline-btn" to="/admin/users">
          Смотреть всех пользователей <i class="fa fa-angle-right"></i>
        </router-link>
      </div>
    </section>

    <section class="fast-section-wrapper">
      <h3>Быстрые действия</h3>
      <div class="fast-action-card-wrapper">
        <div @click="showAddUserModal = true" class="fast-action-card">
          <div class="action-card-icon">
            <i class="fa fa-user-plus"></i>
          </div>
          <p class="fast-action-text">Добавить пользователя</p>
        </div>

        <router-link class="fast-action-card link" to="/manual-creator">
          <div class="action-card-icon">
            <i class="fa fa-tools"></i>
          </div>
          <p class="fast-action-text">Добавить мануал</p>
        </router-link>

        <router-link class="fast-action-card link" to="/admin/manuals">
          <div class="action-card-icon">
            <i class="fa fa-pen"></i>
          </div>
          <p class="fast-action-text">Модерация мануалов</p>
        </router-link>

        <div @click="showNewsletterModal = true" class="fast-action-card">
          <div class="action-card-icon">
            <i class="fa fa-file-text"></i>
          </div>
          <p class="fast-action-text">Отправить рассылку</p>
        </div>
      </div>
    </section>
  </div>

  <AddUserModal
    :is-open="showAddUserModal"
    @close="showAddUserModal = false"
    @saved="onUserSaved"
  />

  <NewsletterModal
    :is-open="showNewsletterModal"
    @close="showNewsletterModal = false"
    @sent="getRegChartData"
  />
</template>

<script setup>
import { onMounted, ref } from 'vue'
import UserRegistrationsChart from '@/components/charts/UserRegistrationsChart.vue'
import Header from '@/components/Header.vue'
import LoadingOverlay from '@/components/LoadingOverlay.vue'
import AddUserModal from '@/components/modals/admin/AddUserModal.vue'
import NewsletterModal from '@/components/modals/admin/NewsletterModal.vue'
import { getAvatarUrl } from '@/utils/mediaUrl'
import { getUserRoleLabel } from '@/utils/formatters'
import formatDate from '@/utils/DateFormatter.js'
import api from '@/api/api'

const loading = ref(false)
const registrationsChartData = ref([])
const usersCount = ref(0)
const motosCount = ref(0)
const manualsCount = ref(0)
const lastRegUserData = ref([])

const showAddUserModal = ref(false)
const showNewsletterModal = ref(false)

onMounted(() => {
  getRegChartData()
})

async function getRegChartData() {
  try {
    loading.value = true
    const response = await api.get('statistic/registrations-chart')
    registrationsChartData.value = response.data.registrations || []
    usersCount.value = response.data.users_count
    motosCount.value = response.data.motos_count
    manualsCount.value = response.data.manuals_count
    lastRegUserData.value = response.data.last_reg
  } catch (err) {
    console.error('Failed load registrations data:', err)
  } finally {
    loading.value = false
  }
}

function onUserSaved() {
  showAddUserModal.value = false
  getRegChartData()
}

function getUserRole(role) {
  return getUserRoleLabel(role)
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
    border: 1px solid var(--border-light);
    transition: all 0.3s ease;
}
.stat-card:hover {
    background-color: var(--accent-trans);
    border-color: var(--accent);
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
    color: var(--text-primary);
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
    border: 1px solid var(--border-light);
}

.chart-wrapper h3 {
    color: var(--text-primary);
    margin-bottom: 12px;
}

/* --- last reg */
.last-reg-wrapper {
    padding: 12px 14px;
    background-color: var(--bg-card);
    border-radius: 10px;
    border: 1px solid var(--border-light);
}

.last-reg-wrapper h3 {
    color: var(--text-primary);
    margin-bottom: 12px;
}

.last-reg-cards {
    display: flex;
    flex-direction: column;
}

.last-reg-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border-light);
    padding: 8px 0;
    margin-bottom: 4px;
}

.last-reg-card:last-child {
    border-bottom: none;
    margin-bottom: 0;
}

.user-info {
    display: flex;
    gap: 14px;
    align-items: center;
}

.user-img {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid var(--border-color);
}

.reg-card-body {
    display: flex;
    flex-direction: column;
}

.user-name {
    font-weight: 600;
    font-size: 14px;
    margin: 0;
    color: var(--text-primary);
}

.user-time {
    font-size: 12px;
    color: var(--text-muted);
    margin: 0;
}

.user-status {
    padding: 4px 10px;
    background-color: var(--bg-secondary);
    border-radius: 6px;
    color: var(--text-secondary);
    font-size: 12px;
    font-weight: 500;
}

.user-status p {
    margin: 0;
}

.user-status.admin {
    color: var(--accent-text);
    background-color: var(--accent-trans);
    font-weight: 600;
}

.user-status.club_member {
    color: var(--success-text);
    background-color: var(--success-trans);
    font-weight: 600;
}

.user-status.motorcyclist {
    color: var(--text-secondary);
    background-color: var(--border-light);
}

.last-reg-wrapper .btn {
    width: 100%;
    margin-top: 12px;
    text-decoration: none;
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
    border: 1px solid var(--border-light);
}

.fast-section-wrapper h3 {
    color: var(--text-primary);
    margin-bottom: 16px;
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
    padding: 16px 20px;
    background-color: var(--bg-secondary);
    border-radius: 10px;
    border: 2px solid var(--border-color);
    transition: all 0.3s ease;
    cursor: pointer;
    text-decoration: none;
    min-height: 72px;
}

.fast-action-card:hover {
    background-color: var(--accent-trans);
    border-color: var(--accent);
    transform: translateY(-2px);
}

.fast-action-card.link {
    text-decoration: none;
}

.action-card-icon {
    font-size: 24px;
    color: var(--accent);
    flex-shrink: 0;
}

.fast-action-text {
    color: var(--text-secondary);
    font-weight: 500;
    margin: 0;
    font-size: 14px;
    text-align: center;
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

    .fast-action-card {
        min-height: 60px;
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
