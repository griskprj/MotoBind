import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import api from '../api/api'

const DEFAULT_COURSE_FILTERS = {
  category: '',
  level: '',
  is_free: null,
  search: '',
}

const DEFAULT_ARTICLE_FILTERS = {
  category: '',
  tag: '',
  search: '',
}

export const useLearningStore = defineStore('learning', () => {
  // ===== State =====
  const courses = ref([])
  const coursesPagination = ref(null)
  const coursesLoading = ref(false)
  const courseFilters = ref({ ...DEFAULT_COURSE_FILTERS })

  const currentCourse = ref(null)
  const currentCourseLoading = ref(false)

  const currentLesson = ref(null)
  const currentLessonLoading = ref(false)

  const articles = ref([])
  const articlesPagination = ref(null)
  const articlesLoading = ref(false)
  const articleFilters = ref({ ...DEFAULT_ARTICLE_FILTERS })

  const currentArticle = ref(null)
  const currentArticleLoading = ref(false)

  const myLearning = ref(null)
  const myLearningLoading = ref(false)

  // ===== Getters =====
  const hasCourses = computed(() => courses.value.length > 0)
  const hasArticles = computed(() => articles.value.length > 0)

  const myLearningCounts = computed(() => ({
    inProgress: myLearning.value?.in_progress?.length || 0,
    completed: myLearning.value?.completed?.length || 0,
    notStarted: myLearning.value?.not_started?.length || 0,
  }))

  // ===== Actions — курсы =====
  async function loadCourses(overrides = {}) {
    coursesLoading.value = true
    try {
      const params = {
        ...courseFilters.value,
        ...overrides,
      }
      // чистим пустые
      Object.keys(params).forEach((k) => {
        if (params[k] === '' || params[k] === null || params[k] === undefined) {
          delete params[k]
        }
      })

      const { data } = await api.get('/learning/courses', { params })
      courses.value = data.courses || []
      coursesPagination.value = data.pagination || null
      return data
    } finally {
      coursesLoading.value = false
    }
  }

  async function loadCourse(slug) {
    currentCourseLoading.value = true
    try {
      const { data } = await api.get(`/learning/courses/${slug}`)
      currentCourse.value = data
      return data
    } finally {
      currentCourseLoading.value = false
    }
  }

  async function loadLesson(courseSlug, lessonSlug) {
    currentLessonLoading.value = true
    try {
      const { data } = await api.get(
        `/learning/courses/${courseSlug}/lessons/${lessonSlug}`
      )
      currentLesson.value = data
      return data
    } finally {
      currentLessonLoading.value = false
    }
  }

  async function completeLesson(courseSlug, lessonSlug) {
    const { data } = await api.post(
      `/learning/courses/${courseSlug}/lessons/${lessonSlug}/complete`
    )
    // обновляем локально
    if (currentLesson.value?.slug === lessonSlug) {
      currentLesson.value.is_completed = true
    }
    // обновляем прогресс курса, если открыт
    if (currentCourse.value?.slug === courseSlug) {
      currentCourse.value.progress = data.course_progress
      // обновляем в списке уроков
      const lesson = currentCourse.value.lessons?.find(
        (l) => l.slug === lessonSlug
      )
      if (lesson) lesson.is_completed = true
    }
    return data
  }

  async function uncompleteLesson(courseSlug, lessonSlug) {
    const { data } = await api.delete(
      `/learning/courses/${courseSlug}/lessons/${lessonSlug}/complete`
    )
    if (currentLesson.value?.slug === lessonSlug) {
      currentLesson.value.is_completed = false
    }
    if (currentCourse.value?.slug === courseSlug) {
      currentCourse.value.progress = data.course_progress
      const lesson = currentCourse.value.lessons?.find(
        (l) => l.slug === lessonSlug
      )
      if (lesson) lesson.is_completed = false
    }
    return data
  }

  // ===== Actions — статьи =====
  async function loadArticles(overrides = {}) {
    articlesLoading.value = true
    try {
      const params = {
        ...articleFilters.value,
        ...overrides,
      }
      Object.keys(params).forEach((k) => {
        if (params[k] === '' || params[k] === null || params[k] === undefined) {
          delete params[k]
        }
      })

      const { data } = await api.get('/learning/articles', { params })
      articles.value = data.articles || []
      articlesPagination.value = data.pagination || null
      return data
    } finally {
      articlesLoading.value = false
    }
  }

  async function loadArticle(slug) {
    currentArticleLoading.value = true
    try {
      const { data } = await api.get(`/learning/articles/${slug}`)
      currentArticle.value = data
      return data
    } finally {
      currentArticleLoading.value = false
    }
  }

  // ===== Actions — моё обучение =====
  async function loadMyLearning() {
    myLearningLoading.value = true
    try {
      const { data } = await api.get('/learning/my')
      myLearning.value = data
      return data
    } finally {
      myLearningLoading.value = false
    }
  }

  // ===== Helpers =====
  function resetCurrent() {
    currentCourse.value = null
    currentLesson.value = null
    currentArticle.value = null
  }

  function reset() {
    courses.value = []
    coursesPagination.value = null
    courseFilters.value = { ...DEFAULT_COURSE_FILTERS }
    articles.value = []
    articlesPagination.value = null
    articleFilters.value = { ...DEFAULT_ARTICLE_FILTERS }
    myLearning.value = null
    resetCurrent()
    coursesLoading.value = false
    articlesLoading.value = false
    myLearningLoading.value = false
  }

  return {
    // state
    courses,
    coursesPagination,
    coursesLoading,
    courseFilters,
    currentCourse,
    currentCourseLoading,
    currentLesson,
    currentLessonLoading,
    articles,
    articlesPagination,
    articlesLoading,
    articleFilters,
    currentArticle,
    currentArticleLoading,
    myLearning,
    myLearningLoading,

    // getters
    hasCourses,
    hasArticles,
    myLearningCounts,

    // actions
    loadCourses,
    loadCourse,
    loadLesson,
    completeLesson,
    uncompleteLesson,
    loadArticles,
    loadArticle,
    loadMyLearning,
    resetCurrent,
    reset,
  }
})
