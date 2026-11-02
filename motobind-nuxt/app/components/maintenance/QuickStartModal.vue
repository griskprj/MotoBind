<script setup lang="ts">
import type { Motorcycle, ApiError } from '~/types'

const props = defineProps<{
  motorcycle: Motorcycle
}>()

const emit = defineEmits<{
  close: []
  created: []
}>()

const api = useApi()
const toast = useToast()
const { errors, setFromApiError, clear } = useFormErrors()

const submitting = ref(false)

// Подставляем текущий пробег мотоцикла, если он есть
const form = reactive({
  current_mileage: (props.motorcycle.mileage || '') as string | number,
  drive_type: 'chain' as 'chain' | 'belt' | 'shaft',
  style: 'normal' as 'calm' | 'normal' | 'aggressive',
  terrain: 'mixed' as 'city' | 'highway' | 'mixed' | 'dusty' | 'offroad',
})

const driveOptions = [
  { value: 'chain', label: 'Цепь' },
  { value: 'belt', label: 'Ремень' },
  { value: 'shaft', label: 'Кардан' },
]

const styleOptions = [
  { value: 'calm', label: 'Спокойный' },
  { value: 'normal', label: 'Обычный' },
  { value: 'aggressive', label: 'Агрессивный' },
]

const terrainOptions = [
  { value: 'city', label: 'Город' },
  { value: 'highway', label: 'Трасса' },
  { value: 'mixed', label: 'Смешанный' },
  { value: 'dusty', label: 'Пыльный' },
  { value: 'offroad', label: 'Бездорожье' },
]

async function onSubmit() {
  if (!form.current_mileage) {
    toast.error('Укажите текущий пробег')
    return
  }

  submitting.value = true
  clear()

  try {
    await api.maintenance.quickStart({
      moto_id: props.motorcycle.id,
      current_mileage: Number(form.current_mileage),
      drive_type: form.drive_type,
      style: form.style,
      terrain: form.terrain,
    })
    toast.success(`Базовый план для ${props.motorcycle.name} создан!`)
    emit('created')
    emit('close')
  } catch (e) {
    const err = e as ApiError
    setFromApiError(err)
    if (!err.fieldErrors) toast.error(err.message)
  } finally {
    submitting.value = false
  }
}

console.log('Moto data:', props.motorcycle)

watch(
  () => props.motorcycle,
  (moto) => {
    if (moto) {
      form.current_mileage = moto.mileage || ''
    }
  },
  { immediate: true }
)
</script>

<template>
  <BaseModal :title="`Быстрый старт: ${motorcycle.name}`" size="md" @close="emit('close')">
    <form @submit.prevent="onSubmit" class="quick-start-form">
      <p class="info-text">
        Мы создадим базовый план обслуживания для <strong>{{ motorcycle.name }}</strong> на основе ваших условий эксплуатации.
      </p>

      <BaseInput
        v-model="form.current_mileage"
        type="number"
        label="Текущий пробег (км)"
        placeholder="Например: 15000"
        required
        :error="errors.current_mileage"

      />

      <div class="form-grid">
        <BaseSelect v-model="form.drive_type" label="Тип привода" :options="driveOptions" :error="errors.drive_type" />
        <BaseSelect v-model="form.style" label="Стиль езды" :options="styleOptions" :error="errors.style" />
        <BaseSelect v-model="form.terrain" label="Местность" :options="terrainOptions" class="span-2" :error="errors.terrain" />
      </div>
    </form>

    <template #footer>
      <BaseButton variant="ghost" size="sm" @click="emit('close')">Отмена</BaseButton>
      <BaseButton variant="primary" size="sm" :loading="submitting" @click="onSubmit">
        <template #icon><i class="fa-solid fa-wand-magic-sparkles"></i></template>
        Сгенерировать
      </BaseButton>
    </template>
  </BaseModal>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.quick-start-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.info-text {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  line-height: var(--leading-relaxed);
  strong { color: var(--color-text); }
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
</style>
