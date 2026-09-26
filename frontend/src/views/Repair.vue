<template>
  <div class="repair-page">
    <LoadingOverlay :isLoading="loading" text="Загрузка данных..." />

    <Header
      title="Ремонт и обслуживание"
      subtitle="Проводите обслуживание мотоцикла с нашими мануалами"
    />

    <!-- ВЫБОР МОТОЦИКЛА И ОБСЛУЖИВАНИЯ -->
    <div class="selection-section">
      <div class="selection-flow">
        <!-- Шаг 1: Мотоцикл -->
        <div class="selection-step">
          <div class="step-indicator">
            <span class="step-number">1</span>
          </div>
          <div class="step-content">
            <BaseSelect
              v-model="selectedMotoId"
              label="Выберите мотоцикл"
              placeholder="Выберите мотоцикл"
              required
            >
              <option
                v-for="moto in motorcycles"
                :key="moto.id"
                :value="moto.id"
              >
                {{ moto.name }}
              </option>
            </BaseSelect>

            <div v-if="selectedMotoData" class="moto-info">
              <span class="moto-mileage">
                <i class="fa-solid fa-gauge-high"></i>
                {{ formatMileage(selectedMotoData.mileage) }}
              </span>
              <span class="moto-year" v-if="selectedMotoData.years">
                <i class="fa fa-calendar"></i>
                {{ selectedMotoData.years }}
              </span>
            </div>
          </div>
        </div>

        <!-- Шаг 2: Обслуживание -->
        <div class="selection-step" :class="{ disabled: !selectedMotoId }">
          <div class="step-indicator">
            <span class="step-number">2</span>
          </div>
          <div class="step-content">
            <BaseSelect
              v-model="selectedMaintenanceId"
              label="Выберите обслуживание"
              placeholder="Выберите обслуживание"
              :disabled="!selectedMotoId"
              required
            >
              <option
                v-for="m in availableMaintenances"
                :key="m.id"
                :value="m.id"
              >
                {{ m.title }}
              </option>
            </BaseSelect>

            <div v-if="selectedMaintenanceData" class="maintenance-info">
              <span class="info-badge" :class="maintenanceStatusClass">
                <i :class="maintenanceStatusIcon"></i>
                {{ maintenanceStatusText }}
              </span>
              <span class="info-mileage" v-if="selectedMaintenanceData.planned_mileage">
                <i class="fa fa-flag-checkered"></i>
                {{ selectedMaintenanceData.planned_mileage }} км
              </span>
            </div>
          </div>
        </div>

        <!-- Шаг 3: Результат -->
        <div
          class="selection-step result-step"
          :class="{
            disabled: !selectedMotoId || !selectedMaintenanceId,
            found: manual,
            notfound: !manual && selectedMotoId && selectedMaintenanceId,
          }"
        >
          <div class="step-content">
            <div class="result-status">
              <div
                class="result-icon"
                :class="{
                  success: manual,
                  empty: !manual && selectedMotoId && selectedMaintenanceId,
                  waiting: !selectedMotoId || !selectedMaintenanceId,
                }"
              >
                <i :class="resultIcon"></i>
              </div>

              <div class="result-text">
                <h4 v-if="manual">Мануал найден</h4>
                <h4 v-else-if="selectedMotoId && selectedMaintenanceId">Мануал не найден</h4>
                <h4 v-else>Ожидание выбора</h4>
                <p v-if="manual">Инструкция автоматически подобрана</p>
                <p v-else-if="selectedMotoId && selectedMaintenanceId">
                  Мы не нашли подходящий мануал. Вы можете создать его сами.
                </p>
                <p v-else>Выберите мотоцикл и обслуживание</p>
              </div>
            </div>

            <div class="result-actions">
              <BaseButton
                v-if="manual"
                variant="outline"
                icon="fa fa-arrow-down"
                block
                @click="scrollToManual"
              >
                К инструкции
              </BaseButton>

              <BaseButton
                v-else-if="selectedMotoId && selectedMaintenanceId && !manual"
                variant="outline"
                icon="fa fa-plus"
                block
                @click="openCreateManual"
              >
                Создать мануал
              </BaseButton>

              <BaseButton v-else variant="secondary" block disabled>
                <i class="fa fa-hourglass-start"></i> Ожидание
              </BaseButton>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ===== МАНУАЛ ===== -->
    <div v-if="manual" class="manual-section" id="manual-section">
      <!-- О МАНУАЛЕ -->
      <div class="manual-header-card">
        <h2 class="manual-title">{{ manual.title }}</h2>
        <p class="manual-description">
          {{ manual.description || 'Инструкция по выполнению обслуживания' }}
        </p>

        <div class="manual-meta-tags">
          <span class="tag" v-if="manual.category">
            <i class="fa fa-tag"></i> {{ getCategoryLabel(manual.category) }}
          </span>
          <span class="tag" v-if="manual.difficult">
            <i class="fa fa-signal"></i> {{ getDifficultyLabel(manual.difficult) }}
          </span>
          <span class="tag">
            <i class="fa fa-motorcycle"></i> {{ manual.motorcycle }}
          </span>
          <span class="tag" v-if="manual.time_estimate">
            <i class="fa fa-clock"></i> {{ manual.time_estimate }}
          </span>
          <span class="tag" v-if="manual.interval">
            <i class="fa fa-repeat"></i> {{ manual.interval }}
          </span>
        </div>
      </div>

      <!-- БЕЗОПАСНОСТЬ -->
      <div v-if="manual.safety_tip || manual.warnings || manual.conditions" class="block block-safety">
        <h4 class="block-title">
          <i class="fa fa-shield"></i> Безопасность и подготовка
        </h4>

        <div v-if="manual.safety_tip" class="safety-item safety-tip">
          <i class="fa fa-lightbulb"></i>
          <span>{{ manual.safety_tip }}</span>
        </div>

        <div v-if="manual.warnings" class="safety-item safety-warning">
          <i class="fa fa-exclamation-triangle"></i>
          <span>{{ manual.warnings }}</span>
        </div>

        <div v-if="manual.conditions" class="safety-item safety-condition">
          <i class="fa fa-check-circle"></i>
          <span>{{ manual.conditions }}</span>
        </div>
      </div>

      <!-- ССЫЛКИ НА ДОКУМЕНТАЦИЮ -->
      <div v-if="manual.docs_links && manual.docs_links.length > 0" class="block block-docs">
        <h4 class="block-title">
          <i class="fa fa-link"></i> Ссылки на документацию
        </h4>

        <div class="docs-list">
          <a
            v-for="(link, index) in manual.docs_links"
            :key="index"
            :href="link"
            target="_blank"
            rel="noopener noreferrer"
            class="docs-link"
          >
            <i class="fa fa-file-pdf-o"></i>
            <span>Документация {{ index + 1 }}</span>
            <i class="fa fa-external-link"></i>
          </a>
        </div>
      </div>

      <!-- ТЕХНИЧЕСКИЕ ДАННЫЕ -->
      <div v-if="manual.specs && hasSpecs(manual.specs)" class="block block-specs">
        <h4 class="block-title">
          <i class="fa fa-table"></i> Технические данные
        </h4>

        <div v-if="manual.specs.torque && manual.specs.torque.length > 0" class="specs-section">
          <h5 class="specs-subtitle">Моменты затяжки</h5>
          <div class="torque-table">
            <div class="torque-header">
              <span>Название</span>
              <span>Момент (Н·м)</span>
              <span>Примечание</span>
            </div>
            <div
              v-for="(item, index) in manual.specs.torque"
              :key="index"
              class="torque-row"
            >
              <span>{{ item.name || '—' }}</span>
              <span>{{ item.nm || '—' }}</span>
              <span>{{ item.note || '—' }}</span>
            </div>
          </div>
        </div>

        <div v-if="manual.specs.fluids && Object.keys(manual.specs.fluids).length > 0" class="specs-section">
          <h5 class="specs-subtitle">Объёмы жидкостей</h5>
          <div class="fluids-grid">
            <div
              v-for="(value, key) in manual.specs.fluids"
              :key="key"
              class="fluid-item"
            >
              <span class="fluid-label">{{ getFluidLabel(key) }}</span>
              <span class="fluid-value">{{ value }}</span>
            </div>
          </div>
        </div>

        <div v-if="manual.specs.tolerances && Object.keys(manual.specs.tolerances).length > 0" class="specs-section">
          <h5 class="specs-subtitle">Допуски и зазоры</h5>
          <div class="tolerances-grid">
            <div
              v-for="(value, key) in manual.specs.tolerances"
              :key="key"
              class="tolerance-item"
            >
              <span class="tolerance-label">{{ getToleranceLabel(key) }}</span>
              <span class="tolerance-value">{{ value }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- ШАГИ -->
      <div class="manual-content">
        <div class="steps-wrapper">
          <h3 class="steps-title">
            <i class="fa fa-list-ol"></i>
            Инструкция по шагам
            <span class="steps-count">{{ manualSteps.length }} шаг{{ manualSteps.length > 1 ? 'а' : '' }}</span>
          </h3>

          <div class="steps-list">
            <div
              v-for="(step, index) in manualSteps"
              :key="step.order || index"
              class="step-item"
            >
              <div class="step-marker">
                <span class="step-number">{{ step.order || index + 1 }}</span>
                <div class="step-connector" v-if="index < manualSteps.length - 1"></div>
              </div>

              <div class="step-body">
                <h4 class="step-title">{{ step.title || `Шаг ${index + 1}` }}</h4>
                <p v-if="step.text" class="step-text">{{ step.text }}</p>

                <div v-if="step.image" class="step-image">
                  <img :src="getManualImageUrl(step.image)" :alt="step.title || 'Шаг'" loading="lazy" />
                </div>

                <div v-if="step.result" class="step-result">
                  <i class="fa fa-check-circle"></i>
                  <span>{{ step.result }}</span>
                </div>

                <div v-if="step.warning" class="step-tip warning">
                  <i class="fa fa-exclamation-triangle"></i>
                  <span>{{ step.warning }}</span>
                </div>

                <div v-if="step.tip" class="step-tip info">
                  <i class="fa fa-lightbulb"></i>
                  <span>{{ step.tip }}</span>
                </div>
              </div>
            </div>
          </div>

          <div v-if="manual.tip" class="manual-tip">
            <i class="fa fa-lightbulb-o"></i>
            <div>
              <strong>Совет:</strong>
              <span>{{ manual.tip }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- ПОСЛЕ ЗАВЕРШЕНИЯ -->
      <div v-if="manual.aftercare" class="block block-aftercare">
        <h4 class="block-title">
          <i class="fa fa-check-circle"></i> После завершения
        </h4>

        <div class="aftercare-content">
          <i class="fa fa-info-circle"></i>
          <span>{{ manual.aftercare }}</span>
        </div>
      </div>

      <!-- САЙДБАР -->
      <div class="manual-sidebar">
        <div class="sidebar-card">
          <h4><i class="fa fa-wrench"></i> Инструменты</h4>
          <ul v-if="instrumentsList.length" class="items-list">
            <li v-for="item in instrumentsList" :key="item">
              <i class="fa fa-check-circle"></i> {{ item }}
            </li>
          </ul>
          <p v-else class="empty-text">Не указаны</p>
        </div>

        <div class="sidebar-card">
          <h4><i class="fa fa-cogs"></i> Материалы</h4>
          <ul v-if="partsList.length" class="items-list">
            <li v-for="item in partsList" :key="item">
              <i class="fa fa-check-circle"></i> {{ item }}
            </li>
          </ul>
          <p v-else class="empty-text">Не указаны</p>
        </div>

        <div class="sidebar-card complete-card">
          <h4><i class="fa fa-flag-checkered"></i> Завершить обслуживание</h4>
          <p class="complete-text">После завершения вы сможете:</p>
          <ul class="complete-benefits">
            <li><i class="fa fa-check"></i> Записать в историю</li>
            <li><i class="fa fa-check"></i> Создать следующее ТО</li>
          </ul>
          <BaseButton variant="success" icon="fa fa-check" block @click="openCompleteModal">
            Завершить обслуживание
          </BaseButton>
        </div>
      </div>
    </div>

    <!-- ПУСТОЕ СОСТОЯНИЕ -->
    <div v-else-if="!selectedMotoId || !selectedMaintenanceId" class="empty-state-wrapper">
      <BaseEmptyState
        icon="fa fa-motorcycle"
        title="Выберите данные для начала"
        description="Выберите мотоцикл и необходимое обслуживание, чтобы получить инструкцию"
      />
    </div>

    <!-- МАНУАЛ НЕ НАЙДЕН -->
    <div v-else-if="selectedMotoId && selectedMaintenanceId && !manual" class="empty-state-wrapper">
      <BaseEmptyState
        icon="fa fa-file-text"
        variant="warning"
        title="Мануал не найден"
        description="К сожалению, мы не нашли подходящий мануал в базе. Вы можете создать его сами."
      >
        <BaseButton variant="primary" @click="openCreateManual">
          Создать мануал
        </BaseButton>
        <BaseButton variant="secondary" @click="openCompleteModal">
          Завершить обслуживание
        </BaseButton>
      </BaseEmptyState>
    </div>

    <!-- МОДАЛ ЗАВЕРШЕНИЯ -->
    <MarkPlanMaintenanceModal
      :is-open="showCompleteModal"
      :motorcycle="selectedMotoData"
      :maintenance="selectedMaintenanceData"
      @close="showCompleteModal = false"
      @submit="handleComplete"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useMotorcyclesStore, useMaintenancesStore, useManualsStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import {
  formatMileage,
  getCategoryLabel,
  getDifficultyLabel,
  getFluidLabel,
  getToleranceLabel,
} from '@/utils/formatters'
import { getManualImageUrl } from '@/utils/mediaUrl'

import { BaseButton, BaseSelect, BaseEmptyState } from '@/components/ui'
import MarkPlanMaintenanceModal from '../components/modals/maintenance/MarkPlanMaintenanceModal.vue'
import Header from '../components/Header.vue'
import LoadingOverlay from '../components/LoadingOverlay.vue'

const router = useRouter()
const toast = useToast()

const motorcyclesStore = useMotorcyclesStore()
const maintenancesStore = useMaintenancesStore()
const manualsStore = useManualsStore()

const { items: motorcycles } = storeToRefs(motorcyclesStore)
const { loading } = storeToRefs(maintenancesStore)

// ===== Local state =====
const selectedMotoId = ref(null)
const selectedMaintenanceId = ref(null)
const manual = ref(null)
const allMaintenances = ref([])
const loadingManual = ref(false)
const showCompleteModal = ref(false)

// ===== Computed =====
const selectedMotoData = computed(() => {
  if (!selectedMotoId.value) return null
  return motorcycles.value.find((m) => m.id === selectedMotoId.value) || null
})

const availableMaintenances = computed(() => {
  if (!selectedMotoId.value) return []
  return allMaintenances.value.filter(
    (m) => m.moto_id === selectedMotoId.value && (m.status === 'planned' || m.status === 'overdue')
  )
})

const selectedMaintenanceData = computed(() => {
  if (!selectedMaintenanceId.value) return null
  return allMaintenances.value.find((m) => m.id === selectedMaintenanceId.value) || null
})

const manualSteps = computed(() => {
  if (!manual.value?.steps) return []
  return [...manual.value.steps].sort((a, b) => (a.order || 0) - (b.order || 0))
})

const instrumentsList = computed(() => {
  if (!manual.value?.instruments) return []
  if (typeof manual.value.instruments === 'string') {
    return manual.value.instruments.split(/[,;]\s*/).filter((s) => s.trim())
  }
  if (Array.isArray(manual.value.instruments)) return manual.value.instruments
  return []
})

const partsList = computed(() => {
  if (!manual.value?.parts) return []
  if (typeof manual.value.parts === 'string') {
    return manual.value.parts.split(/[,;]\s*/).filter((s) => s.trim())
  }
  if (Array.isArray(manual.value.parts)) return manual.value.parts
  return []
})

const maintenanceStatusClass = computed(() => {
  if (!selectedMaintenanceData.value) return ''
  if (selectedMaintenanceData.value.status === 'overdue') return 'status-overdue'
  if (selectedMaintenanceData.value.status === 'planned') return 'status-planned'
  return ''
})

const maintenanceStatusIcon = computed(() => {
  if (!selectedMaintenanceData.value) return ''
  if (selectedMaintenanceData.value.status === 'overdue') return 'fa fa-exclamation-circle'
  if (selectedMaintenanceData.value.status === 'planned') return 'fa fa-clock-o'
  return 'fa fa-circle'
})

const maintenanceStatusText = computed(() => {
  if (!selectedMaintenanceData.value) return ''
  if (selectedMaintenanceData.value.status === 'overdue') return 'Просрочено'
  if (selectedMaintenanceData.value.status === 'planned') return 'Запланировано'
  return selectedMaintenanceData.value.status
})

const resultIcon = computed(() => {
  if (manual.value) return 'fa fa-check-circle'
  if (selectedMotoId.value && selectedMaintenanceId.value) return 'fa fa-search'
  return 'fa fa-hourglass-half'
})

// ===== Lifecycle =====
onMounted(async () => {
  try {
    const promises = []
    if (!motorcycles.value.length) {
      promises.push(motorcyclesStore.loadAll())
    }
    promises.push(loadRepairData())
    await Promise.all(promises)
  } catch (err) {
    console.error('Failed to load repair data:', err)
    toast.error('Не удалось загрузить данные')
  }
})

async function loadRepairData() {
  const data = await maintenancesStore.loadForRepair()
  allMaintenances.value = data.maintenances
}

// ===== Watchers =====
watch(selectedMotoId, () => {
  selectedMaintenanceId.value = null
  manual.value = null
})

watch(selectedMaintenanceId, async (newVal) => {
  manual.value = null
  if (!newVal || !selectedMotoId.value) return

  loadingManual.value = true
  try {
    manual.value = await manualsStore.loadForMaintenance(newVal, selectedMotoId.value)
  } catch (err) {
    console.error('Failed to fetch manual:', err)
    manual.value = null
  } finally {
    loadingManual.value = false
  }
})

// ===== Actions =====
function scrollToManual() {
  const el = document.getElementById('manual-section')
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function openCreateManual() {
  router.push('/manual-creator')
}

function openCompleteModal() {
  if (!selectedMaintenanceData.value) {
    toast.warning('Выберите обслуживание')
    return
  }
  showCompleteModal.value = true
}

async function handleComplete(formData) {
  try {
    const { useMaintenancesStore: useStore } = await import('@/stores')
    await useStore().complete(formData.id, {
      completed_mileage: formData.mileage,
      completed_date: formData.date,
      cost: formData.cost,
      is_repeat: formData.isRepeat,
      interval: formData.interval,
    })

    showCompleteModal.value = false
    toast.success('Обслуживание успешно завершено!')

    await loadRepairData()

    selectedMaintenanceId.value = null
    manual.value = null
  } catch (err) {
    console.error('Failed to complete maintenance:', err)
    toast.error(err.response?.data?.error || 'Ошибка при завершении обслуживания')
  }
}

// ===== Helpers =====
function hasSpecs(specs) {
  if (!specs) return false
  return !!(
    (specs.torque && specs.torque.length > 0) ||
    (specs.fluids && Object.keys(specs.fluids).length > 0) ||
    (specs.tolerances && Object.keys(specs.tolerances).length > 0)
  )
}
</script>

<style scoped>
/* === Стили сохранены без изменений === */

.repair-page {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px 40px;
}

/* ===== SELECTION ===== */
.selection-section {
  margin-bottom: 32px;
}

.selection-flow {
  display: grid;
  grid-template-columns: 1fr 1fr 1.2fr;
  gap: 16px;
  background: var(--bg-secondary);
  border-radius: 16px;
  border: 1px solid var(--border-light);
  padding: 24px;
}

.selection-step {
  display: flex;
  gap: 16px;
}

.selection-step.disabled {
  opacity: 0.5;
  pointer-events: none;
}

.selection-step.result-step.found {
  border-left: 3px solid var(--success);
  padding-left: 16px;
}

.selection-step.result-step.notfound {
  border-left: 3px solid var(--warning);
  padding-left: 16px;
}

.step-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
  padding-top: 4px;
}

.step-number {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--accent);
  color: #fff;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
  min-width: 0;
}

.moto-info,
.maintenance-info {
  margin-top: 8px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.moto-mileage,
.moto-year {
  font-size: 13px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 4px;
}

.info-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 2px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.status-overdue {
  background: var(--danger-trans);
  color: var(--danger-text);
}

.status-planned {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.info-mileage {
  font-size: 13px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 4px;
}

.result-status {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}

.result-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.result-icon.success {
  background: var(--success-trans);
  color: var(--success-text);
}

.result-icon.empty {
  background: var(--warning-trans);
  color: var(--warning-text);
}

.result-icon.waiting {
  background: rgba(100, 116, 139, 0.15);
  color: var(--text-muted);
}

.result-text h4 {
  margin: 0 0 4px 0;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
}

.result-text p {
  margin: 0;
  font-size: 13px;
  color: var(--text-muted);
}

.result-actions {
  display: flex;
  gap: 8px;
}

.result-actions > * {
  width: 100%;
}

/* ===== MANUAL ===== */
.manual-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.manual-header-card {
  background: var(--bg-secondary);
  border-radius: 16px;
  border: 1px solid var(--border-light);
  padding: 24px;
}

.manual-title {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
}

.manual-description {
  margin: 0 0 12px 0;
  font-size: 15px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.manual-meta-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 12px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  font-size: 12px;
  color: var(--text-secondary);
}

.tag i {
  font-size: 12px;
  color: var(--accent-text);
}

/* ===== BLOCKS ===== */
.block {
  background: var(--bg-secondary);
  border-radius: 16px;
  border: 1px solid var(--border-light);
  padding: 20px 24px;
}

.block-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 12px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.block-title i {
  color: var(--accent-text);
}

/* Safety */
.safety-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 8px;
  margin-bottom: 8px;
  font-size: 14px;
  line-height: 1.5;
}

.safety-item:last-child { margin-bottom: 0; }
.safety-item i { font-size: 16px; margin-top: 1px; flex-shrink: 0; }

.safety-tip { background: var(--warning-trans); border-left: 3px solid var(--warning); }
.safety-tip i { color: var(--warning); }
.safety-warning { background: var(--danger-trans); border-left: 3px solid var(--danger); }
.safety-warning i { color: var(--danger); }
.safety-condition { background: var(--success-trans); border-left: 3px solid var(--success); }
.safety-condition i { color: var(--success); }

/* Docs */
.docs-list { display: flex; flex-direction: column; gap: 8px; }

.docs-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  color: var(--accent-text);
  text-decoration: none;
  transition: all 0.2s;
}

.docs-link:hover {
  border-color: var(--accent);
  background: var(--accent-trans);
  transform: translateX(4px);
}

.docs-link i:first-child { font-size: 20px; color: var(--danger); }
.docs-link span { flex: 1; font-size: 14px; }
.docs-link i:last-child { font-size: 14px; color: var(--text-muted); }

/* Specs */
.specs-section { margin-top: 12px; }
.specs-section:first-child { margin-top: 0; }
.specs-subtitle { font-size: 13px; font-weight: 600; color: var(--text-secondary); margin: 0 0 8px 0; }

.torque-table {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border-light);
  border-radius: 8px;
  overflow: hidden;
}

