import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import notificationsApi from '../api/notifications'

const POLL_INTERVAL_MS = 30_000

export const useNotificationsStore = defineStore('notifications', () => {
  // ===== State =====
  const items = ref([])
  const unreadCount = ref(0)
  const loading = ref(false)
  const pagination = ref({
    current_page: 1,
    per_page: 20,
    total: 0,
    pages: 0,
    has_prev: false,
    has_next: false,
  })

  let pollTimer = null

  // ===== Getters =====
  const hasUnread = computed(() => unreadCount.value > 0)
  const unreadItems = computed(() => items.value.filter((n) => !n.is_read))

  // ===== Actions =====
  async function loadCount() {
    const { data } = await notificationsApi.getUnreadCount()
    unreadCount.value = data.unread_count || 0
    return unreadCount.value
  }

  async function loadList(page = 1, { unreadOnly = false } = {}) {
    loading.value = true
    try {
      const { data } = await notificationsApi.getNotifications(page, 20, unreadOnly)
      items.value = data.notifications || []
      pagination.value = {
        current_page: data.current_page,
        per_page: data.per_page,
        total: data.total,
        pages: data.pages,
        has_prev: data.has_prev,
        has_next: data.has_next,
      }
      return items.value
    } finally {
      loading.value = false
    }
  }

  async function loadRecent(limit = 5) {
    loading.value = true
    try {
      const { data } = await notificationsApi.getNotifications(1, limit, false)
      items.value = data.notifications || []
      return items.value
    } finally {
      loading.value = false
    }
  }

  async function markAsRead(id) {
    const item = items.value.find((n) => n.id === id)
    if (item && item.is_read) return
    await notificationsApi.markAsRead(id)
    if (item) item.is_read = true
    unreadCount.value = Math.max(0, unreadCount.value - 1)
  }

  async function markAllRead() {
    await notificationsApi.markAllRead()
    items.value.forEach((n) => (n.is_read = true))
    unreadCount.value = 0
  }

  async function remove(id) {
    const item = items.value.find((n) => n.id === id)
    await notificationsApi.deleteNotification(id)
    items.value = items.value.filter((n) => n.id !== id)
    if (item && !item.is_read) {
      unreadCount.value = Math.max(0, unreadCount.value - 1)
    }
  }

  function startPolling() {
    stopPolling()
    loadCount().catch(() => {})
    pollTimer = setInterval(() => {
      loadCount().catch(() => {})
    }, POLL_INTERVAL_MS)
  }

  function stopPolling() {
    if (pollTimer) {
      clearInterval(pollTimer)
      pollTimer = null
    }
  }

  function reset() {
    stopPolling()
    items.value = []
    unreadCount.value = 0
    loading.value = false
    pagination.value = {
      current_page: 1,
      per_page: 20,
      total: 0,
      pages: 0,
      has_prev: false,
      has_next: false,
    }
  }

  return {
    items,
    unreadCount,
    loading,
    pagination,

    hasUnread,
    unreadItems,

    loadCount,
    loadList,
    loadRecent,
    markAsRead,
    markAllRead,
    remove,
    startPolling,
    stopPolling,
    reset,
  }
})
