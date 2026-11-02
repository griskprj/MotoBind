<script setup lang="ts">
import type { CreateMaintenancePayload, UpdateMaintenancePayload, ApiError, Maintenance, Motorcycle } from '~/types'
import { MAINTENANCE_CATEGORIES, getTemplatesByCategory } from '~/utils/constants/maintenance'

const props = defineProps<{
  motorcycles: Motorcycle[]
  defaultMotorcycleId?: number | string
  initialData?: Maintenance | null
}>()

const emit = defineEmits<{
  created: []
  updated: []
  cancel: []
}>()

const api = useApi()
const toast = useToast()
const { errors, setFromApiError, clear } = useFormErrors()

const isEditing = computed(() => !!props.initialData)
const submitting = ref(false)
const formType = ref<'planned' | 'completed'>('planned')

const form = reactive({
  motorcycleId: props.defaultMotorcycleId || props.motorcycles[0]?.id || '',
  category: 'engine',
  title: '',
  description: '',
  planned_date: '',
  planned_mileage: '' as string | number,
  completed_date: '',
  completed_mileage: '' as string | number,
  cost: '' as string | number,
})

const availableTemplates = computed(() => getTemplatesByCategory(form.category))

function initForm() {
  clear()
  if (props.initialData) {
    const d = props.initialData
    form.motorcycleId = d.motorcycle_id
    form.category = d.category || 'engine'
    form.title = d.title || ''
    form.description = d.description || ''
    form.planned_date = d.planned_date || ''
    form.planned_mileage = d.planned_mileage || ''
    form.completed_date = d.completed_date || ''
    form.completed_mileage = d.completed_mileage || ''
    form.cost = d.cost || ''
    formType.value = d.status // 'planned' | 'completed'
  } else {
    form.motorcycleId = props.defaultMotorcycleId || props.motorcycles[0]?.id || ''
    form.category = 'engine'
    form.title = ''
    form.description = ''
    form.planned_date = ''
    form.planned_mileage = ''
    form.completed_date = ''
    form.completed_mileage = ''
    form.cost = ''
    formType.value = 'planned'
  }
}

watch(() => props.initialData, () => {
  initForm()
}, { immediate: true })

