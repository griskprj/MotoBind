<template>
  <Teleport to="body">
    <div class="toast-container" aria-live="polite" aria-atomic="true">
      <TransitionGroup name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="['toast', `toast--${toast.variant}`]"
          role="alert"
        >
          <i :class="['toast__icon', iconClass(toast.variant)]" aria-hidden="true" />
          <p class="toast__message">{{ toast.message }}</p>
          <button
            v-if="toast.dismissible"
            class="toast__close"
            aria-label="Закрыть"
            @click="remove(toast.id)"
          >
            <i class="fa fa-times" />
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script>
import { useToast } from '@/composables/useToast'

export default {
  name: 'ToastContainer',

  setup() {
    const { toasts, remove } = useToast()
    return { toasts, remove }
  },

  methods: {
    iconClass(variant) {
      return {
        info: 'fa fa-info-circle',
        success: 'fa fa-check-circle',
        warning: 'fa fa-exclamation-triangle',
        error: 'fa fa-times-circle',
      }[variant] || 'fa fa-info-circle'
    },
  },
}
</script>

<style>
.toast-container {
  position: fixed;
  top: var(--space-4);
  right: var(--space-4);
  z-index: var(--z-toast);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  max-width: 380px;
  pointer-events: none;
}

.toast {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-left: 4px solid var(--accent);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  color: var(--text-primary);
  font-size: var(--text-sm);
  pointer-events: auto;
  min-width: 280px;
}

.toast--info { border-left-color: var(--info); }
.toast--success { border-left-color: var(--success); }
.toast--warning { border-left-color: var(--warning); }
.toast--error { border-left-color: var(--danger); }

.toast__icon {
  font-size: var(--text-lg);
  flex-shrink: 0;
  margin-top: 1px;
}

.toast--info .toast__icon { color: var(--info-text); }
.toast--success .toast__icon { color: var(--success-text); }
.toast--warning .toast__icon { color: var(--warning-text); }
.toast--error .toast__icon { color: var(--danger-text); }

.toast__message {
  flex: 1;
  margin: 0;
  line-height: var(--leading-base);
  word-break: break-word;
}

.toast__close {
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  flex-shrink: 0;
  transition: background var(--transition-fast), color var(--transition-fast);
}

.toast__close:hover {
  background: var(--border-light);
  color: var(--text-primary);
}

/* Transitions */
.toast-enter-active,
.toast-leave-active {
  transition: all var(--transition-base);
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.toast-move {
  transition: transform var(--transition-base);
}

/* Mobile */
@media (max-width: 640px) {
  .toast-container {
    left: var(--space-3);
    right: var(--space-3);
    top: var(--space-3);
    max-width: none;
  }

  .toast {
    min-width: 0;
  }
}
</style>
