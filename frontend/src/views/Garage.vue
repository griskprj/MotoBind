<template>
  <div class="garage-page">
    <LoadingOverlay :isLoading="loading" text="Загрузка гаража..."/>

    <div class="container">
      <Header
        title="Мой гараж"
        subtitle="Управляйте своими мотоциклами и следите за их состоянием"
      />

      <!-- Напоминания -->
      <div v-if="hasActiveReminders" class="reminders-banner">
        <div
          v-for="reminder in activeRemindersForSelected"
          :key="reminder.id"
          class="reminder-item"
          :class="'reminder-' + reminderBannerInfo(reminder).variant"
        >
          <div class="reminder-icon">
            <i :class="reminderBannerInfo(reminder).icon"></i>
          </div>
          <div class="reminder-body">
            <div class="reminder-title">{{ reminderBannerInfo(reminder).title }}</div>
            <div class="reminder-text">{{ reminderBannerInfo(reminder).text }}</div>
          </div>
          <div class="reminder-actions">
            <button class="reminder-btn primary" @click="handleReminderAction(reminder)">
              {{ reminderBannerInfo(reminder).cta }}
            </button>
            <button class="reminder-btn ghost danger" @click="dismissReminder(reminder)" title="Скрыть навсегда">
              <i class="fa fa-times"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- Статистика гаража -->
      <div v-if="motorcycles.length > 0" class="garage-stats">
        <div class="stat-chip">
          <i class="fa fa-motorcycle"></i>
          <span>{{ motorcycles.length }}</span>
          {{ declensionMotorcycles(motorcycles.length) }}
        </div>
        <div class="stat-chip">
          <i class="fa fa-wrench"></i>
          <span>{{ totalMaintenances }}</span>
          обслуживаний
        </div>
        <div class="stat-chip">
          <i class="fa fa-ruble-sign"></i>
          <span>{{ formatCost(totalCosts) }}</span>
        </div>
      </div>

      <!-- Мотоциклы -->
      <div class="motorcycles-container">
        <div class="motorcycles-list">
          <div
            v-for="moto in motorcycles"
            :key="moto.id"
            class="moto-list-item"
            :class="{ active: selectedMotoId === moto.id }"
            @click="selectMotorcycle(moto)"
          >
            <div class="moto-card-wrapper">
              <div class="moto-list-preview">
                <img
                  v-if="moto.photo_url"
                  :src="getMotoPhotoUrl(moto.photo_url)"
                  :alt="moto.name"
                  @error="handleImageError"
                  loading="lazy"
                >
                <div v-else class="moto-list-placeholder">
                  <i class="fa fa-motorcycle"></i>
                </div>
              </div>

              <div class="moto-list-info">
                <div class="moto-list-header">
                  <h3 class="moto-list-name">{{ moto.name }}</h3>
                  <span class="moto-list-year">{{ moto.years }}</span>
                  <span class="moto-list-volume">{{ moto.volume }} см³</span>
                </div>
                <div class="moto-list-meta">
                  <span class="moto-list-mileage">
                    <i class="fa-solid fa-gauge-high"></i>
                    {{ formatMileage(moto.mileage) }}
                  </span>
                  <span class="moto-list-color">
                    <span class="color-dot-sm" :style="{ background: moto.color }"></span>
                  </span>
                  <span v-if="moto.maintenances?.length" class="moto-list-maintenances">
                    <i class="fa fa-wrench"></i>
                    {{ moto.maintenances.length }}
                  </span>
                </div>
              </div>
            </div>

            <div class="moto-list-actions" @click.stop>
              <button @click="openEditMoto(moto)" class="icon-btn" title="Редактировать">
                <i class="fa fa-pen"></i>
              </button>
              <button @click="openUpdateMileage(moto)" class="icon-btn" title="Обновить пробег">
                <i class="fa-solid fa-gauge-high"></i>
              </button>
              <button @click="openPhoto(moto)" class="icon-btn" title="Фото">
                <i class="fa fa-camera"></i>
              </button>
              <button @click="openDeleteMoto(moto)" class="icon-btn danger" title="Удалить">
                <i class="fa fa-trash"></i>
              </button>
            </div>
          </div>

          <button @click="showAddMotoModal = true" class="add-btn btn-secondary">
            <i class="fa fa-plus"></i>
            <span>Добавить мотоцикл</span>
          </button>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="motorcycles.length === 0 && !loading" class="empty-state">
        <div class="empty-icon">
          <i class="fa fa-motorcycle"></i>
        </div>
        <h3>Ваш гараж пуст</h3>
        <p>Добавьте свой первый мотоцикл и начните вести учёт обслуживаний</p>
        <button @click="showAddMotoModal = true" class="btn-primary">
          Добавить мотоцикл
        </button>
      </div>

      <!-- Quick Start Promo -->
      <div v-if="selectedMotorcycle && !selectedMotorcycle.maintenances?.length" class="quick-start-promo">
        <div class="promo-icon">
          <i class="fa fa-rocket"></i>
        </div>
        <div class="promo-content">
          <h4>Настройте обслуживание за 30 секунд</h4>
          <p>Мы автоматически создадим базовое расписание на основе пробега и условий эксплуатации</p>
        </div>
        <button @click="showQuickStartModal = true" class="btn-primary">
          <i class="fa fa-bolt"></i>
          Быстрый старт
        </button>
      </div>

      <!-- Детальная информация -->
      <div v-if="selectedMotorcycle" class="moto-detail">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="fa-solid fa-gauge-high"></i>
            </div>
            <div class="stat-info">
              <span class="stat-label">Пробег</span>
              <span class="stat-value">{{ formatMileage(selectedMotorcycle.mileage) }}</span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon">
              <i class="fa fa-wrench"></i>
            </div>
            <div class="stat-info">
              <span class="stat-label">Обслуживаний</span>
              <span class="stat-value">{{ selectedMotorcycle.maintenances?.length || 0 }}</span>
            </div>
          </div>

          <div class="stat-card" :class="{ 'stat-warning': nextMaintenance?.isOverdue }">
            <div class="stat-icon">
              <i class="fa fa-calendar-check"></i>
            </div>
            <div class="stat-info">
              <span class="stat-label">Следующее ТО</span>
              <span class="stat-value">
                <template v-if="nextMaintenance">
                  <span v-if="nextMaintenance.isOverdue" class="text-danger">
                    <i class="fa fa-exclamation-triangle"></i>
                    {{ Math.round(nextMaintenance.distanceOverdue) }} км просрочено
                  </span>
                  <span v-else>
                    через {{ Math.round(nextMaintenance.distanceToNext) }} км
                  </span>
                </template>
                <span v-else class="text-muted">Все выполнены</span>
              </span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon">
              <i class="fa fa-ruble-sign"></i>
            </div>
            <div class="stat-info">
              <span class="stat-label">Расходы на ТО</span>
              <span class="stat-value">{{ formatCost(maintenanceSpends) }}</span>
            </div>
          </div>
        </div>

        <div class="detail-grid">
          <div class="detail-card">
            <h4 class="detail-title">Характеристики</h4>
            <div class="spec-list">
              <div class="spec-item">
                <span class="spec-label">Год выпуска</span>
                <span class="spec-value">{{ selectedMotorcycle.years }}</span>
              </div>
              <div class="spec-item">
                <span class="spec-label">Двигатель</span>
                <span class="spec-value">{{ selectedMotorcycle.volume }} см³</span>
              </div>
              <div class="spec-item">
                <span class="spec-label">Цвет</span>
                <span class="spec-value">
                  <span class="color-dot" :style="{ background: selectedMotorcycle.color }"></span>
                </span>
              </div>
              <div class="spec-item">
                <span class="spec-label">Пробег</span>
                <span class="spec-value">{{ formatMileage(selectedMotorcycle.mileage) }}</span>
              </div>
              <div class="spec-item full" v-if="selectedMotorcycle.vin">
                <span class="spec-label">VIN</span>
                <span class="spec-value spec-code">{{ selectedMotorcycle.vin }}</span>
              </div>
              <div class="spec-item full" v-if="selectedMotorcycle.license_plate">
                <span class="spec-label">Гос. номер</span>
                <span class="spec-value spec-code">{{ selectedMotorcycle.license_plate }}</span>
              </div>
            </div>
          </div>

          <div class="detail-card notes-card">
            <div class="detail-header">
              <h4 class="detail-title">Заметки</h4>
              <button @click="showEditMotoNoteModal = true" class="icon-btn small" title="Редактировать заметку">
                <i class="fa fa-pen"></i>
              </button>
            </div>
            <div class="notes-content">
              <p v-if="selectedMotorcycle.note" class="notes-text">{{ selectedMotorcycle.note }}</p>
              <p v-else class="notes-empty">
                <i class="fa fa-pen"></i>
                Добавьте заметку о мотоцикле
              </p>
            </div>
          </div>
        </div>

        <div class="maintenances-section">
          <div class="section-header">
            <div class="section-header-left">
              <i class="fa fa-wrench"></i>
              <h4>Последние обслуживания</h4>
            </div>
            <button @click="$router.push('/maintenance')" class="btn-link">
              Все записи <i class="fa fa-arrow-right"></i>
            </button>
          </div>

          <div v-if="recentMaintenances.length > 0" class="maintenances-list">
            <div
              v-for="item in recentMaintenances"
              :key="item.id"
              class="maintenance-item"
              @click="openMaintenanceDetails(item)"
            >
              <div class="maint-icon" :class="'maint-icon-' + item.status">
                <i class="fa fa-wrench"></i>
              </div>
              <div class="maint-info">
                <div class="maint-title">{{ item.title }}</div>
                <div class="maint-meta">
                  <span>{{ formatDate(item.completed_date || item.planned_date) }}</span>
                  <span class="dot">•</span>
                  <span>{{ item.completed_mileage || item.planned_mileage || '—' }} км</span>
                  <span class="dot">•</span>
                  <span>{{ item.cost ? formatCost(item.cost) : '—' }}</span>
                </div>
              </div>
              <div class="maint-status">
                <span :class="'badge badge-' + getStatusBadgeVariant(item.status)">
                  {{ getStatusLabel(item.status) }}
                </span>
                <i class="fa fa-chevron-right"></i>
              </div>
            </div>
          </div>

          <div v-else class="empty-small">
            <i class="fa fa-wrench"></i>
            <p>Нет записей обслуживания</p>
            <span class="hint">Перейдите в раздел "Обслуживание" чтобы добавить</span>
          </div>
        </div>
      </div>
    </div>

    <!-- MODALS: MOTO -->
    <AddMotoModal
      :isOpen="showAddMotoModal"
      @submit="addMoto"
      @close="showAddMotoModal = false"
    />

    <EditMotoModal
      :isOpen="showEditMotoModal"
      :motorcycle="selectedMotorcycle"
      @submit="updateMoto"
      @close="showEditMotoModal = false"
    />

    <UpdateMileageModal
      :isOpen="showUpdateMotoMileageModal"
      :motorcycle="selectedMotorcycle"
      @submit="updateMotoMileage"
      @close="showUpdateMotoMileageModal = false"
    />

    <EditMotoNoteModal
      :isOpen="showEditMotoNoteModal"
      :motorcycle="selectedMotorcycle"
      @submit="updateMotoNote"
      @close="showEditMotoNoteModal = false"
    />

    <DeleteMotoModal
      :isOpen="showDeleteMotoModal"
      :motorcycle="selectedMotorcycle"
      @submit="deleteMoto"
      @close="showDeleteMotoModal = false"
    />

    <PhotoModal
      :isOpen="showPhotoModal"
      :motorcycle="selectedMotorcycle"
      @upload="uploadPhoto"
      @delete="deletePhoto"
      @close="showPhotoModal = false"
    />

    <QuickStartModal
      :isOpen="showQuickStartModal"
      :motorcycle="selectedMotorcycle"
      @close="showQuickStartModal = false"
      @created="onQuickStartCreated"
    />

    <!-- MODALS: MAINTENANCE (цепочка) -->
    <MaintenanceDetailsModal
      v-if="selectedMotorcycle && selectedMaintenance"
      :isOpen="showDetailsMaintenanceModal"
      :maintenance="selectedMaintenance"
      :motorcycle="selectedMotorcycle"
      @edit="openEditMaintenance"
      @delete="openDeleteMaintenance"
      @mark="openMarkMaintenance"
      @close="closeMaintenanceDetails"
    />

    <EditMaintenanceModal
      v-if="selectedMaintenance"
      :isOpen="showEditModal"
      :maintenance="selectedMaintenance"
      :motorcycles="motorcycles"
      @close="closeEditMaintenance"
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

