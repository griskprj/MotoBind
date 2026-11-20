<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{
  rule: any
}>()

const emit = defineEmits<{ close: [] }>()

const currentStep = ref(0)
const steps = computed(() => props.rule.steps || [])

function next() {
  if (currentStep.value < steps.value.length - 1) {
    currentStep.value++
  } else {
    emit('close')
  }
}

function prev() {
  if (currentStep.value > 0) currentStep.value--
}

const progress = computed(() => {
  if (steps.value.length === 0) return 0
  return ((currentStep.value + 1) / steps.value.length) * 100
})
</script>

<template>
  <BaseModal
    :title="`Пошаговая диагностика`"
    size="md"
    @close="emit('close')"
  >
    <div class="steps-content">
      <div class="steps-header">
        <h3 class="rule-title">{{ rule.title }}</h3>
        <p class="rule-cause">{{ rule.cause }}</p>
      </div>

      <div class="progress-wrapper">
        <div class="progress-info">
          <span>Шаг {{ currentStep + 1 }} из {{ steps.length }}</span>
          <span class="progress-percent">{{ Math.round(progress) }}%</span>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progress + '%' }"></div>
        </div>
      </div>

      <div v-if="steps[currentStep]" class="step-card">
        <div class="step-number">{{ currentStep + 1 }}</div>
        <div class="step-body">
          <h3 class="step-title">{{ steps[currentStep].title }}</h3>
          <p class="step-desc">{{ steps[currentStep].description }}</p>
          <p v-if="steps[currentStep].tip" class="step-tip">
            <i class="fa-solid fa-lightbulb"></i>
            <span>{{ steps[currentStep].tip }}</span>
          </p>
        </div>
      </div>

      <div v-else class="empty-state">
        <i class="fa-solid fa-circle-info"></i>
        <p>Для этого правила нет пошаговых инструкций.</p>
      </div>
    </div>

    <template #footer>
      <div class="steps-actions">
        <BaseButton
          v-if="currentStep > 0"
          variant="secondary"
          @click="prev"
        >
          <i class="fa-solid fa-arrow-left"></i> Назад
        </BaseButton>
        <BaseButton variant="primary" @click="next">
          {{ currentStep < steps.length - 1 ? 'Далее' : 'Завершить' }}
          <i v-if="currentStep < steps.length - 1" class="fa-solid fa-arrow-right"></i>
        </BaseButton>
      </div>
    </template>
  </BaseModal>
</template>

<style scoped lang="scss">
.steps-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.steps-header {
  padding-bottom: var(--space-3);
  border-bottom: 1px solid var(--color-border);
}

.rule-title {
  font-size: var(--text-lg);
  font-weight: var(--fw-bold);
  margin-bottom: var(--space-1);
}

.rule-cause {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

/* Прогресс */
.progress-wrapper {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.progress-info {
  display: flex;
  justify-content: space-between;
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
  font-weight: var(--fw-medium);
}

.progress-percent {
  color: var(--color-brand);
  font-weight: var(--fw-bold);
}

.progress-bar {
  height: 6px;
  background: var(--color-surface-secondary);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #7000ff, #a855f7);
  border-radius: var(--radius-full);
  transition: width 0.3s ease;
}

/* Шаг */
.step-card {
  display: flex;
  gap: var(--space-3);
  padding: var(--space-4);
  background: var(--color-surface-secondary);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
}

.step-number {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
  border-radius: 50%;
  background: var(--color-brand);
  color: #fff;
  font-weight: var(--fw-bold);
  font-size: var(--text-sm);
  display: flex;
  align-items: center;
  justify-content: center;
}

.step-body {
  flex: 1;
  min-width: 0;
}

.step-title {
  font-size: var(--text-base);
  font-weight: var(--fw-semibold);
  margin-bottom: var(--space-2);
}

.step-desc {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  line-height: 1.5;
}

.step-tip {
  margin-top: var(--space-3);
  padding: var(--space-2) var(--space-3);
  background: rgba(245, 158, 11, 0.1);
  border-left: 3px solid #f59e0b;
  border-radius: var(--radius-sm);
  font-size: var(--text-xs);
  color: var(--color-text-primary);
  display: flex;
  gap: var(--space-2);
  align-items: flex-start;

  i {
    color: #f59e0b;
    margin-top: 2px;
    flex-shrink: 0;
  }
}

/* Кнопки */
.steps-actions {
  display: flex;
  justify-content: space-between;
  gap: var(--space-3);
  width: 100%;

  :deep(button) {
    display: flex;
    align-items: center;
    gap: var(--space-2);
  }
}

/* Пустое */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-6);
  color: var(--color-text-tertiary);
  text-align: center;

  i { font-size: 28px; }
  p { font-size: var(--text-sm); }
}
</style>
