import axios from 'axios'

const TOKEN_KEY = 'access_token'
const REFRESH_TOKEN_KEY = 'refresh_token'
const USER_KEY = 'user'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
})

// ===== In-memory HTTP cache для GET =====
// Кеш по умолчанию выключен: чтобы закешировать — передать { cache: 30_000 } в config
// TTL в миллисекундах. 30_000 = 30 секунд.
const cache = new Map()
const CACHE_PREFIX = '__cache__:'

function cacheKey(url, params) {
  const p = params ? JSON.stringify(params) : ''
  return `${url}?${p}`
}

function getFromCache(key) {
  const entry = cache.get(key)
  if (!entry) return null
  if (Date.now() > entry.expiresAt) {
    cache.delete(key)
    return null
  }
  return entry.data
}

function setCache(key, data, ttl) {
  cache.set(key, { data, expiresAt: Date.now() + ttl })
}

function invalidateCache() {
  cache.clear()
}

// ===== Refresh-queue =====
let isRefreshing = false
let failedQueue = []

function processQueue(error, token = null) {
  failedQueue.forEach((prom) => {
    if (error) prom.reject(error)
    else prom.resolve(token)
  })
  failedQueue = []
}

async function syncStoreAfterLogout() {
  try {
    const { useAuthStore } = await import('../stores/auth')
    useAuthStore().logout()
  } catch {}
}

async function syncStoreAfterRefresh(accessToken, refreshToken) {
  try {
    const { useAuthStore } = await import('../stores/auth')
    useAuthStore().setTokensFromRefresh(accessToken, refreshToken)
  } catch {}
}

// ===== Request interceptor =====
api.interceptors.request.use(
  (config) => {
    if (config.method === 'get' && config.cache) {
      const key = cacheKey(config.url, config.params)
      const cached = getFromCache(key)
      if (cached) {
        config.adapter = () => {
          return Promise.resolve({
            data: cached,
            status: 200,
            statusText: 'OK (from cache)',
            headers: {},
            config,
            request: null,
          })
        }
      }
    }

    const token = localStorage.getItem(TOKEN_KEY)
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// ===== Response interceptor =====
api.interceptors.response.use(
  (response) => {
    const { config } = response

    if (config && config.method) {
      if (config.method === 'get' && config.cache) {
        const key = cacheKey(config.url, config.params)
        setCache(key, response.data, config.cache)
      }

      if (['post', 'put', 'patch', 'delete'].includes(config.method)) {
        invalidateCache()
      }
    }

    return response
  },
  async (error) => {
    const originalRequest = error.config

    if (
      (error.response?.status === 401 || error.response?.status === 422) &&
      !originalRequest._retry &&
      !originalRequest.url?.includes('/auth/refresh')
    ) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`
            return api(originalRequest)
          })
          .catch((err) => Promise.reject(err))
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY)
        if (!refreshToken) throw new Error('No refresh token')

        const response = await api.post('/auth/refresh', {
          refresh_token: refreshToken,
        })

        const { access_token, refresh_token } = response.data
        localStorage.setItem(TOKEN_KEY, access_token)
        localStorage.setItem(REFRESH_TOKEN_KEY, refresh_token)

        await syncStoreAfterRefresh(access_token, refresh_token)

        originalRequest.headers.Authorization = `Bearer ${access_token}`
        processQueue(null, access_token)

        return api(originalRequest)
      } catch (refreshError) {
        processQueue(refreshError, null)
        localStorage.removeItem(TOKEN_KEY)
        localStorage.removeItem(REFRESH_TOKEN_KEY)
        localStorage.removeItem(USER_KEY)

        await syncStoreAfterLogout()

        failedQueue = []
        isRefreshing = false

        if (window.location.pathname !== '/login') {
          window.location.href = '/login'
        }

        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)

export function clearApiCache() {
  invalidateCache()
}

export default api
