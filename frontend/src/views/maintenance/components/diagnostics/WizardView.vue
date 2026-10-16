<template>
  <div class="wizard-view">
    <!-- Прогресс -->
    <div class="wizard-progress">
      <button
        type="button"
        class="progress-step"
        :class="{ active: store.step === 1, done: store.step > 1 }"
        @click="goBackToSymptoms"
      >
        <span class="progress-step__num">1</span>
        <span class="progress-step__label">Симптомы</span>
      </button>
      <div class="progress-line" :class="{ filled: store.step > 1 }" />
      <div
        class="progress-step"
        :class="{ active: store.step === 2 }"
      >
        <span class="progress-step__num">2</span>
        <span class="progress-step__label">Вопросы</span>
      </div>
    </div>

    <SymptomsStep
      v-if="store.step === 1"
      @next="store.goToQuestions"
      @cancel="emit('cancel')"
    />

    <QuestionsStep
      v-else
      @run="store.runDiagnostics"
      @back="goBackToSymptoms"
    />
  </div>
</template>

<script setup>
import { useDiagnosticsStore } from '@/stores'
import SymptomsStep from './SymptomsStep.vue'
import QuestionsStep from './QuestionsStep.vue'

defineProps({
  motorcycle: { type: Object, default: null },
})

const emit = defineEmits(['cancel'])

const store = useDiagnosticsStore()

function goBackToSymptoms() {
  store.goBackToSymptoms()
}
</script>

<style scoped>
.wizard-view {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.wizard-progress {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
}

.progress-step {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  background: none;
  border: none;
  padding: 0;
  font-family: inherit;
  font-size: var(--text-sm);
  color: var(--text-muted);
  cursor: default;
  min-height: 0;
}

.progress-step.active {
  color: var(--accent-text);
  font-weight: var(--fw-semibold);
}

.progress-step.done {
  color: var(--text-secondary);
  cursor: pointer;
}

.progress-step__num {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.progress-step.active .progress-step__num {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
}

.progress-step.done .progress-step__num {
  background: var(--accent-trans);
  border-color: var(--accent);
  color: var(--accent-text);
}

.progress-line {
  flex: 1;
  height: 2px;
  background: var(--border-color);
  border-radius: 1px;
  transition: background var(--transition-base);
}

.progress-line.filled {
  background: var(--accent);
}

@media (max-width: 640px) {
  .progress-step__label {
    display: none;
  }
}
</style>
