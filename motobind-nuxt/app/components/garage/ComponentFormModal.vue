<script setup lang="ts">
import type {
  ApiError,
  MotorcycleComponent,
  ComponentCategory,
  ConditionRating,
  CreateComponentPayload,
} from '~/types'

const props = defineProps<{
  motorcycleId: number | string
  component: MotorcycleComponent | null
}>()

const emit = defineEmits<{
  saved: []
  cancel: []
}>()

const api = useApi()
const toast = useToast()
const { errors, setFromApiError, clear } = useFormErrors()

const saving = ref(false)
const isEdit = computed(() => !!props.component)

const form = reactive({
  name: '',
  category: 'other' as ComponentCategory,
  manufacturer: '',
  part_number: '',
  interval_km: '' as string | number,
  interval_days: '' as string | number,
  last_service_date: '',
  last_service_mileage: '' as string | number,
  condition_rating: '' as ConditionRating | '',
  condition_note: '',
})

onMounted(() => {
  if (props.component) {
    const c = props.component
    form.name = c.name
    form.category = c.category
    form.manufacturer = c.manufacturer || ''
    form.part_number = c.part_number || ''
    form.interval_km = c.interval_km ?? ''
    form.interval_days = c.interval_days ?? ''
    form.last_service_date = c.last_service_date || ''
    form.last_service_mileage = c.last_service_mileage ?? ''
    form.condition_rating = (c.condition_rating as ConditionRating) || ''
    form.condition_note = c.condition_note || ''
  }
})

const categoryOptions = [
  { value: 'fluid', label: 'Жидкость' },
  { value: 'filter', label: 'Фильтр' },
  { value: 'ignition', label: 'Зажигание' },
  { value: 'brake', label: 'Тормоза' },
  { value: 'drive', label: 'Привод' },
  { value: 'other', label: 'Прочее' },
]

const conditionOptions = [
  { value: '', label: 'Без оценки' },
  { value: 'good', label: 'Хорошее' },
  { value: 'ok', label: 'Удовлетворительное' },
  { value: 'bad', label: 'Требует внимания' },
  { value: 'unknown', label: 'Не знаю' },
]

async function onSave() {
  clear()
  saving.value = true
  try {
    const payload: CreateComponentPayload = {
      name: form.name.trim(),
      category: form.category,
      manufacturer: form.manufacturer.trim() || null,
      part_number: form.part_number.trim() || null,
      interval_km: form.interval_km === '' ? null : Number(form.interval_km),
      interval_days: form.interval_days === '' ? null : Number(form.interval_days),
      last_service_date: form.last_service_date || null,
      last_service_mileage:
        form.last_service_mileage === '' ? null : Number(form.last_service_mileage),
      condition_rating: (form.condition_rating || null) as ConditionRating | null,
      condition_note: form.condition_note.trim() || null,
    }

    if (isEdit.value && props.component) {
      await api.components.update(props.motorcycleId, props.component.id, payload)
      toast.success('Компонент обновлён')
    } else {
      await api.components.create(props.motorcycleId, payload)
      toast.success('Компонент создан')
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
  <form class="comp-form" @submit.prevent="onSave">
    <div class="form-grid">
      <BaseInput
        v-model="form.name"
        label="Название"
        required
        class="span-2"
        :error="errors.name"
      />

      <BaseSelect
        v-model="form.category"
        label="Категория"
        :options="categoryOptions"
        :error="errors.category"
      />

      <BaseSelect
        v-model="form.condition_rating"
        label="Оценка состояния"
        :options="conditionOptions"
        hint="Субъективная оценка владельца, не автодиагностика"
        :error="errors.condition_rating"
      />

      <BaseInput
        v-model="form.manufacturer"
        label="Производитель"
        placeholder="Например: Motul"
        :error="errors.manufacturer"
      />

      <BaseInput
        v-model="form.part_number"
        label="Артикул"
        :error="errors.part_number"
      />

      <BaseInput
        v-model="form.interval_km"
        type="number"
        label="Интервал по пробегу, км"
        hint="0 или пусто — не задан"
        :error="errors.interval_km"
      />

      <BaseInput
        v-model="form.interval_days"
        type="number"
        label="Интервал по времени, дней"
        hint="0 или пусто — не задан"
        :error="errors.interval_days"
      />

      <BaseInput
        v-model="form.last_service_date"
        type="date"
        label="Дата последней замены"
        :error="errors.last_service_date"
      />

      <BaseInput
        v-model="form.last_service_mileage"
        type="number"
        label="Пробег последней замены, км"
        :error="errors.last_service_mileage"
      />

      <BaseInput
        v-model="form.condition_note"
        label="Заметка о состоянии"
        class="span-2"
        :error="errors.condition_note"
      />
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

.comp-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
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
  @include sm-up {
    grid-column: span 2;
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
