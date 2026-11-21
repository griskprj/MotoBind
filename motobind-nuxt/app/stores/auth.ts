import { defineStore } from 'pinia'
import type { LoginPayload, User } from '~/types'

type AuthStatus = 'idle' | 'loading' | 'authenticated' | 'guest'

export const useAuthStore = defineStore('auth', () => {
  const api = useApi()

  const user = useState<User | null>('auth:user', () => null)
  const status = useState<AuthStatus>('auth:status', () => 'idle')
  const pending = useState<Promise<User | null> | null>('auth:pending', () => null)

  const isAuthenticated = computed(() => status.value === 'authenticated' && !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isBusiness = computed(() => !!user.value?.has_business_account)

  async function fetchUser(force = false): Promise<User | null> {
    if (!force && status.value === 'authenticated') return user.value
    if (!force && status.value === 'guest') return null
    if (pending.value) return pending.value

    status.value = 'loading'

    let resolve!: (v: User | null) => void
    const p = new Promise<User | null>((r) => { resolve = r })
    pending.value = p

    ;(async () => {
      try {
        const me = await api.auth.me()
        user.value = me
        status.value = 'authenticated'
        resolve(me)
      } catch (e: any) {
        if (e?.status === 429) {
          status.value = user.value ? 'authenticated' : 'idle'
          resolve(user.value)
        } else {
          user.value = null
          status.value = 'guest'
          resolve(null)
        }
      } finally {
        pending.value = null
      }
    })()

    return p
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
