import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import api from '../api/api'

export const useBookingsStore = defineStore('bookings', () => {
  // ===== State =====
  const myBookings = ref([])
  const masterBookings = ref([])
  const currentBooking = ref(null)

  const loadingMine = ref(false)
  const loadingMaster = ref(false)
  const loadingDetail = ref(false)
  const mutating = ref(false)

  // ===== Getters (client) =====
  const myCounts = computed(() => {
    const m = { all: myBookings.value.length }
    for (const b of myBookings.value) {
      m[b.status] = (m[b.status] || 0) + 1
    }
    return m
  })

  // ===== Getters (master) =====
  const masterCounts = computed(() => {
    const m = { all: masterBookings.value.length }
    for (const b of masterBookings.value) {
      m[b.status] = (m[b.status] || 0) + 1
    }
    return m
  })

  // ===== Client actions =====
  async function loadMyBookings(status = null) {
    loadingMine.value = true
    try {
      const params = status ? { status } : {}
      const { data } = await api.get('/bookings/my', { params })
      myBookings.value = data
      return data
    } finally {
      loadingMine.value = false
    }
  }

  async function loadBooking(id, scope = 'client') {
    loadingDetail.value = true
    try {
      const url = scope === 'master'
        ? `/business/bookings/${id}`
        : `/bookings/${id}`
      const { data } = await api.get(url)
      currentBooking.value = data
      return data
    } finally {
      loadingDetail.value = false
    }
  }

  async function createBooking(payload) {
    mutating.value = true
    try {
      const { data } = await api.post('/bookings/', payload)
      myBookings.value.unshift(data)
      return data
    } finally {
      mutating.value = false
    }
  }

  async function cancelBooking(id, reason) {
    mutating.value = true
    try {
      const { data } = await api.post(`/bookings/${id}/cancel`, { reason })
      _replaceInList(myBookings, data)
      if (currentBooking.value?.id === id) currentBooking.value = data
      return data
    } finally {
      mutating.value = false
    }
  }

  // ===== Master actions =====
  async function loadMasterBookings(status = null) {
    loadingMaster.value = true
    try {
      const params = status ? { status } : {}
      const { data } = await api.get('/business/bookings', { params })
      masterBookings.value = data
      return data
    } finally {
      loadingMaster.value = false
    }
  }

  async function confirmBooking(id) {
    return _masterAction(id, 'confirm')
  }
  async function declineBooking(id, reason) {
    return _masterAction(id, 'decline', { reason })
  }
  async function startBooking(id) {
    return _masterAction(id, 'start')
  }
  async function rescheduleBooking(id, scheduledAt) {
    return _masterAction(id, 'reschedule', { scheduled_at: scheduledAt })
  }
  async function completeBooking(id, { priceFinal, masterNote } = {}) {
    return _masterAction(id, 'complete', {
      price_final: priceFinal,
      master_note: masterNote,
    })
  }

  // ===== Internals =====
  async function _masterAction(id, action, body = {}) {
    mutating.value = true
    try {
      const { data } = await api.post(
        `/business/bookings/${id}/${action}`,
        body,
      )
      _replaceInList(masterBookings, data)
      if (currentBooking.value?.id === id) currentBooking.value = data
      return data
    } finally {
      mutating.value = false
    }
  }

  function _replaceInList(listRef, data) {
    const idx = listRef.value.findIndex((b) => b.id === data.id)
    if (idx !== -1) listRef.value[idx] = data
  }

  function reset() {
    myBookings.value = []
    masterBookings.value = []
    currentBooking.value = null
    loadingMine.value = false
    loadingMaster.value = false
    loadingDetail.value = false
    mutating.value = false
  }

  return {
    myBookings,
    masterBookings,
    currentBooking,

    loadingMine,
    loadingMaster,
    loadingDetail,
    mutating,

    myCounts,
    masterCounts,

    loadMyBookings,
    loadBooking,
    createBooking,
    cancelBooking,

    loadMasterBookings,
    confirmBooking,
    declineBooking,
    startBooking,
    rescheduleBooking,
    completeBooking,

    reset,
  }
})
