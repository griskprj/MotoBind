export default defineNuxtRouteMiddleware(async (to) => {
  const auth = useAuthStore()

  if (auth.status === 'idle') {
    await auth.fetchUser()
  }

  if (!auth.isAuthenticated) {
    return navigateTo({
      path: '/login',
      query: { redirect: to.fullPath },
    })
  }
})
