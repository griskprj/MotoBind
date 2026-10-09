<template>
  <ModalWrapper
    :is-open="isOpen"
    :title="isEdit ? 'Редактировать услугу' : 'Новая услуга'"
    :subtitle="isEdit ? 'После сохранения услуга уйдёт на повторную модерацию' : 'Услуга появится в каталоге после одобрения модератором'"
    icon="wrench"
    @close="close"
  >
    <div class="form-stack">
      <BaseInput
        v-model="form.title"
        label="Название услуги"
        placeholder="Замена масла"
        required
      />

      <div class="field">
        <label>Категория</label>
        <select v-model="form.category" class="select-input">
          <option value="maintenance">Обслуживание</option>
          <option value="repair">Ремонт</option>
          <option value="diagnostics">Диагностика</option>
          <option value="tuning">Тюнинг</option>
          <option value="other">Другое</option>
        </select>
      </div>

      <div class="field">
        <label>Описание</label>
        <textarea
          v-model="form.description"
          rows="3"
          placeholder="Что входит в услугу, какие работы выполняются..."
        ></textarea>
      </div>

      <div class="form-row">
        <BaseInput
          v-model.number="form.price_from"
          label="Цена от, ₽"
          type="number"
          placeholder="1000"
        />
        <BaseInput
          v-model.number="form.price_to"
          label="Цена до, ₽"
          type="number"
          placeholder="3000"
        />
      </div>

      <BaseInput
        v-model.number="form.duration_min"
        label="Длительность, мин"
        type="number"
        placeholder="60"
      />

      <div v-if="priceInvalid" class="error-hint">
        <i class="fa fa-circle-exclamation"></i>
        Цена «от» не может быть больше цены «до»
      </div>
    </div>

    <template #actions>
      <BaseButton
        variant="primary"
        block
        icon="fa fa-check"
        :loading="servicesStore.mutating"
        :disabled="!canSave"
        @click="handleSave"
      >
        {{ isEdit ? 'Сохранить' : 'Создать' }}
      </BaseButton>
    </template>
  </ModalWrapper>
</template>

<script setup>
import { computed, reactive, watch } from 'vue'
import { useServicesStore } from '@/stores'
import { useToast } from '../../../composables/useToast'
import ModalWrapper from '../../modals/ModalWrapper.vue'
import { BaseButton, BaseInput } from '../../../components/ui'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  service: { type: Object, default: null },
})
const emit = defineEmits(['close', 'saved'])

const servicesStore = useServicesStore()
const toast = useToast()

const form = reactive({
  title: '',
  category: 'maintenance',
  description: '',
  price_from: null,
  price_to: null,
  duration_min: null,
})

const isEdit = computed(() => !!props.service?.id)

const priceInvalid = computed(() => {
  return (
    form.price_from != null &&
    form.price_to != null &&
    form.price_from > form.price_to
  )
})

const canSave = computed(() => {
  return form.title.trim().length >= 2 && !priceInvalid.value
})

watch(() => props.isOpen, (open) => {
  if (open) {
    form.title = props.service?.title || ''
    form.category = props.service?.category || 'maintenance'
    form.description = props.service?.description || ''
    form.price_from = props.service?.price_from ?? null
    form.price_to = props.service?.price_to ?? null
    form.duration_min = props.service?.duration_min ?? null
  }
})

async function handleSave() {
  if (!canSave.value) return
  const payload = {
    title: form.title.trim(),
    category: form.category,
    description: form.description.trim() || null,
    price_from: form.price_from || null,
    price_to: form.price_to || null,
    duration_min: form.duration_min || null,
  }
  try {
    if (isEdit.value) {
      await servicesStore.update(props.service.id, payload)
      toast.success('Услуга обновлена и отправлена на модерацию')
    } else {
      await servicesStore.create(payload)
      toast.success('Услуга создана и отправлена на модерацию')
    }
    emit('saved')
  } catch (err) {
    toast.error(err.response?.data?.error || 'Ошибка сохранения')
  }
}

function close() { emit('close') }
</script>

<style scoped>
.form-stack { display: flex; flex-direction: column; gap: 14px; }
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.field { display: flex; flex-direction: column; gap: 4px; }
.field label {
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  color: var(--text-secondary);
}
.field textarea,
.select-input {
  width: 100%;
  padding: 0.625rem 0.75rem;
  font-size: var(--text-sm);
  font-family: inherit;
  background: var(--bg-input);
  border: 1px solid var(--border-input);
  border-radius: var(--radius);
  color: var(--text-primary);
}
.field textarea { resize: vertical; }
.field textarea:focus,
.select-input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: var(--shadow-focus);
}
.error-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--danger-text);
  padding: 6px 10px;
  background: var(--danger-trans);
  border-radius: var(--radius-sm);
}

@media (max-width: 480px) {
  .form-row { grid-template-columns: 1fr; }
}
</style>
