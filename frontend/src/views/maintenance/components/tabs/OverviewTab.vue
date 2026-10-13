<template>
  <div class="overview">
    <!-- Сводка по мотоциклу -->
    <div v-if="motorcycle" class="overview__stats">
      <div class="ov-stat">
        <i class="fa fa-gauge-high" />
        <div>
          <span class="ov-stat__label">Пробег</span>
          <span class="ov-stat__value">{{ formatMileage(motorcycle.mileage) }}</span>
        </div>
      </div>
      <div class="ov-stat">
        <i class="fa fa-wrench" />
        <div>
          <span class="ov-stat__label">Обслуживаний</span>
          <span class="ov-stat__value">{{ motorcycle.maintenances?.length || 0 }}</span>
        </div>
      </div>
      <div class="ov-stat">
        <i class="fa fa-ruble-sign" />
        <div>
          <span class="ov-stat__label">Расходы на ТО</span>
          <span class="ov-stat__value">{{ formatCost(spends) }}</span>
        </div>
      </div>
    </div>

    <!-- Быстрые блоки -->
    <div class="overview__grid">
      <OverviewCard
        icon="fa fa-calendar-check"
        title="Ближайшие планы"
        action-label="Все планы"
        @action="emit('goto-tab', 'plans')"
      >
        <p v-if="plans.length === 0" class="ov-empty">Нет запланированных ТО</p>
        <ul v-else class="ov-list">
          <li v-for="p in plans.slice(0, 3)" :key="p.id" @click="emit('open', p)">
            <span class="ov-list__title">{{ p.title }}</span>
            <span class="ov-list__meta">{{ p.planned_mileage }} км</span>
          </li>
        </ul>
      </OverviewCard>

      <OverviewCard
        icon="fa fa-clock-rotate-left"
        title="Последние"
        action-label="Вся история"
        @action="emit('goto-tab', 'history')"
      >
        <p v-if="recent.length === 0" class="ov-empty">Нет записей</p>
        <ul v-else class="ov-list">
          <li v-for="m in recent.slice(0, 3)" :key="m.id" @click="emit('open', m)">
            <span class="ov-list__title">{{ m.title }}</span>
            <span class="ov-list__meta">{{ formatDate(m.completed_date) }}</span>
          </li>
        </ul>
      </OverviewCard>

      <OverviewCard
        icon="fa fa-book"
        title="Мануалы"
        action-label="Все мануалы"
        @action="emit('goto-tab', 'manuals')"
      >
        <p class="ov-empty">Откройте вкладку «Мануалы» для вашей модели</p>
      </OverviewCard>

      <OverviewCard
        icon="fa fa-stethoscope"
        title="Диагностика"
        action-label="Запустить"
        @action="emit('start-diagnostics')"
      >
        <p class="ov-empty">Не уверены, что с мотоциклом? Пройдите диагностику по симптомам.</p>
      </OverviewCard>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { formatMileage, formatCost } from '@/utils/formatters'
import formatDate from '@/utils/DateFormatter.js'
import OverviewCard from '../OverviewCard.vue'

const props = defineProps({
  motorcycle: { type: Object, default: null },
  allMaintenances: { type: Array, default: () => [] },
})

const emit = defineEmits(['open', 'goto-tab', 'start-diagnostics'])

const plans = computed(() =>
  (props.motorcycle?.maintenances || []).filter((m) => m.status === 'planned')
)

const recent = computed(() =>
  (props.motorcycle?.maintenances || [])
    .filter((m) => m.status === 'completed')
    .sort((a, b) => new Date(b.completed_date) - new Date(a.completed_date))
)

const spends = computed(() =>
  (props.motorcycle?.maintenances || [])
    .filter((m) => m.status === 'completed')
    .reduce((sum, m) => sum + (m.cost || 0), 0)
)
</script>

<style scoped>
.overview {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.overview__stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-3);
}

.ov-stat {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4);
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
}

.ov-stat i {
  font-size: var(--text-xl);
  color: var(--accent-text);
  flex-shrink: 0;
}

.ov-stat__label {
  display: block;
  font-size: var(--text-xs);
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.4px;
  font-weight: var(--fw-semibold);
}

.ov-stat__value {
  display: block;
  font-size: var(--text-lg);
  font-weight: var(--fw-bold);
  color: var(--text-primary);
}

.overview__grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-3);
}

.ov-empty {
  font-size: var(--text-sm);
  color: var(--text-muted);
  margin: 0;
  font-style: italic;
}

.ov-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.ov-list li {
  display: flex;
  justify-content: space-between;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  background: var(--bg-primary);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background var(--transition-fast);
  font-size: var(--text-sm);
}

.ov-list li:hover {
  background: var(--bg-card-hover);
}

.ov-list__title {
  color: var(--text-primary);
  font-weight: var(--fw-medium);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ov-list__meta {
  color: var(--text-muted);
  flex-shrink: 0;
  font-size: var(--text-xs);
}

@media (max-width: 820px) {
  .overview__stats { grid-template-columns: 1fr; }
  .overview__grid { grid-template-columns: 1fr; }
}
</style>
