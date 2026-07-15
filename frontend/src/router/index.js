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

function isAdmin() {
  return getUserRole() === 'admin'
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
      meta: {
        requiresGuest: true,
        title: 'MotoBind - Вход',
        showFooter: false,
        showHeader: false
      }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/auth/RegisterView.vue'),
      meta: {
        requiresGuest: true,
        title: 'MotoBind - Регистрация',
        showFooter: false,
        showHeader: false
      }
    },
    {
      path: '/home',
      name: 'home',
      component: () => import('../views/Dashboard.vue'),
      meta: {
        requiresAuth: true,
        title: 'MotoBind - Главная',
        showFooter: true,
        showHeader: true
       }
    },
    {
      path: '/garage',
      name: 'garage',
      component: () => import('../views/Garage.vue'),
      meta: {
        requiresAuth: true,
        title: 'MotoBind - Гараж',
        showFooter: true,
        showHeader: true
       }
    },
    {
      path: '/repair',
      name: 'repair',
      component: () => import('../views/Repair.vue'),
      meta: {
        requiresAuth: true,
        title: 'MotoBind - Ремонт',
        showFooter: true,
        showHeader: true
      }
    },
    {
      path: '/manual-creator',
      name: 'manual creator',
      component: () => import('../views/ManualCreator.vue'),
      meta: {
        requiresAuth: true,
        title: 'MotoBind - Конструктор мануалов',
        showFooter: true,
        showHeader: true
      }
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/AdminPanel.vue'),
      meta: {
        requiresAuth: true,
        requiresAdmin: true,
        title: 'MotoBind - Админ-панель',
        showFooter: true,
        showHeader: true
      }
    },
  ]
})

router.beforeEach((to, from, next) => {
  const authenticated = isAuthenticated()
  const admin = isAdmin()

  if (to.meta.requiresAuth && !authenticated) {
    next('/login')
    return
  }

  if (to.meta.requiresAdmin && !admin) {
    if (authenticated) {
      next('/home')
    } else {
      next('/login')
    }
    return
  }

  next()
})

export default router