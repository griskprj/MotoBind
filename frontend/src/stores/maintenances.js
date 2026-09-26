import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import api from '../api/api'

const DEFAULT_FILTERS = {
  search: '',
  motorcycle: '',
  status: '',
}

export const useMaintenancesStore = defineStore('maintenances', () => {
  // ===== State =====
  const all = ref([])
  const motorcycles = ref([])
  const allCount = ref(0)
  const loading = ref(false)

  const filters = ref({ ...DEFAULT_FILTERS })
  const tab = ref('all') // 'all' | 'planned' | 'history'
  const sortBy = ref('date_desc')

  // ===== Getters =====
  const completed = computed(() => all.value.filter((m) => m.status === 'completed'))
  const planned = computed(() => all.value.filter((m) => m.status === 'planned'))
  const overdue = computed(() => all.value.filter((m) => m.status === 'overdue'))

  const counts = computed(() => ({
    all: allCount.value || all.value.length,
    planned: planned.value.length + overdue.value.length,
    history: completed.value.length,
  }))

  const hasActiveFilters = computed(
    () =>
      !!filters.value.search ||
      !!filters.value.motorcycle ||
      !!filters.value.status ||
      tab.value !== 'all'
  )

  const filtered = computed(() => {
    let list = [...all.value]

    const q = filters.value.search.trim().toLowerCase()
    if (q) {
      list = list.filter(
        (m) =>
          m.title?.toLowerCase().includes(q) ||
          m.description?.toLowerCase().includes(q) ||
          m.moto_name?.toLowerCase().includes(q)
      )
    }

    if (tab.value === 'planned') {
      list = list.filter((m) => m.status === 'planned' || m.status === 'overdue')
    } else if (tab.value === 'history') {
      list = list.filter((m) => m.status === 'completed')
    }

    if (filters.value.motorcycle) {
      list = list.filter((m) => m.moto_id === filters.value.motorcycle)
    }
    if (filters.value.status) {
      list = list.filter((m) => m.status === filters.value.status)
    }

    list = sortItems(list, sortBy.value)

    return list
  })

  // ===== Actions =====

  /**
   * Загружает все обслуживания одним запросом (через statistic endpoint).
   */
  async function loadAll() {
    loading.value = true
    try {
      const { data } = await api.get('/statistic/maintenance')
      motorcycles.value = data.motorcycles || []
      const history = data.history_maintenances || []
      const plannedList = data.planned_maintenances || []
      all.value = [...history, ...plannedList]
      allCount.value = data.all_maintenances_count || all.value.length
      return all.value
    } finally {
      loading.value = false
    }
  }

  function setFilter(key, value) {
    if (key in filters.value) {
      filters.value[key] = value
    }
  }

  function setTab(value) {
    tab.value = value
  }

  function setSortBy(value) {
    sortBy.value = value
  }

  function clearFilters() {
    filters.value = { ...DEFAULT_FILTERS }
    tab.value = 'all'
    sortBy.value = 'date_desc'
  }

  async function create(data) {
    const { data: created } = await api.post('/maintenance/', data)
    all.value.unshift(created)
    return created
  }

  async function update(id, data) {
    const { data: updated } = await api.put(`/maintenance/${id}`, data)
    const idx = all.value.findIndex((m) => m.id === id)
    if (idx !== -1) all.value[idx] = updated
    return updated
  }

  async function remove(id) {
    await api.delete(`/maintenance/${id}`)
    all.value = all.value.filter((m) => m.id !== id)
  }

  async function complete(id, payload) {
    await api.post(`/maintenance/${id}/complete`, payload)
    await loadAll()
  }

  async function loadForRepair() {
    loading.value = true
    try {
      const { data } = await api.get('/statistic/repair')
      return {
        motorcycles: data.motorcycles || [],
        maintenances: data.maintenances || [],
      }
    } finally {
      loading.value = false
    }
  }

  function reset() {
    all.value = []
    motorcycles.value = []
    allCount.value = 0
    filters.value = { ...DEFAULT_FILTERS }
    tab.value = 'all'
    sortBy.value = 'date_desc'
    loading.value = false
  }

  return {
    all,
    motorcycles,
    allCount,
    loading,
    filters,
    tab,
    sortBy,

    completed,
    planned,
    overdue,
    counts,
    filtered,
    hasActiveFilters,

    loadAll,
    setFilter,
    setTab,
    setSortBy,
    clearFilters,
    create,
    update,
    remove,
    complete,
    loadForRepair,
    reset,
  }
})

// ===== Helpers =====
function sortItems(items, sortBy) {
  const sorters = {
    date_desc: (a, b) =>
      new Date(b.completed_date || b.planned_date || b.created_at) -
      new Date(a.completed_date || a.planned_date || a.created_at),
    date_asc: (a, b) =>
      new Date(a.completed_date || a.planned_date || a.created_at) -
      new Date(b.completed_date || b.planned_date || b.created_at),
    mileage_desc: (a, b) =>
      (b.completed_mileage || b.planned_mileage || 0) -
      (a.completed_mileage || a.planned_mileage || 0),
    mileage_asc: (a, b) =>
      (a.completed_mileage || a.planned_mileage || 0) -
      (b.completed_mileage || b.planned_mileage || 0),
    cost_desc: (a, b) => (b.cost || 0) - (a.cost || 0),
    cost_asc: (a, b) => (a.cost || 0) - (b.cost || 0),
  }
  return [...items].sort(sorters[sortBy] || sorters.date_desc)
}
