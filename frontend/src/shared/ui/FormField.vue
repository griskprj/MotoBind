<template>
  <div class="form-field" :class="{ 'has-error': !!error }">
    <label v-if="label" :for="id" class="form-label">
      {{ label }}
      <span v-if="required" class="required">*</span>
    </label>

    <div class="form-control">
      <slot
        :id="id"
        :invalid="!!error"
        :on-blur="onBlur"
      />
    </div>

    <transition name="fade">
      <p v-if="error" class="form-error">{{ error }}</p>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  label?: string
  error?: string | null
  required?: boolean
  id?: string
}>()

const emit = defineEmits<{ blur: [] }>()

const id = computed(() => props.id || `field-${Math.random().toString(36).slice(2, 9)}`)

function onBlur() {
  emit('blur')
}
</script>

<style scoped>
.form-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 14px;
}

.form-label {
  font-size: 0.85rem;
  font-weight: var(--fw-semibold);
  color: var(--text-secondary);
}

.required {
  color: var(--danger-text);
  margin-left: 2px;
}

.form-control :deep(input),
.form-control :deep(select),
.form-control :deep(textarea) {
  width: 100%;
  padding: 0.6rem 0.8rem;
  border-radius: 10px;
  border: 2px solid var(--border-color);
  background-color: var(--bg-input);
  color: var(--text-primary);
  font-size: 0.95rem;
  font-family: inherit;
  transition: border-color 0.2s, box-shadow 0.2s;
  box-sizing: border-box;
  min-height: 44px;
}

.form-control :deep(input:focus),
.form-control :deep(select:focus),
.form-control :deep(textarea:focus) {
  border-color: var(--accent);
  outline: none;
  box-shadow: var(--shadow-focus);
}

.form-field.has-error .form-control :deep(input),
.form-field.has-error .form-control :deep(select),
.form-field.has-error .form-control :deep(textarea) {
  border-color: var(--danger);
}

.form-error {
  font-size: 0.8rem;
  color: var(--danger-text);
  margin: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
