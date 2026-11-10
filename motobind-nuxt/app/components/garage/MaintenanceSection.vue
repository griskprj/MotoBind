<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import type { Maintenance, MaintenanceEvent, Motorcycle, MotorcycleComponent } from '~/types'

const props = defineProps<{ motorcycle: Motorcycle }>()
const emit = defineEmits<{ updated: [] }>()

const api = useApi()
const toast = useToast()

const activeTab = ref<'planned' | 'history'>('history')

// LEGACY
const editingMaintenance = ref<Maintenance | null>(null)
const selectedMaintenance = ref<Maintenance | null>(null)
const completingMaintenance = ref<Maintenance | null>(null)
const deletingMaintenance = ref<Maintenance | null>(null)

const planned = computed(() =>
  (props.motorcycle.maintenances || [])
    .filter((m) => m.status === 'planned')
    .sort((a, b) => {
      if (a.planned_date && b.planned_date) return a.planned_date.localeCompare(b.planned_date)
      if (a.planned_mileage != null && b.planned_mileage != null) return a.planned_mileage - b.planned_mileage
      return 0
    }),
)

function openEdit(m: Maintenance) { selectedMaintenance.value = null; editingMaintenance.value = m }
function openDetails(m: Maintenance) { selectedMaintenance.value = m }
function openComplete(m: Maintenance) { selectedMaintenance.value = null; completingMaintenance.value = m }
function openDelete(m: Maintenance) { selectedMaintenance.value = null; deletingMaintenance.value = m }
function onFormDone() { editingMaintenance.value = null; emit('updated') }
function onCompleted() { completingMaintenance.value = null; emit('updated') }
function onDeleteDone() { deletingMaintenance.value = null; emit('updated') }

// EVENTS
const events = ref<MaintenanceEvent[]>([])
const eventsLoading = ref(false)
const components = ref<MotorcycleComponent[]>([])
const selectedEvent = ref<MaintenanceEvent | null>(null)
const isEventFormOpen = ref(false)
const editingEvent = ref<MaintenanceEvent | null>(null)
const deletingEvent = ref<MaintenanceEvent | null>(null)

async function loadEvents() {
  eventsLoading.value = true
  try {
    const res = await api.maintenance.events.list(props.motorcycle.id, { per_page: 100 })
    events.value = res.events
  } catch {
    events.value = []
  } finally {
    eventsLoading.value = false
  }
}

async function loadComponents() {
  try {
    const res = await api.components.list(props.motorcycle.id)
    components.value = res.components
  } catch {
    components.value = []
  }
}

onMounted(() => {
  loadEvents()
  loadComponents()
})

function openEventCreate() { editingEvent.value = null; isEventFormOpen.value = true }
function openEventEdit(e: MaintenanceEvent) { selectedEvent.value = null; editingEvent.value = e; isEventFormOpen.value = true }
function onEventFormDone() { isEventFormOpen.value = false; editingEvent.value = null; loadEvents(); emit('updated') }
async function confirmDeleteEvent() {
  if (!deletingEvent.value) return
  try {
    await api.maintenance.events.remove(deletingEvent.value.id, props.motorcycle.id)
    toast.success('Событие удалено')
    deletingEvent.value = null
    loadEvents()
    emit('updated')
  } catch (e: any) {
    toast.error(e?.message || 'Не удалось удалить событие')
  }
}

// ОБЪЕДИНЕННЫЙ ТАЙМЛАЙН
type TimelineItem =
  | { source: 'legacy'; date: string; item: Maintenance }
  | { source: 'event'; date: string; item: MaintenanceEvent }

const combinedHistory = computed<TimelineItem[]>(() => {
  const legacy: TimelineItem[] = (props.motorcycle.maintenances || [])
    .filter((m) => m.status === 'completed')
    .map((m) => ({ source: 'legacy', date: m.completed_date || m.created_at?.slice(0, 10) || '', item: m }))
  const ev: TimelineItem[] = events.value.map((e) => ({ source: 'event', date: e.date, item: e }))
  return [...legacy, ...ev].sort((a, b) => (b.date || '').localeCompare(a.date || ''))
})

const groupedHistory = computed<Record<string, TimelineItem[]>>(() => {
  const groups: Record<string, TimelineItem[]> = {}
  for (const it of combinedHistory.value) {
    const year = it.date ? new Date(it.date).getFullYear().toString() : 'Без даты'
    if (!groups[year]) groups[year] = []
    groups[year].push(it)
  }
  return groups
})

function onTimelineItemClick(entry: TimelineItem) {
  if (entry.source === 'legacy') openDetails(entry.item)
  else selectedEvent.value = entry.item
}

