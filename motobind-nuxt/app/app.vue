<script setup lang="ts">
const { resolvedTheme } = useTheme()
useHead({
  htmlAttrs: { 'data-theme': resolvedTheme },
})
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
