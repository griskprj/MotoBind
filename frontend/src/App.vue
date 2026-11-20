<template>
  <div class="animated-bg" />
  <component :is="currentLayout" />
  <ToastContainer />
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'
import PublicLayout from '@/layouts/PublicLayout.vue'
import { ToastContainer } from '@/components/ui'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const auth = useAuthStore()

const currentLayout = computed(() => {
  const layout = route.meta.layout

  if (layout === 'auth') return AuthLayout

  return auth.isAuthenticated ? DefaultLayout : PublicLayout
})
</script>

<style>
.animated-bg {
  position: fixed;
  inset: 0;
  z-index: -2;
  background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
  pointer-events: none;
}
</style>
