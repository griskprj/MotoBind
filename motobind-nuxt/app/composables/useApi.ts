import type {
  ApplyTemplatePayload,
  CreateMaintenancePayload,
  CreateComponentPayload,
  CreateMaintenanceEventPayload,
  CompleteMaintenancePayload,
  CompleteMaintenanceResponse,
  UpdateMaintenancePayload,
  UpdateMaintenanceEventPayload,
  UpdateComponentPayload,
  Maintenance,
  MaintenanceEvent,
  MaintenanceEventsListResponse,
  Motorcycle,
  MotorcycleShort,
  MotorcycleHealth,
  MotorcycleComponent,
  ComponentListResponse,
  ApplyTemplateResponse,
  ComponentHistoryResponse,
  CreateMotorcyclePayload,
  UpdateMotorcyclePayload,
  LoginPayload,
  LoginResponse,
  RegisterPayload,
  User,
  Manual,
  ManualsListResponse,
  CreateManualPayload,
  UpdateManualPayload
} from '~/types'

import { baseFetch, request } from '~/utils/api'

/**
 * Типизированный клиент API.
 * Использование:
 *   const api = useApi()
 *   const motos = await api.motorcycle.list()
 *   await api.motorcycle.update(1, { name: '...' })
 */
export function useApi() {
  // ---------- AUTH ----------
  const auth = {
    login: (payload: LoginPayload) =>
      request(() =>
        $fetch<LoginResponse>('/api/auth/login', {
          method: 'POST',
          body: payload,
        }),
      ),
    register: (payload: RegisterPayload) =>
      request(() =>
        $fetch<LoginResponse>('/api/auth/register', {
          method: 'POST',
          body: payload,
        }),
      ),
    me: () => request(() => baseFetch<User>('/auth/me')),
    logout: () => request(() => baseFetch<{ message: string }>('/auth/logout', { method: 'POST' })),
  }

  // ---------- MOTORCYCLE ----------
  const motorcycle = {
    /** GET /motorcycle/ — отдаёт Detail[] (с maintenances) */
    list: () => request(() => baseFetch<Motorcycle[]>('/motorcycle/')),

    /** GET /motorcycle/<id> */
    get: (id: number | string) =>
      request(() => baseFetch<Motorcycle>(`/motorcycle/${id}`)),

    /** GET /motorcycle/<id>/health — сводка состояния компонентов */
    health: (id: number | string) =>
      request(() => baseFetch<MotorcycleHealth>(`/motorcycle/${id}/health`)),

    /** POST /motorcycle/ */
    create: (payload: CreateMotorcyclePayload) =>
      request(() =>
        baseFetch<Motorcycle>('/motorcycle/', {
          method: 'POST',
          body: payload,
        }),
      ),

    /** PUT /motorcycle/<id> */
    update: (id: number | string, payload: UpdateMotorcyclePayload) =>
      request(() =>
        baseFetch<Motorcycle>(`/motorcycle/${id}`, {
          method: 'PUT',
          body: payload,
        }),
      ),

    /** DELETE /motorcycle/<id> */
    remove: (id: number | string) =>
      request(() =>
        baseFetch<{ message: string }>(`/motorcycle/${id}`, {
          method: 'DELETE',
        }),
      ),

    /** PATCH /motorcycle/<id>/note */
    updateNote: (id: number | string, note: string | null) =>
      request(() =>
        baseFetch<Motorcycle>(`/motorcycle/${id}/note`, {
          method: 'PATCH',
          body: { note },
        }),
      ),

    /** POST /motorcycle/<id>/photo — multipart, поле `photo` */
    uploadPhoto: (id: number | string, file: File) => {
      const fd = new FormData()
      fd.append('photo', file)
      return request(() =>
        baseFetch<Motorcycle>(`/motorcycle/${id}/photo`, {
          method: 'POST',
          body: fd,
        }),
      )
    },

    /** DELETE /motorcycle/<id>/photo */
    deletePhoto: (id: number | string) =>
      request(() =>
        baseFetch<Motorcycle>(`/motorcycle/${id}/photo`, { method: 'DELETE' }),
      ),
  }

    // ---------- MAINTENANCE ----------
  const maintenance = {
    /** GET /maintenance/motorcycle/<id> */
    listByMotorcycle: (motorcycleId: number | string) =>
      request(() =>
        baseFetch<Maintenance[]>(`/maintenance/motorcycle/${motorcycleId}`),
      ),

    /** POST /maintenance/ */
    create: (payload: CreateMaintenancePayload) =>
      request(() =>
        baseFetch<Maintenance>('/maintenance/', {
          method: 'POST',
          body: payload,
        }),
      ),

    /** PUT /maintenance/<id> */
    update: (
      id: number | string,
      payload: UpdateMaintenancePayload,
    ) =>
      request(() =>
        baseFetch<Maintenance>(`/maintenance/${id}`, {
          method: 'PUT',
          body: payload,
        }),
      ),

    /** DELETE /maintenance/<id> */
    remove: (id: number | string) =>
      request(() =>
        baseFetch<{ message: string }>(`/maintenance/${id}`, {
          method: 'DELETE',
        }),
      ),

    /** POST /maintenance/<id>/complete */
    complete: (
      id: number | string,
      payload: CompleteMaintenancePayload,
    ) =>
      request(() =>
        baseFetch<CompleteMaintenanceResponse>(
          `/maintenance/${id}/complete`,
          { method: 'POST', body: payload },
        ),
      ),

    /** POST /maintenance/quick-start */
    quickStart: (payload: {
      moto_id: number | string
      current_mileage: number
      drive_type?: 'chain' | 'belt' | 'shaft'
      style?: 'calm' | 'normal' | 'aggressive'
      terrain?: 'city' | 'highway' | 'mixed' | 'dusty' | 'offroad'
    }) =>
      request(() =>
        baseFetch<{ message: string; created: any[]; moto: any }>('/maintenance/quick-start', {
          method: 'POST',
          body: payload,
        }),
      ),

    /** События обслуживания */
    events: {
      /** GET /maintenance/events/?motorcycle_id=<id> */
      list: (motorcycleId: number | string, params?: { page?: number; per_page?: number }) =>
        request(() =>
          baseFetch<MaintenanceEventsListResponse>('/maintenance/events/', {
            query: { motorcycle_id: motorcycleId, ...params },
          }),
        ),

      /** POST /maintenance/events/ */
      create: (payload: CreateMaintenanceEventPayload) =>
        request(() =>
          baseFetch<MaintenanceEvent>('/maintenance/events/', {
            method: 'POST',
            body: payload,
          }),
        ),

      /** GET /maintenance/events/<id>?motorcycle_id=<id> */
      get: (eventId: number | string, motorcycleId: number | string) =>
        request(() =>
          baseFetch<MaintenanceEvent>(`/maintenance/events/${eventId}`, {
            query: { motorcycle_id: motorcycleId },
          }),
        ),

      /** PUT /maintenance/events/<id>?motorcycle_id=<id> */
      update: (
        eventId: number | string,
        motorcycleId: number | string,
        payload: UpdateMaintenanceEventPayload,
      ) =>
        request(() =>
          baseFetch<MaintenanceEvent>(`/maintenance/events/${eventId}`, {
            method: 'PUT',
            query: { motorcycle_id: motorcycleId },
            body: payload,
          }),
        ),

      /** DELETE /maintenance/events/<id>?motorcycle_id=<id> */
      remove: (eventId: number | string, motorcycleId: number | string) =>
        request(() =>
          baseFetch<{ message: string }>(`/maintenance/events/${eventId}`, {
            method: 'DELETE',
            query: { motorcycle_id: motorcycleId },
          }),
        ),
    },
  }

  // ---------- COMPONENTS ----------
  const components = {
    /** GET /motorcycle/<motoId>/components */
    list: (motoId: number | string, includeInactive = false) =>
      request(() =>
        baseFetch<ComponentListResponse>(
          `/motorcycle/${motoId}/components/`,
          { query: { include_inactive: includeInactive } },
        ),
      ),

    /** GET /motorcycle/<motoId>/components/<id> */
    get: (motoId: number | string, id: number | string) =>
      request(() =>
        baseFetch<MotorcycleComponent>(`/motorcycle/${motoId}/components/${id}`),
      ),

    /** POST /motorcycle/<motoId>/components/ */
    create: (motoId: number | string, payload: CreateComponentPayload) =>
      request(() =>
        baseFetch<MotorcycleComponent>(`/motorcycle/${motoId}/components/`, {
          method: 'POST',
          body: payload,
        }),
      ),

    /** PUT /motorcycle/<motoId>/components/<id> */
    update: (
      motoId: number | string,
      id: number | string,
      payload: UpdateComponentPayload,
    ) =>
      request(() =>
        baseFetch<MotorcycleComponent>(
          `/motorcycle/${motoId}/components/${id}`,
          { method: 'PUT', body: payload },
        ),
      ),

    /** DELETE /motorcycle/<motoId>/components/<id> — soft-delete */
    remove: (motoId: number | string, id: number | string) =>
      request(() =>
        baseFetch<{ message: string }>(
          `/motorcycle/${motoId}/components/${id}`,
          { method: 'DELETE' },
        ),
      ),

    /** POST /motorcycle/<motoId>/components/<id>/reactivate */
    reactivate: (motoId: number | string, id: number | string) =>
      request(() =>
        baseFetch<MotorcycleComponent>(
          `/motorcycle/${motoId}/components/${id}/reactivate`,
          { method: 'POST' },
        ),
      ),

    /** POST /motorcycle/<motoId>/components/apply-template — идемпотентно */
    applyTemplate: (motoId: number | string, payload: ApplyTemplatePayload = {}) =>
      request(() =>
        baseFetch<ApplyTemplateResponse>(
          `/motorcycle/${motoId}/components/apply-template`,
          { method: 'POST', body: payload },
        ),
      ),

    /** GET /motorcycle/<motoId>/components/<id>/history */
    history: (motoId: number | string, id: number | string) =>
      request(() =>
        baseFetch<ComponentHistoryResponse>(
          `/motorcycle/${motoId}/components/${id}/history`,
        ),
      ),
  }

  // ---------- MANUALS ----------
  const manuals = {
    list: (params?: Record<string, any>) =>
      request(() => baseFetch<ManualsListResponse>('/manual/list', { query: params })),
    get: (id: number | string) =>
      request(() => baseFetch<Manual>(`/manual/${id}`)),

    create: (payload: CreateManualPayload, stepImages?: (File | null)[]) => {
      const formData = new FormData()
      formData.append('data', JSON.stringify(payload))

      if (stepImages) {
        stepImages.forEach((file, idx) => {
          if (file) {
            formData.append(`image_${idx + 1}`, file)
          }
        })
      }

      return request(() =>
        baseFetch<Manual>('/manual/new-manual', {
          method: 'POST',
          body: formData,
        }),
      )
    },

    update: (id: number | string, payload: UpdateManualPayload) =>
      request(() =>
        baseFetch<Manual>(`/manual/${id}`, {
          method: 'PUT',
          body: payload,
        }),
      ),

    deleteStepImage: (manualId: number | string, stepId: number | string) =>
      request(() =>
        baseFetch<{ message: string }>(`/manual/${manualId}/steps/${stepId}/image`, {
          method: 'DELETE',
        }),
      ),

    uploadStepImage: (manualId: number | string, stepId: number | string, file: File) => {
      const formData = new FormData()
      formData.append('image', file)
      return request(() =>
        baseFetch<{ message: string; image_url: string }>(`/manual/${manualId}/steps/${stepId}/image`, {
          method: 'POST',
          body: formData,
        }),
      )
    }
  }

  // ---------- TRAINING ----------
  const training = {
    // Курсы
    listCourses: (params?: {
      category?: string
      level?: string
      is_free?: boolean
      search?: string
      page?: number
      per_page?: number
    }) =>
      request(() => baseFetch<CourseListResponse>('/learning/courses', { query: params })),

    getCourse: (slug: string) =>
      request(() => baseFetch<CourseDetail>(`/learning/courses/${slug}`)),

    getLesson: (courseSlug: string, lessonSlug: string) =>
      request(() => baseFetch<LessonDetail>(`/learning/courses/${courseSlug}/lessons/${lessonSlug}`)),

    completeLesson: (courseSlug: string, lessonSlug: string) =>
      request(() => baseFetch<{ completed: boolean; course_progress: CourseProgress }>(
        `/learning/courses/${courseSlug}/lessons/${lessonSlug}/complete`,
        { method: 'POST' }
      )),

    uncompleteLesson: (courseSlug: string, lessonSlug: string) =>
      request(() => baseFetch<{ completed: boolean; course_progress: CourseProgress }>(
        `/learning/courses/${courseSlug}/lessons/${lessonSlug}/complete`,
        { method: 'DELETE' }
      )),

    // Статьи
    listArticles: (params?: {
      category?: string
      tag?: string
      search?: string
      page?: number
      per_page?: number
    }) =>
      request(() => baseFetch<ArticleListResponse>('/learning/articles', { query: params })),

    getArticle: (slug: string) =>
      request(() => baseFetch<ArticleDetail>(`/learning/articles/${slug}`)),

    // Моё обучение
    myLearning: () =>
      request(() => baseFetch<MyLearningResponse>('/learning/my')),
  }

  // ---------- SOCIAL ----------
  const social = {
    getPosts: (params?: { page?: number; per_page?: number; user_id?: number; include_comments?: boolean }) =>
      request(() => baseFetch<PostsListResponse>('/social/posts', { query: params })),

    getPost: (id: number | string, include_comments = true) =>
      request(() => baseFetch<Post>(`/social/posts/${id}`, { query: { include_comments } })),

    createPost: (content: string, imageFile?: File | null) => {
      const fd = new FormData()
      fd.append('content', content)
      if (imageFile) fd.append('image', imageFile)
      return request(() =>
        baseFetch<Post>('/social/posts', {
          method: 'POST',
          body: fd,
        }),
      )
    },

    toggleLike: (id: number | string) =>
      request(() =>
        baseFetch<LikeToggleResponse>(`/social/posts/${id}/like`, { method: 'POST' }),
      ),

    addComment: (postId: number | string, content: string) =>
      request(() =>
        baseFetch<PostComment>(`/social/posts/${postId}/comments`, {
          method: 'POST',
          body: { content },
        }),
      ),

    deleteComment: (commentId: number | string) =>
      request(() =>
        baseFetch<{ message: string }>(`/social/comments/${commentId}`, { method: 'DELETE' }),
      ),

    reportPost: (postId: number | string, category: string, description?: string) =>
      request(() =>
        baseFetch<{ message: string; report: any }>(`/social/posts/${postId}/report`, {
          method: 'POST',
          body: { category, description },
        }),
      ),

    deletePost: (id: number | string) =>
      request(() =>
        baseFetch<{ message: string }>(`/social/posts/${id}`, { method: 'DELETE' }),
      ),

    getReportCategories: () =>
      request(() => baseFetch<ReportCategory[]>('/social/report-categories')),
  }

  // ---------- ADMIN ----------
  const admin = {
    getDashboard: () =>
      request(() => baseFetch<{
        users: AdminUser[]
        manuals: any[]
        users_count: number
        manuals_count: number
        motorcycles_count: number
      }>('/admin/get')),

    getUsers: (params?: { page?: number; per_page?: number; search?: string; role?: string; status?: string }) =>
      request(() => baseFetch<AdminUsersResponse>('/admin/users', { query: params })),

    banUser: (id: number | string) =>
      request(() => baseFetch<{ message: string; user: AdminUser }>(`/admin/user/${id}/ban`, { method: 'POST' })),

    unbanUser: (id: number | string) =>
      request(() => baseFetch<{ message: string; user: AdminUser }>(`/admin/user/${id}/unban`, { method: 'POST' })),

    updateUser: (id: number | string, payload: { role?: string; status?: string; username?: string; email?: string }) =>
      request(() => baseFetch<AdminUser>(`/admin/user/${id}`, { method: 'PUT', body: payload })),

    deleteUser: (id: number | string) =>
      request(() => baseFetch<{ message: string }>(`/admin/user/${id}`, { method: 'DELETE' })),

    // Модерация мануалов
    getManualsForModeration: (params?: { status?: string; page?: number; per_page?: number }) =>
      request(() => baseFetch<{ manuals: any[]; total: number; pages: number }>('/admin/get', { query: params })),

    approveManual: (id: number | string) =>
      request(() => baseFetch<{ message: string }>(`/admin/manual/${id}/approve`, { method: 'POST' })),

    rejectManual: (id: number | string, reason: string) =>
      request(() => baseFetch<{ message: string }>(`/admin/manual/${id}/reject`, { method: 'POST', body: { reason } })),

    reconsiderManual: (id: number | string) =>
      request(() => baseFetch<{ message: string }>(`/admin/manual/${id}/reconsider`, { method: 'POST' })),

    deleteManual: (id: number | string) =>
      request(() => baseFetch<{ message: string }>(`/admin/manual/${id}`, { method: 'DELETE' })),

    // Жалобы
    getReports: (params?: { page?: number; per_page?: number; status?: string; category?: string }) =>
      request(() => baseFetch<AdminReportsResponse>('/admin/reports', { query: params })),

    resolveReport: (id: number | string, action: string, note?: string) =>
      request(() => baseFetch<{ message: string; report: AdminReport }>(`/admin/reports/${id}/resolve`, {
        method: 'POST',
        body: { action, note },
      })),

    deleteReport: (id: number | string) =>
      request(() => baseFetch<{ message: string }>(`/admin/reports/${id}`, { method: 'DELETE' })),

    // Курсы
    adminListCourses: (params?: { page?: number; per_page?: number }) =>
      request(() => baseFetch<{ courses: any[]; pagination: any }>('/learning/admin/courses', { query: params })),

    adminGetCourse: (id: number | string) =>
      request(() => baseFetch<any>(`/learning/admin/courses/${id}`)),

    adminCreateCourse: (payload: any) =>
      request(() => baseFetch<any>('/learning/admin/courses', { method: 'POST', body: payload })),

    adminUpdateCourse: (id: number | string, payload: any) =>
      request(() => baseFetch<any>(`/learning/admin/courses/${id}`, { method: 'PUT', body: payload })),

    adminDeleteCourse: (id: number | string) =>
      request(() => baseFetch<{ message: string }>(`/learning/admin/courses/${id}`, { method: 'DELETE' })),

    adminPublishCourse: (id: number | string) =>
      request(() => baseFetch<any>(`/learning/admin/courses/${id}/publish`, { method: 'POST' })),

    adminArchiveCourse: (id: number | string) =>
      request(() => baseFetch<any>(`/learning/admin/courses/${id}/archive`, { method: 'POST' })),

    // Уроки
    adminCreateLesson: (courseId: number | string, payload: any) =>
      request(() => baseFetch<any>(`/learning/admin/courses/${courseId}/lessons`, { method: 'POST', body: payload })),

    adminUpdateLesson: (lessonId: number | string, payload: any) =>
      request(() => baseFetch<any>(`/learning/admin/lessons/${lessonId}`, { method: 'PUT', body: payload })),

    adminDeleteLesson: (lessonId: number | string) =>
      request(() => baseFetch<{ message: string }>(`/learning/admin/lessons/${lessonId}`, { method: 'DELETE' })),

    adminReorderLessons: (courseId: number | string, items: { id: number; order: number }[]) =>
      request(() => baseFetch<any>(`/learning/admin/courses/${courseId}/lessons/reorder`, { method: 'POST', body: { items } })),

    // Статьи
    adminListArticles: (params?: { page?: number; per_page?: number }) =>
      request(() => baseFetch<{ articles: any[]; pagination: any }>('/learning/admin/articles', { query: params })),

    adminGetArticle: (id: number | string) =>
      request(() => baseFetch<any>(`/learning/admin/articles/${id}`)),

    adminCreateArticle: (payload: any) =>
      request(() => baseFetch<any>('/learning/admin/articles', { method: 'POST', body: payload })),

    adminUpdateArticle: (id: number | string, payload: any) =>
      request(() => baseFetch<any>(`/learning/admin/articles/${id}`, { method: 'PUT', body: payload })),

    adminDeleteArticle: (id: number | string) =>
      request(() => baseFetch<{ message: string }>(`/learning/admin/articles/${id}`, { method: 'DELETE' })),

    adminPublishArticle: (id: number | string) =>
      request(() => baseFetch<any>(`/learning/admin/articles/${id}/publish`, { method: 'POST' })),

    adminArchiveArticle: (id: number | string) =>
      request(() => baseFetch<any>(`/learning/admin/articles/${id}/archive`, { method: 'POST' })),


    adminUploadCover: (file: File) => {
      const fd = new FormData()
      fd.append('file', file)
      return request(() => baseFetch<{ url: string }>('/learning/admin/upload/cover', { method: 'POST', body: fd }))
    },
  }

  // ---------- USER ----------
  const user = {
    getMyProfile: () =>
      request(() => baseFetch<{ user: UserProfile }>('/user/profile/me')),

    updateProfile: (payload: { username?: string; email?: string }) =>
      request(() => baseFetch<UserProfile>('/user/profile', { method: 'PUT', body: payload })),

    uploadAvatar: (file: File) => {
      const fd = new FormData()
      fd.append('avatar', file)
      return request(() => baseFetch<UserProfile>('/user/avatar', { method: 'POST', body: fd }))
    },

    deleteAvatar: () =>
      request(() => baseFetch<UserProfile>('/user/avatar', { method: 'DELETE' })),

    changePassword: (payload: { currentPassword: string; newPassword: string }) =>
      request(() => baseFetch<UserProfile>('/user/change-password', { method: 'PATCH', body: payload })),

    getNotificationSettings: () =>
      request(() => baseFetch<NotificationSettings>('/user/notification-settings')),

    updateNotificationSettings: (payload: Partial<NotificationSettings>) =>
      request(() => baseFetch<{ message: string; settings: NotificationSettings }>('/user/notification-settings', { method: 'PUT', body: payload })),

    deleteAccount: (password: string) =>
      request(() => baseFetch<{ message: string }>('/user/account', { method: 'DELETE', body: { password } })),
  }

  // ---------- NOTIFICATIONS ----------
  const notifications = {
    list: (params?: { page?: number; per_page?: number; unread_only?: boolean }) =>
      request(() => baseFetch<NotificationsResponse>('/notifications/', { query: params })),

    getUnreadCount: () =>
      request(() => baseFetch<UnreadCountResponse>('/notifications/unread-count')),

    markRead: (id: number | string) =>
      request(() => baseFetch<Notification>(`/notifications/${id}/read`, { method: 'PUT' })),

    markAllRead: () =>
      request(() => baseFetch<{ message: string }>('/notifications/read-all', { method: 'PUT' })),

    remove: (id: number | string) =>
      request(() => baseFetch<{ message: string }>(`/notifications/${id}`, { method: 'DELETE' })),
  }

  return {
    auth,
    motorcycle,
    maintenance,
    components,
    manuals,
    training,
    social,
    admin,
    user,
    notifications
  }
}
