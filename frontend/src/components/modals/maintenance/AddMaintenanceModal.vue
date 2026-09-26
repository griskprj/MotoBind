<template>
  <BaseModal
    :is-open="isOpen"
    :title="currentStepTitle"
    :subtitle="currentStepSubtitle"
    :icon="currentStepIcon"
    :variant="currentStepVariant"
    size="md"
    @close="closeModal"
  >
    <!-- Шаг 1: Выбор типа -->
    <template v-if="currentStep === 1">
      <div
        class="choice-card"
        :class="{ selected: selectedType === 'history' }"
        @click="selectType('history')"
      >
        <div class="choice-icon success">
          <i class="fa fa-clock"></i>
        </div>
        <div class="choice-info">
          <div class="choice-title">Добавить в историю</div>
          <div class="choice-subtitle">Уже выполненное обслуживание</div>
        </div>
        <div class="choice-arrow">
          <i class="fa fa-chevron-right"></i>
        </div>
      </div>

      <div
        class="choice-card"
        :class="{ selected: selectedType === 'planned' }"
        @click="selectType('planned')"
      >
        <div class="choice-icon warning">
          <i class="fa fa-calendar"></i>
        </div>
        <div class="choice-info">
          <div class="choice-title">Запланировать</div>
          <div class="choice-subtitle">Плановое обслуживание</div>
        </div>
        <div class="choice-arrow">
          <i class="fa fa-chevron-right"></i>
        </div>
      </div>

      <div class="modal-info-block info">
        <div class="modal-info-icon">
          <i class="fa fa-info-circle"></i>
        </div>
        <p class="modal-info-text">
          Выберите тип обслуживания, которое хотите добавить
        </p>
      </div>
    </template>

    <!-- Шаг 2: Форма -->
    <template v-if="currentStep === 2">
      <div class="form-stack">
        <BaseSelect
          v-model="form.motorcycleId"
          label="Мотоцикл"
          placeholder="Выберите мотоцикл"
          required
        >
          <option
            v-for="moto in motorcycles"
            :key="moto.id"
            :value="moto.id"
          >
            {{ moto.name }} ({{ moto.mileage || 0 }} км)
          </option>
        </BaseSelect>

        <BaseSelect
          v-model="form.category"
          label="Узел / Система"
          placeholder="Выберите категорию"
          required
          @change="onCategoryChange"
        >
          <option value="engine">Двигатель</option>
          <option value="drive">Привод</option>
          <option value="steering">Рулевое управление</option>
          <option value="suspension">Подвеска</option>
          <option value="electronics">Электроника</option>
          <option value="wheel">Колёса / Шины</option>
          <option value="brakes">Тормозная система</option>
          <option value="fuel">Топливная система</option>
          <option value="cooling">Система охлаждения</option>
        </BaseSelect>

        <BaseSelect
          v-if="templates.length > 0"
          v-model="form.templateId"
          label="Тип обслуживания"
          placeholder="Выберите тип обслуживания"
          required
          @change="onTemplateChange"
        >
          <option v-for="tpl in templates" :key="tpl.id" :value="tpl.id">
            {{ tpl.label }}
          </option>
        </BaseSelect>

        <BaseInput
          v-if="!form.category || templates.length === 0"
          v-model="form.title"
          label="Название обслуживания"
          placeholder="Например: Замена масла"
          required
        />

        <BaseTextarea
          v-model="form.description"
          label="Описание работы"
          :placeholder="selectedType === 'history'
            ? 'Опишите, что было сделано...'
            : 'Опишите, что необходимо сделать...'"
          :rows="2"
        />

        <hr class="form-divider" />

        <template v-if="selectedType === 'history'">
          <BaseInput
            v-model.number="form.mileage"
            type="number"
            label="Пробег (км)"
            placeholder="0"
            :min="0"
            required
          />

          <div class="form-row">
            <BaseInput
              v-model.number="form.cost"
              type="number"
              label="Стоимость (₽)"
              placeholder="0"
              :min="0"
            />
            <BaseInput
              v-model="form.date"
              type="date"
              label="Дата выполнения"
              :max="currentDate"
            />
          </div>

          <div class="modal-info-block success">
            <div class="modal-info-icon">
              <i class="fa fa-check-circle"></i>
            </div>
            <p class="modal-info-text">
              Обслуживание будет добавлено в историю с указанными данными
            </p>
          </div>
        </template>

        <template v-if="selectedType === 'planned'">
          <div class="modal-info-block info">
            <div class="modal-info-icon">
              <i class="fa fa-info-circle"></i>
            </div>
            <p class="modal-info-text">
              Вы можете запланировать обслуживание по <strong>пробегу</strong>
              или по <strong>дате</strong>. Заполните хотя бы одно поле.
            </p>
          </div>

          <BaseInput
            v-model.number="form.planned_mileage"
            type="number"
            label="Плановый пробег (км)"
            placeholder="Например: 15000"
            :min="0"
          />

          <div class="or-divider"><span>или</span></div>

          <BaseInput
            v-model="form.planned_date"
            type="date"
            label="Плановая дата"
            :min="today"
          />

          <div class="modal-info-block info">
            <div class="modal-info-icon">
              <i class="fa fa-bell"></i>
            </div>
            <p class="modal-info-text">
              Вы получите уведомление, когда наступит указанная дата или мотоцикл достигнет указанного пробега.
            </p>
          </div>
        </template>
      </div>
    </template>

    <!-- Шаг 3: Успех -->
    <template v-if="currentStep === 3">
      <div class="completion-step">
        <div class="completion-icon">
          <i class="fa fa-check-circle"></i>
        </div>
        <h2 class="step-title">Готово!</h2>
        <p class="step-subtitle">
          {{ selectedType === 'history'
            ? 'Обслуживание добавлено в историю'
            : 'Обслуживание запланировано'
          }}
        </p>

        <div class="summary-card">
          <div class="summary-item">
            <span class="summary-label">Мотоцикл</span>
            <span class="summary-value">{{ getMotoName(form.motorcycleId) }}</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">Обслуживание</span>
            <span class="summary-value">{{ form.title || '—' }}</span>
          </div>
          <div v-if="form.description" class="summary-item">
            <span class="summary-label">Описание</span>
            <span class="summary-value">{{ form.description }}</span>
          </div>
          <div v-if="selectedType === 'history' && form.mileage" class="summary-item">
            <span class="summary-label">Пробег</span>
            <span class="summary-value">{{ form.mileage }} км</span>
          </div>
          <div v-if="selectedType === 'history' && form.cost" class="summary-item">
            <span class="summary-label">Стоимость</span>
            <span class="summary-value">{{ form.cost }} ₽</span>
          </div>
          <div v-if="selectedType === 'planned' && form.planned_mileage" class="summary-item">
            <span class="summary-label">Плановый пробег</span>
            <span class="summary-value">{{ form.planned_mileage }} км</span>
          </div>
          <div v-if="selectedType === 'planned' && form.planned_date" class="summary-item">
            <span class="summary-label">Плановая дата</span>
            <span class="summary-value">{{ formatDate(form.planned_date) }}</span>
          </div>
        </div>
      </div>
    </template>

    <template #actions>
      <BaseButton
        v-if="currentStep === 2"
        variant="secondary"
        icon="fa fa-arrow-left"
        block
        @click="prevStep"
      >
        Назад
      </BaseButton>

      <BaseButton
        v-if="currentStep === 1"
        variant="secondary"
        block
        @click="closeModal"
      >
        Отменить
      </BaseButton>

      <BaseButton
        v-if="currentStep === 1"
        variant="primary"
        block
        :disabled="!selectedType"
        @click="nextStep"
      >
        Продолжить <i class="fa fa-arrow-right"></i>
      </BaseButton>

      <BaseButton
        v-if="currentStep === 2"
        variant="primary"
        icon="fa fa-save"
        block
        :disabled="!isFormValid"
        :loading="loading"
        @click="submit"
      >
        Сохранить
      </BaseButton>

      <BaseButton
        v-if="currentStep === 3"
        variant="success"
        icon="fa fa-check"
        block
        @click="closeModal"
      >
        Закрыть
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import {
  BaseModal,
  BaseButton,
  BaseInput,
  BaseSelect,
  BaseTextarea,
} from '@/components/ui'
import { useToast } from '@/composables/useToast'
import { useMaintenancesStore } from '@/stores'
import { getTemplatesByCategory } from '@/constants/maintenanceTemplates'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  motorcycles: { type: Array, default: () => [] },
})

