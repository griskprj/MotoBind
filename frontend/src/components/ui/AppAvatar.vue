<template>
  <div
    class="app-avatar"
    :class="[`app-avatar--${size}`, { 'app-avatar--round': round }]"
    :style="sizeStyle"
  >
    <img
      v-if="src"
      :src="src"
      :alt="alt"
      @error="onError"
    >
    <i v-else class="fa fa-user app-avatar__placeholder" />
    <slot />
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({
  src: { type: String, default: '' },
  alt: { type: String, default: '' },
  size: { type: [Number, String], default: 40 },  // number (px) или 'small'|'medium'|'large'
  round: { type: Boolean, default: false },
})

const hasError = ref(false)

watch(() => props.src, () => { hasError.value = false })

const sizePx = computed(() => {
  if (typeof props.size === 'number') return props.size
  return { small: 32, medium: 40, large: 64 }[props.size] || 40
})

const sizeStyle = computed(() => ({
  width: sizePx.value + 'px',
  height: sizePx.value + 'px',
  fontSize: Math.round(sizePx.value * 0.45) + 'px',
}))

function onError() {
  hasError.value = true
}
</script>

<style scoped>
.app-avatar {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--accent-trans);
  color: var(--accent-text);
  overflow: hidden;
  border-radius: var(--radius-md);
  flex-shrink: 0;
}

.app-avatar--round {
  border-radius: 50%;
}

.app-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.app-avatar__placeholder {
  opacity: 0.7;
}
</style>
