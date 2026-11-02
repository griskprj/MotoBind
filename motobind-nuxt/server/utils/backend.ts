import type { H3Event } from 'h3'
import { getAccessToken, getRefreshToken, setAuthCookies, clearAuthCookies } from './auth'

interface BackendOptions {
  method?: string
  query?: Record<string, any>
  body?: unknown
  headers?: Record<string, string>
}

export async function backendRequest<T>(
  event: H3Event,
  path: string,
  options: BackendOptions = {}
): Promise<T> {
  const config = useRuntimeConfig(event)
  const baseURL = config.flaskApiBase


  let token = getAccessToken(event)

  async function execute(token: string) {
    return await $fetch<T>(path, {
      baseURL,
      ...options,
      headers: {
        ...options.headers,
        Authorization: `Bearer ${token}`
      }
    })
  }

  if (!token) {
    throw createError({ statusCode: 401, statusMessage: 'Unauthorized' })
  }

  try {
    return await execute(token)
  } catch (error: any) {
    const status = error.statusCode ?? error.response?.status

    if (status === 401) {
      const refreshToken = getRefreshToken(event)
      if (refreshToken) {
        try {
          const result = await $fetch<{ access_token: string; refresh_token: string }>(
            `${baseURL}${config.flaskAuthPrefix}/refresh`,
            { method: 'POST', body: { refresh_token: refreshToken } }
          )
          setAuthCookies(event, result.access_token, result.refresh_token)
          return await execute(result.access_token)
        } catch {
          clearAuthCookies(event)
        }
      }
    }
    throw error
  }
}
