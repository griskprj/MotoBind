// ============================================================
// Auth / User
// ============================================================

export type UserRole = 'user' | 'admin' | 'business' | 'master'
export type UserStatus = 'active' | 'blocked' | 'pending'
export type BusinessAccountType = 'none' | 'service' | 'store' | 'master'

/**
 * Ответ GET /api/auth/me (UserResponseSchema).
 */
export interface User {
  id: number
  email: string
  username: string
  role: UserRole
  status: UserStatus
  has_business_account: boolean
  business_account_type: BusinessAccountType
  avatar?: string | null
  created_at: string

  notify_email?: boolean
  notify_push?: boolean
}

/**
 * Ответ POST /api/auth/login (LoginResponseSchema):
 * { message, access_token, refresh_token, user }
 */
export interface LoginResponse {
  message: string
  access_token: string
  refresh_token: string
  user: User
}

export interface LoginPayload {
  email: string
  password: string
  rememberMe?: boolean
}

export interface RegisterPayload {
  email: string
  username: string
  password: string
  role?: 'motorcyclist' | 'motoclub'
}
