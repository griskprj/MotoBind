import type { Maintenance } from './maintenance'

// ============================================================
// Motorcycle
// ============================================================

export type DriveType = 'chain' | 'belt' | 'shaft'

/**
 * Краткая карточка мотоцикла (MotorcycleShortSchema).
 * GET /api/motorcycle/ отдаёт Detail (с maintenances), но
 */
export interface MotorcycleShort {
  id: number
  name: string
  years?: string | null
  volume?: number | null
  drive_type?: DriveType | null
  color?: string | null
  license_plate?: string | null
  vin?: string | null
  photo_url?: string | null
  created_at: string
}

/**
 * Детальная карточка (MotorcycleDetailSchema).
 * GET /api/motorcycle/<id> и GET /api/motorcycle/ (список) отдают это.
 */
export interface Motorcycle extends MotorcycleShort {
  maintenances: Maintenance[]
  note?: string | null
  mileage?: number | null
  updated_at?: string
}

/**
 * Payload создания (CreateMotorcycleSchema).
 */
export interface CreateMotorcyclePayload {
  name: string
  years?: string | null
  volume?: number | null
  drive_type?: DriveType
  color?: string | null
  licensePlate?: string | null
  vin?: string | null
  note?: string | null
}

/**
 * Payload обновления (UpdateMotorcycleSchema).
 */
export interface UpdateMotorcyclePayload {
  name?: string
  years?: string | null
  volume?: number | null
  drive_type?: DriveType
  color?: string | null
  licensePlate?: string | null
  vin?: string | null
  note?: string | null
}
