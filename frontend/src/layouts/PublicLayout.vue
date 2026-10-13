<template>
  <div class="public-layout">
    <RouterView />
    <Footer v-if="showFooter" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Footer from '@/components/Footer.vue'

const route = useRoute()
const showFooter = computed(() => route.meta.showFooter !== false)
</script>

<style scoped>
.public-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
