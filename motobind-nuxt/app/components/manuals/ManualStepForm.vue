<script setup lang="ts">
import type { ManualStepPayload } from '~/types'

const props = defineProps<{
  index: number
  modelValue: ManualStepPayload
  imageFile: File | null
  existingImage?: string | null
  isEditMode?: boolean
  stepId?: number | null
}>()

const emit = defineEmits<{
  'update:modelValue': [value: ManualStepPayload]
  'update:imageFile': [value: File | null]
  'remove-image': []
  remove: []
}>()

const mediaUrl = useMediaUrl()

const previewUrl = computed(() => {
  if (import.meta.server) return ''

  if (props.imageFile) {
    return URL.createObjectURL(props.imageFile)
  }
  if (props.existingImage) {
    return mediaUrl(props.existingImage)
  }
  return ''
})

let currentBlobUrl: string | null = null

watch(() => props.imageFile, (newFile) => {
  if (currentBlobUrl) {
    URL.revokeObjectURL(currentBlobUrl)
    currentBlobUrl = null
  }
  if (newFile && import.meta.client) {
    currentBlobUrl = URL.createObjectURL(newFile)
  }
}, { immediate: true })

onBeforeUnmount(() => {
  if (currentBlobUrl) URL.revokeObjectURL(currentBlobUrl)
})

function updateField(key: keyof ManualStepPayload, value: any) {
  emit('update:modelValue', { ...props.modelValue, [key]: value })
}

function onFileChange(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0] || null
  emit('update:imageFile', file)
}

function onRemoveImage() {
  if (props.existingImage && props.isEditMode && props.stepId) {
    emit('remove-image')
  } else {
    emit('update:imageFile', null)
  }
}
</script>

<template>
  <BaseCard padding="lg" class="step-card">
    <div class="step-header">
      <h3 class="step-title">Шаг {{ index + 1 }}</h3>
      <BaseButton variant="danger" size="sm" icon-only @click="emit('remove')">
        <i class="fa-solid fa-trash"></i>
      </BaseButton>
    </div>

    <div class="step-grid">
      <BaseInput
        :model-value="modelValue.title"
        label="Заголовок шага"
        placeholder="Например: Слейте старое масло"
        required
        class="span-2"
        @update:model-value="updateField('title', $event)"
      />

      <div class="span-2">
        <label class="field-label">Текст шага (Markdown)</label>
        <MarkdownEditor
          :model-value="modelValue.text || ''"
          placeholder="Подробное описание действий..."
          @update:model-value="updateField('text', $event)"
        />
      </div>

      <BaseInput
        :model-value="modelValue.tip || ''"
        label="Подсказка (Tip)"
        placeholder="Необязательно"
        @update:model-value="updateField('tip', $event)"
      />
      <BaseInput
        :model-value="modelValue.warning || ''"
        label="Предупреждение (Warning)"
        placeholder="Необязательно"
        @update:model-value="updateField('warning', $event)"
      />

      <!-- Загрузка картинки -->
      <div class="span-2 image-upload-wrap">
        <label class="field-label">Изображение шага</label>
        <label class="image-upload" :class="{ 'has-image': imageFile || existingImage }">
          <input type="file" accept="image/*" class="visually-hidden" @change="onFileChange" />

          <template v-if="previewUrl">
            <img :src="previewUrl" alt="Превью" class="preview-img" />
            <BaseButton
              variant="danger"
              size="sm"
              icon-only
              class="remove-btn"
              @click.stop.prevent="onRemoveImage"
            >
              <i class="fa-solid fa-xmark"></i>
            </BaseButton>
          </template>

          <template v-else>
            <div class="placeholder-content">
              <i class="fa-solid fa-camera"></i>
              <span>Загрузить фото</span>
            </div>
          </template>
        </label>
      </div>
    </div>
  </BaseCard>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.step-card {
  position: relative;
  background: var(--color-surface);
}

.step-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-3);
  border-bottom: 1px solid var(--color-border-light);
}

.step-title {
  font-size: var(--text-lg);
  font-weight: var(--fw-semibold);
  color: var(--color-text);
}

.step-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);
  @include sm-up { grid-template-columns: 1fr 1fr; }
}

.span-2 {
  @include sm-up { grid-column: span 2; }
}

.field-label {
  display: block;
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  color: var(--color-text);
  margin-bottom: var(--space-1);
}

.image-upload-wrap { margin-top: var(--space-2); }

.image-upload {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 320px;
  aspect-ratio: 16 / 9;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 2px dashed var(--color-border);
  background: var(--color-surface-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);

  &:hover {
    border-color: var(--color-brand);
    background: var(--color-surface-hover);
  }

  &.has-image {
    border-style: solid;
  }

  .preview-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .remove-btn {
    position: absolute;
    top: var(--space-2);
    right: var(--space-2);
    z-index: 2;
  }

  .placeholder-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-2);
    color: var(--color-text-tertiary);

    i { font-size: 24px; }
    span { font-size: var(--text-sm); }
  }
}

.image-preview {
  position: relative;
  width: 100%;
  height: 100%;
  img { width: 100%; height: 100%; object-fit: cover; }

  button {
    position: absolute;
    top: var(--space-2);
    right: var(--space-2);
  }
}

.image-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  gap: var(--space-2);
  color: var(--color-text-tertiary);
  cursor: pointer;
  transition: all var(--transition-fast);

  &:hover { background: var(--color-surface-hover); color: var(--color-brand); }
  i { font-size: 24px; }
}
</style>
