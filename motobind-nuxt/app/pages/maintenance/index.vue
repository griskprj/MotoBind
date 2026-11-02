<script setup lang="ts">
import type { Motorcycle, Maintenance } from '~/types'

definePageMeta({ middleware: 'auth' })

useSeoMeta({
  title: 'Центр обслуживания',
  robots: 'noindex',
})

const api = useApi()
const { data: motorcycles, pending, error, refresh } = await useAsyncData(
  'maintenance-center',
  () => api.motorcycle.list(),
  { default: () => [] }
)

// Состояние UI
const activeTab = ref<'planned' | 'history'>('planned')
const isFormOpen = ref(false)
const editingMaintenance = ref<Maintenance | null>(null)
const selectedMaintenance = ref<(Maintenance & { motorcycle: Motorcycle }) | null>(null)
const quickStartMotorcycle = ref<Motorcycle | null>(null)

// --- ФИЛЬТРЫ ---
const filterMotorcycleId = ref<number | 'all'>('all')
const filterBy = ref< 'all' | 'date' | 'mileage'>('all')

const allWorks = computed(() => {
  if (!motorcycles.value) return []
  const list: Array<Maintenance & { motorcycle: Motorcycle }> = []
  for (const moto of motorcycles.value) {
    for (const m of moto.maintenances || []) {
      list.push({ ...m, motorcycle: moto })
    }
  }
  return list
})

const filteredWorks = computed(() => {
  if (filterMotorcycleId.value === 'all') return allWorks.value
  return allWorks.value.filter(m => String(m.motorcycle.id) === String(filterMotorcycleId.value))
})

const selectedMotorcycle = computed(() => {
  if (filterMotorcycleId.value === 'all' || !motorcycles.value) return null
  return motorcycles.value.find(m => String(m.id) === String(filterMotorcycleId.value)) || null
})

const hasNoWorksForSelected = computed(() => {
  if (!selectedMotorcycle.value) return false
  const worksForSelected = allWorks.value.filter(
    m => String(m.motorcycle.id) === String(selectedMotorcycle.value!.id)
  )
  return worksForSelected.length === 0
})

// Планы
const planned = computed(() => {
  let filtered = filteredWorks.value.filter(m => m.status === 'planned')

  if (filterBy.value === 'date') {
    filtered = filtered.filter(m => !!m.planned_date)
    return filtered.sort((a, b) => {
      return (a.planned_date || '').localeCompare(b.planned_date || '')
    })
  }

  if (filterBy.value === 'mileage') {
    filtered = filtered.filter(m => m.planned_mileage != null)
    return filtered.sort((a, b) => {
      return (a.planned_mileage || 0) - (b.planned_mileage || 0)
    })
  }

  return filtered.sort((a, b) => b.id - a.id)
})

// История
const history = computed(() => {
  return filteredWorks.value
    .filter(m => m.status === 'completed')
    .sort((a, b) => {
      if (a.completed_date && b.completed_date) return b.completed_date.localeCompare(a.completed_date)
      return b.id - a.id
    })
})

// Форматирование
const formatDate = (isoStr?: string | null) => {
  if (!isoStr) return ''
  return new Date(isoStr).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short', year: 'numeric' })
}
const formatMileage = (val?: number | null) => {
  if (!val) return ''
  return new Intl.NumberFormat('ru-RU').format(val) + ' км'
}
const formatCost = (val?: number | null) => {
  if (!val) return ''
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', maximumFractionDigits: 0 }).format(val)
}

// Обработчики действий
function openCreate() {
  editingMaintenance.value = null
  isFormOpen.value = true
}

function openEdit(m: Maintenance) {
  selectedMaintenance.value = null
  editingMaintenance.value = m
  isFormOpen.value = true
}

function openDetails(m: Maintenance & { motorcycle: Motorcycle }) {
  selectedMaintenance.value = m
}

const completingMaintenance = ref<Maintenance | null>(null)
function openComplete(m: Maintenance) {
  selectedMaintenance.value = null
  completingMaintenance.value = m
}

const deletingMaintenance = ref<Maintenance | null>(null)
function openDelete(m: Maintenance) {
  selectedMaintenance.value = null
  deletingMaintenance.value = m
}

