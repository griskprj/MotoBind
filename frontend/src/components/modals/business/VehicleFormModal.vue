<template>
  <ModalWrapper
    :is-open="isOpen"
    :title="isEdit ? 'Редактировать мотоцикл' : 'Новый мотоцикл'"
    :subtitle="isEdit ? 'Обновите данные' : 'Добавьте мотоцикл клиента'"
    icon="motorcycle"
    size="md"
    @close="close"
  >
    <div class="form-stack">
      <BaseInput
        v-model="form.name"
        label="Модель"
        placeholder="Yamaha R1"
        required
      />

      <div class="form-row">
        <BaseInput
          v-model.number="form.years"
          label="Год"
          type="number"
          placeholder="2018"
        />
        <BaseInput
          v-model.number="form.volume"
          label="Объём, см³"
          type="number"
          placeholder="998"
        />
      </div>

      <div class="form-row">
        <BaseInput
          v-model.number="form.mileage"
          label="Пробег, км"
          type="number"
          placeholder="12000"
        />
        <div class="field color-field">
          <label>Цвет</label>
          <input
            v-model="form.color"
            type="color"
            class="color-input"
          >
        </div>
      </div>

      <div class="form-row">
        <BaseInput
          v-model="form.license_plate"
          label="Гос. номер"
          placeholder="А123БВ777"
        />
        <BaseInput
          v-model="form.vin"
          label="VIN"
          placeholder="JT..."
        />
      </div>

      <div class="field">
        <label>Заметка</label>
        <textarea
          v-model="form.note"
          rows="2"
          placeholder="Состояние, особенности..."
        ></textarea>
      </div>
    </div>

    <template #actions>
      <BaseButton
        variant="primary"
        block
        icon="fa fa-check"
        :loading="business.mutating"
        :disabled="!canSave"
        @click="handleSave"
      >
        {{ isEdit ? 'Сохранить' : 'Добавить' }}
      </BaseButton>
    </template>
  </ModalWrapper>
</template>

<script setup>
import { computed, reactive, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useBusinessStore } from '@/stores'
import { useToast } from '../../../composables/useToast'
import ModalWrapper from '../ModalWrapper.vue'
import { BaseButton, BaseInput } from '../../../components/ui'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  vehicle: { type: Object, default: null },
})
const emit = defineEmits(['close', 'saved'])

const route = useRoute()
const business = useBusinessStore()
const toast = useToast()

const form = reactive({
  name: '',
  years: null,
  volume: null,
  mileage: null,
  license_plate: '',
  vin: '',
  color: '#FFFFFF',
  note: '',
})

const isEdit = computed(() => !!props.vehicle?.id)
const canSave = computed(() => form.name.trim().length >= 2)
const clientId = computed(() => Number(route.params.id))

watch(() => props.isOpen, (open) => {
  if (open) {
    form.name = props.vehicle?.name || ''
    form.years = props.vehicle?.years ?? null
    form.volume = props.vehicle?.volume ?? null
    form.mileage = props.vehicle?.mileage ?? null
    form.license_plate = props.vehicle?.license_plate || ''
    form.vin = props.vehicle?.vin || ''
    form.color = props.vehicle?.color || '#FFFFFF'
    form.note = props.vehicle?.note || ''
  }
})

async function handleSave() {
  if (!canSave.value) return
  const payload = {
    name: form.name.trim(),
    years: form.years || null,
    volume: form.volume || null,
    mileage: form.mileage || 0,
    license_plate: form.license_plate.trim() || null,
    vin: form.vin.trim() || null,
    color: form.color || '#FFFFFF',
    note: form.note.trim() || null,
  }

  try {
    if (isEdit.value) {
      await business.updateVehicle(clientId.value, props.vehicle.id, payload)
      toast.success('Мотоцикл обновлён')
    } else {
      await business.createVehicle(clientId.value, payload)
      toast.success('Мотоцикл добавлен')
    }
    emit('saved')
  } catch (err) {
    toast.error(err.response?.data?.error || 'Ошибка сохранения')
  }
}

function close() {
  emit('close')
}
</script>

<style scoped>
.form-stack { display: flex; flex-direction: column; gap: 14px; }
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.field { display: flex; flex-direction: column; gap: 4px; }
.field label {
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  color: var(--text-secondary);
}
.field textarea {
  width: 100%;
  padding: 0.625rem 0.75rem;
  font-size: var(--text-sm);
  font-family: inherit;
  background: var(--bg-input);
  border: 1px solid var(--border-input);
  border-radius: var(--radius);
  color: var(--text-primary);
  resize: vertical;
}
.field textarea:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: var(--shadow-focus);
}

.color-field .color-input {
  width: 100%;
  height: 40px;
  padding: 4px;
  background: var(--bg-input);
  border: 1px solid var(--border-input);
  border-radius: var(--radius);
  cursor: pointer;
}

@media (max-width: 480px) {
  .form-row { grid-template-columns: 1fr; }
}
</style>
