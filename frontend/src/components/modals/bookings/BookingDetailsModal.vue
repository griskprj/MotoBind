<template>
  <ModalWrapper
    v-if="booking"
    :is-open="isOpen"
    :title="title"
    :subtitle="subtitle"
    :icon="statusIcon"
    :icon-color="iconColor"
    :bg-icon-color="iconBgColor"
    @close="close"
  >
    <!-- Инфо -->
    <div class="details-info">
      <div class="info-row">
        <span class="label">Дата и время</span>
        <span class="value">
          <i class="fa fa-calendar"></i> {{ formatBookingDate(booking.scheduled_at) }}
        </span>
      </div>

      <div v-if="booking.service" class="info-row">
        <span class="label">Услуга</span>
        <span class="value">{{ booking.service.title }}</span>
      </div>

      <div v-if="booking.motorcycle" class="info-row">
        <span class="label">Мотоцикл</span>
        <span class="value">{{ booking.motorcycle.name }}</span>
      </div>

      <div v-if="view === 'master' && booking.client" class="info-row">
        <span class="label">Клиент</span>
        <span class="value">{{ booking.client.username }}</span>
      </div>

      <div v-if="view === 'client' && booking.business" class="info-row">
        <span class="label">Мастер</span>
        <span class="value">{{ booking.business.name }}</span>
      </div>

      <div v-if="booking.business?.phone" class="info-row">
        <span class="label">Телефон</span>
        <span class="value">
          <a :href="`tel:${booking.business.phone}`">{{ booking.business.phone }}</a>
        </span>
      </div>
    </div>

    <!-- Комментарий клиента -->
    <div v-if="booking.client_note" class="note-block">
      <div class="note-title"><i class="fa fa-comment-dots"></i> Комментарий клиента</div>
      <p>{{ booking.client_note }}</p>
    </div>

    <!-- Заметка мастера -->
    <div v-if="booking.master_note" class="note-block master">
      <div class="note-title"><i class="fa fa-clipboard"></i> Заметка мастера</div>
      <p>{{ booking.master_note }}</p>
    </div>

    <!-- Причина отклонения/отмены -->
    <div v-if="booking.cancel_reason" class="note-block danger">
      <div class="note-title"><i class="fa fa-circle-xmark"></i>
        {{ booking.status === 'declined' ? 'Причина отклонения' : 'Причина отмены' }}
      </div>
      <p>{{ booking.cancel_reason }}</p>
    </div>

    <!-- Итог -->
    <div v-if="booking.status === 'completed' && booking.price_final" class="total-block">
      <span>Итого:</span>
      <strong>{{ booking.price_final }} ₽</strong>
    </div>

    <!-- ====== ДЕЙСТВИЯ ====== -->
    <div class="actions">
      <!-- КЛИЕНТ -->
      <template v-if="view === 'client'">
        <button
          v-if="canCancel"
          class="btn-action danger"
          @click="askCancel"
        >
          <i class="fa fa-ban"></i> Отменить заявку
        </button>
      </template>

      <!-- МАСТЕР -->
      <template v-else>
        <button
          v-if="booking.status === 'pending'"
          class="btn-action success"
          @click="onConfirm"
        >
          <i class="fa fa-check"></i> Подтвердить
        </button>
        <button
          v-if="booking.status === 'pending'"
          class="btn-action danger"
          @click="showDecline = true"
        >
          <i class="fa fa-times"></i> Отклонить
        </button>
        <button
          v-if="booking.status === 'confirmed' || booking.status === 'pending'"
          class="btn-action secondary"
          @click="showReschedule = true"
        >
          <i class="fa fa-calendar-edit"></i> Перенести
        </button>
        <button
          v-if="booking.status === 'confirmed'"
          class="btn-action primary"
          @click="onStart"
        >
          <i class="fa fa-play"></i> Начать работу
        </button>
        <button
          v-if="booking.status === 'in_progress' || booking.status === 'confirmed'"
          class="btn-action success"
          @click="showComplete = true"
        >
          <i class="fa fa-circle-check"></i> Завершить
        </button>
      </template>
    </div>

    <!-- Подмодалки -->
    <DeclineBookingModal
      :is-open="showDecline"
      :booking="booking"
      @close="showDecline = false"
      @done="onUpdated"
    />

    <RescheduleBookingModal
      :is-open="showReschedule"
      :booking="booking"
      @close="showReschedule = false"
      @done="onUpdated"
    />

    <CompleteBookingModal
      :is-open="showComplete"
      :booking="booking"
      @close="showComplete = false"
      @done="onUpdated"
    />

    <CancelBookingModal
      :is-open="showCancel"
      :booking="booking"
      @close="showCancel = false"
      @done="onCancelled"
    />
  </ModalWrapper>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useBookingsStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import {
  bookingStatusLabel,
  bookingStatusIcon,
  formatBookingDate,
} from '@/utils/bookingHelpers'
import ModalWrapper from '@/components/modals/ModalWrapper.vue'
import DeclineBookingModal from '@/components/modals/bookings/DeclineBookingModal.vue'
import RescheduleBookingModal from '@/components/modals/bookings/RescheduleBookingModal.vue'
import CompleteBookingModal from '@/components/modals/bookings/CompleteBookingModal.vue'
import CancelBookingModal from '@/components/modals/bookings/CancelBookingModal.vue'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  booking: { type: Object, default: null },
  view: { type: String, default: 'client' }, // client | master
})
const emit = defineEmits(['close', 'changed', 'cancelled'])

