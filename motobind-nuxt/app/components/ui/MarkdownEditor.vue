<script setup lang="ts">
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'

const props = defineProps<{
  modelValue: string
  label?: string
  placeholder?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const editorId = `md-editor-${Math.random().toString(36).substr(2, 9)}`

const toolbars = [
  'bold', 'italic', 'strike', 'title',
  'unorderedList', 'orderedList',
  'link',
  'image',
  'table', 'code', 'preview', 'fullscreen'
]
</script>

<template>
  <div class="markdown-editor-wrap">
    <label v-if="label" class="editor-label">{{ label }}</label>

    <ClientOnly>
      <MdEditor
        :id="editorId"
        :model-value="modelValue"
        :placeholder="placeholder || 'Введите текст...'"
        :toolbars="['bold', 'italic', 'strike', 'title', 'unorderedList', 'orderedList', 'link', 'image', 'table', 'code', 'preview', 'fullscreen']"
        language="ru-RU"
        :on-upload-img="onUploadImg"
        @update:model-value="emit('update:modelValue', $event)"
      />
      <template #fallback>
        <div class="editor-placeholder">Загрузка редактора...</div>
      </template>
    </ClientOnly>
  </div>
</template>

<style scoped lang="scss">
.markdown-editor-wrap {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  width: 100%;
}

.editor-label {
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  color: var(--color-text);
}

:deep(.md-editor) {
  --md-bk-color: var(--color-surface);
  --md-color: var(--color-text);
  --md-border-color: var(--color-border);
  --md-bk-color-outstand: var(--color-surface-secondary);
  --md-bk-hover-color: var(--color-surface-hover);
  --md-border-hover-color: var(--color-border-dark);
  --md-border-active-color: var(--color-brand);
  --md-modal-mask: rgba(0, 0, 0, 0.5);

  border-radius: var(--radius-md);
  font-family: var(--font-sans);
}

:deep(.md-editor-dark) {
  --md-bk-color: var(--color-surface);
  --md-color: var(--color-text);
  --md-border-color: var(--color-border);
  --md-bk-color-outstand: var(--color-surface-secondary);
  --md-bk-hover-color: var(--color-surface-hover);
  --md-border-hover-color: var(--color-border-dark);
  --md-border-active-color: var(--color-brand);
}
</style>
