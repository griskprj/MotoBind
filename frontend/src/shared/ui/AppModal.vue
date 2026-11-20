<template>
  <n-modal
    :show="isOpen"
    :mask-closable="closeOnOverlay && !loading"
    :close-on-esc="closeOnEscape && !loading"
    :style="{ maxWidth: modalWidth }"
    preset="card"
    :title="title"
    :bordered="false"
    @update:show="onUpdateShow"
  >
    <template v-if="icon || subtitle" #header>
      <div class="app-modal__header">
        <div v-if="icon" class="app-modal__icon" :class="`app-modal__icon--${variant}`">
          <i class="fa" :class="`fa-${icon}`" />
        </div>
        <div>
          <h2 class="app-modal__title">{{ title }}</h2>
          <p v-if="subtitle" class="app-modal__subtitle">{{ subtitle }}</p>
        </div>
      </div>
    </template>

    <slot />

    <template v-if="$slots.actions" #footer>
      <div class="app-modal__actions">
        <slot name="actions" />
      </div>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import { computed } from 'vue'

type Variant = 'default' | 'success' | 'warning' | 'danger' | 'info'
type Size = 'sm' | 'md' | 'lg' | 'xl'

const props = withDefaults(defineProps<{
  isOpen: boolean
  title: string
  subtitle?: string
  icon?: string
  variant?: Variant
  size?: Size
  loading?: boolean
  closeOnOverlay?: boolean
  closeOnEscape?: boolean
}>(), {
  variant: 'default',
  size: 'md',
  closeOnOverlay: true,
  closeOnEscape: true,
})

const emit = defineEmits<{ close: [] }>()

const modalWidth = computed(() => {
  switch (props.size) {
    case 'sm': return '400px'
    case 'lg': return '640px'
    case 'xl': return '840px'
    default: return '520px'
  }
})

function onUpdateShow(val: boolean) {
  if (!val && !props.loading) emit('close')
}
</script>
