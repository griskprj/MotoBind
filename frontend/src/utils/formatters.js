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

export const DIFFICULTY_LABELS = {
  easy: 'Легко',
  medium: 'Средне',
  hard: 'Сложно',
}

export const FLUID_LABELS = {
  oil: 'Моторное масло',
  coolant: 'Охлаждающая жидкость',
  brake: 'Тормозная жидкость',
  fork: 'Масло в вилке',
  gear: 'Масло в КПП',
  chain: 'Смазка цепи',
}

export const TOLERANCE_LABELS = {
  chain: 'Зазор цепи',
  valve: 'Зазор клапанов',
  spark: 'Зазор свечи',
  brake: 'Толщина колодок',
  tire: 'Давление в шинах',
}

export const MANUAL_STATUS_LABELS = {
  approved: 'Одобрен',
  moderate: 'На проверке',
  rejected: 'Отклонён',
  draft: 'Черновик',
}

// ===== User-related labels =====
export const USER_STATUS_LABELS = {
  active: 'Активен',
  banned: 'Заблокирован',
  pending: 'Ожидает',
}

export const USER_STATUS_CLASSES = {
  active: 'status-active',
  banned: 'status-banned',
  pending: 'status-pending',
}

export const USER_ROLE_LABELS = {
  admin: 'Администратор',
  motorcyclist: 'Мотоциклист',
  motoclub: 'Мотоклуб',
}

export const USER_EXPERIENCE_LABELS = {
  beginner: 'Новичок',
  intermediate: 'Опытный',
  expert: 'Эксперт',
}

export const SOCIAL_ICONS = {
  instagram: 'fa fa-instagram',
  youtube: 'fa fa-youtube',
  telegram: 'fa fa-telegram',
  vk: 'fa fa-vk',
  facebook: 'fa fa-facebook',
  twitter: 'fa fa-twitter',
  tiktok: 'fa fa-tiktok',
}

export function getUserStatusLabel(status) {
  return USER_STATUS_LABELS[status] || status || '—'
}

export function getUserStatusClass(status) {
  return USER_STATUS_CLASSES[status] || ''
}

export function getUserRoleLabel(role) {
  return USER_ROLE_LABELS[role] || role || '—'
}

export function getUserExperienceLabel(experience) {
  return USER_EXPERIENCE_LABELS[experience] || experience || 'Не указан'
}

export function getSocialIcon(platform) {
  return SOCIAL_ICONS[platform] || 'fa fa-link'
}

export function getFluidLabel(key) {
  return FLUID_LABELS[key] || key
}

export function getToleranceLabel(key) {
  return TOLERANCE_LABELS[key] || key
}

export function getManualStatusLabel(status) {
  return MANUAL_STATUS_LABELS[status] || status || '—'
}

export function getDifficultyLabel(difficulty) {
  return DIFFICULTY_LABELS[difficulty] || difficulty || '—'
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
