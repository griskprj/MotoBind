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
      layout: 'auth',
      title: 'MotoBind - Начало',
      description: 'Добро пожаловать в MotoBind — сервис для учёта обслуживания мотоциклов. Начните вести историю ТО и получайте мануалы от сообщества.',
    },
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../../views/auth/LoginView.vue'),
    meta: {
      requiresGuest: true,
      layout: 'auth',
      title: 'MotoBind - Вход',
      description: 'Войдите в свой аккаунт MotoBind, чтобы управлять мотоциклами, планировать ТО и пользоваться сервисом.',
    },
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../../views/auth/RegisterView.vue'),
    meta: {
      requiresGuest: true,
      layout: 'auth',
      title: 'MotoBind - Регистрация',
      description: 'Создайте аккаунт в MotoBind и начните вести учёт обслуживания мотоцикла. Регистрация бесплатная и занимает минуту.',
    },
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: () => import('../../views/auth/ForgotPassword.vue'),
    meta: {
      requiresGuest: true,
      layout: 'auth',
      title: 'MotoBind - Восстановление пароля',
      description: 'Забыли пароль? Восстановите доступ к аккаунту MotoBind по email. Быстро и безопасно.',
    },
  },
  {
    path: '/reset-password/:token',
    name: 'reset-password',
    component: () => import('../../views/auth/ResetPassword.vue'),
    meta: {
      requiresGuest: true,
      layout: 'auth',
      title: 'MotoBind - Сброс пароля',
      description: 'Установите новый пароль для аккаунта MotoBind. Введите новый пароль и подтвердите его.',
    },
  },
  {
    path: '/unsubscribe/:token',
    name: 'Unsubscribe',
    component: () => import('../../views/Unsubscribe.vue'),
    meta: {
      layout: 'auth',
      title: 'MotoBind - Отписка от рассылки',
      description: 'Отпишитесь от новостной рассылки MotoBind',
    },
  },
]
