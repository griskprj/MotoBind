import { reactive, ref } from 'vue'

export type Rule<T = any> = {
  required?: boolean
  min?: number
  max?: number
  pattern?: RegExp
  email?: boolean
  sameAs?: keyof T
  message?: string
  validator?: (value: any, form: T) => string | true
  trigger?: 'blur' | 'change' | 'submit'
}

export type Rules<T> = Partial<Record<keyof T, Rule<T>[]>>

export function useFormValidation<T extends Record<string, any>>(
  form: T,
  rules: Rules<T>,
) {
  const errors = reactive<Record<string, string>>({})
  const touched = reactive<Record<string, boolean>>({})

  function validateField(field: keyof T): boolean {
    const fieldRules = rules[field] || []
    const value = form[field]

    for (const rule of fieldRules) {
      // required
      if (rule.required) {
        const empty =
          value === null ||
          value === undefined ||
          value === '' ||
          (typeof value === 'boolean' && value === false)
        if (empty) {
          errors[field as string] = rule.message || 'Обязательное поле'
          return false
        }
      }

      // email
      if (rule.email && value) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        if (!re.test(String(value))) {
          errors[field as string] = rule.message || 'Некорректный email'
          return false
        }
      }

      // min
      if (rule.min !== undefined && value != null && value !== '') {
        if (typeof value === 'string' && value.length < rule.min) {
          errors[field as string] =
            rule.message || `Минимум ${rule.min} символов`
          return false
        }
        if (typeof value === 'number' && value < rule.min) {
          errors[field as string] = rule.message || `Минимум ${rule.min}`
          return false
        }
      }

      // max
      if (rule.max !== undefined && value != null && value !== '') {
        if (typeof value === 'string' && value.length > rule.max) {
          errors[field as string] = rule.message || `Максимум ${rule.max} символов`
          return false
        }
      }

      // pattern
      if (rule.pattern && value && !rule.pattern.test(String(value))) {
        errors[field as string] = rule.message || 'Некорректное значение'
        return false
      }

      // sameAs
      if (rule.sameAs && value !== form[rule.sameAs]) {
        errors[field as string] = rule.message || 'Значения не совпадают'
        return false
      }

      // custom validator
      if (rule.validator) {
        const result = rule.validator(value, form)
        if (result !== true) {
          errors[field as string] = result
          return false
        }
      }
    }

    delete errors[field as string]
    return true
  }

  function validateAll(): boolean {
    let ok = true
    for (const field of Object.keys(rules) as (keyof T)[]) {
      touched[field as string] = true
      if (!validateField(field)) ok = false
    }
    return ok
  }

  function touch(field: keyof T) {
    touched[field as string] = true
    validateField(field)
  }

  function reset() {
    for (const k of Object.keys(errors)) delete errors[k]
    for (const k of Object.keys(touched)) delete touched[k]
  }

  function hasError(field: keyof T) {
    return !!errors[field as string]
  }

  return {
    errors,
    touched,
    validateField,
    validateAll,
    touch,
    reset,
    hasError,
  }
}
