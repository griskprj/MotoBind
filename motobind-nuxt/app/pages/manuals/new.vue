<script setup lang="ts">
definePageMeta({ middleware: 'auth' })
useSeoMeta({ title: 'Создать мануал', robots: 'noindex' })
const router = useRouter()
</script>

<template>
  <div class="page-new-manual">
    <header class="page-header">
      <NuxtLink to="/manuals" class="back-link">← Все мануалы</NuxtLink>
      <h1 class="page-title">Создать мануал</h1>
      <NuxtLink class="link" to="/manual-rules">Правила оформления мануалов</NuxtLink>
    </header>
    <ManualForm @success="(m) => router.push(`/manuals/${m.id}`)" @cancel="router.push('/manuals')" />
  </div>
</template>

<style lang="scss" scoped>
.page-header {
  margin-bottom: var(--space-6);
}

.link {
  color: var(--color-brand);
}
</style>
