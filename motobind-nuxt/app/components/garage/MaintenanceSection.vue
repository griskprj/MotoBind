<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Motorcycle, Maintenance } from '~/types'

const props = defineProps<{ motorcycle: Motorcycle }>()
const emit = defineEmits<{ updated: [] }>()

const api = useApi()
const toast = useToast()

const activeTab = ref<'planned' | 'history'>('history')
const isFormOpen = ref(false)
const editingMaintenance = ref<Maintenance | null>(null)
const selectedMaintenance = ref<Maintenance | null>(null)
const completingMaintenance = ref<Maintenance | null>(null)
const deletingMaintenance = ref<Maintenance | null>(null)

const planned = computed(() =>
  (props.motorcycle.maintenances || [])
    .filter(m => m.status === 'planned')
    .sort((a, b) => {
      if (a.planned_date && b.planned_date) return a.planned_date.localeCompare(b.planned_date)
      return 0
    })
)

const history = computed(() =>
  (props.motorcycle.maintenances || [])
    .filter(m => m.status === 'completed')
    .sort((a, b) => {
      if (a.completed_date && b.completed_date) return b.completed_date.localeCompare(a.completed_date)
      return b.id - a.id
    })
)

const groupedHistory = computed(() => {
  const groups: Record<string, Maintenance[]> = {}
  for (const item of history.value) {
    const year = item.completed_date ? new Date(item.completed_date).getFullYear().toString() : 'Без даты'
    if (!groups[year]) groups[year] = []
    groups[year].push(item)
  }
  return groups
})

const stats = computed(() => {
  const totalCost = history.value.reduce((sum, m) => sum + (m.cost || 0), 0)
  const totalEvents = history.value.length
  let ownershipDays = 0
  if (history.value.length > 0) {
    const dates = history.value.map(m => new Date(m.completed_date || m.created_at).getTime())
    const firstDate = Math.min(...dates)
    ownershipDays = Math.floor((Date.now() - firstDate) / (1000 * 60 * 60 * 24))
  }
  return {
    totalCost,
    totalEvents,
    ownershipDays,
    currentMileage: props.motorcycle.mileage || (history.value[0]?.completed_mileage || 0)
  }
})

const costChartData = computed(() => {
  const monthsData: { label: string, value: number }[] = []
  const now = new Date()

  for (let i = 7; i >= 0; i--) {
    const d = new Date(now.getFullYear(), now.getMonth() - i, 1)
    const label = d.toLocaleString('ru-RU', { month: 'short' })
    monthsData.push({ label, value: 0 })
  }

  for (const item of history.value) {
    if (!item.completed_date || !item.cost) continue
    const d = new Date(item.completed_date)
    const label = d.toLocaleString('ru-RU', { month: 'short' })
    const monthObj = monthsData.find(m => m.label === label)
    if (monthObj) {
      monthObj.value += item.cost
    }
  }

  return monthsData
})

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

function openComplete(m: Maintenance) {
  selectedMaintenance.value = null
  completingMaintenance.value = m
}

function openDelete(m: Maintenance) {
  selectedMaintenance.value = null
  deletingMaintenance.value = m
}

function onFormDone() {
  isFormOpen.value = false
  editingMaintenance.value = null
  emit('updated')
}

function onCompleted() {
  completingMaintenance.value = null
  emit('updated')
}

function onDeleteDone() {
  deletingMaintenance.value = null
  emit('updated')
}

function formatDate(dateStr?: string | null) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short', year: 'numeric' })
}
</script>

