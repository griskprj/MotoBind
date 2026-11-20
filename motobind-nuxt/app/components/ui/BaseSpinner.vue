<script setup lang="ts">
interface Props {
  size?: 'sm' | 'md' | 'lg'
  label?: string
}

withDefaults(defineProps<Props>(), {
  size: 'md',
  label: 'Загрузка',
})
</script>

<template>
  <span
    class="spinner"
    :class="`spinner--${size}`"
    role="status"
    :aria-label="label"
  >
    <span class="spinner__icon">
      <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <circle
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          stroke-width="3"
          stroke-opacity="0.25"
        />
        <path
          d="M22 12a10 10 0 0 0-10-10"
          stroke="currentColor"
          stroke-width="3"
          stroke-linecap="round"
        />
      </svg>
    </span>
  </span>
</template>

<style scoped lang="scss">
.spinner {
  display: inline-block;
  flex-shrink: 0;
  color: currentColor;

  svg {
    display: block;
    width: 100%;
    height: 100%;
  }
}

.spinner__icon {
  display: block;
  width: 100%;
  height: 100%;
  animation: spin 0.8s linear infinite;
}

.spinner--sm { width: 16px; height: 16px; }
.spinner--md { width: 24px; height: 24px; }
.spinner--lg { width: 40px; height: 40px; }

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (prefers-reduced-motion: reduce) {
  .spinner__icon { animation-duration: 1.5s; }
}
</style>
