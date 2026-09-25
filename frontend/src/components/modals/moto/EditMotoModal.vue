<template>
  <BaseModal
    :is-open="isOpen"
    title="Редактировать мотоцикл"
    subtitle="Измените информацию о мотоцикле"
    icon="pen"
    variant="default"
    size="md"
    @close="closeModal"
  >
    <form @submit.prevent="submit" class="form-stack">
      <!-- Основная информация -->
      <div class="form-section">
        <div class="form-section-title">
          <i class="fa fa-info-circle"></i>
          Основная информация
        </div>

        <BaseInput
          v-model="form.name"
          label="Название"
          placeholder="Например: Honda CBR600RR"
          required
        />

        <div class="form-row">
          <BaseInput
            v-model.number="form.years"
            type="number"
            label="Год выпуска"
            placeholder="2020"
            :min="1950"
            :max="currentYear"
          />
          <BaseInput
            v-model.number="form.volume"
            type="number"
            label="Объём (см³)"
            placeholder="600"
            :min="49"
            :max="4000"
          />
        </div>

        <div class="form-row">
          <BaseInput
            v-model.number="form.mileage"
            type="number"
            label="Пробег (км)"
            placeholder="0"
            :min="0"
            :max="1000000"
          />
          <div class="form-field-color">
            <label class="color-label">Цвет</label>
            <input v-model="form.color" type="color" class="color-input" />
          </div>
        </div>
      </div>

      <!-- Документы -->
      <div class="form-section">
        <div class="form-section-title">
          <i class="fa fa-file-text"></i>
          Документы
        </div>

        <div class="form-row">
          <BaseInput
            v-model="form.licensePlate"
            label="Гос. номер"
            placeholder="A123BC"
            :maxlength="9"
          />
          <BaseInput
            v-model="form.vin"
            label="VIN (17 символов)"
            placeholder="Введите 17 символов"
            :minlength="17"
            :maxlength="17"
          />
        </div>
      </div>

      <!-- Фото -->
      <div class="form-section">
        <div class="form-section-title">
          <i class="fa fa-image"></i>
          Фото мотоцикла
        </div>

        <div
          v-if="form.existingPhotoUrl && !form.deleteExistingPhoto"
          class="current-photo"
        >
          <img :src="getMotoPhotoUrl(form.existingPhotoUrl)" alt="Текущее фото" />
          <div class="current-photo-info">
            <span class="current-photo-label">Текущее фото</span>
            <button type="button" class="remove-existing-btn" @click="removeExistingPhoto">
              <i class="fa fa-trash"></i> Удалить фото
            </button>
          </div>
        </div>

        <div v-else-if="form.deleteExistingPhoto" class="photo-deleted-message">
          <i class="fa fa-check-circle"></i>
          <span>Фото будет удалено при сохранении</span>
          <button type="button" class="undo-delete-btn" @click="undoDeletePhoto">
            <i class="fa fa-undo"></i> Отменить
          </button>
        </div>

        <div
          class="drop-zone"
          :class="{
            'drag-over': isDragging,
            'has-file': form.newPhotoFile,
            'has-existing': form.existingPhotoUrl && !form.deleteExistingPhoto,
          }"
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="handleDrop"
          @click="$refs.fileInput.click()"
        >
          <div v-if="form.newPhotoPreview" class="photo-preview">
            <img :src="form.newPhotoPreview" alt="Новое фото" />
            <button type="button" class="remove-photo-btn" @click.stop="removeNewPhoto">
              <i class="fa fa-times"></i>
            </button>
          </div>

          <div v-else class="drop-zone-content">
            <i class="fa fa-cloud-upload-alt"></i>
            <p>
              {{ form.existingPhotoUrl && !form.deleteExistingPhoto
                ? 'Нажмите чтобы заменить фото'
                : 'Нажмите или перетащите фото' }}
            </p>
            <span>JPG, PNG, GIF, BMP, WEBP до 10 МБ</span>
          </div>

          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            @change="handleFileSelect"
            style="display: none"
          />
        </div>
      </div>
    </form>

    <template #actions>
      <BaseButton variant="secondary" block type="button" @click="closeModal">
        Отменить
      </BaseButton>
      <BaseButton
        variant="primary"
        icon="fa fa-save"
        block
        type="submit"
        :disabled="loading || !form.name"
        :loading="loading"
        @click="submit"
      >
        Сохранить
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'
import { BaseModal, BaseButton, BaseInput } from '@/components/ui'
import { useToast } from '@/composables/useToast'
import { useMotorcyclesStore } from '@/stores'
import { getMotoPhotoUrl } from '@/utils/mediaUrl'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  motorcycle: { type: Object, default: null },
})

const emit = defineEmits(['close'])
const toast = useToast()
const motorcyclesStore = useMotorcyclesStore()

const form = reactive({
  id: null,
  name: '',
  volume: null,
  years: null,
  mileage: null,
  licensePlate: null,
  vin: null,
  color: '#8B5CF6',
  existingPhotoUrl: null,
  newPhotoFile: null,
  newPhotoPreview: null,
  deleteExistingPhoto: false,
})

const currentYear = new Date().getFullYear()
const isDragging = ref(false)
const loading = ref(false)

watch(
  () => props.isOpen,
  (newVal) => {
    if (newVal && props.motorcycle) loadMotorcycleData()
    else cleanupPreview()
  }
)

watch(
  () => props.motorcycle,
  (newVal) => {
    if (props.isOpen && newVal) loadMotorcycleData()
  },
  { deep: true }
)

