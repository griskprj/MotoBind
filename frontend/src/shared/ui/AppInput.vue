<template>
  <n-input
    :value="modelValue"
    :type="type"
    :placeholder="placeholder"
    :disabled="disabled"
    :status="error ? 'error' : undefined"
    :maxlength="maxlength"
    :minlength="minlength"
    @update:value="onUpdate"
    @blur="$emit('blur', $event)"
    @focus="$emit('focus', $event)"
  >
    <template v-if="label" #prefix>
      <span class="app-input__label">{{ label }}</span>
    </template>
  </n-input>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  modelValue?: string | number | null
  label?: string
  type?: string
  placeholder?: string
  disabled?: boolean
  error?: string
  maxlength?: number
  minlength?: number
}>(), {
  modelValue: '',
  type: 'text',
})

const emit = defineEmits<{
  'update:modelValue': [string | number | null]
  blur: [FocusEvent]
  focus: [FocusEvent]
}>()

function onUpdate(val: string) {
  emit('update:modelValue', val)
}
</script>
