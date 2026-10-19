<template>
  <div class="tabs">
    <button
      v-for="tab in visibleTabs"
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
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

defineProps({
  modelValue: { type: String, required: true },
  counts: { type: Object, default: () => ({}) },
})

const emit = defineEmits(['update:modelValue'])

const authStore = useAuthStore()

const allTabs = [
  { key: 'courses', label: 'Курсы', icon: 'fa fa-graduation-cap' },
  { key: 'articles', label: 'Статьи', icon: 'fa fa-newspaper' },
  { key: 'my', label: 'Моё', icon: 'fa fa-bookmark', requiresAuth: true },
]

const visibleTabs = computed(() =>
  allTabs.filter((t) => !t.requiresAuth || authStore.isAuthenticated)
)
</script>

<style scoped>
.tabs {
  display: flex;
  gap: var(--space-1);
  overflow-x: auto;
  padding-bottom: 2px;
  border-bottom: 1px solid var(--border-light);
  scrollbar-width: none;
  width: 100%;
  min-width: 0;
  -webkit-overflow-scrolling: touch;
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

@media (max-width: 990px) {
  .tabs__item span:not(.tabs__badge) { display: none; }
  .tabs__item { padding: var(--space-2) var(--space-3); flex-shrink: 0; }
}
</style>
