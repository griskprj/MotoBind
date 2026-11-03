<script setup lang="ts">
import { ref, computed } from 'vue'
import { SYMPTOM_GROUPS, SYMPTOMS, getRelevantQuestions, diagnose } from '~/utils/constants/diagnosticsRules'

const props = defineProps<{
  motorcycle: any
}>()

const selectedSymptoms = ref<Set<string>>(new Set())
const answers = ref<Record<string, string>>({})
const results = ref<any[]>([])
const selectedRule = ref<any>(null)

const symptomsByGroup = (groupId: string) => SYMPTOMS.filter(s => s.group === groupId)

function toggleSymptom(id: string) {
  const set = new Set(selectedSymptoms.value)
  if (set.has(id)) set.delete(id)
  else set.add(id)
  selectedSymptoms.value = set
  answers.value = {}
  results.value = []
  selectedRule.value = null
}

const relevantQuestions = computed(() => getRelevantQuestions(selectedSymptoms.value))

const activeZoneFilter = ref<string | null>(null)

const activeZones = computed(() => {
  const set = new Set<string>()
  for (const id of selectedSymptoms.value) {
    const symptom = SYMPTOMS.find(s => s.id === id)
    if (symptom) set.add(symptom.group)
  }
  return Array.from(set)
})

function onZoneClick(zoneId: string) {
  activeZoneFilter.value = activeZoneFilter.value === zoneId ? null : zoneId
}

function selectAnswer(qId: string, optId: string) {
  answers.value = { ...answers.value, [qId]: optId }
}

function runDiagnostics() {
  results.value = diagnose(selectedSymptoms.value, answers.value)
}

function reset() {
  selectedSymptoms.value = new Set()
  answers.value = {}
  results.value = []
  selectedRule.value = null
}

function startSteps(rule: any) {
  selectedRule.value = rule
}

function closeSteps() {
  selectedRule.value = null
}

const selectedSymptomLabels = computed(() =>
  Array.from(selectedSymptoms.value)
    .map(id => SYMPTOMS.find(s => s.id === id)?.label)
    .filter(Boolean)
)
</script>

<template>
  <div class="diagnostics-tab">
    <!-- 1. Баннер -->
    <div class="diag-banner">
      <div class="banner-icon">
        <i class="fa-solid fa-heart-pulse"></i>
      </div>
      <div class="banner-content">
        <h2 class="banner-title">Диагностика неисправностей</h2>
        <p class="banner-subtitle">Найдите возможную причину проблемы и пошаговый план проверки для вашего мотоцикла</p>
      </div>
    </div>

    <!-- 2. Симптомы -->
    <section class="block">
      <div class="block-header">
        <h3 class="block-title">Что происходит?</h3>
        <span v-if="selectedSymptoms.size > 0" class="selected-count">
          Выбрано: {{ selectedSymptoms.size }}
        </span>
      </div>

      <div class="symptom-groups">
        <div v-for="group in SYMPTOM_GROUPS" :key="group.id" class="symptom-group">
          <h4 class="group-title">
            <i :class="group.icon"></i> {{ group.label }}
          </h4>
          <div class="symptom-chips">
            <button
              v-for="s in symptomsByGroup(group.id)"
              :key="s.id"
              class="symptom-chip"
              :class="{ active: selectedSymptoms.has(s.id) }"
              @click="toggleSymptom(s.id)"
            >
              <i :class="s.icon"></i> {{ s.label }}
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- 3. Вопросы -->
    <section v-if="selectedSymptoms.size > 0 && results.length === 0" class="block">
      <div class="block-header">
        <h3 class="block-title">Уточняющие вопросы</h3>
        <button class="reset-link" @click="reset">
          <i class="fa-solid fa-rotate-right"></i> Сбросить
        </button>
      </div>

      <div class="selected-symptoms">
        <span
          v-for="label in selectedSymptomLabels"
          :key="label"
          class="selected-tag"
        >
          {{ label }}
        </span>
      </div>

      <div v-if="relevantQuestions.length === 0" class="empty-state">
        <i class="fa-solid fa-circle-info"></i>
        <p>Для выбранных симптомов уточняющих вопросов нет. Нажмите «Диагностировать».</p>
      </div>

      <div v-else class="questions-list">
        <div v-for="q in relevantQuestions" :key="q.id" class="question-item">
          <p class="question-text">{{ q.text }}</p>
          <div class="question-options">
            <button
              v-for="opt in q.options"
              :key="opt.id"
              class="option-chip"
              :class="{ active: answers[q.id] === opt.id }"
              @click="selectAnswer(q.id, opt.id)"
            >
              {{ opt.label }}
            </button>
          </div>
        </div>
      </div>

      <div class="block-actions">
        <BaseButton
          variant="primary"
          :disabled="Object.keys(answers).length < relevantQuestions.length"
          @click="runDiagnostics"
        >
          <i class="fa-solid fa-bolt"></i> Диагностировать
        </BaseButton>
      </div>
    </section>

    <!-- 4. Результаты -->
    <section v-if="results.length > 0" class="block">
      <div class="block-header">
        <h3 class="block-title">Возможные причины</h3>
        <button class="reset-link" @click="reset">
          <i class="fa-solid fa-rotate-right"></i> Пройти заново
        </button>
      </div>

      <div v-if="results.length === 0" class="empty-state">
        <i class="fa-solid fa-circle-question"></i>
        <p>Точной причины не найдено. Рекомендуем обратиться к мастеру.</p>
      </div>

      <div v-else class="results-list">
        <div
          v-for="r in results"
          :key="r.id"
          class="result-card"
          :class="`severity-${r.severity}`"
        >
          <div class="result-top">
            <div class="result-icon">
              <i class="fa-solid fa-triangle-exclamation"></i>
            </div>
            <div class="result-main">
              <h4 class="result-title">{{ r.title }}</h4>
              <p class="result-cause">{{ r.cause }}</p>
              <p class="result-advice">{{ r.advice }}</p>
            </div>
            <div class="result-score">{{ Math.round(r.score * 100) }}%</div>
          </div>
          <div class="result-actions">
            <BaseButton variant="primary" size="sm" @click="startSteps(r)">
              <i class="fa-solid fa-play"></i> Начать пошаговую диагностику
            </BaseButton>
          </div>
        </div>
      </div>
    </section>

    <DiagnosticsZones
      :active-zones="activeZones"
      @zone-click="onZoneClick"
    />

    <!-- 5. Модалка с шагами -->
    <DiagnosticsStep
      v-if="selectedRule"
      :rule="selectedRule"
      @close="closeSteps"
    />
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.diagnostics-tab {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  color: var(--color-text-primary);
}

