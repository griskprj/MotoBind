import { defineStore } from 'pinia'
import api from '../api/api'
import { 
  getAccessToken, 
  getRefreshToken, 
  setTokens, 
  setUser, 
  getUser, 
  removeTokens,
  isAuthenticated
} from '../api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: getUser(),
    accessToken: getAccessToken(),
    refreshToken: getRefreshToken(),
    isAuthenticated: isAuthenticated(),
    isLoading: false,
    error: null
  }),

  getters: {
    isAdmin: (state) => {
      return state.user?.role === 'admin'
    },
    isMotorcyclist: (state) => {
      return state.user?.role === 'motorcyclist'
    },
    isClubMember: (state) => {
      return state.user?.role === 'club_member'
    },
    userRole: (state) => {
      return state.user?.role || null
    },
    userId: (state) => {
      return state.user?.id || null
    },
    userName: (state) => {
      return state.user?.username || 'Пользователь'
    }
  },

  actions: {
    async login(email, password) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await api.post('/auth/login', {
          email,
          password
        })
        
        const { access_token, refresh_token, user } = response.data
        
        setTokens(access_token, refresh_token)
        setUser(user)
        
        this.user = user
        this.accessToken = access_token
        this.refreshToken = refresh_token
        this.isAuthenticated = true
        
        return user
      } catch (error) {
        this.error = error.response?.data?.error || 'Ошибка входа'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async register(userData) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await api.post('/auth/register', userData)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || 'Ошибка регистрации'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async logout() {
      this.isLoading = true
      
      try {
        await api.post('/auth/logout')
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        removeTokens()
        this.user = null
        this.accessToken = null
        this.refreshToken = null
        this.isAuthenticated = false
        this.isLoading = false
        
        if (window.location.pathname !== '/login') {
          window.location.href = '/login'
        }
      }
    },

    syncAuthState() {
      const user = getUser()
      const token = getAccessToken()
      const refreshToken = getRefreshToken()
      
      this.user = user
      this.accessToken = token
      this.refreshToken = refreshToken
      this.isAuthenticated = !!token
    },

    updateUser(userData) {
      this.user = { ...this.user, ...userData }
      setUser(this.user)
    },

    clearState() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      this.isAuthenticated = false
      this.error = null
    }
  }
})