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

      <!-- Основная сетка: контент + сайдбар -->
      <div class="garage-layout">
        <!-- ===== ЛЕВАЯ КОЛОНКА ===== -->
        <div class="garage-main">
          <!-- Мотоциклы -->
          <section class="motorcycles-section">
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

              <button v-if="motorcycles.length !== 0" @click="showAddMotoModal = true" class="add-btn btn-secondary">
                <i class="fa fa-plus"></i>
                <span>Добавить мотоцикл</span>
              </button>
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
          </section>

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

            <!-- ===== ОБНОВЛЕНИЕ ПРОБЕГА ===== -->
            <div v-if="selectedMotorcycle" class="sidebar-card mileage-card">
              <div class="sidebar-card-header">
                <i class="fa-solid fa-gauge-high"></i>
                <h4>Пробег</h4>
              </div>

              <div class="mileage-display">
                <div class="mileage-value">
                  {{ formatMileage(selectedMotorcycle.mileage) }}
                </div>
                <div class="mileage-updated">
                  <i class="fa fa-clock"></i>
                  Обновлён {{ formatDate(selectedMotorcycle.updated_at || new Date()) }}
                </div>
              </div>

              <div class="mileage-quick-add">
                <span class="quick-add-label">Быстро добавить:</span>
                <div class="quick-add-buttons">
                  <button
                    v-for="step in quickMileageSteps"
                    :key="step"
                    class="quick-add-btn"
                    :disabled="mileageUpdating"
                    @click="quickAddMileage(step)"
                  >
                    +{{ step }}
                  </button>
                </div>
              </div>

              <button
                class="btn-primary mileage-submit"
                :disabled="mileageUpdating"
                @click="openUpdateMileage(selectedMotorcycle)"
              >
                <i :class="mileageUpdating ? 'fa fa-spinner fa-spin' : 'fa fa-pen'"></i>
                {{ mileageUpdating ? 'Обновление...' : 'Ввести точное значение' }}
              </button>
            </div>

            <!-- ===== ДИАГНОСТИКА ===== -->
            <section v-if="selectedMotorcycle" class="diagnostics-section">
              <div class="section-header">
                <div class="section-header-left">
                  <i class="fa fa-stethoscope"></i>
                  <h4>Диагностика</h4>
                </div>
              </div>

              <p class="diag-title">Проведите онлайн-диагностику, указав симптомы</p>
              <p class="diag-hint">Важно: результаты диагностики не являются профессиональными рекомендациями!</p>

              <div class="diagnostics-actions">
                <button @click="showDiagnosticsModal = true" class="diag-cta">
                  Провести онлайн-диагностику
                </button>
              </div>
            </section>

            <!-- Если мотоцикл не выбран -->
            <div v-else class="sidebar-card mileage-card mileage-card-empty">
              <div class="sidebar-card-header">
                <i class="fa-solid fa-gauge-high"></i>
                <h4>Пробег</h4>
              </div>
              <p class="mileage-empty-text">
                <i class="fa fa-info-circle"></i>
                Выберите мотоцикл, чтобы обновить пробег
              </p>
            </div>

            <div class="maintenances-section">
              <div class="section-header">
                <div class="section-header-left">
                  <i class="fa fa-wrench"></i>
                  <h4>Последние обслуживания</h4>
                </div>
                <button @click="router.push('/maintenance')" class="btn-link">
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

          <!-- ===== ПОЛЕЗНЫЕ СТАТЬИ ===== -->
          <section class="articles-section">
            <div class="section-header">
              <div class="section-header-left">
                <i class="fa fa-book-open"></i>
                <h4>Полезные статьи</h4>
              </div>
            </div>

            <div class="articles-grid">
              <article
                v-for="article in filteredArticles"
                :key="article.id"
                class="article-card"
              >
                <div class="article-cover" :class="'article-cover-' + article.tone">
                  <i :class="article.icon"></i>
                </div>
                <div class="article-body">
                  <span class="article-tag">{{ article.tag }}</span>
                  <h5 class="article-title">{{ article.title }}</h5>
                  <p class="article-excerpt">{{ article.excerpt }}</p>
                  <div class="article-footer">
                    <span class="article-time">
                      <i class="fa fa-clock"></i>
                      {{ article.readTime }} мин
                    </span>
                    <button class="btn-link small">Читать <i class="fa fa-arrow-right"></i></button>
                  </div>
                </div>
              </article>
            </div>
          </section>
        </div>

        <!-- ===== ПРАВАЯ КОЛОНКА (САЙДБАР) ===== -->
        <aside class="garage-sidebar">
          <!-- ===== ЗАПИСЬ К МАСТЕРУ ===== -->
          <div class="sidebar-card appointment-card">
            <div class="sidebar-card-header">
              <i class="fa fa-calendar-plus"></i>
              <h4>Запись к мастеру</h4>
            </div>

            <div class="appointment-success">
              <div class="success-icon">
                <i class="fa fa-wrench"></i>
              </div>
              <p>Запишитесь к проверенному мастеру в вашем городе.</p>
            </div>

            <button
              class="btn-primary appointment-submit"
              @click="toast.info('Функция в разработке.')"
            >
              <i class="fa fa-paper-plane"></i>
              Записаться
            </button>
          </div>

          <!-- ===== СОВЕТ ДНЯ ===== -->
          <div class="sidebar-card tip-card">
            <div class="sidebar-card-header">
              <i class="fa fa-lightbulb"></i>
              <h4>Совет дня</h4>
            </div>
            <p class="tip-text">{{ dailyTip }}</p>
            <button class="btn-link small" @click="refreshTip">
              <i class="fa fa-rotate-right"></i>
              Другой совет
            </button>
          </div>
        </aside>
      </div>
    </div>

    <!-- MODALS: MOTO -->
    <AddMotoModal
      :isOpen="showAddMotoModal"
      @created="onMotoCreated"
      @close="showAddMotoModal = false"
    />

    <EditMotoModal
      :isOpen="showEditMotoModal"
      :motorcycle="selectedMotorcycle"
      @close="onMotoUpdated"
    />

    <UpdateMileageModal
      :isOpen="showUpdateMotoMileageModal"
      :motorcycle="selectedMotorcycle"
      @close="onMileageUpdated"
    />

    <EditMotoNoteModal
      :isOpen="showEditMotoNoteModal"
      :motorcycle="selectedMotorcycle"
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

    <DiagnosticsModal
      :is-open="showDiagnosticsModal"
      @close="showDiagnosticsModal = false"
      @write-to-master="handleWriteToMasterFromDiagnostics"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'

