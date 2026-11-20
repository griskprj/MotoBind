<template>
  <ModalWrapper
    :is-open="isOpen"
    :title="stepTitle"
    :subtitle="stepSubtitle"
    :icon="stepIcon"
    :icon-color="stepIconColor"
    :bg-icon-color="stepIconBg"
    size="lg"
    @close="close"
  >
    <!-- ============ ШАГ 1: СИМПТОМЫ ============ -->
    <template v-if="step === 1">
      <p class="diag-intro">
        Отметьте всё, что замечаете в работе мотоцикла. Можно выбрать несколько пунктов.
      </p>

      <div v-for="group in SYMPTOM_GROUPS" :key="group.id" class="symptom-group">
        <div class="symptom-group-title">
          <i :class="group.icon"></i>
          {{ group.label }}
        </div>
        <div class="symptom-chips">
          <button
            v-for="s in symptomsByGroup(group.id)"
            :key="s.id"
            type="button"
            class="symptom-chip"
            :class="{ active: selectedSymptoms.has(s.id) }"
            @click="toggleSymptom(s.id)"
          >
            <i :class="s.icon"></i>
            <span>{{ s.label }}</span>
          </button>
        </div>
      </div>

      <div v-if="selectedSymptoms.size === 0" class="diag-empty">
        <i class="fa fa-info-circle"></i>
        <span>Выберите хотя бы один симптом, чтобы продолжить</span>
      </div>
      <div v-else class="diag-summary">
        Выбрано симптомов: <strong>{{ selectedSymptoms.size }}</strong>
      </div>
    </template>

    <!-- ============ ШАГ 2: ВОПРОСЫ ============ -->
    <template v-else-if="step === 2">
      <p class="diag-intro">
        Ответьте на несколько уточняющих вопросов — это поможет точнее определить причину.
      </p>

      <div v-for="q in relevantQuestions" :key="q.id" class="question-block">
        <div class="question-text">{{ q.text }}</div>
        <div class="question-options">
          <button
            v-for="opt in q.options"
            :key="opt.id"
            type="button"
            class="option-chip"
            :class="{ active: answers[q.id] === opt.id }"
            @click="selectAnswer(q.id, opt.id)"
          >
            {{ opt.label }}
          </button>
        </div>
      </div>

      <div class="diag-summary">
        Отвечено: <strong>{{ answeredCount }}</strong> из {{ relevantQuestions.length }}
      </div>
    </template>

    <!-- ============ ШАГ 3: РЕЗУЛЬТАТ ============ -->
    <template v-else-if="step === 3">
      <div v-if="results.length === 0" class="result-empty">
        <i class="fa fa-circle-question"></i>
        <h4>Точной причины не найдено</h4>
        <p>
          По указанным симптомам не удалось подобрать однозначную причину.
          Рекомендуем обратиться к мастеру для очной диагностики.
        </p>
        <button class="btn-primary" @click="openMaster">
          <i class="fa fa-user-gear"></i>
          Записаться к мастеру
        </button>
      </div>

      <div v-else class="result-list">
        <p class="diag-intro">
          Найдено возможных причин: <strong>{{ results.length }}</strong>.
          Чем выше совпадение — тем вероятнее причина.
        </p>

        <div
          v-for="r in results"
          :key="r.id"
          class="result-card"
          :class="'result-' + r.severity"
        >
          <div class="result-head">
            <div class="result-severity">
              <i :class="severityIcon(r.severity)"></i>
            </div>
            <div class="result-head-text">
              <div class="result-title">{{ r.title }}</div>
              <div class="result-category">{{ categoryLabel(r.category) }}</div>
            </div>
            <div class="result-score">
              {{ Math.round(r.score * 100) }}%
            </div>
          </div>

          <div class="result-body">
            <div class="result-row">
              <span class="result-label">Причина</span>
              <p class="result-value">{{ r.cause }}</p>
            </div>
            <div class="result-row">
              <span class="result-label">Рекомендация</span>
              <p class="result-value">{{ r.advice }}</p>
            </div>
          </div>
        </div>

        <div class="result-disclaimer">
          <i class="fa fa-triangle-exclamation"></i>
          Результат не заменяет профессиональную диагностику. При сомнениях обратитесь к мастеру.
        </div>

        <button class="btn-outline result-master-btn" @click="openMaster">
          <i class="fa fa-user-gear"></i>
          Записаться к мастеру
        </button>
      </div>
    </template>

    <!-- ============ ДЕЙСТВИЯ ============ -->
    <template #actions>
      <div class="diag-actions">
        <button
          v-if="step > 1"
          class="btn-secondary"
          @click="prevStep"
        >
          <i class="fa fa-arrow-left"></i>
          Назад
        </button>

        <button
          v-if="step === 1"
          class="btn-primary"
          :disabled="selectedSymptoms.size === 0"
          @click="nextStep"
        >
          Продолжить
          <i class="fa fa-arrow-right"></i>
        </button>

        <button
          v-else-if="step === 2"
          class="btn-primary"
          :disabled="answeredCount < relevantQuestions.length"
          @click="runDiagnostics"
        >
          <i class="fa fa-stethoscope"></i>
          Диагностировать
        </button>

        <button
          v-else
          class="btn-primary"
          @click="reset"
        >
          <i class="fa fa-rotate-right"></i>
          Пройти заново
        </button>
      </div>
    </template>
  </ModalWrapper>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import ModalWrapper from '../../modals/ModalWrapper.vue'
