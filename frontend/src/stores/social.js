import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import socialApi from '../api/social'

const DEFAULT_PAGINATION = {
  current_page: 1,
  per_page: 10,
  total: 0,
  pages: 0,
  has_prev: false,
  has_next: false,
}

export const useSocialStore = defineStore('social', () => {
  // ===== State =====
  const feed = ref([])
  const current = ref(null)
  const currentComments = ref([])
  const loading = ref(false)
  const loadingCurrent = ref(false)
  const pagination = ref({ ...DEFAULT_PAGINATION })

  // ===== Getters =====
  const hasMore = computed(() => pagination.value.has_next)

  // ===== Actions =====

  async function loadFeed(page = 1) {
    loading.value = true
    try {
      const { data } = await socialApi.getPosts(
        page,
        pagination.value.per_page,
        null,
        true
      )
      feed.value = data.posts || []
      pagination.value = {
        current_page: data.current_page,
        per_page: data.per_page,
        total: data.total,
        pages: data.pages,
        has_prev: data.has_prev,
        has_next: data.has_next,
      }
      return feed.value
    } finally {
      loading.value = false
    }
  }

  async function loadOne(postId) {
    loadingCurrent.value = true
    try {
      const { data } = await socialApi.getPost(postId, true)
      current.value = data
      currentComments.value = data.comments || []
      return data
    } finally {
      loadingCurrent.value = false
    }
  }

  async function createPost(formData) {
    const { data } = await socialApi.createPost(formData)
    return data
  }

  async function updatePost(postId, formData) {
    const { data } = await socialApi.updatePost(postId, formData)

    const idx = feed.value.findIndex((p) => p.id === postId)
    if (idx !== -1) {
      feed.value[idx] = { ...feed.value[idx], ...data }
    }
    if (current.value?.id === postId) {
      current.value = { ...current.value, ...data }
    }

    return data
  }

  async function removePost(postId) {
    await socialApi.deletePost(postId)
    feed.value = feed.value.filter((p) => p.id !== postId)
    pagination.value.total = Math.max(0, pagination.value.total - 1)
    if (current.value?.id === postId) {
      current.value = null
    }
  }

  async function toggleLike(postId) {
    const { data } = await socialApi.toggleLike(postId)

    const inFeed = feed.value.find((p) => p.id === postId)
    if (inFeed) {
      inFeed.likes_count = data.likes_count
      inFeed.is_liked = data.liked
    }
    if (current.value?.id === postId) {
      current.value.likes_count = data.likes_count
      current.value.is_liked = data.liked
    }

    return data
  }

  async function addComment(postId, content) {
    const { data } = await socialApi.addComment(postId, content)
    currentComments.value.push(data)

    if (current.value?.id === postId) {
      current.value.comments_count = (current.value.comments_count || 0) + 1
    }
    const inFeed = feed.value.find((p) => p.id === postId)
    if (inFeed) {
      inFeed.comments_count = (inFeed.comments_count || 0) + 1
    }

    return data
  }

  async function removeComment(commentId) {
    await socialApi.deleteComment(commentId)
    currentComments.value = currentComments.value.filter((c) => c.id !== commentId)

    if (current.value) {
      current.value.comments_count = Math.max(
        0,
        (current.value.comments_count || 0) - 1
      )
    }
  }

  function applyPostUpdate(updatedPost) {
    const idx = feed.value.findIndex((p) => p.id === updatedPost.id)
    if (idx !== -1) {
      feed.value[idx] = { ...feed.value[idx], ...updatedPost }
    }
    if (current.value?.id === updatedPost.id) {
      current.value = { ...current.value, ...updatedPost }
    }
  }

  function reset() {
    feed.value = []
    current.value = null
    currentComments.value = []
    pagination.value = { ...DEFAULT_PAGINATION }
    loading.value = false
    loadingCurrent.value = false
  }

  return {
    feed,
    current,
    currentComments,
    loading,
    loadingCurrent,
    pagination,
    hasMore,
    loadFeed,
    loadOne,
    createPost,
    updatePost,
    removePost,
    toggleLike,
    addComment,
    removeComment,
    applyPostUpdate,
    reset,
  }
})
