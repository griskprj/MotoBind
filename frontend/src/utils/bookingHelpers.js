/**
 * Хелперы для заявок: статусы, иконки, форматы.
 */

export const BOOKING_STATUS = {
  pending:     'pending',
  confirmed:   'confirmed',
  in_progress: 'in_progress',
  completed:   'completed',
  cancelled:   'cancelled',
  declined:    'declined',
}

export function bookingStatusLabel(status) {
  return {
    pending:     'Ожидает',
    confirmed:   'Подтверждена',
    in_progress: 'В работе',
    completed:   'Завершена',
    cancelled:   'Отменена',
    declined:    'Отклонена',
  }[status] || status
}

export function bookingStatusVariant(status) {
  return {
    pending:     'warning',
    confirmed:   'accent',
    in_progress: 'accent',
    completed:   'success',
    cancelled:   'gray',
    declined:    'danger',
  }[status] || 'gray'
}

export function bookingStatusIcon(status) {
  return {
    pending:     'fa fa-clock',
    confirmed:   'fa fa-check',
    in_progress: 'fa fa-wrench',
    completed:   'fa fa-circle-check',
    cancelled:   'fa fa-ban',
    declined:    'fa fa-circle-xmark',
  }[status] || 'fa fa-circle'
}

/**
 * Приводит ISO-дату к локальному виду:
 *  - «Сегодня, 14:00»
 *  - «Завтра, 10:30»
 *  - «12 ноя, 09:00»
 */
export function formatBookingDate(iso) {
  if (!iso) return '—'
  const d = new Date(iso)
  if (isNaN(d)) return '—'

  const now = new Date()
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  const target = new Date(d.getFullYear(), d.getMonth(), d.getDate())
  const diffDays = Math.round((target - today) / 86400000)

  const time = d.toLocaleTimeString('ru-RU', {
    hour: '2-digit',
    minute: '2-digit',
  })

  if (diffDays === 0) return `Сегодня, ${time}`
  if (diffDays === 1) return `Завтра, ${time}`
  if (diffDays === -1) return `Вчера, ${time}`

  const dateStr = d.toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: 'short',
    year: d.getFullYear() === now.getFullYear() ? undefined : 'numeric',
  })
  return `${dateStr}, ${time}`
}

export function bookingTabList() {
  return [
    { id: 'all',         label: 'Все' },
    { id: 'pending',     label: 'Ожидают' },
    { id: 'confirmed',   label: 'Подтверждены' },
    { id: 'in_progress', label: 'В работе' },
    { id: 'completed',   label: 'Завершены' },
    { id: 'cancelled',   label: 'Отменены' },
    { id: 'declined',    label: 'Отклонены' },
  ]
}
