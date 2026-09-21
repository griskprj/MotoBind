<template>
  <Transition name="base-modal-fade">
    <div v-if="isOpen" class="base-modal__overlay" @click.self="onOverlayClick">
      <div
        :class="['base-modal', `base-modal--${size}`, { 'base-modal--loading': loading }]"
        role="dialog"
        aria-modal="true"
      >
        <!-- HEADER -->
        <header class="base-modal__header">
          <div class="base-modal__header-left">
            <div v-if="icon" class="base-modal__icon" :class="`base-modal__icon--${variant}`">
              <i class="fa" :class="`fa-${icon}`" aria-hidden="true" />
            </div>
            <div class="base-modal__header-text">
              <h2 class="base-modal__title">{{ title }}</h2>
              <p v-if="subtitle" class="base-modal__subtitle">{{ subtitle }}</p>
            </div>
          </div>
          <slot name="header-extra" />
          <button
            v-if="!loading && !hideClose"
            class="base-modal__close"
            aria-label="Закрыть"
            @click="close"
          >
            <i class="fa fa-times" />
          </button>
        </header>

        <!-- BODY -->
        <div ref="modalBody" class="base-modal__body">
          <slot />
        </div>

        <!-- FOOTER -->
        <footer v-if="$slots.actions" class="base-modal__footer">
          <slot name="actions" />
        </footer>
      </div>
    </div>
  </Transition>
</template>

<script>
export default {
  name: 'BaseModal',

  props: {
    isOpen: {
      type: Boolean,
      required: true,
      default: false,
    },
    title: {
      type: String,
      required: true,
    },
    subtitle: {
      type: String,
      default: '',
    },
    /**
     * Имя иконки Font Awesome без префикса fa-:
     * 'wrench', 'user', 'trash', 'check-circle'
     */
    icon: {
      type: String,
      default: '',
    },
    /**
     * Цветовая схема иконки и акцентов:
     * 'default' (accent), 'success', 'warning', 'danger', 'info'
     */
    variant: {
      type: String,
      default: 'default',
      validator: (v) => ['default', 'success', 'warning', 'danger', 'info'].includes(v),
    },
    size: {
      type: String,
      default: 'md',
      validator: (v) => ['sm', 'md', 'lg', 'xl'].includes(v),
    },
    /**
     * Блокирует закрытие (overlay/Escape/крестик)
     */
    loading: {
      type: Boolean,
      default: false,
    },
    /**
     * Скрывает крестик (для модалок, где закрытие только через кнопку действия)
     */
    hideClose: {
      type: Boolean,
      default: false,
    },
    closeOnOverlay: {
      type: Boolean,
      default: true,
    },
    closeOnEscape: {
      type: Boolean,
      default: true,
    },
  },

  emits: ['close'],

  mounted() {
    document.addEventListener('keydown', this.handleEscape)
  },

  beforeUnmount() {
    document.removeEventListener('keydown', this.handleEscape)
    document.body.style.overflow = ''
  },

  watch: {
    isOpen: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          document.body.style.overflow = 'hidden'
          this.$nextTick(() => {
            if (this.$refs.modalBody) this.$refs.modalBody.scrollTop = 0
          })
        } else {
          document.body.style.overflow = ''
        }
      },
    },
  },

  methods: {
    close() {
      if (this.loading) return
      this.$emit('close')
    },

    onOverlayClick() {
      if (!this.closeOnOverlay || this.loading) return
      this.close()
    },

    handleEscape(event) {
      if (!this.isOpen || !this.closeOnEscape || this.loading) return
      if (event.key === 'Escape') {
        this.close()
      }
    },
  },
}
</script>

<style scoped>
/* ===== TRANSITIONS ===== */
.base-modal-fade-enter-active,
.base-modal-fade-leave-active {
  transition: opacity var(--transition-base);
}

.base-modal-fade-enter-active .base-modal,
.base-modal-fade-leave-active .base-modal {
  transition: transform var(--transition-bounce), opacity var(--transition-base);
}

.base-modal-fade-enter-from,
.base-modal-fade-leave-to {
  opacity: 0;
}

.base-modal-fade-enter-from .base-modal,
.base-modal-fade-leave-to .base-modal {
  transform: scale(0.95) translateY(20px);
  opacity: 0;
}

/* ===== OVERLAY ===== */
.base-modal__overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: var(--z-modal);
  padding: var(--space-4);
}

/* ===== CONTAINER ===== */
.base-modal {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  width: 100%;
  max-width: 520px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-light);
  overflow: hidden;
  position: relative;
}

.base-modal--sm { max-width: 400px; }
.base-modal--md { max-width: 520px; }
.base-modal--lg { max-width: 640px; }
.base-modal--xl { max-width: 840px; }

/* ===== HEADER ===== */
.base-modal__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-4);
  padding: var(--space-5) var(--space-5) var(--space-4);
  border-bottom: 1px solid var(--border-light);
  flex-shrink: 0;
}

.base-modal__header-left {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  min-width: 0;
  flex: 1;
}

.base-modal__icon {
  width: 44px;
  height: 44px;
  min-width: 44px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-xl);
  flex-shrink: 0;
  background: var(--accent-trans);
  color: var(--accent-text);
}

.base-modal__icon--success { background: var(--success-trans); color: var(--success-text); }
.base-modal__icon--warning { background: var(--warning-trans); color: var(--warning-text); }
.base-modal__icon--danger { background: var(--danger-trans); color: var(--danger-text); }
.base-modal__icon--info { background: var(--info-trans); color: var(--info-text); }

.base-modal__header-text {
  min-width: 0;
  flex: 1;
}

.base-modal__title {
  font-size: var(--text-xl);
  font-weight: var(--fw-bold);
  margin: 0;
  color: var(--text-primary);
  line-height: var(--leading-tight);
}

.base-modal__subtitle {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin: var(--space-1) 0 0;
  line-height: var(--leading-base);
}

.base-modal__close {
  width: 36px;
  height: 36px;
  min-width: 36px;
  border-radius: 50%;
  border: none;
  background: var(--bg-secondary);
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-base);
  transition: all var(--transition-fast);
  flex-shrink: 0;
  margin-top: 2px;
}

.base-modal__close:hover {
  background: var(--danger-trans);
  color: var(--danger-text);
}

/* ===== BODY ===== */
.base-modal__body {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-5);
}

.base-modal__body::-webkit-scrollbar {
  width: 4px;
}

.base-modal__body::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: var(--radius-sm);
}

/* ===== FOOTER ===== */
.base-modal__footer {
  padding: var(--space-4) var(--space-5);
  flex-shrink: 0;
  border-top: 1px solid var(--border-light);
  background: var(--bg-card);
}

/* ===== MOBILE ===== */
@media (max-width: 640px) {
  .base-modal__overlay {
    padding: var(--space-2);
    align-items: flex-end;
  }

  .base-modal {
    max-height: 94vh;
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
    max-width: 100%;
  }

  .base-modal--sm,
  .base-modal--md,
  .base-modal--lg,
  .base-modal--xl {
    max-width: 100%;
  }

  .base-modal__header {
    padding: var(--space-4) var(--space-4) var(--space-3);
  }

  .base-modal__icon {
    width: 38px;
    height: 38px;
    min-width: 38px;
    font-size: var(--text-lg);
  }

  .base-modal__title {
    font-size: var(--text-lg);
  }

  .base-modal__body {
    padding: var(--space-4);
  }

  .base-modal__footer {
    padding: var(--space-3) var(--space-4);
  }
}
</style>