import Header from '@/components/Header.vue'
import LoadingOverlay from '@/components/LoadingOverlay.vue'

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
import DiagnosticsModal from '@/components/modals/diagnostics/DiagnosticsModal.vue'

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
const showDiagnosticsModal = ref(false)

// Maintenance modals
const showDetailsMaintenanceModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const showMarkModal = ref(false)

// ===== Mileage quick update =====
const mileageUpdating = ref(false)
const quickMileageSteps = [50, 100, 500, 1000]

async function quickAddMileage(step) {
  const moto = selectedMotorcycle.value
  if (!moto?.id || mileageUpdating.value) return

  mileageUpdating.value = true
  try {
    await motorcyclesStore.updateMileage(moto.id, moto.mileage + step || 0 + step)
    await remindersStore.loadPending()
    toast.success(`Пробег увеличен на ${step} км`)
  } catch (err) {
    console.error('Failed to update mileage:', err)
    toast.error(err.response?.data?.error || 'Не удалось обновить пробег')
  } finally {
    mileageUpdating.value = false
  }
}

// ===== Tips =====
const tips = [
  'Проверяйте давление в шинах раз в неделю — это влияет на управляемость и расход.',
  'Мойте цепь перед смазкой — так смазка держится дольше.',
  'Следите за уровнем антифриза перед длительными поездками.',
  'Храните мотоцикл с полным баком — меньше конденсата в баке.',
  'Проверяйте натяжение цепи каждые 500 км.',
]
const dailyTip = ref(tips[0])

function refreshTip() {
  const idx = Math.floor(Math.random() * tips.length)
  dailyTip.value = tips[idx]
}

