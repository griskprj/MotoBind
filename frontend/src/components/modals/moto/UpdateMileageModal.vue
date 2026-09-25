<template>
  <BaseModal
    v-if="motorcycle"
    :is-open="isOpen"
    title="Обновить пробег"
    :subtitle="`Текущий пробег: ${motorcycle.mileage || 0} км`"
    icon="tachometer"
    variant="default"
    size="sm"
    @close="$emit('close')"
  >
    <div class="form-stack">
      <BaseInput
        v-model.number="mileage"
        type="number"
        label="Новый пробег (км)"
        placeholder="Введите новый пробег"
        :min="0"
        :max="1000000"
        required
      />

      <div class="modal-info-block info">
        <div class="modal-info-icon">
          <i class="fa fa-info-circle"></i>
        </div>
        <p class="modal-info-text">
          Пробег используется для расчёта интервалов обслуживания и статистики вашего мотоцикла.
          Убедитесь, что значение корректно.
        </p>
      </div>
    </div>

    <template #actions>
      <BaseButton variant="secondary" block @click="$emit('close')">
        Отменить
      </BaseButton>
      <BaseButton
        variant="primary"
        icon="fa fa-save"
        block
        :disabled="!isFormValid"
        :loading="loading"
        @click="submit"
      >
        Сохранить
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { BaseModal, BaseButton, BaseInput } from '@/components/ui'
import { useToast } from '@/composables/useToast'
import { useMotorcyclesStore } from '@/stores'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  motorcycle: { type: Object, default: null },
})

const emit = defineEmits(['close'])
const toast = useToast()
const motorcyclesStore = useMotorcyclesStore()

const mileage = ref(null)
const loading = ref(false)

const isFormValid = computed(() => {
  return (
    mileage.value !== null &&
    mileage.value !== '' &&
    mileage.value >= 0 &&
    mileage.value <= 1000000
  )
})

watch(
  () => props.isOpen,
  (newVal) => {
    if (newVal) {
      mileage.value = null
      loading.value = false
    }
  }
)

async function submit() {
  if (!isFormValid.value) {
    toast.error('Укажите корректный пробег (от 0 до 1 000 000 км)')
    return
  }

  if (props.motorcycle && mileage.value < (props.motorcycle.mileage || 0)) {
    if (!confirm('Внимание! Новый пробег меньше текущего. Продолжить?')) {
      return
    }
  }

  loading.value = true
  try {
    await motorcyclesStore.updateMileage(props.motorcycle.id, mileage.value)
    emit('close')
    toast.success('Пробег обновлён')
  } catch (err) {
    console.error('Failed to update mileage:', err)
    toast.error(err.response?.data?.error || 'Ошибка обновления пробега')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.form-stack {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

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

.modal-info-icon {
  font-size: 18px;
  color: var(--accent-text);
  flex-shrink: 0;
  margin-top: 2px;
}

.modal-info-text {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
}

@media (max-width: 640px) {
  .modal-info-block {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  .modal-info-icon {
    margin-top: 0;
  }
}
</style>
