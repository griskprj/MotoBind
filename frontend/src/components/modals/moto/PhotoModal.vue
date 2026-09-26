<template>
  <BaseModal
    :is-open="isOpen"
    title="Фото мотоцикла"
    subtitle="Загрузите или измените фото мотоцикла"
    icon="camera"
    variant="default"
    size="md"
    @close="close"
  >
    <div v-if="motorcycle?.photo_url && !selectedFile" class="current-photo">
      <img :src="getMotoPhotoUrl(motorcycle.photo_url)" alt="Мотоцикл">
      <BaseButton variant="danger" icon="fa fa-trash" @click="handleDelete">
        Удалить фото
      </BaseButton>
    </div>

    <div class="upload-section">
      <div
        class="drop-zone"
        :class="{ 'drag-over': isDragging, 'has-file': selectedFile }"
        @dragover.prevent="isDragging = true"
        @dragleave.prevent="isDragging = false"
        @drop.prevent="handleDrop"
        @click="$refs.fileInput.click()"
      >
        <div v-if="selectedFile && previewUrl" class="photo-preview">
          <img :src="previewUrl" alt="Превью">
          <button type="button" class="remove-photo-btn" @click.stop="clearFile">
            <i class="fa fa-times"></i>
          </button>
        </div>
        <div v-else class="drop-zone-content">
          <i class="fa fa-cloud-upload-alt"></i>
          <p>Перетащите фото сюда или кликните для выбора</p>
          <span>JPG, PNG, GIF, BMP, WEBP до 10 МБ</span>
        </div>
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          @change="handleFileSelect"
          style="display: none"
        >
      </div>

      <div v-if="selectedFile" class="file-info">
        <div class="file-info-icon"><i class="fa fa-file-image-o"></i></div>
        <div class="file-info-content">
          <span class="file-name">{{ selectedFile.name }}</span>
          <span class="file-size">{{ formatFileSize(selectedFile.size) }}</span>
        </div>
        <button type="button" class="btn-remove-file" @click="clearFile">
          <i class="fa fa-times"></i>
        </button>
      </div>
    </div>

    <div class="modal-info-block info">
      <div class="modal-info-icon"><i class="fa fa-info-circle"></i></div>
      <p class="modal-info-text">
        Рекомендуемый размер: 1200×800 пикселей. Фото будет отображаться в вашем гараже.
      </p>
    </div>

    <template #actions>
      <BaseButton variant="secondary" block @click="close">Отменить</BaseButton>
      <BaseButton
        v-if="selectedFile"
        variant="primary"
        icon="fa fa-upload"
        block
        :loading="uploading"
        @click="handleUpload"
      >
        Загрузить
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, watch } from 'vue'
import { BaseModal, BaseButton } from '@/components/ui'
import { useToast } from '@/composables/useToast'
import { useMotorcyclesStore } from '@/stores'
import { getMotoPhotoUrl } from '@/utils/mediaUrl'

const props = defineProps({
  isOpen: { type: Boolean, required: true },
  motorcycle: { type: Object, required: true },
})

const emit = defineEmits(['close'])
const toast = useToast()
const motorcyclesStore = useMotorcyclesStore()

const selectedFile = ref(null)
const previewUrl = ref(null)
const isDragging = ref(false)
const uploading = ref(false)

watch(
  () => props.isOpen,
  (val) => {
    if (!val) {
      clearFile()
      isDragging.value = false
    }
  }
)

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
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
  selectedFile.value = file
  previewUrl.value = URL.createObjectURL(file)
}

function clearFile() {
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
  selectedFile.value = null
  previewUrl.value = null
}

function formatFileSize(bytes) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

async function handleUpload() {
  if (!selectedFile.value) return
  uploading.value = true
  try {
    await motorcyclesStore.uploadPhoto(props.motorcycle.id, selectedFile.value)
    clearFile()
    emit('close')
    toast.success('Фото загружено')
  } catch (err) {
    console.error('Failed to upload photo:', err)
    toast.error(err.response?.data?.error || 'Ошибка загрузки фото')
  } finally {
    uploading.value = false
  }
}

async function handleDelete() {
  if (!confirm('Удалить фото?')) return
  try {
    await motorcyclesStore.deletePhoto(props.motorcycle.id)
    emit('close')
    toast.success('Фото удалено')
  } catch (err) {
    console.error('Failed to delete photo:', err)
    toast.error(err.response?.data?.error || 'Ошибка удаления фото')
  }
}

function close() {
  clearFile()
  isDragging.value = false
  emit('close')
}
</script>

<style scoped>
.current-photo {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-bottom: 18px;
}

.current-photo img {
  max-width: 100%;
  max-height: 260px;
  border-radius: 12px;
  object-fit: cover;
  border: 1px solid var(--border-light);
}

.upload-section { margin-top: 4px; }

.drop-zone {
  border: 2px dashed var(--border-color);
  border-radius: 12px;
  padding: 32px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  min-height: 140px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  background: var(--bg-secondary);
}

.drop-zone:hover,
.drop-zone.drag-over {
  border-color: var(--accent);
  background: var(--accent-trans);
}

.drop-zone.has-file {
  border-color: var(--success-text);
  background: var(--success-trans);
  padding: 8px;
  min-height: 100px;
}

.drop-zone-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.drop-zone-content i {
  font-size: 40px;
  color: var(--text-muted);
}

.drop-zone-content p {
  margin: 0;
  font-size: 15px;
  color: var(--text-secondary);
}

.drop-zone-content span {
  font-size: 13px;
  color: var(--text-muted);
}

.photo-preview {
  position: relative;
  width: 100%;
  max-height: 200px;
  overflow: hidden;
  border-radius: 8px;
}

.photo-preview img {
  width: 100%;
  height: auto;
  max-height: 200px;
  object-fit: contain;
  border-radius: 8px;
}

.remove-photo-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.9);
  border: none;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  margin-top: 10px;
  background: var(--bg-secondary);
  border-radius: 8px;
  border: 1px solid var(--border-light);
}

.file-info-icon { font-size: 20px; color: var(--accent-text); }

.file-info-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.file-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-size { font-size: 12px; color: var(--text-muted); }

.btn-remove-file {
  border-radius: 50%;
  border: none;
  background: var(--danger-trans);
  color: var(--danger-text);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px;
}

.modal-info-block {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 10px;
  margin-top: 14px;
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
  .modal-info-icon { margin-top: 0; }
}
</style>
