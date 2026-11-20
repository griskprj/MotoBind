<script setup lang="ts">
import type { Motorcycle, UpdateMotorcyclePayload, ApiError } from '~/types'
const props = defineProps<{
  motorcycle: Motorcycle
}>()

const emit = defineEmits<{
  close: []
  updated: []
}>()

const api = useApi()
const toast = useToast()
const mediaUrl = useMediaUrl()
const { errors, setFromApiError, clear } = useFormErrors()

const saving = ref(false)
const uploadingPhoto = ref(false)

const form = reactive({
  name: '',
  years: '',
  volume: '' as string | number,
  drive_type: 'chain' as 'chain' | 'belt' | 'shaft',
  color: '',
  licensePlate: '',
  vin: '',
})

// --- Фоо ---
const photoFile = ref<File | null>(null)
const photoPreview = ref<string | null>(null)

onMounted(() => {
  form.name = props.motorcycle.name || ''
  form.years = props.motorcycle.years || ''
  form.volume = props.motorcycle.volume || ''
  form.drive_type = props.motorcycle.drive_type || 'chain'
  form.color = props.motorcycle.color || '#FFFFFF'
  form.licensePlate = props.motorcycle.license_plate || ''
  form.vin = props.motorcycle.vin || ''

  if (props.motorcycle.photo_url) {
    photoPreview.value = mediaUrl(props.motorcycle.photo_url)
  }
})

function onFileChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return

  if (file.size > 5 * 1024 * 1024) {
    toast.error('Фото не должно превышать 5МБ')
    return
  }

  photoFile.value = file
  photoPreview.value = URL.createObjectURL(file)
}

async function removePhoto() {
  if (props.motorcycle.photo_url) {
    if (!confirm('Удалить фото?')) return
    try {
      uploadingPhoto.value = true
      await api.motorcycle.deletePhoto(props.motorcycle.id)
      toast.success('Фото удалено')
      photoPreview.value = null
      photoFile.value = null
      emit('updated')
    } catch (e) {
      toast.error('Ошибка удаления фото')
    } finally {
      uploadingPhoto.value = false
    }
  } else {
    photoPreview.value = null
    photoFile.value = null
  }
}

async function onSave() {
  saving.value = true
  clear()

  const safeString = (val: any): string => {
    if (val === null || val === undefined) return ''
    return String(val)
  }

  try {
    const payload: UpdateMotorcyclePayload = {
      name: safeString(form.name).trim(),
      years: safeString(form.years).trim() || null,
      volume: form.volume ? Number(form.volume) : null,
      drive_type: form.drive_type,
      color: form.color || null,
      licensePlate: safeString(form.licensePlate).trim().toUpperCase() || null,
      vin: safeString(form.vin).trim().toUpperCase() || null,
    }
    await api.motorcycle.update(props.motorcycle.id, payload)

    if (photoFile.value) {
      uploadingPhoto.value = true
      await api.motorcycle.uploadPhoto(props.motorcycle.id, photoFile.value)
      uploadingPhoto.value = false
    }

    toast.success('Мотоцикл обновлён')
    emit('updated')
    emit('close')
  } catch (e) {
    const err = e as ApiError
    setFromApiError(err)
    if (!err.fieldErrors) toast.error(err.message || 'Ошибка сохранения')
  } finally {
    saving.value = false
    uploadingPhoto.value = false
  }
}
</script>

<template>
  <BaseModal title="Редактировать мотоцикл" @close="emit('close')">
    <div class="edit-content">
      <!-- Блок фото -->
      <div class="photo-section">
        <label class="field-label">Фото мотоцикла</label>
        <div class="photo-wrap">
          <img v-if="photoPreview" :src="photoPreview" alt="Превью" class="photo-preview" />
          <div v-else class="photo-placeholder">
            <i class="fa-solid fa-camera"></i>
            <span>Нет фото</span>
          </div>
          <div class="photo-actions">
            <input type="file" accept="image/*" class="visually-hidden" @change="onFileChange" ref="fileInput" />
            <BaseButton variant="secondary" size="sm" :loading="uploadingPhoto" @click="($refs.fileInput as HTMLInputElement).click()">
              <i class="fa-solid fa-upload"></i> Загрузить
            </BaseButton>
            <BaseButton v-if="photoPreview" variant="danger" size="sm" @click="removePhoto">
              <i class="fa-solid fa-trash"></i> Удалить
            </BaseButton>
          </div>
        </div>
      </div>

      <!-- Форма характеристик -->
      <form @submit.prevent="onSave" class="edit-form">
        <div class="form-grid">
          <BaseInput v-model="form.name" label="Название" required class="span-2" :error="errors.name" />
          <BaseInput v-model="form.years" label="Год выпуска" :error="errors.years" />
          <BaseSelect
            v-model="form.drive_type"
            label="Тип привода"
            :options="[
              { value: 'chain', label: 'Цепь' },
              { value: 'belt', label: 'Ремень' },
              { value: 'shaft', label: 'Кардан' }
            ]"
            :error="errors.drive_type"
          />
          <BaseInput v-model="form.volume" type="number" label="Объем (см³)" :error="errors.volume" />
          <BaseColorPicker v-model="form.color" label="Цвет" :error="errors.color" />
          <BaseInput v-model="form.licensePlate" label="Госномер" style="text-transform: uppercase;" :error="errors.licensePlate" />
          <BaseInput v-model="form.vin" label="VIN" maxlength="17" class="span-2" style="text-transform: uppercase;" :error="errors.vin" />
        </div>
      </form>
    </div>

    <template #footer>
      <BaseButton variant="ghost" size="sm" @click="emit('close')">Отмена</BaseButton>
      <BaseButton variant="primary" size="sm" :loading="saving" @click="onSave">Сохранить</BaseButton>
    </template>
  </BaseModal>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.edit-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

/* Фото */
.photo-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.field-label {
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  color: var(--color-text);
}

.photo-wrap {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.photo-preview {
  width: 100%;
  max-height: 200px;
  object-fit: cover;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
}

.photo-placeholder {
  width: 100%;
  height: 150px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  background: var(--color-surface-secondary);
  border-radius: var(--radius-md);
  border: 2px dashed var(--color-border);
  color: var(--color-text-tertiary);

  i { font-size: 24px; }
}

.photo-actions {
  display: flex;
  gap: var(--space-2);
}

/* Форма */
.edit-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);
  @include sm-up { grid-template-columns: 1fr 1fr; }
}

.span-2 {
  @include sm-up { grid-column: span 2; }
}
</style>
