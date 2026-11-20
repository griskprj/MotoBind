<script setup lang="ts">
import type { Motorcycle, Maintenance } from '~/types'

const api = useApi()

const { data: motorcycles, pending } = await useAsyncData(
  'garage-stats',
  () => api.motorcycle.list(),
  { default: () => [] }
)

const motorcyclesCount = computed(() => motorcycles.value?.length || 0)

const plannedMaintenances = computed(() => {
  if (!motorcycles.value) return []
  const list: Array<Maintenance & { motorcycle: Motorcycle }> = []
  for (const moto of motorcycles.value) {
    for (const m of moto.maintenances || []) {
      if (m.status === 'planned') {
        list.push({ ...m, motorcycle: moto })
      }
    }
  }
  return list
})

const nearestMaintenance = computed(() => {
  const planned = plannedMaintenances.value
  if (planned.length === 0) return null

  const withRemaining = planned
    .map(m => {
      const motoMileage = m.motorcycle.mileage
      const plannedMileage = m.planned_mileage

      if (plannedMileage == null || motoMileage == null) return null

      const remaining = plannedMileage - motoMileage

      return {
        maintenance: m,
        remaining,
        isOverdue: remaining <= 0,
      }
    })
    .filter(Boolean) as Array<{ maintenance: any; remaining: number; isOverdue: boolean }>

  if (withRemaining.length === 0) return null

  withRemaining.sort((a, b) => {
    if (a.isOverdue && !b.isOverdue) return 1
    if (!a.isOverdue && b.isOverdue) return -1
    if (!a.isOverdue && !b.isOverdue) return a.remaining - b.remaining
    return b.remaining - a.remaining
  })

  return withRemaining[0]
})

const totalMileage = computed(() => {
  if (!motorcycles.value) return 0
  return motorcycles.value.reduce((sum, moto) => sum + (moto.mileage || 0), 0)
})

const formatNumber = (val: number) => {
  return new Intl.NumberFormat('ru-RU').format(val)
}

const formatDate = (iso?: string | null) => {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short', year: 'numeric' })
}

const nearestText = computed(() => {
  const data = nearestMaintenance.value
  if (!data) return '—'
  const { remaining, isOverdue, maintenance } = data
  if (isOverdue) {
    return `просрочено на ${formatNumber(Math.abs(remaining))} км`
  }
  return `через ${formatNumber(remaining)} км`
})
</script>

<template>
  <div class="cards-grid" :class="{ 'cards-grid--loading': pending }">
    <!-- Мотоциклы -->
    <BaseCard class="card">
      <div class="icon">
        <i class="fa fa-motorcycle"></i>
      </div>
      <div class="info">
        <p class="value">{{ motorcyclesCount }}</p>
        <p class="description">мотоциклов</p>
      </div>
    </BaseCard>

    <!-- Задачи по ТО -->
    <BaseCard class="card">
      <div class="icon warning">
        <i class="fa fa-wrench"></i>
      </div>
      <div class="info">
        <p class="value">{{ plannedMaintenances.length }}</p>
        <p class="description">задачи по ТО</p>
      </div>
    </BaseCard>

    <!-- Ближайшее ТО -->
    <BaseCard class="card">
      <div class="icon">
        <i class="fa fa-calendar"></i>
      </div>
      <div class="info">
        <p class="value">{{ nearestText }}</p>
        <p class="description">ближайшее ТО</p>
      </div>
    </BaseCard>

    <!-- Общий пробег -->
    <BaseCard class="card">
      <div class="icon brand">
        <i class="fa fa-tachometer"></i>
      </div>
      <div class="info">
        <p class="value">{{ formatNumber(totalMileage) }}</p>
        <p class="description">общий пробег (км)</p>
      </div>
    </BaseCard>
  </div>
</template>

<style lang="scss" scoped>
.cards-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-4);
  transition: opacity var(--transition-fast);
}

.cards-grid--loading {
  opacity: 0.5;
}

.card {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background-color: var(--color-bg-secondary);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: 20px;
  flex-shrink: 0;
}

.icon.warning {
  color: var(--color-warning);
  background-color: var(--color-warning-soft);
}

.icon.brand {
  color: var(--color-brand);
  background-color: var(--color-brand-soft);
}

.value {
  font-weight: var(--fw-semibold);
  font-size: var(--text-2xl);
  line-height: 1.2;
}

.description {
  font-weight: var(--fw-medium);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

/* Адаптив */
@media (max-width: 1200px) {
  .cards-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 440px) {
  .cards-grid {
    grid-template-columns: 1fr;
  }

  .card {
    padding: var(--space-2);
  }
}
</style>
