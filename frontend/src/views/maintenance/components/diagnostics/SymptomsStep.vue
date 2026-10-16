<template>
  <div class="symptoms-step">
    <div class="step-head">
      <h4>
        {{ store.lockedGroup ? groupLabel : 'Общая диагностика' }}
      </h4>
      <p class="step-hint">
        Отметьте всё, что замечаете. Можно выбрать несколько.
      </p>
    </div>

    <!-- Группы симптомов -->
    <div
      v-for="group in visibleGroups"
      :key="group.id"
      class="symptom-group"
    >
      <div v-if="!store.lockedGroup" class="symptom-group-title">
        <i :class="group.icon" />
        {{ group.label }}
      </div>
      <div class="symptom-chips">
        <button
          v-for="s in getSymptomsForGroup(group.id)"
          :key="s.id"
          type="button"
          class="symptom-chip"
          :class="{ active: store.selectedSymptoms.has(s.id) }"
          @click="store.toggleSymptom(s.id)"
        >
          <i :class="s.icon" />
          <span>{{ s.label }}</span>
        </button>
      </div>
    </div>

    <!-- Сводка -->
    <div
      v-if="store.selectedSymptoms.size === 0"
      class="step-empty"
    >
      <i class="fa fa-info-circle" />
      Выберите хотя бы один симптом, чтобы продолжить
    </div>
    <div v-else class="step-summary">
      Выбрано симптомов: <strong>{{ store.selectedSymptoms.size }}</strong>
    </div>

    <!-- Действия -->
    <div class="step-actions">
      <BaseButton
        variant="secondary"
        icon="fa fa-arrow-left"
        @click="emit('cancel')"
      >
        Назад
      </BaseButton>
      <BaseButton
        variant="primary"
        icon-right="fa fa-arrow-right"
        :disabled="!store.canProceedFromSymptoms"
        @click="emit('next')"
      >
        Дальше
      </BaseButton>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { BaseButton } from '@/components/ui'
import { useDiagnosticsStore } from '@/stores'
import {
  SYMPTOM_GROUPS,
  SYMPTOM_GROUP_BY_ID,
  getSymptomsForGroup,
} from '@/constants/diagnisticsRules'

const emit = defineEmits(['next', 'cancel'])

const store = useDiagnosticsStore()

const visibleGroups = computed(() => {
  if (!store.lockedGroup) return SYMPTOM_GROUPS
  return SYMPTOM_GROUPS.filter((g) => g.id === store.lockedGroup)
})

const groupLabel = computed(() => {
  return SYMPTOM_GROUP_BY_ID[store.lockedGroup]?.label || ''
})
</script>

<style scoped>
.symptoms-step {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.step-head h4 {
  margin: 0 0 var(--space-1);
  font-size: var(--text-base);
}

.step-hint {
  margin: 0;
  font-size: var(--text-sm);
  color: var(--text-muted);
}

.symptom-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.symptom-group-title {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 12px;
  font-weight: var(--fw-semibold);
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: var(--text-muted);
}

.symptom-group-title i {
  color: var(--accent-text);
  font-size: 13px;
}

.symptom-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.symptom-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 12px;
  border-radius: var(--radius-full);
  border: 1px solid var(--border-color);
  background: var(--bg-secondary);
  color: var(--text-secondary);
  font-size: 12.5px;
  cursor: pointer;
  transition: all var(--transition-base);
  min-height: 34px;
}

.symptom-chip:hover {
  border-color: var(--accent);
  color: var(--accent-text);
  background: var(--accent-trans);
}

.symptom-chip.active {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
}

.symptom-chip i {
  font-size: 11px;
}

.step-summary {
  padding: 10px 14px;
  background: var(--accent-trans);
  border-radius: var(--radius-md);
  font-size: 13px;
  color: var(--text-secondary);
  text-align: center;
}

.step-summary strong {
  color: var(--accent-text);
}

.step-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 14px;
  background: var(--border-light);
  border-radius: var(--radius-md);
  font-size: 13px;
  color: var(--text-muted);
}

.step-actions {
  display: flex;
  gap: var(--space-2);
  margin-top: var(--space-2);
}

.step-actions > * {
  flex: 1;
}

@media (max-width: 640px) {
  .symptom-chip {
    font-size: 12px;
    padding: 6px 10px;
  }
}
</style>
