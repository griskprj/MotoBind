export type ToastVariant = 'success' | 'error' | 'info' | 'warning'

export interface Toast {
  id: number
  variant: ToastVariant
  message: string
  timeout: number
}

// Глобальный стейт — module-level
const toasts = ref<Toast[]>([])
let nextId = 1

export function useToast() {
  function push(variant: ToastVariant, message: string, timeout = 4000) {
    const id = nextId++
    toasts.value = [...toasts.value, { id, variant, message, timeout }]
    if (timeout > 0 && import.meta.client) {
      setTimeout(() => dismiss(id), timeout)
    }
    return id
  }

  function dismiss(id: number) {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }

  return {
    toasts: readonly(toasts),
    success: (msg: string, timeout?: number) => push('success', msg, timeout),
    error: (msg: string, timeout?: number) => push('error', msg, timeout),
    info: (msg: string, timeout?: number) => push('info', msg, timeout),
    warning: (msg: string, timeout?: number) => push('warning', msg, timeout),
    dismiss,
  }
}
