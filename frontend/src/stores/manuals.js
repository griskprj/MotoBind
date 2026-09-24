import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import api from '../api/api'

const DEFAULT_FILTERS = {
  search: '',
  motorcycle: '',
  category: '',
  sort_by: 'created_at_desc',
}

const DEFAULT_PAGINATION = {
  current_page: 1,
  per_page: 6,
  total: 0,
  pages: 0,
  has_prev: false,
  has_next: false,
}

export const useManualsStore = defineStore('manuals', () => {
  // ===== State =====
  const items = ref([])
  const current = ref(null)
  const loading = ref(false)
  const loadingCurrent = ref(false)

  const filters = ref({ ...DEFAULT_FILTERS })
  const tab = ref('all') // 'all' | 'my' | 'myMotos'
  const pagination = ref({ ...DEFAULT_PAGINATION })

  // ===== Getters =====
  const hasActiveFilters = computed(
    () => !!filters.value.search || !!filters.value.motorcycle || !!filters.value.category
  )

  const totalPages = computed(() => pagination.value.pages)

  const visiblePages = computed(() => {
    const current = pagination.value.current_page
    const total = pagination.value.pages
    const delta = 2
    const range = []

    for (let i = Math.max(2, current - delta); i <= Math.min(total - 1, current + delta); i++) {
      range.push(i)
    }

    if (current - delta > 2) range.unshift('...')
    if (current + delta < total - 1) range.push('...')

    range.unshift(1)
    if (total > 1) range.push(total)

    return range.filter((v, i, a) => a.indexOf(v) === i)
  })

  // ===== Actions =====

  async function loadList() {
    loading.value = true
    try {
      const params = {
        page: pagination.value.current_page,
        per_page: pagination.value.per_page,
        tab: tab.value,
        ...filters.value,
      }

      Object.keys(params).forEach((k) => {
        if (!params[k]) delete params[k]
      })

      const { data } = await api.get('/manual/list', { params })

      items.value = data.manuals || []
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

  async function loadOne(id) {
    loadingCurrent.value = true
    try {
      const { data } = await api.get(`/manual/${id}`)
      current.value = data
      return data
    } finally {
      loadingCurrent.value = false
    }
  }

  function setFilter(key, value) {
    if (key in filters.value) {
      filters.value[key] = value
      pagination.value.current_page = 1
    }
  }

  function setTab(value) {
    tab.value = value
    pagination.value.current_page = 1
  }

  function setSortBy(value) {
    filters.value.sort_by = value
    pagination.value.current_page = 1
  }

  function setPage(page) {
    if (page < 1 || page > pagination.value.pages) return
    pagination.value.current_page = page
  }

  function setPerPage(n) {
    pagination.value.per_page = n
    pagination.value.current_page = 1
  }

  function clearFilters() {
    filters.value = { ...DEFAULT_FILTERS }
    pagination.value.current_page = 1
  }

  function clearAll() {
    filters.value = { ...DEFAULT_FILTERS }
    tab.value = 'all'
    pagination.value.current_page = 1
  }

  async function remove(id) {
    await api.delete(`/manual/${id}`)
    items.value = items.value.filter((m) => m.id !== id)
    pagination.value.total = Math.max(0, pagination.value.total - 1)
  }

  async function create(payload, files = {}) {
    const formData = new FormData()
    formData.append('data', JSON.stringify(payload))

    Object.entries(files).forEach(([key, file]) => {
      if (file) formData.append(key, file)
    })

    const { data } = await api.post('/manual/new-manual', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    items.value.unshift(data)
    pagination.value.total += 1
    return data
  }

  async function update(id, payload) {
    const { data } = await api.put(`/manual/${id}`, payload)

    const idx = items.value.findIndex((m) => m.id === id)
    if (idx !== -1) items.value[idx] = data

    if (current.value?.id === id) {
      current.value = data
    }

    return data
  }

  async function uploadStepImage(manualId, stepId, file) {
    const formData = new FormData()
    formData.append('image', file)
    const { data } = await api.post(
      `/manual/${manualId}/steps/${stepId}/image`,
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    )
    return data.image_url
  }

  async function deleteStepImage(manualId, stepId) {
    await api.delete(`/manual/${manualId}/steps/${stepId}/image`)
  }

  async function loadForMaintenance(maintenanceId, motoId) {
    const { data } = await api.get('/manual/', {
      params: {
        maintenance_id: maintenanceId,
        moto_id: motoId,
      },
    })

    if (!data) return null
    if (Array.isArray(data)) return data.length > 0 ? data[0] : null
    if (data.id) return data
    return null
  }

  function reset() {
    items.value = []
    current.value = null
    loading.value = false
    loadingCurrent.value = false
    filters.value = { ...DEFAULT_FILTERS }
    tab.value = 'all'
    pagination.value = { ...DEFAULT_PAGINATION }
  }

  return {
    items,
    current,
    loading,
    loadingCurrent,
    filters,
    tab,
    pagination,

    hasActiveFilters,
    totalPages,
    visiblePages,

    loadList,
    loadOne,
    setFilter,
    setTab,
    setSortBy,
    setPage,
    setPerPage,
    clearFilters,
    clearAll,
    remove,
    update,
    uploadStepImage,
    deleteStepImage,
    loadForMaintenance,
    reset,
    create,
  }
})