// ===== Lifecycle =====
onMounted(async () => {
  try {
    await Promise.all([
      motorcyclesStore.loadAll(),
      remindersStore.loadPending(),
    ])
    refreshTip()
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

// ===== Moto actions =====
function openEditMoto(moto) {
  selectMotorcycle(moto)
  showEditMotoModal.value = true}

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


function handleWriteToMasterFromDiagnostics() {
  showDiagnosticsModal.value = false
  document.querySelector('.appointment-card')?.scrollIntoView({
    behavior: 'smooth',
    block: 'start',
  })
}
</script>

<style scoped>
/* ============================================
   LAYOUT: MAIN + SIDEBAR
   ============================================ */
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
  gap: 28px;
}

.garage-sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
  position: sticky;
  top: 24px;
}

/* ============================================
   QUICK START PROMO
   ============================================ */
.quick-start-promo {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px 24px;
    background: linear-gradient(135deg, var(--accent-trans), rgba(139, 92, 246, 0.05));
    border: 2px solid var(--accent);
    border-radius: var(--radius-lg);
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

.promo-content { flex: 1; min-width: 0; }
.promo-content h4 { margin: 0 0 4px; font-size: 16px; color: var(--text-primary); }
.promo-content p { margin: 0; font-size: 14px; color: var(--text-secondary); }

/* ============================================
   REMINDERS BANNER
   ============================================ */
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
    border-radius: var(--radius-lg);
    transition: all var(--transition-base);
}

.reminder-item:hover {
    background: var(--bg-card-hover);
    border-color: var(--border-color);
    border-left-color: var(--accent);
}

.reminder-warning { border-left-color: var(--warning); }
.reminder-danger  { border-left-color: var(--danger); }
.reminder-accent  { border-left-color: var(--accent); }

.reminder-icon {
    width: 40px;
    height: 40px;
    border-radius: var(--radius-md);
    background: var(--accent-trans);
    color: var(--accent-text);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
    min-height: 40px;
}

.reminder-warning .reminder-icon { background: var(--warning-trans); color: var(--warning-text); }
.reminder-danger  .reminder-icon { background: var(--danger-trans);  color: var(--danger-text); }

.reminder-body { flex: 1; min-width: 0; }
.reminder-title { font-size: 14px; font-weight: var(--fw-semibold); color: var(--text-primary); margin-bottom: 2px; }
.reminder-text {
    font-size: 13px;
    color: var(--text-secondary);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.reminder-actions { display: flex; gap: 6px; flex-shrink: 0; }

.reminder-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: var(--radius-md);
    border: none;
    cursor: pointer;
    font-size: 13px;
    font-weight: var(--fw-medium);
    transition: all var(--transition-base);
    white-space: nowrap;
    min-height: 32px;
}

.reminder-btn.primary {
    background: var(--accent);
    color: #fff;
}
.reminder-btn.primary:hover { background: var(--accent-hover); }

.reminder-btn.ghost {
    width: 32px;
    height: 32px;
    padding: 0;
    background: transparent;
    color: var(--text-muted);
    border: 1px solid var(--border-color);
}
.reminder-btn.ghost:hover { background: var(--border-light); color: var(--text-primary); }
.reminder-btn.ghost.danger:hover {
    background: var(--danger-trans);
    color: var(--danger-text);
    border-color: var(--danger-trans);
}

/* ============================================
   GARAGE STATS
   ============================================ */
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
    border-radius: var(--radius-full);
    font-size: 13px;
    color: var(--text-secondary);
    transition: all var(--transition-base);
}
.stat-chip:hover { border-color: var(--border-color); background: var(--bg-card-hover); }
.stat-chip i { color: var(--accent-text); font-size: 14px; }
.stat-chip span { font-weight: var(--fw-bold); color: var(--text-primary); }

/* ============================================
   MOTORCYCLES LIST
   ============================================ */
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
    border-radius: var(--radius-lg);
    cursor: pointer;
    transition: all var(--transition-base);
}
.moto-list-item:hover { background: var(--bg-card-hover); border-color: var(--border-light); }
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
    border-radius: var(--radius-md);
    overflow: hidden;
    flex-shrink: 0;
    background: var(--bg-card);
}
.moto-list-preview img { width: 100%; height: 100%; object-fit: cover; }

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

.moto-list-info { flex: 1; min-width: 0; }

.moto-list-header {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}

.moto-list-name {
    font-size: 15px;
    font-weight: var(--fw-semibold);
    margin: 0;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
}

.moto-list-year { font-size: 13px; color: var(--text-muted); flex-shrink: 0; }