async function onSubmit() {
  submitting.value = true
  clear()

  try {
    if (isEditing.value && props.initialData) {
      // РЕЖИМ РЕДАКТИРОВАНИЯ (PUT)
      const payload: UpdateMaintenancePayload = {
        category: form.category,
        title: form.title.trim(),
        description: form.description.trim() || null,
      }

      if (formType.value === 'planned') {
        payload.planned_date = form.planned_date || null
        payload.planned_mileage = form.planned_mileage ? Number(form.planned_mileage) : null
        payload.completed_date = null
        payload.completed_mileage = null
        payload.cost = null
      } else {
        if (!form.completed_mileage) {
          toast.error('Для выполненной работы нужно указать пробег')
          submitting.value = false
          return
        }
        payload.completed_date = form.completed_date || null
        payload.completed_mileage = Number(form.completed_mileage)
        payload.cost = form.cost ? Number(form.cost) : null
        // Очищаем planned-поля
        payload.planned_date = null
        payload.planned_mileage = null
      }

      await api.maintenance.update(props.initialData.id, payload)
      toast.success('Запись обновлена')
      emit('updated')
    } else {
      // РЕЖИМ СОЗДАНИЯ (POST)
      const payload: CreateMaintenancePayload = {
        motorcycleId: form.motorcycleId,
        category: form.category,
        title: form.title.trim(),
        description: form.description.trim() || null,
      }

      if (formType.value === 'planned') {
        payload.planned_date = form.planned_date || null
        payload.planned_mileage = form.planned_mileage ? Number(form.planned_mileage) : null
      } else {
        if (!form.completed_mileage) {
          toast.error('Для выполненной работы нужно указать пробег')
          submitting.value = false
          return
        }
        payload.completed_date = form.completed_date || null
        payload.completed_mileage = Number(form.completed_mileage)
        payload.cost = form.cost ? Number(form.cost) : null
      }

      await api.maintenance.create(payload)
      toast.success('Запись создана')
      emit('created')
    }
  } catch (e) {
    const err = e as ApiError
    setFromApiError(err)
    if (!err.fieldErrors) toast.error(err.message)
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <BaseCard padding="lg" class="m-form">
    <h3 class="m-form__title">{{ isEditing ? 'Редактировать запись' : 'Добавить запись' }}</h3>

    <form @submit.prevent="onSubmit" class="m-form__inner">
      <!-- Выбор мотоцикла (только при создании и если их несколько) -->
      <div v-if="!isEditing && motorcycles.length > 1" class="field-wrapper span-2">
        <label class="field-label">Мотоцикл</label>
        <select v-model="form.motorcycleId" class="custom-input">
          <option v-for="m in motorcycles" :key="m.id" :value="m.id">
            {{ m.name }}
          </option>
        </select>
      </div>

      <!-- Табы (План / Выполнено) -->
      <div class="m-form__tabs">
        <button type="button" class="m-tab" :class="{ 'm-tab--active': formType === 'planned' }" @click="formType = 'planned'">В планы</button>
        <button type="button" class="m-tab" :class="{ 'm-tab--active': formType === 'completed' }" @click="formType = 'completed'">Выполнено</button>
      </div>

      <div class="form-grid">
        <BaseSelect v-model="form.category" label="Категория" :options="MAINTENANCE_CATEGORIES" class="span-2" :error="errors.category" />

        <div class="field-wrapper span-2">
          <label class="field-label">Название работы</label>
          <input v-model="form.title" list="maintenance-templates" class="custom-input" :class="{ 'custom-input--error': !!errors.title }" placeholder="Начните вводить или выберите из списка..." required />
          <datalist id="maintenance-templates">
            <option v-for="tpl in availableTemplates" :key="tpl.id" :value="tpl.label" />
          </datalist>
          <p v-if="errors.title" class="field-error">{{ errors.title }}</p>
        </div>

        <BaseInput v-model="form.description" label="Описание (необязательно)" placeholder="Детали, артикулы, где покупал" class="span-2" :error="errors.description" />

        <template v-if="formType === 'planned'">
          <BaseInput v-model="form.planned_date" type="date" label="Дата (план)" :error="errors.planned_date" />
          <BaseInput v-model="form.planned_mileage" type="number" label="Пробег (план)" placeholder="км" :error="errors.planned_mileage" />
        </template>

        <template v-else>
          <BaseInput v-model="form.completed_date" type="date" label="Дата выполнения" hint="Если пусто — поставим сегодня" :error="errors.completed_date" />
          <BaseInput v-model="form.completed_mileage" type="number" label="Пробег" placeholder="км" :error="errors.completed_mileage" required />
          <BaseInput v-model="form.cost" type="number" label="Стоимость" placeholder="₽" class="span-2" :error="errors.cost" />
        </template>
      </div>

      <div class="m-form__actions">
        <BaseButton type="button" variant="ghost" @click="emit('cancel')">Отмена</BaseButton>
        <BaseButton type="submit" variant="primary" :loading="submitting">
          {{ isEditing ? 'Сохранить изменения' : 'Создать' }}
        </BaseButton>
      </div>
    </form>
  </BaseCard>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.m-form {
  background: var(--color-surface);
  border: 1px solid var(--color-brand-soft);
  box-shadow: var(--shadow-sm);
}
.m-form__title {
  font-size: var(--text-lg);
  font-weight: var(--fw-semibold);
  margin-bottom: var(--space-5);
}
.m-form__inner {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}
.m-form__tabs {
  display: flex;
  background: var(--color-surface-secondary);
  padding: 4px;
  border-radius: var(--radius-md);
  width: 100%;
  @include sm-up { width: fit-content; }
}
.m-tab {
  flex: 1;
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-sm);
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  color: var(--color-text-secondary);
  transition: all var(--transition-fast);
  text-align: center;
  cursor: pointer;
  border: none;
  background: transparent;
  &:hover { color: var(--color-text); }
  &--active {
    background: var(--color-surface);
    color: var(--color-brand);
    box-shadow: var(--shadow-sm);
  }
}
.form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);
  @include sm-up { grid-template-columns: 1fr 1fr; }
}
.span-2 {
  @include sm-up { grid-column: span 2; }
}
.field-wrapper {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  width: 100%;
}
.field-label {
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  color: var(--color-text);
}
.custom-input {
  width: 100%;
  min-height: 40px;
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text);
  font-size: var(--text-base);
  font-family: inherit;
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
  &::placeholder { color: var(--color-text-tertiary); }
  &:hover { border-color: var(--color-border-dark); }
  &:focus {
    outline: none;
    border-color: var(--color-brand);
    box-shadow: var(--shadow-focus);
  }
  @include md-up { min-height: 44px; }
}
.custom-input--error {
  border-color: var(--color-danger);
  &:focus { box-shadow: 0 0 0 3px var(--color-danger-soft); }
}
.field-error {
  font-size: var(--text-sm);
  color: var(--color-danger);
}
.m-form__actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-3);
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border-light);
}
</style>
