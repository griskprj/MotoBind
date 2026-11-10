<script setup lang="ts">
import type { Motorcycle, Maintenance, MaintenanceEvent, MotorcycleComponent } from '~/types'

definePageMeta({ middleware: 'auth' })

useSeoMeta({
  title: 'Центр обслуживания',
  robots: 'noindex',
})

const api = useApi()
const toast = useToast()

// Загружаем мотоциклы
const { data: motorcycles, pending, error, refresh } = await useAsyncData(
  'maintenance-center',
  () => api.motorcycle.list(),
  { default: () => [] }
)

// Загружаем компоненты всех мотоциклов (для формы событий)
const allComponents = ref<MotorcycleComponent[]>([])
const componentsLoading = ref(false)

async function loadAllComponents() {
  if (!motorcycles.value?.length) return
  componentsLoading.value = true
  try {
    const promises = motorcycles.value.map(m => api.components.list(m.id))
    const results = await Promise.all(promises)
    allComponents.value = results.flatMap((res: any) => res.components)
  } catch {
    allComponents.value = []
  } finally {
    componentsLoading.value = false
  }
}

watch(motorcycles, loadAllComponents, { immediate: true })

// --- СОСТОЯНИЕ UI ---
const activeTab = ref<'planned' | 'history' | 'events'>('events') // По умолчанию открываем события
const isLegacyFormOpen = ref(false)
const editingMaintenance = ref<Maintenance | null>(null)
const selectedMaintenance = ref<(Maintenance & { motorcycle: Motorcycle }) | null>(null)

// Состояние для Событий
const events = ref<MaintenanceEvent[]>([])
const eventsLoading = ref(false)
const isEventFormOpen = ref(false)
const editingEvent = ref<MaintenanceEvent | null>(null)
const selectedEvent = ref<MaintenanceEvent | null>(null)
const deletingEvent = ref<MaintenanceEvent | null>(null)

async function loadEvents() {
  if (!motorcycles.value?.length) return
  eventsLoading.value = true
  try {
    const promises = motorcycles.value.map(m => api.maintenance.events.list(m.id, { per_page: 100 }))
    const results = await Promise.all(promises)
    // Собираем все события в один список и сортируем по дате (новые сверху)
    events.value = results
      .flatMap((res: any) => res.events)
      .sort((a, b) => (b.date || '').localeCompare(a.date || ''))
  } catch {
    events.value = []
  } finally {
    eventsLoading.value = false
  }
}

watch(motorcycles, loadEvents, { immediate: true })

const quickStartMotorcycle = ref<Motorcycle | null>(null)

// --- ФИЛЬТРЫ ---
const searchQuery = ref('')
const filterMotorcycleId = ref<number | 'all'>('all')
const filterBy = ref<'all' | 'date' | 'mileage'>('all')
const sortAsc = ref(true)

// --- БАЗОВЫЕ ВЫЧИСЛЕНИЯ ---
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
  let list = allWorks.value
  if (filterMotorcycleId.value !== 'all') {
    list = list.filter(m => String(m.motorcycle.id) === String(filterMotorcycleId.value))
  }
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(m =>
      m.title.toLowerCase().includes(q) ||
      (m.description && m.description.toLowerCase().includes(q))
    )
  }
  return list
})

const filteredEvents = computed(() => {
  let list = events.value
  if (filterMotorcycleId.value !== 'all') {
    list = list.filter(e => String(e.motorcycle_id) === String(filterMotorcycleId.value))
  }
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(e =>
      e.comment?.toLowerCase().includes(q) ||
      e.works.some(w => w.title?.toLowerCase().includes(q))
    )
  }
  return list
})

// --- СТАТИСТИКА ---
const now = new Date()
const twelveMonthsAgo = new Date()
twelveMonthsAgo.setFullYear(now.getFullYear() - 1)

