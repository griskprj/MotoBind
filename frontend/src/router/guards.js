import { useAuthStore } from '../stores/auth'

/**
 * Navigation guard: проверяет meta.requiresAuth / requiresAdmin / requiresGuest
 * и редиректит неавторизованных / не-админов / уже-авторизованных.
 */
export function setupAuthGuards(router) {
  router.beforeEach((to, from, next) => {
    const auth = useAuthStore()

    if (to.meta.requiresAuth && !auth.isAuthenticated) {
      next('/welcome')
      return
    }

    if (to.meta.requiresAdmin && !auth.isAdmin) {
      if (auth.isAuthenticated) {
        next('/garage')
      } else {
        next('/welcome')
      }
      return
    }

    if (to.meta.requiresGuest && auth.isAuthenticated) {
      next('/garage')
      return
    }

    next()
  })
}

/**
 * Мета-обновления после навигации: title, description, robots, canonical, og-теги.
 */
export function setupMetaUpdates(router) {
  router.afterEach((to) => {
    document.title = to.meta?.title || 'MotoBind'

    const description = to.meta?.description
    if (description) {
      let meta = document.querySelector('meta[name="description"]')
      if (!meta) {
        meta = document.createElement('meta')
        meta.setAttribute('name', 'description')
        document.head.appendChild(meta)
      }
      meta.setAttribute('content', description)
    }

    const isPrivate = to.meta?.requiresAdmin || to.meta?.requiresGuest
    let robots = document.querySelector('meta[name="robots"]')
    if (!robots) {
      robots = document.createElement('meta')
      robots.setAttribute('name', 'robots')
      document.head.appendChild(robots)
    }
    robots.setAttribute('content', isPrivate ? 'noindex, nofollow' : 'index, follow')

    let canonical = document.querySelector('link[rel="canonical"]')
    if (!canonical) {
      canonical = document.createElement('link')
      canonical.setAttribute('rel', 'canonical')
      document.head.appendChild(canonical)
    }
    canonical.setAttribute('href', window.location.origin + to.path)

    const setOG = (property, content) => {
      if (!content) return
      let tag = document.querySelector(`meta[property="${property}"]`)
      if (!tag) {
        tag = document.createElement('meta')
        tag.setAttribute('property', property)
        document.head.appendChild(tag)
      }
      tag.setAttribute('content', content)
    }
    setOG('og:title', to.meta?.title || 'MotoBind')
    setOG('og:description', to.meta?.description || '')
    setOG('og:url', window.location.href)
    setOG('og:type', 'website')
  })
}