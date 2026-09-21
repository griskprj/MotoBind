import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import api from '../api/api'

export const useMotorcyclesStore = defineStore('motorcycles', () => {
  // ===== State =====
  const items = ref([])
  const selectedId = ref(null)
  const loading = ref(false)
  const mutatingId = ref(null)

  // ===== Getters =====
  const hasMotorcycles = computed(() => items.value.length > 0)
  const count = computed(() => items.value.length)

  const selected = computed(
    () => items.value.find((m) => m.id === selectedId.value) || null
  )

  /** Все обслуживания по всем мотоциклам */
  const allMaintenances = computed(() =>
    items.value.flatMap((m) => m.maintenances || [])
  )

  const totalMaintenances = computed(() => allMaintenances.value.length)

  const totalCosts = computed(() =>
    allMaintenances.value
      .filter((m) => m.status === 'completed')
      .reduce((sum, m) => sum + (m.cost || 0), 0)
  )

  /** Обслуживания выбранного мотоцикла, отсортированные */
  const selectedMaintenances = computed(() => {
    if (!selected.value?.maintenances) return []
    return [...selected.value.maintenances].sort((a, b) => {
      const da = a.completed_date || a.planned_date || a.created_at
      const db = b.completed_date || b.planned_date || b.created_at
      return new Date(db) - new Date(da)
    })
  })

  const recentMaintenances = computed(() => selectedMaintenances.value.slice(0, 5))

  /** Следующее ТО для выбранного мотоцикла (просроченное или ближайшее) */
  const nextMaintenance = computed(() => {
    if (!selected.value?.maintenances) return null
    const current = selected.value.mileage || 0
    const planned = selected.value.maintenances
      .filter((m) => m.status === 'planned' && m.planned_mileage)
      .sort((a, b) => a.planned_mileage - b.planned_mileage)

    const overdue = planned.filter((m) => m.planned_mileage <= current)
    const upcoming = planned.filter((m) => m.planned_mileage > current)

    if (overdue.length > 0) {
      const item = overdue[0]
      return {
        ...item,
        isOverdue: true,
        distanceOverdue: current - item.planned_mileage,
      }
    }
    if (upcoming.length > 0) {
      const item = upcoming[0]
      return {
        ...item,
        isOverdue: false,
        distanceToNext: item.planned_mileage - current,
      }
    }
    return null
  })

  const maintenanceSpends = computed(() => {
    if (!selected.value?.maintenances) return 0
    return selected.value.maintenances
      .filter((m) => m.status === 'completed')
      .reduce((sum, m) => sum + (m.cost || 0), 0)
  })

  // ===== Actions =====

  /**
   * Загружает все мотоциклы. Обслуживания догружает параллельно.
   */
  async function loadAll() {
    loading.value = true
    try {
      const { data: motos } = await api.get('/motorcycle/', { cache: 30_000 })
      items.value = motos

      if (items.value.length > 0) {
        const exists = items.value.some((m) => m.id === selectedId.value)
        if (!exists) selectedId.value = items.value[0].id
      } else {
        selectedId.value = null
      }

      return items.value
    } finally {
      loading.value = false
    }
  }

  function select(id) {
    if (id && !items.value.some((m) => m.id === id)) return
    selectedId.value = id
  }

  function selectFirst() {
    selectedId.value = items.value[0]?.id || null
  }

  async function create(data, photoFile = null) {
    const { data: moto } = await api.post('/motorcycle/', data)

    if (photoFile) {
      const fd = new FormData()
      fd.append('photo', photoFile)
      const { data: updated } = await api.post(`/motorcycle/${moto.id}/photo`, fd, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      items.value.push(updated)
      selectedId.value = updated.id
      return updated
    }

    items.value.push(moto)
    selectedId.value = moto.id
    return moto
  }

  async function update(id, data, { newPhotoFile = null, deleteExistingPhoto = false } = {}) {
    mutatingId.value = id
    try {
      await api.put(`/motorcycle/${id}`, data)

      if (deleteExistingPhoto) {
        await api.delete(`/motorcycle/${id}/photo`)
      }

      if (newPhotoFile) {
        const fd = new FormData()
        fd.append('photo', newPhotoFile)
        await api.post(`/motorcycle/${id}/photo`, fd, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })
      }

      return await refreshOne(id)
    } finally {
      mutatingId.value = null
    }
  }

  async function updateMileage(id, mileage) {
    await api.patch(`/motorcycle/${id}`, { mileage })
    return await refreshOne(id)
  }

  async function updateNote(id, note) {
    await api.patch(`/motorcycle/${id}/note`, { note })
    return await refreshOne(id)
  }

  async function uploadPhoto(id, file) {
    const fd = new FormData()
    fd.append('photo', file)
    const { data } = await api.post(`/motorcycle/${id}/photo`, fd, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    const idx = items.value.findIndex((m) => m.id === data.id)
    if (idx !== -1) items.value[idx] = data
    return data
  }

  async function deletePhoto(id) {
    const { data } = await api.delete(`/motorcycle/${id}/photo`)
    const idx = items.value.findIndex((m) => m.id === data.id)
    if (idx !== -1) items.value[idx] = data
    return data
  }

  async function remove(id) {
    await api.delete(`/motorcycle/${id}`)
    items.value = items.value.filter((m) => m.id !== id)
    if (selectedId.value === id) {
      selectedId.value = items.value[0]?.id || null
    }
  }

  /**
   * Перезагружает один мотоцикл с его обслуживаниями.
   */
  async function refreshOne(id) {
    const [motoRes, maintRes] = await Promise.all([
      api.get(`/motorcycle/${id}`),
      api.get(`/maintenance/motorcycle/${id}`).catch(() => ({ data: [] })),
    ])
    const moto = motoRes.data
    moto.maintenances = maintRes.data || []
    const idx = items.value.findIndex((m) => m.id === id)
    if (idx !== -1) items.value[idx] = moto
    return moto
  }

  function reset() {
    items.value = []
    selectedId.value = null
    loading.value = false
    mutatingId.value = null
  }

  return {
    items,
    selectedId,
    loading,
    mutatingId,

    hasMotorcycles,
    count,
    selected,
    allMaintenances,
    totalMaintenances,
    totalCosts,
    selectedMaintenances,
    recentMaintenances,
    nextMaintenance,
    maintenanceSpends,

    loadAll,
    select,
    selectFirst,
    create,
    update,
    updateMileage,
    updateNote,
    uploadPhoto,
    deletePhoto,
    remove,
    refreshOne,
    reset,
  }
})
