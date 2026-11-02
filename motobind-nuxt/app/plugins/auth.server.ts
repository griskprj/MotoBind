export default defineNuxtPlugin((nuxtApp) => {
  console.log('🔌 [auth.server] plugin loaded!')

  if (import.meta.server) {
    console.log('🔍 [auth.server] fetching user on server...')
    const auth = useAuthStore()
    if (auth.status === 'idle') {
      return auth.fetchUser()
    }
  }
})
