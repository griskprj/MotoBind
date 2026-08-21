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
      redirect: () => {
        if (isAuthenticated()) {
          return '/garage'
        }
        return '/landing'
      }
    },
    {
      path: '/welcome',
      name: 'welcome screen',
      component: () => import('../views/auth/WelcomeScreen.vue'),
      meta: {
        requiresGuest: true,
        title: 'MotoBind - Начало',
        showFooter: false,
        showHeader: false
      }
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
      path: '/verify-email/:token',
      name: 'verify-email',
      component: () => import('../views/auth/VerifyEmail.vue'),
      meta: {
        title: 'MotoBind - Подтверждение email',
        showFooter: false,
        showHeader: false
      }
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: () => import('../views/auth/ForgotPassword.vue'),
      meta: {
        title: 'MotoBind - Восстановление пароля',
        showFooter: false,
        showHeader: false
      }
    },
    {
      path: '/reset-password/:token',
      name: 'reset-password',
      component: () => import('../views/auth/ResetPassword.vue'),
      meta: {
        title: 'MotoBind - Сброс пароля',
        showFooter: false,
        showHeader: false
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
      path: '/maintenance',
      name: 'maintenance',
      component: () => import('../views/Maintenance.vue'),
      meta: {
        requiresAuth: true,
        title: 'MotoBind - Обслуживание',
        showFooter: true,
        showHeader: true
      }
    },
    {
      path: '/manuals',
      name: 'manuals',
      component: () => import('../views/Manuals.vue'),
      meta: {
        requiresAuth: true,
        title: 'MotoBind - Мануалы',
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
      path: '/manual/rules',
      name: 'manual rules',
      component: () => import('../views/documents/ManualRules.vue'),
      meta: {
        requiresAuth: true,
        title: 'MotoBind - Правила оформления мануалов',
        showFooter: true,
        showHeader: true
      }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/Profile.vue'),
      meta: {
        requiresAuth: true,
        title: 'MotoBind - Профиль пользователя',
        showFooter: true,
        showHeader: true
      }
    },
    {
      path: '/admin/panel',
      name: 'admin panel',
      component: () => import('../views/admin/AdminPanel.vue'),
      meta: {
        requiresAuth: true,
        requiresAdmin: true,
        title: 'MotoBind - Админ-панель',
        showFooter: true,
        showHeader: true
      }
    },
    {
      path: '/admin/users',
      name: 'users',
      component: () => import('../views/admin/UsersPanel.vue'),
      meta: {
        requiresAuth: true,
        requiresAdmin: true,
        title: 'MotoBind - Пользователи',
        showFooter: true,
        showHeader: true
      }
    },
    {
      path: '/admin/manuals',
      name: 'admin manuals',
      component: () => import('../views/admin/ManualsPanel.vue'),
      meta: {
        requiresAuth: true,
        requiresAdmin: true,
        title: 'MotoBind - Мануалы',
        showFooter: true,
        showHeader: true
      }
    },

    {
      path: '/landing',
      name: 'landing',
      component: () => import('../views/Landing.vue'),
      meta: {
        requiresAuth: false,
        title: 'MotoBind',
        showFooter: true,
        showHeader: false
      }
    },

    {
      path: '/privacy',
      name: 'privacy',
      component: () => import('../views/documents/PrivacyPolicy.vue'),
      meta: {
        requiresAuth: false,
        title: 'MotoBind - Политика конфиденциальности',
        showFooter: true,
        showHeader: false
      }
    },
    {
      path: '/terms',
      name: 'terms',
      component: () => import('../views/documents/TermsOfService.vue'),
      meta: {
        requiresAuth: false,
        title: 'MotoBind - Пользовательское соглашение',
        showFooter: true,
        showHeader: false
      }
    },
    {
      path: '/consent',
      name: 'consent',
      component: () => import('../views/documents/Consent.vue'),
      meta: {
        requiresAuth: false,
        title: 'MotoBind - Согласие на обработку персональных данных',
        showFooter: true,
        showHeader: false
      }
    },
    {
      path: '/rules',
      name: 'rules',
      component: () => import('../views/documents/Rules.vue'),
      meta: {
        requiresAuth: false,
        title: 'MotoBind - Правила использования',
        showFooter: true,
        showHeader: false
      }
    },
  ]
})

router.beforeEach((to, from, next) => {
  const authenticated = isAuthenticated()
  const admin = isAdmin()

  if (to.meta.requiresAuth && !authenticated) {
    next('/welcome')
    return
  }

  if (to.meta.requiresAdmin && !admin) {
    if (authenticated) {
      next('/garage')
    } else {
      next('/welcome')
    }
    return
  }

  next()
})

export default router
