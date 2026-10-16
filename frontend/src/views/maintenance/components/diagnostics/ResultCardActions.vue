<template>
  <div class="result-card-actions">
    <!-- Мануалы -->
    <button
      v-if="manualsLoading"
      type="button"
      class="action-btn"
      disabled
    >
      <i class="fa fa-spinner fa-spin" />
      Ищем мануал...
    </button>

    <button
      v-else-if="manuals.length > 0"
      type="button"
      class="action-btn action-btn--manual"
      @click="openManual"
    >
      <i class="fa fa-book" />
      {{ manualsLabel }}
    </button>

    <!-- Мастер -->
    <button
      type="button"
      class="action-btn action-btn--master"
      @click="openMaster"
    >
      <i class="fa fa-user-gear" />
      Записаться к мастеру
    </button>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useDiagnosticsStore } from '@/stores'

const props = defineProps({
  rule: { type: Object, required: true },
  motorcycle: { type: Object, default: null },
})

const router = useRouter()
const store = useDiagnosticsStore()

const manuals = ref([])
const manualsLoading = ref(false)

const manualsLabel = computed(() => {
  if (manuals.value.length === 1) return 'Открыть мануал'
  return `Мануалы (${manuals.value.length})`
})

onMounted(async () => {
  if (!props.motorcycle?.id) return

  manualsLoading.value = true
  try {
    manuals.value = await store.findManualsForRule(
      props.rule.id,
      props.rule.category,
      props.motorcycle.id
    )
  } catch (err) {
    console.error('Failed to load manuals:', err)
    manuals.value = []
  } finally {
    manualsLoading.value = false
  }
})

function openManual() {
  if (manuals.value.length === 1) {
    router.push(`/manuals/${manuals.value[0].id}`)
  } else {
    router.push({
      path: '/manuals',
      query: { category: props.rule.category },
    })
  }
}

function openMaster() {
  router.push('/masters')
}
</script>

<style scoped>
.result-card-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--border-light);
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 12px;
  border-radius: var(--radius-md);
  font-family: inherit;
  font-size: 12.5px;
  font-weight: var(--fw-medium);
  cursor: pointer;
  transition: all var(--transition-base);
  min-height: 34px;
  border: 1px solid var(--border-color);
  background: var(--bg-primary);
  color: var(--text-secondary);
}

.action-btn:hover:not(:disabled) {
  border-color: var(--accent);
  color: var(--accent-text);
  background: var(--accent-trans);
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: default;
}

.action-btn--manual {
  border-color: var(--accent);
  color: var(--accent-text);
}

.action-btn--master {
  border-color: var(--border-color);
}
</style>
