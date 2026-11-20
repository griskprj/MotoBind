import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import api from '../api/api'

const DEFAULT_CLIENT_FILTERS = {
  search: '',
}

export const useBusinessStore = defineStore('business', () => {
  // ===== State =====
  const account = ref(null)
  const accountLoading = ref(false)

  const clients = ref([])
  const clientsLoading = ref(false)
  const clientFilters = ref({ ...DEFAULT_CLIENT_FILTERS })

  const currentClient = ref(null)
  const currentClientLoading = ref(false)

  const myMasters = ref([])
  const myMastersLoading = ref(false)

  const mutating = ref(false)

  // ===== Getters =====
  const hasAccount = computed(() => !!account.value)
  const isMaster = computed(() => account.value?.type === 'master')
  const isStation = computed(() => account.value?.type === 'station')

  const filteredClients = computed(() => {
    const q = clientFilters.value.search.trim().toLowerCase()
    if (!q) return clients.value
    return clients.value.filter((c) =>
      c.name?.toLowerCase().includes(q) ||
      c.phone?.toLowerCase().includes(q) ||
      c.email?.toLowerCase().includes(q)
    )
  })

  // ===== Account actions =====
  async function loadAccount() {
    accountLoading.value = true
    try {
      const { data } = await api.get('/business/account/me')
      account.value = data
      return data
    } catch (err) {
      if (err.response?.status === 403 || err.response?.status === 404) {
        account.value = null
        return null
      }
      throw err
    } finally {
      accountLoading.value = false
    }
  }

  async function createAccount(payload) {
    mutating.value = true
    try {
      const { data } = await api.post('/business/account', payload)
      account.value = data
      return data
    } finally {
      mutating.value = false
    }
  }

  async function updateAccount(payload) {
    mutating.value = true
    try {
      const { data } = await api.put('/business/account/me', payload)
      account.value = data
      return data
    } finally {
      mutating.value = false
    }
  }

  async function uploadLogo(file) {
    mutating.value = true
    try {
      const fd = new FormData()
      fd.append('logo', file)
      const { data } = await api.post('/business/account/me/logo', fd, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      account.value = data
      return data
    } finally {
      mutating.value = false
    }
  }

  async function deleteLogo() {
    mutating.value = true
    try {
      const { data } = await api.delete('/business/account/me/logo')
      account.value = data
      return data
    } finally {
      mutating.value = false
    }
  }

  async function linkClient(clientId, email) {
    mutating.value = true
    try {
      const { data } = await api.post(
        `/business/clients/${clientId}/link`,
        { email }
      )
      // обновляем клиента в списке и в currentClient
      const idx = clients.value.findIndex((c) => c.id === clientId)
      if (idx !== -1) clients.value[idx] = { ...clients.value[idx], ...data }
      if (currentClient.value?.id === clientId) {
        currentClient.value = { ...currentClient.value, ...data }
      }
      return data
    } finally {
      mutating.value = false
    }
  }

  async function unlinkClient(clientId) {
    mutating.value = true
    try {
      const { data } = await api.delete(`/business/clients/${clientId}/link`)
      const idx = clients.value.findIndex((c) => c.id === clientId)
      if (idx !== -1) clients.value[idx] = { ...clients.value[idx], ...data }
      if (currentClient.value?.id === clientId) {
        currentClient.value = { ...currentClient.value, ...data }
      }
      return data
    } finally {
      mutating.value = false
    }
  }

  // ===== Clients actions =====
  async function loadClients() {
    clientsLoading.value = true
    try {
      const params = {}
      if (clientFilters.value.search) params.search = clientFilters.value.search
      const { data } = await api.get('/business/clients', { params })
      clients.value = data
      return data
    } finally {
      clientsLoading.value = false
    }
  }

  async function loadClient(clientId) {
    currentClientLoading.value = true
    try {
      const { data } = await api.get(`/business/clients/${clientId}`)
      currentClient.value = data
      return data
    } finally {
      currentClientLoading.value = false
    }
  }

  async function createClient(payload) {
    mutating.value = true
    try {
      const { data } = await api.post('/business/clients', payload)
      clients.value.unshift(data)
      return data
    } finally {
      mutating.value = false
    }
  }

  async function updateClient(clientId, payload) {
    mutating.value = true
    try {
      const { data } = await api.put(`/business/clients/${clientId}`, payload)
      const idx = clients.value.findIndex((c) => c.id === clientId)
      if (idx !== -1) clients.value[idx] = { ...clients.value[idx], ...data }
      if (currentClient.value?.id === clientId) {
        currentClient.value = { ...currentClient.value, ...data }
      }
      return data
    } finally {
      mutating.value = false
    }
  }

  async function deleteClient(clientId) {
    mutating.value = true
    try {
      await api.delete(`/business/clients/${clientId}`)
      clients.value = clients.value.filter((c) => c.id !== clientId)
      if (currentClient.value?.id === clientId) currentClient.value = null
    } finally {
      mutating.value = false
    }
  }

  async function loadMyMasters() {
    myMastersLoading.value = true
    try {
      const { data } = await api.get('/business/my-masters')
      myMasters.value = data
      return data
    } finally {
      myMastersLoading.value = false
    }
  }

  // ===== Vehicles actions =====
  async function createVehicle(clientId, payload) {
    mutating.value = true
    try {
      const { data } = await api.post(
        `/business/clients/${clientId}/vehicles`,
        payload
      )
      if (currentClient.value?.id === clientId) {
        currentClient.value.vehicles = [
          ...(currentClient.value.vehicles || []),
          data,
        ]
      }
      return data
    } finally {
      mutating.value = false
    }
  }

  async function updateVehicle(clientId, vehicleId, payload) {
    mutating.value = true
    try {
      const { data } = await api.put(
        `/business/clients/${clientId}/vehicles/${vehicleId}`,
        payload
      )
      if (currentClient.value?.id === clientId) {
        const list = currentClient.value.vehicles || []
        const idx = list.findIndex((v) => v.id === vehicleId)
        if (idx !== -1) list[idx] = data
      }
      return data
    } finally {
      mutating.value = false
    }
  }

  async function deleteVehicle(clientId, vehicleId) {
    mutating.value = true
    try {
      await api.delete(`/business/clients/${clientId}/vehicles/${vehicleId}`)
      if (currentClient.value?.id === clientId) {
        currentClient.value.vehicles = (currentClient.value.vehicles || [])
          .filter((v) => v.id !== vehicleId)
      }
    } finally {
      mutating.value = false
    }
  }

  // ===== Filters =====
  function setClientSearch(value) {
    clientFilters.value.search = value
  }

  function reset() {
    account.value = null
    clients.value = []
    currentClient.value = null
    clientFilters.value = { ...DEFAULT_CLIENT_FILTERS }
    accountLoading.value = false
    clientsLoading.value = false
    currentClientLoading.value = false
    mutating.value = false
  }

  return {
    // state
    account,
    accountLoading,
    clients,
    clientsLoading,
    clientFilters,
    currentClient,
    currentClientLoading,
    myMasters,
    myMastersLoading,
    mutating,

    // getters
    hasAccount,
    isMaster,
    isStation,
    filteredClients,

    // account
    loadAccount,
    createAccount,
    updateAccount,
    uploadLogo,
    deleteLogo,

    // clients
    loadClients,
    loadClient,
    createClient,
    updateClient,
    deleteClient,
    linkClient,
    unlinkClient,
    loadMyMasters,

    // vehicles
    createVehicle,
    updateVehicle,
    deleteVehicle,

    // filters
    setClientSearch,

    reset,
  }
})
