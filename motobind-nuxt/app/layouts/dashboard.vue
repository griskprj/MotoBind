
<script setup lang="ts">
import AppHeader from '~/components/layout/AppHeader.vue'
import AppSidebar from '~/components/layout/AppSidebar.vue'
</script>

<template>
  <div class="dashboard-layout">
    <AppHeader />

    <div class="dashboard-content">
      <AppSidebar />

      <main class="main-content">
        <slot />
      </main>
    </div>
  </div>
</template>

<style scoped lang="scss">
.dashboard-layout {
  min-height: 100vh;
  background: #f8f8fa;
}

.dashboard-content {
  display: flex;
  min-height: calc(100vh - 64px);
}

.main-content {
  flex: 1;
  min-width: 0;
  padding: 32px;
}
</style>
