<script setup lang="ts">
interface Props {
  title?: string
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  title: undefined,
  size: 'md',
})

const emit = defineEmits<{ close: [] }>()

const modalRef = ref<HTMLElement | null>(null)

onMounted(() => {
  document.body.style.overflow = 'hidden'
})
onBeforeUnmount(() => {
  document.body.style.overflow = ''
})

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') emit('close')
}

onMounted(() => {
  window.addEventListener('keydown', onKeydown)
})
onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKeydown)
})

function onOverlayClick(e: MouseEvent) {
  if (e.target === e.currentTarget) {
    emit('close')
  }
}
</script>

<template>
  <Teleport to="body">
    <div class="modal-overlay" @click="onOverlayClick">
      <div
        ref="modalRef"
        class="modal-content"
        :class="`modal-content--${size}`"
        role="dialog"
        aria-modal="true"
      >
        <header class="modal-header">
          <h3 v-if="title" class="modal-title">{{ title }}</h3>
          <button class="modal-close" type="button" @click="emit('close')" aria-label="Закрыть">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </header>

        <div class="modal-body">
          <slot />
        </div>

        <footer v-if="$slots.footer" class="modal-footer">
          <slot name="footer" />
        </footer>
      </div>
    </div>
  </Teleport>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: var(--z-modal);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(2px);
  padding: 0;

  @include md-up {
    align-items: center;
    padding: var(--space-4);
  }
}

.modal-content {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-height: 90dvh;
  background: var(--color-surface);
  border-radius: var(--radius-xl) var(--radius-xl) 0 0;
  box-shadow: var(--shadow-lg);
  animation: slideUp var(--transition-base) ease-out;

  @include md-up {
    border-radius: var(--radius-xl);
    max-height: 85dvh;
    animation: fadeIn var(--transition-base) ease-out;
  }

  &--sm { @include md-up { max-width: 400px; } }
  &--md { @include md-up { max-width: 560px; } }
  &--lg { @include md-up { max-width: 800px; } }
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4);
  border-bottom: 1px solid var(--color-border-light);
  flex-shrink: 0;
}

.modal-title {
  font-size: var(--text-lg);
  font-weight: var(--fw-semibold);
  color: var(--color-text);
  line-height: var(--leading-tight);
}

.modal-close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  color: var(--color-text-secondary);
  transition: background var(--transition-fast), color var(--transition-fast);

  &:hover {
    background: var(--color-surface-hover);
    color: var(--color-text);
  }
}

.modal-body {
  padding: var(--space-4);
  overflow-y: auto;
  flex: 1;

  @include md-up {
    padding: var(--space-5);
  }
}

.modal-footer {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: flex-end;
  gap: var(--space-2);
  padding: var(--space-4);
  border-top: 1px solid var(--color-border-light);
  background: var(--color-surface-secondary);
  border-radius: 0 0 var(--radius-xl) var(--radius-xl);
  flex-shrink: 0;

  @media (max-width: 639px) {
    padding: var(--space-3);
  }
}

@keyframes slideUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

@media (prefers-reduced-motion: reduce) {
  .modal-content {
    animation: none;
  }
}
</style>
