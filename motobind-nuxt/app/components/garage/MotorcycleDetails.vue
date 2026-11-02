<script setup lang="ts">
import type { Motorcycle, UpdateMotorcyclePayload, ApiError } from '~/types'
import { asString } from '#imports';

const props = defineProps<{ motorcycle: Motorcycle }>()
const emit = defineEmits<{ updated: [] }>()

const api = useApi()
const toast = useToast()
const { errors, setFromApiError, clear } = useFormErrors()

const isEditing = ref(false)
const saving = ref(false)

const form = reactive({
  name: '',
  years: '',
  volume: '' as string | number,
  color: '',
  licensePlate: '',
  vin: '',
})

function resetForm() {
  form.name = asString(props.motorcycle.name)
  form.years = asString(props.motorcycle.years)
  form.volume = props.motorcycle.volume || ''
  form.color = props.motorcycle.color || '#FFFFFF'
  form.licensePlate = asString(props.motorcycle.license_plate)
  form.vin = asString(props.motorcycle.vin)
}

watch(isEditing, (val) => {
  if (val) {
    resetForm()
    clear()
  }
})

async function onSave() {
  saving.value = true
  clear()

  try {
    const payload: UpdateMotorcyclePayload = {
      name: asString(form.name).trim(),
      years: asString(form.years).trim() || null,
      volume: form.volume ? Number(form.volume) : null,
      color: form.color || null,
      licensePlate: asString(form.licensePlate).trim().toUpperCase() || null,
      vin: asString(form.vin).trim().toUpperCase() || null,
    }
    await api.motorcycle.update(props.motorcycle.id, payload)
    toast.success('Характеристики обновлены')
    isEditing.value = false
    emit('updated')
  } catch (e) {
    const err = e as ApiError
    setFromApiError(err)
    if (!err.fieldErrors) toast.error(err.message)
  } finally {
    saving.value = false
  }
}

function onCancel() {
  isEditing.value = false
  clear()
}
</script>

<template>
  <BaseCard padding="lg">
    <div class="details-header">
      <h2 class="section-title">Характеристики</h2>
      <BaseButton
        v-if="!isEditing"
        variant="ghost"
        size="sm"
        @click="isEditing = true"
      >
        <template #icon>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </template>
        Редактировать
      </BaseButton>
    </div>

    <!-- Режим просмотра -->
    <div v-if="!isEditing" class="details-grid">
      <div class="detail-item">
        <span class="detail-label">Год выпуска</span>
        <span class="detail-value">{{ motorcycle.years || '—' }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Объем двигателя</span>
        <span class="detail-value">{{ motorcycle.volume ? `${motorcycle.volume} см³` : '—' }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Цвет</span>
        <span class="detail-value flex-center">
          <span v-if="motorcycle.color" class="color-dot" :style="{ backgroundColor: motorcycle.color }" />
          {{ motorcycle.color || '—' }}
        </span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Госномер</span>
        <span class="detail-value font-mono">{{ motorcycle.license_plate || '—' }}</span>
      </div>
      <div class="detail-item span-2">
        <span class="detail-label">VIN</span>
        <span class="detail-value font-mono">{{ motorcycle.vin || '—' }}</span>
      </div>
    </div>

    <!-- Режим редактирования -->
    <form v-else class="details-form" @submit.prevent="onSave">
      <div class="form-grid">
        <BaseInput v-model="form.name" label="Название" required class="span-2" :error="errors.name" />
        <BaseInput v-model="form.years" label="Год выпуска" :error="errors.years" />
        <BaseInput v-model="form.volume" type="number" label="Объем (см³)" :error="errors.volume" />
        <BaseColorPicker v-model="form.color" label="Цвет" :error="errors.color" />
        <BaseInput v-model="form.licensePlate" label="Госномер" style="text-transform: uppercase;" :error="errors.licensePlate" />
        <BaseInput v-model="form.vin" label="VIN" maxlength="17" class="span-2" style="text-transform: uppercase;" :error="errors.vin" />
      </div>

      <div class="form-actions">
        <BaseButton variant="secondary" type="button" @click="onCancel">Отмена</BaseButton>
        <BaseButton variant="primary" type="submit" :loading="saving">Сохранить</BaseButton>
      </div>
    </form>
  </BaseCard>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.details-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-4);
}

.section-title {
  font-size: var(--text-lg);
  font-weight: var(--fw-semibold);
  color: var(--color-text);
}

.details-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);

  @include sm-up {
    grid-template-columns: 1fr 1fr;
  }
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.span-2 {
  @include sm-up { grid-column: span 2; }
}

.detail-label {
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-tertiary);
}

.detail-value {
  font-size: var(--text-base);
  color: var(--color-text);
  font-weight: var(--fw-medium);
}

.flex-center {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.color-dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 1px solid var(--color-border);
  flex-shrink: 0;
}

.font-mono {
  font-family: var(--font-mono);
  text-transform: uppercase;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);
  margin-bottom: var(--space-4);

  @include sm-up { grid-template-columns: 1fr 1fr; }
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-2);
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border-light);
}
</style>