.torque-header,
.torque-row {
  display: grid;
  grid-template-columns: 2fr 1fr 2fr;
  padding: 8px 14px;
  font-size: 13px;
}

.torque-header {
  background: var(--bg-primary);
  font-weight: 600;
  font-size: 12px;
  text-transform: uppercase;
  color: var(--text-muted);
  letter-spacing: 0.5px;
}

.torque-row {
  border-top: 1px solid var(--border-light);
  font-size: 14px;
  color: var(--text-primary);
}

.torque-row:nth-child(even) { background: var(--bg-primary); }

.fluids-grid,
.tolerances-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 8px;
}

.fluid-item,
.tolerance-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 14px;
  background: var(--bg-primary);
  border-radius: 8px;
  border: 1px solid var(--border-light);
}

.fluid-label,
.tolerance-label { font-size: 13px; color: var(--text-secondary); }
.fluid-value,
.tolerance-value { font-weight: 600; font-size: 14px; color: var(--text-primary); }

/* Steps */
.manual-content {
  background: var(--bg-secondary);
  border-radius: 16px;
  border: 1px solid var(--border-light);
  padding: 24px;
}

.steps-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 16px 0;
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
}

.steps-count {
  font-size: 13px;
  font-weight: 400;
  color: var(--text-muted);
  margin-left: auto;
}

