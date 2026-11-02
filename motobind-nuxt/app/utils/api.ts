import type { ApiError } from '~/types'
import { getHeader } from 'h3'

/**
 * Базовый $fetch для всех запросов к бэкенду.
 */
const baseFetch = $fetch.create({
  baseURL: '/api/backend',
  credentials: 'include',
  headers: {
    Accept: 'application/json',
  },
  onRequest({ options }) {
    if (import.meta.server) {
      const nuxtApp = useNuxtApp()
      const event = nuxtApp.ssrContext?.event
      if (event) {
        const cookie = getHeader(event, 'cookie')
        if (cookie) {
          options.headers = { ...options.headers, cookie }
        }
      }
    }
  },
  async onResponseError({ response }) {
    if (response.status === 401 && import.meta.client) {
      const auth = useAuthStore()
      auth.user = null
      auth.status = 'guest'
      const route = useRoute()
      await navigateTo({ path: '/login', query: { redirect: route.fullPath } })
    }
  },
})

/**
 * Парсит ошибку $fetch/ofetch в нормализованный ApiError.
 */
export function parseApiError(error: unknown): ApiError {
  const fallback: ApiError = {
    status: 0,
    message: 'Не удалось выполнить запрос',
    raw: error,
  }

  if (typeof error !== 'object' || error === null) return fallback

  const err = error as {
    status?: number
    statusCode?: number
    data?: {
      error?: string
      message?: string
      detail?: string
      errors?: Array<{ loc?: (string | number)[]; msg?: string }>
    }
    message?: string
  }

  const status = err.status ?? err.statusCode ?? 0
  const data = err.data

  const message =
    data?.error ||
    data?.message ||
    data?.detail ||
    err.message ||
    fallback.message

    let fieldErrors: Record<string, string> | undefined
    if (Array.isArray(data?.errors)) {
      fieldErrors = {}
      for (const e of data.errors) {
        const key = e.loc?.filter((s) => typeof s === 'string').pop()
        if (key && typeof e.msg === 'string' && e.msg.trim()) {
          fieldErrors[key] = e.msg
        }
      }
      if (Object.keys(fieldErrors).length === 0) fieldErrors = undefined
    }

  return { status, message, fieldErrors, raw: error }
}

export async function request<T>(
  fn: () => Promise<T>,
): Promise<T> {
  try {
    return await fn()
  } catch (e) {
    throw parseApiError(e)
  }
}

/** Безопасно приводит значение к строке (числа -> строки, null/undefined -> '') */
export function asString(val: string | number | null | undefined): string {
  if (val === null || val === undefined) return ''
  return String(val)
}

export { baseFetch }
