<script setup lang="ts">
import { type Motorcycle, type Maintenance, type MotorcycleComponent, type MaintenanceEvent } from '~/types'

const props = defineProps<{
  motorcycle: Motorcycle
  initialComponentId?: number | null
}>()

const emit = defineEmits<{ updated: []; 'event-saved': [] }>()

const api = useApi()
const toast = useToast()
const router = useRouter()

const isFormOpen = ref(false)
const isEventFormOpen = ref(false)
const editingMaintenance = ref<Maintenance | null>(null)
const editingEvent = ref<MaintenanceEvent | null>(null)
const eventComponentId = ref<number | null>(null)

const selectedMaintenance = ref<Maintenance | null>(null)
const completingMaintenance = ref<Maintenance | null>(null)
const deletingMaintenance = ref<Maintenance | null>(null)
const components = ref<MotorcycleComponent[]>([])

const currentMileage = computed(() => props.motorcycle.mileage || 0)

const plannedMaintenances = computed(() => {
  return (props.motorcycle.maintenances || [])
    .filter(m => m.status === 'planned')
    .sort((a, b) => {
      if (a.planned_mileage && b.planned_mileage) return a.planned_mileage - b.planned_mileage
      return 0
    })
})

const completedMaintenances = computed(() => {
  return (props.motorcycle.maintenances || [])
    .filter(m => m.status === 'completed')
    .sort((a, b) => {
      if (a.completed_mileage && b.completed_mileage) return b.completed_mileage - a.completed_mileage
      return 0
    })
})

const maintenanceStats = computed(() => {
  const all = props.motorcycle.maintenances || []
  const completed = all.filter(m => m.status === 'completed').length
  const total = all.length
  const percent = total > 0 ? Math.round((completed / total) * 100) : 0
  return { completed, total, percent }
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
    return { maintenance: withRemaining[0].maintenance, remaining: withRemaining[0].remaining, isOverdue: false }
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
  const completed = completedMaintenances.value
  return completed.length > 0 ? completed[0] : null
})

const formatNumber = (val: number) => new Intl.NumberFormat('ru-RU').format(val)
const formatDate = (iso?: string | null) => {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short', year: 'numeric' })
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
  if (m.completed_date) return formatDate(m.completed_date)
  return '—'
})

const planTab = ref<'mileage' | 'date'>('mileage')

const filteredPlan = computed(() => {
  const planned = plannedMaintenances.value

  if (planTab.value === 'mileage') {
    return planned
      .filter(m => m.planned_mileage != null)
      .sort((a, b) => (a.planned_mileage || 0) - (b.planned_mileage || 0))
  } else {
    return planned
      .filter(m => m.planned_date != null)
      .sort((a, b) => (a.planned_date || '').localeCompare(b.planned_date || ''))
  }
})

async function loadComponents() {
  try {
    const res = await api.components.list(props.motorcycle.id)
    components.value = res.components
  } catch {
    components.value = []
  }
}

function openCreate() {
  editingMaintenance.value = null
  isFormOpen.value = true
}

function openEdit(m: Maintenance) {
  selectedMaintenance.value = null
  editingMaintenance.value = m
  isFormOpen.value = true
}

function openDetails(m: Maintenance) {
  selectedMaintenance.value = m
}

function openEventCreate(componentId: number | null = null) {
  editingEvent.value = null
  eventComponentId.value = componentId
  isEventFormOpen.value = true
}

function onEventSaved() {
  isEventFormOpen.value = false
  editingEvent.value = null
  eventComponentId.value = null
  loadComponents()
  emit('updated')
  emit('event-saved')
}

const onFormDone = () => {
  isFormOpen.value = false
  editingMaintenance.value = null
  emit('updated')
}

const onDelete = () => {
  deletingMaintenance.value = null
  emit('updated')
}

const onCompleted = () => {
  completingMaintenance.value = null
  emit('updated')
}

const manualsLink = computed(() => `/manuals?motorcycle=${encodeURIComponent(props.motorcycle.name)}`)
const trainingLink = '/training'
const articlesLink = '/training'

watch(
  () => props.initialComponentId,
  (v) => {
    if (v != null) openEventCreate(v)
  },
  { immediate: true },
)

