<script setup lang="ts">
import { getCategoryMeta } from '~/utils/constants/maintenance'

const props = defineProps<{
  category: string
}>()

const meta = computed(() => getCategoryMeta(props.category))
</script>

<template>
  <span
    class="category-badge"
    :style="{
      '--badge-color': meta.color,
      '--badge-bg': `color-mix(in srgb, ${meta.color} 15%, transparent)`
    }"
  >
    <i :class="meta.icon" class="badge-icon"></i>
    {{ meta.label }}
  </span>
</template>

<style scoped lang="scss">
.category-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  padding: 2px 8px;
  font-size: var(--text-xs);
  font-weight: var(--fw-medium);
  color: var(--badge-color);
  background: var(--badge-bg);
  border-radius: var(--radius-full);
  white-space: nowrap;
}

.badge-icon {
  font-size: 0.85em;
}
</style>
