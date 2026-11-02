<script setup lang="ts">
import type { Maintenance } from '~/types'

const props = defineProps<{ maintenances: Maintenance[] }>()

const stats = computed(() => {
  const planned = props.maintenances.filter(m => m.status === 'planned').length
  const completed = props.maintenances.filter(m => m.status === 'completed').length
  const totalCost = props.maintenances.reduce((sum, m) => sum + (m.cost || 0), 0)

  return {
    total: props.maintenances.length,
    planned,
    totalCost,
  }
})

const formatCost = (val: number) => {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', maximumFractionDigits: 0 }).format(val)
}
</script>

<template>
  <div class="m-stats">
    <BaseCard padding="md" class="stat-card">
      <span class="stat-label">Всего работ</span>
      <span class="stat-value">{{ stats.total }}</span>
    </BaseCard>
    <BaseCard padding="md" class="stat-card">
      <span class="stat-label">В плане</span>
      <span class="stat-value text-warning">{{ stats.planned }}</span>
    </BaseCard>
    <BaseCard padding="md" class="stat-card">
      <span class="stat-label">Потрачено</span>
      <span class="stat-value text-success">{{ formatCost(stats.totalCost) }}</span>
    </BaseCard>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.m-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: var(--space-3);
}

.stat-card {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.stat-label {
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-tertiary);
}

.stat-value {
  font-size: var(--text-xl);
  font-weight: var(--fw-bold);
  color: var(--color-text);
}

.text-warning { color: var(--color-warning); }
.text-success { color: var(--color-success); }
</style>
