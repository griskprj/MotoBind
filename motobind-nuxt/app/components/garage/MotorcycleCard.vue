<script setup lang="ts">
import type { Motorcycle, Maintenance } from '~/types'

const props = defineProps<{
  motorcycle: Motorcycle
}>()

const emit = defineEmits<{ updated: [] }>()

const api = useApi()
const toast = useToast()
const router = useRouter()
const mediaUrl = useMediaUrl()

const photo = computed(() => mediaUrl(props.motorcycle.photo_url))

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
    return {
      maintenance: withRemaining[0].maintenance,
      remaining: withRemaining[0].remaining,
      isOverdue: false,
    }
  }

  // Если все просрочены — берём самый просроченный
  const overdue = withMileage
    .map(m => ({
      maintenance: m,
      remaining: (m.planned_mileage || 0) - currentMileage.value,
    }))
    .sort((a, b) => b.remaining - a.remaining)

  if (overdue.length > 0) {
    return {
      maintenance: overdue[0].maintenance,
      remaining: overdue[0].remaining,
      isOverdue: true,
    }
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

const plannedCount = computed(() => plannedMaintenances.value.length)

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

const isMileageModalOpen = ref(false)
const isDeleteConfirmOpen = ref(false)
const deleting = ref(false)

async function onDelete() {
  deleting.value = true
  try {
    await api.motorcycle.remove(props.motorcycle.id)
    toast.success('Мотоцикл удалён')
    emit('updated')
  } catch (e) {
    toast.error((e as any).message || 'Ошибка удаления')
  } finally {
    deleting.value = false
    isDeleteConfirmOpen.value = false
  }
}

const maintenanceLink = computed(() => `/garage/${props.motorcycle.id}`)
const diagnosticsLink = computed(() => `/garage/${props.motorcycle.id}#diagnostics`)
const manualsLink = computed(() => `/manuals?motorcycle=${encodeURIComponent(props.motorcycle.name)}`)
const historyLink = computed(() => `/garage/${props.motorcycle.id}#history`)
</script>

<template>
  <BaseCard padding="none" class="moto-card">
    <div class="moto-card__layout">
      <!-- Фото (слева) -->
      <div class="moto-card__image-wrap">
        <img
          v-if="photo"
          :src="photo"
          :alt="motorcycle.name"
          class="moto-card__image"
          loading="lazy"
        />
        <div v-else class="moto-card__image-placeholder">
          <i class="fa-solid fa-motorcycle"></i>
        </div>
      </div>

      <!-- Контент (справа) -->
      <div class="moto-card__content">
        <!-- Заголовок и бейджи -->
        <div class="moto-card__header">
          <div>
            <h3 class="moto-card__name">{{ motorcycle.name }}</h3>
            <p class="moto-card__details">
              <span v-if="motorcycle.years">{{ motorcycle.years }}</span>
              <span v-if="motorcycle.years && motorcycle.volume" class="dot">•</span>
              <span v-if="motorcycle.volume">{{ motorcycle.volume }} см³</span>
              <span v-if="motorcycle.license_plate" class="dot">•</span>
              <span v-if="motorcycle.license_plate" class="plate">{{ motorcycle.license_plate }}</span>
            </p>
          </div>
          <div class="moto-card__badges">
            <BaseBadge v-if="plannedCount > 0" variant="warning" size="sm">
              {{ plannedCount }} {{ plannedCount === 1 ? 'задача' : plannedCount < 5 ? 'задачи' : 'задач' }}
            </BaseBadge>
          </div>
        </div>

        <!-- Статистика в три колонки -->
        <div class="moto-card__stats">
          <div class="stat">
            <i class="fa-solid fa-gauge-high stat-icon"></i>
            <div>
              <span class="stat-label">Пробег</span>
              <span class="stat-value">{{ formatNumber(currentMileage) }} км</span>
            </div>
          </div>
          <div class="stat">
            <i class="fa-solid fa-calendar stat-icon"></i>
            <div>
              <span class="stat-label">Следующее ТО</span>
              <span class="stat-value">{{ nextMaintenanceText }}</span>
            </div>
          </div>
          <div class="stat">
            <i class="fa-solid fa-wrench stat-icon"></i>
            <div>
              <span class="stat-label">Последнее ТО</span>
              <span class="stat-value">{{ lastMaintenanceText }}</span>
            </div>
          </div>
        </div>

        <!-- Прогресс обслуживания -->
        <div class="moto-card__progress">
          <div class="progress-header">
            <span class="progress-label">Состояние обслуживания</span>
            <span class="progress-count">{{ maintenanceStats.completed }} из {{ maintenanceStats.total }} задач</span>
          </div>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: `${maintenanceStats.percent}%` }" />
          </div>
        </div>

      </div>
    </div>
  </BaseCard>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.moto-card {
  overflow: hidden;
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);

  &:hover {
    border-color: var(--color-border-dark);
    box-shadow: var(--shadow-md);
  }
}

.moto-card__layout {
  padding: var(--space-3);
  display: flex;
  flex-direction: column;

  @include md-up {
    flex-direction: row;
  }
}

.moto-card__image-wrap {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  background: var(--color-surface-secondary);
  flex-shrink: 0;
  border-radius: var(--radius-md);

  @include md-up {
    width: 300px;
    aspect-ratio: 4 / 3;
  }
}

.moto-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  inset: 0;
  border-radius: var(--radius-md);

}

.moto-card__image-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-tertiary);
  font-size: 48px;
}

.moto-card__content {
  flex: 1;
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  min-width: 0;
}

.moto-card__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-2);
}

.moto-card__name {
  font-size: var(--text-xl);
  font-weight: var(--fw-bold);
  color: var(--color-text);
  line-height: var(--leading-tight);
  margin-bottom: var(--space-1);
}

.moto-card__details {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-2);
}

.dot {
  color: var(--color-text-tertiary);
}

.plate {
  font-family: var(--font-mono);
  text-transform: uppercase;
}

/* Статистика */
.moto-card__stats {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-3);
  padding: var(--space-3) 0;
  border-top: 1px solid var(--color-border-light);
  border-bottom: 1px solid var(--color-border-light);

  @include sm-up {
    grid-template-columns: repeat(3, 1fr);
  }
}

.stat {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.stat-icon {
  font-size: 18px;
  color: var(--color-brand);
  width: 24px;
  text-align: center;
}

.stat-label {
  display: block;
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
  text-transform: uppercase;
}

.stat-value {
  display: block;
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  color: var(--color-text);
}

/* Прогресс */
.moto-card__progress {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.progress-header {
  display: flex;
  justify-content: space-between;
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
}

.progress-count {
  color: var(--color-text-tertiary);
}

.progress-bar {
  height: 6px;
  background: var(--color-surface-secondary);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--color-brand);
  border-radius: var(--radius-full);
  transition: width var(--transition-base);
}
</style>