.steps-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.step-item {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: var(--bg-primary);
  border-radius: 12px;
  border: 1px solid var(--border-light);
  transition: all 0.25s ease;
}

.step-item:hover { border-color: var(--accent); }

.step-marker { display: flex; flex-direction: column; align-items: center; flex-shrink: 0; }

.step-connector {
  width: 2px;
  flex: 1;
  min-height: 20px;
  background: var(--border-light);
  margin: 4px 0;
}

.step-item:last-child .step-connector { display: none; }

.step-body { flex: 1; min-width: 0; }
.step-title { margin: 0 0 4px 0; font-size: 15px; font-weight: 600; color: var(--text-primary); }
.step-text { margin: 0 0 8px 0; font-size: 14px; color: var(--text-secondary); line-height: 1.6; }

.step-image { margin-top: 8px; border-radius: 8px; overflow: hidden; }
.step-image img { width: 100%; max-height: 200px; object-fit: cover; border-radius: 8px; }

.step-result,
.step-tip {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 8px;
  margin-top: 8px;
  font-size: 13px;
}

.step-result { background: var(--success-trans); color: var(--success-text); }
.step-result i { color: var(--success); margin-top: 2px; }
.step-tip.info { background: rgba(59, 130, 246, 0.1); color: #3b82f6; }
.step-tip.warning { background: var(--warning-trans); color: var(--warning-text); }
.step-tip i { margin-top: 2px; }

.manual-tip {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: var(--warning-trans);
  border-radius: 12px;
  border: 1px solid rgba(245, 158, 11, 0.15);
  margin-top: 20px;
}

.manual-tip i { color: var(--warning-text); font-size: 20px; flex-shrink: 0; margin-top: 2px; }
.manual-tip div { font-size: 14px; color: var(--text-secondary); line-height: 1.6; }
.manual-tip strong { color: var(--text-primary); }

/* Aftercare */
.aftercare-content {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 16px;
  background: var(--bg-primary);
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-secondary);
}

