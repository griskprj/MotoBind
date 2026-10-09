import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import api from '../api/api'

export const useServicesStore = defineStore('services', () => {
  // ===== State =====
  const myServices = ref([])
  const loading = ref(false)
  const mutating = ref(false)

  const publicServices = ref([])
  const publicLoading = ref(false)

  // ===== Getters =====
  const grouped = computed(() => {
    const map = {
      pending: [],
      approved: [],
      rejected: [],
    }
    for (const s of myServices.value) {
      if (map[s.status]) map[s.status].push(s)
    }
    return map
  })

  const counts = computed(() => ({
    all: myServices.value.length,
    pending: grouped.value.pending.length,
    approved: grouped.value.approved.length,
    rejected: grouped.value.rejected.length,
  }))

  // ===== Actions =====
  async function loadMine() {
    loading.value = true
    try {
      const { data } = await api.get('/services/')
      myServices.value = data
      return data
    } finally {
      loading.value = false
    }
  }

  async function create(payload) {
    mutating.value = true
    try {
      const { data } = await api.post('/services/', payload)
      myServices.value.unshift(data)
      return data
    } finally {
      mutating.value = false
    }
  }

  async function update(id, payload) {
    mutating.value = true
    try {
      const { data } = await api.put(`/services/${id}`, payload)
      const idx = myServices.value.findIndex((s) => s.id === id)
      if (idx !== -1) myServices.value[idx] = data
      return data
    } finally {
      mutating.value = false
    }
  }

  async function remove(id) {
    mutating.value = true
    try {
      await api.delete(`/services/${id}`)
      myServices.value = myServices.value.filter((s) => s.id !== id)
    } finally {
      mutating.value = false
    }
  }

  async function loadPublic(slug) {
    publicLoading.value = true
    try {
      const { data } = await api.get(`/services/public/${slug}`)
      publicServices.value = data
      return data
    } finally {
      publicLoading.value = false
    }
  }

  function reset() {
    myServices.value = []
    publicServices.value = []
    loading.value = false
    publicLoading.value = false
    mutating.value = false
  }

  return {
    myServices,
    loading,
    mutating,
    publicServices,
    publicLoading,

    grouped,
    counts,

    loadMine,
    create,
    update,
    remove,
    loadPublic,
    reset,
  }
})
