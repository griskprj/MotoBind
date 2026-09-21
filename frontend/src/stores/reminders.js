import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import remindersApi from '../api/reminders'

export const useRemindersStore = defineStore('reminders', () => {
  // ===== State =====
  const items = ref([])
  const count = ref(0)
  const loading = ref(false)

  // ===== Getters =====
  /** Напоминания для конкретного мотоцикла, отсортированные по приоритету */
  const forMotorcycle = computed(() => (motoId) => {
    if (!motoId) return []
    const priority = {
      maintenance_overdue: 0,
      maintenance_soon: 1,
      mileage_update: 2,
    }
    return items.value
      .filter((r) => r.motorcycle_id === motoId)
      .sort((a, b) => (priority[a.type] ?? 99) - (priority[b.type] ?? 99))
  })

  const hasAny = computed(() => items.value.length > 0)

  // ===== Actions =====
  async function loadPending() {
    loading.value = true
    try {
      const { data } = await remindersApi.getReminders('pending')
      items.value = data.reminders || []
      count.value = items.value.length
      return items.value
    } finally {
      loading.value = false
    }
  }

  async function loadCount() {
    const { data } = await remindersApi.getCount()
    count.value = data.count || 0
    return count.value
  }

  async function dismiss(id) {
    await remindersApi.dismiss(id)
    items.value = items.value.filter((r) => r.id !== id)
    count.value = Math.max(0, count.value - 1)
  }

  async function snooze(id, days = 7) {
    const { data } = await remindersApi.snooze(id, days)
    const idx = items.value.findIndex((r) => r.id === id)
    if (idx !== -1 && data.reminder) {
      items.value[idx] = data.reminder
    }
    return data.reminder
  }

  function reset() {
    items.value = []
    count.value = 0
    loading.value = false
  }

  return {
    items,
    count,
    loading,

    forMotorcycle,
    hasAny,

    loadPending,
    loadCount,
    dismiss,
    snooze,
    reset,
  }
})