.aftercare-content i { font-size: 18px; color: var(--accent-text); margin-top: 1px; flex-shrink: 0; }

/* Sidebar */
.manual-sidebar {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 16px;
}

.sidebar-card {
  background: var(--bg-secondary);
  border-radius: 16px;
  border: 1px solid var(--border-light);
  padding: 20px;
}

.sidebar-card h4 {
  margin: 0 0 12px 0;
  font-size: 15px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-primary);
}

.sidebar-card h4 i { color: var(--accent-text); }

.items-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.items-list li { display: flex; align-items: center; gap: 8px; font-size: 14px; color: var(--text-secondary); }
.items-list li i { color: var(--success-text); font-size: 14px; }

.empty-text { font-size: 14px; color: var(--text-muted); font-style: italic; margin: 0; }

.complete-card { background: var(--success-trans); border-color: rgba(16, 185, 129, 0.2); }
.complete-card h4 { color: var(--success-text); }
.complete-text { font-size: 13px; color: var(--text-secondary); margin: 0 0 8px 0; }

.complete-benefits {
  list-style: none;
  padding: 0;
  margin: 0 0 16px 0;
}

.complete-benefits li {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-secondary);
  padding: 4px 0;
}

.complete-benefits li i { color: var(--success-text); }

/* Empty states */
.empty-state-wrapper { margin-top: 8px; }

