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
const rollbackWarning = ref(false)

const inputValue = ref(props.currentMileage || 0)
watch(inputValue, () => { rollbackWarning.value = false })

const quickSteps = [50, 100, 500, 1000]

function addToMileage(amount: number) {
  inputValue.value = Number(inputValue.value || 0) + amount
}

async function onSave(confirmDeletion = false) {
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
    await api.motorcycle.update(props.motorcycleId, {
      mileage: newMileage,
      ...(confirmDeletion ? { confirm_maintenance_deletion: true } : {}),
    })
    toast.success(confirmDeletion ? 'Пробег обновлён, выполненные ТО удалены' : 'Пробег обновлён')
    emit('updated')
    emit('close')
  } catch (e) {
    const error = e as ApiError
    if (error.status === 409 && newMileage < props.currentMileage && !confirmDeletion) {
      rollbackWarning.value = true
      return
    }
    toast.error(error.message || 'Ошибка обновления')
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

      <p v-if="rollbackWarning" class="rollback-warning" role="alert">
        Все выполненные ТО, отмеченные пробегом выше {{ Number(inputValue).toLocaleString('ru-RU') }} км,
        будут удалены. Запланированные ТО останутся. Подтвердить изменение пробега?
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
      <BaseButton v-if="rollbackWarning" variant="ghost" size="sm" :disabled="submitting" @click="rollbackWarning = false">Назад</BaseButton>
      <BaseButton v-else variant="ghost" size="sm" @click="emit('close')">Отмена</BaseButton>
      <BaseButton v-if="rollbackWarning" variant="danger" size="sm" :loading="submitting" @click="onSave(true)">
        Удалить ТО и сохранить
      </BaseButton>
      <BaseButton v-else variant="primary" size="sm" :loading="submitting" @click="onSave()">
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

.rollback-warning {
  padding: var(--space-3);
  border-radius: var(--radius-md);
  color: var(--color-danger);
  background: var(--color-danger-soft);
  font-size: var(--text-sm);
  line-height: var(--leading-relaxed);
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
