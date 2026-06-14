import { createRouter, createWebHistory } from 'vue-router'
import { isAuthenticated } from '../api/auth'

function getUserRole() {
  const token = localStorage.getItem('access_token')
  if (!token) return null

  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.role
  } catch {
    return null
  }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/auth/LoginView.vue'),
      meta: { requiresGuest: true, title: 'MotoBind - Вход' }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/auth/RegisterView.vue'),
      meta: { requiresGuest: true, title: 'MotoBind - Регистрация' }
    },
    {
      path: '/home',
      name: 'home',
      component: () => import('../views/Dashboard.vue'),
      meta: { requiresAuth: true, title: 'MotoBind - Главная' }
    },
    {
      path: '/garage',
      name: 'garage',
      meta: { requiresAuth: true, title: 'MotoBind - Гараж' }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authenticated = isAuthenticated()

  if (to.meta.requiresAuth && !authenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router