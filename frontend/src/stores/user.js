import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import api from '../api/api'
import { getAvatarUrl as resolveAvatarUrl } from '../utils/mediaUrl'

const DEFAULT_NOTIFICATION_SETTINGS = {
  email_notifications_enabled: true,
  email_newsletter_enabled: true,
  email_verification_enabled: true,
  reminders_mileage_enabled: true,
  reminders_maintenance_enabled: true,
}

export const useUserStore = defineStore('user', () => {
  // ===== State =====
  const profile = ref(null)
  const notificationSettings = ref({ ...DEFAULT_NOTIFICATION_SETTINGS })

  const loading = ref(false)
  const savingProfile = ref(false)
  const savingSettings = ref(false)
  const uploadingAvatar = ref(false)

  // ===== Getters =====
  const stats = computed(() => ({
    posts: profile.value?.stats?.posts_count || 0,
    likes: profile.value?.stats?.likes_received || 0,
    comments: profile.value?.stats?.comments_received || 0,
    motorcycles: profile.value?.motorcycles?.length || 0,
  }))

  const avatarUrl = computed(() => resolveAvatarUrl(profile.value?.avatar))

  const hasSocialLinks = computed(() => {
    const links = profile.value?.social_links
    if (!links) return false
    return Object.values(links).some((url) => url && url.trim())
  })

  // ===== Actions =====

  async function loadProfile() {
    loading.value = true
    try {
      const { data } = await api.get('/user/profile/me', { cache: 30_000 })
      profile.value = data.user
      return profile.value
    } finally {
      loading.value = false
    }
  }

  async function updateProfile(formData) {
    savingProfile.value = true
    try {
      const { data } = await api.put('/user/profile', formData)
      profile.value = data
      try {
        const { useAuthStore } = await import('./auth')
        useAuthStore().setUser(data)
      } catch {
      }
      return data
    } finally {
      savingProfile.value = false
    }
  }

  async function uploadAvatar(file) {
    uploadingAvatar.value = true
    try {
      const fd = new FormData()
      fd.append('avatar', file)
      const { data } = await api.post('/user/avatar', fd, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      profile.value = data
      try {
        const { useAuthStore } = await import('./auth')
        useAuthStore().setUser(data)
      } catch {
        /* ignore */
      }
      return data
    } finally {
      uploadingAvatar.value = false
    }
  }

  async function deleteAvatar() {
    const { data } = await api.delete('/user/avatar')
    profile.value = data
    try {
      const { useAuthStore } = await import('./auth')
      useAuthStore().setUser(data)
    } catch {
      /* ignore */
    }
    return data
  }

  async function changePassword({ currentPassword, newPassword }) {
    await api.patch('/user/change-password', { currentPassword, newPassword })
  }

  async function deleteAccount(password) {
    await api.delete('/user/account', { data: { password } })
  }

  async function loadNotificationSettings() {
    const { data } = await api.get('/user/notification-settings')
    notificationSettings.value = {
      email_notifications_enabled: data.email_notifications_enabled ?? true,
      email_newsletter_enabled: data.email_newsletter_enabled ?? true,
      email_verification_enabled: data.email_verification_enabled ?? true,
      reminders_mileage_enabled: data.reminders_mileage_enabled ?? true,
      reminders_maintenance_enabled: data.reminders_maintenance_enabled ?? true,
    }
    return notificationSettings.value
  }

  async function updateNotificationSettings(settings) {
    savingSettings.value = true
    try {
      notificationSettings.value = { ...notificationSettings.value, ...settings }
      await api.put('/user/notification-settings', notificationSettings.value)
      return notificationSettings.value
    } catch (err) {
      await loadNotificationSettings().catch(() => {})
      throw err
    } finally {
      savingSettings.value = false
    }
  }

  function reset() {
    profile.value = null
    notificationSettings.value = { ...DEFAULT_NOTIFICATION_SETTINGS }
    loading.value = false
    savingProfile.value = false
    savingSettings.value = false
    uploadingAvatar.value = false
  }

  return {
    profile,
    notificationSettings,
    loading,
    savingProfile,
    savingSettings,
    uploadingAvatar,

    stats,
    avatarUrl,
    hasSocialLinks,

    loadProfile,
    updateProfile,
    uploadAvatar,
    deleteAvatar,
    changePassword,
    deleteAccount,
    loadNotificationSettings,
    updateNotificationSettings,
    reset,
  }
})
