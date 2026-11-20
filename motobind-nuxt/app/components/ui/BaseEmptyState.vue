<script setup lang="ts">
interface Props {
  title?: string
  description?: string
  compact?: boolean
}

withDefaults(defineProps<Props>(), {
  title: 'Пока ничего нет',
  description: undefined,
  compact: false,
})
</script>

<template>
  <div class="empty" :class="{ 'empty--compact': compact }">
    <div v-if="$slots.icon" class="empty__icon">
      <slot name="icon" />
    </div>
    <h3 v-if="title" class="empty__title">{{ title }}</h3>
    <p v-if="description" class="empty__description">{{ description }}</p>
    <div v-if="$slots.action" class="empty__action">
      <slot name="action" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: var(--space-10) var(--space-4);
  gap: var(--space-3);
}

.empty--compact {
  padding: var(--space-6) var(--space-4);
}

.empty__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  border-radius: var(--radius-full);
  background: var(--color-surface-secondary);
  color: var(--color-text-tertiary);
  margin-bottom: var(--space-1);

  :deep(svg) {
    width: 24px;
    height: 24px;
  }
}

.empty--compact .empty__icon {
  width: 40px;
  height: 40px;

  :deep(svg) {
    width: 20px;
    height: 20px;
  }
}

.empty__title {
  font-size: var(--text-lg);
  font-weight: var(--fw-semibold);
  color: var(--color-text);
}

.empty__description {
  max-width: 42ch;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.empty__action {
  margin-top: var(--space-2);
}
</style>