import {
  SYMPTOM_GROUPS,
  SYMPTOMS,
  diagnose,
  getRelevantQuestions,
} from '../../../constants/diagnisticsRules'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
})

const emit = defineEmits(['close', 'write-to-master'])

// ===== Состояние =====
const step = ref(1)
const selectedSymptoms = ref(new Set())
const answers = ref({})
const results = ref([])

// ===== Вычисляемые =====
const relevantQuestions = computed(() => getRelevantQuestions(selectedSymptoms.value))
const answeredCount = computed(() => {
  return relevantQuestions.value.filter((q) => answers.value[q.id]).length
})

const stepTitle = computed(() => ({
  1: 'Онлайн-диагностика',
  2: 'Уточняющие вопросы',
  3: 'Результат диагностики',
}[step.value]))

const stepSubtitle = computed(() => ({
  1: 'Выберите симптомы',
  2: `${answeredCount.value} из ${relevantQuestions.value.length} отвечено`,
  3: results.value.length ? 'Возможные причины' : 'Нужна очная диагностика',
}[step.value]))

const stepIcon = computed(() => ({
  1: 'stethoscope',
  2: 'circle-question',
  3: 'clipboard-check',
}[step.value]))

const stepIconColor = computed(() => {
  if (step.value === 3) {
    return results.value.length ? 'var(--success-text)' : 'var(--warning-text)'
  }
  return 'var(--accent-text)'
})
const stepIconBg = computed(() => {
  if (step.value === 3) {
    return results.value.length ? 'var(--success-trans)' : 'var(--warning-trans)'
  }
  return 'var(--accent-trans)'
})

// ===== Методы =====
function symptomsByGroup(groupId) {
  return SYMPTOMS.filter((s) => s.group === groupId)
}

function toggleSymptom(id) {
  const set = new Set(selectedSymptoms.value)
  if (set.has(id)) set.delete(id)
  else set.add(id)
  selectedSymptoms.value = set
}

function selectAnswer(questionId, optionId) {
  answers.value = { ...answers.value, [questionId]: optionId }
}

function nextStep() {
  if (step.value < 3) step.value++
}

function prevStep() {
  if (step.value > 1) step.value--
}

function runDiagnostics() {
  results.value = diagnose(selectedSymptoms.value, answers.value)
  step.value = 3
}

function reset() {
  step.value = 1
  selectedSymptoms.value = new Set()
  answers.value = {}
  results.value = []
}

function close() {
  emit('close')
  setTimeout(reset, 300)
}

function openMaster() {
  emit('write-to-master')
  close()
}

function severityIcon(severity) {
  return {
    info:    'fa fa-circle-info',
    warning: 'fa fa-triangle-exclamation',
    danger:  'fa fa-circle-exclamation',
  }[severity] || 'fa fa-circle-info'
}

function categoryLabel(category) {
  const map = {
    engine: 'Двигатель',
    drive: 'Привод',
    brakes: 'Тормоза',
    electrics: 'Электрика',
    suspension: 'Подвеска',
    wheels: 'Колёса',
  }
  return map[category] || category
}

// Сброс при закрытии
watch(() => props.isOpen, (open) => {
  if (!open) setTimeout(reset, 300)
})
</script>

