<template>
  <div class="detail-grid">
    <!-- Характеристики -->
    <div class="detail-card">
      <h4 class="detail-title">Характеристики</h4>
      <div class="spec-list">
        <div class="spec-item">
          <span class="spec-label">Год выпуска</span>
          <span class="spec-value">{{ moto.years || '—' }}</span>
        </div>
        <div class="spec-item">
          <span class="spec-label">Двигатель</span>
          <span class="spec-value">{{ moto.volume ? `${moto.volume} см³` : '—' }}</span>
        </div>
        <div class="spec-item">
          <span class="spec-label">Цвет</span>
          <span class="spec-value">
            <span class="color-dot" :style="{ background: moto.color }"></span>
          </span>
        </div>
        <div class="spec-item">
          <span class="spec-label">Пробег</span>
          <span class="spec-value">{{ formatMileage(moto.mileage) }}</span>
        </div>
        <div v-if="moto.vin" class="spec-item full">
          <span class="spec-label">VIN</span>
          <span class="spec-value spec-code">{{ moto.vin }}</span>
        </div>
        <div v-if="moto.license_plate" class="spec-item full">
          <span class="spec-label">Гос. номер</span>
          <span class="spec-value spec-code">{{ moto.license_plate }}</span>
        </div>
      </div>
    </div>

    <!-- Заметки -->
    <div class="detail-card notes-card">
      <div class="detail-header">
        <h4 class="detail-title">Заметки</h4>
        <button class="icon-btn small" title="Редактировать заметку" @click="emit('edit-note')">
          <i class="fa fa-pen"></i>
        </button>
      </div>
      <div class="notes-content">
        <p v-if="moto.note" class="notes-text">{{ moto.note }}</p>
        <p v-else class="notes-empty">
          <i class="fa fa-pen"></i>
          Добавьте заметку о мотоцикле
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { formatMileage } from '@/utils/formatters'

defineProps<{ moto: any }>()

const emit = defineEmits<{ 'edit-note': [] }>()
</script>

<style scoped>
.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}

.detail-card {
  padding: 20px 24px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  transition: all var(--transition-base);
}

.detail-card:hover {
  border-color: var(--border-color);
}

.notes-card {
  display: flex;
  flex-direction: column;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.detail-title {
  font-size: 14px;
  font-weight: var(--fw-semibold);
  margin: 0;
  color: var(--text-primary);
  letter-spacing: 0.3px;
}

.spec-list {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px 20px;
}

.spec-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 6px 0;
  min-width: 0;
}

.spec-item.full {
  grid-column: 1 / -1;
}

.spec-label {
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-weight: var(--fw-medium);
}

.spec-value {
  font-size: 14px;
  font-weight: var(--fw-medium);
  color: var(--text-primary);
  word-break: break-word;
  overflow-wrap: anywhere;
}

.spec-value.spec-code {
  font-family: var(--font-mono);
  font-size: 13px;
  letter-spacing: 0.5px;
  background: var(--bg-primary);
  padding: 4px 10px;
  border-radius: var(--radius-sm);
  display: inline-block;
}

.color-dot {
  display: inline-block;
  width: 32px;
  height: 16px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
  transition: transform var(--transition-base);
}

.color-dot:hover {
  transform: scale(1.1);
}

.notes-content {
  flex: 1;
  display: flex;
  align-items: flex-start;
  padding-top: 4px;
}

.notes-text {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
  line-height: var(--leading-relaxed);
}

.notes-empty {
  font-size: 14px;
  color: var(--text-muted);
  font-style: italic;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.notes-empty i {
  color: var(--text-muted);
  font-size: 14px;
}

.icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  min-height: 34px;
  padding: 0;
  border: none;
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  transition: all var(--transition-base);
  font-size: 14px;
  line-height: 1;
  flex-shrink: 0;
  touch-action: manipulation;
}

.icon-btn:hover {
  background: var(--border-light);
  color: var(--text-primary);
}

.icon-btn.small {
  width: 28px;
  height: 28px;
  min-height: 28px;
  font-size: 12px;
}

.icon-btn i {
  pointer-events: none;
}

@media (max-width: 820px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .detail-card {
    padding: 14px 16px;
  }

  .spec-list {
    gap: 4px 12px;
  }

  .spec-value {
    font-size: 13px;
  }
}

@media (max-width: 400px) {
  .spec-list {
    grid-template-columns: 1fr;
  }
}
</style>
