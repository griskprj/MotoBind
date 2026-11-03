<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

useSeoMeta({
  title: 'Мой гараж',
  description: 'Управляйте своими мотоциклами и обслуживанием.',
  robots: 'noindex',
})

const api = useApi()

const { data: motorcycles, pending, error, refresh } = await useAsyncData(
  'garage-list',
  () => api.motorcycle.list(),
  { default: () => [] }
)
</script>

<template>
  <div class="garage-page">
    <header class="page-header">
      <div>
        <h1 class="page-title">Мой гараж</h1>
        <p class="page-subtitle">Ваши мотоциклы и записи об обслуживании</p>
      </div>
      <BaseButton to="/garage/new" variant="primary" size="md">
        <template #icon>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <path d="M12 5v14M5 12h14" />
          </svg>
        </template>
        Добавить
      </BaseButton>
    </header>

    <!-- Загрузка (скелетоны) -->
    <div v-if="pending" class="garage-grid">
      <BaseCard v-for="i in 2" :key="i" padding="none" class="skeleton-card">
        <div class="skeleton-card__img"><BaseSkeleton height="100%" /></div>
        <div class="skeleton-card__content">
          <BaseSkeleton width="60%" height="24px" />
          <BaseSkeleton width="40%" height="16px" />
        </div>
      </BaseCard>
    </div>

    <!-- Ошибка -->
    <div v-else-if="error" class="garage-error">
      <p>Не удалось загрузить гараж.</p>
      <BaseButton variant="secondary" @click="refresh()">Попробовать снова</BaseButton>
    </div>

    <!-- Пустое состояние -->
    <BaseEmptyState
      v-else-if="motorcycles.length === 0"
      title="Гараж пуст"
      description="Добавьте свой первый мотоцикл, чтобы отслеживать его обслуживание и историю."
    >
      <template #icon>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M12 9v6m3-3H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" stroke-linecap="round" />
        </svg>
      </template>
      <template #action>
        <BaseButton to="/garage/new" variant="primary">Добавить мотоцикл</BaseButton>
      </template>
    </BaseEmptyState>

    <div v-else class="garage-body-wrapper">
      <!-- Статистика гаража -->
      <GarageStatistics/>

      <!-- Список мотоциклов -->
      <div class="garage-grid">
        <MotorcycleCard
          v-for="moto in motorcycles"
          :key="moto.id"
          :motorcycle="moto"
          @updated="refresh()"
        />
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.garage-page {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.page-header {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);

  @include sm-up {
    flex-direction: row;
    align-items: flex-end;
    justify-content: space-between;
  }
}

.page-title {
  font-size: var(--text-2xl);
  font-weight: var(--fw-bold);
  color: var(--color-text);
  line-height: var(--leading-tight);
}

.page-subtitle {
  margin-top: var(--space-1);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.garage-grid {
  gap: var(--space-4);

  @include sm-up {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }

  @include lg-up {
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  }
}

.skeleton-card {
  display: flex;
  flex-direction: column;
  height: 280px;
}
.skeleton-card__img {
  height: 160px;
}
.skeleton-card__content {
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.garage-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-8);
  text-align: center;
  color: var(--color-danger);
}
</style>
