<template>
  <button
    type="button"
    role="switch"
    :aria-checked="modelValue"
    :disabled="disabled"
    class="app-switch"
    :class="{ 'app-switch--on': modelValue, 'app-switch--disabled': disabled }"
    @click="toggle"
  >
    <span class="app-switch__thumb" />
  </button>
</template>

<script setup>
const props = defineProps({
  modelValue: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
})

const emit = defineEmits(['update:modelValue', 'update:value', 'change'])

function toggle() {
  if (props.disabled) return
  const next = !props.modelValue
  emit('update:modelValue', next)
  emit('update:value', next)
  emit('change', next)
}
</script>

<style scoped>
.app-switch {
  all: unset;
  box-sizing: border-box;

  position: relative;
  display: inline-flex;
  align-items: center;

  width: 44px;
  height: 24px;
  min-width: 44px;
  min-height: 24px;
  max-height: 24px;

  padding: 0;
  margin: 0;

  border-radius: 999px;
  background: var(--border-color);
  border: none;
  cursor: pointer;
  flex-shrink: 0;
  transition: background var(--transition-fast);
  vertical-align: middle;
}

.app-switch:focus-visible {
  outline: none;
  box-shadow: var(--shadow-focus);
}

.app-switch--on {
  background: var(--accent);
}

.app-switch--disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.app-switch__thumb {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25);
  transition: transform var(--transition-fast);
  pointer-events: none;
}

.app-switch--on .app-switch__thumb {
  transform: translateX(20px);
}
</style>