onMounted(loadComponents)
</script>

<template>
  <div class="maintenance-tab">
    <!-- ============================================================
         Статистика
         ============================================================ -->
    <div class="stats-grid">
      <BaseCard padding="md" class="stat-card">
        <i class="fa-solid fa-wrench stat-icon"></i>
        <div>
          <span class="stat-label">Следующее ТО</span>
          <span class="stat-value">{{ nextMaintenanceText }}</span>
        </div>
      </BaseCard>
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

    <!-- ============================================================
         План обслуживания и Ближайшие задачи
         ============================================================ -->
    <div class="middle-row">
        <!-- План обслуживания -->
        <BaseCard padding="lg" class="plan-card">
        <div class="section-header">
            <h2 class="section-title">План обслуживания</h2>
            <div class="plan-tabs">
            <button
                class="plan-tab"
                :class="{ 'plan-tab--active': planTab === 'mileage' }"
                @click="planTab = 'mileage'"
            >
                По пробегу
            </button>
            <button
                class="plan-tab"
                :class="{ 'plan-tab--active': planTab === 'date' }"
                @click="planTab = 'date'"
            >
                По времени
            </button>
            </div>
        </div>

        <div v-if="filteredPlan.length === 0" class="empty">
            {{ planTab === 'mileage' ? 'Нет работ с указанным пробегом.' : 'Нет работ с указанной датой.' }}
        </div>
        <ul v-else class="plan-list">
            <li v-for="m in filteredPlan" :key="m.id" class="plan-item">
            <div class="plan-marker" :class="{ 'plan-marker--next': m.id === nextMaintenance?.maintenance.id }"></div>
            <div class="plan-content">
                <div class="plan-title">{{ m.title }}</div>
                <div class="plan-meta">
                <span v-if="m.planned_mileage">{{ formatNumber(m.planned_mileage) }} км</span>
                <span v-if="m.planned_date">{{ formatDate(m.planned_date) }}</span>
                </div>
            </div>
            <div class="plan-status">
                <!-- Бейдж для пробега -->
                <BaseBadge
                v-if="planTab === 'mileage' && m.planned_mileage"
                :variant="m.planned_mileage <= currentMileage + 500 ? 'warning' : 'neutral'"
                size="sm"
                >
                {{ m.planned_mileage <= currentMileage ? 'Просрочено' : `Через ${formatNumber(m.planned_mileage - currentMileage)} км` }}
                </BaseBadge>
                <!-- Бейдж для даты  -->
                <BaseBadge
                v-else-if="planTab === 'date' && m.planned_date"
                variant="neutral"
                size="sm"
                >
                {{ formatDate(m.planned_date) }}
                </BaseBadge>
            </div>
            </li>
        </ul>
        </BaseCard>

      <!-- Ближайшие задачи -->
      <BaseCard padding="lg" class="tasks-card">
        <div class="section-header">
          <h2 class="section-title">Ближайшие задачи</h2>
          <NuxtLink to="#history" class="link">Все задачи →</NuxtLink>
        </div>
        <div v-if="plannedMaintenances.length === 0" class="empty">
          Нет задач.
        </div>
        <div v-else class="tasks-list">
          <div v-for="m in plannedMaintenances" :key="m.id" class="task-item">
            <div class="task-content">
              <span class="task-title">{{ m.title }}</span>
              <span v-if="m.planned_mileage" class="task-mileage">
                {{ formatNumber(m.planned_mileage) }} км
              </span>
            </div>
          </div>
        </div>
        <BaseButton variant="primary" block class="add-tast-btn" @click="openEventCreate">
          <template #icon><i class="fa-solid fa-layer-group"></i></template>
          Создать событие
        </BaseButton>
      </BaseCard>

      <!-- Полезное -->
      <BaseCard padding="lg" class="useful-card">
        <h2 class="section-title">Полезно</h2>
        <div class="useful-links">
          <NuxtLink :to="manualsLink" class="useful-link">
            <i class="fa-solid fa-book"></i>
            <div>
              <span class="useful-title">Регламент ТО</span>
              <span class="useful-desc">Для {{ motorcycle.name }}</span>
            </div>
            <i class="fa-solid fa-chevron-right useful-arrow"></i>
          </NuxtLink>
          <NuxtLink :to="trainingLink" class="useful-link">
            <i class="fa-solid fa-graduation-cap"></i>
            <div>
              <span class="useful-title">Курсы для мотоциклистов</span>
              <span class="useful-desc">Обучение для мотоциклистов</span>
            </div>
            <i class="fa-solid fa-chevron-right useful-arrow"></i>
          </NuxtLink>
          <NuxtLink :to="articlesLink" class="useful-link">
            <i class="fa-solid fa-newspaper"></i>
            <div>
              <span class="useful-title">Статьи и гайды</span>
              <span class="useful-desc">Полезные материалы</span>
            </div>
            <i class="fa-solid fa-chevron-right useful-arrow"></i>
          </NuxtLink>
        </div>
      </BaseCard>
    </div>

    <!-- ============================================================
         История обслуживания
         ============================================================ -->
    <BaseCard padding="lg">
      <div class="section-header">
        <h2 class="section-title">История обслуживания</h2>
        <NuxtLink to="#history" class="link">Вся история →</NuxtLink>
      </div>
      <div v-if="completedMaintenances.length === 0" class="empty">
        Нет выполненных работ.
      </div>
      <div v-else class="history-table">
        <div class="history-header">
          <span>Дата</span>
          <span>Тип работ</span>
          <span>Пробег</span>
          <span>Примечание</span>
          <span></span>
        </div>
        <div v-for="m in completedMaintenances" :key="m.id" class="history-row">
          <span class="history-date">{{ formatDate(m.completed_date) }}</span>
          <span class="history-title">{{ m.title }}</span>
          <span class="history-mileage">{{ m.completed_mileage ? `${formatNumber(m.completed_mileage)} км` : '—' }}</span>
          <span class="history-note">{{ m.description || '—' }}</span>
          <button class="history-action" @click="openDetails(m)">
            <i class="fa-solid fa-ellipsis"></i>
          </button>
        </div>
      </div>
    </BaseCard>

    <!-- ============================================================
         Модалки
         ============================================================ -->
    <BaseModal v-if="isFormOpen" :title="editingMaintenance ? 'Редактировать запись' : 'Новая запись'" @close="isFormOpen = false">
      <MaintenanceForm
        :motorcycles="[motorcycle]"
        :default-motorcycle-id="motorcycle.id"
        :initial-data="editingMaintenance"
        @created="onFormDone"
        @updated="onFormDone"
        @cancel="isFormOpen = false"
      />
    </BaseModal>

    <MaintenanceDetailsModal
      v-if="selectedMaintenance"
      :maintenance="{ ...selectedMaintenance, motorcycle }"
      @close="selectedMaintenance = null"
      @updated="emit('updated'); selectedMaintenance = null"
      @edit="openEdit(selectedMaintenance!)"
      @complete="completingMaintenance = selectedMaintenance; selectedMaintenance = null"
      @delete="deletingMaintenance = selectedMaintenance; selectedMaintenance = null"
    />

    <CompleteMaintenanceModal
      v-if="completingMaintenance"
      :maintenance="completingMaintenance"
      @close="completingMaintenance = null"
      @completed="onCompleted"
    />

    <DeleteMaintenanceModal
      v-if="deletingMaintenance"
      :maintenance="deletingMaintenance"
      @close="deletingMaintenance = null"
      @deleted="onDelete"
    />

    <BaseModal
      v-if="isEventFormOpen"
      :title="editingEvent ? 'Редактировать событие' : 'Новое событие обслуживания'"
      @close="isEventFormOpen = false"
    >
      <MaintenanceEventForm
        :motorcycle-id="motorcycle.id"
        :current-mileage="motorcycle.mileage ?? null"
        :components="components"
        :initial-component-id="eventComponentId"
        :event="editingEvent"
        @saved="onEventSaved"
        @cancel="isEventFormOpen = false"
      />
    </BaseModal>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.maintenance-tab {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

/* ============================================================
   Статистика
   ============================================================ */
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
  flex-shrink: 0;
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
  transition: width var(--transition-base);
}

