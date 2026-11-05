// ============================================================
// Компоненты мотоцикла
// ============================================================
import type { WorkKind } from './maintenance_event'

export type ComponentCategory =
  | 'fluid'
  | 'filter'
  | 'ignition'
  | 'brake'
  | 'drive'
  | 'other'

export type ConditionRating = 'good' | 'ok' | 'bad' | 'unknown'

export interface MotorcycleComponent {
  id: number
  motorcycle_id: number
  template_key: string | null
  name: string
  category: ComponentCategory
  manufacturer: string | null
  part_number: string | null
  interval_km: number | null
  interval_days: number | null
  last_service_date: string | null   // YYYY-MM-DD
  last_service_mileage: number | null
  condition_rating: ConditionRating | null
  condition_note: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface ComponentListResponse {
  components: MotorcycleComponent[]
  total: number
}

export interface CreateComponentPayload {
  name: string
  category?: ComponentCategory
  manufacturer?: string | null
  part_number?: string | null
  interval_km?: number | null
  interval_days?: number | null
  last_service_date?: string | null
  last_service_mileage?: number | null
  condition_rating?: ConditionRating | null
  condition_note?: string | null
}

export type UpdateComponentPayload = Partial<CreateComponentPayload>

export interface ApplyTemplatePayload {
  style?: 'calm' | 'normal' | 'aggressive'
  terrain?: 'city' | 'highway' | 'mixed' | 'dusty' | 'offroad'
}

export interface ApplyTemplateResponse {
  created: { template_key: string; name: string }[]
  skipped: { template_key: string; name: string }[]
  drive_type: 'chain' | 'belt' | 'shaft'
  counts: { created: number; skipped: number }
}

// ---------- История компонента ----------

export interface ComponentHistoryEvent {
  id: number
  date: string
  mileage: number | null
  comment: string | null
}

export interface ComponentHistoryItem {
  id: number
  event_id: number
  component_id: number | null
  kind: WorkKind
  title: string | null
  cost: number
  note: string | null
  created_at: string
  event?: ComponentHistoryEvent | null
}

export interface ComponentHistoryResponse {
  component: MotorcycleComponent
  history: ComponentHistoryItem[]
}
