<template>
  <ModalWrapper
    :is-open="isOpen"
    title="Записаться"
    :subtitle="business ? `К мастеру: ${business.name}` : ''"
    icon="calendar-plus"
    @close="close"
  >
    <div class="form-stack">
      <!-- Услуга -->
      <div v-if="services.length" class="field">
        <label>Услуга</label>
        <select v-model="form.serviceId" class="select-input">
          <option :value="null">Без выбора — опишу в комментарии</option>
          <option v-for="s in services" :key="s.id" :value="s.id">
            {{ s.title }}{{ priceLabel(s) }}
          </option>
        </select>
      </div>
      <p v-else class="hint">
        <i class="fa fa-info-circle"></i>
        У мастера пока нет одобренных услуг — можете записаться и описать задачу в комментарии.
      </p>

      <!-- Мотоцикл -->
      <div v-if="motorcycles.length" class="field">
        <label>Мотоцикл</label>
        <select v-model="form.motorcycleId" class="select-input">
          <option :value="null">Не указывать</option>
          <option v-for="m in motorcycles" :key="m.id" :value="m.id">
            {{ m.name }} ({{ m.years || '—' }})
          </option>
        </select>
      </div>
      <p v-else class="hint">
        <i class="fa fa-motorcycle"></i>
        У вас пока нет мотоциклов в гараже. Можно записаться без указания.
      </p>

      <!-- Дата и время -->
      <div class="field">
        <label>Дата и время</label>
        <input
          v-model="form.scheduledAt"
          type="datetime-local"
          class="select-input"
          :min="minDate"
        >
      </div>

      <!-- Комментарий -->
      <div class="field">
        <label>Комментарий (необязательно)</label>
        <textarea
          v-model="form.note"
          rows="3"
          placeholder="Опишите, что беспокоит, что хотите сделать"
        ></textarea>
      </div>

      <div v-if="error" class="error-hint">
        <i class="fa fa-circle-exclamation"></i> {{ error }}
      </div>
    </div>

    <template #actions>
      <BaseButton
        variant="primary"
        block
        icon="fa fa-paper-plane"
        :loading="bookingsStore.mutating"
        :disabled="!canSubmit"
        @click="handleSubmit"
      >
        Записаться
      </BaseButton>
    </template>
  </ModalWrapper>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { useBookingsStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import ModalWrapper from '@/components/modals/ModalWrapper.vue'
import { BaseButton } from '@/components/ui'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  business: { type: Object, default: null },
  services: { type: Array, default: () => [] },
  motorcycles: { type: Array, default: () => [] },
})
const emit = defineEmits(['close', 'created'])

const bookingsStore = useBookingsStore()
const toast = useToast()

const form = reactive({
  serviceId: null,
  motorcycleId: null,
  scheduledAt: '',
  note: '',
})
const error = ref('')

const minDate = computed(() => {
  const d = new Date()
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
  return d.toISOString().slice(0, 16)
})

const canSubmit = computed(() => !!form.scheduledAt)

watch(() => props.isOpen, (open) => {
  if (open) {
    form.serviceId = null
    form.motorcycleId = null
    form.scheduledAt = ''
    form.note = ''
    error.value = ''
  }
})

function priceLabel(s) {
  if (!s.price_from && !s.price_to) return ''
  if (s.price_from && s.price_to) return ` — ${s.price_from}–${s.price_to} ₽`
  if (s.price_from) return ` — от ${s.price_from} ₽`
  return ` — до ${s.price_to} ₽`
}

async function handleSubmit() {
  if (!canSubmit.value || !props.business) return
  error.value = ''

  // datetime-local → ISO
  const scheduledAtIso = new Date(form.scheduledAt).toISOString()

  try {
    await bookingsStore.createBooking({
      business_account_id: props.business.id,
      service_id: form.serviceId,
      motorcycle_id: form.motorcycleId,
      scheduled_at: scheduledAtIso,
      client_note: form.note.trim() || null,
    })
    toast.success('Заявка отправлена!')
    emit('created')
  } catch (err) {
    error.value = err.response?.data?.error || 'Не удалось создать заявку'
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
.select-input,
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
.select-input:focus,
.field textarea:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: var(--shadow-focus);
}

.hint {
  display: flex;
  gap: 8px;
  padding: 10px 14px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
}
.hint i { color: var(--accent-text); margin-top: 2px; flex-shrink: 0; }

.error-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--danger-text);
  padding: 8px 12px;
  background: var(--danger-trans);
  border-radius: var(--radius-sm);
}
</style>
