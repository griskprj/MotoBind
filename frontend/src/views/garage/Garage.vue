<template>
  <div class="garage-page">
    <div class="container">
      <Header title="Мой гараж" subtitle="Управляйте своими мотоциклами и следите за их состоянием" />

      <n-spin :show="loading">
        <GarageStats
          :motorcycles="motorcycles"
          :total-maintenances="totalMaintenances"
          :total-costs="totalCosts"
        />

        <div class="garage-layout">
          <div class="garage-main">
            <MotoList
              :motorcycles="motorcycles"
              :selected-id="selectedMotoId"
              :loading="loading"
              @select="selectMotorcycle"
              @edit="openEditMoto"
              @update-mileage="openUpdateMileage"
              @photo="openPhoto"
              @delete="openDeleteMoto"
              @add="showAddMotoModal = true"
            />

            <div v-if="selectedMotorcycle" class="moto-detail">
              <MotoStatsCards
                :moto="selectedMotorcycle"
                :next-maintenance="nextMaintenance"
                :maintenance-spends="maintenanceSpends"
              />

              <MotoSpecsAndNotes
                :moto="selectedMotorcycle"
                @edit-note="showEditMotoNoteModal = true"
              />

              <MileageCard
                :moto="selectedMotorcycle"
                :updating="mileageUpdating"
                @quick-add="quickAddMileage"
                @open-precise="openUpdateMileage(selectedMotorcycle)"
              />

              <DiagnosticsSection
                v-if="selectedMotorcycle"
                @start="showDiagnosticsModal = true"
              />

              <MaintenancesList
                :maintenances="recentMaintenances"
                @open="openMaintenanceDetails"
                @view-all="router.push('/maintenance')"
              />
            </div>
          </div>

          <GarageSidebar
            :my-masters="myMasters"
            :tip="dailyTip"
            @refresh-tip="refreshTip"
          />
        </div>
      </n-spin>
    </div>

    <!-- Модалки — все те же, не трогаем -->
    <AddMotoModal :is-open="showAddMotoModal" @created="onMotoCreated" @close="showAddMotoModal = false" />
    <EditMotoModal :is-open="showEditMotoModal" :motorcycle="selectedMotorcycle" @close="onMotoUpdated" />
    <UpdateMileageModal :is-open="showUpdateMotoMileageModal" :motorcycle="selectedMotorcycle" @close="onMileageUpdated" />
    <EditMotoNoteModal :is-open="showEditMotoNoteModal" :motorcycle="selectedMotorcycle" @close="showEditMotoNoteModal = false" />
    <DeleteMotoModal :is-open="showDeleteMotoModal" :motorcycle="selectedMotorcycle" @submit="deleteMoto" @close="showDeleteMotoModal = false" />
    <PhotoModal :is-open="showPhotoModal" :motorcycle="selectedMotorcycle" @close="showPhotoModal = false" />
    <QuickStartModal :is-open="showQuickStartModal" :motorcycle="selectedMotorcycle" @close="showQuickStartModal = false" @created="onQuickStartCreated" />

    <MaintenanceDetailsModal
      v-if="selectedMotorcycle && selectedMaintenance"
      :is-open="showDetailsMaintenanceModal"
      :maintenance="selectedMaintenance"
      :motorcycle="selectedMotorcycle"
      @edit="openEditMaintenance"
      @delete="openDeleteMaintenance"
      @mark="openMarkMaintenance"
      @close="closeMaintenanceDetails"
    />
    <EditMaintenanceModal
      v-if="selectedMaintenance"
      :is-open="showEditModal"
      :maintenance="selectedMaintenance"
      :motorcycles="motorcycles"
      @close="closeEditMaintenance"
    />
    <DeleteMaintenanceModal
      v-if="selectedMaintenance"
      :is-open="showDeleteModal"
      :maintenance-id="selectedMaintenance.id"
      @submit="confirmDeleteMaintenance"
      @close="showDeleteModal = false"
    />
    <MarkPlanMaintenanceModal
      v-if="selectedMaintenance"
      :is-open="showMarkModal"
      :maintenance="selectedMaintenance"
      :motorcycle="selectedMotorcycle"
      @submit="handleMarkMaintenance"
      @close="showMarkModal = false"
    />
    <DiagnosticsModal
      :is-open="showDiagnosticsModal"
      @close="showDiagnosticsModal = false"
      @write-to-master="handleWriteToMasterFromDiagnostics"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'

