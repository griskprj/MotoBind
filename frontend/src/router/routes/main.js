/**
 * Основные страницы приложения.
 */
import { useAuthStore } from '../../stores/auth'

export default [
  {
    path: '/',
    redirect: () => {
      const auth = useAuthStore()
      return auth.isAuthenticated ? '/garage' : '/landing'
    },
  },
  {
    path: '/contacts',
    name: 'contacts',
    component: () => import('../../views/Contacts.vue'),
    meta: {
      requiresAuth: false,
      title: 'MotoBind - Контакты',
      description: 'Свяжитесь с нами через Telegram или Email',
      showFooter: true,
      showHeader: true,
    },
  },
  {
    path: '/landing',
    name: 'landing',
    component: () => import('../../views/Landing.vue'),
    meta: {
      requiresAuth: false,
      title: 'MotoBind - Учёт обслуживания мотоциклов',
      description: 'Сервис для мотоциклистов: планируйте ТО, ведите историю обслуживания, считайте расходы и получайте мануалы от сообщества. Бесплатно.',
      showFooter: true,
      showHeader: false,
    },
  },
  {
    path: '/garage',
    name: 'garage',
    component: () => import('../../views/Garage.vue'),
    meta: {
      requiresAuth: true,
      title: 'MotoBind - Гараж мотоцикла',
      description: 'Ведите историю обслуживания всех мотоциклов, планируйте ТО, отслеживайте пробег и контролируйте расходы. Удобный гараж для вашего байка.',
      showFooter: true,
      showHeader: true,
    },
  },
  {
    path: '/repair',
    name: 'repair',
    component: () => import('../../views/Repair.vue'),
    meta: {
      requiresAuth: true,
      title: 'MotoBind - Ремонт мотоциклов',
      description: 'Пошаговые инструкции по ремонту мотоциклов. Выбирайте обслуживание и получайте подробные мануалы от сообщества.',
      showFooter: true,
      showHeader: true,
    },
  },
  {
    path: '/maintenance',
    name: 'maintenance',
    component: () => import('../../views/Maintenance.vue'),
    meta: {
      requiresAuth: true,
      title: 'MotoBind - Обслуживание мотоцикла',
      description: 'Добавляйте и планируйте обслуживание мотоцикла. Следите за состоянием байка, получайте напоминания о ТО и контролируйте расходы.',
      showFooter: true,
      showHeader: true,
    },
  },
  {
    path: '/manuals',
    name: 'manuals',
    component: () => import('../../views/Manuals.vue'),
    meta: {
      requiresAuth: true,
      title: 'MotoBind - Мануалы по ремонту',
      description: 'База инструкций по ремонту и обслуживанию мотоциклов от сообщества. Находите мануалы для своего мотоцикла и делитесь своим опытом.',
      showFooter: true,
      showHeader: true,
    },
  },
  {
    path: '/manual/:id',
    name: 'ManualView',
    component: () => import('../../views/ManualView.vue'),
    meta: {
      requiresAuth: false,
      title: 'MotoBind - Мануал по ремонту мотоцикла',
      description: 'Подробная страница с инструкцией по ремонту мотоцикла',
      showFooter: true,
      showHeader: true,
    },
  },
  {
    path: '/manual-creator',
    name: 'manual creator',
    component: () => import('../../views/ManualCreator.vue'),
    meta: {
      requiresAuth: true,
      title: 'MotoBind - Конструктор мануалов',
      description: 'Создавайте пошаговые мануалы по ремонту и обслуживанию мотоциклов. Делитесь своим опытом с сообществом.',
      showFooter: true,
      showHeader: true,
    },
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('../../views/Profile.vue'),
    meta: {
      requiresAuth: true,
      title: 'MotoBind - Профиль пользователя',
      description: 'Управляйте личными данными, настройками аккаунта и безопасностью. Меняйте аватар и пароль в один клик.',
      showFooter: true,
      showHeader: true,
    },
  },
  {
    path: '/profile/:id',
    name: 'public-profile',
    component: () => import('../../views/PublicProfile.vue'),
    meta: {
      requiresAuth: true,
      title: 'MotoBind - Профиль пользователя',
      description: 'Публичный профиль пользователя MotoBind',
      showFooter: true,
      showHeader: true,
    },
  },
  {
    path: '/notifications',
    name: 'notifications',
    component: () => import('../../views/Notifications.vue'),
    meta: {
      requiresAuth: true,
      title: 'MotoBind - Уведомления',
      description: 'Все ваши уведомления',
      showFooter: true,
      showHeader: true,
    },
  },
  {
    path: '/social',
    name: 'social',
    component: () => import('../../views/Social.vue'),
    meta: {
      requiresAuth: true,
      title: 'MotoBind - MotoSocial',
      description: 'Социальная сеть для мотоциклистов. Делитесь опытом, общайтесь и вдохновляйтесь',
      showFooter: true,
      showHeader: true,
    },
  },
  {
    path: '/social/post/:id',
    name: 'post-view',
    component: () => import('../../views/PostView.vue'),
    meta: {
      requiresAuth: true,
      title: 'MotoBind - Просмотр поста',
      description: 'Просмотр поста в социальной сети MotoSocial',
      showFooter: true,
      showHeader: true,
    },
  },
]