.moto-list-volume {
    font-size: 12px;
    color: var(--text-muted);
    background: var(--bg-primary);
    padding: 2px 12px;
    border-radius: var(--radius-full);
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
.moto-list-mileage i { font-size: 12px; color: var(--text-muted); }

.moto-list-color { display: flex; align-items: center; }

.color-dot-sm {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    border: 1px solid var(--border-color);
    display: block;
    transition: transform var(--transition-base);
}
.moto-list-item:hover .color-dot-sm { transform: scale(1.15); }

.moto-list-maintenances {
    font-size: 12px;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 4px;
}
.moto-list-maintenances i { font-size: 12px; }

.moto-list-actions {
    display: flex;
    gap: 2px;
    flex-shrink: 0;
    opacity: 0.6;
    transition: opacity var(--transition-base);
}
.moto-list-item:hover .moto-list-actions { opacity: 1; }

.add-btn {
    padding: 12px;
    border: 2px dashed var(--border-color);
    border-radius: var(--radius-lg);
    background: transparent;
    color: var(--text-muted);
    font-size: 14px;
    font-weight: var(--fw-medium);
    cursor: pointer;
    transition: all var(--transition-base);
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

/* ============================================
   EMPTY STATE
   ============================================ */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 60px 24px;
    background: var(--bg-secondary);
    border: 2px dashed var(--border-color);
    border-radius: var(--radius-xl);
    text-align: center;
    transition: all var(--transition-base);
}
.empty-state:hover { border-color: var(--border-color); }

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
    transition: transform var(--transition-base);
}
.empty-icon i { margin-bottom: 0; }
.empty-state:hover .empty-icon { transform: scale(1.05); }

.empty-state h3 { font-size: 22px; margin: 0 0 8px; color: var(--text-primary); }
.empty-state p { color: var(--text-muted); font-size: 14px; margin: 0 0 28px; }

/* ============================================
   DETAIL SECTION
   ============================================ */
.moto-detail {
    padding-top: 4px;
}

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
    border-radius: var(--radius-lg);
    transition: all var(--transition-base);
    min-width: 0;
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
    min-height: 44px;
    border-radius: var(--radius-md);
    background: var(--accent-trans);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    color: var(--accent-text);
    flex-shrink: 0;
}
.stat-warning .stat-icon { background: var(--danger-trans); color: var(--danger-text); }

.stat-info { display: flex; flex-direction: column; min-width: 0; }
.stat-label {
    font-size: 11px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.4px;
    font-weight: var(--fw-semibold);
}
.stat-value {
    font-size: 18px;
    font-weight: var(--fw-bold);
    color: var(--text-primary);
    overflow: hidden;
    text-overflow: ellipsis;
}
.stat-value.text-danger { color: var(--danger); }
.stat-value .text-muted { font-size: 13px; font-weight: var(--fw-normal); color: var(--text-muted); }

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
    border-radius: var(--radius-lg);
    transition: all var(--transition-base);
}
.detail-card:hover { border-color: var(--border-color); }
.notes-card { display: flex; flex-direction: column; }

.detail-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
}

.detail-title {
    font-size: 14px;
    font-weight: var(--fw-semibold);
    margin: 0;
    color: var(--text-primary);
    letter-spacing: 0.3px;
}

.spec-list {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px 20px;
}
.spec-item { display: flex; flex-direction: column; gap: 2px; padding: 6px 0; min-width: 0; }
.spec-item.full { grid-column: 1 / -1; }
.spec-label {
    font-size: 11px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.3px;
    font-weight: var(--fw-medium);
}
.spec-value {
    font-size: 14px;
    font-weight: var(--fw-medium);
    color: var(--text-primary);
    word-break: break-word;
    overflow-wrap: anywhere;
}
.spec-value.spec-code {
    font-family: var(--font-mono);
    font-size: 13px;
    letter-spacing: 0.5px;
    background: var(--bg-primary);
    padding: 4px 10px;
    border-radius: var(--radius-sm);
    display: inline-block;
}

.color-dot {
    display: inline-block;
    width: 32px;
    height: 16px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border-color);
    transition: transform var(--transition-base);
}
.color-dot:hover { transform: scale(1.1); }

.notes-content { flex: 1; display: flex; align-items: flex-start; padding-top: 4px; }
.notes-text { font-size: 14px; color: var(--text-secondary); margin: 0; line-height: var(--leading-relaxed); }
.notes-empty {
    font-size: 14px;
    color: var(--text-muted);
    font-style: italic;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.notes-empty i { color: var(--text-muted); font-size: 14px; }

/* ============================================
   MAINTENANCES
   ============================================ */
.maintenances-section {
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-lg);
    padding: 20px 24px;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
    flex-wrap: wrap;
}

.section-header-left { display: flex; align-items: center; gap: 10px; min-width: 0; }
.section-header-left i { color: var(--accent-text); font-size: 18px; }
.section-header h4 { font-size: 15px; font-weight: var(--fw-semibold); margin: 0; }

