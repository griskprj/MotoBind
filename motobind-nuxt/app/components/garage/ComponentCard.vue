<script setup lang="ts">
import type { MotorcycleComponent } from '~/types'

const props = defineProps<{
  component: MotorcycleComponent
  motorcycleId: number | string
}>()

const emit = defineEmits<{
  edit: []
  delete: []
  reactivate: []
  'open-event': [componentId: number]
}>()

const api = useApi()

const historyOpen = ref(false)
const history = ref<any[] | null>(null)
const historyLoading = ref(false)

const categoryLabel: Record<string, string> = {
  fluid: 'Жидкость',
  filter: 'Фильтр',
  ignition: 'Зажигание',
  brake: 'Тормоза',
  drive: 'Привод',
  other: 'Прочее',
}

const conditionLabel: Record<string, string> = {
  good: 'Хорошее',
  ok: 'Удовлетворительное',
  bad: 'Требует внимания',
  unknown: 'Без оценки',
}

const conditionVariant = computed(() => {
  switch (props.component.condition_rating) {
    case 'good':
      return 'success'
    case 'ok':
      return 'neutral'
    case 'bad':
      return 'danger'
    default:
      return 'neutral'
  }
})

const intervalText = computed(() => {
  const parts: string[] = []
  if (props.component.interval_km && props.component.interval_km > 0) {
    parts.push(`${props.component.interval_km.toLocaleString('ru-RU')} км`)
  }
  if (props.component.interval_days && props.component.interval_days > 0) {
    parts.push(`${props.component.interval_days} дн.`)
  }
  return parts.length ? parts.join(' / ') : 'Интервал не задан'
})

const lastServiceText = computed(() => {
  const d = props.component.last_service_date
  const m = props.component.last_service_mileage
  const parts: string[] = []
  if (d) parts.push(new Date(d).toLocaleDateString('ru-RU'))
  if (m != null) parts.push(`${m.toLocaleString('ru-RU')} км`)
  return parts.length ? parts.join(' · ') : 'Нет данных'
})

async function toggleHistory() {
  historyOpen.value = !historyOpen.value
  if (!historyOpen.value || history.value !== null) return
  historyLoading.value = true
  try {
    const res = await api.components.history(props.motorcycleId, props.component.id)
    history.value = res.history
  } catch {
    history.value = []
  } finally {
    historyLoading.value = false
  }
}
</script>

<template>
  <div class="comp-card" :class="{ 'comp-card--inactive': !component.is_active }">
    <div class="comp-main">
      <div class="comp-head">
        <div class="comp-name">
          {{ component.name }}
          <BaseBadge v-if="!component.is_active" variant="neutral" size="sm">
            Удалён
          </BaseBadge>
        </div>
        <div class="comp-badges">
          <BaseBadge variant="neutral" size="sm">
            {{ categoryLabel[component.category] || component.category }}
          </BaseBadge>
          <BaseBadge
            v-if="component.condition_rating"
            :variant="conditionVariant"
            size="sm"
          >
            {{ conditionLabel[component.condition_rating] }}
          </BaseBadge>
        </div>
      </div>

      <div class="comp-meta">
        <span><i class="fa-solid fa-road"></i> {{ intervalText }}</span>
        <span><i class="fa-solid fa-clock-rotate-left"></i> {{ lastServiceText }}</span>
        <span v-if="component.manufacturer">
          <i class="fa-solid fa-industry"></i> {{ component.manufacturer }}
        </span>
        <span v-if="component.part_number">
          <i class="fa-solid fa-barcode"></i> {{ component.part_number }}
        </span>
      </div>
    </div>

    <div class="comp-actions">
      <BaseButton
        v-if="component.is_active"
        variant="ghost"
        size="sm"
        @click="emit('open-event', component.id)"
      >
        <i class="fa-solid fa-wrench"></i>
      </BaseButton>
      <BaseButton variant="ghost" size="sm" @click="toggleHistory">
        <i class="fa-solid fa-clock-rotate-left"></i>
      </BaseButton>
      <BaseButton
        v-if="component.is_active"
        variant="ghost"
        size="sm"
        @click="emit('edit')"
      >
        <i class="fa-solid fa-pen"></i>
      </BaseButton>
      <BaseButton
        v-if="component.is_active"
        variant="ghost"
        size="sm"
        @click="emit('delete')"
      >
        <i class="fa-solid fa-trash"></i>
      </BaseButton>
      <BaseButton v-else variant="secondary" size="sm" @click="emit('reactivate')">
        Вернуть
      </BaseButton>
    </div>

    <div v-if="historyOpen" class="comp-history">
      <div v-if="historyLoading" class="comp-history-empty">Загрузка…</div>
      <div v-else-if="!history || history.length === 0" class="comp-history-empty">
        Работ по компоненту пока нет.
      </div>
      <ul v-else class="comp-history-list">
        <li v-for="h in history" :key="h.id" class="comp-history-item">
          <span class="ch-date">
            {{ h.event?.date ? new Date(h.event.date).toLocaleDateString('ru-RU') : '—' }}
          </span>
          <span class="ch-kind">{{ h.kind }}</span>
          <span v-if="h.cost" class="ch-cost">{{ h.cost.toLocaleString('ru-RU') }} ₽</span>
          <span v-if="h.note" class="ch-note">{{ h.note }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.comp-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-3);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.comp-card--inactive {
  opacity: 0.6;
}

.comp-main {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.comp-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.comp-name {
  font-weight: var(--fw-semibold);
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.comp-badges {
  display: flex;
  gap: var(--space-1);
  flex-wrap: wrap;
}

.comp-meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  font-size: var(--text-xs);
  color: var(--color-text-secondary);

  i {
    color: var(--color-text-tertiary);
    margin-right: 4px;
  }
}

.comp-actions {
  display: flex;
  gap: var(--space-1);
  justify-content: flex-end;
  flex-wrap: wrap;
}

.comp-history {
  border-top: 1px dashed var(--color-border);
  padding-top: var(--space-2);
}

.comp-history-empty {
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
}

.comp-history-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.comp-history-item {
  display: flex;
  gap: var(--space-2);
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
}

.ch-date {
  font-family: var(--font-mono);
}
.ch-kind {
  color: var(--color-brand);
  text-transform: uppercase;
}
.ch-cost {
  font-weight: var(--fw-semibold);
}
.ch-note {
  color: var(--color-text-tertiary);
}
</style>
