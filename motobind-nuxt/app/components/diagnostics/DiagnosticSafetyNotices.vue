<script setup lang="ts">
import type { DiagnosticSafetyAlert } from '~/utils/constants/diagnosticsRules'

defineProps<{
  alerts: DiagnosticSafetyAlert[]
}>()
</script>

<template>
  <section
    v-if="alerts.length"
    class="safety-notices"
    role="status"
    aria-live="polite"
    aria-label="Предупреждения по безопасности"
  >
    <article v-for="alert in alerts" :key="alert.id" class="safety-notice">
      <i class="fa-solid fa-triangle-exclamation" aria-hidden="true"></i>
      <div>
        <h4>{{ alert.title }}</h4>
        <p>{{ alert.message }}</p>
      </div>
    </article>
    <p class="safety-disclaimer">Онлайн-подсказка не определяет точную неисправность. При сомнениях обратитесь в сервис.</p>
  </section>
</template>

<style scoped lang="scss">
.safety-notices {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  padding: var(--space-4);
  border: 1px solid rgba(239, 68, 68, 0.45);
  border-radius: var(--radius-lg);
  background: rgba(239, 68, 68, 0.08);
}

.safety-notice {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  color: var(--color-text-primary);

  > i {
    margin-top: 3px;
    color: #ef4444;
  }

  h4 {
    margin-bottom: var(--space-1);
    font-size: var(--text-sm);
    font-weight: var(--fw-semibold);
  }

  p {
    color: var(--color-text-secondary);
    font-size: var(--text-sm);
    line-height: 1.5;
  }
}

.safety-disclaimer {
  padding-top: var(--space-2);
  border-top: 1px solid rgba(239, 68, 68, 0.25);
  color: var(--color-text-tertiary);
  font-size: var(--text-xs);
}
</style>