.btn-link {
    background: none;
    border: none;
    color: var(--accent-text);
    font-weight: var(--fw-medium);
    font-size: 13px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: all var(--transition-base);
    padding: 6px 12px;
    border-radius: var(--radius-md);
    min-height: 32px;
}
.btn-link:hover { color: var(--accent); gap: 10px; background: var(--accent-trans); }
.btn-link:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-link.small { font-size: 12px; padding: 4px 8px; }

.maintenances-list { display: flex; flex-direction: column; gap: 6px; }

.maintenance-item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 16px;
    background: var(--bg-primary);
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all var(--transition-base);
    min-width: 0;
}
.maintenance-item:hover { background: var(--bg-card-hover); transform: translateX(4px); }

.maint-icon {
    width: 36px;
    height: 36px;
    min-height: 36px;
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-size: 14px;
}
.maint-icon-completed { background: var(--success-trans); color: var(--success-text); }
.maint-icon-planned   { background: var(--warning-trans); color: var(--warning-text); }
.maint-icon-overdue   { background: var(--danger-trans);  color: var(--danger-text); }

.maint-info { flex: 1; min-width: 0; }
.maint-title {
    font-weight: var(--fw-medium);
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
.maint-meta .dot { opacity: 0.3; }

.maint-status { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.maint-status i { color: var(--text-muted); font-size: 12px; opacity: 0.5; }

.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: var(--radius-full);
    font-size: 11px;
    font-weight: var(--fw-medium);
    white-space: nowrap;
}
.badge-success { background: var(--success-trans); color: var(--success-text); }
.badge-warning { background: var(--warning-trans); color: var(--warning-text); }
.badge-danger  { background: var(--danger-trans);  color: var(--danger-text); }
.badge-gray    { background: rgba(107, 114, 128, 0.15); color: #9ca3af; }

.empty-small {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 32px 16px;
    text-align: center;
}
.empty-small i { font-size: 28px; color: var(--text-muted); margin-bottom: 8px; opacity: 0.4; }
.empty-small p { font-size: 14px; color: var(--text-secondary); margin: 0; }
.empty-small .hint { font-size: 12px; color: var(--text-muted); margin-top: 4px; }

/* ============================================
   DIAGNOSTICS
   ============================================ */
.diagnostics-section {
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-lg);
    padding: 20px 24px;
}

.diagnostics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 10px;
    margin-bottom: 16px;
}

.diagnostic-card {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 14px;
    background: var(--bg-primary);
    border: 1px solid var(--border-light);
    border-left: 3px solid var(--border-color);
    border-radius: var(--radius-md);
    transition: all var(--transition-base);
    min-width: 0;
}
.diagnostic-card:hover { background: var(--bg-card-hover); }

.diag-ok      { border-left-color: var(--success); }
.diag-warning { border-left-color: var(--warning); }
.diag-unknown { border-left-color: var(--text-muted); }

.diag-icon {
    width: 38px;
    height: 38px;
    min-height: 38px;
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
    background: var(--bg-secondary);
    color: var(--text-secondary);
}
.diag-ok .diag-icon      { background: var(--success-trans); color: var(--success-text); }
.diag-warning .diag-icon { background: var(--warning-trans); color: var(--warning-text); }
.diag-unknown .diag-icon { background: var(--border-light);   color: var(--text-muted); }

.diag-body { flex: 1; min-width: 0; }
.diag-title {
    font-weight: var(--fw-semibold);
    color: var(--text-primary);
    overflow: hidden;
    text-overflow: ellipsis;
    text-align: center;
    margin-bottom: 8px;
}
.diag-hint {
    font-size: 12px;
    color: var(--text-muted);
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 12px;
    text-align: center;
}

.diag-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: var(--radius-full);
    font-size: 11px;
    font-weight: var(--fw-medium);
    white-space: nowrap;
}
.diag-badge-ok      { background: var(--success-trans); color: var(--success-text); }
.diag-badge-warning { background: var(--warning-trans); color: var(--warning-text); }
.diag-badge-unknown { background: var(--border-light);   color: var(--text-muted); }

.diagnostics-actions {
    display: flex;
    justify-content: center;
}

.diag-cta {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 18px;
    border: 1px solid var(--accent);
    border-radius: var(--radius-md);
    font-size: 13px;
    font-weight: var(--fw-medium);
    cursor: pointer;
    transition: all var(--transition-base);
    min-height: 40px;
}
.diag-cta:hover { background: var(--accent-trans); color: var(--text-primary); }

