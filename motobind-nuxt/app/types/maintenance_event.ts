// ============================================================
// События обслуживания
// ============================================================

export type WorkKind = 'replace' | 'inspect' | 'adjust' | 'repair' | 'other'

export interface MaintenanceWork {
  id: number
  event_id: number
  component_id: number | null
  kind: WorkKind
  title: string | null
  cost: number
  note: string | null
  created_at: string
}

export interface MaintenanceEvent {
  id: number
  user_id: number
  motorcycle_id: number
  date: string                // YYYY-MM-DD
  mileage: number | null
  total_cost: number
  comment: string | null
  created_at: string
  updated_at: string
  works: MaintenanceWork[]
}

export interface CreateWorkPayload {
  component_id?: number | null
  kind?: WorkKind
  title?: string | null
  cost?: number | null
  note?: string | null
}

export interface CreateMaintenanceEventPayload {
  motorcycleId: number | string
  date: string
  mileage?: number | null
  totalCost?: number | null
  comment?: string | null
  works: CreateWorkPayload[]
}

export interface UpdateMaintenanceEventPayload {
  date?: string
  mileage?: number | null
  totalCost?: number | null
  comment?: string | null
  works?: CreateWorkPayload[]
}

export interface MaintenanceEventsListResponse {
  events: MaintenanceEvent[]
  total: number
  page: number
  per_page: number
  pages: number
}
