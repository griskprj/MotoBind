<template>
  <div class="maintenance-page">
    <LoadingOverlay :isLoading="loading" text="Загрузка обслуживаний..." />

    <div class="container">
      <!-- === HEADER === -->
      <Header
        title="Обслуживание"
        subtitle="Управляйте обслуживанием своих мотоциклов"
      />

      <!-- === STATISTIC SECTION === -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon total">
            <i class="fa fa-wrench"></i>
          </div>
          <div class="stat-info">
            <span class="stat-label">Всего обслуживаний</span>
            <span class="stat-value">{{ counts.all }}</span>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon completed">
            <i class="fa fa-check"></i>
          </div>
          <div class="stat-info">
            <span class="stat-label">Выполнено</span>
            <span class="stat-value">{{ counts.history }}</span>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon planned">
            <i class="fa fa-clock"></i>
          </div>
          <div class="stat-info">
            <span class="stat-label">Запланировано</span>
            <span class="stat-value">{{ counts.planned }}</span>
          </div>
        </div>

        <div class="stat-card" :class="{ 'stat-danger': overdue.length > 0 }">
          <div class="stat-icon overdue">
            <i class="fa fa-exclamation-triangle"></i>
          </div>
          <div class="stat-info">
            <span class="stat-label">Просрочено</span>
            <span class="stat-value" :class="{ 'text-danger': overdue.length > 0 }">
              {{ overdue.length }}
            </span>
          </div>
        </div>
      </div>

      <!-- === FILTERS === -->
      <div class="filters-section">
        <div class="tabs-wrapper">
          <div class="tabs">
            <div class="tabs-btn">
              <button
                v-for="tabItem in tabs"
                :key="tabItem.value"
                class="tab"
                :class="{ active: tab === tabItem.value }"
                @click="setTab(tabItem.value)"
              >
                <i :class="tabItem.icon"></i>
                {{ tabItem.label }}
                <span class="tab-count" v-if="tabItem.value === 'all'">{{ counts.all }}</span>
                <span class="tab-count" v-else-if="tabItem.value === 'planned'">{{ counts.planned }}</span>
                <span class="tab-count" v-else-if="tabItem.value === 'history'">{{ counts.history }}</span>
              </button>
            </div>
            <button
              class="outline-btn"
              style="padding: 10px 24px;"
              @click="showAddMaintenanceModal = true"
            >
              <i class="fa fa-plus" style="min-width: 14px; margin-right: 0;"></i> Добавить обслуживание
            </button>
          </div>
        </div>

        <div class="filters">
          <div class="filter-group">
            <div class="search-wrapper">
              <i class="fa fa-search"></i>
              <input
                type="text"
                :value="filters.search"
                @input="setFilter('search', $event.target.value)"
                placeholder="Поиск по названию, описанию, мотоциклу..."
                class="search-input"
              >
              <button
                v-if="filters.search"
                @click="setFilter('search', '')"
                class="clear-search"
              >
                <i class="fa fa-times"></i>
              </button>
            </div>
          </div>
          <div class="filter-group">
            <select
              :value="filters.motorcycle"
              @change="setFilter('motorcycle', $event.target.value || '')"
              class="filter-select"
            >
              <option value="">Все мотоциклы</option>
              <option
                v-for="motorcycle in motorcycles"
                :key="motorcycle.id"
                :value="motorcycle.id"
              >
                {{ motorcycle.name }}
              </option>
            </select>
            <select
              :value="filters.status"
              @change="setFilter('status', $event.target.value)"
              class="filter-select"
            >
              <option value="">Все статусы</option>
              <option value="completed">✅ Выполнено</option>
              <option value="planned">⏳ Запланировано</option>
              <option value="overdue">⚠️ Просрочено</option>
            </select>
            <select
              :value="sortBy"
              @change="setSortBy($event.target.value)"
              class="filter-select"
            >
              <option value="date_desc">📅 По дате (новые)</option>
              <option value="date_asc">📅 По дате (старые)</option>
              <option value="mileage_desc">📊 По пробегу (макс)</option>
              <option value="mileage_asc">📊 По пробегу (мин)</option>
              <option value="cost_desc">💰 По стоимости (макс)</option>
              <option value="cost_asc">💰 По стоимости (мин)</option>
            </select>
          </div>
        </div>

        <div class="filter-results" v-if="filtered.length > 0 && hasActiveFilters">
          <span>
            <i class="fa fa-filter"></i>
            Найдено: {{ filtered.length }} записей
          </span>
          <button class="clear-filters" @click="clearFilters">
            <i class="fa fa-times"></i> Очистить фильтры
          </button>
        </div>
      </div>

      <!-- === MAINTENANCE LIST === -->
      <div v-if="filtered.length > 0" class="maintenance-list">
        <div
          v-for="maintenance in filtered"
          :key="maintenance.id"
          class="maintenance-card"
          @click="openDetailsMaintenance(maintenance)"
        >
          <div class="card-left">
            <div class="card-icon" :class="getStatusIconClass(maintenance.status)">
              <i :class="getStatusIcon(maintenance.status)"></i>
            </div>
            <div class="card-content">
              <div class="card-header-row">
                <h3 class="card-title">{{ maintenance.title }}</h3>
                <span class="card-date">
                  <i class="fa fa-calendar-alt"></i>
                  {{ getMaintenanceDate(maintenance) }}
                </span>
              </div>
              <div class="card-description" v-if="maintenance.description">
                {{ maintenance.description }}
              </div>
              <div class="card-meta">
                <span class="meta-item">
                  <i class="fa fa-motorcycle"></i>
                  {{ getMotoName(maintenance) }}
                </span>
                <span class="meta-item">
                  <i class="fa-solid fa-gauge-high"></i>
                  {{ getMaintenanceMileage(maintenance) }}
                </span>
                <span class="meta-item" v-if="maintenance.cost">
                  <i class="fa fa-ruble-sign"></i>
                  {{ formatCost(maintenance.cost) }}
                </span>
                <span class="badge" :class="`badge-${getStatusBadgeVariant(maintenance.status)}`">
                  {{ getStatusLabel(maintenance.status) }}
                </span>
              </div>
            </div>
          </div>
          <div class="card-right">
            <i class="fa fa-chevron-right"></i>
          </div>
        </div>
      </div>

      <!-- === EMPTY STATE === -->
      <div v-else class="empty-state">
        <i class="fa fa-wrench"></i>
        <h3 v-if="hasActiveFilters">Ничего не найдено</h3>
        <h3 v-else>Нет записей обслуживания</h3>
        <p class="empty-text" v-if="hasActiveFilters">
          Попробуйте изменить параметры фильтрации
        </p>
        <p class="empty-text" v-else>
          Начните вести учёт обслуживания своих мотоциклов
        </p>
        <button
          v-if="!hasActiveFilters"
          @click="showAddMaintenanceModal = true"
          class="btn-primary"
        >
          Добавить обслуживание
        </button>
        <button v-else @click="clearFilters" class="btn-secondary">
          Сбросить фильтры
        </button>
      </div>
    </div>

    <!-- MODALS -->
    <AddMaintenanceModal
      :isOpen="showAddMaintenanceModal"
      :motorcycles="motorcycles"
      @created="onMaintenanceCreated"
      @close="showAddMaintenanceModal = false"
    />

    <MaintenanceDetailsModal
      v-if="selectedMaintenance"
      :isOpen="showDetailsMaintenanceModal"
      :motorcycle="selectedMotorcycle"
      :maintenance="selectedMaintenance"
      @edit="showDetailsMaintenanceModal = false; showEditModal = true"
      @delete="showDetailsMaintenanceModal = false; showDeleteModal = true"
      @mark="showDetailsMaintenanceModal = false; showMarkModal = true"
      @close="closeDetailsMaintenance"
    />

    <EditMaintenanceModal
      v-if="selectedMaintenance"
      :isOpen="showEditModal"
      :maintenance="selectedMaintenance"
      :motorcycles="motorcycles"
      @close="showEditModal = false; closeDetailsMaintenance()"
    />

    <DeleteMaintenanceModal
      v-if="selectedMaintenance"
      :isOpen="showDeleteModal"
      :maintenanceId="selectedMaintenance.id"
      @submit="confirmDeleteMaintenance"
      @close="showDeleteModal = false"
    />

    <MarkPlanMaintenanceModal
      v-if="selectedMaintenance"
      :isOpen="showMarkModal"
      :maintenance="selectedMaintenance"
      :motorcycle="selectedMotorcycle"
      @submit="handleMarkMaintenance"
      @close="showMarkModal = false"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useMaintenancesStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import {
  formatCost,
  getStatusLabel,
  getStatusBadgeVariant,
} from '@/utils/formatters'
import formatDate from '@/utils/DateFormatter.js'