/* ============================================
   ARTICLES
   ============================================ */
.articles-section {
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-lg);
    padding: 20px 24px;
    display: none;
}

.articles-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 12px;
}

.article-card {
    display: flex;
    flex-direction: column;
    background: var(--bg-primary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-lg);
    overflow: hidden;
    transition: all var(--transition-base);
    cursor: pointer;
}
.article-card:hover {
    border-color: var(--border-color);
    transform: translateY(-3px);
    box-shadow: var(--shadow-md);
}

.article-cover {
    height: 72px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
}
.article-cover-accent  { background: var(--accent-trans);  color: var(--accent-text); }
.article-cover-warning { background: var(--warning-trans); color: var(--warning-text); }
.article-cover-success { background: var(--success-trans); color: var(--success-text); }

.article-body { padding: 14px 16px; display: flex; flex-direction: column; gap: 6px; flex: 1; }

.article-tag {
    align-self: flex-start;
    font-size: 10px;
    font-weight: var(--fw-semibold);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--accent-text);
    background: var(--accent-trans);
    padding: 2px 8px;
    border-radius: var(--radius-full);
}

.article-title {
    font-size: 14px;
    font-weight: var(--fw-semibold);
    color: var(--text-primary);
    margin: 0;
    line-height: var(--leading-tight);
}

.article-excerpt {
    font-size: 12px;
    color: var(--text-secondary);
    margin: 0;
    line-height: var(--leading-base);
    flex: 1;
}

.article-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-top: 4px;
    padding-top: 8px;
    border-top: 1px solid var(--border-light);
}

.article-time {
    font-size: 11px;
    color: var(--text-muted);
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

/* ============================================
   SIDEBAR CARDS
   ============================================ */
.sidebar-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-lg);
    padding: 18px 20px;
    transition: all var(--transition-base);
}
.sidebar-card:hover { border-color: var(--border-color); }

.sidebar-card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 16px;
}
.sidebar-card-header i { color: var(--accent-text); font-size: 16px; }
.sidebar-card-header h4 { font-size: 14px; font-weight: var(--fw-semibold); margin: 0; }

/* --- Mileage card --- */
.mileage-card { display: flex; flex-direction: column; gap: 14px; margin-bottom: 20px; }

.mileage-display {
    display: flex;
    flex-direction: column;
    gap: 2px;
    padding: 12px 14px;
    background: var(--bg-primary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
}

.mileage-value {
    font-size: 26px;
    font-weight: var(--fw-bold);
    color: var(--text-primary);
    letter-spacing: -0.5px;
    line-height: 1.1;
}

.mileage-updated {
    font-size: 11px;
    color: var(--text-muted);
    display: inline-flex;
    align-items: center;
    gap: 5px;
}
.mileage-updated i { font-size: 10px; }

.mileage-quick-add { display: flex; flex-direction: column; gap: 8px; }

.quick-add-label {
    font-size: 11px;
    font-weight: var(--fw-semibold);
    text-transform: uppercase;
    letter-spacing: 0.4px;
    color: var(--text-muted);
}

.quick-add-buttons {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 6px;
}

.quick-add-btn {
    padding: 8px 4px;
    border-radius: var(--radius-md);
    border: 1px solid var(--border-color);
    background: var(--bg-primary);
    color: var(--text-primary);
    font-size: 12px;
    font-weight: var(--fw-semibold);
    cursor: pointer;
    transition: all var(--transition-base);
    min-height: 36px;
    font-family: var(--font-mono);
}
.quick-add-btn:hover:not(:disabled) {
    border-color: var(--accent);
    background: var(--accent-trans);
    color: var(--accent-text);
    transform: translateY(-1px);
}
.quick-add-btn:active:not(:disabled) { transform: translateY(0); }
.quick-add-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.mileage-submit {
    width: 100%;
    padding: 10px 16px;
    border-radius: var(--radius-md);
    background: var(--accent);
    color: #fff;
    border: none;
    font-size: 13px;
    font-weight: var(--fw-semibold);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: all var(--transition-base);
    min-height: 40px;
}
.mileage-submit:hover:not(:disabled) { background: var(--accent-hover); transform: translateY(-1px); }
.mileage-submit:disabled { opacity: 0.5; cursor: not-allowed; }

.mileage-card-empty .mileage-empty-text {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: var(--text-muted);
    margin: 0;
}
.mileage-card-empty .mileage-empty-text i { color: var(--text-muted); }

/* Мобильная адаптация */
@media (max-width: 400px) {
    .quick-add-buttons { grid-template-columns: repeat(2, 1fr); }
    .mileage-value { font-size: 22px; }
}

/* --- Appointment form --- */
.appointment-form { display: flex; flex-direction: column; gap: 12px; }

.appointment-field { display: flex; flex-direction: column; gap: 4px; }
.appointment-field label {
    font-size: 11px;
    font-weight: var(--fw-semibold);
    text-transform: uppercase;
    letter-spacing: 0.4px;
    color: var(--text-muted);
}

.appointment-input {
    width: 100%;
    padding: 8px 12px;
    border-radius: var(--radius-md);
    border: 1px solid var(--border-color);
    background: var(--bg-input);
    color: var(--text-primary);
    font-size: 13px;
    font-family: inherit;
    transition: border var(--transition-base);
    min-height: 38px;
}
.appointment-input:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: var(--shadow-focus);
}

