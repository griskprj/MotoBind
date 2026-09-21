<template>
  <component
    :is="tag"
    :type="tag === 'button' ? type : undefined"
    :disabled="disabled || loading"
    :class="[
      'base-btn',
      `base-btn--${variant}`,
      `base-btn--${size}`,
      {
        'base-btn--block': block,
        'base-btn--loading': loading,
        'base-btn--icon-only': iconOnly,
      },
    ]"
    v-bind="$attrs"
    @click="handleClick"
  >
    <span v-if="loading" class="base-btn__spinner" aria-hidden="true" />
    <i v-else-if="icon" :class="icon" class="base-btn__icon" aria-hidden="true" />
    <span v-if="!iconOnly && $slots.default" class="base-btn__label">
      <slot />
    </span>
    <slot v-else-if="!iconOnly" />
  </component>
</template>

<script>
export default {
  name: 'BaseButton',

  inheritAttrs: false,

  props: {
    /**
     * Визуальный вариант:
     * primary — основное действие (заполненный accent)
     * secondary — второстепенное (серый фон)
     * outline — с обводкой accent, прозрачный фон
     * ghost — без фона и обводки, только текст+иконка
     * danger — удаление/опасное действие
     * success — завершение/подтверждение
     * warning — предупреждение/отложенное действие
     */
    variant: {
      type: String,
      default: 'primary',
      validator: (v) =>
        ['primary', 'secondary', 'outline', 'ghost', 'danger', 'success', 'warning'].includes(v),
    },

    /**
     * Размер: sm (compact, для toolbar), md (обычная кнопка), lg (CTA)
     */
    size: {
      type: String,
      default: 'md',
      validator: (v) => ['sm', 'md', 'lg'].includes(v),
    },

    /**
     * Иконка слева: 'fa fa-plus', 'fa fa-trash' и т.д.
     * Если задана без slot — становится icon-only кнопкой.
     */
    icon: {
      type: String,
      default: '',
    },

    /**
     * Растянуть на всю ширину родителя
     */
    block: {
      type: Boolean,
      default: false,
    },

    /**
     * Состояние загрузки
     */
    loading: {
      type: Boolean,
      default: false,
    },

    disabled: {
      type: Boolean,
      default: false,
    },

    /**
     * HTML-тег: button (по умолчанию), a, router-link
     * Для ссылок передавать tag="router-link" и to="..." через $attrs
     */
    tag: {
      type: String,
      default: 'button',
    },

    type: {
      type: String,
      default: 'button',
      validator: (v) => ['button', 'submit', 'reset'].includes(v),
    },
  },

  emits: ['click'],

  computed: {
    iconOnly() {
      return !!this.icon && !this.$slots.default
    },
  },

  methods: {
    handleClick(event) {
      if (this.disabled || this.loading) {
        event.preventDefault()
        event.stopPropagation()
        return
      }
      this.$emit('click', event)
    },
  },
}
</script>

<style scoped>
.base-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  font-family: inherit;
  font-weight: var(--fw-medium);
  line-height: 1;
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  cursor: pointer;
  white-space: nowrap;
  transition: background-color var(--transition-fast), border-color var(--transition-fast),
    color var(--transition-fast), transform var(--transition-fast), box-shadow var(--transition-fast);
  user-select: none;
  position: relative;
  text-decoration: none;
}

.base-btn:focus-visible {
  outline: none;
  box-shadow: var(--shadow-focus);
}

.base-btn:disabled,
.base-btn--loading {
  opacity: 0.6;
  cursor: not-allowed;
}

.base-btn:not(:disabled):active {
  transform: translateY(1px);
}

/* ===== SIZES ===== */
.base-btn--sm {
  padding: var(--space-1) var(--space-3);
  font-size: var(--text-xs);
  min-height: 32px;
}

.base-btn--md {
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-sm);
  min-height: 40px;
}

.base-btn--lg {
  padding: var(--space-4) var(--space-5);
  font-size: var(--text-base);
  min-height: 48px;
}

/* ===== VARIANTS ===== */
.base-btn--primary {
  background: var(--accent);
  color: #fff;
}
.base-btn--primary:hover:not(:disabled) {
  background: var(--accent-hover);
}

.base-btn--secondary {
  background: var(--bg-secondary);
  border-color: var(--border-color);
  color: var(--text-primary);
}
.base-btn--secondary:hover:not(:disabled) {
  background: var(--bg-card-hover);
  border-color: var(--text-muted);
}

.base-btn--outline {
  background: transparent;
  border-color: var(--accent);
  color: var(--accent-text);
}
.base-btn--outline:hover:not(:disabled) {
  background: var(--accent-trans);
  border-color: var(--accent);
  color: var(--accent);
}

.base-btn--ghost {
  background: transparent;
  color: var(--text-secondary);
  border-color: transparent;
}
.base-btn--ghost:hover:not(:disabled) {
  background: var(--border-light);
  color: var(--text-primary);
}

.base-btn--danger {
  background: var(--danger);
  color: #fff;
}
.base-btn--danger:hover:not(:disabled) {
  background: var(--danger-hover);
}

.base-btn--success {
  background: var(--success);
  color: #fff;
}
.base-btn--success:hover:not(:disabled) {
  background: var(--success-hover);
}

.base-btn--warning {
  background: var(--warning);
  color: #fff;
}
.base-btn--warning:hover:not(:disabled) {
  background: var(--warning-hover);
}

/* ===== MODIFIERS ===== */
.base-btn--block {
  width: 100%;
}

.base-btn--icon-only.base-btn--sm { width: 32px; padding: 0; }
.base-btn--icon-only.base-btn--md { width: 40px; padding: 0; }
.base-btn--icon-only.base-btn--lg { width: 48px; padding: 0; }

/* ===== LOADING SPINNER ===== */
.base-btn__spinner {
  width: 16px;
  height: 16px;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  animation: base-btn-spin 0.7s linear infinite;
  flex-shrink: 0;
}

@keyframes base-btn-spin {
  to { transform: rotate(360deg); }
}

/* ===== ICON ===== */
.base-btn__icon {
  font-size: 1em;
  flex-shrink: 0;
}

.base-btn__label {
  display: inline-block;
}

/* ===== MOBILE ===== */
@media (max-width: 640px) {
  .base-btn--md {
    min-height: 44px;
  }
  .base-btn--sm {
    min-height: 36px;
  }
}
</style>
