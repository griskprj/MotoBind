import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

export const useModalsStore = defineStore('modals', () => {
  // ===== State =====
  const stack = ref([])

  // ===== Getters =====
  const current = computed(() => stack.value[stack.value.length - 1] || null)
  const isOpen = computed(() => (name) => stack.value.some((m) => m.name === name))

  // ===== Actions =====
  function open(name, props = {}) {
    const existing = stack.value.find((m) => m.name === name)
    if (existing) {
      existing.props = props
      return
    }
    stack.value.push({ name, props })
  }

  function close(name = null) {
    if (name) {
      stack.value = stack.value.filter((m) => m.name !== name)
    } else {
      stack.value.pop()
    }
  }

  function closeAll() {
    stack.value = []
  }

  return {
    stack,

    current,
    isOpen,

    open,
    close,
    closeAll,
  }
})
