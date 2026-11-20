<template>
  <div class="sidebar-card mileage-card">
    <div class="sidebar-card-header">
      <i class="fa-solid fa-gauge-high"></i>
      <h4>Пробег</h4>
    </div>

    <div class="mileage-display">
      <div class="mileage-value">{{ formatMileage(moto.mileage) }}</div>
      <div class="mileage-updated">
        <i class="fa fa-clock"></i>
        Обновлён {{ formatDate(moto.updated_at || new Date()) }}
      </div>
    </div>

    <div class="mileage-quick-add">
      <span class="quick-add-label">Быстро добавить:</span>
      <div class="quick-add-buttons">
        <button
          v-for="step in quickSteps"
          :key="step"
          class="quick-add-btn"
          :disabled="updating"
          @click="emit('quick-add', step)"
        >
          +{{ step }}
        </button>
      </div>
    </div>

    <button
      class="btn-primary mileage-submit"
      :disabled="updating"
      @click="emit('open-precise')"
    >
      <i :class="updating ? 'fa fa-spinner fa-spin' : 'fa fa-pen'"></i>
      {{ updating ? 'Обновление...' : 'Ввести точное значение' }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { formatMileage } from '@/utils/formatters'
import formatDate from '@/utils/DateFormatter.js'

defineProps<{
  moto: any
  updating: boolean
}>()

const emit = defineEmits<{
  'quick-add': [number]
  'open-precise': []
}>()

const quickSteps = [50, 100, 500, 1000]
</script>

<style scoped>
.sidebar-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 18px 20px;
  transition: all var(--transition-base);
}

.sidebar-card:hover {
  border-color: var(--border-color);
}

.sidebar-card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}

.sidebar-card-header i {
  color: var(--accent-text);
  font-size: 16px;
}

.sidebar-card-header h4 {
  font-size: 14px;
  font-weight: var(--fw-semibold);
  margin: 0;
}

.mileage-card {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-bottom: 20px;
}

.mileage-display {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 12px 14px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
}

.mileage-value {
  font-size: 26px;
  font-weight: var(--fw-bold);
  color: var(--text-primary);
  letter-spacing: -0.5px;
  line-height: 1.1;
}

.mileage-updated {
  font-size: 11px;
  color: var(--text-muted);
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.mileage-updated i {
  font-size: 10px;
}

.mileage-quick-add {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.quick-add-label {
  font-size: 11px;
  font-weight: var(--fw-semibold);
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: var(--text-muted);
}

.quick-add-buttons {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px;
}

.quick-add-btn {
  padding: 8px 4px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 12px;
  font-weight: var(--fw-semibold);
  cursor: pointer;
  transition: all var(--transition-base);
  min-height: 36px;
  font-family: var(--font-mono);
}

.quick-add-btn:hover:not(:disabled) {
  border-color: var(--accent);
  background: var(--accent-trans);
  color: var(--accent-text);
  transform: translateY(-1px);
}

.quick-add-btn:active:not(:disabled) {
  transform: translateY(0);
}

.quick-add-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.mileage-submit {
  width: 100%;
  padding: 10px 16px;
  border-radius: var(--radius-md);
  background: var(--accent);
  color: #fff;
  border: none;
  font-size: 13px;
  font-weight: var(--fw-semibold);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all var(--transition-base);
  min-height: 40px;
}

.mileage-submit:hover:not(:disabled) {
  background: var(--accent-hover);
  transform: translateY(-1px);
}

.mileage-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 400px) {
  .quick-add-buttons {
    grid-template-columns: repeat(2, 1fr);
  }

  .mileage-value {
    font-size: 22px;
  }
}
</style>
