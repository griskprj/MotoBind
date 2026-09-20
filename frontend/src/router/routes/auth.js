/**
 * Аутентификация: вход, регистрация, восстановление пароля,
 * подтверждение email, отписка от рассылки.
 */
export default [
  {
    path: '/welcome',
    name: 'welcome screen',
    component: () => import('../../views/auth/WelcomeScreen.vue'),
    meta: {
      requiresGuest: true,
      title: 'MotoBind - Начало',
      description: 'Добро пожаловать в MotoBind — сервис для учёта обслуживания мотоциклов. Начните вести историю ТО и получайте мануалы от сообщества.',
      showFooter: false,
      showHeader: false,
    },
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../../views/auth/LoginView.vue'),
    meta: {
      requiresGuest: true,
      title: 'MotoBind - Вход',
      description: 'Войдите в свой аккаунт MotoBind, чтобы управлять мотоциклами, планировать ТО и пользоваться сервисом.',
      showFooter: false,
      showHeader: false,
    },
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../../views/auth/RegisterView.vue'),
    meta: {
      requiresGuest: true,
      title: 'MotoBind - Регистрация',
      description: 'Создайте аккаунт в MotoBind и начните вести учёт обслуживания мотоцикла. Регистрация бесплатная и занимает минуту.',
      showFooter: false,
      showHeader: false,
    },
  },
  {
    path: '/verify-email/:token',
    name: 'verify-email',
    component: () => import('../../views/auth/VerifyEmail.vue'),
    meta: {
      title: 'MotoBind - Подтверждение email',
      description: 'Подтвердите свой email, чтобы активировать аккаунт MotoBind и начать пользоваться всеми функциями сервиса.',
      showFooter: false,
      showHeader: false,
    },
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: () => import('../../views/auth/ForgotPassword.vue'),
    meta: {
      title: 'MotoBind - Восстановление пароля',
      description: 'Забыли пароль? Восстановите доступ к аккаунту MotoBind по email. Быстро и безопасно.',
      showFooter: false,
      showHeader: false,
    },
  },
  {
    path: '/reset-password/:token',
    name: 'reset-password',
    component: () => import('../../views/auth/ResetPassword.vue'),
    meta: {
      title: 'MotoBind - Сброс пароля',
      description: 'Установите новый пароль для аккаунта MotoBind. Введите новый пароль и подтвердите его.',
      showFooter: false,
      showHeader: false,
    },
  },
  {
    path: '/unsubscribe/:token',
    name: 'Unsubscribe',
    component: () => import('../../views/Unsubscribe.vue'),
    meta: {
      title: 'MotoBind - Отписка от рассылки',
      description: 'Отпишитесь от новостной рассылки MotoBind',
      showFooter: false,
      showHeader: false,
    },
  },
]