/* ===== RESPONSIVE ===== */
@media (max-width: 992px) {
  .selection-flow { grid-template-columns: 1fr; gap: 20px; }
  .selection-step.result-step {
    border-left: none;
    padding-left: 0;
    border-top: 1px solid var(--border-light);
    padding-top: 20px;
  }
  .step-connector { display: none !important; }
}

@media (max-width: 768px) {
  .repair-page { padding: 0 12px 32px; }
  .manual-sidebar { grid-template-columns: 1fr; }
  .manual-content { padding: 16px; }
  .manual-header-card { padding: 16px; }
  .manual-title { font-size: 20px; }
  .step-item { flex-direction: column; gap: 12px; }
  .step-marker { flex-direction: row; gap: 8px; }
  .step-connector { display: none !important; }
  .result-status { flex-direction: column; align-items: center; text-align: center; }
  .result-actions { flex-direction: column; }
  .selection-flow { padding: 16px; }
  .torque-header,
  .torque-row { grid-template-columns: 1fr 1fr 1fr; font-size: 12px; }
  .fluids-grid,
  .tolerances-grid { grid-template-columns: 1fr; }
}

@media (max-width: 480px) {
  .manual-meta-tags { flex-direction: column; align-items: flex-start; }
  .steps-title { flex-wrap: wrap; }
  .steps-count { margin-left: 0; width: 100%; }
  .block { padding: 14px 16px; }
  .selection-step { flex-direction: column; gap: 8px; }
  .step-indicator { flex-direction: row; gap: 8px; }
}
</style>