/* Баннер */
.diag-banner {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-5);
  background: linear-gradient(90deg, rgba(112, 0, 255, 0.15) 0%, rgba(20, 20, 25, 1) 100%);
  border-radius: var(--radius-lg);
  border: 1px solid rgba(112, 0, 255, 0.3);
}

.banner-icon {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  background: rgba(112, 0, 255, 0.2);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #a855f7;
  font-size: 24px;
}

.banner-title {
  font-size: var(--text-xl);
  font-weight: var(--fw-bold);
  margin-bottom: var(--space-1);
}

.banner-subtitle {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

/* Блоки */
.block {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
}

.block-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-3);
  flex-wrap: wrap;
  gap: var(--space-2);
}

.block-title {
  font-size: var(--text-lg);
  font-weight: var(--fw-semibold);
}

.selected-count {
  font-size: var(--text-xs);
  color: var(--color-brand);
  background: var(--color-brand-soft);
  padding: 2px 8px;
  border-radius: var(--radius-full);
}

.reset-link {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  font-size: var(--text-sm);
  display: flex;
  align-items: center;
  gap: var(--space-1);
  transition: color 0.2s;

  &:hover {
    color: var(--color-brand);
  }
}

/* Симптомы */
.symptom-groups {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);

  @include md-up {
    grid-template-columns: 1fr 1fr;
  }

  @include lg-up {
    grid-template-columns: repeat(3, 1fr);
  }
}

.symptom-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.group-title {
  font-size: var(--text-xs);
  font-weight: var(--fw-semibold);
  text-transform: uppercase;
  color: var(--color-text-tertiary);
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

.symptom-chips {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.symptom-chip {
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-full);
  border: 1px solid var(--color-border);
  background: var(--color-surface-secondary);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  gap: var(--space-1);

  &:hover {
    border-color: var(--color-brand);
    color: var(--color-brand);
  }

  &.active {
    background: var(--color-brand);
    border-color: var(--color-brand);
    color: #fff;
  }

  i {
    font-size: 12px;
  }
}

/* Выбранные теги */
.selected-symptoms {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-bottom: var(--space-4);
}

.selected-tag {
  font-size: var(--text-xs);
  padding: 4px 10px;
  border-radius: var(--radius-full);
  background: rgba(112, 0, 255, 0.15);
  color: #a855f7;
  border: 1px solid rgba(112, 0, 255, 0.3);
}

/* Вопросы */
.questions-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.question-item {
  padding: var(--space-3);
  background: var(--color-surface-secondary);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
}

.question-text {
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  margin-bottom: var(--space-2);
}

.question-options {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.option-chip {
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    border-color: var(--color-brand);
  }

  &.active {
    background: var(--color-brand);
    border-color: var(--color-brand);
    color: #fff;
  }
}

.block-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: var(--space-4);
}

/* Результаты */
.results-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.result-card {
  padding: var(--space-4);
  border-radius: var(--radius-md);
  background: var(--color-surface-secondary);
  border: 1px solid var(--color-border);
  border-left: 4px solid var(--color-border);

  &.severity-danger { border-left-color: #ef4444; }
  &.severity-warning { border-left-color: #f59e0b; }
  &.severity-info { border-left-color: #3b82f6; }
}

.result-top {
  display: flex;
  gap: var(--space-3);
  align-items: flex-start;
}

.result-icon {
  color: var(--color-text-tertiary);
  font-size: 18px;
  margin-top: 2px;
  flex-shrink: 0;
}

.result-main {
  flex: 1;
  min-width: 0;
}

.result-title {
  font-size: var(--text-base);
  font-weight: var(--fw-semibold);
  margin-bottom: var(--space-1);
}

.result-cause,
.result-advice {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-1);
}

.result-advice {
  color: var(--color-text-primary);
}

.result-score {
  font-size: var(--text-sm);
  font-weight: var(--fw-bold);
  color: var(--color-text-primary);
  background: var(--color-surface);
  padding: 2px 10px;
  border-radius: var(--radius-full);
  border: 1px solid var(--color-border);
  flex-shrink: 0;
}

.result-actions {
  margin-top: var(--space-3);
  display: flex;
  justify-content: flex-end;
}

/* Пустое состояние */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-6);
  color: var(--color-text-tertiary);
  text-align: center;
  background: var(--color-surface-secondary);
  border-radius: var(--radius-md);
  border: 1px dashed var(--color-border);

  i { font-size: 28px; }
  p { font-size: var(--text-sm); }
}
</style>
