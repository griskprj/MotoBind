<template>
  <BaseModal
    :is-open="isOpen"
    title="Завершить обслуживание"
    subtitle="Подтвердите завершение обслуживания"
    icon="check"
    variant="success"
    size="md"
    @close="$emit('close')"
  >
    <!-- Инфо-карточка -->
    <div class="info-card">
      <div class="info-card-row">
        <span class="info-label">Мотоцикл</span>
        <span class="info-value">{{ motorcycle?.name || '—' }}</span>
      </div>
      <div class="info-card-row">
        <span class="info-label">Обслуживание</span>
        <span class="info-value">
          <span class="maintenance-tag">
            <i class="fa fa-wrench"></i>
            {{ maintenance?.title || '—' }}
          </span>
        </span>
      </div>
      <div v-if="maintenance?.planned_mileage" class="info-card-row">
        <span class="info-label">Плановый пробег</span>
        <span class="info-value">
          <span class="planned-badge">
            <i class="fa fa-clock"></i>
            {{ maintenance.planned_mileage }} км
          </span>
        </span>
      </div>
      <div v-if="maintenance?.planned_date" class="info-card-row">
        <span class="info-label">Плановая дата</span>
        <span class="info-value">
          <span class="planned-badge">
            <i class="fa fa-calendar"></i>
            {{ formatDate(maintenance.planned_date) }}
          </span>
        </span>
      </div>
    </div>

    <!-- Форма -->
    <div class="form-stack">
      <BaseInput
        v-model.number="form.mileage"
        type="number"
        label="Пробег выполнения"
        placeholder="Введите пробег"
        :min="0"
        :max="1000000"
        required
      />

      <div class="form-row">
        <BaseInput
          v-model="form.date"
          type="date"
          label="Дата выполнения"
          :max="today"
        />
        <BaseInput
          v-model.number="form.cost"
          type="number"
          label="Стоимость (₽)"
          placeholder="0"
          :min="0"
        />
      </div>

      <label class="checkbox-group">
        <input v-model="form.isRepeat" type="checkbox" />
        <span>Запланировать следующее обслуживание</span>
      </label>

      <template v-if="form.isRepeat">
        <div class="modal-info-block info">
          <div class="modal-info-icon">
            <i class="fa fa-info-circle"></i>
          </div>
          <p class="modal-info-text">
            Вы можете запланировать следующее обслуживание по <strong>пробегу</strong>
            или по <strong>дате</strong>. Заполните только одно поле.
          </p>
        </div>

        <BaseInput
          v-model.number="form.interval"
          type="number"
          label="Интервал (км)"
          placeholder="Например: 5000"
          :min="1"
          :max="100000"
        />

        <div class="or-divider"><span>или</span></div>

        <BaseInput
          v-model.number="form.interval_days"
          type="number"
          label="Интервал (дни)"
          placeholder="Например: 365 (1 год)"
          :min="1"
          :max="1095"
        />

        <div v-if="form.interval && form.interval_days" class="modal-info-block warning">
          <div class="modal-info-icon">
            <i class="fa fa-exclamation-triangle"></i>
          </div>
          <p class="modal-info-text">
            Укажите только один тип интервала: пробег или дни.
          </p>
        </div>
      </template>
    </div>

    <div class="modal-info-block warning">
      <div class="modal-info-icon">
        <i class="fa fa-exclamation-triangle"></i>
      </div>
      <div>
        <p class="modal-info-text modal-info-text--strong-warning">
          Это действие нельзя отменить!
        </p>
        <p class="modal-info-text">
          Запись будет добавлена в историю обслуживания. Вы всегда сможете её просмотреть.
        </p>
      </div>
    </div>

    <template #actions>
      <BaseButton variant="secondary" block @click="$emit('close')">
        Отменить
      </BaseButton>
      <BaseButton
        variant="success"
        icon="fa fa-check"
        block
        :disabled="!isFormValid"
        @click="submit"
      >
        Завершить
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup>
import { computed, reactive, watch } from 'vue'
import { BaseModal, BaseButton, BaseInput } from '@/components/ui'
import { useToast } from '@/composables/useToast'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  motorcycle: { type: Object, default: null },
  maintenance: { type: Object, default: null },
})

const emit = defineEmits(['close', 'submit'])
const toast = useToast()

const form = reactive({
  id: null,
  moto_id: null,
  mileage: null,
  date: null,
  cost: null,
  isRepeat: false,
  interval: null,
  interval_days: null,
})

const today = computed(() => new Date().toISOString().split('T')[0])

const isFormValid = computed(() => {
  if (!form.mileage || form.mileage < 0) return false

  if (form.isRepeat) {
    const hasInterval = form.interval && form.interval > 0
    const hasDays = form.interval_days && form.interval_days > 0
    if (hasInterval && hasDays) return false
    if (!hasInterval && !hasDays) return false
  }

  return true
})

watch(
  () => props.isOpen,
  (newVal) => {
    if (newVal && props.maintenance) resetForm()
  }
)

function resetForm() {
  form.id = props.maintenance?.id || null
  form.moto_id = props.motorcycle?.id || null
  form.mileage = null
  form.date = today.value
  form.cost = null
  form.isRepeat = false
  form.interval = null
  form.interval_days = null
}

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

function submit() {
  if (!props.maintenance) {
    toast.error('Нет данных об обслуживании')
    return
  }

  emit('submit', {
    id: props.maintenance.id,
    moto_id: props.motorcycle?.id,
    mileage: form.mileage,
    date: form.date || today.value,
    cost: form.cost || 0,
    isRepeat: form.isRepeat,
    interval: form.interval,
    interval_days: form.interval_days,
  })
}
</script>

<style scoped>
.info-card {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 14px 16px;
  margin-bottom: 16px;
  border: 1px solid var(--border-light);
}

.info-card-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
  border-bottom: 1px solid var(--border-light);
}

.info-card-row:last-child { border-bottom: none; }

.info-label { font-size: 13px; color: var(--text-muted); }

.info-value {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.maintenance-tag,
.planned-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 2px 12px;
  border-radius: 12px;
  font-size: 13px;
}

.maintenance-tag {
  background: var(--accent-trans);
  color: var(--accent-text);
}

.planned-badge {
  background: var(--warning-trans);
  color: var(--warning-text);
}

.form-stack {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-bottom: 12px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
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

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  font-size: 14px;
  color: var(--text-secondary);
}

.checkbox-group input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: var(--accent);
  cursor: pointer;
  flex-shrink: 0;
}

.checkbox-group span { user-select: none; }

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

.modal-info-block.warning {
  background: var(--warning-trans);
  border: 1px solid rgba(245, 158, 11, 0.2);
}

.modal-info-icon {
  font-size: 18px;
  flex-shrink: 0;
  margin-top: 2px;
}

.modal-info-block.info .modal-info-icon { color: var(--accent-text); }
.modal-info-block.warning .modal-info-icon { color: var(--warning-text); }

.modal-info-text {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
}

.modal-info-text--strong-warning {
  font-weight: 600;
  color: var(--warning-text);
}

@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
    gap: 14px;
  }

  .info-card-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 2px;
    padding: 8px 0;
  }

  .modal-info-block {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .modal-info-icon { margin-top: 0; }
}
</style>
