<template>
  <div class="booking-card" :class="'status-' + booking.status" @click="$emit('click', booking)">
    <div class="bc-top">
      <div class="bc-icon">
        <i :class="statusIcon"></i>
      </div>
      <div class="bc-title">
        <template v-if="view === 'client'">
          {{ booking.business?.name || 'Мастер' }}
        </template>
        <template v-else>
          {{ booking.client?.username || 'Клиент' }}
        </template>
      </div>
      <span :class="'badge badge-' + statusVariant">
        {{ statusLabel }}
      </span>
    </div>

    <div class="bc-meta">
      <div class="meta-row">
        <i class="fa fa-calendar"></i>
        <span>{{ formatBookingDate(booking.scheduled_at) }}</span>
      </div>
      <div v-if="booking.service" class="meta-row">
        <i class="fa fa-wrench"></i>
        <span>{{ booking.service.title }}</span>
      </div>
      <div v-if="booking.motorcycle" class="meta-row">
        <i class="fa fa-motorcycle"></i>
        <span>{{ booking.motorcycle.name }}</span>
      </div>
    </div>

    <div v-if="booking.client_note" class="bc-note">
      <i class="fa fa-comment-dots"></i> {{ booking.client_note }}
    </div>

    <div v-if="booking.status === 'declined' && booking.cancel_reason" class="bc-decline">
      <i class="fa fa-circle-xmark"></i> {{ booking.cancel_reason }}
    </div>

    <div v-if="booking.status === 'completed' && booking.price_final" class="bc-price">
      Итого: <strong>{{ booking.price_final }} ₽</strong>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import {
  bookingStatusLabel,
  bookingStatusVariant,
  bookingStatusIcon,
  formatBookingDate,
} from '@/utils/bookingHelpers'

const props = defineProps({
  booking: { type: Object, required: true },
  view: { type: String, default: 'client' },
})
defineEmits(['click'])

const statusLabel = computed(() => bookingStatusLabel(props.booking.status))
const statusVariant = computed(() => bookingStatusVariant(props.booking.status))
const statusIcon = computed(() => bookingStatusIcon(props.booking.status))
</script>

<style scoped>
.booking-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-left: 3px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 14px 16px;
  cursor: pointer;
  transition: all var(--transition-base);
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.booking-card:hover {
  border-color: var(--accent);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}
.status-pending     { border-left-color: var(--warning); }
.status-confirmed   { border-left-color: var(--accent); }
.status-in_progress { border-left-color: var(--accent); }
.status-completed   { border-left-color: var(--success); }
.status-cancelled   { border-left-color: var(--border-color); opacity: 0.75; }
.status-declined    { border-left-color: var(--danger); opacity: 0.85; }

.bc-top {
  display: flex;
  align-items: center;
  gap: 10px;
}
.bc-icon {
  width: 34px;
  height: 34px;
  min-height: 34px;
  border-radius: var(--radius-md);
  background: var(--accent-trans);
  color: var(--accent-text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
}
.bc-title {
  flex: 1;
  min-width: 0;
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.bc-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 13px;
  color: var(--text-secondary);
}
.meta-row {
  display: flex;
  align-items: center;
  gap: 6px;
}
.meta-row i {
  width: 14px;
  min-width: 14px;
  color: var(--text-muted);
  font-size: 12px;
}

.bc-note {
  padding: 8px 10px;
  background: var(--bg-secondary);
  border-radius: var(--radius-sm);
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.5;
}
.bc-note i { color: var(--accent-text); margin-right: 4px; }

.bc-decline {
  padding: 8px 10px;
  background: var(--danger-trans);
  border-radius: var(--radius-sm);
  font-size: 12px;
  color: var(--danger-text);
}
.bc-decline i { margin-right: 4px; }

.bc-price {
  font-size: 13px;
  color: var(--text-secondary);
  text-align: right;
}
.bc-price strong { color: var(--accent-text); font-size: 15px; }

.badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: var(--fw-medium);
  white-space: nowrap;
  flex-shrink: 0;
}
.badge-warning { background: var(--warning-trans); color: var(--warning-text); }
.badge-accent  { background: var(--accent-trans);  color: var(--accent-text); }
.badge-success { background: var(--success-trans); color: var(--success-text); }
.badge-danger  { background: var(--danger-trans);  color: var(--danger-text); }
.badge-gray    { background: var(--border-light);  color: var(--text-muted); }
</style>