import Header from '@/components/Header.vue'
import GarageStats from './components/GarageStats.vue'
import MotoList from './components/MotoList.vue'
import MotoStatsCards from './components/MotoStatsCards.vue'
import MotoSpecsAndNotes from './components/MotoSpecsAndNotes.vue'
import MileageCard from './components/MileageCard.vue'
import MaintenancesList from './components/MaintenancesList.vue'
import GarageSidebar from './components/GarageSidebar.vue'

import AddMotoModal from '@/components/modals/moto/AddMotoModal.vue'
import EditMotoModal from '@/components/modals/moto/EditMotoModal.vue'
import DeleteMotoModal from '@/components/modals/moto/DeleteMotoModal.vue'
import UpdateMileageModal from '@/components/modals/moto/UpdateMileageModal.vue'
import EditMotoNoteModal from '@/components/modals/moto/EditMotoNoteModal.vue'
import PhotoModal from '@/components/modals/moto/PhotoModal.vue'
import QuickStartModal from '@/components/modals/moto/QuickStartModal.vue'
import MaintenanceDetailsModal from '@/components/modals/maintenance/MaintenanceDetailsModal.vue'
import EditMaintenanceModal from '@/components/modals/maintenance/EditMaintenanceModal.vue'
import DeleteMaintenanceModal from '@/components/modals/maintenance/DeleteMaintenanceModal.vue'
import MarkPlanMaintenanceModal from '@/components/modals/maintenance/MarkPlanMaintenanceModal.vue'
import DiagnosticsSection from './components/DiagnosticsSection.vue'
import DiagnosticsModal from '@/components/modals/diagnostics/DiagnosticsModal.vue'

import { useMotorcyclesStore, useMaintenancesStore, useRemindersStore, useBusinessStore } from '@/stores'
import { useToast } from '@/composables/useToast'

const router = useRouter()
const toast = useToast()

const motorcyclesStore = useMotorcyclesStore()
const maintenancesStore = useMaintenancesStore()
const remindersStore = useRemindersStore()
const businessStore = useBusinessStore()

const { items: motorcycles, selectedId: selectedMotoId, loading } = storeToRefs(motorcyclesStore)
const { myMasters } = storeToRefs(businessStore)

const selectedMotorcycle = computed(() => motorcyclesStore.selected)
const recentMaintenances = computed(() => motorcyclesStore.recentMaintenances)
const nextMaintenance = computed(() => motorcyclesStore.nextMaintenance)
const totalMaintenances = computed(() => motorcyclesStore.totalMaintenances)
const totalCosts = computed(() => motorcyclesStore.totalCosts)
const maintenanceSpends = computed(() => motorcyclesStore.maintenanceSpends)

const activeReminders = computed(() =>
  selectedMotoId.value ? remindersStore.forMotorcycle(selectedMotoId.value) : []
)

const selectedMaintenance = ref<any>(null)

const showAddMotoModal = ref(false)
const showEditMotoModal = ref(false)
const showDeleteMotoModal = ref(false)
const showUpdateMotoMileageModal = ref(false)
const showEditMotoNoteModal = ref(false)
const showPhotoModal = ref(false)
const showQuickStartModal = ref(false)
const showDiagnosticsModal = ref(false)
const showDetailsMaintenanceModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const showMarkModal = ref(false)

const mileageUpdating = ref(false)

const tips = [
  'Проверяйте давление в шинах раз в неделю — это влияет на управляемость и расход.',
  'Мойте цепь перед смазкой — так смазка держится дольше.',
  'Следите за уровнем антифриза перед длительными поездками.',
  'Храните мотоцикл с полным баком — меньше конденсата в баке.',
  'Проверяйте натяжение цепи каждые 500 км.',
]
const dailyTip = ref(tips[0])

function refreshTip() {
  dailyTip.value = tips[Math.floor(Math.random() * tips.length)]
}

onMounted(async () => {
  try {
    await Promise.all([motorcyclesStore.loadAll(), remindersStore.loadPending()])
    refreshTip()
    await businessStore.loadMyMasters()
  } catch (err) {
    console.error('Failed to load garage data:', err)
    toast.error('Не удалось загрузить гараж')
  }
})

// ===== Moto actions =====
function selectMotorcycle(moto: any) {
  if (moto?.id) motorcyclesStore.select(moto.id)
}

function openEditMoto(moto: any) {
  selectMotorcycle(moto)
  showEditMotoModal.value = true
}

