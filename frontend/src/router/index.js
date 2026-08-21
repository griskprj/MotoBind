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
    // ===== ГЛАВНАЯ =====
    {
      path: '/',
      redirect: () => {
        if (isAuthenticated()) {
          return '/garage'
        }
        return '/landing'
      }
    },

    // ===== АУТЕНТИФИКАЦИЯ =====
    {
      path: '/welcome',
      name: 'welcome screen',
      component: () => import('../views/auth/WelcomeScreen.vue'),
      meta: {
        requiresGuest: true,
        title: 'MotoBind - Начало',
        description: 'Добро пожаловать в MotoBind — сервис для учёта обслуживания мотоциклов. Начните вести историю ТО и получайте мануалы от сообщества.',
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
        description: 'Войдите в свой аккаунт MotoBind, чтобы управлять мотоциклами, планировать ТО и пользоваться сервисом.',
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
        description: 'Создайте аккаунт в MotoBind и начните вести учёт обслуживания мотоцикла. Регистрация бесплатная и занимает минуту.',
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
        description: 'Подтвердите свой email, чтобы активировать аккаунт MotoBind и начать пользоваться всеми функциями сервиса.',
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
        description: 'Забыли пароль? Восстановите доступ к аккаунту MotoBind по email. Быстро и безопасно.',
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
        description: 'Установите новый пароль для аккаунта MotoBind. Введите новый пароль и подтвердите его.',
        showFooter: false,
        showHeader: false
      }
    },

    // ===== ОСНОВНЫЕ СТРАНИЦЫ =====
    {
      path: '/landing',
      name: 'landing',
      component: () => import('../views/Landing.vue'),
      meta: {
        requiresAuth: false,
        title: 'MotoBind - Учёт обслуживания мотоциклов',
        description: 'Сервис для мотоциклистов: планируйте ТО, ведите историю обслуживания, считайте расходы и получайте мануалы от сообщества. Бесплатно.',
        showFooter: true,
        showHeader: false
      }
    },
    {
      path: '/garage',
      name: 'garage',
      component: () => import('../views/Garage.vue'),
      meta: {
        requiresAuth: true,
        title: 'MotoBind - Гараж мотоцикла',
        description: 'Ведите историю обслуживания всех мотоциклов, планируйте ТО, отслеживайте пробег и контролируйте расходы. Удобный гараж для вашего байка.',
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
        title: 'MotoBind - Ремонт мотоциклов',
        description: 'Пошаговые инструкции по ремонту мотоциклов. Выбирайте обслуживание и получайте подробные мануалы от сообщества.',
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
        title: 'MotoBind - Обслуживание мотоцикла',
        description: 'Добавляйте и планируйте обслуживание мотоцикла. Следите за состоянием байка, получайте напоминания о ТО и контролируйте расходы.',
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
        title: 'MotoBind - Мануалы по ремонту',
        description: 'База инструкций по ремонту и обслуживанию мотоциклов от сообщества. Находите мануалы для своего мотоцикла и делитесь своим опытом.',
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
        description: 'Создавайте пошаговые мануалы по ремонту и обслуживанию мотоциклов. Делитесь своим опытом с сообществом.',
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
        description: 'Управляйте личными данными, настройками аккаунта и безопасностью. Меняйте аватар и пароль в один клик.',
        showFooter: true,
        showHeader: true
      }
    },

    // ===== ДОКУМЕНТЫ =====
    {
      path: '/manual/rules',
      name: 'manual rules',
      component: () => import('../views/documents/ManualRules.vue'),
      meta: {
        requiresAuth: true,
        title: 'MotoBind - Правила оформления мануалов',
        description: 'Правила оформления мануалов в MotoBind. Узнайте, как создавать качественные инструкции по ремонту и обслуживанию мотоциклов.',
        showFooter: true,
        showHeader: true
      }
    },
    {
      path: '/privacy',
      name: 'privacy',
      component: () => import('../views/documents/PrivacyPolicy.vue'),
      meta: {
        requiresAuth: false,
        title: 'MotoBind - Политика конфиденциальности',
        description: 'Политика конфиденциальности MotoBind. Узнайте, как мы собираем, используем и защищаем ваши персональные данные.',
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
        description: 'Пользовательское соглашение MotoBind. Условия использования сервиса, права и обязанности сторон.',
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
        title: 'MotoBind - Согласие на обработку данных',
        description: 'Согласие на обработку персональных данных в MotoBind. Подробная информация о защите и использовании ваших данных.',
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
        description: 'Правила использования сервиса MotoBind. Ознакомьтесь с условиями перед началом работы.',
        showFooter: true,
        showHeader: false
      }
    },

    // ===== АДМИН-ПАНЕЛЬ =====
    {
      path: '/admin/panel',
      name: 'admin panel',
      component: () => import('../views/admin/AdminPanel.vue'),
      meta: {
        requiresAuth: true,
        requiresAdmin: true,
        title: 'MotoBind - Админ-панель',
        description: 'Административная панель MotoBind. Управление пользователями, мануалами и контентом.',
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
        title: 'MotoBind - Управление пользователями',
        description: 'Управление пользователями MotoBind. Просмотр, блокировка, редактирование и удаление пользователей.',
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
        title: 'MotoBind - Управление мануалами',
        description: 'Модерация и управление мануалами MotoBind. Просмотр, одобрение, отклонение и удаление инструкций.',
        showFooter: true,
        showHeader: true
      }
    },
  ]
})

// ===== НАВИГАЦИОННЫЙ ХУК =====
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

  if (to.meta.requiresGuest && authenticated) {
    next('/garage')
    return
  }

  next()
})

export default router