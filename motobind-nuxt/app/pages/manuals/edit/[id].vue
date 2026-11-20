<script setup lang="ts">
definePageMeta({ middleware: 'auth' })
const route = useRoute()
const router = useRouter()
const api = useApi()

const { data: manual, pending, error } = await useAsyncData(
  `manual-edit-${route.params.id}`,
  () => api.manuals.get(route.params.id as string)
)

if (error.value || !manual.value) {
  throw createError({ statusCode: 404, statusMessage: 'Мануал не найден' })
}

useSeoMeta({ title: `Редактировать: ${manual.value.title}`, robots: 'noindex' })
</script>

<template>
  <div class="page-edit-manual">
    <header class="page-header">
      <NuxtLink :to="`/manuals/${route.params.id}`" class="back-link">← Назад к мануалу</NuxtLink>
      <h1 class="page-title">Редактировать мануал</h1>
    </header>
    <div v-if="pending" class="loading">Загрузка...</div>
    <ManualForm
      v-else-if="manual"
      :initial-data="manual"
      @success="() => router.push(`/manuals/${manual.id}`)"
      @cancel="router.push(`/manuals/${manual.id}`)"
    />
  </div>
</template>