import AddMaintenanceModal from '../components/modals/maintenance/AddMaintenanceModal.vue'
import MaintenanceDetailsModal from '../components/modals/maintenance/MaintenanceDetailsModal.vue'
import EditMaintenanceModal from '../components/modals/maintenance/EditMaintenanceModal.vue'
import DeleteMaintenanceModal from '../components/modals/maintenance/DeleteMaintenanceModal.vue'
import MarkPlanMaintenanceModal from '../components/modals/maintenance/MarkPlanMaintenanceModal.vue'
import Header from '../components/Header.vue'
import LoadingOverlay from '../components/LoadingOverlay.vue'

const toast = useToast()
const maintenancesStore = useMaintenancesStore()

const {
  motorcycles,
  loading,
  filters,
  tab,
  sortBy,
  completed,
  planned,
  overdue,
  counts,
  filtered,
  hasActiveFilters,
} = storeToRefs(maintenancesStore)

const {
  loadAll,
  setFilter,
  setTab,
  setSortBy,
  clearFilters,
  create,
  remove,
  complete,
} = maintenancesStore

// ===== Local UI state =====
const showAddMaintenanceModal = ref(false)
const showDetailsMaintenanceModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const showMarkModal = ref(false)
const selectedMaintenance = ref(null)

const selectedMotorcycle = computed(() => {
  if (!selectedMaintenance.value) return null
  return motorcycles.value.find((m) => m.id === selectedMaintenance.value.moto_id) || null
})

