<template>
  <div class="base-input" :class="{ 'base-input--error': error, 'base-input--disabled': disabled }">
    <label v-if="label" :for="inputId" class="base-input__label">
      <span class="base-input__label-text">{{ label }}</span>
      <span v-if="required" class="base-input__required">*</span>
      <span v-if="hint" class="base-input__hint">{{ hint }}</span>
    </label>

    <input
      :id="inputId"
      ref="inputEl"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :required="required"
      :autocomplete="autocomplete"
      :min="min"
      :max="max"
      :minlength="minlength"
      :maxlength="maxlength"
      :step="step"
      class="base-input__field"
      v-bind="$attrs"
      @input="handleInput"
      @blur="$emit('blur', $event)"
      @focus="$emit('focus', $event)"
    />

    <p v-if="error" class="base-input__error">{{ error }}</p>
    <p v-else-if="description" class="base-input__description">{{ description }}</p>
  </div>
</template>

<script>
let uid = 0

export default {
  name: 'BaseInput',

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
    hint: {
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
    type: {
      type: String,
      default: 'text',
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
    autocomplete: {
      type: String,
      default: 'off',
    },
    min: {
      type: [String, Number],
      default: undefined,
    },
    max: {
      type: [String, Number],
      default: undefined,
    },
    minlength: {
      type: [String, Number],
      default: undefined,
    },
    maxlength: {
      type: [String, Number],
      default: undefined,
    },
    step: {
      type: [String, Number],
      default: undefined,
    },
    /**
     * При true возвращает number | null вместо string
     */
    number: {
      type: Boolean,
      default: false,
    },
  },

  emits: ['update:modelValue', 'blur', 'focus'],

  data() {
    uid += 1
    return {
      inputId: `base-input-${uid}`,
    }
  },

  methods: {
    handleInput(event) {
      const raw = event.target.value
      if (this.number) {
        if (raw === '') {
          this.$emit('update:modelValue', null)
        } else {
          const parsed = Number(raw)
          this.$emit('update:modelValue', Number.isNaN(parsed) ? null : parsed)
        }
      } else {
        this.$emit('update:modelValue', raw)
      }
    },

    focus() {
      this.$refs.inputEl?.focus()
    },
  },
}
</script>

<style scoped>
.base-input {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.base-input__label {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  color: var(--text-secondary);
  margin-bottom: var(--space-1);
}

.base-input__required {
  color: var(--danger-text);
  font-weight: var(--fw-bold);
}

.base-input__hint {
  font-weight: var(--fw-normal);
  font-size: var(--text-xs);
  color: var(--text-muted);
  margin-left: auto;
}

.base-input__field {
  width: 100%;
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
  font-family: inherit;
  background: var(--bg-input);
  border: 1px solid var(--border-input);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
  min-height: 40px;
}

.base-input__field::placeholder {
  color: var(--text-muted);
}

.base-input__field:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: var(--shadow-focus);
}

.base-input--error .base-input__field {
  border-color: var(--danger);
}

.base-input--error .base-input__field:focus {
  box-shadow: 0 0 0 3px var(--danger-trans);
}

.base-input--disabled .base-input__field {
  background: var(--bg-primary);
  cursor: not-allowed;
  opacity: 0.7;
}

.base-input__error {
  font-size: var(--text-xs);
  color: var(--danger-text);
  margin: 0;
}

.base-input__description {
  font-size: var(--text-xs);
  color: var(--text-muted);
  margin: 0;
}

@media (max-width: 640px) {
  .base-input__field {
    min-height: 44px;
    font-size: var(--text-base);
  }
}
</style>
