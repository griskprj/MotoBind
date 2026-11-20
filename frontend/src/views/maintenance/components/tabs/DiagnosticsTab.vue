<template>
  <div class="diagnostics-tab">
    <IntroView
      v-if="store.view === 'intro'"
      :motorcycle="motorcycle"
      @start-node="store.startNodeDiagnostics($event)"
      @start-general="store.startGeneralDiagnostics"
      @open-history="store.goToHistory"
    />

    <WizardView
      v-else-if="store.view === 'wizard'"
      :motorcycle="motorcycle"
      @cancel="store.goToIntro"
    />

    <ResultView
      v-else-if="store.view === 'result'"
      :motorcycle="motorcycle"
      @restart="store.goToIntro"
      @open-history="store.goToHistory"
    />

    <HistoryView
      v-else-if="store.view === 'history'"
      @back="store.goToIntro"
      @open="store.openReport($event)"
      @delete="store.deleteReport($event)"
    />

    <ReportView
      v-else-if="store.view === 'report'"
      :report="store.currentReport"
      @back="store.closeReport"
    />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useDiagnosticsStore } from '@/stores'
import IntroView from '../diagnostics/IntroView.vue'
import WizardView from '../diagnostics/WizardView.vue'
import ResultView from '../diagnostics/ResultView.vue'
import HistoryView from '../diagnostics/HistoryView.vue'
import ReportView from '../diagnostics/ReportView.vue'

defineProps({
  motorcycle: { type: Object, default: null },
})

const store = useDiagnosticsStore()

onMounted(() => {
  store.reset()
  store.loadHistory().catch(() => {})
})
</script>

<style scoped>
.diagnostics-tab {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  width: 100%;
  min-width: 0;
}
</style>
