<script setup lang="ts">
export interface SelectOption {
  value: string | number
  label: string
  disabled?: boolean
}

interface Props {
  modelValue?: string | number
  options?: SelectOption[]
  label?: string
  hint?: string
  error?: string
  placeholder?: string
  disabled?: boolean
  required?: boolean
  id?: string
  name?: string
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  options: () => [],
  disabled: false,
  required: false,
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number]
  change: [value: string | number]
}>()

const inputId = useId()
const id = computed(() => props.id ?? inputId)

function onChange(event: Event) {
  const value = (event.target as HTMLSelectElement).value
  emit('update:modelValue', value)
  emit('change', value)
}
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

    <div class="field__select-wrap">
      <select
        :id="id"
        :name="name"
        :value="modelValue"
        :disabled="disabled"
        :required="required"
        class="field__select"
        :class="{ 'field__select--error': !!error }"
        :aria-invalid="!!error || undefined"
        :aria-describedby="
          [error ? `${id}-error` : null, hint ? `${id}-hint` : null]
            .filter(Boolean)
            .join(' ') || undefined
        "
        @change="onChange"
      >
        <option v-if="placeholder" value="" disabled>
          {{ placeholder }}
        </option>
        <slot>
          <option
            v-for="opt in options"
            :key="opt.value"
            :value="opt.value"
            :disabled="opt.disabled"
          >
            {{ opt.label }}
          </option>
        </slot>
      </select>
      <span class="field__select-arrow" aria-hidden="true">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none">
          <path
            d="M6 9l6 6 6-6"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </span>
    </div>

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

.field__select-wrap {
  position: relative;
}

.field__select {
  width: 100%;
  min-height: 40px;
  padding: var(--space-2) var(--space-8) var(--space-2) var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text);
  font-family: inherit;
  font-size: var(--text-base);
  line-height: var(--leading-base);
  appearance: none;
  cursor: pointer;
  transition:
    border-color var(--transition-fast),
    box-shadow var(--transition-fast),
    background-color var(--transition-fast);

  &:hover:not(:disabled) {
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

  @include md-up {
    min-height: 44px;
  }
}

.field__select--error {
  border-color: var(--color-danger);

  &:focus {
    border-color: var(--color-danger);
    box-shadow: 0 0 0 3px var(--color-danger-soft);
  }
}

.field__select-arrow {
  position: absolute;
  top: 50%;
  right: var(--space-3);
  transform: translateY(-50%);
  pointer-events: none;
  color: var(--color-text-tertiary);
  display: flex;
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