<style scoped>
/* ===== INTRO ===== */
.diag-intro {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0 0 16px;
  line-height: var(--leading-base);
}

/* ===== SYMPTOM GROUPS ===== */
.symptom-group {
  margin-bottom: 16px;
}

.symptom-group-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: var(--fw-semibold);
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: var(--text-muted);
  margin-bottom: 8px;
}
.symptom-group-title i { color: var(--accent-text); font-size: 13px; }

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
.symptom-chip i { font-size: 11px; }

/* ===== QUESTIONS ===== */
.question-block {
  margin-bottom: 16px;
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

/* ===== SUMMARY / EMPTY ===== */
.diag-summary {
  margin-top: 16px;
  padding: 10px 14px;
  background: var(--accent-trans);
  border-radius: var(--radius-md);
  font-size: 13px;
  color: var(--text-secondary);
  text-align: center;
}
.diag-summary strong { color: var(--accent-text); }

.diag-empty {
  margin-top: 16px;
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

/* ===== RESULTS ===== */
.result-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.result-card {
  padding: 14px 16px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-light);
  background: var(--bg-secondary);
  border-left: 3px solid var(--border-color);
}
.result-info    { border-left-color: var(--info); }
.result-warning { border-left-color: var(--warning); }
.result-danger  { border-left-color: var(--danger); }

.result-head {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.result-severity {
  width: 34px;
  height: 34px;
  min-height: 34px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: var(--bg-primary);
  color: var(--text-secondary);
  font-size: 15px;
}
.result-info    .result-severity { background: var(--info-trans);    color: var(--info-text); }
.result-warning .result-severity { background: var(--warning-trans); color: var(--warning-text); }
.result-danger  .result-severity { background: var(--danger-trans);  color: var(--danger-text); }

.result-head-text { flex: 1; min-width: 0; }
.result-title {
  font-size: 14px;
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
}
.result-category {
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.result-score {
  font-size: 14px;
  font-weight: var(--fw-bold);
  color: var(--accent-text);
  padding: 4px 10px;
  background: var(--accent-trans);
  border-radius: var(--radius-full);
  flex-shrink: 0;
}

.result-body {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-left: 44px;
}

.result-row { display: flex; flex-direction: column; gap: 2px; }
.result-label {
  font-size: 10px;
  font-weight: var(--fw-semibold);
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: var(--text-muted);
}
.result-value {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0;
  line-height: var(--leading-base);
}

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
  margin-top: 8px;
}
.result-disclaimer i { color: var(--warning-text); margin-top: 2px; }

.result-master-btn {
  margin-top: 8px;
  width: 100%;
  padding: 10px 16px;
  border-radius: var(--radius-md);
  border: 1px solid var(--accent);
  background: transparent;
  color: var(--accent-text);
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
.result-master-btn:hover {
  background: var(--accent-trans);
  color: var(--text-primary);
}

/* Пусто */
.result-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 10px;
  padding: 20px 8px;
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
  max-width: 320px;
}
.result-empty .btn-primary {
  margin-top: 8px;
  padding: 10px 20px;
  border-radius: var(--radius-md);
  background: var(--accent);
  color: #fff;
  border: none;
  font-size: 13px;
  font-weight: var(--fw-semibold);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 40px;
}
.result-empty .btn-primary:hover { background: var(--accent-hover); }

/* ===== ACTIONS ===== */
.diag-actions {
  display: flex;
  gap: 8px;
}
.diag-actions .btn-secondary,
.diag-actions .btn-primary {
  flex: 1;
  padding: 10px 16px;
  border-radius: var(--radius-md);
  font-size: 13px;
  font-weight: var(--fw-semibold);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 42px;
  border: none;
  transition: all var(--transition-base);
}
.diag-actions .btn-primary {
  background: var(--accent);
  color: #fff;
}
.diag-actions .btn-primary:hover:not(:disabled) { background: var(--accent-hover); }
.diag-actions .btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
.diag-actions .btn-secondary {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}
.diag-actions .btn-secondary:hover { background: var(--border-light); }

/* ===== MOBILE ===== */
@media (max-width: 640px) {
  .result-body { padding-left: 0; }
  .result-score { font-size: 12px; padding: 3px 8px; }
  .symptom-chip { font-size: 12px; padding: 6px 10px; }
}
</style>