function openUpdateMileage(moto: any) {
  selectMotorcycle(moto)
  showUpdateMotoMileageModal.value = true
}

function openPhoto(moto: any) {
  selectMotorcycle(moto)
  showPhotoModal.value = true
}

function openDeleteMoto(moto: any) {
  selectMotorcycle(moto)
  showDeleteMotoModal.value = true
}

async function quickAddMileage(step: number) {
  const moto = selectedMotorcycle.value
  if (!moto?.id || mileageUpdating.value) return

  mileageUpdating.value = true
  try {
    await motorcyclesStore.updateMileage(moto.id, (moto.mileage || 0) + step)
    await remindersStore.loadPending()
    toast.success(`Пробег увеличен на ${step} км`)
  } catch (err: any) {
    toast.error(err.response?.data?.error || 'Не удалось обновить пробег')
  } finally {
    mileageUpdating.value = false
  }
}

async function onMotoCreated() {
  await remindersStore.loadPending()
  showAddMotoModal.value = false
}

async function onMotoUpdated() {
  await remindersStore.loadPending()
  showEditMotoModal.value = false
}

async function onMileageUpdated() {
  await remindersStore.loadPending()
  showUpdateMotoMileageModal.value = false
}

async function deleteMoto(id: number) {
  try {
    await motorcyclesStore.remove(id)
    await remindersStore.loadPending()
    showDeleteMotoModal.value = false
    toast.success('Мотоцикл удалён')
  } catch (err: any) {
    toast.error(err.response?.data?.error || 'Ошибка удаления')
  }
}

function onQuickStartCreated() {
  motorcyclesStore.loadAll()
  showQuickStartModal.value = false
}

// ===== Maintenance =====
function openMaintenanceDetails(item: any) {
  selectedMaintenance.value = item
  showDetailsMaintenanceModal.value = true
}

function closeMaintenanceDetails() {
  selectedMaintenance.value = null
  showDetailsMaintenanceModal.value = false
}

function openEditMaintenance() {
  showDetailsMaintenanceModal.value = false
  showEditModal.value = true
}

function closeEditMaintenance() {
  showEditModal.value = false
  closeMaintenanceDetails()
}

function openDeleteMaintenance() {
  showDetailsMaintenanceModal.value = false
  showDeleteModal.value = true
}

function openMarkMaintenance() {
  showDetailsMaintenanceModal.value = false
  showMarkModal.value = true
}

async function confirmDeleteMaintenance() {
  if (!selectedMaintenance.value) return
  try {
    await maintenancesStore.remove(selectedMaintenance.value.id)
    showDeleteModal.value = false
    closeMaintenanceDetails()
    toast.success('Обслуживание удалено')
  } catch (err: any) {
    toast.error(err.response?.data?.error || 'Не удалось удалить')
  }
}

async function handleMarkMaintenance(formData: any) {
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
    closeMaintenanceDetails()
    await motorcyclesStore.loadAll()
    await remindersStore.loadPending()
    toast.success('Обслуживание завершено')
  } catch (err: any) {
    toast.error(err.response?.data?.error || 'Ошибка завершения')
  }
}

// ===== Reminders =====
async function dismissReminder(reminder: any) {
  try {
    await remindersStore.dismiss(reminder.id)
  } catch {
    toast.error('Не удалось скрыть напоминание')
  }
}

function handleReminderAction(reminder: any) {
  if (reminder.type === 'mileage_update') {
    const moto = motorcycles.value.find((m: any) => m.id === reminder.motorcycle_id)
    if (moto) {
      motorcyclesStore.select(moto.id)
      showUpdateMotoMileageModal.value = true
    }
  } else {
    router.push('/maintenance')
  }
}

function handleWriteToMasterFromDiagnostics() {
  showDiagnosticsModal.value = false
  document.querySelector('.appointment-card')?.scrollIntoView({
    behavior: 'smooth',
    block: 'start',
  })
}
</script>

<style scoped>
.garage-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 360px;
  gap: 24px;
  align-items: start;
}

.garage-main {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.moto-detail {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 600;
}

.section-header i {
  color: var(--accent);
}

.diag-title {
  font-size: 14px;
  color: var(--text-secondary);
  text-align: center;
  margin: 0 0 6px;
}

.diag-hint {
  font-size: 12px;
  color: var(--text-muted);
  text-align: center;
  margin: 0 0 14px;
}

@media (max-width: 1100px) {
  .garage-layout {
    grid-template-columns: 1fr;
  }
}
</style>
