/**
 * Админ-панель: управление пользователями, мотоциклами, мануалами, репортами.
 */
export default [
  {
    path: '/admin/panel',
    name: 'admin panel',
    component: () => import('../../views/admin/AdminPanel.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      title: 'MotoBind - Админ-панель',
      description: 'Административная панель MotoBind. Управление пользователями, мануалами и контентом.',
      showFooter: true,
      showHeader: true,
    },
  },
  {
    path: '/admin/users',
    name: 'users',
    component: () => import('../../views/admin/UsersPanel.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      title: 'MotoBind - Управление пользователями',
      description: 'Управление пользователями MotoBind. Просмотр, блокировка, редактирование и удаление пользователей.',
      showFooter: true,
      showHeader: true,
    },
  },
  {
    path: '/admin/manuals',
    name: 'admin manuals',
    component: () => import('../../views/admin/ManualsPanel.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      title: 'MotoBind - Управление мануалами',
      description: 'Модерация и управление мануалами MotoBind. Просмотр, одобрение, отклонение и удаление инструкций.',
      showFooter: true,
      showHeader: true,
    },
  },
  {
    path: '/admin/motorcycles',
    name: 'AdminMotorcycles',
    component: () => import('../../views/admin/AdminMotorcyclesPanel.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      title: 'MotoBind - Управление мотоциклами',
      description: 'Управление мотоциклами MotoBind. Просмотр и удаление мотоциклов пользователей',
      showFooter: true,
      showHeader: true,
    },
  },
  {
    path: '/admin/reports',
    name: 'AdminReports',
    component: () => import('../../views/admin/AdminReportsPanel.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      title: 'MotoBind - Управление репортами',
      description: 'Модерация жалоб на посты. Просмотр, рассмотрение и принятие решений по репортам пользователей.',
      showFooter: true,
      showHeader: true,
    },
  },
]