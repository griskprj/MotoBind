<template>
  <article class="maint-row" @click="emit('click', item)">
    <div class="maint-row__icon" :class="`maint-row__icon--${item.status}`">
      <i class="fa fa-wrench" />
    </div>

    <div class="maint-row__body">
      <h4 class="maint-row__title">{{ item.title }}</h4>
      <p class="maint-row__meta">
        <span>
          <i class="fa fa-calendar" />
          {{ formatDate(item.completed_date || item.planned_date) }}
        </span>
        <span class="maint-row__dot">•</span>
        <span>
          <i class="fa fa-gauge-high" />
          {{ item.completed_mileage || item.planned_mileage || '—' }} км
        </span>
        <span v-if="item.cost" class="maint-row__dot">•</span>
        <span v-if="item.cost">
          <i class="fa fa-ruble-sign" />
          {{ formatCost(item.cost) }}
        </span>
      </p>
    </div>

    <div class="maint-row__status">
      <span :class="`badge badge--${badgeVariant(item.status)}`">
        {{ statusLabel(item.status) }}
      </span>
      <i class="fa fa-chevron-right" />
    </div>
  </article>
</template>

<script setup>
import { formatCost } from '@/utils/formatters'
import formatDate from '@/utils/DateFormatter.js'

defineProps({
  item: { type: Object, required: true },
})

const emit = defineEmits(['click'])

function statusLabel(status) {
  return {
    completed: 'Выполнено',
    planned: 'Запланировано',
    overdue: 'Просрочено',
  }[status] || status
}

function badgeVariant(status) {
  return {
    completed: 'success',
    planned: 'warning',
    overdue: 'danger',
  }[status] || 'gray'
}
</script>

<style scoped>
.maint-row {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.maint-row:hover {
  background: var(--bg-card-hover);
  border-color: var(--border-color);
  transform: translateX(2px);
}

.maint-row__icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: var(--text-base);
}

.maint-row__icon--completed { background: var(--success-trans); color: var(--success-text); }
.maint-row__icon--planned { background: var(--warning-trans); color: var(--warning-text); }
.maint-row__icon--overdue { background: var(--danger-trans); color: var(--danger-text); }

.maint-row__body {
  flex: 1;
  min-width: 0;
}

.maint-row__title {
  margin: 0 0 2px;
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.maint-row__meta {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  margin: 0;
  font-size: var(--text-xs);
  color: var(--text-muted);
  flex-wrap: wrap;
}

.maint-row__meta i {
  margin-right: 3px;
}

.maint-row__dot {
  opacity: 0.4;
  margin: 0 4px;
}

.maint-row__status {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  flex-shrink: 0;
}

.maint-row__status > i {
  color: var(--text-muted);
  font-size: var(--text-xs);
  opacity: 0.5;
}

.badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: var(--fw-medium);
  white-space: nowrap;
}

.badge--success { background: var(--success-trans); color: var(--success-text); }
.badge--warning { background: var(--warning-trans); color: var(--warning-text); }
.badge--danger { background: var(--danger-trans); color: var(--danger-text); }
.badge--gray { background: var(--border-light); color: var(--text-muted); }

@media (max-width: 640px) {
  .maint-row__status > i { display: none; }
  .maint-row__meta { font-size: 11px; }
}
</style>