const bookingsStore = useBookingsStore()
const toast = useToast()

const showDecline = ref(false)
const showReschedule = ref(false)
const showComplete = ref(false)
const showCancel = ref(false)

const title = computed(() => {
  if (!props.booking) return ''
  return props.view === 'client'
    ? (props.booking.business?.name || 'Заявка')
    : (props.booking.client?.username || 'Заявка')
})

const subtitle = computed(() => props.booking ? bookingStatusLabel(props.booking.status) : '')
const statusIcon = computed(() => props.booking ? bookingStatusIcon(props.booking.status) : 'calendar')

const iconColor = computed(() => {
  const s = props.booking?.status
  if (s === 'completed') return 'var(--success-text)'
  if (s === 'pending') return 'var(--warning-text)'
  if (s === 'cancelled' || s === 'declined') return 'var(--danger-text)'
  return 'var(--accent-text)'
})
const iconBgColor = computed(() => {
  const s = props.booking?.status
  if (s === 'completed') return 'var(--success-trans)'
  if (s === 'pending') return 'var(--warning-trans)'
  if (s === 'cancelled' || s === 'declined') return 'var(--danger-trans)'
  return 'var(--accent-trans)'
})

const canCancel = computed(() => {
  return props.booking && ['pending', 'confirmed'].includes(props.booking.status)
})

function close() { emit('close') }

async function onConfirm() {
  try {
    await bookingsStore.confirmBooking(props.booking.id)
    toast.success('Заявка подтверждена')
    emit('changed', bookingsStore.currentBooking)
  } catch (err) {
    toast.error(err.response?.data?.error || 'Ошибка')
  }
}

async function onStart() {
  try {
    await bookingsStore.startBooking(props.booking.id)
    toast.success('Работа начата')
    emit('changed', bookingsStore.currentBooking)
  } catch (err) {
    toast.error(err.response?.data?.error || 'Ошибка')
  }
}

function askCancel() {
  showCancel.value = true
}

function onUpdated(updated) {
  emit('changed', updated)
}

function onCancelled(updated) {
  emit('cancelled', updated)
}
</script>

<style scoped>
.details-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 14px 16px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  margin-bottom: 14px;
}
.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  font-size: 13px;
}
.info-row .label {
  color: var(--text-muted);
  flex-shrink: 0;
}
.info-row .value {
  color: var(--text-primary);
  text-align: right;
  word-break: break-word;
}
.info-row .value i {
  color: var(--accent-text);
  margin-right: 4px;
  font-size: 12px;
}
.info-row .value a {
  color: var(--accent-text);
}

.note-block {
  padding: 10px 14px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  margin-bottom: 10px;
}
.note-block.master { background: var(--accent-trans); }
.note-block.danger { background: var(--danger-trans); }
.note-title {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: var(--text-muted);
  font-weight: var(--fw-semibold);
  margin-bottom: 4px;
}
.note-block.danger .note-title { color: var(--danger-text); }
.note-block p {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
}

.total-block {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 14px;
  background: var(--success-trans);
  border-radius: var(--radius-md);
  margin: 10px 0;
  font-size: 14px;
}
.total-block strong {
  color: var(--success-text);
  font-size: 18px;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 16px;
}

.btn-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: var(--radius-md);
  border: none;
  font-size: 13px;
  font-weight: var(--fw-semibold);
  cursor: pointer;
  transition: all var(--transition-base);
  min-height: 42px;
  width: 100%;
}
.btn-action.primary { background: var(--accent); color: #fff; }
.btn-action.primary:hover { background: var(--accent-hover); }
.btn-action.success { background: var(--success); color: #fff; }
.btn-action.success:hover { background: var(--success-hover); }
.btn-action.danger { background: var(--danger); color: #fff; }
.btn-action.danger:hover { background: var(--danger-hover); }
.btn-action.secondary {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}
.btn-action.secondary:hover { background: var(--border-light); }
</style>
