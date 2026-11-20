<template>
  <ModalWrapper
    :is-open="isOpen"
    title="Перенести запись"
    subtitle="Выберите новую дату и время"
    icon="calendar-edit"
    size="sm"
    @close="close"
  >
    <div class="field">
      <label>Новая дата и время</label>
      <input v-model="dateTime" type="datetime-local" :min="minDate">
    </div>

    <template #actions>
      <BaseButton
        variant="primary"
        block
        icon="fa fa-calendar-check"
        :disabled="!dateTime"
        :loading="bookingsStore.mutating"
        @click="submit"
      >
        Перенести
      </BaseButton>
    </template>
  </ModalWrapper>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
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
const dateTime = ref('')

const minDate = computed(() => {
  const d = new Date()
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
  return d.toISOString().slice(0, 16)
})

watch(() => props.isOpen, (open) => {
  if (open && props.booking?.scheduled_at) {
    const d = new Date(props.booking.scheduled_at)
    d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
    dateTime.value = d.toISOString().slice(0, 16)
  }
})

async function submit() {
  if (!dateTime.value) return
  try {
    const iso = new Date(dateTime.value).toISOString()
    await bookingsStore.rescheduleBooking(props.booking.id, iso)
    toast.success('Запись перенесена')
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
.field input {
  width: 100%;
  padding: 0.625rem 0.75rem;
  font-size: var(--text-sm);
  font-family: inherit;
  background: var(--bg-input);
  border: 1px solid var(--border-input);
  border-radius: var(--radius);
  color: var(--text-primary);
}
.field input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: var(--shadow-focus);
}
</style>
