// ============================================================
// Общие типы API
// ============================================================

/**
 * Ошибка API в нормализованном виде.
 * Бэк отдаёт { timestamp, status, error, path, errors? }
 * (см. app/exceptions.py).
 */
export interface ApiError {
  status: number
  /** Человекочитаемое сообщение из поля `error` */
  message: string
  /** Ошибки по полям из Pydantic ValidationError: { name: 'Field required' } */
  fieldErrors?: Record<string, string>
  /** Сырой ответ бэка — на случай отладки */
  raw?: unknown
}

/**
 * Единый формат пагинации.
 */
export interface Pagination {
  total: number
  page: number
  per_page: number
  pages: number
  has_prev: boolean
  has_next: boolean
}

export interface Paginated<T> {
  items: T[]
  pagination: Pagination
}

/** Query-параметры пагинации */
export interface PaginationQuery {
  page?: number
  per_page?: number
}