// ===== Tabs config =====
const tabs = [
  { value: 'all', label: 'Все записи', icon: 'fa fa-list' },
  { value: 'planned', label: 'Плановые', icon: 'fa fa-clock' },
  { value: 'history', label: 'История', icon: 'fa fa-history' },
]

// ===== Lifecycle =====
onMounted(() => {
  loadAll().catch((err) => {
    console.error('Failed to load maintenance data:', err)
    toast.error('Ошибка загрузки данных')
  })
})

// ===== CRUD =====
function onMaintenanceCreated() {
  showAddMaintenanceModal.value = false
}

async function confirmDeleteMaintenance() {
  if (!selectedMaintenance.value) return
  try {
    await maintenancesStore.remove(selectedMaintenance.value.id)
    showDeleteModal.value = false
    closeDetailsMaintenance()
    toast.success('Обслуживание удалено')
  } catch (err) {
    toast.error('Не удалось удалить')
  }
}

async function handleMarkMaintenance(formData) {
  try {
    await maintenancesStore.complete(formData.id, {
      completed_mileage: formData.mileage,
      completed_date: formData.date,
      cost: formData.cost,
      is_repeat: formData.isRepeat,
      interval: formData.interval,
      interval_days: formData.interval_days,
    })
    showMarkModal.value = false
    closeDetailsMaintenance()
    toast.success('Обслуживание завершено')
  } catch (err) {
    toast.error(err.response?.data?.error || 'Ошибка завершения')
  }
}

// ===== Details modal =====
function openDetailsMaintenance(maintenance) {
  selectedMaintenance.value = maintenance
  showDetailsMaintenanceModal.value = true
}

function closeDetailsMaintenance() {
  selectedMaintenance.value = null
  showDetailsMaintenanceModal.value = false
}

// ===== Helpers for template =====
function getMotoName(maintenance) {
  return maintenance.moto_name || '—'
}

function getMaintenanceDate(maintenance) {
  return formatDate(
    maintenance.completed_date || maintenance.planned_date || maintenance.created_at
  )
}

function getMaintenanceMileage(maintenance) {
  if (maintenance.completed_mileage) {
    return `${maintenance.completed_mileage} км`
  }
  if (maintenance.planned_mileage) {
    return `(план) ${maintenance.planned_mileage} км`
  }
  return '—'
}

function getStatusIconClass(status) {
  return {
    completed: 'icon-completed',
    planned: 'icon-planned',
    overdue: 'icon-overdue',
  }[status] || 'icon-gray'
}