<template>
  <div class="m-section">
    <!-- Заголовок с кнопкой -->
    <div class="m-header">
      <div class="m-header-title">
        <div class="m-icon-badge">
          <i class="fa-solid fa-layer-group"></i>
        </div>
        <div>
          <h2 class="m-title">История мотоцикла</h2>
          <p class="m-subtitle">Все события: обслуживание, ремонты, замены и важные заметки</p>
        </div>
      </div>
      <BaseButton v-if="!isFormOpen" variant="primary" @click="openCreate">
        <template #icon><i class="fa-solid fa-plus"></i></template>
        Добавить событие
      </BaseButton>
    </div>

    <MaintenanceStats :maintenances="motorcycle.maintenances || []" />

    <!-- Модалки -->
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
      :maintenance="{ ...selectedMaintenance, motorcycle: motorcycle }"
      @close="selectedMaintenance = null"
      @updated="emit('updated'); selectedMaintenance = null"
      @edit="openEdit(selectedMaintenance!)"
      @complete="openComplete(selectedMaintenance!)"
      @delete="openDelete(selectedMaintenance!)"
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
      @deleted="onDeleteDone"
    />

    <!-- Основной контент -->
    <div v-if="!isFormOpen" class="m-layout">
      <!-- Левая колонка: Таймлайн -->
      <div class="m-main-col">
        <div class="m-tabs">
          <button class="m-tab-btn" :class="{ 'm-tab-btn--active': activeTab === 'planned' }" @click="activeTab = 'planned'">
            Планы <span v-if="planned.length" class="badge">{{ planned.length }}</span>
          </button>
          <button class="m-tab-btn" :class="{ 'm-tab-btn--active': activeTab === 'history' }" @click="activeTab = 'history'">
            История <span v-if="history.length" class="badge">{{ history.length }}</span>
          </button>
        </div>

        <!-- ТАБ: Планы -->
        <div v-if="activeTab === 'planned'" class="m-content">
          <div v-if="planned.length === 0" class="m-empty">
            <p>Нет запланированных работ.</p>
          </div>
          <div v-else class="m-list">
            <MaintenanceItem
              v-for="m in planned"
              :key="m.id"
              :maintenance="m"
              @click="openDetails(m)"
              @complete="openComplete(m)"
              @delete="openDelete(m)"
            />
          </div>
        </div>

        <!-- ТАБ: История (Таймлайн) -->
        <div v-else class="m-content">
          <div v-if="history.length === 0" class="m-empty">
            <p>История обслуживания пуста.</p>
          </div>

          <div v-else class="timeline">
            <div v-for="(items, year) in groupedHistory" :key="year" class="timeline-year-group">
              <div class="timeline-year">
                <span>{{ year }}</span>
              </div>

              <div class="timeline-items">
                <div
                  v-for="m in items"
                  :key="m.id"
                  class="timeline-item"
                  @click="openDetails(m)"
                >
                  <div class="timeline-marker"></div>
                  <div class="timeline-card">
                    <div class="tc-header">
                      <span class="tc-date">{{ formatDate(m.completed_date) }}</span>
                      <span class="tc-mileage">{{ m.completed_mileage }} км</span>
                    </div>
                    <div class="tc-body">
                      <div class="tc-icon">
                        <i class="fa-solid fa-wrench"></i>
                      </div>
                      <div class="tc-info">
                        <h4 class="tc-title">{{ m.title }}</h4>
                        <p class="tc-desc">{{ m.description || m.category }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Правая колонка: Статистика и График -->
      <div class="m-side-col">
        <!-- Сводка -->
        <div class="m-widget">
          <h3 class="widget-title">Сводка</h3>
          <div class="summary-grid">
            <div class="summary-item">
              <i class="fa-solid fa-gauge-high"></i>
              <div class="summary-val">{{ stats.currentMileage.toLocaleString() }} км</div>
              <div class="summary-lbl">Текущий пробег</div>
            </div>
            <div class="summary-item">
              <i class="fa-solid fa-calendar-check"></i>
              <div class="summary-val">{{ stats.totalEvents }}</div>
              <div class="summary-lbl">Событий</div>
            </div>
            <div class="summary-item">
              <i class="fa-solid fa-sack-dollar"></i>
              <div class="summary-val">{{ stats.totalCost.toLocaleString() }} ₽</div>
              <div class="summary-lbl">Затраты</div>
            </div>
          </div>
        </div>

        <!-- График затрат -->
        <div class="m-widget">
          <h3 class="widget-title">Динамика затрат</h3>
          <MaintenanceCostChart :chart-data="costChartData" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.m-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.m-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

/* Заголовок */
.m-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--space-4);
  padding: var(--space-4);
  background: linear-gradient(90deg, rgba(112, 0, 255, 0.1) 0%, rgba(20, 20, 25, 1) 100%);
  border-radius: var(--radius-lg);
  border: 1px solid rgba(112, 0, 255, 0.2);
}

