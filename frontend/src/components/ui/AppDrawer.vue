<template>
  <Teleport to="body">
    <Transition name="drawer-fade">
      <div
        v-if="modelValue"
        class="app-drawer__overlay"
        @click.self="close"
      >
        <Transition name="drawer-slide">
          <aside
            v-if="modelValue"
            class="app-drawer"
            :class="`app-drawer--${placement}`"
            :style="drawerStyle"
            role="dialog"
            aria-modal="true"
          >
            <slot />
          </aside>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed, watch, onBeforeUnmount } from 'vue'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  placement: {
    type: String,
    default: 'left',
    validator: (v) => ['left', 'right', 'top', 'bottom'].includes(v),
  },
  width: { type: [String, Number], default: 280 },
  height: { type: [String, Number], default: 280 },
  closeOnOverlay: { type: Boolean, default: true },
  closeOnEscape: { type: Boolean, default: true },
})

const emit = defineEmits(['update:modelValue', 'close'])

const drawerStyle = computed(() => {
  if (props.placement === 'left' || props.placement === 'right') {
    return { width: typeof props.width === 'number' ? `${props.width}px` : props.width }
  }
  return { height: typeof props.height === 'number' ? `${props.height}px` : props.height }
})

function close() {
  emit('update:modelValue', false)
  emit('close')
}

function onKeydown(e) {
  if (e.key === 'Escape' && props.closeOnEscape) close()
}

watch(
  () => props.modelValue,
  (open) => {
    if (open) {
      document.body.style.overflow = 'hidden'
      document.addEventListener('keydown', onKeydown)
    } else {
      document.body.style.overflow = ''
      document.removeEventListener('keydown', onKeydown)
    }
  },
)

onBeforeUnmount(() => {
  document.body.style.overflow = ''
  document.removeEventListener('keydown', onKeydown)
})
</script>

<style scoped>
.app-drawer__overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  z-index: var(--z-modal);
}

.app-drawer {
  position: fixed;
  background: var(--bg-primary);
  box-shadow: var(--shadow-lg);
  overflow-y: auto;
  max-width: 90vw;
  max-height: 100dvh;
}

.app-drawer--left {
  top: 0;
  left: 0;
  height: 100vh;
}
.app-drawer--right {
  top: 0;
  right: 0;
  height: 100vh;
}
.app-drawer--top {
  top: 0;
  left: 0;
  right: 0;
}
.app-drawer--bottom {
  bottom: 0;
  left: 0;
  right: 0;
}

/* Transitions */
.drawer-fade-enter-active,
.drawer-fade-leave-active {
  transition: opacity var(--transition-base);
}
.drawer-fade-enter-from,
.drawer-fade-leave-to {
  opacity: 0;
}

.drawer-slide-enter-active,
.drawer-slide-leave-active {
  transition: transform var(--transition-base);
}
.drawer-slide-enter-from,
.drawer-slide-leave-to {
  /* Сдвиг зависит от placement */
}
.app-drawer--left.drawer-slide-enter-from,
.app-drawer--left.drawer-slide-leave-to {
  transform: translateX(-100%);
}
.app-drawer--right.drawer-slide-enter-from,
.app-drawer--right.drawer-slide-leave-to {
  transform: translateX(100%);
}
.app-drawer--top.drawer-slide-enter-from,
.app-drawer--top.drawer-slide-leave-to {
  transform: translateY(-100%);
}
.app-drawer--bottom.drawer-slide-enter-from,
.app-drawer--bottom.drawer-slide-leave-to {
  transform: translateY(100%);
}
</style>
