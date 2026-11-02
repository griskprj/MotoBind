<script setup lang="ts">
interface Props {
  modelValue?: boolean
  label?: string
  disabled?: boolean
  id?: string
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: false,
  disabled: false,
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const inputId = useId()
const id = computed(() => props.id ?? inputId)

function onChange(event: Event) {
  emit('update:modelValue', (event.target as HTMLInputElement).checked)
}
</script>

<template>
  <label :for="id" class="checkbox" :class="{ 'checkbox--disabled': disabled }">
    <input
      :id="id"
      type="checkbox"
      :checked="modelValue"
      :disabled="disabled"
      class="checkbox__input"
      @change="onChange"
    />
    <span class="checkbox__box" aria-hidden="true">
      <svg viewBox="0 0 24 24" fill="none">
        <path
          d="M5 12l5 5L20 7"
          stroke="currentColor"
          stroke-width="3"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </span>
    <span v-if="label" class="checkbox__label">{{ label }}</span>
  </label>
</template>

<style scoped lang="scss">
.checkbox {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  cursor: pointer;
  user-select: none;
  font-size: var(--text-sm);
  color: var(--color-text);
}

.checkbox--disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.checkbox__input {
  position: absolute;
  opacity: 0;
  width: 1px;
  height: 1px;
  pointer-events: none;
}

.checkbox__box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  color: transparent;
  transition: all var(--transition-fast);
  flex-shrink: 0;

  svg {
    width: 14px;
    height: 14px;
  }
}

.checkbox__input:focus-visible + .checkbox__box {
  box-shadow: var(--shadow-focus);
  border-color: var(--color-brand);
}

.checkbox__input:checked + .checkbox__box {
  background: var(--color-brand);
  border-color: var(--color-brand);
  color: #fff; /* Галочка всегда белая */
}

.checkbox__input:disabled + .checkbox__box {
  background: var(--color-surface-secondary);
  border-color: var(--color-border-light);
}
</style>
