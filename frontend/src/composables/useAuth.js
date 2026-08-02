import { storeToRefs } from 'pinia'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

export function useAuth() {
  const authStore = useAuthStore()
  const router = useRouter()
  
  const { user, isAuthenticated, isAdmin, isLoading, error } = storeToRefs(authStore)
  
  const login = async (email, password) => {
    try {
      const userData = await authStore.login(email, password)
      
      if (userData.role === 'admin') {
        router.push('/admin/panel')
      } else {
        router.push('/home')
      }
      
      return userData
    } catch (error) {
      throw error
    }
  }
  
  const register = async (userData) => {
    try {
      await authStore.register(userData)
      router.push('/login?registered=true')
    } catch (error) {
      throw error
    }
  }
  
  const logout = async () => {
    await authStore.logout()
  }
  
  const checkAuth = () => {
    authStore.syncAuthState()
    return isAuthenticated.value
  }
  
  return {
    user,
    isAuthenticated,
    isAdmin,
    isLoading,
    error,
    
    login,
    register,
    logout,
    checkAuth
  }
}