.master-list { display: flex; flex-direction: column; gap: 4px; }

.master-chip {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 6px 10px;
    border-radius: var(--radius-md);
    border: 1px solid var(--border-light);
    background: var(--bg-primary);
    color: var(--text-primary);
    cursor: pointer;
    transition: all var(--transition-base);
    text-align: left;
    min-height: 40px;
}
.master-chip:hover { border-color: var(--accent); }
.master-chip.active {
    border-color: var(--accent);
    background: var(--accent-trans);
}

.master-avatar {
    width: 28px;
    height: 28px;
    min-height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: var(--fw-bold);
    color: #fff;
    flex-shrink: 0;
}

.master-info { display: flex; flex-direction: column; min-width: 0; }
.master-name { font-size: 12px; font-weight: var(--fw-medium); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.master-spec { font-size: 11px; color: var(--text-muted); }

.appointment-submit {
    width: 100%;
    padding: 10px 16px;
    border-radius: var(--radius-md);
    background: var(--accent);
    color: #fff;
    border: none;
    font-size: 13px;
    font-weight: var(--fw-semibold);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: all var(--transition-base);
    min-height: 40px;
}
.appointment-submit:hover:not(:disabled) { background: var(--accent-hover); transform: translateY(-1px); }
.appointment-submit:disabled { opacity: 0.5; cursor: not-allowed; }

.appointment-success {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 8px;
    padding: 8px 0;
}
.success-icon {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    background: var(--success-trans);
    color: var(--success);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
}
.appointment-success h5 { margin: 0; font-size: 15px; color: var(--text-primary); }
.appointment-success p { margin: 0; font-size: 13px; color: var(--text-secondary); }
.appointment-success .btn-outline {
    margin-top: 8px;
    padding: 8px 16px;
    border-radius: var(--radius-md);
    border: 1px solid var(--border-color);
    background: transparent;
    color: var(--text-primary);
    font-size: 13px;
    cursor: pointer;
    transition: all var(--transition-base);
    display: inline-flex;
    align-items: center;
    gap: 6px;
    min-height: 36px;
}
.appointment-success .btn-outline:hover { border-color: var(--accent); color: var(--accent-text); }

/* --- Tip card --- */
.tip-card { display: flex; flex-direction: column; gap: 12px; }
.tip-text {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: var(--leading-relaxed);
    margin: 0;
}

/* ============================================
   ICON BUTTON
   ============================================ */
.icon-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    min-height: 34px;
    padding: 0;
    border: none;
    border-radius: var(--radius-md);
    background: transparent;
    color: var(--text-muted);
    cursor: pointer;
    transition: all var(--transition-base);
    font-size: 14px;
    line-height: 1;
    flex-shrink: 0;
    touch-action: manipulation;
}
.icon-btn:hover { background: var(--border-light); color: var(--text-primary); }
.icon-btn.danger:hover { background: var(--danger-trans); color: var(--danger); }
.icon-btn.small { width: 28px; height: 28px; min-height: 28px; font-size: 12px; }
.icon-btn i { pointer-events: none; }

/* ============================================
   АДАПТИВ
   ============================================ */