const plannedList = computed(() => filteredWorks.value.filter(m => m.status === 'planned'))
const overdueList = computed(() => {
  return plannedList.value.filter(m => {
    if (m.planned_date && new Date(m.planned_date) < now) return true
    if (m.planned_mileage && m.motorcycle.mileage && m.planned_mileage < m.motorcycle.mileage) return true
    return false
  })
})
const completedLast12m = computed(() => {
  return filteredWorks.value.filter(m => {
    return m.status === 'completed' && m.completed_date && new Date(m.completed_date) >= twelveMonthsAgo
  })
})
const totalCost = computed(() => {
  const legacyCost = allWorks.value.filter(m => m.status === 'completed' && m.cost).reduce((sum, m) => sum + (m.cost || 0), 0)
  const eventsCost = filteredEvents.value.reduce((sum, e) => sum + (e.total_cost || 0), 0)
  return legacyCost + eventsCost
})
const costLast12m = computed(() => {
  const legacyCost = completedLast12m.value.reduce((sum, m) => sum + (m.cost || 0), 0)
  const eventsCost = filteredEvents.value
    .filter(e => e.date && new Date(e.date) >= twelveMonthsAgo)
    .reduce((sum, e) => sum + (e.total_cost || 0), 0)
  return legacyCost + eventsCost
})

// --- СПИСКИ ДЛЯ ТАБОВ ---
const planned = computed(() => {
  let list = [...plannedList.value]
  if (filterBy.value === 'date') {
    list = list.filter(m => !!m.planned_date).sort((a, b) => {
      const res = (a.planned_date || '').localeCompare(b.planned_date || '')
      return sortAsc.value ? res : -res
    })
  } else if (filterBy.value === 'mileage') {
    list = list.filter(m => m.planned_mileage != null).sort((a, b) => {
      const res = (a.planned_mileage || 0) - (b.planned_mileage || 0)
      return sortAsc.value ? res : -res
    })
  } else {
    list.sort((a, b) => {
      const dateA = a.planned_date || '9999-12-31'
      const dateB = b.planned_date || '9999-12-31'
      if (dateA !== dateB) {
        const res = dateA.localeCompare(dateB)
        return sortAsc.value ? res : -res
      }
      const milA = a.planned_mileage || 9999999
      const milB = b.planned_mileage || 9999999
      const res = milA - milB
      return sortAsc.value ? res : -res
    })
  }
  return list
})

const history = computed(() => {
  return filteredWorks.value
    .filter(m => m.status === 'completed')
    .sort((a, b) => {
      if (a.completed_date && b.completed_date) return b.completed_date.localeCompare(a.completed_date)
      return b.id - a.id
    })
})

const selectedMotorcycle = computed(() => {
  if (filterMotorcycleId.value === 'all' || !motorcycles.value) return null
  return motorcycles.value.find(m => String(m.id) === String(filterMotorcycleId.value)) || null
})

const hasNoWorksForSelected = computed(() => {
  if (!selectedMotorcycle.value) return false
  const hasLegacy = allWorks.value.some(m => String(m.motorcycle.id) === String(selectedMotorcycle.value!.id))
  const hasEvents = events.value.some(e => String(e.motorcycle_id) === String(selectedMotorcycle.value!.id))
  return !hasLegacy && !hasEvents
})

// --- ВИДЖЕТЫ СПРАВА ---
const upcomingMaintenances = computed(() => {
  return plannedList.value
    .sort((a, b) => {
      if (a.planned_date && b.planned_date) return a.planned_date.localeCompare(b.planned_date)
      if (a.planned_date) return -1
      if (b.planned_date) return 1
      return (a.planned_mileage || 0) - (b.planned_mileage || 0)
    })
    .slice(0, 3)
})

// --- ФОРМАТИРОВАНИЕ ---
const formatDate = (isoStr?: string | null) => {
  if (!isoStr) return ''
  return new Date(isoStr).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short', year: 'numeric' })
}
const formatMileage = (val?: number | null) => {
  if (!val) return ''
  return new Intl.NumberFormat('ru-RU').format(val) + ' км'
}
const formatCost = (val?: number | null) => {
  if (!val) return '0 ₽'
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', maximumFractionDigits: 0 }).format(val)
}

function getMotoName(motoId: number) {
  return motorcycles.value?.find(m => m.id === motoId)?.name || 'Мотоцикл'
}