function getStatusIcon(status) {
  return {
    completed: 'fa fa-check',
    planned: 'fa fa-clock',
    overdue: 'fa fa-exclamation-triangle',
  }[status] || 'fa fa-circle'
}
</script>

<style scoped>
/* ===== BASE ===== */
.maintenance-page {
  padding: 20px 0 40px;
  max-width: 100%;
  overflow-x: hidden;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
  overflow-x: hidden;
}

/* ===== STATS ===== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 28px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px 20px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: 14px;
  transition: all 0.25s ease;
}

.stat-card:hover {
  border-color: var(--border-color);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.stat-card.stat-danger {
  border-color: var(--danger-trans);
  background: var(--danger-trans);
}

.stat-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.stat-icon.total {
  background: var(--accent-trans);
  color: var(--accent-text);
}

.stat-icon.completed {
  background: var(--success-trans);
  color: var(--success-text);
}

.stat-icon.planned {
  background: var(--warning-trans);
  color: var(--warning-text);
}

.stat-icon.overdue {
  background: var(--danger-trans);
  color: var(--danger-text);
}

.stat-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.stat-label {
  font-size: 12px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.4px;
  font-weight: 600;
}

.stat-value {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-value.text-danger {
  color: var(--danger);
}

/* ===== FILTERS ===== */
.filters-section {
  margin-bottom: 24px;
}

.tabs-wrapper {
  margin-bottom: 16px;
}

.tabs {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--bg-secondary);
  padding: 4px;
  border-radius: 12px;
  border: 1px solid var(--border-light);
}

.tabs-btn {
  display: flex;
  gap: 4px;
  width: 100%;
  margin-bottom: 8px;
}

.tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: transparent;
  border: none;
  border-radius: 8px;
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s ease;
}

.tab:hover {
  color: var(--text-primary);
  background: var(--border-light);
}

.tab.active {
  background: var(--bg-primary);
  color: var(--accent-text);
  box-shadow: var(--shadow-sm);
}

.tab-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  background: var(--bg-primary);
  color: var(--text-muted);
  min-width: 20px;
  height: 20px;
}

.tab.active .tab-count {
  background: var(--accent-trans);
  color: var(--accent-text);
}

.filters {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.filter-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.filter-group:first-child {
  flex: 1;
  min-width: 200px;
}

.search-wrapper {
  display: flex;
  align-items: center;
  position: relative;
  width: 100%;
  background: var(--bg-input);
  border: 1px solid var(--border-input);
  border-radius: 10px;
  transition: border 0.2s;
}

.search-wrapper:focus-within {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-trans);
}

.search-wrapper i {
  position: absolute;
  left: 12px;
  color: var(--text-muted);
  font-size: 14px;
}

.search-input {
  width: 100%;
  padding: 10px 36px 10px 38px;
  background: transparent;
  border: none;
  color: var(--text-primary);
  font-size: 14px;
  outline: none;
}

.search-input::placeholder {
  color: var(--text-muted);
}

.clear-search {
  position: absolute;
  right: 10px;
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: all 0.2s;
}

.clear-search:hover {
  color: var(--text-primary);
  background: var(--border-light);
}

.filter-select {
  padding: 10px 14px;
  background: var(--bg-input);
  border: 1px solid var(--border-input);
  border-radius: 10px;
  color: var(--text-primary);
  font-size: 14px;
  outline: none;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 160px;
  flex: 1;
}

.filter-select:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-trans);
}

.filter-select option {
  background: var(--bg-input);
}

.filter-results {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 16px;
  background: var(--accent-trans);
  border-radius: 10px;
  font-size: 13px;
  color: var(--text-muted);
  margin-top: 8px;
}

.filter-results i {
  color: var(--accent-text);
}

.clear-filters {
  background: transparent;
  border: none;
  color: var(--accent-text);
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
  padding: 4px 12px;
  border-radius: 6px;
}

.clear-filters:hover {
  background: var(--accent-trans);
  color: var(--accent);
}

/* ===== MAINTENANCE LIST ===== */
.maintenance-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.maintenance-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.25s ease;
}

.maintenance-card:hover {
  background: var(--bg-card-hover);
  border-color: var(--border-color);
  transform: translateX(4px);
}

