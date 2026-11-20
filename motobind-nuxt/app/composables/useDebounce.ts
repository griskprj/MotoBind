export function useDebounce<T>(value: Ref<T>, delay = 500): Ref<T> {
  const debounced = ref(value.value) as Ref<T>
  let timeout: ReturnType<typeof setTimeout> | null = null

  watch(value, (newVal) => {
    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(() => {
      debounced.value = newVal
    }, delay)
  })

  onBeforeUnmount(() => {
    if (timeout) clearTimeout(timeout)
  })

  return debounced
}
