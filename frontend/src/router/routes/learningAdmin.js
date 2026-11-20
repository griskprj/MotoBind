export default [
  {
    path: '/admin/learning',
    component: () => import('@/views/admin/learning/AdminLearningLayout.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      title: 'MotoBind - Админка обучения',
      layout: 'default',
    },
    children: [
      {
        path: '',
        name: 'admin-learning',
        redirect: { name: 'admin-learning-courses' },
      },
      {
        path: 'courses',
        name: 'admin-learning-courses',
        component: () =>
          import('@/views/admin/learning/AdminCoursesListPage.vue'),
        meta: { title: 'MotoBind - Курсы (админ)' },
      },
      {
        path: 'courses/new',
        name: 'admin-learning-course-new',
        component: () =>
          import('@/views/admin/learning/AdminCourseEditorPage.vue'),
        meta: { title: 'MotoBind - Новый курс' },
      },
      {
        path: 'courses/:id',
        name: 'admin-learning-course',
        component: () =>
          import('@/views/admin/learning/AdminCourseEditorPage.vue'),
        props: true,
        meta: { title: 'MotoBind - Редактор курса' },
      },
      {
        path: 'articles',
        name: 'admin-learning-articles',
        component: () =>
          import('@/views/admin/learning/AdminArticlesListPage.vue'),
        meta: { title: 'MotoBind - Статьи (админ)' },
      },
      {
        path: 'articles/new',
        name: 'admin-learning-article-new',
        component: () =>
          import('@/views/admin/learning/AdminArticleEditorPage.vue'),
        meta: { title: 'MotoBind - Новая статья' },
      },
      {
        path: 'articles/:id',
        name: 'admin-learning-article',
        component: () =>
          import('@/views/admin/learning/AdminArticleEditorPage.vue'),
        props: true,
        meta: { title: 'MotoBind - Редактор статьи' },
      },
    ],
  },
]
