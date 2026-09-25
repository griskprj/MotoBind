<template>
  <BaseModal
    :is-open="isOpen"
    :title="maintenance?.title || 'Детали обслуживания'"
    :subtitle="motorcycle?.name || ''"
    icon="wrench"
    variant="default"
    size="md"
    @close="$emit('close')"
  >
    <!-- Статус и дата -->
    <div class="maintenance-meta">
      <BaseBadge :variant="statusBadgeVariant" dot>
        {{ statusLabel }}
      </BaseBadge>
      <span
        v-if="maintenance?.completed_date || maintenance?.planned_date"
        class="meta-date"
      >
        <i class="fa fa-calendar"></i>
        {{ formatDate(maintenance.completed_date || maintenance.planned_date) }}
      </span>
    </div>

    <!-- Описание -->
    <p v-if="maintenance?.description" class="maintenance-description">
      <i class="fa fa-message"></i>
      {{ maintenance.description }}
    </p>

    <!-- Детали -->
    <div class="details-card">
      <div class="details-title">
        <i class="fa fa-receipt"></i>
        Детали обслуживания
      </div>
      <div class="details-list">
        <div
          v-if="maintenance?.completed_date || maintenance?.planned_date"
          class="detail-item"
        >
          <span class="detail-label">
            <i class="fa fa-calendar"></i> Дата
          </span>
          <span class="detail-value">
            {{ formatDate(maintenance.completed_date || maintenance.planned_date) }}
          </span>
        </div>

        <div v-if="maintenance?.completed_mileage" class="detail-item">
          <span class="detail-label">
            <i class="fa fa-gauge-high"></i> Пробег выполнения
          </span>
          <span class="detail-value">
            {{ maintenance.completed_mileage }} <span class="unit">км</span>
          </span>
        </div>

        <div v-if="maintenance?.planned_mileage" class="detail-item">
          <span class="detail-label">
            <i class="fa fa-clock"></i> Плановый пробег
          </span>
          <span class="detail-value">
            {{ maintenance.planned_mileage }} <span class="unit">км</span>
          </span>
        </div>

        <div v-if="maintenance?.cost" class="detail-item">
          <span class="detail-label">
            <i class="fa fa-ruble-sign"></i> Стоимость
          </span>
          <span class="detail-value">
            {{ maintenance.cost }} <span class="unit">₽</span>
          </span>
        </div>

        <div v-if="maintenance?.category" class="detail-item">
          <span class="detail-label">
            <i class="fa fa-tags"></i> Категория
          </span>
          <span class="detail-value">
            <span class="category-tag">{{ getCategoryLabel(maintenance.category) }}</span>
          </span>
        </div>
      </div>
    </div>

    <template #actions>
      <div class="modal-actions">
        <BaseButton
          v-if="maintenance?.status !== 'completed'"
          variant="success"
          icon="fa fa-check"
          block
          @click="$emit('mark')"
        >
          Завершить
        </BaseButton>
        <div class="modal-actions-group">
          <BaseButton
            variant="warning"
            icon="fa fa-pen"
            block
            @click="$emit('edit')"
          >
            Редактировать
          </BaseButton>
          <BaseButton
            variant="danger"
            icon="fa fa-trash"
            block
            @click="$emit('delete')"
          >
            Удалить
          </BaseButton>
        </div>
        <BaseButton
          variant="secondary"
          icon="fa fa-times"
          block
          @click="$emit('close')"
        >
          Закрыть
        </BaseButton>
      </div>
    </template>
  </BaseModal>
</template>

<script setup>
import { computed } from 'vue'
import { BaseModal, BaseButton, BaseBadge } from '@/components/ui'
import { getCategoryLabel, getStatusLabel } from '@/utils/formatters'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  motorcycle: { type: Object, default: null },
  maintenance: { type: Object, default: null },
})

defineEmits(['close', 'edit', 'delete', 'mark'])

const statusLabel = computed(() => getStatusLabel(props.maintenance?.status))

const statusBadgeVariant = computed(() => {
  return {
    completed: 'success',
    planned: 'warning',
    overdue: 'danger',
  }[props.maintenance?.status] || 'gray'
})

function formatDate(dateString) {
  if (!dateString) return '—'
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) return '—'
    return date.toLocaleDateString('ru-RU', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    })
  } catch {
    return '—'
  }
}
</script>

<style scoped>
.maintenance-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.meta-date {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--text-muted);
  padding: 4px 12px;
  background: var(--bg-secondary);
  border-radius: 50px;
}

.meta-date i { font-size: 13px; }

.maintenance-description {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0 0 16px 0;
  line-height: 1.6;
  padding: 12px 16px;
  background: var(--bg-secondary);
  border-radius: 10px;
  border-left: 3px solid var(--accent);
}

.maintenance-description i {
  margin-top: 2px;
  color: var(--accent-text);
  flex-shrink: 0;
}

.details-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 16px 18px;
}

.details-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 700;
  color: var(--text-muted);
  margin-bottom: 12px;
  letter-spacing: 0.8px;
  text-transform: uppercase;
}

.details-title i { font-size: 14px; color: var(--accent-text); }

.details-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  background: var(--bg-card);
  border-radius: 8px;
  transition: background 0.2s;
}

.detail-item:hover { background: var(--bg-card-hover); }

.detail-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-muted);
}

.detail-label i {
  font-size: 14px;
  color: var(--accent-text);
  width: 18px;
  text-align: center;
}

.detail-value {
  display: flex;
  align-items: baseline;
  gap: 2px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.unit {
  font-size: 11px;
  font-weight: 400;
  color: var(--text-muted);
  margin-left: 2px;
}

.category-tag {
  display: inline-block;
  padding: 2px 12px;
  border-radius: 50px;
  font-size: 12px;
  font-weight: 500;
  background: var(--accent-trans);
  color: var(--accent-text);
}

.modal-actions {
  display: flex;
  gap: 10px;
}

.modal-actions > * { flex: 1; }

.modal-actions-group {
  display: flex;
  gap: 8px;
}

.modal-actions-group > * { flex: 1; }

@media (max-width: 640px) {
  .maintenance-meta {
    flex-direction: column;
    align-items: flex-start;
  }

  .detail-item {
    flex-wrap: wrap;
    gap: 4px;
  }

  .detail-value {
    width: 100%;
    padding-left: 26px;
  }

  .modal-actions {
    flex-direction: column-reverse;
  }

  .modal-actions-group {
    flex-direction: column;
  }

  .maintenance-description {
    font-size: 13px;
    padding: 10px 14px;
  }
}
</style>
