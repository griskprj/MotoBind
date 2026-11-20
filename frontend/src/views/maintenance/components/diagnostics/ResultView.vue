<template>
  <div class="result-view">
    <div class="result-head">
      <h4>Результат диагностики</h4>
      <p class="result-hint">
        Найдено причин: <strong>{{ store.results.length }}</strong>
      </p>
    </div>

    <!-- Пусто -->
    <div v-if="store.results.length === 0" class="result-empty">
      <i class="fa fa-circle-question" />
      <h4>Точной причины не найдено</h4>
      <p>
        По указанным симптомам не удалось подобрать однозначную причину.
        Рекомендуем обратиться к мастеру для очной диагностики.
      </p>
    </div>

    <!-- Список причин -->
    <div v-else class="result-list">
      <div
        v-for="r in store.results"
        :key="r.id"
        class="diag-card"
        :class="'diag-card--' + r.severity"
      >
        <div class="diag-card__head">
          <div class="diag-card__icon">
            <i :class="severityIcon(r.severity)" />
          </div>
          <div class="diag-card__head-text">
            <div class="diag-card__title">{{ r.title }}</div>
            <div class="diag-card__category">{{ categoryLabel(r.category) }}</div>
          </div>
          <div class="diag-card__score">
            {{ Math.round(r.score * 100) }}%
          </div>
        </div>

        <div class="diag-card__body">
          <div class="diag-card__row">
            <span class="diag-card__label">Причина</span>
            <p class="diag-card__value">{{ r.cause }}</p>
          </div>
          <div class="diag-card__row">
            <span class="diag-card__label">Рекомендация</span>
            <p class="diag-card__value">{{ r.advice }}</p>
          </div>
        </div>

        <ResultCardActions
          :rule="r"
          :motorcycle="motorcycle"
        />
      </div>
    </div>

    <!-- Дисклеймер -->
    <div class="result-disclaimer">
      <i class="fa fa-triangle-exclamation" />
      Результат не заменяет профессиональную диагностику.
      При сомнениях обратитесь к мастеру.
    </div>

    <!-- Действия -->
    <div class="result-actions">
      <BaseButton
        variant="primary"
        icon="fa fa-floppy-disk"
        :loading="store.saving"
        :disabled="store.saving || !!store.lastReportId"
        @click="saveReport"
      >
        {{ store.lastReportId ? 'Отчёт сохранён' : 'Сохранить отчёт' }}
      </BaseButton>

      <BaseButton
        variant="secondary"
        icon="fa fa-rotate-right"
        @click="emit('restart')"
      >
        Пройти заново
      </BaseButton>

      <BaseButton
        v-if="store.lastReportId"
        variant="outline"
        icon="fa fa-clock-rotate-left"
        block
        @click="emit('open-history')"
      >
        К истории диагностик
      </BaseButton>
    </div>
  </div>
</template>

<script setup>
import { BaseButton } from '@/components/ui'
import { useDiagnosticsStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import { SYMPTOM_GROUP_BY_ID } from '@/constants/diagnisticsRules'
import ResultCardActions from './ResultCardActions.vue';

const props = defineProps({
  motorcycle: { type: Object, default: null },
})

const emit = defineEmits(['restart', 'open-history'])

const store = useDiagnosticsStore()
const toast = useToast()

function severityIcon(severity) {
  return (
    {
      info: 'fa fa-circle-info',
      warning: 'fa fa-triangle-exclamation',
      danger: 'fa fa-circle-exclamation',
    }[severity] || 'fa fa-circle-info'
  )
}

function categoryLabel(category) {
  return SYMPTOM_GROUP_BY_ID[category]?.label || category
}

async function saveReport() {
  try {
    await store.saveReport({
      motorcycleId: props.motorcycle?.id || null,
      mileage: props.motorcycle?.mileage || null,
    })
    toast.success('Отчёт сохранён')
  } catch (err) {
    console.error('Failed to save report:', err)
    toast.error(err.response?.data?.error || 'Не удалось сохранить отчёт')
  }
}
</script>

<style scoped>
.result-view {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.result-head {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.result-head h4 {
  margin: 0;
  font-size: var(--text-base);
}

.result-hint {
  margin: 0;
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.result-hint strong {
  color: var(--accent-text);
}

/* ===== Список ===== */
.result-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* ===== Пусто ===== */
.result-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 10px;
  padding: 28px 16px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  border: 1px dashed var(--border-color);
}

.result-empty i {
  font-size: 44px;
  color: var(--warning-text);
}

.result-empty h4 {
  margin: 0;
  font-size: 18px;
  color: var(--text-primary);
}

.result-empty p {
  margin: 0;
  font-size: 13px;
  color: var(--text-secondary);
  max-width: 340px;
  line-height: var(--leading-base);
}

/* ===== Дисклеймер ===== */
.result-disclaimer {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 10px 14px;
  background: var(--warning-trans);
  border: 1px solid rgba(245, 158, 11, 0.2);
  border-radius: var(--radius-md);
  font-size: 12.5px;
  color: var(--text-secondary);
  line-height: var(--leading-base);
}

.result-disclaimer i {
  color: var(--warning-text);
  margin-top: 2px;
  flex-shrink: 0;
}

/* ===== Действия ===== */
.result-actions {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  margin-top: var(--space-2);
}

.result-actions > * {
  width: 100%;
}

@media (min-width: 640px) {
  .result-actions {
    flex-direction: row;
    flex-wrap: wrap;
  }

  .result-actions > * {
    flex: 1;
    min-width: 200px;
    width: auto;
  }
}
</style>
