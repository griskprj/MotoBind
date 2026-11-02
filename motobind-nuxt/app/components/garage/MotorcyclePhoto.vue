<script setup lang="ts">
import type { Motorcycle, ApiError } from '~/types'

const props = defineProps<{ motorcycle: Motorcycle }>()
const emit = defineEmits<{ updated: [] }>()

const api = useApi()
const toast = useToast()
const mediaUrl = useMediaUrl()

const fileInput = ref<HTMLInputElement | null>(null)
const uploading = ref(false)

const photo = computed(() => mediaUrl(props.motorcycle.photo_url))

async function onFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  if (file.size > 5 * 1024 * 1024) {
    toast.error('Фото не должно превышать 5МБ')
    return
  }

  uploading.value = true
  try {
    await api.motorcycle.uploadPhoto(props.motorcycle.id, file)
    toast.success('Фото обновлено')
    emit('updated')
  } catch (e) {
    toast.error((e as ApiError).message || 'Ошибка загрузки фото')
  } finally {
    uploading.value = false
    if (fileInput.value) fileInput.value.value = ''
  }
}

async function onDelete() {
  if (!confirm('Удалить фото?')) return

  uploading.value = true
  try {
    await api.motorcycle.deletePhoto(props.motorcycle.id)
    toast.success('Фото удалено')
    emit('updated')
  } catch (e) {
    toast.error((e as ApiError).message || 'Ошибка удаления фото')
  } finally {
    uploading.value = false
  }
}
</script>

<template>
  <BaseCard padding="none" class="photo-card">
    <div class="photo-wrap">
      <img v-if="photo" :src="photo" :alt="motorcycle.name" class="photo-img" />
      <div v-else class="photo-placeholder">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" opacity="0.5">
          <path d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>Нет фото</span>
      </div>

      <!-- Оверлей с кнопками -->
      <div class="photo-actions">
        <input type="file" accept="image/*" class="visually-hidden" ref="fileInput" @change="onFileChange" />
        <BaseButton variant="secondary" size="sm" :loading="uploading" @click="fileInput?.click()">
          {{ photo ? 'Заменить' : 'Загрузить' }}
        </BaseButton>
        <BaseButton v-if="photo" variant="danger" size="sm" icon-only :disabled="uploading" @click="onDelete">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </BaseButton>
      </div>
    </div>
  </BaseCard>
</template>

<style scoped lang="scss">
.photo-card {
  overflow: hidden;
}

.photo-wrap {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  background: var(--color-surface-secondary);

  @media (min-width: 1024px) {
    aspect-ratio: 21 / 9;
  }
}

.photo-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  color: var(--color-text-tertiary);
  font-size: var(--text-sm);
}

.photo-actions {
  position: absolute;
  bottom: var(--space-3);
  right: var(--space-3);
  display: flex;
  gap: var(--space-2);
  opacity: 0;
  transition: opacity var(--transition-fast);

  .photo-wrap:hover &,
  &:focus-within {
    opacity: 1;
  }

  @media (hover: none) {
    opacity: 1;
  }
}
</style>
