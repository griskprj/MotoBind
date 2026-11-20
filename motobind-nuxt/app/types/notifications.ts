export interface Notification {
  id: number
  type: string
  title: string
  content: string
  link?: string | null
  is_read: boolean
  created_at: string
  extra_data?: Record<string, any> | null
}

export interface NotificationsResponse {
  notifications: Notification[]
  total: number
  pages: number
  current_page: number
  per_page: number
  has_prev: boolean
  has_next: boolean
}

export interface UnreadCountResponse {
  unread_count: number
}
