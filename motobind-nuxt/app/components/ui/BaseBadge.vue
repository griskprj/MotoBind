<script setup lang="ts">
interface Props {
  variant?: 'neutral' | 'brand' | 'success' | 'warning' | 'danger' | 'info'
  size?: 'sm' | 'md'
  dot?: boolean
}

withDefaults(defineProps<Props>(), {
  variant: 'neutral',
  size: 'md',
  dot: false,
})
</script>

<template>
  <span class="badge" :class="[`badge--${variant}`, `badge--${size}`]">
    <span v-if="dot" class="badge__dot" aria-hidden="true" />
    <slot />
  </span>
</template>

<style scoped lang="scss">
.badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  border-radius: var(--radius-full);
  font-weight: var(--fw-medium);
  line-height: 1;
  white-space: nowrap;
  border: 1px solid transparent;
}

.badge--sm {
  padding: 2px var(--space-2);
  font-size: var(--text-xs);
}

.badge--md {
  padding: 4px var(--space-3);
  font-size: var(--text-sm);
}

// ---------- Variants ----------
.badge--neutral {
  background: var(--color-surface-secondary);
  color: var(--color-text-secondary);
  border-color: var(--color-border-light);
}

.badge--brand {
  background: var(--color-brand-soft);
  color: var(--color-brand-active);
  border-color: transparent;
}

.badge--success {
  background: var(--color-success-soft);
  color: var(--color-success-strong);
}

.badge--warning {
  background: var(--color-warning-soft);
  color: var(--color-warning-strong);
}

.badge--danger {
  background: var(--color-danger-soft);
  color: var(--color-danger-strong);
}

.badge--info {
  background: var(--color-info-soft);
  color: var(--color-info-strong);
}

// ---------- Dot ----------
.badge__dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
  flex-shrink: 0;
}
</style>
