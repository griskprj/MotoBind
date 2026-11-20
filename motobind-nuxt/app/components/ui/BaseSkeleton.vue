<script setup lang="ts">
interface Props {
  width?: string
  height?: string
  circle?: boolean
  rounded?: boolean
}

withDefaults(defineProps<Props>(), {
  width: '100%',
  height: '1em',
  circle: false,
  rounded: false,
})
</script>

<template>
  <span
    class="skeleton"
    :class="{
      'skeleton--circle': circle,
      'skeleton--rounded': rounded,
    }"
    :style="{ width, height }"
    aria-hidden="true"
  />
</template>

<style scoped lang="scss">
.skeleton {
  display: block;
  background: linear-gradient(
    90deg,
    var(--color-surface-secondary) 0%,
    var(--color-surface-hover) 50%,
    var(--color-surface-secondary) 100%
  );
  background-size: 200% 100%;
  border-radius: var(--radius-sm);
  animation: shimmer 1.4s ease-in-out infinite;
}

.skeleton--circle {
  border-radius: 50%;
}

.skeleton--rounded {
  border-radius: var(--radius-md);
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton {
    animation: none;
    background: var(--color-surface-secondary);
  }
}
</style>