// --- ОБРАБОТЧИКИ ---
function openCreate() {
  editingMaintenance.value = null
  isLegacyFormOpen.value = true
}

function openEdit(m: Maintenance) {
  selectedMaintenance.value = null
  editingMaintenance.value = m
  isLegacyFormOpen.value = true
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
  if (selectedMotorcycle.value) quickStartMotorcycle.value = selectedMotorcycle.value
}

// Обработчики событий
function openEventCreate() {
  editingEvent.value = null
  isEventFormOpen.value = true
}
function openEventEdit(e: MaintenanceEvent) {
  selectedEvent.value = null
  editingEvent.value = e
  isEventFormOpen.value = true
}
function onEventFormDone() {
  isEventFormOpen.value = false
  editingEvent.value = null
  loadEvents()
  refresh() // Для обновления пробега и компонентов
}
async function confirmDeleteEvent() {
  if (!deletingEvent.value) return
  try {
    await api.maintenance.events.remove(deletingEvent.value.id, deletingEvent.value.motorcycle_id)
    toast.success('Событие удалено')
    deletingEvent.value = null
    loadEvents()
    refresh()
  } catch (e: any) {
    toast.error(e?.message || 'Не удалось удалить событие')
  }
}

function onQuickStartDone() { quickStartMotorcycle.value = null; refresh() }
function onFormDone() { isLegacyFormOpen.value = false; editingMaintenance.value = null; refresh() }
function onCompleted() { completingMaintenance.value = null; refresh() }
function onDelete() { deletingMaintenance.value = null; refresh() }

const motoOptions = computed(() => [
  { value: 'all', label: 'Все мотоциклы' },
  ...(motorcycles.value || []).map(m => ({ value: m.id, label: m.name }))
])
</script>

