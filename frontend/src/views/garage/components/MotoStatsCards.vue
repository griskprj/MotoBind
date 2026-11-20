<template>
  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-icon">
        <i class="fa-solid fa-gauge-high"></i>
      </div>
      <div class="stat-info">
        <span class="stat-label">Пробег</span>
        <span class="stat-value">{{ formatMileage(moto.mileage) }}</span>
      </div>
    </div>

    <div class="stat-card">
      <div class="stat-icon">
        <i class="fa fa-wrench"></i>
      </div>
      <div class="stat-info">
        <span class="stat-label">Обслуживаний</span>
        <span class="stat-value">{{ moto.maintenances?.length || 0 }}</span>
      </div>
    </div>

    <div class="stat-card" :class="{ 'stat-warning': nextMaintenance?.isOverdue }">
      <div class="stat-icon">
        <i class="fa fa-calendar-check"></i>
      </div>
      <div class="stat-info">
        <span class="stat-label">Следующее ТО</span>
        <span class="stat-value">
          <template v-if="nextMaintenance">
            <span v-if="nextMaintenance.isOverdue" class="text-danger">
              <i class="fa fa-exclamation-triangle"></i>
              {{ Math.round(nextMaintenance.distanceOverdue) }} км просрочено
            </span>
            <span v-else>
              через {{ Math.round(nextMaintenance.distanceToNext) }} км
            </span>
          </template>
          <span v-else class="text-muted">Все выполнены</span>
        </span>
      </div>
    </div>

    <div class="stat-card">
      <div class="stat-icon">
        <i class="fa fa-ruble-sign"></i>
      </div>
      <div class="stat-info">
        <span class="stat-label">Расходы на ТО</span>
        <span class="stat-value">{{ formatCost(maintenanceSpends) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { formatMileage, formatCost } from '@/utils/formatters'

defineProps<{
  moto: any
  nextMaintenance: any
  maintenanceSpends: number
}>()
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px 20px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  transition: all var(--transition-base);
  min-width: 0;
}

.stat-card:hover {
  border-color: var(--border-color);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.stat-card.stat-warning {
  border-color: var(--danger-trans);
  background: var(--danger-trans);
}

.stat-icon {
  width: 44px;
  height: 44px;
  min-height: 44px;
  border-radius: var(--radius-md);
  background: var(--accent-trans);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: var(--accent-text);
  flex-shrink: 0;
}

.stat-warning .stat-icon {
  background: var(--danger-trans);
  color: var(--danger-text);
}

.stat-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.stat-label {
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.4px;
  font-weight: var(--fw-semibold);
}

.stat-value {
  font-size: 18px;
  font-weight: var(--fw-bold);
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
}

.stat-value.text-danger {
  color: var(--danger);
}

.stat-value .text-muted {
  font-size: 13px;
  font-weight: var(--fw-normal);
  color: var(--text-muted);
}

@media (max-width: 1680px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(1, 1fr);
  }
}

@media (max-width: 1100px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 820px) {
  .stats-grid {
    grid-template-columns: repeat(1, 1fr);
  }
}

@media (max-width: 640px) {

  .stat-card {
    padding: 12px 14px;
    gap: 10px;
  }

  .stat-icon {
    width: 36px;
    height: 36px;
    min-height: 36px;
    font-size: 15px;
  }

  .stat-value {
    font-size: 15px;
  }
}

@media (max-width: 400px) {
  .stat-card {
    padding: 10px 12px;
  }
}
</style>