<script>
import { computed, onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'

import Header from '../components/Header.vue'
import AddMotoModal from '../components/modals/moto/AddMotoModal.vue'
import EditMotoModal from '../components/modals/moto/EditMotoModal.vue'
import DeleteMotoModal from '../components/modals/moto/DeleteMotoModal.vue'
import UpdateMileageModal from '../components/modals/moto/UpdateMileageModal.vue'
import EditMotoNoteModal from '../components/modals/moto/EditMotoNoteModal.vue'
import PhotoModal from '../components/modals/moto/PhotoModal.vue'
import QuickStartModal from '../components/modals/moto/QuickStartModal.vue'
import MaintenanceDetailsModal from '../components/modals/maintenance/MaintenanceDetailsModal.vue'
import EditMaintenanceModal from '../components/modals/maintenance/EditMaintenanceModal.vue'
import DeleteMaintenanceModal from '../components/modals/maintenance/DeleteMaintenanceModal.vue'
import MarkPlanMaintenanceModal from '../components/modals/maintenance/MarkPlanMaintenanceModal.vue'
import LoadingOverlay from '../components/LoadingOverlay.vue'

import { useMotorcyclesStore, useMaintenancesStore, useRemindersStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import {
  formatMileage,
  formatCost,
  declensionMotorcycles,
  getStatusLabel,
  getStatusBadgeVariant,
} from '@/utils/formatters'
import { getMotoPhotoUrl } from '@/utils/mediaUrl'
import formatDate from '@/utils/DateFormatter.js'

export default {
  name: 'GaragePage',

  components: {
    Header,
    AddMotoModal,
    EditMotoModal,
    DeleteMotoModal,
    UpdateMileageModal,
    EditMotoNoteModal,
    PhotoModal,
    QuickStartModal,
    MaintenanceDetailsModal,
    EditMaintenanceModal,
    DeleteMaintenanceModal,
    MarkPlanMaintenanceModal,
    LoadingOverlay,
  },

  setup() {
    const router = useRouter()
    const toast = useToast()

    const motorcyclesStore = useMotorcyclesStore()
    const maintenancesStore = useMaintenancesStore()
    const remindersStore = useRemindersStore()

    // ===== Store refs =====
    const { items: motorcycles, selectedId: selectedMotoId, loading } = storeToRefs(motorcyclesStore)

    // ===== Computed =====
    const selectedMotorcycle = computed(() => motorcyclesStore.selected)
    const recentMaintenances = computed(() => motorcyclesStore.recentMaintenances)
    const nextMaintenance = computed(() => motorcyclesStore.nextMaintenance)
    const totalMaintenances = computed(() => motorcyclesStore.totalMaintenances)
    const totalCosts = computed(() => motorcyclesStore.totalCosts)
    const maintenanceSpends = computed(() => motorcyclesStore.maintenanceSpends)

    const activeRemindersForSelected = computed(() => {
      if (!selectedMotoId.value) return []
      return remindersStore.forMotorcycle(selectedMotoId.value)
    })
    const hasActiveReminders = computed(() => activeRemindersForSelected.value.length > 0)

    // ===== Local UI state =====
    const selectedMaintenance = ref(null)

    // Moto modals
    const showAddMotoModal = ref(false)
    const showEditMotoModal = ref(false)
    const showDeleteMotoModal = ref(false)
    const showUpdateMotoMileageModal = ref(false)
    const showEditMotoNoteModal = ref(false)
    const showPhotoModal = ref(false)
    const showQuickStartModal = ref(false)

    // Maintenance modals (цепочка Details → Edit/Delete/Mark)
    const showDetailsMaintenanceModal = ref(false)
    const showEditModal = ref(false)
    const showDeleteModal = ref(false)
    const showMarkModal = ref(false)

    // ===== Lifecycle =====
    onMounted(async () => {
      try {
        await Promise.all([
          motorcyclesStore.loadAll(),
          remindersStore.loadPending(),
        ])
      } catch (err) {
        console.error('Failed to load garage data:', err)
        toast.error('Не удалось загрузить гараж')
      }
    })

    // ===== Helpers =====
    function selectMotorcycle(moto) {
      if (!moto?.id) return
      motorcyclesStore.select(moto.id)
    }

    function handleImageError(e) {
      e.target.src = ''
      e.target.style.display = 'none'
      const placeholder = e.target.parentElement?.querySelector('.moto-list-placeholder')
      if (placeholder) placeholder.classList.remove('hidden')
    }

    // ===== Moto actions (открытие модалок) =====
    function openEditMoto(moto) {
      selectMotorcycle(moto)
      showEditMotoModal.value = true
    }

    function openUpdateMileage(moto) {
      selectMotorcycle(moto)
      showUpdateMotoMileageModal.value = true
    }

    function openPhoto(moto) {
      selectMotorcycle(moto)
      showPhotoModal.value = true
    }

    function openDeleteMoto(moto) {
      selectMotorcycle(moto)
      showDeleteMotoModal.value = true
    }

    // ===== Moto CRUD =====
    async function addMoto(formData) {
      try {
        const { photoFile, ...data } = formData
        await motorcyclesStore.create(data, photoFile)
        await remindersStore.loadPending()
        showAddMotoModal.value = false
        toast.success('Мотоцикл добавлен')
      } catch (err) {
        toast.error(err.response?.data?.error || 'Ошибка добавления')
      }
    }

    async function updateMoto(formData) {
      try {
        const { id, newPhotoFile, deleteExistingPhoto, ...data } = formData
        await motorcyclesStore.update(id, data, { newPhotoFile, deleteExistingPhoto })
        await remindersStore.loadPending()
        showEditMotoModal.value = false
        toast.success('Мотоцикл обновлён')
      } catch (err) {
        toast.error(err.response?.data?.error || 'Ошибка обновления')
      }
    }

    async function updateMotoMileage(formData) {
      try {
        await motorcyclesStore.updateMileage(formData.id, formData.mileage)
        await remindersStore.loadPending()
        showUpdateMotoMileageModal.value = false
        toast.success('Пробег обновлён')
      } catch (err) {
        toast.error(err.response?.data?.error || 'Ошибка обновления пробега')
      }
    }

    async function updateMotoNote(formData) {
      try {
        await motorcyclesStore.updateNote(formData.id, formData.note)
        showEditMotoNoteModal.value = false
        toast.success('Заметка обновлена')
      } catch (err) {
        toast.error(err.response?.data?.error || 'Ошибка обновления заметки')
      }
    }

    async function deleteMoto(id) {
      try {
        await motorcyclesStore.remove(id)
        await remindersStore.loadPending()
        showDeleteMotoModal.value = false
        toast.success('Мотоцикл удалён')
      } catch (err) {
        toast.error(err.response?.data?.error || 'Ошибка удаления')
      }
    }

    async function uploadPhoto(formData) {
      try {
        const file = formData.get('photo')
        if (!file) return
        await motorcyclesStore.uploadPhoto(selectedMotoId.value, file)
        showPhotoModal.value = false
        toast.success('Фото загружено')
      } catch (err) {
        toast.error(err.response?.data?.error || 'Ошибка загрузки фото')
      }
    }

    async function deletePhoto() {
      if (!confirm('Удалить фото?')) return
      try {
        await motorcyclesStore.deletePhoto(selectedMotoId.value)
        showPhotoModal.value = false
        toast.success('Фото удалено')
      } catch (err) {
        toast.error(err.response?.data?.error || 'Ошибка удаления фото')
      }
    }

    // ===== Maintenance =====
    function openMaintenanceDetails(item) {
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
      } catch (err) {
        console.error('Failed to delete maintenance:', err)
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
        closeMaintenanceDetails()
        await motorcyclesStore.loadAll()
        await remindersStore.loadPending()
        toast.success('Обслуживание завершено')
      } catch (err) {
        console.error('Failed to complete maintenance:', err)
        toast.error(err.response?.data?.error || 'Ошибка завершения')
      }
    }

    function onQuickStartCreated() {
      motorcyclesStore.loadAll()
      showQuickStartModal.value = false
    }

    // ===== Reminders =====
    async function dismissReminder(reminder) {
      try {
        await remindersStore.dismiss(reminder.id)
      } catch (err) {
        toast.error('Не удалось скрыть напоминание')
      }
    }

    function reminderBannerInfo(reminder) {
      const moto = motorcycles.value.find((m) => m.id === reminder.motorcycle_id)
      const motoName = moto?.name || 'мотоцикл'

      switch (reminder.type) {
        case 'mileage_update': {
          const last = reminder.motorcycle?.mileage || moto?.mileage || 0
          return {
            icon: 'fa-solid fa-gauge-high',
            variant: 'warning',
            title: `Обновите пробег для ${motoName}`,
            text: `Текущий: ${last} км. Свежие данные помогают точнее напоминать о ТО.`,
            cta: 'Обновить',
          }
        }
        case 'maintenance_soon': {
          const maint = reminder.maintenance
          return {
            icon: 'fa fa-wrench',
            variant: 'accent',
            title: `Скоро ТО: ${maint?.title || 'обслуживание'}`,
            text: `Запланировано на ${maint?.planned_mileage || '—'} км.`,
            cta: 'Открыть',
          }
        }
        case 'maintenance_overdue': {
          const maint = reminder.maintenance
          return {
            icon: 'fa fa-exclamation-triangle',
            variant: 'danger',
            title: `Просрочено ТО: ${maint?.title || 'обслуживание'}`,
            text: `Планировалось на ${maint?.planned_mileage || '—'} км.`,
            cta: 'Открыть',
          }
        }
        default:
          return {
            icon: 'fa fa-bell',
            variant: 'accent',
            title: 'Напоминание',
            text: '',
            cta: 'Открыть',
          }
      }
    }

    function handleReminderAction(reminder) {
      if (reminder.type === 'mileage_update') {
        const moto = motorcycles.value.find((m) => m.id === reminder.motorcycle_id)
        if (moto) {
          motorcyclesStore.select(moto.id)
          showUpdateMotoMileageModal.value = true
        }
      } else {
        router.push('/maintenance')
      }
    }

    return {
      // stores
      motorcyclesStore,
      maintenancesStore,
      remindersStore,

      // store refs
      motorcycles,
      selectedMotoId,
      loading,

      // computed
      selectedMotorcycle,
      recentMaintenances,
      nextMaintenance,
      totalMaintenances,
      totalCosts,
      maintenanceSpends,
      activeRemindersForSelected,
      hasActiveReminders,

      // local state
      selectedMaintenance,

      // moto modals
      showAddMotoModal,
      showEditMotoModal,
      showDeleteMotoModal,
      showUpdateMotoMileageModal,
      showEditMotoNoteModal,
      showPhotoModal,
      showQuickStartModal,

      // maintenance modals
      showDetailsMaintenanceModal,
      showEditModal,
      showDeleteModal,
      showMarkModal,

      // utils
      formatMileage,
      formatCost,
      declensionMotorcycles,
      getStatusLabel,
      getStatusBadgeVariant,
      getMotoPhotoUrl,
      formatDate,

      // methods: helpers
      selectMotorcycle,
      handleImageError,

      // methods: moto
      openEditMoto,
      openUpdateMileage,
      openPhoto,
      openDeleteMoto,
      addMoto,
      updateMoto,
      updateMotoMileage,
      updateMotoNote,
      deleteMoto,
      uploadPhoto,
      deletePhoto,

      // methods: maintenance
      openMaintenanceDetails,
      closeMaintenanceDetails,
      openEditMaintenance,
      closeEditMaintenance,
      openDeleteMaintenance,
      openMarkMaintenance,
      confirmDeleteMaintenance,
      handleMarkMaintenance,
      onQuickStartCreated,

      // methods: reminders
      dismissReminder,
      reminderBannerInfo,
      handleReminderAction,
    }
  },
}
</script>

<style scoped>
.quick-start-promo {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px 24px;
    background: linear-gradient(135deg, var(--accent-trans), rgba(139, 92, 246, 0.05));
    border: 2px solid var(--accent);
    border-radius: 14px;
    margin-bottom: 24px;
}

.promo-icon {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    background: var(--accent);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 var(--accent-trans); }
    50% { transform: scale(1.05); box-shadow: 0 0 0 10px transparent; }
}