<template>
  <div class="center-page">
    <!-- Заголовок -->
    <header class="page-header">
      <div>
        <h1 class="page-title">Центр обслуживания</h1>
        <p class="page-subtitle">Планируйте работы и ведите историю обслуживания</p>
      </div>
      <div class="header-actions">
        <BaseButton v-if="motorcycles?.length" variant="primary" @click="openEventCreate">
          <template #icon><i class="fa-solid fa-layer-group"></i></template>
          Создать событие
        </BaseButton>
      </div>
    </header>

    <!-- LEGACY МОДАЛКИ -->
    <BaseModal v-if="isLegacyFormOpen" :title="editingMaintenance ? 'Редактировать запись' : 'Новая запись'" @close="isLegacyFormOpen = false">
      <MaintenanceForm :motorcycles="motorcycles || []" :default-motorcycle-id="motorcycles?.[0]?.id" :initial-data="editingMaintenance" @created="onFormDone" @updated="onFormDone" @cancel="isLegacyFormOpen = false" />
    </BaseModal>

    <MaintenanceDetailsModal v-if="selectedMaintenance" :maintenance="selectedMaintenance" @close="selectedMaintenance = null" @updated="refresh(); selectedMaintenance = null" @edit="openEdit(selectedMaintenance)" @complete="openComplete(selectedMaintenance)" @delete="openDelete(selectedMaintenance)" />
    <CompleteMaintenanceModal v-if="completingMaintenance" :maintenance="completingMaintenance" @close="completingMaintenance = null" @completed="onCompleted" />
    <DeleteMaintenanceModal v-if="deletingMaintenance" :maintenance="deletingMaintenance" @close="deletingMaintenance = null" @deleted="onDelete" />
    <QuickStartModal v-if="quickStartMotorcycle" :motorcycle="quickStartMotorcycle" @close="quickStartMotorcycle = null" @created="onQuickStartDone" />

    <!-- EVENT МОДАЛКИ -->
    <BaseModal v-if="isEventFormOpen" :title="editingEvent ? 'Редактировать событие' : 'Новое событие обслуживания'" @close="isEventFormOpen = false">
      <MaintenanceEventForm
        :motorcycle-id="editingEvent?.motorcycle_id || (selectedMotorcycle?.id || motorcycles?.[0]?.id || 0)"
        :current-mileage="motorcycles?.find(m => m.id === (editingEvent?.motorcycle_id || (selectedMotorcycle?.id || motorcycles?.[0]?.id)))?.mileage ?? null"
        :components="allComponents.filter(c => c.motorcycle_id === (editingEvent?.motorcycle_id || (selectedMotorcycle?.id || motorcycles?.[0]?.id)))"
        :event="editingEvent"
        @saved="onEventFormDone"
        @cancel="isEventFormOpen = false"
      />
    </BaseModal>

    <MaintenanceEventDetailsModal
      v-if="selectedEvent"
      :event="selectedEvent"
      @close="selectedEvent = null"
      @edit="openEventEdit(selectedEvent!)"
      @delete="deletingEvent = selectedEvent; selectedEvent = null"
    />

    <BaseModal v-if="deletingEvent" title="Удалить событие?" @close="deletingEvent = null">
      <p>Вы уверены, что хотите удалить это событие? История работ по компонентам будет пересчитана.</p>
      <template #footer>
        <BaseButton variant="ghost" size="sm" @click="deletingEvent = null">Отмена</BaseButton>
        <BaseButton variant="danger" size="sm" @click="confirmDeleteEvent">Удалить</BaseButton>
      </template>
    </BaseModal>

    <!-- Загрузка / Ошибки / Пустой гараж -->
    <div v-if="pending" class="loading">
      <BaseSkeleton height="80px" rounded />
      <BaseSkeleton height="200px" rounded />
    </div>
    <div v-else-if="error" class="error">
      <p>Не удалось загрузить данные.</p>
      <BaseButton @click="refresh()">Повторить</BaseButton>
    </div>
    <template v-else-if="motorcycles?.length === 0">
      <BaseEmptyState title="Гараж пуст" description="Сначала добавьте мотоцикл, чтобы отслеживать его обслуживание.">
        <template #action>
          <BaseButton to="/garage/new" variant="primary">Добавить мотоцикл</BaseButton>
        </template>
      </BaseEmptyState>
    </template>

    <!-- Основной контент -->
    <template v-else>
      <!-- Сводка (4 карточки) -->
      <div class="stats-grid">
        <BaseCard padding="md" class="stat-card">
          <div class="stat-icon"><i class="fa-regular fa-calendar"></i></div>
          <div class="stat-info">
            <span class="stat-label">В плане</span>
            <span class="stat-value">{{ plannedList.length }}</span>
          </div>
        </BaseCard>
        <BaseCard padding="md" class="stat-card stat-card--danger">
          <div class="stat-icon"><i class="fa-solid fa-triangle-exclamation"></i></div>
          <div class="stat-info">
            <span class="stat-label">Просрочено</span>
            <span class="stat-value text-danger">{{ overdueList.length }}</span>
          </div>
        </BaseCard>
        <BaseCard padding="md" class="stat-card">
          <div class="stat-icon"><i class="fa-regular fa-circle-check"></i></div>
          <div class="stat-info">
            <span class="stat-label">Выполнено за 12 мес.</span>
            <span class="stat-value">{{ completedLast12m.length + filteredEvents.filter(e => new Date(e.date) >= twelveMonthsAgo).length }}</span>
          </div>
        </BaseCard>
        <BaseCard padding="md" class="stat-card">
          <div class="stat-icon"><i class="fa-solid fa-coins"></i></div>
          <div class="stat-info">
            <span class="stat-label">Расходы</span>
            <span class="stat-value text-success">{{ formatCost(totalCost) }}</span>
          </div>
        </BaseCard>
      </div>

      <!-- Сетка: Левая часть (Фильтры + Таблица) и Правая часть (Виджеты) -->
      <div class="main-layout">
        <!-- ЛЕВАЯ КОЛОНКА -->
        <div class="main-col">
          <!-- Фильтры -->
          <div class="filters-bar">
            <BaseSelect v-model="filterMotorcycleId" :options="motoOptions" class="filter-select" />
            <div class="search-box">
              <i class="fa-solid fa-magnifying-glass"></i>
              <input v-model="searchQuery" type="text" placeholder="Поиск..." class="search-input" />
            </div>

            <!-- Переключатель типа плана -->
            <BaseSelect
              v-if="activeTab === 'planned'"
              v-model="filterBy"
              :options="[
                { value: 'all', label: 'Все планы' },
                { value: 'date', label: 'По дате' },
                { value: 'mileage', label: 'По пробегу' }
              ]"
              class="filter-select"
              style="max-width: 150px;"
            />

            <div class="filters-actions">
              <button class="btn-sort" @click="sortAsc = !sortAsc">
                <i class="fa-solid fa-arrow-down-up-across-line"></i> {{ sortAsc ? 'По возрастанию' : 'По убыванию' }}
              </button>
            </div>
          </div>

          <!-- Баннер быстрого старта -->
          <div v-if="hasNoWorksForSelected && selectedMotorcycle" class="quick-start-banner">
            <div class="banner-content">
              <div class="banner-icon"><i class="fa-solid fa-wand-magic-sparkles"></i></div>
              <div>
                <h3 class="banner-title">У {{ selectedMotorcycle.name }} пока нет обслуживаний</h3>
                <p class="banner-text">Сгенерируйте базовый план ТО за 10 секунд на основе вашего стиля езды.</p>
              </div>
            </div>
            <BaseButton variant="primary" @click="openQuickStart" class="banner-btn">Настроить</BaseButton>
          </div>

          <!-- Табы -->
          <div class="tabs">
            <button class="tab-btn" :class="{ 'tab-btn--active': activeTab === 'events' }" @click="activeTab = 'events'">
              События <span v-if="filteredEvents.length" class="badge">{{ filteredEvents.length }}</span>
            </button>
            <button class="tab-btn" :class="{ 'tab-btn--active': activeTab === 'planned' }" @click="activeTab = 'planned'">
              План <span v-if="planned.length" class="badge">{{ planned.length }}</span>
            </button>
            <button class="tab-btn" :class="{ 'tab-btn--active': activeTab === 'history' }" @click="activeTab = 'history'">
              Старая история <span v-if="history.length" class="badge">{{ history.length }}</span>
            </button>
          </div>

          <!-- СПИСОК (Таблица) -->
          <div class="list-container">
            <div v-if="activeTab === 'events' && filteredEvents.length === 0" class="empty-list">Событий пока нет.</div>
            <div v-if="activeTab === 'planned' && planned.length === 0" class="empty-list">Нет запланированных работ.</div>
            <div v-if="activeTab === 'history' && history.length === 0" class="empty-list">Старая история обслуживания пуста.</div>

            <!-- СОБЫТИЯ -->
            <template v-if="activeTab === 'events'">
              <div v-for="e in filteredEvents" :key="e.id" class="table-row" @click="selectedEvent = e">
                <div class="row-moto">
                  <span class="moto-badge">{{ getMotoName(e.motorcycle_id) }}</span>
                </div>
                <div class="row-title">
                  <span class="work-title">{{ e.works.map(w => w.title).filter(Boolean).join(' · ') || 'Событие обслуживания' }}</span>
                  <span v-if="e.comment" class="work-desc">{{ e.comment }}</span>
                </div>
                <div class="row-date">
                  <span class="meta-item"><i class="fa-regular fa-calendar-check"></i> {{ formatDate(e.date) }}</span>
                  <span v-if="e.mileage" class="meta-item"><i class="fa-solid fa-gauge-high"></i> {{ formatMileage(e.mileage) }}</span>
                </div>
                <div class="row-status">
                  <span class="status-pill status-completed">Событие</span>
                  <span v-if="e.total_cost" class="work-cost">{{ formatCost(e.total_cost) }}</span>
                </div>
                <div class="row-actions">
                  <button class="action-btn" @click.stop="selectedEvent = e"><i class="fa-solid fa-ellipsis"></i></button>
                </div>
              </div>
            </template>

            <!-- ПЛАНЫ -->
            <template v-else-if="activeTab === 'planned'">
              <div v-for="m in planned" :key="`${m.motorcycle.id}-${m.id}`" class="table-row" @click="openDetails(m)">
                <div class="row-moto">
                  <span class="moto-badge">{{ m.motorcycle.name }}</span>
                </div>
                <div class="row-title">
                  <span class="work-title">{{ m.title }}</span>
                  <span v-if="m.description" class="work-desc">{{ m.description }}</span>
                </div>
                <div class="row-date">
                  <span v-if="m.planned_date" class="meta-item"><i class="fa-regular fa-calendar"></i> {{ formatDate(m.planned_date) }}</span>
                  <span v-if="m.planned_mileage" class="meta-item"><i class="fa-solid fa-gauge-high"></i> {{ formatMileage(m.planned_mileage) }}</span>
                </div>
                <div class="row-status">
                  <span class="status-pill status-planned">В плане</span>
                </div>
                <div class="row-actions">
                  <button class="action-btn" @click.stop="openEdit(m)"><i class="fa-solid fa-pen"></i></button>
                  <button class="action-btn" @click.stop="openDetails(m)"><i class="fa-solid fa-ellipsis"></i></button>
                </div>
              </div>
            </template>

            <!-- СТАРАЯ ИСТОРИЯ -->
            <template v-else-if="activeTab === 'history'">
              <div v-for="m in history" :key="`${m.motorcycle.id}-${m.id}`" class="table-row" @click="openDetails(m)">
                <div class="row-moto">
                  <span class="moto-badge">{{ m.motorcycle.name }}</span>
                </div>
                <div class="row-title">
                  <span class="work-title">{{ m.title }}</span>
                  <span v-if="m.description" class="work-desc">{{ m.description }}</span>
                </div>
                <div class="row-date">
                  <span v-if="m.completed_date" class="meta-item"><i class="fa-regular fa-calendar-check"></i> {{ formatDate(m.completed_date) }}</span>
                  <span v-if="m.completed_mileage" class="meta-item"><i class="fa-solid fa-gauge-high"></i> {{ formatMileage(m.completed_mileage) }}</span>
                </div>
                <div class="row-status">
                  <span class="status-pill status-completed">Выполнено</span>
                  <span v-if="m.cost" class="work-cost">{{ formatCost(m.cost) }}</span>
                </div>
                <div class="row-actions">
                  <button class="action-btn" @click.stop="openDetails(m)"><i class="fa-solid fa-ellipsis"></i></button>
                </div>
              </div>
            </template>
          </div>
        </div>

        <!-- ПРАВАЯ КОЛОНКА -->
        <div class="side-col">
          <!-- Ближайшее обслуживание -->
          <BaseCard padding="md" class="widget-card">
            <h3 class="widget-title"><i class="fa-regular fa-calendar-days"></i> Ближайшее обслуживание</h3>
            <div class="widget-list">
              <div v-if="upcomingMaintenances.length === 0" class="widget-empty">Нет запланированных работ.</div>
              <div v-for="m in upcomingMaintenances" :key="m.id" class="widget-item">
                <div class="wi-header">
                  <span class="wi-title">{{ m.title }}</span>
                  <span class="wi-date">
                    {{ m.planned_date ? formatDate(m.planned_date) : (m.planned_mileage ? formatMileage(m.planned_mileage) : '') }}
                  </span>
                </div>
                <div class="wi-moto">{{ m.motorcycle.name }}</div>
              </div>
            </div>
          </BaseCard>

          <!-- Расходы на обслуживание -->
          <BaseCard padding="md" class="widget-card">
            <h3 class="widget-title"><i class="fa-solid fa-sack-dollar"></i> Расходы на обслуживание</h3>
            <div class="expenses-list">
              <div class="expense-item">
                <span class="expense-label">За 12 месяцев</span>
                <span class="expense-value">{{ formatCost(costLast12m) }}</span>
              </div>
              <div class="expense-item">
                <span class="expense-label">За всё время</span>
                <span class="expense-value">{{ formatCost(totalCost) }}</span>
              </div>
            </div>
          </BaseCard>
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
  gap: var(--space-5);
}

