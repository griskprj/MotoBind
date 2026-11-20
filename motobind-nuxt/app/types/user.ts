export interface UserStats {
  posts_count: number
  likes_received: number
  comments_received: number
}

export interface UserProfile {
  id: number
  email: string
  username: string
  role: 'motorcyclist' | 'motoclub' | 'admin'
  status: 'active' | 'banned'
  avatar?: string | null
  created_at?: string
  stats?: UserStats
}

export interface NotificationSettings {
  email_notifications_enabled: boolean
  email_newsletter_enabled: boolean
  email_verification_enabled: boolean
  reminders_mileage_enabled: boolean
  reminders_maintenance_enabled: boolean
}