.promo-content {
    flex: 1;
    min-width: 0;
}

.promo-content h4 {
    margin: 0 0 4px;
    font-size: 16px;
    color: var(--text-primary);
}

.promo-content p {
    margin: 0;
    font-size: 14px;
    color: var(--text-secondary);
}

@media (max-width: 1020px) {
    .quick-start-promo {
        flex-direction: column;
        text-align: center;
    }

    .quick-start-promo .btn-primary {
        width: 100%;
        justify-content: center;
    }
}

/* ===== REMINDERS BANNER ===== */
.reminders-banner {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 20px;
}

.reminder-item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 16px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-left: 3px solid var(--accent);
    border-radius: 12px;
    transition: all 0.2s ease;
}

.reminder-item:hover {
    background: var(--bg-card-hover);
    border-color: var(--border-color);
    border-left-color: var(--accent);
}

.reminder-warning {
    border-left-color: var(--warning);
}

.reminder-danger {
    border-left-color: var(--danger);
}

.reminder-accent {
    border-left-color: var(--accent);
}

.reminder-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: var(--accent-trans);
    color: var(--accent-text);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}

.reminder-warning .reminder-icon {
    background: var(--warning-trans);
    color: var(--warning-text);
}

.reminder-danger .reminder-icon {
    background: var(--danger-trans);
    color: var(--danger-text);
}

