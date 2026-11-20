<template>
  <div class="maintenances-section">
    <div class="section-header">
      <div class="section-header-left">
        <i class="fa fa-wrench"></i>
        <h4>Последние обслуживания</h4>
      </div>
      <button class="btn-link" @click="emit('view-all')">
        Все записи <i class="fa fa-arrow-right"></i>
      </button>
    </div>

    <div v-if="maintenances.length > 0" class="maintenances-list">
      <div
        v-for="item in maintenances"
        :key="item.id"
        class="maintenance-item"
        @click="emit('open', item)"
      >
        <div class="maint-icon" :class="'maint-icon-' + item.status">
          <i class="fa fa-wrench"></i>
        </div>

        <div class="maint-info">
          <div class="maint-title">{{ item.title }}</div>
          <div class="maint-meta">
            <span>{{ formatDate(item.completed_date || item.planned_date) }}</span>
            <span class="dot">•</span>
            <span>{{ item.completed_mileage || item.planned_mileage || '—' }} км</span>
            <span class="dot">•</span>
            <span>{{ item.cost ? formatCost(item.cost) : '—' }}</span>
          </div>
        </div>

        <div class="maint-status">
          <span :class="'badge badge-' + getStatusBadgeVariant(item.status)">
            {{ getStatusLabel(item.status) }}
          </span>
          <i class="fa fa-chevron-right"></i>
        </div>
      </div>
    </div>

    <div v-else class="empty-small">
      <i class="fa fa-wrench"></i>
      <p>Нет записей обслуживания</p>
      <span class="hint">Перейдите в раздел "Обслуживание" чтобы добавить</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { formatCost, getStatusLabel, getStatusBadgeVariant } from '@/utils/formatters'
import formatDate from '@/utils/DateFormatter.js'

defineProps<{ maintenances: any[] }>()

const emit = defineEmits<{
  open: [any]
  'view-all': []
}>()
</script>

<style scoped>
.maintenances-section {
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 20px 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.section-header-left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.section-header-left i {
  color: var(--accent-text);
  font-size: 18px;
}

.section-header h4 {
  font-size: 15px;
  font-weight: var(--fw-semibold);
  margin: 0;
}

.btn-link {
  background: none;
  border: none;
  color: var(--accent-text);
  font-weight: var(--fw-medium);
  font-size: 13px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all var(--transition-base);
  padding: 6px 12px;
  border-radius: var(--radius-md);
  min-height: 32px;
}

.btn-link:hover {
  color: var(--accent);
  gap: 10px;
  background: var(--accent-trans);
}

.maintenances-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.maintenance-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 16px;
  background: var(--bg-primary);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
  min-width: 0;
}

.maintenance-item:hover {
  background: var(--bg-card-hover);
  transform: translateX(4px);
}

.maint-icon {
  width: 36px;
  height: 36px;
  min-height: 36px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 14px;
}

.maint-icon-completed {
  background: var(--success-trans);
  color: var(--success-text);
}
.maint-icon-planned {
  background: var(--warning-trans);
  color: var(--warning-text);
}
.maint-icon-overdue {
  background: var(--danger-trans);
  color: var(--danger-text);
}

.maint-info {
  flex: 1;
  min-width: 0;
}

.maint-title {
  font-weight: var(--fw-medium);
  font-size: 13px;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.maint-meta {
  font-size: 12px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.maint-meta .dot {
  opacity: 0.3;
}

.maint-status {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.maint-status i {
  color: var(--text-muted);
  font-size: 12px;
  opacity: 0.5;
}

.badge {
  display: inline-block;
  padding: 3px 12px;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: var(--fw-medium);
  white-space: nowrap;
}

.badge-success {
  background: var(--success-trans);
  color: var(--success-text);
}
.badge-warning {
  background: var(--warning-trans);
  color: var(--warning-text);
}
.badge-danger {
  background: var(--danger-trans);
  color: var(--danger-text);
}
.badge-gray {
  background: rgba(107, 114, 128, 0.15);
  color: #9ca3af;
}

.empty-small {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32px 16px;
  text-align: center;
}

.empty-small i {
  font-size: 28px;
  color: var(--text-muted);
  margin-bottom: 8px;
  opacity: 0.4;
}

.empty-small p {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

.empty-small .hint {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 4px;
}

@media (max-width: 820px) {
  .maintenances-section {
    padding: 14px 16px;
  }

  .maintenance-item {
    padding: 10px 12px;
    gap: 10px;
  }

  .maint-icon {
    width: 32px;
    height: 32px;
    min-height: 32px;
    font-size: 12px;
  }

  .maint-title {
    font-size: 12px;
  }

  .maint-meta {
    font-size: 11px;
  }

  .maint-status i {
    display: none;
  }
}

@media (max-width: 480px) {
  .maintenance-item {
    flex-wrap: wrap;
  }

  .maint-info {
    flex-basis: calc(100% - 52px);
  }

  .maint-status {
    width: 100%;
    flex-basis: 100%;
    padding-top: 6px;
    border-top: 1px solid var(--border-light);
  }

  .badge {
    width: 100%;
    text-align: center;
  }
}
</style>
