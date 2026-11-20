<script setup lang="ts">
interface Props {
  padding?: 'none' | 'sm' | 'md' | 'lg'
  hoverable?: boolean
  clickable?: boolean
  as?: string
  to?: string
}

const props = withDefaults(defineProps<Props>(), {
  padding: 'md',
  hoverable: false,
  clickable: false,
  as: undefined,
  to: undefined,
})

const tag = computed(() => {
  if (props.to) return resolveComponent('NuxtLink')
  return props.as ?? 'div'
})
</script>

<template>
  <component
    :is="tag"
    :to="to"
    class="card"
    :class="[
      `card--pad-${padding}`,
      {
        'card--hoverable': hoverable,
        'card--clickable': clickable || !!to,
      },
    ]"
  >
    <slot />
  </component>
</template>

<style scoped lang="scss">
.card {
  display: block;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  transition:
    border-color var(--transition-fast),
    box-shadow var(--transition-fast),
    transform var(--transition-fast);
}

.card--pad-none { padding: 0; }
.card--pad-sm { padding: var(--space-3); }
.card--pad-md { padding: var(--space-4); }
.card--pad-lg { padding: var(--space-5); }

.card--hoverable:hover {
  border-color: var(--color-border-dark);
  box-shadow: var(--shadow-md);
}

.card--clickable {
  cursor: pointer;

  &:focus-visible {
    outline: none;
    box-shadow: var(--shadow-focus);
  }

  &:active {
    transform: scale(0.997);
  }
}
</style>
