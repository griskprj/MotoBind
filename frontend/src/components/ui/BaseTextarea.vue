<template>
  <div class="base-textarea" :class="{ 'base-textarea--error': error }">
    <label v-if="label" :for="inputId" class="base-textarea__label">
      {{ label }}
      <span v-if="required" class="base-textarea__required">*</span>
    </label>

    <textarea
      :id="inputId"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :required="required"
      :rows="rows"
      :maxlength="maxlength"
      class="base-textarea__field"
      v-bind="$attrs"
      @input="$emit('update:modelValue', $event.target.value)"
      @blur="$emit('blur', $event)"
      @focus="$emit('focus', $event)"
    />

    <div class="base-textarea__footer">
      <p v-if="error" class="base-textarea__error">{{ error }}</p>
      <p v-else-if="description" class="base-textarea__description">{{ description }}</p>
      <span v-if="maxlength && showCounter" class="base-textarea__counter">
        {{ (modelValue || '').length }} / {{ maxlength }}
      </span>
    </div>
  </div>
</template>

<script>
let uid = 0

export default {
  name: 'BaseTextarea',

  inheritAttrs: false,

  props: {
    modelValue: {
      type: String,
      default: '',
    },
    label: {
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
    placeholder: {
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
    rows: {
      type: [String, Number],
      default: 3,
    },
    maxlength: {
      type: [String, Number],
      default: undefined,
    },
    showCounter: {
      type: Boolean,
      default: true,
    },
  },

  emits: ['update:modelValue', 'blur', 'focus'],

  data() {
    uid += 1
    return {
      inputId: `base-textarea-${uid}`,
    }
  },
}
</script>

<style scoped>
.base-textarea {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.base-textarea__label {
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  color: var(--text-secondary);
}

.base-textarea__required {
  color: var(--danger-text);
  font-weight: var(--fw-bold);
  margin-left: 2px;
}

.base-textarea__field {
  width: 100%;
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
  font-family: inherit;
  background: var(--bg-input);
  border: 1px solid var(--border-input);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  resize: vertical;
  min-height: 80px;
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.base-textarea__field::placeholder {
  color: var(--text-muted);
}

.base-textarea__field:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: var(--shadow-focus);
}

.base-textarea--error .base-textarea__field {
  border-color: var(--danger);
}

.base-textarea__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-2);
  min-height: 16px;
}

.base-textarea__error {
  font-size: var(--text-xs);
  color: var(--danger-text);
  margin: 0;
}

.base-textarea__description {
  font-size: var(--text-xs);
  color: var(--text-muted);
  margin: 0;
}

.base-textarea__counter {
  font-size: var(--text-xs);
  color: var(--text-muted);
  margin-left: auto;
}
</style>
