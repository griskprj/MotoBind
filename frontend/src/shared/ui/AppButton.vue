<template>
  <n-button
    :type="naiveType"
    :size="size"
    :disabled="disabled"
    :loading="loading"
    :block="block"
    :quaternary="variant === 'ghost'"
    :secondary="variant === 'secondary'"
    :tertiary="variant === 'outline'"
    @click="onClick"
  >
    <template v-if="icon" #icon>
      <i :class="icon" />
    </template>
    <slot />
  </n-button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

type Variant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' | 'success' | 'warning'
type Size = 'sm' | 'md' | 'lg'

const props = withDefaults(defineProps<{
  variant?: Variant
  size?: Size
  icon?: string
  block?: boolean
  loading?: boolean
  disabled?: boolean
}>(), {
  variant: 'primary',
  size: 'md',
})

const emit = defineEmits<{ click: [MouseEvent] }>()

const naiveType = computed(() => {
  switch (props.variant) {
    case 'danger': return 'error'
    case 'success': return 'success'
    case 'warning': return 'warning'
    case 'secondary': return 'default'
    case 'outline': return 'primary'
    case 'ghost': return 'default'
    default: return 'primary'
  }
})

function onClick(e: MouseEvent) {
  emit('click', e)
}
</script>
