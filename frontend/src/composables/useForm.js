import { computed, reactive, ref } from 'vue'

/**
 * Composable для форм.
 *
 * Использование:
 *   const { values, errors, loading, isValid, setErrors, reset, submit } = useForm({
 *     initial: { email: '', password: '' },
 *     validate: (v) => {
 *       const errs = {}
 *       if (!v.email) errs.email = 'Обязательное поле'
 *       if (v.password.length < 6) errs.password = 'Минимум 6 символов'
 *       return errs
 *     },
 *     onSubmit: async (v) => { await api.post('/login', v) },
 *     onSuccess: () => { router.push('/garage') },
 *   })
 */

export function useForm({ initial = {}, validate = null, onSubmit, onSuccess, onError } = {}) {
  const values = reactive({ ...initial })
  const errors = ref({})
  const loading = ref(false)
  const touched = ref(false)

  const isValid = computed(() => {
    if (!validate) return true
    return Object.keys(validate(values)).length === 0
  })

  const hasErrors = computed(() => Object.keys(errors.value).length > 0)

  function setErrors(newErrors) {
    errors.value = newErrors || {}
  }

  function clearErrors() {
    errors.value = {}
  }

  function reset(newInitial = null) {
    const source = newInitial || initial
    Object.keys(values).forEach((key) => {
      delete values[key]
    })
    Object.assign(values, { ...source })
    errors.value = {}
    touched.value = false
    loading.value = false
  }

  function validateNow() {
    if (!validate) return true
    const errs = validate(values)
    errors.value = errs
    return Object.keys(errs).length === 0
  }

  async function submit() {
    touched.value = true

    if (!validateNow()) {
      return { ok: false, errors: errors.value }
    }

    loading.value = true
    try {
      const result = await onSubmit?.(values)
      await onSuccess?.(result)
      return { ok: true, data: result }
    } catch (err) {
      // Извлекаем ошибки валидации от бэкенда (Pydantic 422)
      const backendErrors = err?.response?.data?.errors
      if (backendErrors && typeof backendErrors === 'object') {
        errors.value = backendErrors
      } else {
        const message = err?.response?.data?.message || err?.message || 'Ошибка'
        errors.value = { _global: message }
      }
      await onError?.(err)
      return { ok: false, error: err }
    } finally {
      loading.value = false
    }
  }

  return {
    values,
    errors,
    loading,
    touched,
    isValid,
    hasErrors,
    setErrors,
    clearErrors,
    reset,
    validateNow,
    submit,
  }
}
