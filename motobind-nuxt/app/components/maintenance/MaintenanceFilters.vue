<script setup lang="ts">
import type { Motorcycle } from '~/types'

const props = defineProps<{
  motorcycles: Motorcycle[]
  selectedMotorcycleId: number | 'all'
  filterBy: 'all' | 'date' | 'mileage'
  activeTab: 'planned' | 'history'
}>()

const emit = defineEmits<{
  'update:selectedMotorcycleId': [value: number | 'all']
  'update:filterBy': [value: 'all' | 'date' | 'mileage']
}>()

const motoOptions = computed(() => [
  { value: 'all', label: 'Все мотоциклы' },
  ...props.motorcycles.map(m => ({ value: m.id, label: m.name }))
])
</script>

<template>
  <div class="filters-bar">
    <!-- Фильтр по мотоциклу -->
    <BaseSelect
      :model-value="selectedMotorcycleId"
      :options="motoOptions"
      @update:model-value="emit('update:selectedMotorcycleId', $event as number | 'all')"
      class="filter-select"
    />

    <!-- Сортировка (только для планов) -->
    <div v-if="activeTab === 'planned'" class="sort-tabs">
      <button
        class="sort-btn"
        :class="{ 'sort-btn--active': filterBy === 'all' }"
        @click="emit('update:filterBy', 'all')"
      >
        <i class="fa-solid fa-list"></i> Все
      </button>
      <button
        class="sort-btn"
        :class="{ 'sort-btn--active': filterBy === 'date' }"
        @click="emit('update:filterBy', 'date')"
      >
        <i class="fa-regular fa-calendar"></i> По дате
      </button>
      <button
        class="sort-btn"
        :class="{ 'sort-btn--active': filterBy === 'mileage' }"
        @click="emit('update:filterBy', 'mileage')"
      >
        <i class="fa-solid fa-gauge-high"></i> По пробегу
      </button>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.filters-bar {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  background: var(--color-surface);
  padding: var(--space-3);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);

  @include sm-up {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}

.filter-select {
  width: 100%;
  max-width: 300px;

  @include sm-up {
    width: auto;
    min-width: 220px;
  }
}

.sort-tabs {
  display: flex;
  background: var(--color-surface-secondary);
  padding: 4px;
  border-radius: var(--radius-md);
  width: fit-content;
}

.sort-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-sm);
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  color: var(--color-text-secondary);
  transition: all var(--transition-fast);
  border: none;
  background: transparent;
  cursor: pointer;

  &:hover { color: var(--color-text); }

  &--active {
    background: var(--color-surface);
    color: var(--color-brand);
    box-shadow: var(--shadow-sm);
  }
}
</style>
