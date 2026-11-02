import type { ApiError } from '~/types'

export function useFormErrors() {
  const errors = ref<Record<string, string>>({})

  function setError(field: string, message: string) {
    errors.value = { ...errors.value, [field]: message }
  }

  function clearError(field: string) {
    if (!(field in errors.value)) return
    const next = { ...errors.value }
    delete next[field]
    errors.value = next
  }

  function clear() {
    errors.value = {}
  }

  /**
   * Раскладывает ApiError.fieldErrors по полям.
   */
  function setFromApiError(error: ApiError) {
    if (error.fieldErrors && Object.keys(error.fieldErrors).length > 0) {
      errors.value = { ...error.fieldErrors }
    } else if (error.message) {
      errors.value = { _form: error.message }
    }
  }

  return { errors, setError, clearError, clear, setFromApiError }
}
