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
      layout: 'public'
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
      layout: 'public'
    },
  },
  {
    path: '/garage',
    name: 'garage',
    component: () => import('../../views/garage/Garage.vue'),
    meta: {
      requiresAuth: true,
      title: 'MotoBind - Гараж мотоцикла',
      description: 'Ведите историю обслуживания всех мотоциклов, планируйте ТО, отслеживайте пробег и контролируйте расходы. Удобный гараж для вашего байка.',
      showFooter: true,
      showHeader: true,
      layout: 'default',
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
      layout: 'default',
    },
  },
  {
    path: '/maintenance',
    name: 'maintenance',
    component: () => import('../../views/maintenance/Maintenance.vue'),
    meta: {
      requiresAuth: true,
      title: 'MotoBind - Обслуживание мотоцикла',
      description: 'Добавляйте и планируйте обслуживание мотоцикла. Следите за состоянием байка, получайте напоминания о ТО и контролируйте расходы.',
      layout: 'default',
    },
  },
  {
    path: '/manuals',
    name: 'manuals',
    component: () => import('../../views/Manuals.vue'),
    meta: {
      requiresAuth: false,
      title: 'MotoBind - Мануалы по ремонту',
      description: 'База инструкций по ремонту и обслуживанию мотоциклов от сообщества. Находите мануалы для своего мотоцикла и делитесь своим опытом.',
      layout: 'public'
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
      layout: 'public'
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
      layout: 'default',
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
      layout: 'default',
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
      layout: 'default',
    },
  },
  {
    path: '/business',
    name: 'business-dashboard',
    component: () => import('../../views/business/BusinessDashboard.vue'),
    meta: {
      requiresAuth: true,
      title: 'MotoBind - Кабинет бизнеса',
      description: 'Управляйте своим бизнес-аккаунтом: мастер или СТО.',
      layout: 'default',
    },
  },
  {
    path: '/business/clients',
    name: 'business-clients',
    component: () => import('../../views/business/BusinessClients.vue'),
    meta: {
      requiresAuth: true,
      title: 'MotoBind - Мои клиенты',
      description: 'Список клиентов вашего бизнес-аккаунта.',
      layout: 'default',
    },
  },
  {
    path: '/business/clients/:id',
    name: 'business-client-detail',
    component: () => import('../../views/business/BusinessClientDetail.vue'),
    meta: {
      requiresAuth: true,
      title: 'MotoBind - Карточка клиента',
      description: 'Информация о клиенте и его мотоциклах.',
      layout: 'default',
    },
  },
  {
    path: '/business/services',
    name: 'business-services',
    component: () => import('../../views/business/BusinessServices.vue'),
    meta: {
      requiresAuth: true,
      title: 'MotoBind - Мои услуги',
      description: 'Управляйте каталогом услуг.',
      layout: 'default',
    },
  },
  {
    path: '/business/:slug',
    name: 'business-public',
    component: () => import('../../views/business/BusinessPublicPage.vue'),
    meta: {
      requiresAuth: false,
      title: 'MotoBind - Мастер',
      description: 'Публичная страница мастера или СТО.',
      layout: 'default'
    },
  },
  {
    path: '/bookings',
    name: 'bookings',
    component: () => import('../../views/Bookings.vue'),
    meta: {
      requiresAuth: true,
      title: 'MotoBind - Мои заявки',
      description: 'Записи к мастерам и станциям.',
      layout: 'default',
    },
  },
  {
    path: '/business/bookings',
    name: 'business-bookings',
    component: () => import('../../views/business/BusinessBookings.vue'),
    meta: {
      requiresAuth: true,
      title: 'MotoBind - Заявки',
      description: 'Управление заявками.',
      layout: 'default',
    },
  },
  {
    path: '/masters',
    name: 'masters',
    component: () => import('../../views/Masters.vue'),
    meta: {
      requiresAuth: true,
      title: 'MotoBind - Мастера и СТО',
      description: 'Каталог мастеров и станций. Найдите специалиста для обслуживания мотоцикла.',
      layout: 'default'
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
      layout: 'default',
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
      layout: 'default',
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
      layout: 'default',
    },
  },
]
