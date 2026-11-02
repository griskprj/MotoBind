export interface AdminStats {
  total: number
  active: number
  banned: number
  admin: number
}

export interface AdminUser {
  id: number
  email: string
  username: string
  role: 'motorcyclist' | 'motoclub' | 'admin'
  status: 'active' | 'banned'
  created_at?: string
  avatar?: string | null
}

export interface AdminUsersResponse {
  users: AdminUser[]
  total: number
  pages: number
  current_page: number
  per_page: number
  has_prev: boolean
  has_next: boolean
  stats: AdminStats
}

export interface ReportSnapshot {
  content: string
  image?: string | null
  author_id: number
  author?: string | null
  author_avatar?: string | null
  created_at?: string | null
}

export interface AdminReport {
  id: number
  post_id: number | null
  reporter_id: number
  reporter?: string | null
  reporter_avatar?: string | null
  category: string
  category_label?: string | null
  description?: string | null
  status: 'pending' | 'resolved' | 'rejected'
  resolution_action?: 'post_deleted' | 'user_banned' | 'both' | 'none' | null
  resolution_note?: string | null
  resolved_by?: number | null
  resolved_at?: string | null
  created_at?: string | null
  post_snapshot?: ReportSnapshot | null
}

export interface AdminReportsResponse {
  reports: AdminReport[]
  total: number
  pages: number
  current_page: number
  per_page: number
  has_prev: boolean
  has_next: boolean
  stats: {
    total: number
    pending: number
    resolved: number
    rejected: number
  }
}
