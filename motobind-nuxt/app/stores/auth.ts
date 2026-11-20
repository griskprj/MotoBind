import { defineStore } from 'pinia'
import type { LoginPayload, User } from '~/types'

type AuthStatus = 'idle' | 'loading' | 'authenticated' | 'guest'

export const useAuthStore = defineStore('auth', () => {
  const api = useApi()

  const user = ref<User | null>(null)
  const status = ref<AuthStatus>('idle')

  let fetchPromise: Promise<User | null> | null = null

  const isAuthenticated = computed(() => status.value === 'authenticated' && !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isBusiness = computed(() => !!user.value?.has_business_account)

  async function fetchUser(force = false): Promise<User | null> {
    if (!force && status.value === 'authenticated') return user.value
    if (!force && status.value === 'guest') return null

    if (fetchPromise) return fetchPromise

    status.value = 'loading'

    fetchPromise = (async () => {
      try {
        const me = await api.auth.me()
        user.value = me
        status.value = 'authenticated'
        return me
      } catch (e) {
        user.value = null
        status.value = 'guest'
        return null
      } finally {
        fetchPromise = null
      }
    })()

    return fetchPromise
  }

  async function login(payload: LoginPayload): Promise<User> {
    status.value = 'loading'
    try {
      const res = await api.auth.login(payload)
      user.value = res.user
      status.value = 'authenticated'
      return res.user
    } catch (e) {
      user.value = null
      status.value = 'guest'
      throw e
    }
  }

  async function register(payload: RegisterPayload): Promise<User> {
    status.value = 'loading'
    try {
      const res = await api.auth.register(payload)
      user.value = res.user
      status.value = 'authenticated'
      return res.user
    } catch (e) {
      user.value = null
      status.value = 'guest'
      throw e
    }
  }

  async function logout() {
    try {
      await api.auth.logout()
    } catch {
      // ignore
    } finally {
      user.value = null
      status.value = 'guest'
    }
  }

  return {
    user,
    status,
    isAuthenticated,
    isAdmin,
    isBusiness,
    fetchUser,
    login,
    register,
    logout,
  }
})
