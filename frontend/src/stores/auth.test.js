import { beforeEach, describe, expect, it } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useAuthStore } from './auth'

const TOKEN_KEY = 'access_token'
const REFRESH_TOKEN_KEY = 'refresh_token'
const USER_KEY = 'user'

describe('auth store', () => {
  beforeEach(() => {
    localStorage.clear()
    // Свежий Pinia для каждого теста — чтобы hydration переиспользовался
    setActivePinia(createPinia())
  })

  // ---- Hydration ----

  describe('hydration from localStorage', () => {
    it('starts empty when localStorage is empty', () => {
      const auth = useAuthStore()
      expect(auth.accessToken).toBeNull()
      expect(auth.refreshToken).toBeNull()
      expect(auth.user).toBeNull()
    })

    it('reads tokens from localStorage on init', () => {
      localStorage.setItem(TOKEN_KEY, 'token-abc')
      localStorage.setItem(REFRESH_TOKEN_KEY, 'refresh-xyz')

      const auth = useAuthStore()
      expect(auth.accessToken).toBe('token-abc')
      expect(auth.refreshToken).toBe('refresh-xyz')
    })

    it('parses user JSON from localStorage on init', () => {
      localStorage.setItem(USER_KEY, JSON.stringify({ id: 1, role: 'admin' }))

      const auth = useAuthStore()
      expect(auth.user).toEqual({ id: 1, role: 'admin' })
    })

    it('handles corrupted user JSON gracefully', () => {
      localStorage.setItem(USER_KEY, 'not-valid-json{{{')

      const auth = useAuthStore()
      expect(auth.user).toBeNull()
    })
  })

  // ---- setTokens ----

  describe('setTokens', () => {
    it('writes to store and localStorage', () => {
      const auth = useAuthStore()
      auth.setTokens('access-1', 'refresh-1')

      expect(auth.accessToken).toBe('access-1')
      expect(auth.refreshToken).toBe('refresh-1')
      expect(localStorage.getItem(TOKEN_KEY)).toBe('access-1')
      expect(localStorage.getItem(REFRESH_TOKEN_KEY)).toBe('refresh-1')
    })

    it('overwrites previous tokens', () => {
      const auth = useAuthStore()
      auth.setTokens('old-access', 'old-refresh')
      auth.setTokens('new-access', 'new-refresh')

      expect(auth.accessToken).toBe('new-access')
      expect(localStorage.getItem(TOKEN_KEY)).toBe('new-access')
    })
  })

  // ---- setTokensFromRefresh ----

  describe('setTokensFromRefresh', () => {
    it('updates store but does not touch localStorage', () => {
      localStorage.setItem(TOKEN_KEY, 'from-api-call')

      const auth = useAuthStore()
      auth.setTokensFromRefresh('new-access', 'new-refresh')

      expect(auth.accessToken).toBe('new-access')
      expect(auth.refreshToken).toBe('new-refresh')
      // localStorage не трогается этим методом
      expect(localStorage.getItem(TOKEN_KEY)).toBe('from-api-call')
    })
  })

  // ---- setUser ----

  describe('setUser', () => {
    it('writes to store and localStorage', () => {
      const auth = useAuthStore()
      auth.setUser({ id: 1, username: 'rider' })

      expect(auth.user).toEqual({ id: 1, username: 'rider' })
      expect(JSON.parse(localStorage.getItem(USER_KEY))).toEqual({
        id: 1,
        username: 'rider',
      })
    })

    it('removes user from localStorage when set to null', () => {
      localStorage.setItem(USER_KEY, JSON.stringify({ id: 1 }))

      const auth = useAuthStore()
      auth.setUser(null)

      expect(auth.user).toBeNull()
      expect(localStorage.getItem(USER_KEY)).toBeNull()
    })
  })

  // ---- logout ----

  describe('logout', () => {
    it('clears store and localStorage', () => {
      localStorage.setItem(TOKEN_KEY, 'access')
      localStorage.setItem(REFRESH_TOKEN_KEY, 'refresh')
      localStorage.setItem(USER_KEY, JSON.stringify({ id: 1 }))

      const auth = useAuthStore()
      // Убеждаемся, что store наполнен
      expect(auth.accessToken).toBe('access')

      auth.logout()

      expect(auth.accessToken).toBeNull()
      expect(auth.refreshToken).toBeNull()
      expect(auth.user).toBeNull()
      expect(localStorage.getItem(TOKEN_KEY)).toBeNull()
      expect(localStorage.getItem(REFRESH_TOKEN_KEY)).toBeNull()
      expect(localStorage.getItem(USER_KEY)).toBeNull()
    })
  })

  // ---- Getters ----

  describe('isAuthenticated', () => {
    it('is false when no access token', () => {
      const auth = useAuthStore()
      expect(auth.isAuthenticated).toBe(false)
    })

    it('is true when access token exists', () => {
      const auth = useAuthStore()
      auth.setTokens('token', 'refresh')
      expect(auth.isAuthenticated).toBe(true)
    })
  })

  describe('isAdmin', () => {
    it('is false when user is null', () => {
      const auth = useAuthStore()
      expect(auth.isAdmin).toBe(false)
    })

    it('is false for non-admin role', () => {
      const auth = useAuthStore()
      auth.setUser({ id: 1, role: 'motorcyclist' })
      expect(auth.isAdmin).toBe(false)
    })

    it('is true for admin role', () => {
      const auth = useAuthStore()
      auth.setUser({ id: 1, role: 'admin' })
      expect(auth.isAdmin).toBe(true)
    })
  })

  describe('isPremium', () => {
    it('is false when user is null', () => {
      const auth = useAuthStore()
      expect(auth.isPremium).toBe(false)
    })

    it('is false when is_premium is missing', () => {
      const auth = useAuthStore()
      auth.setUser({ id: 1, role: 'motorcyclist' })
      expect(auth.isPremium).toBe(false)
    })

    it('is true when is_premium is true', () => {
      const auth = useAuthStore()
      auth.setUser({ id: 1, is_premium: true })
      expect(auth.isPremium).toBe(true)
    })

    it('is false when is_premium is falsy', () => {
      const auth = useAuthStore()
      auth.setUser({ id: 1, is_premium: false })
      expect(auth.isPremium).toBe(false)
    })
  })
})