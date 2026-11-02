export default defineNuxtRouteMiddleware((to) => {
  const auth = useAuthStore()

  if (auth.status === 'idle') {
  }

  if (!auth.isAuthenticated) {
    return navigateTo({
      path: '/login',
      query: { redirect: to.fullPath },
    })
  }
})
