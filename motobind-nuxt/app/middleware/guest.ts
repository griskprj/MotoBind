export default defineNuxtRouteMiddleware(async () => {
  const auth = useAuthStore()

  if (auth.status === 'idle') {
    await auth.fetchUser()
  }

  if (auth.isAuthenticated) {
    return navigateTo('/garage')
  }
})
