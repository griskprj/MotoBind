export type Theme = 'light' | 'dark' | 'system'

const STORAGE_KEY = 'motobind-theme'

export function useTheme() {
  const themeCookie = useCookie<Theme>(STORAGE_KEY, {
    default: () => 'system',
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 365,
  })

  const resolvedTheme = ref<'light' | 'dark'>('light')

  function applyTheme(theme: Theme) {
    if (import.meta.server) return

    const root = document.documentElement
    let actual: 'light' | 'dark'

    if (theme === 'system') {
      actual = window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light'
    } else {
      actual = theme
    }

    resolvedTheme.value = actual
    root.setAttribute('data-theme', actual)
  }

  function setTheme(theme: Theme) {
    themeCookie.value = theme
    applyTheme(theme)
  }

  function toggleTheme() {
    setTheme(resolvedTheme.value === 'dark' ? 'light' : 'dark')
  }

  watch(themeCookie, (newVal) => {
    applyTheme(newVal)
  }, { immediate: true })

  onMounted(() => {
    applyTheme(themeCookie.value)

    const mq = window.matchMedia('(prefers-color-scheme: dark)')
    const handler = () => {
      if (themeCookie.value === 'system') applyTheme('system')
    }
    mq.addEventListener('change', handler)

    onBeforeUnmount(() => mq.removeEventListener('change', handler))
  })

  return {
    theme: themeCookie,
    resolvedTheme,
    setTheme,
    toggleTheme,
  }
}