function openQuickStart() {
  if (selectedMotorcycle.value) {
    quickStartMotorcycle.value = selectedMotorcycle.value
  }
}

function onQuickStartDone() {
  quickStartMotorcycle.value = null
  refresh()
}

function onFormDone() {
  isFormOpen.value = false
  editingMaintenance.value = null
  refresh()
}

function onCompleted() {
  completingMaintenance.value = null
  refresh()
}

function onDelete() {
  deletingMaintenance.value = null
  refresh()
}
</script>

<template>
  <div class="center-page">
    <!-- Заголовок -->
    <header class="page-header">
      <div>
        <h1 class="page-title">Центр обслуживания</h1>
        <p class="page-subtitle">Все работы по всем вашим мотоциклам в одном месте.</p>
      </div>
      <div class="header-actions">
        <BaseButton v-if="motorcycles?.length" @click="openCreate">
          <template #icon><i class="fa-solid fa-plus"></i></template>
          Добавить запись
        </BaseButton>
      </div>
    </header>

    <!-- Модалка создания/редактирования -->
    <BaseModal
      v-if="isFormOpen"
      :title="editingMaintenance ? 'Редактировать запись' : 'Новая запись'"
      @close="isFormOpen = false"
    >
      <MaintenanceForm
        :motorcycles="motorcycles || []"
        :default-motorcycle-id="motorcycles?.[0]?.id"
        :initial-data="editingMaintenance"
        @created="onFormDone"
        @updated="onFormDone"
        @cancel="isFormOpen = false"
      />
    </BaseModal>

    <!-- Модалка деталей -->
    <MaintenanceDetailsModal
      v-if="selectedMaintenance"
      :maintenance="selectedMaintenance"
      @close="selectedMaintenance = null"
      @updated="refresh(); selectedMaintenance = null"
      @edit="openEdit(selectedMaintenance)"
      @complete="openComplete(selectedMaintenance)"
      @delete="openDelete(selectedMaintenance)"
    />

    <!-- Модалка завершения -->
    <CompleteMaintenanceModal
      v-if="completingMaintenance"
      :maintenance="completingMaintenance"
      @close="completingMaintenance = null"
      @completed="onCompleted"
    />

    <!-- Модалка удаления -->
    <DeleteMaintenanceModal
      v-if="deletingMaintenance"
      :maintenance="deletingMaintenance"
      @close="deletingMaintenance = null"
      @deleted="onDelete"
    />

    <!-- Модалка быстрого добавления обслуживаний -->
    <QuickStartModal
      v-if="quickStartMotorcycle"
      :motorcycle="quickStartMotorcycle"
      @close="quickStartMotorcycle = null"
      @created="onQuickStartDone"
    />

    <!-- Загрузка -->
    <div v-if="pending" class="loading">
      <BaseSkeleton height="80px" rounded />
      <BaseSkeleton height="200px" rounded />
    </div>

    <!-- Ошибка -->
    <div v-else-if="error" class="error">
      <p>Не удалось загрузить данные.</p>
      <BaseButton @click="refresh()">Повторить</BaseButton>
    </div>

    <!-- Пустой гараж -->
    <template v-else-if="motorcycles?.length === 0">
      <BaseEmptyState
        title="Гараж пуст"
        description="Сначала добавьте мотоцикл, чтобы отслеживать его обслуживание."
      >
        <template #action>
          <BaseButton to="/garage/new" variant="primary">Добавить мотоцикл</BaseButton>
        </template>
      </BaseEmptyState>
    </template>

    <!-- Контент -->
    <template v-else>
      <!-- Сводка -->
      <div class="stats-grid">
        <BaseCard padding="md" class="stat-card">
          <span class="stat-label">Всего работ</span>
          <span class="stat-value">{{ allWorks.length }}</span>
        </BaseCard>
        <BaseCard padding="md" class="stat-card">
          <span class="stat-label">В плане</span>
          <span class="stat-value text-warning">{{ planned.length }}</span>
        </BaseCard>
        <BaseCard padding="md" class="stat-card">
          <span class="stat-label">Потрачено</span>
          <span class="stat-value text-success">
            {{ formatCost(history.reduce((sum, m) => sum + (m.cost || 0), 0)) }}
          </span>
        </BaseCard>
      </div>

      <MaintenanceFilters
        v-model:selected-motorcycle-id="filterMotorcycleId"
        v-model:filter-by="filterBy"
        :motorcycles="motorcycles || []"
        :active-tab="activeTab"
      />

      <!-- БАННЕР: Быстрый старт -->
      <div v-if="hasNoWorksForSelected && selectedMotorcycle" class="quick-start-banner">
        <div class="banner-content">
          <div class="banner-icon">
            <i class="fa-solid fa-wand-magic-sparkles"></i>
          </div>
          <div>
            <h3 class="banner-title">У {{ selectedMotorcycle.name }} пока нет обслуживаний</h3>
            <p class="banner-text">Сгенерируйте базовый план ТО за 10 секунд на основе вашего стиля езды.</p>
          </div>
        </div>
        <BaseButton variant="primary" @click="openQuickStart" class="banner-btn">
          Настроить
        </BaseButton>
      </div>

      <!-- Табы -->
      <div class="tabs">
        <button
          class="tab-btn"
          :class="{ 'tab-btn--active': activeTab === 'planned' }"
          @click="activeTab = 'planned'"
        >
          Планы
          <span v-if="planned.length" class="badge">{{ planned.length }}</span>
        </button>
        <button
          class="tab-btn"
          :class="{ 'tab-btn--active': activeTab === 'history' }"
          @click="activeTab = 'history'"
        >
          История
          <span v-if="history.length" class="badge">{{ history.length }}</span>
        </button>
      </div>

      <!-- Список планов -->
      <div v-if="activeTab === 'planned'" class="list">
        <div v-if="planned.length === 0" class="empty-list">Нет запланированных работ.</div>
        <div
          v-for="m in planned"
          :key="`${m.motorcycle.id}-${m.id}`"
          class="work-card"
          @click="openDetails(m)"
        >
          <div class="work-status-bar planned" />
          <div class="work-content">
            <div class="work-header">
              <NuxtLink :to="`/garage/${m.motorcycle.id}`" class="moto-link" @click.stop>
                {{ m.motorcycle.name }}
              </NuxtLink>
              <span class="work-title">{{ m.title }}</span>
              <MaintenanceCategoryBadge :category="m.category" />
            </div>
            <p v-if="m.description" class="work-desc">{{ m.description }}</p>
            <div class="work-meta">
              <span v-if="m.planned_date">
                <i class="fa-regular fa-calendar"></i> {{ formatDate(m.planned_date) }}
              </span>

              <span v-if="m.planned_mileage">
                <i class="fa-solid fa-gauge-high"></i> {{ formatMileage(m.planned_mileage) }}
              </span>

              <!-- Остаток до пробега -->
              <template v-if="getMileageRemaining(m)">
                <span
                  class="mileage-remaining"
                  :class="{
                    'is-overdue': getMileageRemaining(m)?.isOverdue,
                    'is-warning': getMileageRemaining(m)?.isWarning
                  }"
                >
                  <i class="fa-solid fa-flag-checkered"></i>
                  {{ formatRemaining(getMileageRemaining(m)) }}
                </span>
              </template>
            </div>
          </div>
        </div>
      </div>

      <!-- Список истории -->
      <div v-else class="list">
        <div v-if="history.length === 0" class="empty-list">История обслуживания пуста.</div>
        <div
          v-for="m in history"
          :key="`${m.motorcycle.id}-${m.id}`"
          class="work-card"
          @click="openDetails(m)"
        >
          <div class="work-status-bar completed" />
          <div class="work-content">
            <div class="work-header">
              <NuxtLink :to="`/garage/${m.motorcycle.id}`" class="moto-link" @click.stop>
                {{ m.motorcycle.name }}
              </NuxtLink>
              <span class="work-title">{{ m.title }}</span>
              <MaintenanceCategoryBadge :category="m.category" />
              <span v-if="m.cost" class="work-cost">{{ formatCost(m.cost) }}</span>
            </div>
            <p v-if="m.description" class="work-desc">{{ m.description }}</p>
            <div class="work-meta">
              <span v-if="m.completed_date">
                <i class="fa-regular fa-calendar-check"></i> {{ formatDate(m.completed_date) }}
              </span>
              <span v-if="m.completed_mileage">
                <i class="fa-solid fa-gauge-high"></i> {{ formatMileage(m.completed_mileage) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.center-page {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.page-header {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);

  @include sm-up {
    flex-direction: row;
    align-items: flex-start;
    justify-content: space-between;
  }
}

.page-title {
  font-size: var(--text-2xl);
  font-weight: var(--fw-bold);
}

.page-subtitle {
  font-size: var(--text-base);
  color: var(--color-text-secondary);
  margin-top: var(--space-1);
}

.add-btn {
  align-self: flex-start;
}

/* Сводка */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: var(--space-3);
}
.stat-card {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}
.stat-label {
  font-size: var(--text-xs);
  text-transform: uppercase;
  color: var(--color-text-tertiary);
}
.stat-value {
  font-size: var(--text-xl);
  font-weight: var(--fw-bold);
}
.text-warning { color: var(--color-warning); }
.text-success { color: var(--color-success); }

/* Баннер быстрого старта */
.quick-start-banner {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  padding: var(--space-4);
  background: var(--color-brand-soft);
  border: 1px solid color-mix(in srgb, var(--color-brand) 30%, transparent);
  border-radius: var(--radius-lg);

  @include sm-up {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}

.banner-content {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.banner-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--color-brand);
  color: #fff;
  font-size: 20px;
  flex-shrink: 0;
}

.banner-title {
  font-size: var(--text-lg);
  font-weight: var(--fw-semibold);
  color: var(--color-text);
  margin-bottom: var(--space-1);
}

.banner-text {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.banner-btn {
  flex-shrink: 0;
}

/* Табы */
.tabs {
  display: flex;
  border-bottom: 1px solid var(--color-border);
  gap: var(--space-4);
}
.tab-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) 0;
  font-size: var(--text-base);
  font-weight: var(--fw-medium);
  color: var(--color-text-secondary);
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  transition: all var(--transition-fast);

  &--active {
    color: var(--color-brand);
    border-bottom-color: var(--color-brand);
  }
}
.badge {
  background: var(--color-surface-secondary);
  padding: 2px 8px;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
}

