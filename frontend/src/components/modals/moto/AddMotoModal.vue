<template>
  <BaseModal
    :is-open="isOpen"
    title="Добавить мотоцикл"
    subtitle="Заполните информацию о мотоцикле"
    icon="motorcycle"
    variant="success"
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
            required
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
          class="drop-zone"
          :class="{ 'drag-over': isDragging, 'has-file': form.photoFile }"
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="handleDrop"
          @click="$refs.fileInput.click()"
        >
          <div v-if="form.photoPreview" class="photo-preview">
            <img :src="form.photoPreview" alt="Фото мотоцикла" />
            <button type="button" class="remove-photo-btn" @click.stop="removePhoto">
              <i class="fa fa-times"></i>
            </button>
          </div>

          <div v-else class="drop-zone-content">
            <i class="fa fa-cloud-upload-alt"></i>
            <p>Нажмите или перетащите фото</p>
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

      <div class="modal-info-block info">
        <div class="modal-info-icon">
          <i class="fa fa-lightbulb"></i>
        </div>
        <p class="modal-info-text">
          Эти данные помогут строить статистику и подбирать мануалы для вашего мотоцикла
        </p>
      </div>
    </form>

    <template #actions>
      <BaseButton variant="secondary" block type="button" @click="closeModal">
        Отменить
      </BaseButton>
      <BaseButton
        variant="primary"
        icon="fa fa-plus"
        block
        type="submit"
        :disabled="!isFormValid"
        :loading="loading"
        @click="submit"
      >
        Добавить мотоцикл
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { BaseModal, BaseButton, BaseInput } from '@/components/ui'
import { useToast } from '@/composables/useToast'
import { useMotorcyclesStore } from '@/stores'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
})

const emit = defineEmits(['close', 'created'])
const toast = useToast()
const motorcyclesStore = useMotorcyclesStore()

const form = reactive({
  name: '',
  volume: null,
  years: null,
  mileage: null,
  licensePlate: null,
  vin: null,
  color: '#8B5CF6',
  photoFile: null,
  photoPreview: null,
})

const currentYear = new Date().getFullYear()
const isDragging = ref(false)
const loading = ref(false)

const isFormValid = computed(() => {
  return (
    form.name &&
    form.name.trim().length >= 2 &&
    form.mileage !== null &&
    form.mileage >= 0
  )
})

watch(
  () => props.isOpen,
  (newVal) => {
    if (newVal) resetForm()
    else cleanupPreview()
  }
)

function resetForm() {
  Object.assign(form, {
    name: '',
    volume: null,
    years: null,
    mileage: null,
    licensePlate: null,
    vin: null,
    color: '#8B5CF6',
    photoFile: null,
    photoPreview: null,
  })
  isDragging.value = false
  loading.value = false
}

function cleanupPreview() {
  if (form.photoPreview?.startsWith('blob:')) {
    URL.revokeObjectURL(form.photoPreview)
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
  form.photoFile = file
  form.photoPreview = URL.createObjectURL(file)
}

function removePhoto() {
  cleanupPreview()
  form.photoFile = null
  form.photoPreview = null
}

function closeModal() {
  cleanupPreview()
  emit('close')
}

async function submit() {
  if (!isFormValid.value) {
    toast.warning('Введите название и пробег')
    return
  }
  if (form.years && form.years > currentYear) {
    toast.error('Год выпуска не может быть в будущем')
    return
  }

  loading.value = true
  try {
    await motorcyclesStore.create(
      {
        name: form.name.trim(),
        volume: form.volume || null,
        years: form.years || null,
        mileage: form.mileage || 0,
        licensePlate: form.licensePlate || null,
        vin: form.vin || null,
        color: form.color || '#8B5CF6',
      },
      form.photoFile
    )
    cleanupPreview()
    emit('created')
    emit('close')
    toast.success('Мотоцикл добавлен')
  } catch (err) {
    console.error('Failed to create motorcycle:', err)
    toast.error(err.response?.data?.error || 'Ошибка при добавлении')
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
  transition: 0.2s;
}

.remove-photo-btn:hover {
  background: var(--danger);
  transform: scale(1.1);
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
  .form-row {
    grid-template-columns: 1fr;
  }
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
