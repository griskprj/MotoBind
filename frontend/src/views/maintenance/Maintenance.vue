<template>
  <div class="maintenance-page">
    <div class="container">
      <Header
        title="Обслуживание"
        subtitle="Планируйте ТО, изучайте мануалы и диагностируйте мотоцикл"
      />

      <n-spin v-if="false" />

      <MotoSelector
        v-if="motorcycles.length > 0"
        :motorcycles="motorcycles"
        :selected-id="selectedMotoId"
        @select="onSelectMoto"
      />

      <AttentionBanner
        v-if="attentionItems.length > 0"
        :items="attentionItems"
        @open-maintenance="openMaintenanceDetails"
        @open-manual="openManualFor"
        @complete="openMarkMaintenance"
        @find-master="goToMasters"
      />

      <MaintenanceTabs
        v-model="activeTab"
        :counts="tabCounts"
      />

      <KeepAlive>
        <component
          :is="activeTabComponent"
          :motorcycle="selectedMotorcycle"
          :maintenances="filteredMaintenances"
          :all-maintenances="allMaintenances"
          :loading="loading"
          :filters="filters"
          :sort-by="sortBy"
          :motorcycles="motorcycles"
          :manuals="manuals"
          :manuals-loading="manualsLoading"
          @open="openMaintenanceDetails"
          @add="openAddMaintenance"
          @edit-filters="onFiltersChange"
          @sort="onSortChange"
          @open-manual="openManualFor"
          @create-manual="goToManualCreator"
          @start-diagnostics="openDiagnostics"
          @goto-tab="activeTab = $event"
        />
      </KeepAlive>
    </div>

    <!-- Модалки -->
    <AddMaintenanceModal
      :is-open="showAddModal"
      :motorcycles="motorcycles"
      :preselected-moto-id="selectedMotoId"
      @close="showAddModal = false"
      @created="onMaintenanceCreated"
    />

    <MaintenanceDetailsModal
      v-if="selectedMaintenance && selectedMotorcycle"
      :is-open="showDetailsModal"
      :maintenance="selectedMaintenance"
      :motorcycle="selectedMotorcycle"
      @close="closeDetails"
      @edit="openEditMaintenance"
      @delete="openDeleteMaintenance"
      @mark="openMarkMaintenance"
      @open-manual="openManualFor"
    />

    <EditMaintenanceModal
      v-if="selectedMaintenance"
      :is-open="showEditModal"
      :maintenance="selectedMaintenance"
      :motorcycles="motorcycles"
      @close="closeEdit"
      @updated="onMaintenanceUpdated"
    />

    <DeleteMaintenanceModal
      v-if="selectedMaintenance"
      :is-open="showDeleteModal"
      :maintenance-id="selectedMaintenance.id"
      @close="showDeleteModal = false"
      @submit="confirmDelete"
    />

    <MarkPlanMaintenanceModal
      v-if="selectedMaintenance"
      :is-open="showMarkModal"
      :maintenance="selectedMaintenance"
      :motorcycle="selectedMotorcycle"
      @close="showMarkModal = false"
      @submit="handleMarkMaintenance"
    />

    <DiagnosticsModal
      :is-open="showDiagnosticsModal"
      @close="showDiagnosticsModal = false"
      @write-to-master="handleWriteToMasterFromDiagnostics"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'

import Header from '@/components/Header.vue'
import MotoSelector from './components/MotoSelector.vue'
import AttentionBanner from './components/AttentionBanner.vue'
import MaintenanceTabs from './components/MaintenanceTabs.vue'

import OverviewTab from './components/tabs/OverviewTab.vue'
import HistoryTab from './components/tabs/HistoryTab.vue'
import PlansTab from './components/tabs/PlansTab.vue'
import ManualsTab from './components/tabs/ManualsTab.vue'
import DiagnosticsTab from './components/tabs/DiagnosticsTab.vue'

import AddMaintenanceModal from '@/components/modals/maintenance/AddMaintenanceModal.vue'
import EditMaintenanceModal from '@/components/modals/maintenance/EditMaintenanceModal.vue'
import DeleteMaintenanceModal from '@/components/modals/maintenance/DeleteMaintenanceModal.vue'
import MaintenanceDetailsModal from '@/components/modals/maintenance/MaintenanceDetailsModal.vue'
import MarkPlanMaintenanceModal from '@/components/modals/maintenance/MarkPlanMaintenanceModal.vue'
import DiagnosticsModal from '@/components/modals/diagnostics/DiagnosticsModal.vue'

