<script setup lang="ts">
interface Props {
  modelValue?: string
  label?: string
  error?: string
  hint?: string
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '#7C5CFC',
  disabled: false,
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const inputId = useId()
const id = computed(() => props.label ? inputId : undefined)

const localHex = ref(props.modelValue)

watch(() => props.modelValue, (val) => {
  localHex.value = val
})

function onNativeChange(event: Event) {
  const val = (event.target as HTMLInputElement).value
  localHex.value = val
  emit('update:modelValue', val)
}

function onTextInput(event: Event) {
  let val = (event.target as HTMLInputElement).value.trim().toUpperCase()

  if (val && !val.startsWith('#')) {
    val = '#' + val
  }

  localHex.value = val

  if (/^#([0-9A-F]{3}){1,2}$/i.test(val)) {
    emit('update:modelValue', val)
  }
}

function onBlur() {
  if (!/^#([0-9A-F]{3}){1,2}$/i.test(localHex.value)) {
    localHex.value = props.modelValue
  }
}

const presetColors = [
  '#000000', '#FFFFFF', '#7C5CFC', '#D94A4A', '#18A66A', '#D88919', '#3E82D7', '#66707D',
  '#FF5733', '#33FF57', '#3357FF', '#FF33F1', '#F1FF33', '#33FFF1', '#C70039', '#900C3F',
  '#FFC300', '#DAF7A6', '#581845', '#2C3E50'
]
</script>

<template>
  <div class="color-field" :class="{ 'color-field--error': !!error, 'color-field--disabled': disabled }">
    <label v-if="label" :for="id" class="color-field__label">
      {{ label }}
    </label>

    <div class="color-field__control">
      <!-- Нативный color picker в виде квадратика -->
      <div class="color-field__picker-wrap">
        <input
          type="color"
          :value="modelValue"
          :disabled="disabled"
          class="color-field__native"
          @input="onNativeChange"
        />
      </div>

      <!-- Текстовое поле для HEX -->
      <input
        :id="id"
        type="text"
        :value="localHex"
        :disabled="disabled"
        placeholder="#000000"
        maxlength="7"
        class="color-field__text"
        :class="{ 'color-field__text--error': !!error }"
        @input="onTextInput"
        @blur="onBlur"
      />
    </div>

    <!-- Палитра -->
    <div class="color-field__palette">
      <button
        v-for="color in presetColors"
        :key="color"
        type="button"
        class="color-field__swatch"
        :class="{ 'color-field__swatch--active': modelValue?.toUpperCase() === color }"
        :style="{ backgroundColor: color }"
        :title="color"
        :disabled="disabled"
        @click="emit('update:modelValue', color); localHex = color"
      />
    </div>

    <p v-if="error" class="color-field__error" role="alert">{{ error }}</p>
    <p v-else-if="hint" class="color-field__hint">{{ hint }}</p>
  </div>
</template>

<style scoped lang="scss">
.color-field {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  width: 100%;
}

.color-field__label {
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  color: var(--color-text);
}

.color-field__control {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.color-field__picker-wrap {
  position: relative;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--color-border);
  flex-shrink: 0;

  @include md-up {
    width: 44px;
    height: 44px;
  }
}

.color-field__native {
  position: absolute;
  top: -10px;
  left: -10px;
  width: 60px;
  height: 60px;
  padding: 0;
  border: none;
  cursor: pointer;
  background: transparent;
}

.color-field__text {
  flex: 1;
  min-height: 40px;
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text);
  font-family: var(--font-mono);
  font-size: var(--text-base);
  text-transform: uppercase;
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);

  &:focus {
    outline: none;
    border-color: var(--color-brand);
    box-shadow: var(--shadow-focus);
  }

  @include md-up {
    min-height: 44px;
  }
}

.color-field__text--error {
  border-color: var(--color-danger);
  &:focus { box-shadow: 0 0 0 3px var(--color-danger-soft); }
}

.color-field__palette {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-top: var(--space-1);
}

.color-field__swatch {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid var(--color-surface);
  box-shadow: 0 0 0 1px var(--color-border);
  cursor: pointer;
  padding: 0;
  transition: transform var(--transition-fast);

  &:hover:not(:disabled) {
    transform: scale(1.15);
  }

  &--active {
    box-shadow: 0 0 0 2px var(--color-brand);
  }
}

.color-field__error {
  font-size: var(--text-sm);
  color: var(--color-danger);
}

.color-field__hint {
  font-size: var(--text-sm);
  color: var(--color-text-tertiary);
}

.color-field--disabled .color-field__label {
  color: var(--color-text-disabled);
}
</style>
