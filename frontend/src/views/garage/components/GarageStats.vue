<template>
  <div v-if="motorcycles.length > 0" class="garage-stats">
    <div class="stat-chip">
      <i class="fa fa-motorcycle"></i>
      <span>{{ motorcycles.length }}</span>
      {{ declensionMotorcycles(motorcycles.length) }}
    </div>
    <div class="stat-chip">
      <i class="fa fa-wrench"></i>
      <span>{{ totalMaintenances }}</span>
      обслуживаний
    </div>
    <div class="stat-chip">
      <i class="fa fa-ruble-sign"></i>
      <span>{{ formatCost(totalCosts) }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { formatCost, declensionMotorcycles } from '@/utils/formatters'

defineProps<{
  motorcycles: any[]
  totalMaintenances: number
  totalCosts: number
}>()
</script>

<style scoped>
.garage-stats {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 24px;
}

.stat-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-full);
  font-size: 13px;
  color: var(--text-secondary);
  transition: all var(--transition-base);
}

.stat-chip:hover {
  border-color: var(--border-color);
  background: var(--bg-card-hover);
}

.stat-chip i {
  color: var(--accent-text);
  font-size: 14px;
}

.stat-chip span {
  font-weight: var(--fw-bold);
  color: var(--text-primary);
}

@media (max-width: 640px) {
  .garage-stats {
    gap: 6px;
  }

  .stat-chip {
    width: 100%;
    font-size: 12px;
    padding: 6px 12px;
  }
}
</style>
