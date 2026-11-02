<script setup lang="ts">
const auth = useAuthStore()
</script>

<template>
  <div class="default-layout">
    <!-- Для авторизованных: рабочий хедер и сайдбар -->
    <template v-if="auth.isAuthenticated">
      <AppHeader />
      <div class="layout-body">
        <AppSidebar class="desktop-sidebar" />
        <main class="layout-main">
          <slot />
        </main>
      </div>
    </template>

    <!-- Для гостей: публичный хедер без сайдбара -->
    <template v-else>
      <header class="public-header">
        <div class="container header-container">
          <NuxtLink to="/" class="logo">
            <span class="logo-m">Moto</span><span class="accent">Bind</span>
          </NuxtLink>
          <div class="header-actions">
            <NuxtLink to="/login" class="login-link">Войти</NuxtLink>
            <BaseButton to="/register" variant="primary" size="sm">Начать</BaseButton>
          </div>
        </div>
      </header>
      <main class="public-main">
        <slot />
      </main>
    </template>

    <AppFooter />
    <BaseToastHost />
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.default-layout {
  display: flex;
  flex-direction: column;
  min-height: 100dvh;
  background: var(--color-bg);
}

/* === Авторизованный лэйаут === */
.layout-body {
  display: flex;
  flex: 1;
}

.desktop-sidebar {
  display: none;

  @include lg-up {
    display: flex;
    position: sticky;
    top: 60px;
    height: calc(100dvh - 60px);
  }
}

.layout-main {
  flex: 1;
  min-width: 0;
  padding: var(--space-4);
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;

  @include md-up {
    padding: var(--space-6);
  }
}

/* === Публичный лэйаут (для гостей) === */
.public-header {
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
  background: color-mix(in srgb, var(--color-bg) 85%, transparent);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--color-border-light);
  padding: var(--space-3) 0;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--space-4);
}

.logo {
  font-size: 24px;
  font-weight: var(--fw-bold);
  text-decoration: none;
  color: var(--color-text);
}
.logo-m { font-weight: 900; }
.accent { color: var(--color-brand); }

.header-actions {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.login-link {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  text-decoration: none;
  &:hover { color: var(--color-text); }
}

.public-main {
  flex: 1;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--space-6) var(--space-4);
}
</style>