import { useMotorcyclesStore, useMaintenancesStore, useRemindersStore, useManualsStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import { getEffectiveStatus, getMaintenanceDistance } from '@/utils/maintenanceStatus.js'

const router = useRouter()
const toast = useToast()

const motorcyclesStore = useMotorcyclesStore()
const maintenancesStore = useMaintenancesStore()
const remindersStore = useRemindersStore()
const manualsStore = useManualsStore()

const { items: motorcycles, selectedId: selectedMotoId, loading: motosLoading } = storeToRefs(motorcyclesStore)
const { items: manuals, loading: manualsLoading } = storeToRefs(manualsStore)
const { all: allMaintenances, loading: maintenancesLoading, filters, sortBy } = storeToRefs(maintenancesStore)

const selectedMotorcycle = computed(() => motorcyclesStore.selected)
const loading = computed(() => motosLoading.value || maintenancesLoading.value)

// ===== Tabs =====
const activeTab = ref('overview')
const tabComponents = {
  overview: OverviewTab,
  history: HistoryTab,
  plans: PlansTab,
  manuals: ManualsTab,
  diagnostics: DiagnosticsTab,
}
const activeTabComponent = computed(() => tabComponents[activeTab.value])

const tabCounts = computed(() => {
  const withStatus = allMaintenances.value.map((m) => {
    const moto = motorcycles.value.find((mm) => mm.id === m.moto_id)
    return { ...m, effectiveStatus: getEffectiveStatus(m, moto) }
  })

  return {
    overview: 0,
    history: withStatus.filter((m) => m.effectiveStatus === 'completed').length,
    plans: withStatus.filter(
      (m) => m.effectiveStatus === 'planned' || m.effectiveStatus === 'overdue'
    ).length,
    manuals: manuals.value.length,
    diagnostics: 0,
  }
})

// ===== Attention =====
const attentionItems = computed(() => {
  if (!selectedMotorcycle.value?.maintenances) return []

  return selectedMotorcycle.value.maintenances
    .filter((m) => m.status !== 'completed')
    .map((m) => {
      const { overdue, distance, days } = getMaintenanceDistance(m, selectedMotorcycle.value)
      return {
        ...m,
        isOverdue: overdue,
        distance: distance ?? Infinity,
        days: days ?? Infinity,
      }
    })
    .filter((m) => m.isOverdue || m.distance <= 1000 || m.days <= 30)
    .sort((a, b) => a.distance - b.distance)
    .slice(0, 3)
})

// ===== Filtered =====
const filteredMaintenances = computed(() => {
  let list = [...allMaintenances.value]

  const q = filters.value.search?.trim().toLowerCase()
  if (q) {
    list = list.filter(
      (m) =>
        m.title?.toLowerCase().includes(q) ||
        m.description?.toLowerCase().includes(q)
    )
  }

  list = list.map((m) => {
    const moto = motorcycles.value.find((mm) => mm.id === m.moto_id)
    return {
      ...m,
      effectiveStatus: getEffectiveStatus(m, moto),
    }
  })

  if (filters.value.status) {
    list = list.filter((m) => m.effectiveStatus === filters.value.status)
  }

  if (filters.value.motorcycle) {
    list = list.filter((m) => m.moto_id === filters.value.motorcycle)
  }

  return list
})

// ===== Modals state =====
const showAddModal = ref(false)
const showDetailsModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const showMarkModal = ref(false)
const showDiagnosticsModal = ref(false)
const selectedMaintenance = ref(null)

// ===== Lifecycle =====
onMounted(async () => {
  try {
    await Promise.all([
      motorcyclesStore.loadAll(),
      maintenancesStore.loadAll(),
      remindersStore.loadPending(),
    ])
    if (selectedMotoId.value) {
      await loadManualsForMoto(selectedMotoId.value)
    }
  } catch (err) {
    console.error('Failed to load maintenance data:', err)
    toast.error('Не удалось загрузить данные')
  }
})

watch(selectedMotoId, () => {
  filters.value.motorcycle = selectedMotoId.value || ''
})

watch(selectedMotoId, () => {
   filters.value.motorcycle = selectedMotoId.value || ''
  if (selectedMotoId.value) {
    loadManualsForMoto(selectedMotoId.value)
  }
})

// ===== Actions =====
function onSelectMoto(moto) {
  motorcyclesStore.select(moto.id)
}

function onFiltersChange(newFilters) {
  filters.value = { ...filters.value, ...newFilters }
}

function onSortChange(newSort) {
  sortBy.value = newSort
}

function openAddMaintenance() {
  showAddModal.value = true
}

function openMaintenanceDetails(item) {
  selectedMaintenance.value = item
  showDetailsModal.value = true
}

function closeDetails() {
  selectedMaintenance.value = null
  showDetailsModal.value = false
}

function openEditMaintenance() {
  showDetailsModal.value = false
  showEditModal.value = true
}

function closeEdit() {
  showEditModal.value = false
  closeDetails()
}

function openDeleteMaintenance() {
  showDetailsModal.value = false
  showDeleteModal.value = true
}

function openMarkMaintenance() {
  showDetailsModal.value = false
  showMarkModal.value = true
}

function openDiagnostics() {
  showDiagnosticsModal.value = true
}


function openManualFor(maintenance) {
  // TODO: связать maintenance → manual через manualsStore.loadForMaintenance
  router.push('/manuals')
}

function goToMasters() {
  router.push('/masters')
}

function goToManualCreator() {
  router.push('/manual-creator')
}

async function loadManualsForMoto(motoId) {
  try {
    manualsStore.filters.motorcycle = motoId
    await manualsStore.loadList()
  } catch (err) {
    console.error('Failed to load manuals:', err)
  }
}

// ===== Handlers =====
async function onMaintenanceCreated() {
  await maintenancesStore.loadAll()
  await motorcyclesStore.loadAll()
  showAddModal.value = false
  toast.success('Обслуживание добавлено')
}

async function onMaintenanceUpdated() {
  await maintenancesStore.loadAll()
  await motorcyclesStore.loadAll()
  closeEdit()
  toast.success('Обслуживание обновлено')
}

async function confirmDelete() {
  if (!selectedMaintenance.value) return
  try {
    await maintenancesStore.remove(selectedMaintenance.value.id)
    await motorcyclesStore.loadAll()
    showDeleteModal.value = false
    closeDetails()
    toast.success('Обслуживание удалено')
  } catch (err) {
    toast.error(err.response?.data?.error || 'Не удалось удалить')
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
    closeDetails()
    await maintenancesStore.loadAll()
    await motorcyclesStore.loadAll()
    await remindersStore.loadPending()
    toast.success('Обслуживание завершено')
  } catch (err) {
    toast.error(err.response?.data?.error || 'Ошибка завершения')
  }
}

function handleWriteToMasterFromDiagnostics() {
  showDiagnosticsModal.value = false
  router.push('/masters')
}
</script>

<style scoped>
.maintenance-page {
  padding-bottom: var(--space-6);
}

.container {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}
</style>
