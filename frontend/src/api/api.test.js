import { beforeEach, describe, expect, it, vi } from 'vitest'

// ---- Mocks ----
const mockRequestUse = vi.fn()
const mockResponseUse = vi.fn()
const mockApiCall = vi.fn()
const mockApiPost = vi.fn()
const mockApiGet = vi.fn()
const mockApiPut = vi.fn()
const mockApiDelete = vi.fn()

const mockLogout = vi.fn()
const mockSetTokensFromRefresh = vi.fn()

vi.mock('axios', () => {
  const mockInstance = vi.fn(mockApiCall)
  mockInstance.post = mockApiPost
  mockInstance.get = mockApiGet
  mockInstance.put = mockApiPut
  mockInstance.delete = mockApiDelete
  mockInstance.interceptors = {
    request: { use: mockRequestUse },
    response: { use: mockResponseUse },
  }

  return {
    default: { create: vi.fn(() => mockInstance) },
  }
})

vi.mock('../stores/auth', () => ({
  useAuthStore: () => ({
    logout: mockLogout,
    setTokensFromRefresh: mockSetTokensFromRefresh,
  }),
}))


describe('api.js', () => {
  let requestInterceptor
  let responseInterceptorSuccess
  let responseInterceptorError

  beforeEach(async () => {
    vi.clearAllMocks()
    localStorage.clear()
    mockRequestUse.mockClear()
    mockResponseUse.mockClear()

    vi.resetModules()
    await import('./api.js')

    requestInterceptor = mockRequestUse.mock.calls[0][0]
    responseInterceptorSuccess = mockResponseUse.mock.calls[0][0]
    responseInterceptorError = mockResponseUse.mock.calls[0][1]
  })

  // ---- Request interceptor ----

  describe('request interceptor', () => {
    it('adds Authorization header when token exists', () => {
      localStorage.setItem('access_token', 'test-token-123')
      const config = { headers: {} }
      const result = requestInterceptor(config)
      expect(result.headers.Authorization).toBe('Bearer test-token-123')
    })

    it('does not add Authorization header when no token', () => {
      const config = { headers: {} }
      const result = requestInterceptor(config)
      expect(result.headers.Authorization).toBeUndefined()
    })
  })

  // ---- Response interceptor: success ----

  describe('response interceptor: success', () => {
    it('passes successful response through', async () => {
      const response = { status: 200, data: { ok: true } }
      const result = await responseInterceptorSuccess(response)
      expect(result).toBe(response)
    })
  })

  // ---- Response interceptor: non-retry errors ----

  describe('response interceptor: non-401 errors', () => {
    it('rejects 500 without refresh', async () => {
      const error = {
        response: { status: 500 },
        config: { url: '/test', headers: {} },
      }
      await expect(responseInterceptorError(error)).rejects.toBe(error)
      expect(mockSetTokensFromRefresh).not.toHaveBeenCalled()
      expect(mockApiPost).not.toHaveBeenCalled()
    })

    it('rejects 403 without refresh', async () => {
      const error = {
        response: { status: 403 },
        config: { url: '/test', headers: {} },
      }
      await expect(responseInterceptorError(error)).rejects.toBe(error)
      expect(mockSetTokensFromRefresh).not.toHaveBeenCalled()
    })

    it('does not refresh on /auth/refresh URL', async () => {
      const error = {
        response: { status: 401 },
        config: { url: '/auth/refresh', headers: {} },
      }
      await expect(responseInterceptorError(error)).rejects.toBe(error)
      expect(mockApiPost).not.toHaveBeenCalled()
    })

    it('does not refresh if already retried', async () => {
      const error = {
        response: { status: 401 },
        config: { url: '/test', headers: {}, _retry: true },
      }
      await expect(responseInterceptorError(error)).rejects.toBe(error)
      expect(mockApiPost).not.toHaveBeenCalled()
    })
  })

  // ---- Response interceptor: 401 → refresh success ----

  describe('response interceptor: 401 → refresh success', () => {
    it('calls /auth/refresh and retries the original request', async () => {
      localStorage.setItem('refresh_token', 'refresh-old')
      localStorage.setItem('access_token', 'access-old')

      mockApiPost.mockResolvedValueOnce({
        data: {
          access_token: 'access-new',
          refresh_token: 'refresh-new',
        },
      })

      mockApiCall.mockResolvedValueOnce({ status: 200, data: { ok: true } })

      const originalRequest = {
        url: '/test',
        headers: {},
      }
      const error = {
        response: { status: 401 },
        config: originalRequest,
      }

      const result = await responseInterceptorError(error)

      expect(mockApiPost).toHaveBeenCalledWith('/auth/refresh', {
        refresh_token: 'refresh-old',
      })

      expect(localStorage.getItem('access_token')).toBe('access-new')
      expect(localStorage.getItem('refresh_token')).toBe('refresh-new')

      expect(mockSetTokensFromRefresh).toHaveBeenCalledWith('access-new', 'refresh-new')

      expect(originalRequest.headers.Authorization).toBe('Bearer access-new')
      expect(mockApiCall).toHaveBeenCalledWith(originalRequest)

      expect(result).toEqual({ status: 200, data: { ok: true } })
    })
  })

  // ---- Response interceptor: 401 → refresh fail ----

  describe('response interceptor: 401 → refresh fail', () => {
    it('logs out and redirects on refresh failure', async () => {
      localStorage.setItem('refresh_token', 'refresh-old')
      localStorage.setItem('access_token', 'access-old')
      localStorage.setItem('user', JSON.stringify({ id: 1 }))

      const refreshError = new Error('Refresh failed')
      mockApiPost.mockRejectedValueOnce(refreshError)

      const originalLocation = window.location
      delete window.location
      window.location = { pathname: '/garage', href: '' }

      const error = {
        response: { status: 401 },
        config: { url: '/test', headers: {} },
      }

      await expect(responseInterceptorError(error)).rejects.toBe(refreshError)

      expect(localStorage.getItem('access_token')).toBeNull()
      expect(localStorage.getItem('refresh_token')).toBeNull()
      expect(localStorage.getItem('user')).toBeNull()

      expect(mockLogout).toHaveBeenCalled()

      expect(window.location.href).toBe('/login')

      window.location = originalLocation
    })

    it('does not redirect if already on /login', async () => {
      localStorage.setItem('refresh_token', 'refresh-old')
      mockApiPost.mockRejectedValueOnce(new Error('fail'))

      const originalLocation = window.location
      delete window.location
      window.location = { pathname: '/login', href: '' }

      const error = {
        response: { status: 401 },
        config: { url: '/test', headers: {} },
      }

      await expect(responseInterceptorError(error)).rejects.toThrow()

      expect(window.location.href).toBe('')

      window.location = originalLocation
    })

    it('throws if no refresh token available', async () => {
      localStorage.setItem('access_token', 'access-old')

      const originalLocation = window.location
      delete window.location
      window.location = { pathname: '/garage', href: '' }

      const error = {
        response: { status: 401 },
        config: { url: '/test', headers: {} },
      }

      await expect(responseInterceptorError(error)).rejects.toThrow('No refresh token')

      expect(mockApiPost).not.toHaveBeenCalled()
      expect(mockLogout).toHaveBeenCalled()

      window.location = originalLocation
    })
  })
})