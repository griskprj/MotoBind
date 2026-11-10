<script setup lang="ts">
import type { ApiError } from '~/types'

const props = defineProps<{
  motorcycleId: number | string
  currentMileage: number
}>()

const emit = defineEmits<{
  close: []
  updated: []
}>()

const api = useApi()
const toast = useToast()
const submitting = ref(false)

const inputValue = ref(props.currentMileage || 0)

const quickSteps = [50, 100, 500, 1000]

function addToMileage(amount: number) {
  inputValue.value = Number(inputValue.value || 0) + amount
}

async function onSave() {
  const newMileage = Number(inputValue.value)
  if (isNaN(newMileage) || newMileage < 0) {
    toast.error('Некорректный пробег')
    return
  }

  if (newMileage === props.currentMileage) {
    emit('close')
    return
  }

  submitting.value = true
  try {
    await api.motorcycle.update(props.motorcycleId, { mileage: newMileage })
    toast.success('Пробег обновлён')
    emit('updated')
    emit('close')
  } catch (e) {
    toast.error((e as ApiError).message || 'Ошибка обновления')
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <BaseModal title="Обновить пробег" size="sm" @close="emit('close')">
    <div class="mileage-form">
      <p class="info-text">
        Текущий пробег: <strong>{{ currentMileage }} км</strong>
      </p>

      <!-- Ввод точного значения -->
      <BaseInput
        v-model="inputValue"
        type="number"
        label="Новый пробег (км)"
        required
      />

      <!-- Быстрые кнопки -->
      <div class="quick-add">
        <span class="quick-label">Быстро добавить:</span>
        <div class="quick-buttons">
          <BaseButton
            v-for="step in quickSteps"
            :key="step"
            variant="secondary"
            size="sm"
            @click="addToMileage(step)"
          >
            +{{ step }}
          </BaseButton>
        </div>
      </div>
    </div>

    <template #footer>
      <BaseButton variant="ghost" size="sm" @click="emit('close')">Отмена</BaseButton>
      <BaseButton variant="primary" size="sm" :loading="submitting" @click="onSave">
        <template #icon><i class="fa-solid fa-check"></i></template>
        Сохранить
      </BaseButton>
    </template>
  </BaseModal>
</template>

<style scoped lang="scss">
.mileage-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.info-text {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  strong { color: var(--color-text); }
}

.quick-add {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  margin-top: var(--space-2);
}

.quick-label {
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.quick-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}
</style>
