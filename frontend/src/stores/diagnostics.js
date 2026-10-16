import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import api from '../api/api'
import {
  diagnose as runEngine,
  getRelevantQuestions,
  SYMPTOM_BY_ID,
} from '../constants/diagnisticsRules'

export const useDiagnosticsStore = defineStore('diagnostics', () => {
  // ===== State =====
  const view = ref('intro') // 'intro' | 'wizard' | 'result' | 'history' | 'report'
  const step = ref(1)

  const lockedGroup = ref(null) // 'engine' | ... | null (общая диагностика)
  const selectedSymptoms = ref(new Set())
  const answers = ref({})
  const manualsCache = ref({})

  const results = ref([])
  const lastReportId = ref(null)
  const saving = ref(false)

  const reports = ref([])
  const reportsLoaded = ref(false)
  const currentReport = ref(null)

  // ===== Getters =====

  /** Релевантные вопросы для текущих симптомов и lockedGroup */
  const relevantQuestions = computed(() =>
    getRelevantQuestions(selectedSymptoms.value, {
      lockedGroup: lockedGroup.value,
    })
  )

  const totalQuestions = computed(() => relevantQuestions.value.length)

  const answeredCount = computed(
    () => relevantQuestions.value.filter((q) => answers.value[q.id] !== undefined).length
  )

  /** Можно ли идти дальше с шага симптомов */
  const canProceedFromSymptoms = computed(() => selectedSymptoms.value.size > 0)

  /** Можно ли запустить диагностику с шага вопросов */
  const canRunDiagnostics = computed(
    () =>
      selectedSymptoms.value.size > 0 &&
      answeredCount.value === totalQuestions.value
  )

  /** Топ-результат (для превью / бейджей) */
  const topResult = computed(() => results.value[0] || null)

  /** Есть ли среди результатов опасные */
  const hasDanger = computed(() =>
    results.value.some((r) => r.severity === 'danger')
  )

  /** Есть ли среди результатов предупреждения */
  const hasWarning = computed(() =>
    results.value.some((r) => r.severity === 'warning')
  )

  /** Общее число сохранённых отчётов */
  const reportCount = computed(() => reports.value.length)

  // ===== Actions — навигация =====

  function startNodeDiagnostics(group) {
    lockedGroup.value = group
    resetWizardState()
    view.value = 'wizard'
    step.value = 1
  }

  function startGeneralDiagnostics() {
    lockedGroup.value = null
    resetWizardState()
    view.value = 'wizard'
    step.value = 1
  }

  function goToQuestions() {
    if (!canProceedFromSymptoms.value) return
    step.value = 2
  }

  function goBackToSymptoms() {
    step.value = 1
  }

  function goToIntro() {
    resetAll()
    view.value = 'intro'
  }

  function goToHistory() {
    view.value = 'history'
    if (!reportsLoaded.value) {
      loadHistory().catch(() => {
        console.error('Failed to load history:', err)
      })
    }
  }

  function openReport(id) {
    const cached = reports.value.find((r) => r.id === id)
    if (cached) {
      currentReport.value = cached
      view.value = 'report'
      return Promise.resolve(cached)
    }
    return api
      .get(`/diagnostics/reports/${id}`)
      .then(({ data }) => {
        currentReport.value = data
        view.value = 'report'
        return data
      })
  }

  function closeReport() {
    currentReport.value = null
    view.value = 'history'
  }

  // ===== Actions — ввод =====

  function toggleSymptom(id) {
    const next = new Set(selectedSymptoms.value)
    next.has(id) ? next.delete(id) : next.add(id)
    selectedSymptoms.value = next

    const validIds = new Set(
      getRelevantQuestions(next, { lockedGroup: lockedGroup.value }).map((q) => q.id)
    )
    const cleaned = {}
    for (const [qId, optId] of Object.entries(answers.value)) {
      if (validIds.has(qId)) cleaned[qId] = optId
    }
    answers.value = cleaned
  }

  function setAnswer(questionId, optionId) {
    answers.value = { ...answers.value, [questionId]: optionId }
  }

  function clearAnswer(questionId) {
    const { [questionId]: _, ...rest } = answers.value
    answers.value = rest
  }

  // ===== Actions — движок =====

  function runDiagnostics() {
    if (!canRunDiagnostics.value) return
    results.value = runEngine(selectedSymptoms.value, answers.value, {
      lockedGroup: lockedGroup.value,
    })
    view.value = 'result'
  }

  // ===== Actions — сохранение =====

  /**
   * @param {{ motorcycleId?: number, mileage?: number }} payload
   */
  async function saveReport({ motorcycleId = null, mileage = null } = {}) {
    if (results.value.length === 0) return null

    saving.value = true
    try {
      const payload = {
        motorcycle_id: motorcycleId,
        mileage,
        locked_group: lockedGroup.value,
        symptoms: [...selectedSymptoms.value],
        answers: { ...answers.value },
        results: results.value.map((r) => ({
          rule_id: r.id,
          score: Math.round(r.score * 100) / 100,
        })),
      }

      const { data } = await api.post('/diagnostics/reports', payload)
      lastReportId.value = data.id

      reports.value = [data, ...reports.value]
      reportsLoaded.value = true

      return data
    } finally {
      saving.value = false
    }
  }

  async function loadHistory(force = false) {
    if (reportsLoaded.value && !force) return reports.value

    const { data } = await api.get('/diagnostics/reports')
    reports.value = Array.isArray(data) ? data : []
    reportsLoaded.value = true
    return reports.value
  }

  async function deleteReport(id) {
    await api.delete(`/diagnostics/reports/${id}`)
    reports.value = reports.value.filter((r) => r.id !== id)
    if (currentReport.value?.id === id) {
      currentReport.value = null
      view.value = 'history'
    }
  }

  // ===== Actions — сброс =====

  function resetWizardState() {
    selectedSymptoms.value = new Set()
    answers.value = {}
    results.value = []
    lastReportId.value = null
    saving.value = false
  }

  function resetAll() {
    resetWizardState()
    lockedGroup.value = null
    step.value = 1
  }

  function reset() {
    resetAll()
    view.value = 'intro'
    reports.value = []
  }

  function clearMaintenancesCache() {
    manualsCache.value = {}
  }

  // ===== Actions - поиск =====

  /**
   * Ищет мануалы для правила диагностики.
   * @param {string} ruleId
   * @param {string} category
   * @param {number} motoId
   * @returns {Promise<Array>}
   */
  async function findManualsForRule(ruleId, category, motoId) {
    if (manualsCache.value[ruleId]) return manualsCache.value[ruleId]

    const { data } = await api.get(`/diagnostics/rules/${ruleId}/manuals`, {
      params: { category, moto_id: motoId },
    })
    const list = Array.isArray(data) ? data : []
    manualsCache.value = { ...manualsCache.value, [ruleId]: list }
    return Array.isArray(data) ? data : []
  }

  // ===== Возврат =====

  return {
    // state
    view,
    step,
    lockedGroup,
    selectedSymptoms,
    answers,
    results,
    lastReportId,
    saving,
    reports,
    reportsLoaded,
    currentReport,

    // getters
    relevantQuestions,
    totalQuestions,
    answeredCount,
    canProceedFromSymptoms,
    canRunDiagnostics,
    topResult,
    hasDanger,
    hasWarning,
    reportCount,

    // navigation
    startNodeDiagnostics,
    startGeneralDiagnostics,
    goToQuestions,
    goBackToSymptoms,
    goToIntro,
    goToHistory,
    openReport,
    closeReport,

    // input
    toggleSymptom,
    setAnswer,
    clearAnswer,

    // engine
    runDiagnostics,

    // save
    saveReport,
    loadHistory,
    deleteReport,

    // reset
    resetWizardState,
    resetAll,
    reset,

    //find
    findManualsForRule,
  }
})
