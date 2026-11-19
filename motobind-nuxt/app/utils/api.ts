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

  if (typeof error !== 'object' || error === null) {
    return fallback
  }

  const err = error as Record<string, any>

  const status =
    err.statusCode ??
    err.status ??
    0

  const payloads = [
    err.data,
    err.data?.data,
    err.response?._data,
    err.cause?.data,
  ]

  const getString = (...values: unknown[]): string | undefined => {
    return values.find(
      (value): value is string =>
        typeof value === 'string' && value.trim().length > 0
    )
  }

  let message: string | undefined

  for (const payload of payloads) {
    if (!payload || typeof payload !== 'object') continue

    message = getString(
      payload.error,
      payload.message,
      payload.detail,
    )

    if (message) break
  }

  message ??= getString(err.message) ?? fallback.message

  let fieldErrors: Record<string, string> | undefined

  for (const payload of payloads) {
    if (!payload || typeof payload !== 'object') continue

    const validationErrors = payload.errors

    if (!Array.isArray(validationErrors)) continue

    fieldErrors = {}

    for (const item of validationErrors) {
      const key = item.loc
        ?.filter((part: unknown) => typeof part === 'string')
        .pop()

      if (key && typeof item.msg === 'string' && item.msg.trim()) {
        fieldErrors[key] = item.msg
      }
    }

    if (Object.keys(fieldErrors).length === 0) {
      fieldErrors = undefined
    }

    if (fieldErrors) break
  }

  return {
    status,
    message,
    fieldErrors,
    raw: error,
  }
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

export function asString(val: string | number | null | undefined): string {
  if (val === null || val === undefined) return ''
  return String(val)
}

export { baseFetch }
