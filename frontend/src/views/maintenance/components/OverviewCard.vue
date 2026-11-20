<template>
  <div class="ov-card">
    <header class="ov-card__head">
      <div class="ov-card__head-left">
        <i :class="icon" />
        <h4>{{ title }}</h4>
      </div>
      <button v-if="actionLabel" class="ov-card__action" @click="emit('action')">
        {{ actionLabel }} <i class="fa fa-arrow-right" />
      </button>
    </header>
    <div class="ov-card__body">
      <slot />
    </div>
  </div>
</template>

<script setup>
defineProps({
  icon: { type: String, default: '' },
  title: { type: String, required: true },
  actionLabel: { type: String, default: '' },
})
const emit = defineEmits(['action'])
</script>

<style scoped>
.ov-card {
  display: flex;
  flex-direction: column;
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.ov-card__head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--border-light);
}

.ov-card__head-left {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.ov-card__head-left i {
  color: var(--accent-text);
  font-size: var(--text-base);
}

.ov-card__head-left h4 {
  margin: 0;
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
}

.ov-card__action {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: none;
  border: none;
  color: var(--accent-text);
  font-size: var(--text-xs);
  font-weight: var(--fw-medium);
  cursor: pointer;
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
  transition: background var(--transition-fast);
  font-family: inherit;
}

.ov-card__action:hover {
  background: var(--accent-trans);
}

.ov-card__body {
  padding: var(--space-3) var(--space-4) var(--space-4);
}
</style>
