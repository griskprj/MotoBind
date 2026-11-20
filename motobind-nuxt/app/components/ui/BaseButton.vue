<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  type?: 'button' | 'submit' | 'reset'
  disabled?: boolean
  loading?: boolean
  block?: boolean
  to?: string
  title?: string
  iconOnly?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  type: 'button',
  disabled: false,
  loading: false,
  block: false,
  to: undefined,
  title: undefined,
  iconOnly: false,
})

const isDisabled = computed(() => props.disabled || props.loading)

const tag = computed(() => (props.to ? resolveComponent('NuxtLink') : 'button'))
</script>

<template>
  <component
    :is="tag"
    :to="to"
    :type="to ? undefined : type"
    :disabled="to ? undefined : isDisabled"
    :aria-disabled="isDisabled || undefined"
    :aria-busy="loading || undefined"
    :title="title || undefined"
    class="btn"
    :class="[
      `btn--${variant}`,
      `btn--${size}`,
      {
        'btn--block': block,
        'btn--icon': iconOnly,
        'btn--loading': loading,
      },
    ]"
  >
    <BaseSpinner v-if="loading" size="sm" class="btn__spinner" />
    <span class="btn__content" :class="{ 'btn__content--hidden': loading }">
      <slot name="icon" />
      <slot />
    </span>
  </component>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  font-family: inherit;
  font-weight: var(--fw-semibold);
  line-height: 1;
  white-space: nowrap;
  cursor: pointer;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
  transition:
    background-color var(--transition-fast),
    border-color var(--transition-fast),
    color var(--transition-fast),
    box-shadow var(--transition-fast),
    opacity var(--transition-fast);

  &:focus-visible {
    outline: none;
    box-shadow: var(--shadow-focus);
  }

  &:disabled,
  &[aria-disabled='true'] {
    cursor: not-allowed;
    opacity: 0.55;
  }

  &:active:not(:disabled) {
    transform: translateY(1px);
  }
}

// ---------- Sizes ----------
.btn--sm {
  min-height: 32px;
  padding: 0 var(--space-3);
  font-size: var(--text-sm);
}

.btn--md {
  min-height: 40px;
  padding: 0 var(--space-4);
  font-size: var(--text-sm);

  @include md-up {
    min-height: 44px;
    font-size: var(--text-base);
  }
}

.btn--lg {
  min-height: 48px;
  padding: 0 var(--space-5);
  font-size: var(--text-base);
}

.btn--icon {
  padding: 0;
  aspect-ratio: 1 / 1;
  width: 40px;

  &.btn--sm { width: 32px; }
  &.btn--lg { width: 48px; }
}

// ---------- Variants ----------
.btn--primary {
  background: var(--color-brand);
  color: var(--color-text-inverse);

  &:hover:not(:disabled) {
    background: var(--color-brand-hover);
  }

  &:active:not(:disabled) {
    background: var(--color-brand-active);
  }
}

.btn--secondary {
  background: var(--color-surface);
  border-color: var(--color-border);
  color: var(--color-text);

  &:hover:not(:disabled) {
    background: var(--color-surface-hover);
    border-color: var(--color-border-dark);
  }

  &:active:not(:disabled) {
    background: var(--color-surface-active);
  }
}

.btn--ghost {
  background: transparent;
  color: var(--color-text-secondary);

  &:hover:not(:disabled) {
    background: var(--color-surface-hover);
    color: var(--color-text);
  }

  &:active:not(:disabled) {
    background: var(--color-surface-active);
  }
}

.btn--danger {
  background: var(--color-danger);
  color: #fff;

  &:hover:not(:disabled) {
    background: var(--color-danger-strong);
  }

  &:active:not(:disabled) {
    background: var(--color-danger-strong);
    filter: brightness(0.92);
  }
}

// ---------- Modifiers ----------
.btn--block {
  width: 100%;
}

.btn--loading {
  cursor: progress;
}

.btn__content {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  transition: opacity var(--transition-fast);

  &--hidden {
    opacity: 0;
  }
}

.btn__spinner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>
