<template>
  <ModalWrapper
    :is-open="isOpen"
    title="Редактировать аккаунт"
    subtitle="Обновите информацию о бизнесе"
    icon="briefcase"
    @close="close"
  >
    <div class="form-stack">
      <BaseInput v-model="form.name" label="Название" required />
      <BaseInput v-model="form.city" label="Город" />
      <BaseInput v-model="form.phone" label="Телефон" />
      <BaseInput v-model="form.email" label="Email" type="email" />
      <BaseInput v-model="form.address" label="Адрес" />
      <BaseInput v-model="form.website" label="Сайт" />
      <div class="field">
        <label>Описание</label>
        <textarea v-model="form.description" rows="3"></textarea>
      </div>
    </div>

    <template #actions>
      <BaseButton
        variant="primary"
        block
        icon="fa fa-check"
        :loading="business.mutating"
        :disabled="!canSave"
        @click="handleSave"
      >
        Сохранить
      </BaseButton>
    </template>
  </ModalWrapper>
</template>

<script setup>
import { computed, reactive, watch } from 'vue'
import { useBusinessStore } from '@/stores'
import { useToast } from '../../../composables/useToast'
import ModalWrapper from '../../modals/ModalWrapper.vue'
import { BaseButton, BaseInput } from '../../ui/index.js'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  account: { type: Object, default: null },
})
const emit = defineEmits(['close', 'saved'])

const business = useBusinessStore()
const toast = useToast()

const form = reactive({
  name: '',
  city: '',
  phone: '',
  email: '',
  address: '',
  website: '',
  description: '',
})

const canSave = computed(() => form.name.trim().length >= 2)

watch(() => props.isOpen, (open) => {
  if (open && props.account) {
    form.name = props.account.name || ''
    form.city = props.account.city || ''
    form.phone = props.account.phone || ''
    form.email = props.account.email || ''
    form.address = props.account.address || ''
    form.website = props.account.website || ''
    form.description = props.account.description || ''
  }
})

async function handleSave() {
  if (!canSave.value) return
  const payload = {
    name: form.name.trim(),
    city: form.city.trim() || null,
    phone: form.phone.trim() || null,
    email: form.email.trim() || null,
    address: form.address.trim() || null,
    website: form.website.trim() || null,
    description: form.description.trim() || null,
  }
  try {
    await business.updateAccount(payload)
    toast.success('Сохранено')
    emit('saved')
  } catch (err) {
    toast.error(err.response?.data?.error || 'Ошибка сохранения')
  }
}

function close() { emit('close') }
</script>

<style scoped>
.form-stack { display: flex; flex-direction: column; gap: 14px; }
.field { display: flex; flex-direction: column; gap: 4px; }
.field label {
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  color: var(--text-secondary);
}
.field textarea {
  width: 100%;
  padding: 0.625rem 0.75rem;
  font-size: var(--text-sm);
  font-family: inherit;
  background: var(--bg-input);
  border: 1px solid var(--border-input);
  border-radius: var(--radius);
  color: var(--text-primary);
  resize: vertical;
}
.field textarea:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: var(--shadow-focus);
}
</style>
