<script setup lang="ts">
const auth = useAuthStore()
const api = useApi()
const route = useRoute()
const { resolvedTheme, toggleTheme } = useTheme()
const isMenuOpen = ref(false)
const unreadCount = ref(0)

async function loadUnreadCount() {
  if (!auth.isAuthenticated) return
  try {
    const res = await api.notifications.getUnreadCount()
    unreadCount.value = res.unread_count
  } catch (e) {}
}

onMounted(loadUnreadCount)

watch(() => route.path, loadUnreadCount)
</script>

<template>
  <header class="app-header">
    <!-- Логотип и бургер (мобилка) -->
    <div class="header-left">
      <button class="burger" @click="isMenuOpen = !isMenuOpen">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M4 6h16M4 12h16M4 18h16" stroke-linecap="round"/>
        </svg>
      </button>
      <NuxtLink to="/garage" class="logo">MotoBind</NuxtLink>
    </div>

    <!-- Правая часть: тема, профиль -->
    <div class="header-right">
      <NuxtLink to="/notifications" class="icon-btn notif-link" title="Уведомления">
        <i class="fa-solid fa-bell"></i>
        <span v-if="unreadCount > 0" class="unread-dot">{{ unreadCount > 9 ? '9+' : unreadCount }}</span>
      </NuxtLink>

      <button class="icon-btn" @click="toggleTheme" title="Сменить тему">
        <svg v-if="resolvedTheme === 'dark'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="5"/><path d="M12 1v2m0 18v2M4.22 4.22l1.42 1.42m12.72 12.72l1.42 1.42M1 12h2m18 0h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" stroke-linecap="round"/>
        </svg>
        <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>

      <div v-if="auth.user" class="user-profile">
        <span class="user-name">{{ auth.user.username }}</span>
      </div>
    </div>
  </header>

  <!-- Мобильное меню (выезжает) -->
  <Transition name="fade">
    <div v-if="isMenuOpen" class="mobile-menu-overlay" @click="isMenuOpen = false">
      <div class="mobile-menu" @click.stop>
        <AppSidebar @navigate="isMenuOpen = false" />
      </div>
    </div>
  </Transition>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.app-header {
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  padding: 0 var(--space-4);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);

  @include md-up {
    padding: 0 var(--space-6);
  }
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.burger {
  display: flex;
  color: var(--color-text);

  @include lg-up {
    display: none;
  }
}

.logo {
  font-size: var(--text-xl);
  font-weight: var(--fw-bold);
  color: var(--color-brand);
}

.header-right {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.icon-btn {
  display: flex;
  color: var(--color-text-secondary);
  transition: color var(--transition-fast);

  &:hover { color: var(--color-text); }
}

.notif-link {
  position: relative;
}

.unread-dot {
  position: absolute;
  top: -4px;
  right: -4px;
  background: var(--color-danger);
  color: #fff;
  font-size: 10px;
  font-weight: bold;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--color-surface);
}

.user-profile {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.user-name {
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  color: var(--color-text);
}

.mobile-menu-overlay {
  position: fixed;
  inset: 0;
  z-index: var(--z-overlay);
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(2px);

  @include lg-up {
    display: none;
  }
}

.mobile-menu {
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  width: 280px;
  background: var(--color-sidebar);
  animation: slideIn var(--transition-fast) ease-out;
}

@keyframes slideIn {
  from { transform: translateX(-100%); }
  to { transform: translateX(0); }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity var(--transition-fast);
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
