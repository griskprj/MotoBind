<template>
  <ModalWrapper
    :is-open="isOpen"
    title="Связать с аккаунтом MotoBind"
    subtitle="Клиент увидит вашу запись в своём гараже"
    icon="link"
    @close="close"
  >
    <p class="hint">
      <i class="fa fa-info-circle"></i>
      Укажите email, под которым клиент зарегистрирован в MotoBind.
      Мы найдём его аккаунт и свяжем с этой записью.
    </p>

    <BaseInput
      v-model="email"
      label="Email клиента"
      type="email"
      placeholder="client@example.com"
      required
    />

    <template #actions>
      <BaseButton
        variant="primary"
        block
        icon="fa fa-link"
        :loading="business.mutating"
        :disabled="!isValid"
        @click="handleSave"
      >
        Связать
      </BaseButton>
    </template>
  </ModalWrapper>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useBusinessStore } from '@/stores'
import { useToast } from '../../../composables/useToast'
import ModalWrapper from '../../modals/ModalWrapper.vue'
import { BaseButton, BaseInput } from '../../ui'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  clientId: { type: Number, required: true },
  clientEmail: { type: String, default: '' },
})
const emit = defineEmits(['close', 'linked'])

const business = useBusinessStore()
const toast = useToast()
const email = ref('')

const isValid = computed(() => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email.value))

watch(() => props.isOpen, (open) => {
  if (open) email.value = props.clientEmail || ''
})

async function handleSave() {
  if (!isValid.value) return
  try {
    await business.linkClient(props.clientId, email.value.trim())
    toast.success('Клиент связан с аккаунтом')
    emit('linked')
  } catch (err) {
    toast.error(err.response?.data?.error || 'Не удалось связать')
  }
}

function close() { emit('close') }
</script>

<style scoped>
.hint {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 10px 14px;
  background: var(--accent-trans);
  color: var(--text-secondary);
  border-radius: var(--radius-md);
  font-size: 13px;
  line-height: 1.5;
  margin: 0 0 16px;
}
.hint i { color: var(--accent-text); margin-top: 2px; flex-shrink: 0; }
</style>
