<template>
  <div class="base-select" :class="{ 'base-select--error': error, 'base-select--disabled': disabled }">
    <label v-if="label" :for="inputId" class="base-select__label">
      {{ label }}
      <span v-if="required" class="base-select__required">*</span>
    </label>

    <div class="base-select__wrapper">
      <select
        :id="inputId"
        :value="modelValue"
        :disabled="disabled"
        :required="required"
        class="base-select__field"
        v-bind="$attrs"
        @change="handleChange"
        @blur="$emit('blur', $event)"
        @focus="$emit('focus', $event)"
      >
        <option v-if="placeholder" :value="''" disabled>{{ placeholder }}</option>
        <slot />
      </select>
      <i class="fa fa-chevron-down base-select__arrow" aria-hidden="true" />
    </div>

    <p v-if="error" class="base-select__error">{{ error }}</p>
    <p v-else-if="description" class="base-select__description">{{ description }}</p>
  </div>
</template>

<script>
let uid = 0

export default {
  name: 'BaseSelect',

  inheritAttrs: false,

  props: {
    modelValue: {
      type: [String, Number, null],
      default: '',
    },
    label: {
      type: String,
      default: '',
    },
    placeholder: {
      type: String,
      default: '',
    },
    description: {
      type: String,
      default: '',
    },
    error: {
      type: String,
      default: '',
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    required: {
      type: Boolean,
      default: false,
    },
  },

  emits: ['update:modelValue', 'change', 'blur', 'focus'],

  data() {
    uid += 1
    return {
      inputId: `base-select-${uid}`,
    }
  },

  methods: {
    handleChange(event) {
      this.$emit('update:modelValue', event.target.value)
      this.$emit('change', event)
    },
  },
}
</script>

<style scoped>
.base-select {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.base-select__label {
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  color: var(--text-secondary);
  margin-bottom: var(--space-1);
}

.base-select__required {
  color: var(--danger-text);
  font-weight: var(--fw-bold);
  margin-left: 2px;
}

.base-select__wrapper {
  position: relative;
}

.base-select__field {
  width: 100%;
  padding: var(--space-2) var(--space-6) var(--space-2) var(--space-3);
  font-size: var(--text-sm);
  font-family: inherit;
  background: var(--bg-input);
  border: 1px solid var(--border-input);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  appearance: none;
  cursor: pointer;
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
  min-height: 40px;
}

.base-select__field:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: var(--shadow-focus);
}

.base-select--error .base-select__field {
  border-color: var(--danger);
}

.base-select--disabled .base-select__field {
  background: var(--bg-primary);
  cursor: not-allowed;
  opacity: 0.7;
}

.base-select__arrow {
  position: absolute;
  right: var(--space-3);
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  font-size: var(--text-xs);
  pointer-events: none;
}

.base-select__error {
  font-size: var(--text-xs);
  color: var(--danger-text);
  margin: 0;
}

.base-select__description {
  font-size: var(--text-xs);
  color: var(--text-muted);
  margin: 0;
}

@media (max-width: 640px) {
  .base-select__field {
    min-height: 44px;
    font-size: var(--text-base);
  }
}
</style>
