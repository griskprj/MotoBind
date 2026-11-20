<script setup lang="ts">
import type {
  ApiError,
  MaintenanceEvent,
  MotorcycleComponent,
  WorkKind,
  CreateWorkPayload,
} from '~/types'

const props = defineProps<{
  motorcycleId: number | string
  currentMileage: number | null
  components: MotorcycleComponent[]
  initialComponentId?: number | null
  event?: MaintenanceEvent | null
}>()

const emit = defineEmits<{
  saved: []
  cancel: []
}>()

const api = useApi()
const toast = useToast()
const { errors, setFromApiError, clear } = useFormErrors()

const saving = ref(false)
const isEdit = computed(() => !!props.event)

type WorkRow = {
  component_id: number | null
  kind: WorkKind
  title: string
  cost: string | number
  note: string
}

const form = reactive({
  date: new Date().toISOString().slice(0, 10),
  mileage: '' as string | number,
  total_cost: '' as string | number,
  comment: '',
  works: [] as WorkRow[],
})

function formatDateForInput(dateVal: any): string {
  if (!dateVal) return new Date().toISOString().slice(0, 10)

  const parsed = new Date(dateVal)

  if (!isNaN(parsed.getTime())) {
    const yyyy = parsed.getFullYear()
    const mm = String(parsed.getMonth() + 1).padStart(2, '0')
    const dd = String(parsed.getDate()).padStart(2, '0')
    return `${yyyy}-${mm}-${dd}`
  }

  return new Date().toISOString().slice(0, 10)
}

onMounted(() => {
  if (props.event) {
    form.date = formatDateForInput(props.event.date)
    form.mileage = props.event.mileage ?? ''
    form.total_cost = props.event.total_cost ?? ''
    form.comment = props.event.comment || ''
    form.works = props.event.works.map((w) => ({
      component_id: w.component_id,
      kind: w.kind,
      title: w.title || '',
      cost: w.cost ?? '',
      note: w.note || '',
    }))
  } else {
    form.date = new Date().toISOString().slice(0, 10)
    form.mileage = props.currentMileage ?? ''
    if (props.initialComponentId) {
      form.works = [
        {
          component_id: props.initialComponentId,
          kind: 'replace',
          title: '',
          cost: '',
          note: '',
        },
      ]
    } else {
      addWork()
    }
  }
})

const kindOptions = [
  { value: 'replace', label: 'Замена' },
  { value: 'inspect', label: 'Осмотр' },
  { value: 'adjust', label: 'Регулировка' },
  { value: 'repair', label: 'Ремонт' },
  { value: 'other', label: 'Другое' },
]

const componentOptions = computed(() => [
  { value: '', label: '— без компонента —' },
  ...props.components
    .filter((c) => c.is_active)
    .map((c) => ({ value: String(c.id), label: c.name })),
])

function addWork() {
  form.works.push({
    component_id: null,
    kind: 'replace',
    title: '',
    cost: '',
    note: '',
  })
}

function removeWork(idx: number) {
  form.works.splice(idx, 1)
}

function onComponentChange(row: WorkRow, value: string | number) {
  row.component_id = value === '' ? null : Number(value)
  if (row.component_id) {
    const c = props.components.find((x) => x.id === row.component_id)
    if (c && !row.title) row.title = c.name
  }
}

async function onSave() {
  clear()
  saving.value = true
  try {
    const works: CreateWorkPayload[] = form.works.map((w) => ({
      component_id: w.component_id,
      kind: w.kind,
      title: w.title.trim() || null,
      cost: w.cost === '' ? 0 : Number(w.cost),
      note: w.note.trim() || null,
    }))

    const payload = {
      motorcycleId: props.motorcycleId,
      date: form.date,
      mileage: form.mileage === '' ? null : Number(form.mileage),
      totalCost: form.total_cost === '' ? null : Number(form.total_cost),
      comment: form.comment.trim() || null,
      works,
    }

    if (isEdit.value && props.event) {
      await api.maintenance.events.update(props.event.id, props.motorcycleId, payload)
      toast.success('Событие обновлено')
    } else {
      await api.maintenance.events.create(payload)
      toast.success('Событие создано')
    }
    emit('saved')
  } catch (e) {
    const err = e as ApiError
    setFromApiError(err)
    if (!err.fieldErrors) toast.error(err.message || 'Ошибка сохранения')
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <form class="event-form" @submit.prevent="onSave">
    <div class="form-grid">
      <BaseInput v-model="form.date" type="date" label="Дата" required :error="errors.date" />
      <BaseInput v-model="form.mileage" type="number" label="Пробег, км" :error="errors.mileage" />
      <BaseInput
        v-model="form.total_cost"
        type="number"
        label="Общая стоимость, ₽"
        hint="Пусто — сумма работ"
        :error="errors.total_cost"
      />
      <BaseInput v-model="form.comment" label="Комментарий" class="span-2" :error="errors.comment" />
    </div>

    <div class="works-section">
      <div class="works-header">
        <h3 class="works-title">Работы</h3>
        <BaseButton variant="secondary" size="sm" type="button" @click="addWork">
          <i class="fa-solid fa-plus"></i> Добавить работу
        </BaseButton>
      </div>

      <div v-for="(w, idx) in form.works" :key="idx" class="work-card">
        <div class="work-card-header">
          <span class="work-card-title">Работа #{{ idx + 1 }}</span>
          <BaseButton
            v-if="form.works.length > 1"
            variant="ghost"
            size="sm"
            type="button"
            @click="removeWork(idx)"
          >
            <i class="fa-solid fa-trash"></i>
          </BaseButton>
        </div>
        <div class="work-grid">
          <BaseSelect
            :model-value="w.component_id === null ? '' : String(w.component_id)"
            label="Компонент"
            :options="componentOptions"
            @update:model-value="(v) => onComponentChange(w, v)"
          />
          <BaseSelect v-model="w.kind" label="Вид работ" :options="kindOptions" />
          <BaseInput v-model="w.title" label="Название (если без компонента)" />
          <BaseInput v-model="w.cost" type="number" label="Стоимость, ₽" />
          <BaseInput v-model="w.note" label="Заметка" class="span-2" />
        </div>
      </div>
    </div>

    <p v-if="errors._form" class="form-error-global">{{ errors._form }}</p>

    <div class="form-actions">
      <BaseButton variant="ghost" size="sm" type="button" @click="emit('cancel')">
        Отмена
      </BaseButton>
      <BaseButton variant="primary" size="sm" type="submit" :loading="saving">
        Сохранить
      </BaseButton>
    </div>
  </form>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.event-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-3);

  @include sm-up {
    grid-template-columns: 1fr 1fr;
  }
}

.span-2 {
  @include sm-up { grid-column: span 2; }
}

.works-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.works-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.works-title {
  font-size: var(--text-base);
  font-weight: var(--fw-semibold);
}

.work-card {
  background: var(--color-surface-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.work-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px dashed var(--color-border);
  padding-bottom: var(--space-2);
  margin-bottom: var(--space-1);
}

.work-card-title {
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  color: var(--color-text-secondary);
}

.work-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-3);

  @include sm-up {
    grid-template-columns: 1fr 1fr;
  }
}

.form-error-global {
  color: var(--color-danger);
  font-size: var(--text-sm);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-2);
  padding-top: var(--space-2);
  border-top: 1px solid var(--color-border);
}
</style>