const emit = defineEmits(['close', 'created'])
const toast = useToast()
const maintenancesStore = useMaintenancesStore()

const currentStep = ref(1)
const selectedType = ref(null)
const templates = ref([])
const loading = ref(false)

const form = reactive({
  motorcycleId: null,
  category: '',
  templateId: '',
  title: '',
  description: '',
  cost: null,
  mileage: null,
  date: null,
  planned_mileage: null,
  planned_date: null,
})

const currentDate = new Date().toISOString().split('T')[0]

const today = computed(() => new Date().toISOString().split('T')[0])

const currentStepTitle = computed(() => {
  return {
    1: 'Добавить обслуживание',
    2: selectedType.value === 'history' ? 'Добавить в историю' : 'Запланировать обслуживание',
    3: 'Готово!',
  }[currentStep.value] || 'Добавить обслуживание'
})

const currentStepSubtitle = computed(() => {
  return {
    1: 'Выберите, что хотите сделать',
    2: selectedType.value === 'history'
      ? 'Заполните информацию о выполненной работе'
      : 'Заполните информацию о плановом обслуживании',
    3: '',
  }[currentStep.value] || ''
})

const currentStepIcon = computed(() => {
  return {
    1: 'wrench',
    2: selectedType.value === 'history' ? 'clipboard-list' : 'calendar-plus',
    3: 'check-circle',
  }[currentStep.value] || 'wrench'
})