.reminder-body {
    flex: 1;
    min-width: 0;
}

.reminder-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 2px;
}

.reminder-text {
    font-size: 13px;
    color: var(--text-secondary);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.reminder-actions {
    display: flex;
    gap: 6px;
    flex-shrink: 0;
}

.reminder-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    font-size: 13px;
    font-weight: 500;
    transition: all 0.2s ease;
    white-space: nowrap;
}

.reminder-btn.primary {
    background: var(--accent);
    color: #fff;
}

.reminder-btn.primary:hover {
    background: var(--accent-hover);
}

.reminder-btn.ghost {
    width: 32px;
    height: 32px;
    padding: 0;
    background: transparent;
    color: var(--text-muted);
    border: 1px solid var(--border-color);
}

.reminder-btn.ghost:hover {
    background: var(--border-light);
    color: var(--text-primary);
}

.reminder-btn.ghost.danger:hover {
    background: var(--danger-trans);
    color: var(--danger-text);
    border-color: var(--danger-trans);
}

/* Мобильная адаптация */
@media (max-width: 640px) {
    .reminder-item {
        flex-wrap: wrap;
        gap: 10px;
    }

    .reminder-body {
        flex-basis: calc(100% - 54px);
    }

    .reminder-text {
        white-space: normal;
    }

    .reminder-actions {
        flex-basis: 100%;
        justify-content: flex-end;
        padding-top: 8px;
        border-top: 1px solid var(--border-light);
    }

    .reminder-btn.primary {
        flex: 1;
        justify-content: center;
    }
}