/* ============================================================
   Средний ряд (План, Задачи, Полезно)
   ============================================================ */
.middle-row {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);

  @include lg-up {
    grid-template-columns: 1.5fr 1fr 1fr;
  }
}

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

.plan-tabs {
  display: flex;
  gap: var(--space-1);
  background: var(--color-surface-secondary);
  padding: 2px;
  border-radius: var(--radius-md);
}

.plan-tab {
  padding: 4px 8px;
  font-size: var(--text-xs);
  font-weight: var(--fw-medium);
  color: var(--color-text-secondary);
  border-radius: var(--radius-sm);
  border: none;
  background: transparent;
  cursor: pointer;

  &--active {
    background: var(--color-surface);
    color: var(--color-brand);
    box-shadow: var(--shadow-sm);
  }
}

.plan-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.plan-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) 0;
  border-bottom: 1px solid var(--color-border-light);

  &:last-child { border-bottom: none; }
}

.plan-marker {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid var(--color-border);
  flex-shrink: 0;

  &--next {
    border-color: var(--color-brand);
    background: var(--color-brand);
  }
}

.plan-content {
  flex: 1;
}

.plan-title {
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  color: var(--color-text);
}

.plan-meta {
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
  display: flex;
  gap: var(--space-2);
}

.plan-status {
  flex-shrink: 0;
}

