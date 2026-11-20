<template>
  <div class="questions-step">
    <div class="step-head">
      <h4>Уточняющие вопросы</h4>
      <p class="step-hint">
        Ответьте — это поможет точнее определить причину.
      </p>
    </div>

    <div
      v-for="q in store.relevantQuestions"
      :key="q.id"
      class="question-block"
    >
      <div class="question-text">{{ q.text }}</div>
      <div class="question-options">
        <button
          v-for="opt in q.options"
          :key="opt.id"
          type="button"
          class="option-chip"
          :class="{ active: store.answers[q.id] === opt.id }"
          @click="store.setAnswer(q.id, opt.id)"
        >
          {{ opt.label }}
        </button>
      </div>
    </div>

    <div class="step-summary">
      Отвечено: <strong>{{ store.answeredCount }}</strong>
      из {{ store.totalQuestions }}
    </div>

    <div class="step-actions">
      <BaseButton
        variant="secondary"
        icon="fa fa-arrow-left"
        @click="emit('back')"
      >
        Назад
      </BaseButton>
      <BaseButton
        variant="primary"
        icon="fa fa-stethoscope"
        :disabled="!store.canRunDiagnostics"
        @click="emit('run')"
      >
        Диагностировать
      </BaseButton>
    </div>
  </div>
</template>

<script setup>
import { BaseButton } from '@/components/ui'
import { useDiagnosticsStore } from '@/stores'

const emit = defineEmits(['back', 'run'])

const store = useDiagnosticsStore()
</script>

<style scoped>
.questions-step {
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

.question-block {
  padding: 14px 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
}

.question-text {
  font-size: 14px;
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
  margin-bottom: 10px;
}

.question-options {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.option-chip {
  padding: 7px 14px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  background: var(--bg-primary);
  color: var(--text-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: all var(--transition-base);
  min-height: 34px;
}

.option-chip:hover {
  border-color: var(--accent);
  color: var(--accent-text);
}

.option-chip.active {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
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

.step-actions {
  display: flex;
  gap: var(--space-2);
}

.step-actions > * {
  flex: 1;
}
</style>
