<template>
  <!-- Desktop: постоянный сайдбар -->
  <aside v-if="isDesktop" class="sidebar">
    <SidebarContent />
  </aside>

  <!-- Mobile: drawer + гамбургер -->
  <template v-else>
    <button
      class="sidebar-toggle"
      :class="{ active: isDrawerOpen }"
      aria-label="Меню"
      @click="isDrawerOpen = !isDrawerOpen"
    >
      <span class="burger-line" />
      <span class="burger-line" />
      <span class="burger-line" />
    </button>

    <AppDrawer v-model="isDrawerOpen" placement="left" :width="280">
      <SidebarContent @navigate="isDrawerOpen = false" />
    </AppDrawer>
  </template>
</template>

<script setup>
import { ref } from 'vue'
import { useMediaQuery } from '@vueuse/core'
import SidebarContent from './sidebar/SidebarContent.vue'
import { AppDrawer } from '@/components/ui'

const isDesktop = useMediaQuery('(min-width: 771px)')
const isDrawerOpen = ref(false)
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 260px;
  height: 100vh;
  background: var(--bg-primary);
  border-right: 1px solid var(--border-light);
  z-index: 1000;
  display: flex;
  flex-direction: column;
}

.sidebar-toggle {
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 1001;
  display: flex;
  flex-direction: column;
  gap: 5px;
  width: 30px;
  height: 21px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
}

.sidebar-toggle .burger-line {
  width: 100%;
  height: 3px;
  background-color: var(--text-primary);
  transition: all 0.3s ease;
}

.sidebar-toggle.active .burger-line:nth-child(1) {
  transform: translateY(8px) rotate(45deg);
}
.sidebar-toggle.active .burger-line:nth-child(2) {
  opacity: 0;
}
.sidebar-toggle.active .burger-line:nth-child(3) {
  transform: translateY(-8px) rotate(-45deg);
}
</style>