/* ===== GARAGE STATS ===== */
.garage-stats {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 24px;
}

.stat-chip {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: 20px;
    font-size: 13px;
    color: var(--text-secondary);
    transition: all 0.2s ease;
}

.stat-chip:hover {
    border-color: var(--border-color);
    background: var(--bg-card-hover);
}

.stat-chip i {
    color: var(--accent-text);
    font-size: 14px;
}

.stat-chip span {
    font-weight: 700;
    color: var(--text-primary);
}

/* ===== MOTORCYCLES LIST ===== */
.motorcycles-container {
    margin-bottom: 28px;
}

.motorcycles-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.moto-list-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 12px 16px;
    background: var(--bg-secondary);
    border: 2px solid transparent;
    border-radius: 14px;
    cursor: pointer;
    transition: all 0.25s ease;
}

.moto-list-item:hover {
    background: var(--bg-card-hover);
    border-color: var(--border-light);
}

.moto-list-item.active {
    border-color: var(--accent);
    background: var(--accent-trans);
    box-shadow: 0 0 0 1px var(--accent-trans);
}

.moto-card-wrapper {
    display: flex;
    align-items: center;
    gap: 16px;
    flex: 1;
    min-width: 0;
}

.moto-list-preview {
    position: relative;
    width: 56px;
    height: 56px;
    border-radius: 12px;
    overflow: hidden;
    flex-shrink: 0;
    background: var(--bg-card);
}

