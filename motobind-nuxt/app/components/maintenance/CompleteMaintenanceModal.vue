<script setup lang="ts">
import type { Maintenance, ApiError } from '~/types'

const props = defineProps<{
  maintenance: Maintenance
}>()

const emit = defineEmits<{
  close: []
  completed: []
}>()

const api = useApi()
const toast = useToast()
const { errors, setFromApiError, clear } = useFormErrors()

const submitting = ref(false)

const form = reactive({
  completed_mileage: '' as string | number,
  completed_date: '',
  cost: '' as string | number,
  is_repeat: false,
  interval_type: 'km' as 'km' | 'days',
  interval_value: '' as string | number,
})

async function onSubmit() {
  if (!form.completed_mileage) {
    toast.error('Пробег обязателен для завершения')
    return
  }

  if (form.is_repeat && !form.interval_value) {
    toast.error('Укажите интервал для следующего обслуживания')
    return
  }

  submitting.value = true
  clear()

  try {
    const payload: any = {
      completed_mileage: Number(form.completed_mileage),
      completed_date: form.completed_date || null,
      cost: form.cost ? Number(form.cost) : null,
      is_repeat: form.is_repeat,
    }

    if (form.is_repeat) {
      if (form.interval_type === 'km') {
        payload.interval = Number(form.interval_value)
      } else {
        payload.interval_days = Number(form.interval_value)
      }
    }

    await api.maintenance.complete(props.maintenance.id, payload)
    toast.success('Работа отмечена как выполненная')
    emit('completed')
    emit('close')
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
  <BaseModal title="Завершить работу" size="sm" @close="emit('close')">
    <form @submit.prevent="onSubmit" class="complete-form">
      <p class="info-text">
        Вы завершаете: <strong>{{ maintenance.title }}</strong>
      </p>

      <BaseInput
        v-model="form.completed_mileage"
        type="number"
        label="Текущий пробег (км)"
        placeholder="Например: 15400"
        required
        :error="errors.completed_mileage"
      />

      <div class="form-row">
        <BaseInput
          v-model="form.completed_date"
          type="date"
          label="Дата выполнения"
          hint="Если пусто — будет сегодняшняя"
          :error="errors.completed_date"
        />
        <BaseInput
          v-model="form.cost"
          type="number"
          label="Стоимость (₽)"
          placeholder="0"
          :error="errors.cost"
        />
      </div>

      <!-- Блок повтора -->
      <div class="repeat-block">
        <BaseCheckbox
          v-model="form.is_repeat"
          label="Запланировать следующее обслуживание"
        />

        <div v-if="form.is_repeat" class="repeat-details">
          <div class="repeat-tabs">
            <button
              type="button"
              class="repeat-tab"
              :class="{ 'repeat-tab--active': form.interval_type === 'km' }"
              @click="form.interval_type = 'km'"
            >
              По пробегу
            </button>
            <button
              type="button"
              class="repeat-tab"
              :class="{ 'repeat-tab--active': form.interval_type === 'days' }"
              @click="form.interval_type = 'days'"
            >
              По дням
            </button>
          </div>

          <BaseInput
            v-model="form.interval_value"
            type="number"
            :label="form.interval_type === 'km' ? 'Через сколько км?' : 'Через сколько дней?'"
            :placeholder="form.interval_type === 'km' ? 'Например: 5000' : 'Например: 180'"
            required
          />
        </div>
      </div>
    </form>

    <template #footer>
      <BaseButton variant="ghost" size="sm" @click="emit('close')">
        Отмена
      </BaseButton>
      <BaseButton variant="primary" size="sm" :loading="submitting" @click="onSubmit">
        <template #icon><i class="fa-solid fa-check"></i></template>
        Завершить
      </BaseButton>
    </template>
  </BaseModal>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.complete-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.info-text {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-2);
  strong { color: var(--color-text); }
}

.form-row {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);

  @include sm-up {
    grid-template-columns: 1fr 1fr;
  }
}

.repeat-block {
  background: var(--color-surface-secondary);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.repeat-details {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  padding-top: var(--space-3);
  border-top: 1px solid var(--color-border-light);
}

.repeat-tabs {
  display: flex;
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: 4px;
  width: fit-content;
}

.repeat-tab {
  padding: var(--space-1) var(--space-3);
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  color: var(--color-text-secondary);
  border-radius: var(--radius-sm);
  transition: all var(--transition-fast);

  &--active {
    background: var(--color-brand);
    color: #fff;
  }
}
</style>
