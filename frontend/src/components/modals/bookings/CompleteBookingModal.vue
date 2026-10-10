<template>
  <ModalWrapper
    :is-open="isOpen"
    title="Завершить работу"
    subtitle="Отметьте выполненные работы и итоговую стоимость"
    icon="circle-check"
    :icon-color="'var(--success-text)'"
    :bg-icon-color="'var(--success-trans)'"
    @close="close"
  >
    <div class="form-stack">
      <div class="field">
        <label>Итоговая стоимость, ₽</label>
        <input
          v-model.number="price"
          type="number"
          min="0"
          placeholder="3500"
        >
      </div>

      <div class="field">
        <label>Заметка мастера (необязательно)</label>
        <textarea
          v-model="note"
          rows="3"
          placeholder="Что было сделано, на что обратить внимание"
        ></textarea>
      </div>

      <div class="info-hint">
        <i class="fa fa-info-circle"></i>
        Работы и запланированные ТО появятся в следующем обновлении.
      </div>
    </div>

    <template #actions>
      <BaseButton
        variant="success"
        block
        icon="fa fa-circle-check"
        :loading="bookingsStore.mutating"
        @click="submit"
      >
        Завершить
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

const price = ref(null)
const note = ref('')

watch(() => props.isOpen, (open) => {
  if (open) {
    price.value = props.booking?.price_final ?? null
    note.value = props.booking?.master_note ?? ''
  }
})

async function submit() {
  try {
    await bookingsStore.completeBooking(props.booking.id, {
      priceFinal: price.value || null,
      masterNote: note.value.trim() || null,
    })
    toast.success('Работа завершена')
    emit('done', bookingsStore.currentBooking)
  } catch (err) {
    toast.error(err.response?.data?.error || 'Ошибка')
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
.field input,
.field textarea {
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
.field input:focus,
.field textarea:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: var(--shadow-focus);
}
.info-hint {
  display: flex;
  gap: 8px;
  padding: 10px 14px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
}
.info-hint i { color: var(--accent-text); margin-top: 2px; flex-shrink: 0; }
</style>
