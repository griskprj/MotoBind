import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '../api/api'

export const useAdminLearningStore = defineStore('adminLearning', () => {
  // ===== State =====
  const courses = ref([])
  const coursesPagination = ref(null)
  const coursesLoading = ref(false)

  const currentCourse = ref(null)
  const currentCourseLoading = ref(false)

  const articles = ref([])
  const articlesPagination = ref(null)
  const articlesLoading = ref(false)

  const currentArticle = ref(null)
  const currentArticleLoading = ref(false)

  const saving = ref(false)
  const uploading = ref(false)

  // ===== Курсы =====
  async function loadCourses(page = 1, perPage = 20) {
    coursesLoading.value = true
    try {
      const { data } = await api.get('/learning/admin/courses', {
        params: { page, per_page: perPage },
      })
      courses.value = data.courses || []
      coursesPagination.value = data.pagination || null
      return data
    } finally {
      coursesLoading.value = false
    }
  }

  async function loadCourse(id) {
    currentCourseLoading.value = true
    try {
      const { data } = await api.get(`/learning/admin/courses/${id}`)
      currentCourse.value = data
      return data
    } finally {
      currentCourseLoading.value = false
    }
  }

  async function createCourse(payload) {
    saving.value = true
    try {
      const { data } = await api.post('/learning/admin/courses', payload)
      currentCourse.value = data
      return data
    } finally {
      saving.value = false
    }
  }

  async function updateCourse(id, payload) {
    saving.value = true
    try {
      const { data } = await api.put(`/learning/admin/courses/${id}`, payload)
      currentCourse.value = data
      // обновляем в списке
      const idx = courses.value.findIndex((c) => c.id === id)
      if (idx !== -1) courses.value[idx] = { ...courses.value[idx], ...data }
      return data
    } finally {
      saving.value = false
    }
  }

  async function deleteCourse(id) {
    await api.delete(`/learning/admin/courses/${id}`)
    courses.value = courses.value.filter((c) => c.id !== id)
    if (currentCourse.value?.id === id) currentCourse.value = null
  }

  async function publishCourse(id) {
    const { data } = await api.post(`/learning/admin/courses/${id}/publish`)
    currentCourse.value = data
    const idx = courses.value.findIndex((c) => c.id === id)
    if (idx !== -1) courses.value[idx] = { ...courses.value[idx], ...data }
    return data
  }

  async function archiveCourse(id) {
    const { data } = await api.post(`/learning/admin/courses/${id}/archive`)
    currentCourse.value = data
    const idx = courses.value.findIndex((c) => c.id === id)
    if (idx !== -1) courses.value[idx] = { ...courses.value[idx], ...data }
    return data
  }

  // ===== Уроки =====
  async function loadLesson(lessonId) {
    const { data } = await api.get(`/learning/admin/lessons/${lessonId}`)
    return data
  }

  async function createLesson(courseId, payload) {
    saving.value = true
    try {
      const { data } = await api.post(
        `/learning/admin/courses/${courseId}/lessons`,
        payload
      )
      await loadCourse(courseId)
      return data
    } finally {
      saving.value = false
    }
  }

  async function updateLesson(lessonId, payload) {
    saving.value = true
    try {
      const { data } = await api.put(
        `/learning/admin/lessons/${lessonId}`,
        payload
      )
      return data
    } finally {
      saving.value = false
    }
  }

  async function deleteLesson(courseId, lessonId) {
    await api.delete(`/learning/admin/lessons/${lessonId}`)
    await loadCourse(courseId)
  }

  async function reorderLessons(courseId, items) {
    saving.value = true
    try {
      const { data } = await api.post(
        `/learning/admin/courses/${courseId}/lessons/reorder`,
        { items }
      )
      currentCourse.value = data
      return data
    } finally {
      saving.value = false
    }
  }

  // ===== Статьи =====
  async function loadArticles(page = 1, perPage = 20) {
    articlesLoading.value = true
    try {
      const { data } = await api.get('/learning/admin/articles', {
        params: { page, per_page: perPage },
      })
      articles.value = data.articles || []
      articlesPagination.value = data.pagination || null
      return data
    } finally {
      articlesLoading.value = false
    }
  }

  async function loadArticle(id) {
    currentArticleLoading.value = true
    try {
      const { data } = await api.get(`/learning/admin/articles/${id}`)
      currentArticle.value = data
      return data
    } finally {
      currentArticleLoading.value = false
    }
  }

  async function createArticle(payload) {
    saving.value = true
    try {
      const { data } = await api.post('/learning/admin/articles', payload)
      currentArticle.value = data
      return data
    } finally {
      saving.value = false
    }
  }

  async function updateArticle(id, payload) {
    saving.value = true
    try {
      const { data } = await api.put(
        `/learning/admin/articles/${id}`,
        payload
      )
      currentArticle.value = data
      const idx = articles.value.findIndex((a) => a.id === id)
      if (idx !== -1) articles.value[idx] = { ...articles.value[idx], ...data }
      return data
    } finally {
      saving.value = false
    }
  }

  async function deleteArticle(id) {
    await api.delete(`/learning/admin/articles/${id}`)
    articles.value = articles.value.filter((a) => a.id !== id)
    if (currentArticle.value?.id === id) currentArticle.value = null
  }

  async function publishArticle(id) {
    const { data } = await api.post(`/learning/admin/articles/${id}/publish`)
    currentArticle.value = data
    const idx = articles.value.findIndex((a) => a.id === id)
    if (idx !== -1) articles.value[idx] = { ...articles.value[idx], ...data }
    return data
  }

  async function archiveArticle(id) {
    const { data } = await api.post(`/learning/admin/articles/${id}/archive`)
    currentArticle.value = data
    const idx = articles.value.findIndex((a) => a.id === id)
    if (idx !== -1) articles.value[idx] = { ...articles.value[idx], ...data }
    return data
  }

  // ===== Загрузка обложки =====
  async function uploadCover(file) {
    uploading.value = true
    try {
      const fd = new FormData()
      fd.append('file', file)
      const { data } = await api.post('/learning/admin/upload/cover', fd, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      return data.url
    } finally {
      uploading.value = false
    }
  }

  function resetCurrent() {
    currentCourse.value = null
    currentArticle.value = null
  }

  return {
    courses,
    coursesPagination,
    coursesLoading,
    currentCourse,
    currentCourseLoading,
    articles,
    articlesPagination,
    articlesLoading,
    currentArticle,
    currentArticleLoading,
    saving,
    uploading,

    loadCourses,
    loadCourse,
    createCourse,
    updateCourse,
    deleteCourse,
    publishCourse,
    archiveCourse,

    loadLesson,
    createLesson,
    updateLesson,
    deleteLesson,
    reorderLessons,

    loadArticles,
    loadArticle,
    createArticle,
    updateArticle,
    deleteArticle,
    publishArticle,
    archiveArticle,

    uploadCover,
    resetCurrent,
  }
})