.moto-list-preview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.moto-list-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    font-size: 22px;
    background: var(--bg-card);
}

.moto-status-badge {
    position: absolute;
    bottom: 4px;
    right: 4px;
    padding: 1px 8px;
    border-radius: 10px;
    font-size: 9px;
    font-weight: 600;
    backdrop-filter: blur(8px);
    background: rgba(0, 0, 0, 0.7);
    color: #fff;
}

.moto-status-badge.status-warning {
    background: rgba(239, 68, 68, 0.9);
}

.moto-status-badge.status-ok {
    background: rgba(16, 185, 129, 0.9);
}

.moto-list-info {
    flex: 1;
    min-width: 0;
}

.moto-list-header {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}

.moto-list-name {
    font-size: 15px;
    font-weight: 600;
    margin: 0;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.moto-list-year {
    font-size: 13px;
    color: var(--text-muted);
    flex-shrink: 0;
}

.moto-list-volume {
    font-size: 12px;
    color: var(--text-muted);
    background: var(--bg-primary);
    padding: 2px 12px;
    border-radius: 12px;
    flex-shrink: 0;
}

.moto-list-meta {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-top: 3px;
    flex-wrap: wrap;
}

.moto-list-mileage {
    font-size: 13px;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 4px;
}

.moto-list-mileage i {
    font-size: 12px;
    color: var(--text-muted);
}

.moto-list-color {
    display: flex;
    align-items: center;
}

.color-dot-sm {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    border: 1px solid var(--border-color);
    display: block;
    transition: transform 0.2s ease;
}

.moto-list-item:hover .color-dot-sm {
    transform: scale(1.15);
}

.moto-list-maintenances {
    font-size: 12px;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 4px;
}

.moto-list-maintenances i {
    font-size: 12px;
}

.moto-list-actions {
    display: flex;
    gap: 2px;
    flex-shrink: 0;
    opacity: 0.6;
    transition: opacity 0.2s ease;
}

.moto-list-item:hover .moto-list-actions {
    opacity: 1;
}

.add-btn {
    padding: 12px;
    border: 2px dashed var(--border-color);
    border-radius: 14px;
    background: transparent;
    color: var(--text-muted);
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.25s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.add-btn:hover {
    border-color: var(--accent);
    color: var(--accent-text);
    background: var(--accent-trans);
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
    margin-bottom: 32px;
    transition: all 0.3s ease;
}

.empty-state:hover {
    border-color: var(--border-color);
}

.empty-icon {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: var(--accent-trans);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 36px;
    color: var(--accent-text);
    margin-bottom: 20px;
    transition: transform 0.3s ease;
}

.empty-icon i {
    margin-bottom: 0;
}

.empty-state:hover .empty-icon {
    transform: scale(1.05);
}

.empty-state h3 {
    font-size: 22px;
    margin: 0 0 8px;
    color: var(--text-primary);
}

.empty-state p {
    color: var(--text-muted);
    font-size: 14px;
    margin: 0 0 28px;
}

/* ===== DETAIL SECTION ===== */
.moto-detail {
    margin-top: 28px;
    padding-top: 24px;
    border-top: 1px solid var(--border-light);
}

/* Stats */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
    margin-bottom: 24px;
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

.stat-card.stat-warning {
    border-color: var(--danger-trans);
    background: var(--danger-trans);
}

.stat-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: var(--accent-trans);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    color: var(--accent-text);
    flex-shrink: 0;
}

.stat-warning .stat-icon {
    background: var(--danger-trans);
    color: var(--danger-text);
}

.stat-info {
    display: flex;
    flex-direction: column;
    min-width: 0;
}

.stat-label {
    font-size: 11px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.4px;
    font-weight: 600;
}

.stat-value {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-primary);
}

