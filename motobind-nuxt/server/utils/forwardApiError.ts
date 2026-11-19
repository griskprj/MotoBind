
export function forwardApiError(error: unknown): never {
  const err = error as {
    response?: {
      status?: number
      statusText?: string
      _data?: unknown
    }
    data?: unknown
    statusCode?: number
  }

  const backendData =
    err.response?._data ?? err.data

  const data =
    typeof backendData === 'object' && backendData !== null
      ? backendData as Record<string, unknown>
      : {}

  const message =
    typeof data.error === 'string'
      ? data.error
      : typeof data.message === 'string'
        ? data.message
        : typeof data.detail === 'string'
          ? data.detail
          : 'Не удалось выполнить запрос'

  const statusCode =
    err.response?.status ??
    err.statusCode ??
    500

  throw createError({
    statusCode,
    statusMessage: err.response?.statusText || 'API Error',
    message,
    data: backendData,
  })
}
