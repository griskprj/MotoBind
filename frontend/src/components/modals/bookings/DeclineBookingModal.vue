<template>
  <ModalWrapper
    :is-open="isOpen"
    title="Отклонить заявку"
    subtitle="Клиент увидит причину и сможет выбрать другое время"
    icon="circle-xmark"
    :icon-color="'var(--danger-text)'"
    :bg-icon-color="'var(--danger-trans)'"
    size="sm"
    @close="close"
  >
    <div class="field">
      <label>Причина (необязательно)</label>
      <textarea
        v-model="reason"
        rows="3"
        placeholder="Не могу в это время, попробуйте позже"
      ></textarea>
    </div>

    <template #actions>
      <BaseButton
        variant="danger"
        block
        icon="fa fa-times"
        :loading="bookingsStore.mutating"
        @click="submit"
      >
        Отклонить
      </BaseButton>
    </template>
  </ModalWrapper>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useBookingsStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import ModalWrapper from '@/components/modals/ModalWrapper.vue'
import { BaseButton } from '@/components/ui'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  booking: { type: Object, required: true },
})
const emit = defineEmits(['close', 'done'])

const bookingsStore = useBookingsStore()
const toast = useToast()
const reason = ref('')

watch(() => props.isOpen, (open) => { if (open) reason.value = '' })

async function submit() {
  try {
    await bookingsStore.declineBooking(props.booking.id, reason.value.trim() || null)
    toast.success('Заявка отклонена')
    emit('done', bookingsStore.currentBooking)
  } catch (err) {
    toast.error(err.response?.data?.error || 'Ошибка')
  }
}

function close() { emit('close') }
</script>

<style scoped>
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
  border-color: var(--danger);
}
</style>
