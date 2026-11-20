<script setup lang="ts">
const isVisible = ref(false)

onMounted(() => {
  const consent = localStorage.getItem('cookie-consent')
  if (!consent) {
    isVisible.value = true
  }
})

function accept() {
  localStorage.setItem('cookie-consent', 'true')
  isVisible.value = false
}
</script>

<template>
  <Transition name="slide-up">
    <div v-if="isVisible" class="cookie-banner">
      <div class="cookie-content">
        <p>
          Мы используем куки для работы сайта и улучшения опыта.
          Продолжая, вы соглашаетесь с <NuxtLink to="/privacy">политикой конфиденциальности</NuxtLink>.
        </p>
        <BaseButton variant="primary" size="sm" @click="accept">Принять</BaseButton>
      </div>
    </div>
  </Transition>
</template>

<style scoped lang="scss">
.cookie-banner {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
  padding: var(--space-4);
  z-index: var(--z-toast);
  box-shadow: 0 -4px 12px rgba(0,0,0,0.1);
}

.cookie-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  font-size: var(--text-sm);

  @media (max-width: 640px) {
    flex-direction: column;
    align-items: stretch;
    text-align: center;
  }
}

.slide-up-enter-active, .slide-up-leave-active {
  transition: transform var(--transition-base);
}
.slide-up-enter-from, .slide-up-leave-to {
  transform: translateY(100%);
}
</style>