.tasks-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  margin-bottom: var(--space-3);
}

.task-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) 0;
  border-bottom: 1px solid var(--color-border-light);

  &:last-child { border-bottom: none; }
}

.task-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex: 1;
}

.task-title {
  font-size: var(--text-sm);
  color: var(--color-text);
}

.task-mileage {
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
  background: var(--color-surface-secondary);
  padding: 2px 6px;
  border-radius: var(--radius-sm);
}

.add-task-btn {
  margin-top: var(--space-2);
}

.useful-links {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.useful-link {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--color-surface-secondary);
  border-radius: var(--radius-md);
  text-decoration: none;
  color: var(--color-text);
  transition: background var(--transition-fast);

  &:hover { background: var(--color-surface-hover); }

  i:first-child {
    font-size: 20px;
    color: var(--color-brand);
    width: 24px;
    text-align: center;
  }
}

.useful-title {
  display: block;
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
}

.useful-desc {
  display: block;
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
}

.useful-arrow {
  margin-left: auto;
  color: var(--color-text-tertiary);
  font-size: 12px;
}

/* ============================================================
   История
   ============================================================ */
.history-table {
  display: flex;
  flex-direction: column;
}

.history-header {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr 2fr 40px;
  gap: var(--space-3);
  padding: var(--space-2) 0;
  border-bottom: 1px solid var(--color-border);
  font-size: var(--text-xs);
  font-weight: var(--fw-semibold);
  color: var(--color-text-tertiary);
  text-transform: uppercase;
}

.history-row {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr 2fr 40px;
  gap: var(--space-3);
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--color-border-light);
  font-size: var(--text-sm);
  align-items: center;

  &:last-child { border-bottom: none; }
}

.history-date {
  color: var(--color-text-secondary);
}

.history-title {
  font-weight: var(--fw-medium);
  color: var(--color-text);
}

.history-mileage {
  color: var(--color-text-secondary);
  font-family: var(--font-mono);
}

.history-note {
  color: var(--color-text-tertiary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.history-action {
  background: none;
  border: none;
  color: var(--color-text-tertiary);
  cursor: pointer;
  padding: var(--space-1);
  border-radius: var(--radius-sm);

  &:hover { background: var(--color-surface-hover); }
}

.empty {
  padding: var(--space-4);
  text-align: center;
  color: var(--color-text-tertiary);
  background: var(--color-surface-secondary);
  border-radius: var(--radius-md);
}

@include md-down {
  .history-header { display: none; }
  .history-row {
    grid-template-columns: 1fr;
    gap: var(--space-1);
    padding: var(--space-3) 0;
  }
  .history-date { font-size: var(--text-xs); }
  .history-mileage { font-size: var(--text-xs); }
}
</style>
