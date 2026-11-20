export interface Author {
  id: number
  username: string
}

export interface CourseShort {
  id: number
  slug: string
  title: string
  short_description?: string | null
  cover_url?: string | null
  category?: string | null
  level?: 'beginner' | 'intermediate' | 'advanced' | null
  price: number
  is_free: boolean
  lessons_count: number
  author?: Author | null
  created_at?: string | null
  published_at?: string | null
  is_purchased: boolean
}

export interface LessonShort {
  id: number
  slug: string
  order: number
  title: string
  is_free_preview: boolean
  has_video: boolean
  video_duration?: number | null
  is_completed: boolean
  is_accessible: boolean
}

export interface CourseProgress {
  completed: number
  total: number
}

export interface CourseDetail extends CourseShort {
  description?: string | null
  lessons: LessonShort[]
  progress: CourseProgress
  last_viewed_lesson_id?: number | null
}

export interface LessonNav {
  slug: string
  title: string
  order: number
  is_accessible: boolean
}

export interface LessonDetail {
  id: number
  slug: string
  order: number
  title: string
  content: string
  video_url?: string | null
  video_duration?: number | null
  cover_url?: string | null
  is_free_preview: boolean
  course_id: number
  course_slug: string
  course_title: string
  is_completed: boolean
  prev_lesson?: LessonNav | null
  next_lesson?: LessonNav | null
}

export interface ArticleShort {
  id: number
  slug: string
  title: string
  short_description?: string | null
  cover_url?: string | null
  category?: string | null
  tags: string[]
  author?: Author | null
  created_at?: string | null
  published_at?: string | null
}

export interface ArticleDetail extends ArticleShort {
  content: string
  updated_at?: string | null
  related: ArticleShort[]
}

export interface CourseListResponse {
  courses: CourseShort[]
  pagination: Pagination
}

export interface ArticleListResponse {
  articles: ArticleShort[]
  pagination: Pagination
}

export interface MyLearningResponse {
  in_progress: CourseWithProgress[]
  completed: CourseWithProgress[]
  not_started: CourseWithProgress[]
}

export interface CourseWithProgress {
  course: CourseShort
  progress: CourseProgress
  last_viewed_lesson_slug?: string | null
  last_viewed_lesson_title?: string | null
}
