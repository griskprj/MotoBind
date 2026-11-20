export interface PostComment {
  id: number
  post_id: number
  user_id: number
  author?: string | null
  author_avatar?: string | null
  content: string
  created_at?: string | null
}

export interface Post {
  id: number
  author_id: number
  author?: string | null
  author_avatar?: string | null
  content: string
  image?: string | null
  likes_count: number
  comments_count: number
  created_at?: string | null
  updated_at?: string | null
  is_liked?: boolean | null
  comments?: PostComment[]
}

export interface PostsListResponse {
  posts: Post[]
  total: number
  pages: number
  current_page: number
  per_page: number
  has_prev: boolean
  has_next: boolean
}

export interface LikeToggleResponse {
  liked: boolean
  likes_count: number
}

export interface ReportCategory {
  value: string
  label: string
}
