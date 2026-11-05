<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import type { Motorcycle, Maintenance, MotorcycleHealth } from '~/types'
import MotorcycleHealthCard from './MotorcycleHealthCard.vue'

const props = defineProps<{
  motorcycle: Motorcycle
}>()

const emit = defineEmits<{ updated: []; 'open-components': [] }>()

const api = useApi()
const router = useRouter()
const mediaUrl = useMediaUrl()

const health = ref<MotorcycleHealth | null>(null)
const healthLoading = ref(false)

async function loadHealth() {
  if (!props.motorcycle?.id) return
  healthLoading.value = true
  try {
    health.value = await api.motorcycle.health(props.motorcycle.id)
  } catch {
    health.value = null
  } finally {
    healthLoading.value = false
  }
}

onMounted(loadHealth)

const currentMileage = computed(() => props.motorcycle.mileage || 0)

const plannedMaintenances = computed(() => {
  return (props.motorcycle.maintenances || [])
    .filter(m => m.status === 'planned')
    .sort((a, b) => {
      if (a.planned_mileage && b.planned_mileage) return a.planned_mileage - b.planned_mileage
      return 0
    })
})

const nextMaintenance = computed(() => {
  const withMileage = plannedMaintenances.value.filter(m => m.planned_mileage != null)
  if (withMileage.length === 0) return null

  const withRemaining = withMileage
    .map(m => ({
      maintenance: m,
      remaining: (m.planned_mileage || 0) - currentMileage.value,
    }))
    .filter(item => item.remaining > 0)
    .sort((a, b) => a.remaining - b.remaining)

  if (withRemaining.length > 0) {
    return { maintenance: withRemaining[0].maintenance, remaining: withRemaining[0].remaining }
  }

  const overdue = withMileage
    .map(m => ({
      maintenance: m,
      remaining: (m.planned_mileage || 0) - currentMileage.value,
    }))
    .sort((a, b) => b.remaining - a.remaining)

  if (overdue.length > 0) {
    return { maintenance: overdue[0].maintenance, remaining: overdue[0].remaining, isOverdue: true }
  }

  return null
})

const lastMaintenance = computed(() => {
  const completed = (props.motorcycle.maintenances || [])
    .filter(m => m.status === 'completed')
    .sort((a, b) => {
      if (a.completed_mileage && b.completed_mileage) return b.completed_mileage - a.completed_mileage
      return 0
    })
  return completed.length > 0 ? completed[0] : null
})

const maintenanceStats = computed(() => {
  const all = props.motorcycle.maintenances || []
  const completed = all.filter(m => m.status === 'completed').length
  const total = all.length
  const percent = total > 0 ? Math.round((completed / total) * 100) : 0
  return { completed, total, percent }
})

const formatNumber = (val: number) => {
  return new Intl.NumberFormat('ru-RU').format(val)
}

const nextMaintenanceText = computed(() => {
  const data = nextMaintenance.value
  if (!data) return '—'
  if (data.isOverdue) {
    return `просрочено на ${formatNumber(Math.abs(data.remaining))} км`
  }
  return `через ${formatNumber(data.remaining)} км`
})

const lastMaintenanceText = computed(() => {
  const m = lastMaintenance.value
  if (!m) return '—'
  if (m.completed_mileage) return `${formatNumber(m.completed_mileage)} км`
  if (m.completed_date) return new Date(m.completed_date).toLocaleDateString('ru-RU')
  return '—'
})

// Ссылки для быстрых действий
const maintenanceLink = computed(() => `/garage/${props.motorcycle.id}`)
const diagnosticsLink = computed(() => `/garage/${props.motorcycle.id}#diagnostics`)
const manualsLink = computed(() => `/manuals?motorcycle=${encodeURIComponent(props.motorcycle.name)}`)
const historyLink = computed(() => `/garage/${props.motorcycle.id}#history`)
</script>

