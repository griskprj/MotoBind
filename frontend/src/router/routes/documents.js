/**
 * Юридические документы и правила сервиса.
 */
export default [
  {
    path: '/manual/rules',
    name: 'manual rules',
    component: () => import('../../views/documents/ManualRules.vue'),
    meta: {
      requiresAuth: true,
      title: 'MotoBind - Правила оформления мануалов',
      description: 'Правила оформления мануалов в MotoBind. Узнайте, как создавать качественные инструкции по ремонту и обслуживанию мотоциклов.',
      layout: 'default',
    },
  },
  {
    path: '/privacy',
    name: 'privacy',
    component: () => import('../../views/documents/PrivacyPolicy.vue'),
    meta: {
      requiresAuth: false,
      title: 'MotoBind - Политика конфиденциальности',
      description: 'Политика конфиденциальности MotoBind. Узнайте, как мы собираем, используем и защищаем ваши персональные данные.',
      layout: 'public',
    },
  },
  {
    path: '/terms',
    name: 'terms',
    component: () => import('../../views/documents/TermsOfService.vue'),
    meta: {
      requiresAuth: false,
      title: 'MotoBind - Пользовательское соглашение',
      description: 'Пользовательское соглашение MotoBind. Условия использования сервиса, права и обязанности сторон.',
      layout: 'public',
    },
  },
  {
    path: '/consent',
    name: 'consent',
    component: () => import('../../views/documents/Consent.vue'),
    meta: {
      requiresAuth: false,
      title: 'MotoBind - Согласие на обработку данных',
      description: 'Согласие на обработку персональных данных в MotoBind. Подробная информация о защите и использовании ваших данных.',
      layout: 'public',
    },
  },
  {
    path: '/rules',
    name: 'rules',
    component: () => import('../../views/documents/Rules.vue'),
    meta: {
      requiresAuth: false,
      title: 'MotoBind - Правила использования',
      description: 'Правила использования сервиса MotoBind. Ознакомьтесь с условиями перед началом работы.',
      layout: 'public',
    },
  },
]