/* Заголовок */
.page-header {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);

  @include sm-up {
    flex-direction: row;
    align-items: center;
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

/* Сводка (4 карточки) */
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
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  background: var(--color-surface-secondary);
  color: var(--color-brand);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.stat-card--danger .stat-icon { color: var(--color-danger); }
.stat-card--danger { border-color: rgba(239, 68, 68, 0.2); }

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: var(--text-xs);
  text-transform: uppercase;
  color: var(--color-text-tertiary);
  font-weight: var(--fw-medium);
}

.stat-value {
  font-size: var(--text-xl);
  font-weight: var(--fw-bold);
}
.text-danger { color: var(--color-danger); }
.text-success { color: var(--color-success); }

/* Сетка контента */
.main-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-5);

  @include lg-up {
    grid-template-columns: 1fr 320px;
  }
}

.main-col {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

/* Фильтры */
.filters-bar {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  align-items: center;
}

.filter-select {
  width: 100%;
  max-width: 250px;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 200px;

  i {
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--color-text-tertiary);
  }
}

.search-input {
  width: 100%;
  padding: var(--space-2) var(--space-3) var(--space-2) 36px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text);
  font-size: var(--text-sm);

  &:focus {
    outline: none;
    border-color: var(--color-brand);
  }
}

.btn-sort {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    border-color: var(--color-text-tertiary);
  }
}