.stat-value.text-danger {
    color: var(--danger);
}

.stat-value .text-muted {
    font-size: 13px;
    font-weight: 400;
    color: var(--text-muted);
}

/* Detail Grid */
.detail-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 24px;
}

.detail-card {
    padding: 20px 24px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: 14px;
    transition: all 0.25s ease;
}

.detail-card:hover {
    border-color: var(--border-color);
}

.notes-card {
    display: flex;
    flex-direction: column;
}

.detail-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
}

.detail-title {
    font-size: 14px;
    font-weight: 600;
    margin: 0;
    color: var(--text-primary);
    letter-spacing: 0.3px;
}

.spec-list {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px 20px;
}

.spec-item {
    display: flex;
    flex-direction: column;
    gap: 2px;
    padding: 6px 0;
}

.spec-item.full {
    grid-column: 1 / -1;
}

.spec-label {
    font-size: 11px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.3px;
    font-weight: 500;
}

.spec-value {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-primary);
    word-break: break-all;
}

.spec-value.spec-code {
    font-family: 'Courier New', monospace;
    font-size: 13px;
    letter-spacing: 0.5px;
    background: var(--bg-primary);
    padding: 4px 10px;
    border-radius: 6px;
    display: inline-block;
}

.color-dot {
    display: inline-block;
    width: 32px;
    height: 16px;
    border-radius: 6px;
    border: 1px solid var(--border-color);
    transition: transform 0.2s ease;
}

.color-dot:hover {
    transform: scale(1.1);
}

.notes-content {
    flex: 1;
    display: flex;
    align-items: flex-start;
    padding-top: 4px;
}

.notes-text {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.7;
}

