<template>
  <header class="page-header">
    <div class="header-left">
      <h2>{{ title }}</h2>
      <p class="header-subtitle">{{ subtitle }}</p>
    </div>

    <div class="header-right">
      <NotificationBell v-if="isAuthenticated" />
      <button
        class="theme-toggle"
        :title="isDark ? 'Включить светлую тему' : 'Включить тёмную тему'"
        @click="toggleTheme"
      >
        <i :class="isDark ? 'fa fa-sun' : 'fa fa-moon'" />
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from '@/shared/theme/useTheme'
import NotificationBell from './NotificationBell.vue'

defineProps<{
  title: string
  subtitle?: string
}>()

const auth = useAuthStore()
const { isDark, toggle: toggleTheme } = useTheme()

const isAuthenticated = computed(() => auth.isAuthenticated)
</script>

<style scoped>
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

.header-subtitle {
    font-size: 14px;
    color: var(--text-secondary);
}

.header-right {
    display: flex;
    align-items: center;
    gap: 16px;
}

/* ===== КНОПКА ПЕРЕКЛЮЧЕНИЯ ТЕМЫ ===== */
.theme-toggle {
    min-width: 40px;
    min-height: 40px;
    padding: 0;
    background: var(--bg-primary);
    border: 2px solid var(--border-color);
    border-radius: 50%;
    color: var(--text-primary);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    transition: all 0.3s ease;
}

.theme-toggle:hover {
    background: var(--accent);
    border-color: var(--accent);
    color: white;
    transform: translateY(0px);
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
}


.theme-toggle i {
    transition: transform 0.3s ease;
}

/* ===== АДАПТИВНОСТЬ ===== */
@media(max-width: 720px) {
    .header-right {
        display: flex;
        gap: 12px;
    }
}
</style>
