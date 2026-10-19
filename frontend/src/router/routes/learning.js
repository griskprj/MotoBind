export default [
  {
    path: '/learning',
    component: () => import('@/views/learning/LearningPage.vue'),
    meta: {
      requiresAuth: false,
      title: 'MotoBind - Обучение',
      description: 'Курсы, статьи и полезные материалы для мотоциклистов. Учитесь вождению, ремонту, первой помощи.',
      layout: 'default',
    },
    children: [
      {
        path: '',
        name: 'learning',
        redirect: { name: 'learning-courses' },
      },
      {
        path: 'courses',
        name: 'learning-courses',
        component: () => import('@/views/learning/CoursesListPage.vue'),
        meta: { title: 'MotoBind - Курсы' },
      },
      {
        path: 'courses/:slug',
        name: 'learning-course',
        component: () => import('@/views/learning/CourseDetailPage.vue'),
        props: true,
        meta: { title: 'MotoBind - Курс' },
      },
      {
        path: 'courses/:slug/:lessonSlug',
        name: 'learning-lesson',
        component: () => import('@/views/learning/LessonPage.vue'),
        props: true,
        meta: { hideParentTabs: true, title: 'MotoBind - Урок' },
      },
      {
        path: 'articles',
        name: 'learning-articles',
        component: () => import('@/views/learning/ArticlesListPage.vue'),
        meta: { title: 'MotoBind - Статьи' },
      },
      {
        path: 'articles/:slug',
        name: 'learning-article',
        component: () => import('@/views/learning/ArticlePage.vue'),
        props: true,
        meta: { hideParentTabs: true, title: 'MotoBind - Статья' },
      },
      {
        path: 'my',
        name: 'learning-my',
        component: () => import('@/views/learning/MyLearningPage.vue'),
        meta: { requiresAuth: true, title: 'MotoBind - Моё обучение' },
      },
    ],
  },
]
