<script setup lang="ts">
import { SYMPTOM_GROUPS, SYMPTOMS, getRelevantQuestions, diagnose } from '~/utils/constants/diagnosticsRules'

const props = defineProps<{ motorcycleId?: number }>()
const emit = defineEmits<{ close: []; startSteps: [rule: any] }>()

const step = ref(1)
const selectedSymptoms = ref<Set<string>>(new Set())
const answers = ref<Record<string, string>>({})
const results = ref<any[]>([])

const symptomsByGroup = (groupId: string) => SYMPTOMS.filter(s => s.group === groupId)

function toggleSymptom(id: string) {
  const set = new Set(selectedSymptoms.value)
  set.has(id) ? set.delete(id) : set.add(id)
  selectedSymptoms.value = set
  answers.value = {}
}

const relevantQuestions = computed(() => getRelevantQuestions(selectedSymptoms.value))

function selectAnswer(qId: string, optId: string) {
  answers.value = { ...answers.value, [qId]: optId }
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

function startSteps(rule: any) {
  emit('startSteps', rule)
  emit('close')
}
</script>

<template>
  <BaseModal title="Онлайн-диагностика" size="lg" @close="emit('close')">
    <!-- ШАГ 1: Симптомы -->
    <div v-if="step === 1" class="diag-step">
      <p class="diag-intro">Отметьте всё, что замечаете в работе мотоцикла.</p>
      <div v-for="group in SYMPTOM_GROUPS" :key="group.id" class="symptom-group">
        <h4 class="group-title"><i :class="group.icon"></i> {{ group.label }}</h4>
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

    <!-- ШАГ 2: Вопросы -->
    <div v-else-if="step === 2" class="diag-step">
      <p class="diag-intro">Ответьте на уточняющие вопросы.</p>
      <div v-for="q in relevantQuestions" :key="q.id" class="question-block">
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

    <!-- ШАГ 3: Результат -->
    <div v-else class="diag-step">
      <div v-if="results.length === 0" class="result-empty">
        <i class="fa-solid fa-circle-question"></i>
        <h4>Точной причины не найдено</h4>
        <p>Рекомендуем обратиться к мастеру для очной диагностики.</p>
      </div>
      <div v-else class="result-list">
        <p class="diag-intro">Найдено возможных причин: <strong>{{ results.length }}</strong>.</p>
        <div v-for="r in results" :key="r.id" class="result-card" :class="`result-${r.severity}`">
          <div class="result-header">
            <div class="result-title">{{ r.title }}</div>
            <div class="result-score">{{ Math.round(r.score * 100) }}%</div>
          </div>
          <p class="result-cause">{{ r.cause }}</p>
          <p class="result-advice">{{ r.advice }}</p>
          <BaseButton variant="primary" size="sm" @click="startSteps(r)">
            <i class="fa-solid fa-play"></i> Начать пошаговую диагностику
          </BaseButton>
        </div>
      </div>
    </div>

    <!-- Кнопки навигации -->
    <template #footer>
      <div class="diag-actions">
        <BaseButton v-if="step > 1" variant="secondary" @click="step--">Назад</BaseButton>
        <BaseButton v-if="step === 1" variant="primary" :disabled="selectedSymptoms.size === 0" @click="step = 2">Продолжить</BaseButton>
        <BaseButton v-if="step === 2" variant="primary" :disabled="Object.keys(answers).length < relevantQuestions.length" @click="runDiagnostics">Диагностировать</BaseButton>
        <BaseButton v-if="step === 3" variant="secondary" @click="reset">Пройти заново</BaseButton>
      </div>
    </template>
  </BaseModal>
</template>
