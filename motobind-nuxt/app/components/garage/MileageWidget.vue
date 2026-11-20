<script setup lang="ts">
import type { ApiError } from '~/types'

const props = defineProps<{
  motorcycleId: number | string
  currentMileage: number
  lastUpdated?: string | null
}>()

const emit = defineEmits<{
  updated: []
}>()

const api = useApi()
const toast = useToast()

const isEditing = ref(false)
const inputValue = ref<number | string>(props.currentMileage)
const submitting = ref(false)

const quickSteps = [50, 100, 500, 1000]

watch(() => props.currentMileage, (val) => {
  inputValue.value = val
})

async function updateMileage(newVal: number) {
  if (newVal === props.currentMileage) {
    isEditing.value = false
    return
  }

  submitting.value = true
  try {
    await api.motorcycle.update(props.motorcycleId, { mileage: newVal })
    toast.success('Пробег обновлён')
    emit('updated')
    isEditing.value = false
  } catch (e) {
    toast.error((e as ApiError).message || 'Ошибка обновления')
  } finally {
    submitting.value = false
  }
}

function addToMileage(amount: number) {
  const current = Number(inputValue.value || 0)
  updateMileage(current + amount)
}

function onSaveExact() {
  const val = Number(inputValue.value)
  if (isNaN(val) || val < 0) {
    toast.error('Некорректный пробег')
    return
  }
  updateMileage(val)
}

function startEdit() {
  inputValue.value = props.currentMileage
  isEditing.value = true
}

// Форматирование больших чисел (24400 -> 24.4 тыс.)
const formatMileage = (val: number) => {
  if (val >= 1000) {
    return `${(val / 1000).toFixed(1).replace('.0', '')} тыс.`
  }
  return val.toString()
}

const formattedDate = computed(() => {
  if (!props.lastUpdated) return null
  return new Date(props.lastUpdated).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
})
</script>

<template>
  <BaseCard padding="md" class="mileage-widget">
    <div class="mw-header">
      <i class="fa-solid fa-gauge-high mw-icon"></i>
      <span class="mw-title">Пробег</span>
    </div>

    <div class="mw-value-block">
      <template v-if="!isEditing">
        <div class="mw-value">
          <span class="mw-number">{{ formatMileage(currentMileage) }}</span>
          <span class="mw-unit">км</span>
        </div>
        <div v-if="formattedDate" class="mw-date">
          <i class="fa-regular fa-clock"></i> Обновлен {{ formattedDate }} г.
        </div>
      </template>

      <template v-else>
        <div class="mw-edit-row">
          <BaseInput
            v-model="inputValue"
            type="number"
            placeholder="Точный пробег"
            class="mw-input"
            autofocus
            @keyup.enter="onSaveExact"
          />
          <BaseButton variant="primary" size="sm" :loading="submitting" @click="onSaveExact">
            <i class="fa-solid fa-check"></i>
          </BaseButton>
          <BaseButton variant="ghost" size="sm" @click="isEditing = false">
            <i class="fa-solid fa-xmark"></i>
          </BaseButton>
        </div>
      </template>
    </div>

    <div class="mw-actions">
      <span class="mw-hint">Быстро добавить:</span>
      <div class="mw-quick-btns">
        <BaseButton
          v-for="step in quickSteps"
          :key="step"
          variant="secondary"
          size="sm"
          :disabled="submitting"
          @click="addToMileage(step)"
        >
          +{{ step }}
        </BaseButton>
      </div>

      <BaseButton
        v-if="!isEditing"
        variant="secondary"
        block
        class="mw-exact-btn"
        @click="startEdit"
      >
        <i class="fa-solid fa-pen"></i> Ввести точное значение
      </BaseButton>
    </div>
  </BaseCard>
</template>

<style scoped lang="scss">
.mileage-widget {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  background: var(--color-surface);
}

.mw-header {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
}

.mw-icon {
  color: var(--color-brand);
  font-size: 16px;
}

.mw-value-block {
  background: var(--color-surface-secondary);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 90px;
}

.mw-value {
  display: flex;
  align-items: baseline;
  gap: var(--space-2);
}

.mw-number {
  font-size: 32px;
  font-weight: var(--fw-bold);
  color: var(--color-text);
  line-height: 1;
}

.mw-unit {
  font-size: var(--text-lg);
  font-weight: var(--fw-semibold);
  color: var(--color-text);
}

.mw-date {
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
  margin-top: var(--space-2);
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

.mw-edit-row {
  display: flex;
  gap: var(--space-2);
  align-items: center;
}

.mw-input {
  flex: 1;
}

.mw-actions {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.mw-hint {
  font-size: 10px;
  color: var(--color-text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.mw-quick-btns {
  display: flex;
  gap: var(--space-2);

  :deep(.base-button) {
    flex: 1;
    padding-left: 0;
    padding-right: 0;
  }
}

.mw-exact-btn {
  margin-top: var(--space-2);
}
</style>
