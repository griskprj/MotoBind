<template>
  <div class="sidebar-content">
    <!-- Логотип -->
    <div class="sidebar-logo">
      <img src="/icons/favicon-remove-bg.png" alt="MotoBind">
      <div class="logo-text">
        <span class="logo-left">Moto</span><span class="logo-right">Bind</span>
        <span v-if="isAdminRoute" class="admin-logo">Admin</span>
      </div>
    </div>

    <!-- Меню -->
    <nav class="sidebar-nav">
      <AppMenu
        :options="menuOptions"
        :active-key="route.path"
        @select="onMenuSelect"
      />
    </nav>

    <!-- Футер -->
    <div class="sidebar-footer">
      <div v-if="!isDesktop" class="footer-row-mobile">
        <button class="theme-toggle" @click="toggleTheme">
          <i :class="isDark ? 'fa fa-sun' : 'fa fa-moon'" />
        </button>
        <button class="theme-toggle" @click="goNotifications">
          <i class="fa fa-bell" />
        </button>
      </div>

      <router-link to="/profile" class="footer-link" @click="emit('navigate')">
        <i class="fa fa-user" />
        <span>Профиль</span>
      </router-link>

      <button class="btn-logout-sidebar" @click="logout">
        <i class="fa fa-sign-out" />
        <span>Выйти</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMediaQuery } from '@vueuse/core'
import { useAuthStore } from '@/stores/auth'
import { useBusinessStore } from '@/stores/business'
import { useBookingsStore } from '@/stores/bookings'
import { useTheme } from '@/composables/useTheme'
import { AppMenu } from '@/components/ui'
import api from '@/api/api'

const emit = defineEmits(['navigate'])

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const business = useBusinessStore()
const bookings = useBookingsStore()
const { isDark, toggle: toggleTheme } = useTheme()
const isDesktop = useMediaQuery('(min-width: 771px)')

const isAdmin = computed(() => auth.isAdmin)
const isAdminRoute = computed(() => route.path.startsWith('/admin'))
const hasBusinessAccount = computed(() => business.hasAccount)

// === Бейджи ===
const myBookingsCount = computed(
  () =>
    bookings.myBookings?.filter(
      (b) => b.status === 'pending' || b.status === 'confirmed'
    ).length || 0
)
const pendingMasterBookings = computed(
  () => bookings.masterBookings?.filter((b) => b.status === 'pending').length || 0
)

// === Меню ===
const menuOptions = computed(() => {
  if (isAdminRoute.value) {
    return [
      {
        type: 'group',
        label: 'Главная',
        key: 'admin-main',
        children: [
          { label: 'Панель управления', key: '/admin/panel', icon: 'fa fa-sitemap' },
        ],
      },
      {
        type: 'group',
        label: 'Управление',
        key: 'admin-manage',
        children: [
          { label: 'Пользователи', key: '/admin/users', icon: 'fa fa-users' },
          { label: 'Мотоциклы', key: '/admin/motorcycles', icon: 'fa fa-motorcycle' },
        ],
      },
      {
        type: 'group',
        label: 'Модерация',
        key: 'admin-moderate',
        children: [
          { label: 'Мануалы', key: '/admin/manuals', icon: 'fa fa-tools' },
          { label: 'Репорты', key: '/admin/reports', icon: 'fa fa-flag' },
          { label: 'Услуги', key: '/admin/services', icon: 'fa fa-wrench' },
        ],
      },
      { type: 'divider', key: 'divider-admin' },
      { label: 'Назад к сервису', key: '/garage', icon: 'fa fa-home' },
    ]
  }

  const groups = [
    {
      type: 'group',
      label: 'Гараж',
      key: 'garage',
      children: [
        { label: 'Мой гараж', key: '/garage', icon: 'fa fa-motorcycle' },
        { label: 'Обслуживание', key: '/maintenance', icon: 'fa fa-tools' },
        {
          label: 'Мои заявки',
          key: '/bookings',
          icon: 'fa fa-calendar-check',
          ...(myBookingsCount.value > 0 ? { badge: myBookingsCount.value } : {}),
        },
      ],
    },
    {
      type: 'group',
      label: 'Сообщество',
      key: 'community',
      children: [
        { label: 'Мастера и СТО', key: '/masters', icon: 'fa fa-user-tie' },
        { label: 'Мануалы', key: '/manuals', icon: 'fa fa-book' },
        { label: 'MotoSocial', key: '/social', icon: 'fa fa-users' },
      ],
    },
  ]

  if (hasBusinessAccount.value) {
    groups.push({
      type: 'group',
      label: 'Мой бизнес',
      key: 'business',
      children: [
        { label: 'Кабинет бизнеса', key: '/business', icon: 'fa fa-suitcase' },
        { label: 'Клиенты', key: '/business/clients', icon: 'fa fa-users' },
        { label: 'Мои услуги', key: '/business/services', icon: 'fa fa-wrench' },
        {
          label: 'Заявки мастеру',
          key: '/business/bookings',
          icon: 'fa fa-inbox',
          ...(pendingMasterBookings.value > 0
            ? { badge: pendingMasterBookings.value }
            : {}),
        },
      ],
    })
  }

  if (isAdmin.value) {
    groups.push({
      type: 'group',
      label: '',
      key: 'admin',
      children: [
        { label: 'Админ-панель', key: '/admin/panel', icon: 'fa fa-shield' },
      ],
    })
  }

  return groups
})

// === Навигация ===
function onMenuSelect(key) {
  if (!key.startsWith('/')) return
  router.push(key)
  emit('navigate')
}

function goNotifications() {
  router.push('/notifications')
  emit('navigate')
}

// === Logout ===
async function logout() {
  try {
    await api.post('/auth/logout')
  } catch (err) {
    console.error('Logout failed:', err)
  } finally {
    auth.logout()
    router.push('/login')
  }
}

// === Инициализация ===
onMounted(async () => {
  if (!auth.isAuthenticated) return
  try {
    await business.loadAccount()
  } catch {}
  try {
    await bookings.loadMyBookings()
    if (business.hasAccount) {
      await bookings.loadMasterBookings()
    }
  } catch {}
})
</script>

<style scoped>
.sidebar-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: var(--bg-primary);
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px 20px 16px;
  border-bottom: 1px solid var(--border-light);
}

.sidebar-logo img {
  width: 40px;
  height: 40px;
}

.logo-text {
  font-size: 22px;
  font-weight: 700;
  white-space: nowrap;
}

.logo-left { color: var(--text-primary); }
.logo-right { color: var(--accent); }

.admin-logo {
  font-size: 14px;
  color: var(--accent);
  margin-left: 4px;
}

.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.sidebar-footer {
  border-top: 1px solid var(--border-light);
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.footer-row-mobile {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.footer-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.footer-link:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.footer-link i {
  width: 20px;
  text-align: center;
}

.btn-logout-sidebar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 10px;
  border: none;
  border-radius: var(--radius-md);
  background: var(--danger-trans);
  color: var(--danger-text);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-logout-sidebar:hover {
  background: var(--danger);
  color: #fff;
}

.theme-toggle {
  padding: 8px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 16px;
  transition: all 0.2s ease;
}

.theme-toggle:hover {
  background: var(--accent-trans);
  color: var(--accent);
}
</style>