// СТАТИСТИКА
function timelineCost(it: TimelineItem): number {
  if (it.source === 'legacy') return it.item.cost || 0
  return it.item.total_cost || 0
}

function timelineMileage(it: TimelineItem): number | null {
  if (it.source === 'legacy') return it.item.completed_mileage ?? null
  return it.item.mileage ?? null
}

const stats = computed(() => {
  const totalCost = combinedHistory.value.reduce((sum, it) => sum + timelineCost(it), 0)
  const totalEvents = combinedHistory.value.length
  const lastMileage = combinedHistory.value.map((it) => timelineMileage(it)).find((v) => v != null)
  return { totalCost, totalEvents, currentMileage: props.motorcycle.mileage || lastMileage || 0 }
})

const costChartData = computed(() => {
  const monthsData: { label: string; value: number }[] = []
  const now = new Date()
  for (let i = 7; i >= 0; i--) {
    const d = new Date(now.getFullYear(), now.getMonth() - i, 1)
    monthsData.push({ label: d.toLocaleString('ru-RU', { month: 'short' }), value: 0 })
  }
  for (const it of combinedHistory.value) {
    if (!it.date) continue
    const cost = timelineCost(it)
    if (!cost) continue
    const d = new Date(it.date)
    const label = d.toLocaleString('ru-RU', { month: 'short' })
    const monthObj = monthsData.find((m) => m.label === label)
    if (monthObj) monthObj.value += cost
  }
  return monthsData
})

function formatDate(dateStr?: string | null) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short', year: 'numeric' })
}

function eventTitle(e: MaintenanceEvent): string {
  const titles = e.works.map((w) => w.title).filter((t): t is string => !!t)
  return titles.length ? titles.join(' · ') : 'Событие обслуживания'
}

function eventSubtitle(e: MaintenanceEvent): string {
  if (e.comment) return e.comment
  return `${e.works.length} работ`
}
</script>