.card-left {
  display: flex;
  gap: 16px;
  flex: 1;
  min-width: 0;
}

.card-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.icon-completed {
  background: var(--success-trans);
  color: var(--success-text);
}

.icon-planned {
  background: var(--warning-trans);
  color: var(--warning-text);
}

.icon-overdue {
  background: var(--danger-trans);
  color: var(--danger-text);
}

.icon-gray {
  background: rgba(107, 114, 128, 0.15);
  color: #9ca3af;
}

.card-content {
  flex: 1;
  min-width: 0;
}

.card-header-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.card-title {
  font-size: 15px;
  font-weight: 600;
  margin: 0;
  color: var(--text-primary);
}

.card-date {
  font-size: 13px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 4px;
}

.card-date i {
  font-size: 12px;
}

.card-description {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 2px;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-top: 4px;
  flex-wrap: wrap;
}

.meta-item {
  font-size: 13px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 4px;
}

.meta-item i {
  font-size: 12px;
  color: var(--text-muted);
}

.card-right {
  color: var(--text-muted);
  padding-left: 12px;
  transition: all 0.25s ease;
}

.maintenance-card:hover .card-right {
  color: var(--accent-text);
  transform: translateX(4px);
}

.badge {
  display: inline-block;
  padding: 3px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 500;
}

.badge-success {
  background: var(--success-trans);
  color: var(--success-text);
}

.badge-warning {
  background: var(--warning-trans);
  color: var(--warning-text);
}

.badge-danger {
  background: var(--danger-trans);
  color: var(--danger-text);
}

.badge-gray {
  background: rgba(107, 114, 128, 0.15);
  color: #9ca3af;
}

/* ===== EMPTY STATE ===== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 24px;
  background: var(--bg-secondary);
  border: 2px dashed var(--border-color);
  border-radius: 24px;
  text-align: center;
}

.empty-state i {
  font-size: 40px;
  color: var(--accent-text);
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 20px;
  margin: 0 0 8px;
  color: var(--text-primary);
}

.empty-text {
  color: var(--text-muted);
  font-size: 14px;
  margin: 0 0 20px;
}

.btn-primary {
  padding: 12px 28px;
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: 10px;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover {
  background: var(--accent-hover);
  transform: translateY(-2px);
}

.btn-secondary {
  padding: 12px 28px;
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: var(--border-color);
}

/* ===== RESPONSIVE ===== */
@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 820px) {
  .filters {
    flex-direction: column;
  }

  .filter-group {
    flex-direction: column;
    width: 100%;
  }

  .filter-group:first-child {
    min-width: unset;
  }

  .filter-select {
    width: 100%;
    min-width: unset;
  }

  .tabs {
    flex-wrap: wrap;
  }

  .tab {
    flex: 1;
    justify-content: center;
    min-width: 80px;
  }
}

@media (max-width: 600px) {
  .container {
    padding: 0 12px;
  }

  .maintenance-page {
    padding: 12px 0 24px;
  }

  .stats-grid {
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }

  .stat-card {
    padding: 12px 14px;
    gap: 10px;
  }

  .stat-icon {
    width: 36px;
    height: 36px;
    font-size: 15px;
  }

  .stat-value {
    font-size: 18px;
  }

  .stat-label {
    font-size: 10px;
  }

  .maintenance-card {
    padding: 14px 16px;
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }

  .card-left {
    gap: 12px;
  }

  .card-icon {
    width: 36px;
    height: 36px;
    font-size: 14px;
  }

  .card-title {
    font-size: 14px;
  }

  .card-header-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 2px;
  }

  .card-meta {
    gap: 8px;
    font-size: 12px;
  }

  .card-right {
    display: none;
  }

  .tabs {
    gap: 2px;
    padding: 3px;
  }

  .tab {
    padding: 6px 10px;
    font-size: 12px;
  }

  .tab-count {
    font-size: 10px;
    height: 18px;
    min-width: 18px;
    padding: 0 6px;
  }

  .filter-results {
    flex-direction: column;
    gap: 6px;
    text-align: center;
  }
}

@media (max-width: 400px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .tab {
    font-size: 11px;
    padding: 4px 8px;
  }

  .tab-count {
    display: none;
  }
}
</style>