/* Баннер */
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
  margin-bottom: var(--space-1);
}
.banner-text {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
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
  background: none;
  border: none;
  cursor: pointer;

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

/* Список / Таблица */
.list-container {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.empty-list {
  padding: var(--space-6);
  text-align: center;
  color: var(--color-text-secondary);
}

.table-row {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--color-border-light);
  background: var(--color-surface);
  cursor: pointer;
  transition: background 0.2s;
  position: relative;

  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 3px;
    background: transparent;
  }

  &:hover {
    background: var(--color-surface-secondary);

    .row-actions {
      opacity: 1;
    }
  }

  &:last-child {
    border-bottom: none;
  }

  @include md-up {
    grid-template-columns: 180px 1fr 180px 120px 80px;
    align-items: center;
    gap: var(--space-4);
  }
}

.row-moto {
  display: flex;
  align-items: center;
}

.moto-badge {
  font-size: var(--text-xs);
  font-weight: var(--fw-semibold);
  color: var(--color-brand);
  background: var(--color-brand-soft);
  padding: 4px 10px;
  border-radius: var(--radius-full);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.row-title {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.work-title {
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  color: var(--color-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.work-desc {
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.row-date {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.row-status {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
}

.status-pill {
  font-size: 11px;
  font-weight: var(--fw-medium);
  padding: 2px 8px;
  border-radius: var(--radius-full);
}
.status-planned { background: rgba(245, 158, 11, 0.15); color: var(--color-warning); }
.status-completed { background: rgba(34, 197, 94, 0.15); color: var(--color-success); }

.work-cost {
  font-size: var(--text-xs);
  font-weight: var(--fw-semibold);
  color: var(--color-text);
}

.row-actions {
  display: flex;
  gap: var(--space-1);
  justify-content: flex-end;
  opacity: 0.6;
  transition: opacity 0.2s;

  @media (max-width: 768px) {
    opacity: 1;
    justify-content: flex-start;
  }
}

.action-btn {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    border-color: var(--color-brand);
    color: var(--color-brand);
  }
}

/* Правая колонка (Виджеты) */
.side-col {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.widget-card {
  display: flex;
  flex-direction: column;
}

.widget-title {
  font-size: var(--text-base);
  font-weight: var(--fw-semibold);
  margin-bottom: var(--space-3);
  display: flex;
  align-items: center;
  gap: var(--space-2);

  i {
    color: var(--color-brand);
  }
}

.widget-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.widget-empty {
  font-size: var(--text-sm);
  color: var(--color-text-tertiary);
}

.widget-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding-bottom: var(--space-3);
  border-bottom: 1px solid var(--color-border-light);

  &:last-child {
    padding-bottom: 0;
    border-bottom: none;
  }
}

.wi-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-2);
}

.wi-title {
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  color: var(--color-text);
}

.wi-date {
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
  white-space: nowrap;
}

.wi-moto {
  font-size: var(--text-xs);
  color: var(--color-brand);
}

.expenses-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.expense-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.expense-label {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.expense-value {
  font-size: var(--text-base);
  font-weight: var(--fw-bold);
  color: var(--color-text);
}
</style>