/* --- Планшеты --- */
@media (max-width: 1100px) {
    .garage-layout { grid-template-columns: 1fr; }
    .garage-sidebar { position: static; }
    .stats-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 820px) {
    .detail-grid { grid-template-columns: 1fr; }
    .stats-grid  { grid-template-columns: repeat(2, 1fr); }
    .quick-start-promo { flex-direction: column; text-align: center; }
    .quick-start-promo .btn-primary { width: 100%; justify-content: center; }
    .stats-grid { display: flex; flex-direction: column; }

    .maintenances-section,
    .diagnostics-section,
    .articles-section { padding: 14px 16px; }
    .maintenance-item { padding: 10px 12px; gap: 10px; }
    .maint-icon { width: 32px; height: 32px; min-height: 32px; font-size: 12px; }
    .maint-title { font-size: 12px; }
    .maint-meta { font-size: 11px; }
    .maint-status i { display: none; }

    .diagnostics-grid { grid-template-columns: 1fr 1fr; }
    .articles-grid { grid-template-columns: 1fr 1fr; }
}

/* --- Мобильные (широкие) --- */
@media (max-width: 640px) {
    .reminder-item { flex-wrap: wrap; gap: 10px; }
    .reminder-body { flex-basis: calc(100% - 54px); }
    .reminder-text { white-space: normal; }
    .reminder-actions {
        flex-basis: 100%;
        justify-content: flex-end;
        padding-top: 8px;
        border-top: 1px solid var(--border-light);
    }
    .reminder-btn.primary { flex: 1; justify-content: center; }

    .garage-stats { gap: 6px; }
    .stat-chip { width: 100%; font-size: 12px; padding: 6px 12px; }

    .stats-grid { grid-template-columns: repeat(2, 1fr); gap: 8px; }
    .stat-card { padding: 12px 14px; gap: 10px; }
    .stat-icon { width: 36px; height: 36px; min-height: 36px; font-size: 15px; }
    .stat-value { font-size: 15px; }

    .detail-card { padding: 14px 16px; }
    .spec-list { gap: 4px 12px; }
    .spec-value { font-size: 13px; }

    .maintenances-section { padding: 14px 16px; }
    .maintenance-item { padding: 10px 12px; gap: 10px; }
    .maint-icon { width: 32px; height: 32px; min-height: 32px; font-size: 12px; }
    .maint-title { font-size: 12px; }
    .maint-meta { font-size: 11px; }
    .maint-status i { display: none; }

    .moto-list-item { padding: 10px 12px; gap: 10px; }
    .moto-list-preview { width: 48px; height: 48px; }
    .moto-list-name { font-size: 14px; }

    .moto-list-actions { opacity: 1; gap: 0; }
    .icon-btn { width: 32px; height: 32px; min-height: 32px; font-size: 13px; }

    .empty-state { padding: 40px 16px; }
    .empty-icon { width: 60px; height: 60px; font-size: 26px; }
    .empty-state h3 { font-size: 18px; }

    .section-header { gap: 8px; }
    .article-filters { width: 100%; }
    .article-filter-btn { flex: 1; text-align: center; }

    .diagnostics-grid { grid-template-columns: 1fr; }
    .articles-grid { grid-template-columns: 1fr; }

    .diagnostics-actions { justify-content: stretch; }
    .diag-cta { width: 100%; justify-content: center; }
}

/* --- Мобильные (узкие) --- */
@media (max-width: 480px) {
    .moto-list-item { flex-wrap: wrap; }
    .moto-card-wrapper { flex-basis: 100%; }
    .moto-list-actions {
        width: 100%;
        justify-content: flex-end;
        padding-top: 8px;
        border-top: 1px solid var(--border-light);
        opacity: 1;
    }

    .quick-start-promo { padding: 16px; gap: 12px; }
    .promo-icon { width: 44px; height: 44px; font-size: 18px; }
    .promo-content h4 { font-size: 15px; }
    .promo-content p { font-size: 13px; }

    .maintenance-item { flex-wrap: wrap; }
    .maint-info { flex-basis: calc(100% - 52px); }
    .maint-status {
        flex-basis: 100%;
        justify-content: flex-end;
        padding-top: 6px;
        border-top: 1px solid var(--border-light);
    }
}

/* --- Очень узкие --- */
@media (max-width: 400px) {
    .stats-grid { grid-template-columns: 1fr; }
    .spec-list  { grid-template-columns: 1fr; }
    .moto-list-meta { gap: 8px; }
    .moto-list-volume { font-size: 11px; padding: 1px 10px; }
    .stat-card { padding: 10px 12px; }

    .stat-chip { padding: 6px 10px; font-size: 11px; }
    .stat-chip i { font-size: 12px; }

    .moto-list-actions { justify-content: space-between; }
    .icon-btn { width: 34px; height: 34px; min-height: 34px; }
}
</style>
