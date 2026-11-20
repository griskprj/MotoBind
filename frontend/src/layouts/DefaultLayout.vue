<template>
  <div class="app-with-sidebar">
    <Sidebar />
    <div class="app-content">
      <div class="page-content">
        <RouterView />
      </div>
      <Footer v-if="showFooter" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import Footer from '@/components/Footer.vue'

const route = useRoute()
const showFooter = computed(() => route.meta.showFooter !== false)
</script>

<style scoped>
.app-with-sidebar {
  display: flex;
  min-height: 100vh;
}

.app-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  margin-left: 260px;
  transition: margin-left 0.3s ease;
}

.page-content {
  flex: 1;
  padding: 24px 32px;
  width: 100%;
  min-width: 0;
}

@media (max-width: 770px) {
  .app-content {
    margin-left: 0;
  }
  .page-content {
    padding: 80px 16px 20px;
  }
}
</style>
