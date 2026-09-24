<template>
  <div :class="['base-card', { 'base-card--flat': flat, 'base-card--interactive': interactive }]">
    <header v-if="title || $slots.header || $slots.actions" class="base-card__header">
      <div class="base-card__header-left">
        <i v-if="icon" :class="[icon, 'base-card__icon']" aria-hidden="true" />
        <div class="base-card__header-text">
          <h3 v-if="title" class="base-card__title">{{ title }}</h3>
          <p v-if="subtitle" class="base-card__subtitle">{{ subtitle }}</p>
        </div>
        <slot name="header" />
      </div>
      <div v-if="$slots.actions" class="base-card__actions">
        <slot name="actions" />
      </div>
    </header>

    <div class="base-card__body">
      <slot />
    </div>

    <footer v-if="$slots.footer" class="base-card__footer">
      <slot name="footer" />
    </footer>
  </div>
</template>

<script>
export default {
  name: 'BaseCard',

  props: {
    title: { type: String, default: '' },
    subtitle: { type: String, default: '' },
    icon: { type: String, default: '' },
    flat: { type: Boolean, default: false },
    interactive: { type: Boolean, default: false },
  },
}
</script>

<style scoped>
.base-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: border-color var(--transition-fast), background var(--transition-fast);
}

.base-card--flat {
  background: transparent;
  border-color: transparent;
}

.base-card--interactive {
  cursor: pointer;
}

.base-card--interactive:hover {
  border-color: var(--accent);
  background: var(--bg-card-hover);
}

.base-card__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--border-light);
}

.base-card--flat .base-card__header {
  border-bottom: none;
  padding-left: 0;
  padding-right: 0;
}

.base-card__header-left {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  min-width: 0;
  flex: 1;
}

.base-card__icon {
  font-size: var(--text-lg);
  color: var(--accent-text);
  flex-shrink: 0;
  margin-top: 2px;
}

.base-card__header-text {
  min-width: 0;
  flex: 1;
}

.base-card__title {
  font-size: var(--text-base);
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
  margin: 0;
  line-height: var(--leading-tight);
}

.base-card__subtitle {
  font-size: var(--text-sm);
  color: var(--text-muted);
  margin: var(--space-1) 0 0;
  line-height: var(--leading-base);
}

.base-card__actions {
  display: flex;
  gap: var(--space-2);
  flex-shrink: 0;
}

.base-card__body {
  padding: var(--space-5);
}

.base-card--flat .base-card__body {
  padding-left: 0;
  padding-right: 0;
}

.base-card__footer {
  padding: var(--space-3) var(--space-5);
  border-top: 1px solid var(--border-light);
  display: flex;
  gap: var(--space-2);
  justify-content: flex-end;
}

@media (max-width: 640px) {
  .base-card__header,
  .base-card__body,
  .base-card__footer {
    padding-left: var(--space-4);
    padding-right: var(--space-4);
  }
}
</style>