<template>
  <div class="m-section">
    <div class="m-header">
      <div class="m-header-title">
        <div class="m-icon-badge"><i class="fa-solid fa-layer-group"></i></div>
        <div>
          <h2 class="m-title">История мотоцикла</h2>
          <p class="m-subtitle">Все события: обслуживание, ремонты, замены</p>
        </div>
      </div>
      <BaseButton variant="primary" @click="openEventCreate">
        <template #icon><i class="fa-solid fa-plus"></i></template>
        Создать событие
      </BaseButton>
    </div>

    <MaintenanceStats :maintenances="motorcycle.maintenances || []" />

    <!-- LEGACY МОДАЛКИ -->
    <BaseModal v-if="editingMaintenance" title="Редактировать запись" @close="editingMaintenance = null">
      <MaintenanceForm :motorcycles="[motorcycle]" :default-motorcycle-id="motorcycle.id" :initial-data="editingMaintenance" @updated="onFormDone" @cancel="editingMaintenance = null" />
    </BaseModal>
    <MaintenanceDetailsModal v-if="selectedMaintenance" :maintenance="{ ...selectedMaintenance, motorcycle: motorcycle }" @close="selectedMaintenance = null" @updated="emit('updated'); selectedMaintenance = null" @edit="openEdit(selectedMaintenance!)" @complete="openComplete(selectedMaintenance!)" @delete="openDelete(selectedMaintenance!)" />
    <CompleteMaintenanceModal v-if="completingMaintenance" :maintenance="completingMaintenance" @close="completingMaintenance = null" @completed="onCompleted" />
    <DeleteMaintenanceModal v-if="deletingMaintenance" :maintenance="deletingMaintenance" @close="deletingMaintenance = null" @deleted="onDeleteDone" />

    <!-- EVENT МОДАЛКИ -->
    <MaintenanceEventDetailsModal v-if="selectedEvent" :event="selectedEvent" @close="selectedEvent = null" @edit="openEventEdit(selectedEvent!)" @delete="deletingEvent = selectedEvent; selectedEvent = null" />
    <BaseModal v-if="isEventFormOpen" :title="editingEvent ? 'Редактировать событие' : 'Новое событие обслуживания'" @close="isEventFormOpen = false">
      <MaintenanceEventForm :motorcycle-id="motorcycle.id" :current-mileage="motorcycle.mileage ?? null" :components="components" :event="editingEvent" @saved="onEventFormDone" @cancel="isEventFormOpen = false" />
    </BaseModal>
    <BaseModal v-if="deletingEvent" title="Удалить событие?" @close="deletingEvent = null">
      <p>Вы уверены, что хотите удалить событие от <strong>{{ new Date(deletingEvent.date).toLocaleDateString('ru-RU') }}</strong>? История работ по компонентам будет пересчитана.</p>
      <template #footer>
        <BaseButton variant="ghost" size="sm" @click="deletingEvent = null">Отмена</BaseButton>
        <BaseButton variant="danger" size="sm" @click="confirmDeleteEvent">Удалить</BaseButton>
      </template>
    </BaseModal>

    <!-- ОСНОВНОЙ КОНТЕНТ -->
    <div class="m-layout">
      <div class="m-main-col">
        <div class="m-tabs">
          <button class="m-tab-btn" :class="{ 'm-tab-btn--active': activeTab === 'planned' }" @click="activeTab = 'planned'">
            Планы <span v-if="planned.length" class="badge">{{ planned.length }}</span>
          </button>
          <button class="m-tab-btn" :class="{ 'm-tab-btn--active': activeTab === 'history' }" @click="activeTab = 'history'">
            История <span v-if="combinedHistory.length" class="badge">{{ combinedHistory.length }}</span>
          </button>
        </div>

        <div v-if="activeTab === 'planned'" class="m-content">
          <div v-if="planned.length === 0" class="m-empty"><p>Нет запланированных работ.</p></div>
          <div v-else class="m-list">
            <MaintenanceItem v-for="m in planned" :key="m.id" :maintenance="m" @click="openDetails(m)" @complete="openComplete(m)" @delete="openDelete(m)" />
          </div>
        </div>

        <div v-else class="m-content">
          <div v-if="eventsLoading" class="m-empty"><p>Загрузка истории…</p></div>
          <div v-else-if="combinedHistory.length === 0" class="m-empty"><p>История обслуживания пуста.</p></div>
          <div v-else class="timeline">
            <div v-for="(items, year) in groupedHistory" :key="year" class="timeline-year-group">
              <div class="timeline-year"><span>{{ year }}</span></div>
              <div class="timeline-items">
                <div v-for="entry in items" :key="`${entry.source}-${entry.item.id}`" class="timeline-item" @click="onTimelineItemClick(entry)">
                  <div class="timeline-marker" :class="{ 'timeline-marker--event': entry.source === 'event' }"></div>
                  <div class="timeline-card">
                    <div class="tc-header">
                      <span class="tc-date">
                        {{ formatDate(entry.date) }}
                        <BaseBadge v-if="entry.source === 'event'" variant="neutral" size="sm">событие</BaseBadge>
                      </span>
                      <span class="tc-mileage">
                        <template v-if="entry.source === 'legacy'">{{ entry.item.completed_mileage ? `${entry.item.completed_mileage.toLocaleString('ru-RU')} км` : '' }}</template>
                        <template v-else>{{ entry.item.mileage ? `${entry.item.mileage.toLocaleString('ru-RU')} км` : '' }}</template>
                      </span>
                    </div>
                    <div class="tc-body">
                      <div class="tc-icon"><i class="fa-solid fa-wrench"></i></div>
                      <div class="tc-info">
                        <template v-if="entry.source === 'legacy'">
                          <h4 class="tc-title">{{ entry.item.title }}</h4>
                          <p class="tc-desc">{{ entry.item.description || entry.item.category }}</p>
                        </template>
                        <template v-else>
                          <h4 class="tc-title">{{ eventTitle(entry.item) }}</h4>
                          <p class="tc-desc">{{ eventSubtitle(entry.item) }}</p>
                        </template>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="m-side-col">
        <div class="m-widget">
          <h3 class="widget-title">Сводка</h3>
          <div class="summary-grid">
            <div class="summary-item">
              <i class="fa-solid fa-gauge-high"></i>
              <div class="summary-val">{{ stats.currentMileage.toLocaleString('ru-RU') }} км</div>
              <div class="summary-lbl">Текущий пробег</div>
            </div>
            <div class="summary-item">
              <i class="fa-solid fa-calendar-check"></i>
              <div class="summary-val">{{ stats.totalEvents }}</div>
              <div class="summary-lbl">Событий</div>
            </div>
            <div class="summary-item">
              <i class="fa-solid fa-sack-dollar"></i>
              <div class="summary-val">{{ stats.totalCost.toLocaleString('ru-RU') }} ₽</div>
              <div class="summary-lbl">Затраты</div>
            </div>
          </div>
        </div>
        <div class="m-widget">
          <h3 class="widget-title">Динамика затрат</h3>
          <MaintenanceCostChart :chart-data="costChartData" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.m-section { display: flex; flex-direction: column; gap: var(--space-5); }
