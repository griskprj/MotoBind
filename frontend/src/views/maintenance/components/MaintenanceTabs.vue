<template>
  <div class="tabs">
    <button
      v-for="tab in tabs"
      :key="tab.key"
      type="button"
      class="tabs__item"
      :class="{ 'tabs__item--active': modelValue === tab.key }"
      @click="emit('update:modelValue', tab.key)"
    >
      <i :class="tab.icon" />
      <span>{{ tab.label }}</span>
      <span v-if="counts[tab.key] > 0" class="tabs__badge">
        {{ counts[tab.key] }}
      </span>
    </button>
  </div>
</template>

<script setup>
defineProps({
  modelValue: { type: String, required: true },
  counts: { type: Object, default: () => ({}) },
})

const emit = defineEmits(['update:modelValue'])

const tabs = [
  { key: 'overview', label: 'Обзор', icon: 'fa fa-chart-pie' },
  { key: 'history', label: 'История', icon: 'fa fa-clock-rotate-left' },
  { key: 'plans', label: 'Планы', icon: 'fa fa-calendar-check' },
  { key: 'manuals', label: 'Мануалы', icon: 'fa fa-book' },
  { key: 'diagnostics', label: 'Диагностика', icon: 'fa fa-stethoscope' },
]
</script>

<style scoped>
.tabs {
  display: flex;
  gap: var(--space-1);
  overflow-x: auto;
  padding-bottom: 2px;
  border-bottom: 1px solid var(--border-light);
  scrollbar-width: none;
}

.tabs::-webkit-scrollbar { display: none; }

.tabs__item {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: var(--text-secondary);
  font-family: inherit;
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
  white-space: nowrap;
  min-height: 40px;
  margin-bottom: -1px;
}

.tabs__item:hover {
  color: var(--text-primary);
  background: var(--bg-secondary);
}

.tabs__item--active {
  color: var(--accent-text);
  border-bottom-color: var(--accent);
}

.tabs__item i {
  font-size: var(--text-base);
}

.tabs__badge {
  background: var(--accent);
  color: #fff;
  font-size: 11px;
  font-weight: 600;
  padding: 1px 7px;
  border-radius: var(--radius-full);
  min-width: 18px;
  text-align: center;
}

@media (max-width: 640px) {
  .tabs__item span:not(.tabs__badge) {
    display: none;
  }

  .tabs__item {
    padding: var(--space-2) var(--space-3);
  }
}
</style>
