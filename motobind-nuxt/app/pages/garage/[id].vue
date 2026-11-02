<script setup lang="ts">
import type { Motorcycle } from '~/types'

definePageMeta({ middleware: 'auth' })

const route = useRoute()
const api = useApi()
const id = computed(() => route.params.id as string)

const { data: motorcycle, pending, error, refresh } = await useAsyncData(
  `moto-${id.value}`,
  () => api.motorcycle.get(id.value),
)

useSeoMeta({
  title: () => motorcycle.value ? `${motorcycle.value.name} — Гараж` : 'Мотоцикл — Гараж',
  robots: 'noindex',
})

async function onUpdated() {
  await refresh()
}
</script>

<template>
  <div class="moto-page">
    <!-- Состояние загрузки -->
    <div v-if="pending" class="moto-skeleton">
      <BaseSkeleton height="300px" rounded class="mb-4" />
      <div class="grid-2">
        <BaseSkeleton height="200px" rounded />
        <BaseSkeleton height="200px" rounded />
      </div>
    </div>

    <!-- Ошибка -->
    <BaseEmptyState
      v-else-if="error || !motorcycle"
      title="Мотоцикл не найден"
      description="Возможно, он был удалён или у вас нет доступа."
    >
      <template #action>
        <BaseButton to="/garage" variant="primary">Вернуться в гараж</BaseButton>
      </template>
    </BaseEmptyState>

    <!-- Контент -->
    <template v-else>
      <!-- Хлебные крошки и заголовок -->
      <header class="moto-header">
        <NuxtLink to="/garage" class="back-link">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <path d="M15 19l-7-7 7-7" />
          </svg>
          Назад в гараж
        </NuxtLink>
        <h1 class="moto-title">{{ motorcycle.name }}</h1>
      </header>

      <div class="moto-layout">
        <!-- Левая колонка -->
        <div class="moto-main stack" style="--stack-gap: var(--space-6)">
          <MotorcyclePhoto :motorcycle="motorcycle" @updated="onUpdated" />
          <MotorcycleDetails :motorcycle="motorcycle" @updated="onUpdated" />
          <MotorcycleMileage :motorcycle="motorcycle" @updated="onUpdated" />
          <MotorcycleNote :motorcycle="motorcycle" @updated="onUpdated" />

          <MaintenanceSection :motorcycle="motorcycle" @updated="onUpdated"/>
        </div>

        <!-- Правая колонка -->
        <div class="moto-sidebar stack" style="--stack-gap: var(--space-6)">
          <MotorcycleDelete :motorcycle="motorcycle" />
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.moto-page {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.moto-header {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  width: fit-content;

  &:hover { color: var(--color-brand); }
}

.moto-title {
  font-size: var(--text-3xl);
  font-weight: var(--fw-bold);
  color: var(--color-text);
  line-height: var(--leading-tight);
}

.moto-layout {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);

  @include lg-up {
    display: grid;
    grid-template-columns: 1fr 340px;
    align-items: start;
  }
}

.moto-main {
  min-width: 0;
}

.mb-4 { margin-bottom: var(--space-4); }
.grid-2 {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);
  @include md-up { grid-template-columns: 1fr 1fr; }
}
</style>
