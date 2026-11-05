<script setup lang="ts">
import type { MotorcycleHealth, ComponentHealthItem } from '~/types'

const props = defineProps<{
  health: MotorcycleHealth | null
  loading?: boolean
}>()

const emit = defineEmits<{ 'open-components': [] }>()

const statusLabel: Record<string, string> = {
  ok: 'В норме',
  due_soon: 'Скоро',
  overdue: 'Просрочено',
  unknown: 'Нет данных',
}

function remainingText(item: ComponentHealthItem): string {
  const parts: string[] = []
  if (item.remaining_km !== null) {
    const v = item.remaining_km
    parts.push(v >= 0 ? `~${v.toLocaleString('ru-RU')} км` : `просрочено на ${Math.abs(v).toLocaleString('ru-RU')} км`)
  }
  if (item.remaining_days !== null) {
    const d = item.remaining_days
    parts.push(d >= 0 ? `~${d} дн.` : `просрочено на ${Math.abs(d)} дн.`)
  }
  return parts.length ? parts.join(' / ') : '—'
}
</script>

<template>
  <BaseCard padding="lg" class="health-card">
    <div class="hc-header">
      <div>
        <h2 class="hc-title">Состояние компонентов</h2>
        <p class="hc-subtitle">
          Ориентировочная оценка. Не подтверждает техническую исправность.
        </p>
      </div>
      <BaseButton variant="ghost" size="sm" @click="emit('open-components')">
        Все компоненты <i class="fa-solid fa-arrow-right"></i>
      </BaseButton>
    </div>

    <div v-if="loading" class="hc-skeleton">
      <BaseSkeleton height="80px" rounded />
    </div>

    <div v-else-if="!health || health.counts.total === 0" class="hc-empty">
      Компоненты не добавлены. Создайте базовый набор на вкладке «Компоненты».
    </div>

    <template v-else>
      <!-- Общая оценка -->
      <div class="hc-overall">
        <div class="hc-percent">
          <template v-if="health.overall.percent !== null">
            <span class="hc-percent-value">{{ health.overall.percent }}%</span>
            <span class="hc-percent-label">{{ health.overall.label }}</span>
          </template>
          <template v-else>
            <span class="hc-percent-value hc-percent-value--muted">—</span>
            <span class="hc-percent-label">недостаточно данных</span>
          </template>
        </div>
        <div class="hc-counts">
          <div class="hc-count hc-count--ok">
            <span>{{ health.counts.ok }}</span>
            <small>в норме</small>
          </div>
          <div class="hc-count hc-count--soon">
            <span>{{ health.counts.due_soon }}</span>
            <small>скоро</small>
          </div>
          <div class="hc-count hc-count--overdue">
            <span>{{ health.counts.overdue }}</span>
            <small>просрочено</small>
          </div>
          <div class="hc-count hc-count--unknown">
            <span>{{ health.counts.unknown }}</span>
            <small>нет данных</small>
          </div>
        </div>
      </div>

      <!-- Безопасность — отдельно -->
      <div v-if="health.safety_attention.length > 0" class="hc-safety">
        <div class="hc-safety-title">
          <i class="fa-solid fa-triangle-exclamation"></i>
          Требует внимания: безопасность
        </div>
        <ul class="hc-list">
          <li v-for="i in health.safety_attention" :key="i.id" class="hc-list-item">
            <span class="hc-item-name">{{ i.name }}</span>
            <BaseBadge variant="danger" size="sm">
              {{ statusLabel[i.status] }}
            </BaseBadge>
            <span class="hc-item-remaining">{{ remainingText(i) }}</span>
          </li>
        </ul>
      </div>

      <!-- Прочее внимание -->
      <div v-if="health.attention.length > 0" class="hc-attention">
        <div class="hc-section-title">Требует внимания</div>
        <ul class="hc-list">
          <li v-for="i in health.attention.slice(0, 5)" :key="i.id" class="hc-list-item">
            <span class="hc-item-name">{{ i.name }}</span>
            <BaseBadge :variant="i.status === 'overdue' ? 'danger' : 'warning'" size="sm">
              {{ statusLabel[i.status] }}
            </BaseBadge>
            <span class="hc-item-remaining">{{ remainingText(i) }}</span>
          </li>
        </ul>
      </div>

      <!-- Предстоящее -->
      <div v-if="health.upcoming.length > 0" class="hc-upcoming">
        <div class="hc-section-title">Предстоящее обслуживание</div>
        <ul class="hc-list">
          <li v-for="i in health.upcoming.slice(0, 5)" :key="i.id" class="hc-list-item">
            <span class="hc-item-name">{{ i.name }}</span>
            <span class="hc-item-remaining">{{ remainingText(i) }}</span>
          </li>
        </ul>
      </div>

      <!-- Без данных -->
      <div v-if="health.no_data.length > 0" class="hc-nodata">
        <span class="hc-nodata-title">Без данных для оценки:</span>
        <span class="hc-nodata-list">
          {{ health.no_data.map((i) => i.name).join(', ') }}
        </span>
      </div>
    </template>
  </BaseCard>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.health-card {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.hc-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.hc-title {
  font-size: var(--text-lg);
  font-weight: var(--fw-semibold);
}

.hc-subtitle {
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
  margin-top: var(--space-1);
}

.hc-skeleton,
.hc-empty {
  color: var(--color-text-tertiary);
  font-size: var(--text-sm);
}

.hc-overall {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-3);

  @include sm-up {
    grid-template-columns: auto 1fr;
    align-items: center;
  }
}

.hc-percent {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: var(--space-3);
  background: var(--color-surface-secondary);
  border-radius: var(--radius-md);
  min-width: 160px;
}

.hc-percent-value {
  font-size: var(--text-2xl);
  font-weight: var(--fw-bold);
  color: var(--color-brand);
}

.hc-percent-value--muted {
  color: var(--color-text-tertiary);
}

.hc-percent-label {
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
}

.hc-counts {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-2);
}

.hc-count {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--space-2);
  border-radius: var(--radius-md);
  background: var(--color-surface-secondary);

  span {
    font-weight: var(--fw-bold);
  }

  small {
    font-size: 10px;
    color: var(--color-text-tertiary);
  }
}

.hc-count--ok span { color: var(--color-success, #22c55e); }
.hc-count--soon span { color: var(--color-warning, #f59e0b); }
.hc-count--overdue span { color: var(--color-danger, #ef4444); }
.hc-count--unknown span { color: var(--color-text-tertiary); }

.hc-section-title,
.hc-safety-title {
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  margin-bottom: var(--space-2);
}

.hc-safety {
  padding: var(--space-3);
  border: 1px solid var(--color-danger);
  border-radius: var(--radius-md);
  background: var(--color-danger-soft, rgba(239, 68, 68, 0.08));
}

.hc-safety-title {
  color: var(--color-danger);
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.hc-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.hc-list-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
}

.hc-item-name {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.hc-item-remaining {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
}

.hc-nodata {
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-1);
}

.hc-nodata-title {
  font-weight: var(--fw-semibold);
}
</style>
