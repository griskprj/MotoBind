<template>
  <div class="filters">
    <div class="filters__row">
      <div class="filters__search">
        <i class="fa fa-search" />
        <input
          :value="modelValue.search"
          type="text"
          placeholder="Поиск по названию..."
          @input="onSearch"
        >
      </div>

      <BaseSelect
      :model-value="modelValue.status || ''"
        :options="statusOptions"
        placeholder="Все статусы"
        @update:model-value="onStatus"
        />

      <BaseSelect
        v-if="showMotorcycleFilter"
        :model-value="modelValue.motorcycle || ''"
        :options="motoOptions"
        placeholder="Все мотоциклы"
        @update:model-value="onMotorcycle"
      />

      <BaseSelect
      :model-value="sortBy"
      :options="sortOptions"
      @update:model-value="onSort"
      />

      <BaseButton
        variant="primary"
        icon="fa fa-plus"
        @click="emit('add')"
      >
        Добавить
      </BaseButton>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { BaseButton, BaseSelect } from '@/components/ui'

const props = defineProps({
  modelValue: { type: Object, required: true },
  sortBy: { type: String, default: 'date_desc' },
  motorcycles: { type: Array, default: () => [] },
  showMotorcycleFilter: { type: Boolean, default: false },
})

const emit = defineEmits(['update:model-value', 'update:sort-by', 'add'])

const statusOptions = [
  { value: '', label: 'Все статусы' },
  { value: 'planned', label: 'Запланировано' },
  { value: 'completed', label: 'Выполнено' },
  { value: 'overdue', label: 'Просрочено' },
]

const sortOptions = [
  { value: 'date_desc', label: 'Сначала новые' },
  { value: 'date_asc', label: 'Сначала старые' },
  { value: 'mileage_desc', label: 'По пробегу ↓' },
  { value: 'mileage_asc', label: 'По пробегу ↑' },
  { value: 'cost_desc', label: 'По стоимости ↓' },
]

const motoOptions = computed(() => [
  { value: '', label: 'Все мотоциклы' },
  ...props.motorcycles.map((m) => ({ value: m.id, label: m.name })),
])

function onSearch(e) {
  emit('update:model-value', { ...props.modelValue, search: e.target.value })
}
function onStatus(v) {
  emit('update:model-value', { ...props.modelValue, status: v })
}
function onMotorcycle(v) {
  emit('update:model-value', { ...props.modelValue, motorcycle: v })
}
function onSort(v) {
  emit('update:sort-by', v)
}
</script>

<style scoped>
.filters {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.filters__row {
  display: grid;
  grid-template-columns: 1fr 160px 160px 160px auto;
  gap: var(--space-2);
  align-items: end;
}

.filters__search {
  position: relative;
  display: flex;
  align-items: center;
}

.filters__search i {
  position: absolute;
  left: var(--space-3);
  color: var(--text-muted);
  font-size: var(--text-sm);
  pointer-events: none;
}

.filters__search input {
  width: 100%;
  padding: var(--space-2) var(--space-3) var(--space-2) var(--space-8);
  min-height: 40px;
  border: 1px solid var(--border-input);
  border-radius: var(--radius-md);
  background: var(--bg-input);
  color: var(--text-primary);
  font-family: inherit;
  font-size: var(--text-sm);
}

.filters__search input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: var(--shadow-focus);
}

@media (max-width: 1024px) {
  .filters__row {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 640px) {
  .filters__row {
    grid-template-columns: 1fr;
  }
}
</style>