.m-list { display: flex; flex-direction: column; gap: var(--space-3); }

.m-layout {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
}

.m-main-col {
  flex: 1 1 600px;
  min-width: 0;
}

.m-side-col {
  flex: 0 1 340px;
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.m-header {
  display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: var(--space-4);
  padding: var(--space-4); background: linear-gradient(90deg, rgba(112, 0, 255, 0.1) 0%, rgba(20, 20, 25, 1) 100%);
  border-radius: var(--radius-lg); border: 1px solid rgba(112, 0, 255, 0.2);
}
.m-header-title { display: flex; align-items: center; gap: var(--space-3); }
.m-icon-badge { width: 48px; height: 48px; background: rgba(112, 0, 255, 0.2); border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; color: #a855f7; font-size: 20px; }
.m-title { font-size: var(--text-xl); font-weight: var(--fw-bold); color: var(--color-text-primary); }
.m-subtitle { font-size: var(--text-sm); color: var(--color-text-secondary); }
.m-tabs { display: flex; border-bottom: 1px solid var(--color-border); gap: var(--space-4); margin-bottom: var(--space-4); }
.m-tab-btn { display: flex; align-items: center; gap: var(--space-2); padding: var(--space-2) 0; font-size: var(--text-base); font-weight: var(--fw-medium); color: var(--color-text-secondary); border-bottom: 2px solid transparent; margin-bottom: -1px; transition: all var(--transition-fast); background: none; border: none; cursor: pointer; }
.m-tab-btn--active { color: var(--color-brand); border-bottom-color: var(--color-brand); }
.badge { background: var(--color-surface-secondary); padding: 2px 8px; border-radius: var(--radius-full); font-size: var(--text-xs); }
.m-empty { padding: var(--space-6); text-align: center; color: var(--color-text-secondary); font-size: var(--text-sm); background: var(--color-surface-secondary); border-radius: var(--radius-md); border: 1px dashed var(--color-border); }
.timeline { display: flex; flex-direction: column; gap: var(--space-4); position: relative; }
.timeline-year-group { display: flex; flex-direction: column; gap: var(--space-3); }
.timeline-year { display: flex; align-items: center; gap: var(--space-2); }
.timeline-year span { font-size: var(--text-xs); font-weight: var(--fw-bold); color: var(--color-brand); background: rgba(112, 0, 255, 0.15); padding: 2px 8px; border-radius: var(--radius-full); }
.timeline-items { display: flex; flex-direction: column; gap: var(--space-3); position: relative; padding-left: var(--space-4); }
.timeline-items::before { content: ''; position: absolute; left: 5px; top: 0; bottom: 0; width: 2px; background: var(--color-border); }
.timeline-item { position: relative; cursor: pointer; }
.timeline-marker { position: absolute; left: -19px; top: 20px; width: 12px; height: 12px; border-radius: 50%; background: var(--color-brand); border: 3px solid var(--color-surface); box-shadow: 0 0 0 2px var(--color-border); z-index: 1; }
.timeline-card { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: var(--space-3); transition: border-color 0.2s, background 0.2s; }
.timeline-card:hover { border-color: rgba(112, 0, 255, 0.4); background: var(--color-surface-secondary); }
.tc-header { display: flex; justify-content: space-between; font-size: var(--text-xs); color: var(--color-text-tertiary); margin-bottom: var(--space-2); }
.tc-mileage { font-weight: var(--fw-semibold); }
.tc-body { display: flex; align-items: flex-start; gap: var(--space-3); }
.tc-icon { width: 32px; height: 32px; border-radius: var(--radius-md); background: rgba(112, 0, 255, 0.1); color: var(--color-brand); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.tc-info { flex: 1; min-width: 0; }
.tc-title { font-size: var(--text-sm); font-weight: var(--fw-semibold); margin-bottom: 2px; word-break: break-word; }
.tc-desc { font-size: var(--text-xs); color: var(--color-text-secondary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.m-widget { min-width: 0; background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: var(--space-4); }
.widget-title { font-size: var(--text-base); font-weight: var(--fw-semibold); margin-bottom: var(--space-3); }
.summary-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-2); text-align: center; }
.summary-item { display: flex; flex-direction: column; align-items: center; gap: var(--space-1); padding: var(--space-2); background: var(--color-surface-secondary); border-radius: var(--radius-md); }
.summary-item i { color: var(--color-brand); font-size: 16px; }
.summary-val { font-size: var(--text-sm); font-weight: var(--fw-bold); }
.summary-lbl { font-size: 10px; color: var(--color-text-tertiary); }
</style>
