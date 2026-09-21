<template>
  <div class="base-empty">
    <div class="base-empty__icon" :class="`base-empty__icon--${variant}`">
      <i :class="icon" aria-hidden="true" />
    </div>
    <h3 class="base-empty__title">{{ title }}</h3>
    <p v-if="description" class="base-empty__description">{{ description }}</p>
    <div v-if="$slots.default" class="base-empty__actions">
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  name: 'BaseEmptyState',

  props: {
    icon: {
      type: String,
      default: 'fa fa-inbox',
    },
    title: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      default: '',
    },
    variant: {
      type: String,
      default: 'default',
      validator: (v) => ['default', 'warning', 'danger'].includes(v),
    },
  },
}
</script>

<style scoped>
.base-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-10) var(--space-5);
  background: var(--bg-secondary);
  border: 2px dashed var(--border-color);
  border-radius: var(--radius-xl);
  text-align: center;
}

.base-empty__icon {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: var(--accent-trans);
  color: var(--accent-text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-3xl);
  margin-bottom: var(--space-4);
}

.base-empty__icon--warning {
  background: var(--warning-trans);
  color: var(--warning-text);
}

.base-empty__icon--danger {
  background: var(--danger-trans);
  color: var(--danger-text);
}

.base-empty__title {
  font-size: var(--text-xl);
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
  margin: 0 0 var(--space-2);
}

.base-empty__description {
  font-size: var(--text-sm);
  color: var(--text-muted);
  margin: 0 0 var(--space-5);
  max-width: 400px;
  line-height: var(--leading-base);
}

.base-empty__actions {
  display: flex;
  gap: var(--space-3);
  flex-wrap: wrap;
  justify-content: center;
}

@media (max-width: 640px) {
  .base-empty {
    padding: var(--space-6) var(--space-4);
  }

  .base-empty__icon {
    width: 60px;
    height: 60px;
    font-size: var(--text-2xl);
  }

  .base-empty__title {
    font-size: var(--text-lg);
  }

  .base-empty__actions {
    width: 100%;
    flex-direction: column;
  }
}
</style>
