<script setup lang="ts">
import type { Maintenance } from '~/types'

const props = defineProps<{ maintenance: Maintenance }>()
const emit = defineEmits<{ complete: []; delete: [] }>()

const formatDate = (isoStr?: string | null) => {
  if (!isoStr) return ''
  return new Date(isoStr).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short', year: 'numeric' })
}

const formatMileage = (val?: number | null) => {
  if (!val) return ''
  return new Intl.NumberFormat('ru-RU').format(val) + ' км'
}

const isPlanned = computed(() => props.maintenance.status === 'planned')
</script>

<template>
  <div class="m-item" :class="{ 'm-item--planned': isPlanned }">
    <div class="m-item__status-bar" />

    <div class="m-item__content">
      <div class="m-item__header">
        <h4 class="m-item__title">{{ maintenance.title }}</h4>
        <div v-if="!isPlanned && maintenance.cost" class="m-item__cost">
          {{ new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', maximumFractionDigits: 0 }).format(maintenance.cost) }}
        </div>
      </div>

      <p v-if="maintenance.description" class="m-item__desc">{{ maintenance.description }}</p>

      <div class="m-item__meta">
        <!-- Для плана -->
        <template v-if="isPlanned">
          <span v-if="maintenance.planned_date" class="meta-badge">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            {{ formatDate(maintenance.planned_date) }}
          </span>
          <span v-if="maintenance.planned_mileage" class="meta-badge">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/></svg>
            {{ formatMileage(maintenance.planned_mileage) }}
          </span>
        </template>

        <!-- Для выполненного -->
        <template v-else>
          <span v-if="maintenance.completed_date" class="meta-badge">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
            {{ formatDate(maintenance.completed_date) }}
          </span>
          <span v-if="maintenance.completed_mileage" class="meta-badge">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/></svg>
            {{ formatMileage(maintenance.completed_mileage) }}
          </span>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.m-item {
  display: flex;
  align-items: stretch;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
  transition: box-shadow var(--transition-fast);

  &:hover {
    box-shadow: var(--shadow-sm);
  }
}

.m-item__status-bar {
  width: 4px;
  background: var(--color-success);
  flex-shrink: 0;
}

.m-item--planned .m-item__status-bar {
  background: var(--color-warning);
}

.m-item__content {
  flex: 1;
  padding: var(--space-3) var(--space-4);
  min-width: 0;
}

.m-item__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-2);
  margin-bottom: var(--space-1);
}

.m-item__title {
  font-size: var(--text-base);
  font-weight: var(--fw-semibold);
  color: var(--color-text);
}

.m-item__cost {
  font-weight: var(--fw-bold);
  color: var(--color-text);
  white-space: nowrap;
}

.m-item__desc {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-2);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.m-item__meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
}

.meta-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.m-item__actions {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-2) var(--space-3);
  background: var(--color-surface-secondary);
  border-left: 1px solid var(--color-border-light);

  @include sm-down {
    flex-direction: column;
    justify-content: center;
  }
}
</style>
