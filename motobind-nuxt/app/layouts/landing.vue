<template>
  <div class="landing-layout">
    <slot />
    <AppFooter />
  </div>
</template>

<style scoped>
.landing-layout {
  display: flex;
  flex-direction: column;
  min-height: 100dvh;
}
</style>
