<template>
  <div class="report-view">
    <div class="report-head">
      <button type="button" class="back-btn" @click="emit('back')">
        <i class="fa fa-arrow-left" />
        К истории
      </button>
      <h4>Отчёт от {{ formatDate(report?.created_at) }}</h4>
      <p v-if="report?.mileage" class="report-mileage">
        Пробег: {{ report.mileage }} км
      </p>
    </div>

    <div v-if="!report" class="report-empty">
      Отчёт не найден
    </div>

    <template v-else>
      <!-- Симптомы -->
      <div class="report-section">
        <h5>Симптомы</h5>
        <div class="report-chips">
          <span
            v-for="sid in report.symptoms"
            :key="sid"
            class="report-chip"
          >
            {{ SYMPTOM_BY_ID[sid]?.label || sid }}
          </span>
        </div>
      </div>

      <!-- Ответы -->
      <div v-if="Object.keys(report.answers || {}).length" class="report-section">
        <h5>Ответы</h5>
        <div class="report-answers">
          <div
            v-for="(optId, qId) in report.answers"
            :key="qId"
            class="report-answer"
          >
            <span class="report-answer__q">
              {{ QUESTION_BY_ID[qId]?.text || qId }}
            </span>
            <span class="report-answer__a">
              {{ answerLabel(qId, optId) }}
            </span>
          </div>
        </div>
      </div>

      <!-- Результаты -->
      <div class="report-section">
        <h5>Найденные причины</h5>
        <div
          v-for="r in enrichedResults"
          :key="r.rule_id"
          class="diag-card"
          :class="'diag-card--' + r.severity"
        >
          <div class="diag-card__head">
            <div class="diag-card__head-text">
              <div class="diag-card__title">{{ r.title }}</div>
            </div>
            <div class="diag-card__score">{{ Math.round(r.score * 100) }}%</div>
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
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import {
  RULES,
  SYMPTOM_BY_ID,
  QUESTION_BY_ID,
} from '@/constants/diagnisticsRules'

const props = defineProps({
  report: { type: Object, default: null },
})

const emit = defineEmits(['back'])

const RULES_BY_ID = Object.fromEntries(RULES.map((r) => [r.id, r]))

const enrichedResults = computed(() => {
  if (!props.report?.results) return []
  return props.report.results
    .map((r) => {
      const rule = RULES_BY_ID[r.rule_id]
      if (!rule) {
        return {
          rule_id: r.rule_id,
          title: 'Правило удалено',
          cause: 'Это правило больше не существует в базе знаний.',
          advice: 'Обратитесь к мастеру для уточнения.',
          severity: 'info',
          score: r.score,
        }
      }
      return {
        rule_id: r.rule_id,
        title: rule.title,
        cause: rule.cause,
        advice: rule.advice,
        severity: rule.severity,
        score: r.score,
      }
    })
    .sort((a, b) => b.score - a.score)
})

function formatDate(iso) {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function answerLabel(qId, optId) {
  const q = QUESTION_BY_ID[qId]
  if (!q) return optId
  const opt = q.options.find((o) => o.id === optId)
  return opt?.label || optId
}
</script>

<style scoped>
.report-view {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

/* ===== Шапка ===== */
.report-head {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.back-btn {
  align-self: flex-start;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 0;
  background: none;
  border: none;
  color: var(--text-primary);
  font-family: inherit;
  font-size: var(--text-sm);
  cursor: pointer;
  min-height: 0;
  transition: all var(--transition-base);
}

.back-btn:hover {
  color: var(--accent-text);
}

.back-btn i {
  font-size: 12px;
}

.report-head h4 {
  margin: 0;
  font-size: var(--text-base);
}

.report-mileage {
  margin: 0;
  font-size: var(--text-sm);
  color: var(--text-muted);
}

/* ===== Пусто ===== */
.report-empty {
  padding: 40px 16px;
  text-align: center;
  color: var(--text-muted);
  font-size: var(--text-sm);
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  border: 1px dashed var(--border-color);
}

/* ===== Секции ===== */
.report-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.report-section h5 {
  margin: 0;
  font-size: 12px;
  font-weight: var(--fw-semibold);
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: var(--text-muted);
}

/* ===== Симптомы ===== */
.report-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.report-chip {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  background: var(--accent-trans);
  color: var(--accent-text);
  border-radius: var(--radius-full);
  font-size: 12.5px;
  font-weight: var(--fw-medium);
}

/* ===== Ответы ===== */
.report-answers {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.report-answer {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 10px 14px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-light);
}

.report-answer__q {
  font-size: 12px;
  color: var(--text-muted);
  line-height: var(--leading-base);
}

.report-answer__a {
  font-size: 13px;
  font-weight: var(--fw-medium);
  color: var(--text-primary);
}

/* ===== Результаты ===== */
.report-result {
  /* стили .diag-card уже в components.scss */
}

.report-result__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 8px;
}

.report-result__title {
  font-size: 14px;
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
}

.report-result__score {
  font-size: 13px;
  font-weight: var(--fw-bold);
  color: var(--accent-text);
  padding: 3px 9px;
  background: var(--accent-trans);
  border-radius: var(--radius-full);
  flex-shrink: 0;
}

.report-result__cause {
  margin: 0 0 6px;
  font-size: 13px;
  color: var(--text-secondary);
  line-height: var(--leading-base);
}

.report-result__advice {
  margin: 0;
  font-size: 13px;
  color: var(--text-secondary);
  line-height: var(--leading-base);
}

.report-result__advice strong {
  color: var(--text-primary);
  font-weight: var(--fw-semibold);
}

/* ===== Мобилка ===== */
@media (max-width: 640px) {
  .report-result__head {
    flex-direction: column;
    align-items: flex-start;
    gap: 6px;
  }
}
</style>
