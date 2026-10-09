<template>
  <ModalWrapper
    :is-open="isOpen"
    :title="isEdit ? 'Редактировать клиента' : 'Новый клиент'"
    :subtitle="isEdit ? 'Обновите информацию' : 'Добавьте клиента в базу'"
    icon="user"
    @close="close"
  >
    <div class="form-stack">
      <BaseInput
        v-model="form.name"
        label="Имя"
        placeholder="Иван Петров"
        required
      />
      <BaseInput
        v-model="form.phone"
        label="Телефон"
        placeholder="+7 (___) ___-__-__"
      />
      <BaseInput
        v-model="form.email"
        label="Email"
        type="email"
        placeholder="mail@example.com"
      />
      <div class="field">
        <label>Заметка</label>
        <textarea
          v-model="form.note"
          rows="3"
          placeholder="Особенности клиента, договорённости..."
        ></textarea>
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
        {{ isEdit ? 'Сохранить' : 'Добавить' }}
      </BaseButton>
    </template>
  </ModalWrapper>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { useBusinessStore } from '@/stores'
import { useToast } from '../../../composables/useToast'
import ModalWrapper from '../ModalWrapper.vue'
import { BaseButton, BaseInput } from '../../../components/ui'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  client: { type: Object, default: null },
})
const emit = defineEmits(['close', 'saved'])

const business = useBusinessStore()
const toast = useToast()

const form = reactive({
  name: '',
  phone: '',
  email: '',
  note: '',
})

const isEdit = computed(() => !!props.client?.id)
const canSave = computed(() => form.name.trim().length >= 2)

watch(() => props.isOpen, (open) => {
  if (open) {
    form.name = props.client?.name || ''
    form.phone = props.client?.phone || ''
    form.email = props.client?.email || ''
    form.note = props.client?.note || ''
  }
})

async function handleSave() {
  if (!canSave.value) return
  const payload = {
    name: form.name.trim(),
    phone: form.phone.trim() || null,
    email: form.email.trim() || null,
    note: form.note.trim() || null,
  }
  try {
    if (isEdit.value) {
      await business.updateClient(props.client.id, payload)
      toast.success('Клиент обновлён')
    } else {
      await business.createClient(payload)
      toast.success('Клиент добавлен')
    }
    emit('saved')
  } catch (err) {
    toast.error(err.response?.data?.error || 'Ошибка сохранения')
  }
}

function close() {
  emit('close')
}
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