/* Список работ */
.list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}
.empty-list {
  padding: var(--space-6);
  text-align: center;
  color: var(--color-text-secondary);
  background: var(--color-surface-secondary);
  border-radius: var(--radius-md);
}

.work-card {
  display: flex;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: pointer;
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);

  &:hover {
    border-color: var(--color-border-dark);
    box-shadow: var(--shadow-sm);
  }
}

.work-status-bar {
  width: 4px;
  flex-shrink: 0;

  &.planned { background: var(--color-warning); }
  &.completed { background: var(--color-success); }
}

.work-content {
  flex: 1;
  padding: var(--space-3) var(--space-4);
  min-width: 0;
}

.work-header {
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  flex-wrap: wrap;
  margin-bottom: var(--space-1);
}

.moto-link {
  font-size: var(--text-xs);
  font-weight: var(--fw-semibold);
  color: var(--color-brand);
  text-decoration: none;
  background: var(--color-brand-soft);
  padding: 2px 8px;
  border-radius: var(--radius-sm);

  &:hover { text-decoration: underline; }
}

.work-title {
  font-size: var(--text-base);
  font-weight: var(--fw-semibold);
  color: var(--color-text);
}

.work-cost {
  margin-left: auto;
  font-weight: var(--fw-bold);
  color: var(--color-text);
}

.work-desc {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-2);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.work-meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
}

.mileage-remaining {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  background: var(--color-surface-secondary);
  color: var(--color-text-secondary);
  font-weight: var(--fw-medium);

  &.is-warning {
    background: var(--color-warning-soft);
    color: var(--color-warning-strong);
  }

  &.is-overdue {
    background: var(--color-danger-soft);
    color: var(--color-danger-strong);
  }
}
</style>
