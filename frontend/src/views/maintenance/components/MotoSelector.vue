<template>
  <div class="moto-selector">
    <label class="moto-selector__label">
      <i class="fa fa-motorcycle" />
      Мотоцикл
    </label>
    <div class="moto-selector__chips">
      <button
        v-for="moto in motorcycles"
        :key="moto.id"
        type="button"
        class="moto-chip"
        :class="{ 'moto-chip--active': moto.id === selectedId }"
        @click="emit('select', moto)"
      >
        <span class="moto-chip__name">{{ moto.name }}</span>
        <span class="moto-chip__mileage">{{ formatMileage(moto.mileage) }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { formatMileage } from '@/utils/formatters'

defineProps({
  motorcycles: { type: Array, required: true },
  selectedId: { type: Number, default: null },
})

const emit = defineEmits(['select'])
</script>

<style scoped>
.moto-selector {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.moto-selector__label {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  color: var(--text-secondary);
}

.moto-selector__label i {
  color: var(--accent-text);
}

.moto-selector__chips {
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.moto-chip {
  display: inline-flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
  padding: var(--space-2) var(--space-4);
  background: var(--bg-secondary);
  border: 2px solid transparent;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-family: inherit;
  text-align: left;
  min-height: 48px;
}

.moto-chip:hover {
  background: var(--bg-card-hover);
  border-color: var(--border-color);
}

.moto-chip--active {
  background: var(--accent-trans);
  border-color: var(--accent);
}

.moto-chip__name {
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
}

.moto-chip--active .moto-chip__name {
  color: var(--accent-text);
}

.moto-chip__mileage {
  font-size: var(--text-xs);
  color: var(--text-muted);
}
</style>