function loadMotorcycleData() {
  if (!props.motorcycle) return
  Object.assign(form, {
    id: props.motorcycle.id,
    name: props.motorcycle.name || '',
    volume: props.motorcycle.volume || null,
    years: props.motorcycle.years || null,
    mileage: props.motorcycle.mileage || null,
    licensePlate: props.motorcycle.license_plate || null,
    vin: props.motorcycle.vin || null,
    color: props.motorcycle.color || '#8B5CF6',
    existingPhotoUrl: props.motorcycle.photo_url || null,
    newPhotoFile: null,
    newPhotoPreview: null,
    deleteExistingPhoto: false,
  })
  isDragging.value = false
  loading.value = false
}

function cleanupPreview() {
  if (form.newPhotoPreview?.startsWith('blob:')) {
    URL.revokeObjectURL(form.newPhotoPreview)
  }
}

function handleFileSelect(event) {
  const file = event.target.files[0]
  if (file) processFile(file)
}

function handleDrop(event) {
  isDragging.value = false
  const file = event.dataTransfer.files[0]
  if (file) processFile(file)
}

function processFile(file) {
  if (file.size > 10 * 1024 * 1024) {
    toast.error('Файл слишком большой. Максимальный размер 10 МБ.')
    return
  }
  const allowedTypes = [
    'image/jpeg', 'image/jpg', 'image/png',
    'image/gif', 'image/bmp', 'image/webp',
  ]
  if (!allowedTypes.includes(file.type)) {
    toast.error('Неподдерживаемый формат. Разрешены: JPG, PNG, GIF, BMP, WEBP')
    return
  }

  cleanupPreview()
  form.newPhotoFile = file
  form.newPhotoPreview = URL.createObjectURL(file)
  form.deleteExistingPhoto = false
}

function removeNewPhoto() {
  cleanupPreview()
  form.newPhotoFile = null
  form.newPhotoPreview = null
}

function removeExistingPhoto() {
  if (!confirm('Удалить текущее фото мотоцикла?')) return
  form.deleteExistingPhoto = true
  removeNewPhoto()
}

function undoDeletePhoto() {
  form.deleteExistingPhoto = false
  if (props.motorcycle) {
    form.existingPhotoUrl = props.motorcycle.photo_url || null
  }
}

function closeModal() {
  cleanupPreview()
  emit('close')
}

async function submit() {
  if (!form.name || form.name.trim().length < 2) {
    toast.warning('Введите название мотоцикла (минимум 2 символа)')
    return
  }
  if (form.years && form.years > currentYear) {
    toast.error('Год выпуска не может быть в будущем')
    return
  }

  loading.value = true
  try {
    await motorcyclesStore.update(
      form.id,
      {
        name: form.name.trim(),
        volume: form.volume || null,
        years: form.years || null,
        mileage: form.mileage || null,
        licensePlate: form.licensePlate || null,
        vin: form.vin || null,
        color: form.color || '#8B5CF6',
      },
      {
        newPhotoFile: form.newPhotoFile,
        deleteExistingPhoto: form.deleteExistingPhoto,
      }
    )
    cleanupPreview()
    emit('close')
    toast.success('Мотоцикл обновлён')
  } catch (err) {
    console.error('Failed to update motorcycle:', err)
    toast.error(err.response?.data?.error || 'Ошибка при сохранении')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.form-stack {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.form-section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-muted);
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.form-section-title i {
  color: var(--accent-text);
  font-size: 14px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.form-field-color {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.color-label {
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  color: var(--text-secondary);
}

.color-input {
  width: 100%;
  height: 40px;
  padding: 2px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-input);
  cursor: pointer;
  background: var(--bg-input);
}

.current-photo {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 16px;
  background: var(--bg-secondary);
  border-radius: 10px;
  border: 1px solid var(--border-light);
}

.current-photo img {
  width: 64px;
  height: 64px;
  border-radius: 8px;
  object-fit: cover;
  border: 1px solid var(--border-light);
  flex-shrink: 0;
}

.current-photo-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.current-photo-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
}

.remove-existing-btn {
  padding: 4px 14px;
  background: var(--danger-trans);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 6px;
  color: var(--danger-text);
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  width: fit-content;
}

.remove-existing-btn:hover {
  border-color: rgba(239, 68, 68, 0.4);
}

.photo-deleted-message {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  background: var(--warning-trans);
  border: 1px solid rgba(245, 158, 11, 0.2);
  border-radius: 8px;
  color: var(--warning-text);
  font-size: 14px;
}

.undo-delete-btn {
  margin-left: auto;
  padding: 4px 12px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 12px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.drop-zone {
  border: 2px dashed var(--border-color);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  min-height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  background: var(--bg-secondary);
}

.drop-zone:hover {
  border-color: var(--accent);
  background: var(--accent-trans);
}

.drop-zone.drag-over {
  border-color: var(--accent);
  background: var(--accent-trans);
}

.drop-zone.has-file {
  border-color: var(--success-text);
  background: var(--success-trans);
  padding: 8px;
}

.drop-zone-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.drop-zone-content i {
  font-size: 32px;
  color: var(--text-muted);
}

.drop-zone-content p {
  margin: 0;
  font-size: 14px;
  color: var(--text-secondary);
}

.drop-zone-content span {
  font-size: 12px;
  color: var(--text-muted);
}

.photo-preview {
  position: relative;
  width: 100%;
  max-height: 180px;
  overflow: hidden;
  border-radius: 8px;
}

.photo-preview img {
  width: 100%;
  height: auto;
  max-height: 180px;
  object-fit: contain;
  border-radius: 8px;
}

.remove-photo-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.9);
  border: none;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.remove-photo-btn:hover {
  background: var(--danger);
  transform: scale(1.1);
}

@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  .current-photo {
    flex-direction: column;
    text-align: center;
  }
  .remove-existing-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
