<script setup lang="ts">
import { ref, onMounted } from 'vue'

const deferredPrompt = ref<any>(null)
const showPrompt = ref(false)
const showIosInstructions = ref(false)
const isIos = ref(false)

onMounted(() => {
  const standalone = window.matchMedia('(display-mode: standalone)').matches || (navigator as any).standalone === true
  isIos.value = /iphone|ipad|ipod/i.test(navigator.userAgent)
  if (standalone) return

  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault()
    deferredPrompt.value = e
    showPrompt.value = true
  })

  window.addEventListener('appinstalled', () => {
    showPrompt.value = false
    showIosInstructions.value = false
    deferredPrompt.value = null
  })

  if (isIos.value) showPrompt.value = true
})

async function install() {
  if (!deferredPrompt.value) {
    showIosInstructions.value = isIos.value
    return
  }
  deferredPrompt.value.prompt()
  const { outcome } = await deferredPrompt.value.userChoice
  if (outcome === 'accepted') {
    showPrompt.value = false
  }
  deferredPrompt.value = null
}
</script>

<template>
  <div v-if="showPrompt" class="pwa-banner">
    <div class="pwa-icon">
      <img src="/icons/icon-192x192.png" alt="MotoBind" />
    </div>
    <div class="pwa-text">
      <strong>Установить MotoBind</strong>
      <span>Быстрый доступ с рабочего стола</span>
    </div>
    <BaseButton size="sm" variant="primary" @click="install">{{ isIos ? 'Как установить' : 'Установить' }}</BaseButton>
    <button class="pwa-close" @click="showPrompt = false">×</button>
  </div>
  <BaseModal v-if="showIosInstructions" title="Установить MotoBind" @close="showIosInstructions = false">
    <p>Откройте сайт в Safari, нажмите «Поделиться», затем выберите «На экран Домой».</p>
    <p class="ios-note">После добавления MotoBind будет открываться отдельно, как приложение.</p>
  </BaseModal>
</template>

<style scoped lang="scss">
.pwa-banner {
  position: fixed;
  bottom: 20px;
  left: 20px;
  right: 20px;
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: 0 8px 24px rgba(0,0,0,0.4);
  z-index: 1000;

  @include md-up {
    left: auto;
    right: 20px;
    max-width: 400px;
  }
}
.pwa-icon img {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
}
.pwa-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  strong { color: var(--color-text); }
}
.pwa-close {
  background: none;
  border: none;
  color: var(--color-text-tertiary);
  font-size: 20px;
  cursor: pointer;
  padding: 0 4px;
}
.ios-note { margin-top: var(--space-3); color: var(--color-text-secondary); }
</style>
