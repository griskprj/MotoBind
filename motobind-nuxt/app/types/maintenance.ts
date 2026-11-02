// ============================================================
// Maintenance (обслуживание)
// ============================================================

export type MaintenanceType = 'planned' | 'completed'

/**
 * Одна запись обслуживания.
 */
export interface Maintenance {
  id: number
  motorcycle_id: number
  category: string
  title: string
  description?: string | null
  status: MaintenanceType
  planned_date?: string | null   // YYYY-MM-DD
  completed_date?: string | null // YYYY-MM-DD
  planned_mileage?: number | null
  completed_mileage?: number | null
  cost?: number | null
  created_at: string
  updated_at?: string
}

/**
 * Payload для создания.
 */
export interface CreateMaintenancePayload {
  motorcycleId: number | string
  category: string
  title: string
  description?: string | null
  planned_date?: string | null
  planned_mileage?: number | null
  completed_date?: string | null
  completed_mileage?: number | null
  cost?: number | null
}

/**
 * Payload для «отметить выполненным».
 */
export interface CompleteMaintenancePayload {
  completed_mileage: number
  completed_date?: string | null
  cost?: number | null
  is_repeat?: boolean
  interval?: number | null
  interval_days?: number | null
}

export interface CompleteMaintenanceResponse {
  message: string
  maintenance: Maintenance
  new_planned: Maintenance | null
}

/**
 * Payload для PUT /maintenance/<id> (UpdateMaintenanceSchema).
 */
export interface UpdateMaintenancePayload {
  category?: string
  title?: string
  description?: string | null
  planned_date?: string | null
  planned_mileage?: number | null
  completed_date?: string | null
  completed_mileage?: number | null
  cost?: number | null
}