const currentStepVariant = computed(() => {
  if (currentStep.value === 3) return 'success'
  if (currentStep.value === 2 && selectedType.value === 'history') return 'success'
  if (currentStep.value === 2 && selectedType.value === 'planned') return 'warning'
  return 'default'
})

const isFormValid = computed(() => {
  const baseValid = form.motorcycleId && form.category && form.title

  if (selectedType.value === 'history') {
    return baseValid && form.mileage && form.mileage > 0
  }

  if (selectedType.value === 'planned') {
    const hasPlanned =
      (form.planned_mileage && form.planned_mileage > 0) || form.planned_date
    return baseValid && hasPlanned
  }

  return false
})

watch(
  () => props.isOpen,
  (newVal) => {
    if (newVal) resetForm()
  }
)

function formatDate(dateString) {
  if (!dateString) return '—'
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) return '—'
    return date.toLocaleDateString('ru-RU', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    })
  } catch {
    return '—'
  }
}

function getMotoName(id) {
  const moto = props.motorcycles.find((m) => m.id === id)
  return moto ? moto.name : '—'
}

function selectType(type) {
  selectedType.value = type
}

function onCategoryChange() {
  form.templateId = ''
  form.title = ''
  templates.value = form.category ? getTemplatesByCategory(form.category) : []
}

function onTemplateChange() {
  const found = templates.value.find((t) => t.id === form.templateId)
  form.title = found ? found.label : ''
}

function nextStep() {
  if (currentStep.value < 3) currentStep.value++
}

function prevStep() {
  if (currentStep.value > 1) currentStep.value--
}

function closeModal() {
  emit('close')
}

function resetForm() {
  currentStep.value = 1
  selectedType.value = null
  form.motorcycleId = null
  form.category = ''
  form.templateId = ''
  form.title = ''
  form.description = ''
  form.cost = null
  form.mileage = null
  form.date = null
  form.planned_mileage = null
  form.planned_date = null
  templates.value = []
  loading.value = false
}