<template>
  <div class="overview">
    <!-- Здоровье мотоцикла -->
    <MotorcycleHealthCard
      :health="health"
      :loading="healthLoading"
      @open-components="emit('open-components')"
    />

    <!-- Статистика -->
    <div class="stats-grid">
      <BaseCard padding="md" class="stat-card">
        <i class="fa-solid fa-gauge-high stat-icon"></i>
        <div>
          <span class="stat-label">Пробег</span>
          <span class="stat-value">{{ formatNumber(currentMileage) }} км</span>
        </div>
      </BaseCard>
      <BaseCard padding="md" class="stat-card">
        <i class="fa-solid fa-calendar stat-icon"></i>
        <div>
          <span class="stat-label">Следующее ТО</span>
          <span class="stat-value">{{ nextMaintenanceText }}</span>
        </div>
      </BaseCard>
      <BaseCard padding="md" class="stat-card">
        <i class="fa-solid fa-wrench stat-icon"></i>
        <div>
          <span class="stat-label">Последнее ТО</span>
          <span class="stat-value">{{ lastMaintenanceText }}</span>
        </div>
      </BaseCard>
      <BaseCard padding="md" class="stat-card">
        <div class="progress-wrap">
          <span class="stat-label">Состояние обслуживания</span>
          <span class="stat-value">{{ maintenanceStats.completed }} из {{ maintenanceStats.total }} задач</span>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: `${maintenanceStats.percent}%` }" />
          </div>
        </div>
      </BaseCard>
    </div>

    <!-- Ближайшие работы -->
    <BaseCard padding="lg">
      <div class="section-header">
        <h2 class="section-title">Ближайшие работы</h2>
        <NuxtLink to="#history" class="link">Все задачи →</NuxtLink>
      </div>
      <div v-if="plannedMaintenances.length === 0" class="empty">Нет запланированных работ.</div>
      <ul v-else class="work-list">
        <li v-for="m in plannedMaintenances" :key="m.id" class="work-item">
          <span class="work-title">{{ m.title }}</span>
          <span class="work-mileage">{{ m.planned_mileage ? `${formatNumber(m.planned_mileage)} км` : '' }}</span>
        </li>
      </ul>
    </BaseCard>

    <!-- О мотоцикле -->
    <BaseCard padding="lg">
      <h2 class="section-title">О мотоцикле</h2>
      <div class="specs-list">
        <div class="spec-row"><span>Модель:</span> <strong>{{ motorcycle.name }}</strong></div>
        <div class="spec-row"><span>Год выпуска:</span> <strong>{{ motorcycle.years || '—' }}</strong></div>
        <div class="spec-row"><span>Объём двигателя:</span> <strong>{{ motorcycle.volume ? `${motorcycle.volume} см³` : '—' }}</strong></div>
        <div class="spec-row"><span>Госномер:</span> <strong>{{ motorcycle.license_plate || '—' }}</strong></div>
        <div class="spec-row"><span>VIN:</span> <strong>{{ motorcycle.vin || '—' }}</strong></div>
        <div class="spec-row"><span>Цвет:</span> <strong>{{ motorcycle.color || '—' }}</strong></div>
      </div>
    </BaseCard>

    <!-- Последние работы -->
    <BaseCard padding="lg">
      <div class="section-header">
        <h2 class="section-title">Последние работы</h2>
        <NuxtLink to="#history" class="link">Все работы →</NuxtLink>
      </div>
      <div v-if="!motorcycle.maintenances || motorcycle.maintenances.filter(m => m.status === 'completed').length === 0" class="empty">
        Нет выполненных работ.
      </div>
      <ul v-else class="history-list">
        <li v-for="m in (motorcycle.maintenances || []).filter(m => m.status === 'completed').slice(0, 3)" :key="m.id" class="history-item">
          <div class="history-title">{{ m.title }}</div>
          <div class="history-meta">
            <span>{{ m.completed_date ? new Date(m.completed_date).toLocaleDateString('ru-RU') : '' }}</span>
            <span v-if="m.completed_mileage">{{ formatNumber(m.completed_mileage) }} км</span>
          </div>
        </li>
      </ul>
    </BaseCard>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.overview {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

/* Статистика */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-3);
}

.stat-card {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.stat-icon {
  font-size: 24px;
  color: var(--color-brand);
}

.stat-label {
  display: block;
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
  text-transform: uppercase;
}

.stat-value {
  display: block;
  font-size: var(--text-lg);
  font-weight: var(--fw-semibold);
  color: var(--color-text);
}

.progress-wrap {
  flex: 1;
}

.progress-bar {
  margin-top: var(--space-2);
  height: 6px;
  background: var(--color-surface-secondary);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--color-brand);
  border-radius: var(--radius-full);
}

/* Ближайшие работы */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-3);
}

.section-title {
  font-size: var(--text-lg);
  font-weight: var(--fw-semibold);
}

.link {
  font-size: var(--text-sm);
  color: var(--color-brand);
  text-decoration: none;
  &:hover { text-decoration: underline; }
}

.work-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.work-item {
  display: flex;
  justify-content: space-between;
  padding: var(--space-2) 0;
  border-bottom: 1px solid var(--color-border-light);
  font-size: var(--text-sm);

  &:last-child { border-bottom: none; }
}

.work-title {
  color: var(--color-text);
}

.work-mileage {
  color: var(--color-text-tertiary);
  font-family: var(--font-mono);
}

/* О мотоцикле */
.specs-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.spec-row {
  display: flex;
  justify-content: space-between;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  padding: var(--space-1) 0;
  border-bottom: 1px solid var(--color-border-light);

  &:last-child { border-bottom: none; }
  strong { color: var(--color-text); }
}

/* История */
.history-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.history-item {
  padding: var(--space-2) 0;
  border-bottom: 1px solid var(--color-border-light);

  &:last-child { border-bottom: none; }
}

.history-title {
  font-weight: var(--fw-medium);
}

.history-meta {
  display: flex;
  gap: var(--space-3);
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
  margin-top: var(--space-1);
}

.empty {
  padding: var(--space-4);
  text-align: center;
  color: var(--color-text-tertiary);
  background: var(--color-surface-secondary);
  border-radius: var(--radius-md);
}
</style>
