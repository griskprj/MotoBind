<script setup lang="ts">
interface Props {
  modelValue?: string
  label?: string
  hint?: string
  error?: string
  placeholder?: string
  disabled?: boolean
  readonly?: boolean
  required?: boolean
  rows?: number
  maxlength?: number
  autosize?: boolean
  id?: string
  name?: string
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  rows: 4,
  disabled: false,
  readonly: false,
  required: false,
  autosize: false,
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  blur: [event: FocusEvent]
  focus: [event: FocusEvent]
}>()

const inputId = useId()
const id = computed(() => props.id ?? inputId)
const textareaRef = ref<HTMLTextAreaElement | null>(null)

function resize() {
  if (!props.autosize || !textareaRef.value) return
  const el = textareaRef.value
  el.style.height = 'auto'
  el.style.height = `${el.scrollHeight}px`
}

function onInput(event: Event) {
  emit('update:modelValue', (event.target as HTMLTextAreaElement).value)
  resize()
}

onMounted(resize)
watch(() => props.modelValue, () => nextTick(resize))
</script>

<template>
  <div
    class="field"
    :class="{
      'field--error': !!error,
      'field--disabled': disabled,
    }"
  >
    <label v-if="label" :for="id" class="field__label">
      {{ label }}
      <span v-if="required" class="field__required" aria-hidden="true">*</span>
    </label>

    <textarea
      :id="id"
      ref="textareaRef"
      :name="name"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :readonly="readonly"
      :required="required"
      :rows="rows"
      :maxlength="maxlength"
      class="field__textarea"
      :class="{ 'field__textarea--error': !!error }"
      :aria-invalid="!!error || undefined"
      :aria-describedby="
        [error ? `${id}-error` : null, hint ? `${id}-hint` : null]
          .filter(Boolean)
          .join(' ') || undefined
      "
      @input="onInput"
      @blur="emit('blur', $event)"
      @focus="emit('focus', $event)"
    />

    <p v-if="error && typeof error === 'string'" :id="`${id}-error`" class="field__error" role="alert">
      {{ error }}
    </p>
    <p v-else-if="hint" :id="`${id}-hint`" class="field__hint">
      {{ hint }}
    </p>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.field {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  width: 100%;
}

.field__label {
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  color: var(--color-text);
}

.field__required {
  color: var(--color-danger);
  margin-left: 2px;
}

.field__textarea {
  width: 100%;
  min-height: 80px;
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text);
  font-family: inherit;
  font-size: var(--text-base);
  line-height: var(--leading-base);
  resize: vertical;
  transition:
    border-color var(--transition-fast),
    box-shadow var(--transition-fast),
    background-color var(--transition-fast);

  &::placeholder {
    color: var(--color-text-tertiary);
  }

  &:hover:not(:disabled):not(:read-only) {
    border-color: var(--color-border-dark);
  }

  &:focus {
    outline: none;
    border-color: var(--color-brand);
    box-shadow: var(--shadow-focus);
  }

  &:disabled {
    cursor: not-allowed;
    background: var(--color-surface-secondary);
    color: var(--color-text-disabled);
  }

  &:read-only {
    background: var(--color-surface-secondary);
  }

  @include md-up {
    min-height: 96px;
  }
}

.field__textarea--error {
  border-color: var(--color-danger);

  &:focus {
    border-color: var(--color-danger);
    box-shadow: 0 0 0 3px var(--color-danger-soft);
  }
}

.field__error {
  font-size: var(--text-sm);
  color: var(--color-danger);
}

.field__hint {
  font-size: var(--text-sm);
  color: var(--color-text-tertiary);
}

.field--disabled .field__label {
  color: var(--color-text-disabled);
}
</style>