.notes-empty {
    font-size: 14px;
    color: var(--text-muted);
    font-style: italic;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.notes-empty i {
    color: var(--text-muted);
    font-size: 14px;
}

/* Maintenances */
.maintenances-section {
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 24px;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.section-header-left {
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-header-left i {
    color: var(--accent-text);
    font-size: 18px;
}

.section-header h4 {
    font-size: 15px;
    font-weight: 600;
    margin: 0;
}

.btn-link {
    background: none;
    border: none;
    color: var(--accent-text);
    font-weight: 500;
    font-size: 13px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: all 0.25s ease;
    padding: 6px 12px;
    border-radius: 8px;
}

.btn-link:hover {
    color: var(--accent);
    gap: 10px;
    background: var(--accent-trans);
}

.maintenances-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.maintenance-item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 16px;
    background: var(--bg-primary);
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.maintenance-item:hover {
    background: var(--bg-card-hover);
    transform: translateX(4px);
}

.maint-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-size: 14px;
}

.maint-icon-completed {
    background: var(--success-trans);
    color: var(--success-text);
}

.maint-icon-planned {
    background: var(--warning-trans);
    color: var(--warning-text);
}

.maint-icon-overdue {
    background: var(--danger-trans);
    color: var(--danger-text);
}

.maint-info {
    flex: 1;
    min-width: 0;
}

.maint-title {
    font-weight: 500;
    font-size: 13px;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.maint-meta {
    font-size: 12px;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
}

.maint-meta .dot {
    opacity: 0.3;
}

.maint-status {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
}

.maint-status i {
    color: var(--text-muted);
    font-size: 12px;
    opacity: 0.5;
}

.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 500;
    white-space: nowrap;
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

/* Empty small */
.empty-small {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 32px 16px;
    text-align: center;
}

.empty-small i {
    font-size: 28px;
    color: var(--text-muted);
    margin-bottom: 8px;
    opacity: 0.4;
}

.empty-small p {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
}

.empty-small .hint {
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 4px;
}

/* ===== ICON BTN ===== */
.icon-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    padding: 0;
    border: none;
    border-radius: 8px;
    background: transparent;
    color: var(--text-muted);
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 14px;
    line-height: 1;
    flex-shrink: 0;
}

.icon-btn:hover {
    background: var(--border-light);
    color: var(--text-primary);
}

.icon-btn.danger:hover {
    background: var(--danger-trans);
    color: var(--danger);
}

.icon-btn.small {
    width: 28px;
    height: 28px;
    font-size: 12px;
}

.icon-btn i {
    pointer-events: none;
}

/* ===== MEDIA QUERIES ===== */
@media (max-width: 820px) {
    .page-header {
        flex-direction: column;
        align-items: stretch;
        gap: 12px;
    }

    .page-title {
        font-size: 24px;
    }

    .btn-primary {
        width: 100%;
        justify-content: center;
        padding: 12px;
    }

    .stats-grid {
        grid-template-columns: 1fr 1fr;
    }

    .detail-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 600px) {
    .reminder-item {
        flex-wrap: wrap;
        gap: 10px;
    }

    .reminder-body {
        flex-basis: calc(100% - 54px);
    }

    .reminder-text {
        white-space: normal;
    }

    .reminder-actions {
        flex-basis: 100%;
        justify-content: flex-end;
        padding-top: 8px;
        border-top: 1px solid var(--border-light);
    }

    .reminder-btn.primary {
        flex: 1;
        justify-content: center;
    }

    .garage-stats {
        gap: 6px;
    }

    .stat-chip {
        width: 100%;
        font-size: 12px;
        padding: 6px 12px;
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
        font-size: 15px;
    }

    .detail-card {
        padding: 14px 16px;
    }

    .spec-list {
        grid-template-columns: 1fr 1fr;
        gap: 4px 12px;
    }

    .spec-value {
        font-size: 13px;
    }

    .maintenances-section {
        padding: 14px 16px;
    }

    .maintenance-item {
        padding: 10px 12px;
        gap: 10px;
        flex-wrap: wrap;
    }

    .maint-icon {
        width: 32px;
        height: 32px;
        font-size: 12px;
    }

    .maint-title {
        font-size: 12px;
    }

    .maint-meta {
        font-size: 11px;
    }

    .moto-list-item {
        padding: 10px 12px;
        flex-wrap: wrap;
        gap: 10px;
    }

    .moto-list-preview {
        width: 48px;
        height: 48px;
    }

    .moto-list-name {
        font-size: 14px;
    }

    .moto-list-actions {
        opacity: 1;
        width: 100%;
        justify-content: flex-end;
        padding-top: 6px;
        border-top: 1px solid var(--border-light);
    }

    .empty-state {
        padding: 40px 16px;
    }

    .empty-icon {
        width: 60px;
        height: 60px;
        font-size: 26px;
    }

    .empty-state h3 {
        font-size: 18px;
    }
}

@media (max-width: 400px) {
    .stats-grid {
        grid-template-columns: 1fr;
    }

    .spec-list {
        grid-template-columns: 1fr;
    }

    .moto-list-meta {
        gap: 8px;
    }

    .moto-list-volume {
        font-size: 11px;
        padding: 1px 10px;
    }

    .stat-card {
        padding: 10px 12px;
    }
}
</style>