async function submit() {
  loading.value = true
  try {
    let payload = {
      motorcycleId: form.motorcycleId,
      title: form.title,
      category: form.category,
      description: form.description || '',
    }

    if (selectedType.value === 'history') {
      payload = {
        ...payload,
        cost: form.cost || null,
        completed_mileage: form.mileage,
        completed_date: form.date || null,
      }
    } else {
      payload = {
        ...payload,
        planned_mileage: form.planned_mileage || null,
        planned_date: form.planned_date || null,
      }
    }

    await maintenancesStore.create(payload)
    emit('created')
    nextStep()
  } catch (err) {
    console.error('Failed to create maintenance:', err)
    toast.error(err.response?.data?.error || 'Ошибка при сохранении')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* ===== КАРТОЧКИ ВЫБОРА ===== */
.choice-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: var(--bg-secondary);
  border: 2px solid transparent;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 12px;
}

.choice-card:hover {
  background: var(--bg-card-hover);
  transform: translateY(-2px);
}

.choice-card.selected {
  border-color: var(--accent);
  background: var(--accent-trans);
  box-shadow: 0 0 0 2px var(--accent-trans);
}

.choice-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.choice-icon.success {
  background: var(--success-trans);
  color: var(--success-text);
}

.choice-icon.warning {
  background: var(--warning-trans);
  color: var(--warning-text);
}

.choice-info { flex: 1; }

.choice-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.choice-subtitle {
  font-size: 13px;
  color: var(--text-secondary);
}

.choice-arrow {
  color: var(--text-muted);
  font-size: 16px;
}

/* ===== ФОРМА ===== */
.form-stack {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.form-divider {
  border: none;
  border-top: 1px solid var(--border-light);
  margin: 4px 0;
}

.or-divider {
  display: flex;
  align-items: center;
  gap: 16px;
  color: var(--text-muted);
}

.or-divider::before,
.or-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border-color);
}

.or-divider span {
  font-size: 13px;
  font-weight: 500;
}

/* ===== ИНФО-БЛОКИ ===== */
.modal-info-block {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 10px;
}

.modal-info-block.info {
  background: var(--accent-trans);
  border: 1px solid var(--accent-light);
}

.modal-info-block.success {
  background: var(--success-trans);
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.modal-info-icon {
  font-size: 18px;
  flex-shrink: 0;
  margin-top: 2px;
}

.modal-info-block.info .modal-info-icon { color: var(--accent-text); }
.modal-info-block.success .modal-info-icon { color: var(--success-text); }

.modal-info-text {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
}

/* ===== ФИНАЛЬНЫЙ ШАГ ===== */
.completion-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 16px 4px;
  text-align: center;
}

.completion-icon {
  font-size: 56px;
  color: var(--success-text);
  margin-bottom: 12px;
}

.completion-step .step-title {
  font-size: 22px;
  font-weight: 700;
  margin: 0 0 4px 0;
  color: var(--text-primary);
}

.completion-step .step-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0 0 16px 0;
}

.summary-card {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 16px;
  width: 100%;
  border: 1px solid var(--border-light);
}

.summary-item {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px solid var(--border-light);
}

.summary-item:last-child { border-bottom: none; }

.summary-label {
  font-size: 13px;
  color: var(--text-muted);
}

.summary-value {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  text-align: right;
  max-width: 60%;
  word-break: break-word;
}

@media (max-width: 640px) {
  .choice-card { padding: 14px 16px; }
  .choice-icon { width: 38px; height: 38px; font-size: 16px; }
  .form-row { grid-template-columns: 1fr; gap: 14px; }

  .summary-item {
    flex-direction: column;
    align-items: center;
    gap: 2px;
    text-align: center;
  }

  .summary-value { max-width: 100%; text-align: center; }
  .completion-icon { font-size: 44px; }
  .completion-step .step-title { font-size: 20px; }

  .modal-info-block {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  .modal-info-icon { margin-top: 0; }
}
</style>
