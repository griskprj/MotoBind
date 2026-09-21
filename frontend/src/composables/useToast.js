import { ref } from 'vue'

/**
 * Глобальный toast-сервис.
 *
 * Использование:
 *   const toast = useToast()
 *   toast.success('Сохранено')
 *   toast.error('Не удалось загрузить')
 */

const toasts = ref([])
let uid = 0

const DEFAULT_DURATION = 4000

function push(message, variant = 'info', options = {}) {
  uid += 1
  const id = uid
  const toast = {
    id,
    message,
    variant, // 'info' | 'success' | 'warning' | 'error'
    duration: options.duration ?? DEFAULT_DURATION,
    dismissible: options.dismissible ?? true,
  }
  toasts.value.push(toast)

  if (toast.duration > 0) {
    setTimeout(() => {
      remove(id)
    }, toast.duration)
  }

  return id
}

function remove(id) {
  const idx = toasts.value.findIndex((t) => t.id === id)
  if (idx !== -1) {
    toasts.value.splice(idx, 1)
  }
}

function clear() {
  toasts.value = []
}

export function useToast() {
  return {
    toasts,

    info: (msg, opts) => push(msg, 'info', opts),
    success: (msg, opts) => push(msg, 'success', opts),
    warning: (msg, opts) => push(msg, 'warning', opts),
    error: (msg, opts) => push(msg, 'error', opts),

    remove,
    clear,
  }
}
