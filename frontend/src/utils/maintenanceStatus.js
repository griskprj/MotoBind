export function getEffectiveStatus(maintenance, motorcycle) {
  if (maintenance.status === 'completed') return 'completed'

  const currentMileage = motorcycle?.mileage || 0
  const today = new Date().toISOString().split('T')[0]

  const mileageOverdue =
    maintenance.planned_mileage != null &&
    maintenance.planned_mileage <= currentMileage

  const dateOverdue =
    maintenance.planned_date != null &&
    maintenance.planned_date < today

  if (mileageOverdue || dateOverdue) return 'overdue'
  return 'planned'
}

export function getMaintenanceDistance(maintenance, motorcycle) {
  const currentMileage = motorcycle?.mileage || 0
  const currentDate = new Date()
  currentDate.setHours(0, 0, 0, 0)

  let distance = null
  if (maintenance.planned_mileage != null) {
    distance = maintenance.planned_mileage - currentMileage
  }

  let days = null
  if (maintenance.planned_date) {
    const planned = new Date(maintenance.planned_date)
    planned.setHours(0, 0, 0, 0)
    days = Math.round((planned - currentDate) / (1000 * 60 * 60 * 24))
  }

  const overdue =
    (distance != null && distance <= 0) ||
    (days != null && days < 0)

  return { overdue, distance, days }
}
