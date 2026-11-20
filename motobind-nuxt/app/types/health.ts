// ============================================================
// Сводка состояния мотоцикла
// ============================================================

export type ComponentHealthStatus = 'ok' | 'due_soon' | 'overdue' | 'unknown'

export interface ComponentHealthItem {
  id: number
  name: string
  category: string
  template_key: string | null
  condition_rating: string | null
  is_safety: boolean
  status: ComponentHealthStatus
  remaining_km: number | null
  remaining_days: number | null
  limited_by: 'km' | 'days' | null
  is_estimate: boolean
}

export interface HealthOverall {
  percent: number | null
  label: string
  is_estimate: boolean
}

export interface MotorcycleHealth {
  motorcycle_id: number
  current_mileage: number | null
  is_estimate: boolean
  overall: HealthOverall
  counts: {
    total: number
    ok: number
    due_soon: number
    overdue: number
    unknown: number
    safety_attention: number
  }
  safety_attention: ComponentHealthItem[]
  attention: ComponentHealthItem[]
  upcoming: ComponentHealthItem[]
  no_data: ComponentHealthItem[]
  items: ComponentHealthItem[]
}
