<script setup lang="ts">
const emit = defineEmits<{ navigate: [] }>()
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const toast = useToast()

async function logout() {
  if (!confirm('Выйти из аккаунта?')) return
  await auth.logout()
  toast.success('Вы вышли из системы')
  router.push('/login')
}

function isActive(path: string) {
  return route.path === path || route.path.startsWith(path + '/')
}

function onNavigate() {
  emit('navigate')
}

const baseNavItems = [
  {
    label: 'Гараж',
    links: [
      { name: 'Мой гараж', to: '/garage', icon: 'fa-solid fa-motorcycle' },
      { name: 'Обслуживание', to: '/maintenance', icon: 'fa-solid fa-wrench' },
    ]
  },
  {
    label: 'Сообщество',
    links: [
      { name: 'Мануалы', to: '/manuals', icon: 'fa-solid fa-book' },
      { name: 'Обучение', to: '/training', icon: 'fa-solid fa-graduation-cap' },
      { name: 'MotoSocial', to: '/social', icon: 'fa-solid fa-comments' },
    ]
  },
]

const adminNavItems = computed(() => {
  if (!auth.isAdmin) return []

  return [
    {
      label: 'Администрирование',
      links: [
        { name: 'Дашборд', to: '/admin', icon: 'fa-solid fa-gauge' },
        { name: 'Пользователи', to: '/admin/users', icon: 'fa-solid fa-users' },
        { name: 'Модерация мануалов', to: '/admin/manuals', icon: 'fa-solid fa-book-open' },
        { name: 'Жалобы', to: '/admin/reports', icon: 'fa-solid fa-flag' },
        { name: 'Управление обучением', to: '/admin/learning/courses', icon: 'fa-solid fa-graduation-cap' },
      ]
    }
  ]
})

const allNavGroups = computed(() => [...baseNavItems, ...adminNavItems.value])
</script>

<template>
  <aside class="app-sidebar">
    <div class="sidebar-content">
      <nav class="sidebar-nav">
        <div v-for="group in allNavGroups" :key="group.label" class="nav-group">
          <h3 class="nav-group-title">{{ group.label }}</h3>
          <ul class="nav-list">
            <li v-for="link in group.links" :key="link.to">
              <NuxtLink
                :to="link.to"
                class="nav-link"
                :class="{ 'nav-link--active': isActive(link.to) }"
                @click="onNavigate"
              >
                <span class="nav-icon">
                  <i :class="link.icon"></i>
                </span>
                {{ link.name }}
              </NuxtLink>
            </li>
          </ul>
        </div>
      </nav>
    </div>
    <div class="sidebar-footer">
      <NuxtLink to="/profile" v-if="auth.user" class="user-info">
        <div class="user-avatar">
          <i class="fa-solid fa-user"></i>
        </div>
        <div class="user-details">
          <span class="user-name">{{ auth.user.username }}</span>
          <span class="user-role">{{ auth.user.role === 'admin' ? 'Админ' : 'Мотоциклист' }}</span>
        </div>
      </NuxtLink>
      <button class="logout-btn" @click="logout" title="Выйти">
        <i class="fa-solid fa-arrow-right-from-bracket"></i>
        <span>Выйти</span>
      </button>
    </div>
  </aside>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.app-sidebar {
  width: 260px;
  height: 100%;
  background: var(--color-sidebar);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-4) 0;
}

.nav-group {
  margin-bottom: var(--space-6);
}

.nav-group-title {
  padding: 0 var(--space-4);
  margin-bottom: var(--space-2);
  font-size: var(--text-xs);
  font-weight: var(--fw-semibold);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-tertiary);
}

.nav-list {
  display: flex;
  flex-direction: column;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  transition: background var(--transition-fast), color var(--transition-fast);
  text-decoration: none;

  &:hover {
    background: var(--color-sidebar-hover);
  }

  &--active {
    background: var(--color-sidebar-active);
    color: var(--color-brand);
    font-weight: var(--fw-medium);

    .nav-icon {
      color: var(--color-brand);
    }
  }
}

.nav-icon {
  color: var(--color-text-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.sidebar-footer {
  margin-top: auto;
  padding: var(--space-4);
  border-top: 1px solid var(--color-border-light);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-surface-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-tertiary);
  font-size: 14px;
  flex-shrink: 0;
}

.user-details {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.user-name {
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  color: var(--color-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  width: 100%;
  padding: var(--space-2);
  background: var(--color-danger-soft);
  color: var(--color-danger);
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  cursor: pointer;
  transition: all var(--transition-fast);

  &:hover {
    background: var(--color-danger);
    color: #fff;
    border-color: var(--color-danger);
  }

  i {
    font-size: 14px;
  }
}
</style>
