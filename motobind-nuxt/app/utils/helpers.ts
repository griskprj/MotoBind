// Вычисляет, сколько км осталось до планового ТО
// Возвращает объект: { diff: number | null, isOverdue: boolean }
export function getMileageRemaining(m: Maintenance & { motorcycle: Motorcycle }) {
  if (m.planned_mileage == null) return null
  if (m.motorcycle.mileage == null) return null

  const diff = m.planned_mileage - m.motorcycle.mileage

  return {
    diff,
    isOverdue: diff <= 0,
    isWarning: diff > 0 && diff <= 500,
  }
}

// Форматирование остатка км до ТО
export function formatRemaining(data: ReturnType<typeof getMileageRemaining>) {
  if (!data) return ''
  if (data.isOverdue) return `Просрочено на ${Math.abs(data.diff)} км`
  return `Осталось ${data.diff} км`
}
