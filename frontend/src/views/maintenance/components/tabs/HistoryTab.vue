<template>
  <div class="history">
    <MaintenanceFilters
      :model-value="filters"
      :sort-by="sortBy"
      :motorcycles="motorcycles"
      :show-motorcycle-filter="true"
      @update:model-value="emit('edit-filters', $event)"
      @update:sort-by="emit('sort', $event)"
      @add="emit('add')"
    />

    <div v-if="loading" class="history__loading">
      <div class="spinner" />
    </div>

    <div v-else-if="maintenances.length === 0" class="history__empty">
      <i class="fa fa-inbox" />
      <p>Нет записей по заданным фильтрам</p>
    </div>

    <div v-else class="history__list">
      <MaintenanceRow
        v-for="m in maintenances"
        :key="m.id"
        :item="m"
        @click="emit('open', m)"
      />
    </div>
  </div>
</template>

<script setup>
import MaintenanceFilters from '../filters/MaintenanceFilters.vue'
import MaintenanceRow from '../MaintenanceRow.vue'

defineProps({
  maintenances: { type: Array, default: () => [] },
  filters: { type: Object, default: () => ({}) },
  sortBy: { type: String, default: 'date_desc' },
  loading: { type: Boolean, default: false },
  motorcycles: { type: Array, default: () => [] },
})

const emit = defineEmits(['open', 'add', 'edit-filters', 'sort'])
</script>

<style scoped>
.history {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.history__list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.history__loading {
  display: flex;
  justify-content: center;
  padding: var(--space-6);
}

.history__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-8);
  color: var(--text-muted);
}

.history__empty i {
  font-size: var(--text-3xl);
  opacity: 0.4;
}

.history__empty p {
  margin: 0;
  font-size: var(--text-sm);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--border-color);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
