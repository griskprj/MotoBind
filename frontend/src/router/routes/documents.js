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
      showFooter: true,
      showHeader: true,
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
      showFooter: true,
      showHeader: false,
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
      showFooter: true,
      showHeader: false,
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
      showFooter: true,
      showHeader: false,
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
      showFooter: true,
      showHeader: false,
    },
  },
]