.m-header-title {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.m-icon-badge {
  width: 48px;
  height: 48px;
  background: rgba(112, 0, 255, 0.2);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #a855f7;
  font-size: 20px;
}

.m-title {
  font-size: var(--text-xl);
  font-weight: var(--fw-bold);
  color: var(--color-text-primary);
}

.m-subtitle {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

/* Сетка */
.m-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);

  @include lg-up {
    grid-template-columns: 1fr 340px;
  }
}

/* Табы */
.m-tabs {
  display: flex;
  border-bottom: 1px solid var(--color-border);
  gap: var(--space-4);
  margin-bottom: var(--space-4);
}

.m-tab-btn {
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

/* Пустое состояние */
.m-empty {
  padding: var(--space-6);
  text-align: center;
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  background: var(--color-surface-secondary);
  border-radius: var(--radius-md);
  border: 1px dashed var(--color-border);
}

/* --- ТАЙМЛАЙН --- */
.timeline {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  position: relative;
}

.timeline-year-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.timeline-year {
  display: flex;
  align-items: center;
  gap: var(--space-2);

  span {
    font-size: var(--text-xs);
    font-weight: var(--fw-bold);
    color: var(--color-brand);
    background: rgba(112, 0, 255, 0.15);
    padding: 2px 8px;
    border-radius: var(--radius-full);
  }
}

.timeline-items {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  position: relative;
  padding-left: var(--space-4);

  &::before {
    content: '';
    position: absolute;
    left: 5px;
    top: 0;
    bottom: 0;
    width: 2px;
    background: var(--color-border);
  }
}

.timeline-item {
  position: relative;
  cursor: pointer;
}

.timeline-marker {
  position: absolute;
  left: -19px;
  top: 20px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--color-brand);
  border: 3px solid var(--color-surface);
  box-shadow: 0 0 0 2px var(--color-border);
  z-index: 1;
}

.timeline-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-3);
  transition: border-color 0.2s, background 0.2s;

  &:hover {
    border-color: rgba(112, 0, 255, 0.4);
    background: var(--color-surface-secondary);
  }
}

.tc-header {
  display: flex;
  justify-content: space-between;
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
  margin-bottom: var(--space-2);
}

.tc-mileage {
  font-weight: var(--fw-semibold);
}

.tc-body {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
}

.tc-icon {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
  background: rgba(112, 0, 255, 0.1);
  color: var(--color-brand);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.tc-info {
  flex: 1;
  min-width: 0;
}

.tc-title {
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  margin-bottom: 2px;
}

.tc-desc {
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* --- ПРАВАЯ КОЛОНКА (ВИДЖЕТЫ) --- */
.m-side-col {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.m-widget {
  min-width: 0; /* Важно для ApexCharts */
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
}

.widget-title {
  font-size: var(--text-base);
  font-weight: var(--fw-semibold);
  margin-bottom: var(--space-3);
}

/* Сводка */
.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-2);
  text-align: center;
}

.summary-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-2);
  background: var(--color-surface-secondary);
  border-radius: var(--radius-md);

  i {
    color: var(--color-brand);
    font-size: 16px;
  }
}

.summary-val {
  font-size: var(--text-sm);
  font-weight: var(--fw-bold);
}

.summary-lbl {
  font-size: 10px;
  color: var(--color-text-tertiary);
}
</style>
