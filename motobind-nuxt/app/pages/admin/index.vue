<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'admin'] })

useSeoMeta({ title: 'Админ-панель', robots: 'noindex' })

const api = useApi()
const { data, pending } = await useAsyncData('admin-dashboard', () => api.admin.getDashboard())

</script>

<template>
  <div class="admin-page">
    <header class="page-header">
      <h1 class="page-title">Админ-панель</h1>
      <p class="page-subtitle">Управление пользователями, контентом и жалобами.</p>
    </header>

    <div v-if="pending" class="loading">
      <BaseSkeleton height="100px" rounded v-for="i in 3" :key="i" />
    </div>

    <template v-else-if="data">
      <!-- Статистика -->
      <div class="stats-grid">
        <BaseCard padding="lg" class="stat-card">
          <div class="stat-icon"><i class="fa-solid fa-users"></i></div>
          <div class="stat-info">
            <span class="stat-value">{{ data.users_count }}</span>
            <span class="stat-label">Пользователей</span>
          </div>
        </BaseCard>
        <BaseCard padding="lg" class="stat-card">
          <div class="stat-icon"><i class="fa-solid fa-book"></i></div>
          <div class="stat-info">
            <span class="stat-value">{{ data.manuals_count }}</span>
            <span class="stat-label">Мануалов</span>
          </div>
        </BaseCard>
        <BaseCard padding="lg" class="stat-card">
          <div class="stat-icon"><i class="fa-solid fa-motorcycle"></i></div>
          <div class="stat-info">
            <span class="stat-value">{{ data.motorcycles_count }}</span>
            <span class="stat-label">Мотоциклов</span>
          </div>
        </BaseCard>
      </div>

      <!-- Быстрые ссылки -->
      <div class="quick-links">
        <h2 class="section-title">Разделы</h2>
        <div class="links-grid">
          <NuxtLink to="/admin/users" class="link-card">
            <i class="fa-solid fa-users-gear"></i>
            <span>Пользователи</span>
          </NuxtLink>
          <NuxtLink to="/admin/manuals" class="link-card">
            <i class="fa-solid fa-book-open"></i>
            <span>Модерация мануалов</span>
          </NuxtLink>
          <NuxtLink to="/admin/reports" class="link-card">
            <i class="fa-solid fa-flag"></i>
            <span>Жалобы</span>
          </NuxtLink>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.admin-page { display: flex; flex-direction: column; gap: var(--space-6); }
.page-title { font-size: var(--text-2xl); font-weight: var(--fw-bold); }
.page-subtitle { color: var(--color-text-secondary); margin-top: var(--space-1); }

.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: var(--space-4); }
.stat-card { display: flex; align-items: center; gap: var(--space-4); }
.stat-icon { font-size: 28px; color: var(--color-brand); width: 48px; height: 48px; display: flex; align-items: center; justify-content: center; background: var(--color-brand-soft); border-radius: var(--radius-md); }
.stat-info { display: flex; flex-direction: column; }
.stat-value { font-size: var(--text-2xl); font-weight: var(--fw-bold); }
.stat-label { font-size: var(--text-sm); color: var(--color-text-secondary); }

.quick-links { display: flex; flex-direction: column; gap: var(--space-4); }
.section-title { font-size: var(--text-lg); font-weight: var(--fw-semibold); }
.links-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: var(--space-4); }
.link-card {
  display: flex; flex-direction: column; align-items: center; gap: var(--space-2);
  padding: var(--space-6); background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md);
  text-decoration: none; color: var(--color-text); font-weight: var(--fw-medium); transition: all var(--transition-fast);
  i { font-size: 24px; color: var(--color-brand); }
  &:hover { border-color: var(--color-brand); box-shadow: var(--shadow-sm); transform: translateY(-2px); }
}
</style>
