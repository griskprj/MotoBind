/**
 * Общие форматтеры. Использовать вместо локальных копий в компонентах.
 */

export function formatMileage(value) {
  if (value === null || value === undefined || value === '') return '—'
  const n = Number(value)
  if (Number.isNaN(n)) return '—'
  if (n >= 1000) return (n / 1000).toFixed(1) + ' тыс. км'
  return n + ' км'
}

export function formatCost(value) {
  if (!value) return '0 ₽'
  const n = Number(value)
  if (Number.isNaN(n)) return '0 ₽'
  if (n >= 1000) return (n / 1000).toFixed(1) + ' тыс. ₽'
  return Math.round(n) + ' ₽'
}

export function declensionMotorcycles(count) {
  const last = count % 10
  const last2 = count % 100
  if (last2 >= 11 && last2 <= 19) return 'мотоциклов'
  if (last === 1) return 'мотоцикл'
  if (last >= 2 && last <= 4) return 'мотоцикла'
  return 'мотоциклов'
}

export const STATUS_LABELS = {
  completed: 'Выполнено',
  planned: 'Запланировано',
  overdue: 'Просрочено',
}

export const STATUS_BADGE_VARIANT = {
  completed: 'success',
  planned: 'warning',
  overdue: 'danger',
}

export const CATEGORY_LABELS = {
  engine: 'Двигатель',
  drive: 'Привод',
  steering: 'Рулевое управление',
  suspension: 'Подвеска',
  electronics: 'Электроника',
  wheel: 'Колёса / Шины',
  brakes: 'Тормозная система',
  fuel: 'Топливная система',
  cooling: 'Система охлаждения',
  other: 'Другое',
}

export function getStatusLabel(status) {
  return STATUS_LABELS[status] || status || '—'
}

export function getStatusBadgeVariant(status) {
  return STATUS_BADGE_VARIANT[status] || 'gray'
}

export function getCategoryLabel(category) {
  return CATEGORY_LABELS[category] || category || 'Другое'
}
