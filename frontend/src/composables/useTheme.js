import { computed, ref, watch } from 'vue'

const STORAGE_KEY = 'motobind-theme'

function getInitialTheme() {
  if (typeof window === 'undefined') return 'light'

  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved === 'light' || saved === 'dark') return saved
  } catch {
    /* ignore */
  }

  if (window.matchMedia?.('(prefers-color-scheme: dark)').matches) {
    return 'dark'
  }
  return 'light'
}

const theme = ref(getInitialTheme())

function applyTheme(value) {
  if (typeof document === 'undefined') return
  document.documentElement.setAttribute('data-theme', value)
}

applyTheme(theme.value)

watch(
  theme,
  (value) => {
    applyTheme(value)
    try {
      localStorage.setItem(STORAGE_KEY, value)
    } catch {
      /* ignore */
    }
  },
  { flush: 'sync' }
)

export function useTheme() {
  const isDark = computed(() => theme.value === 'dark')

  function setTheme(value) {
    if (value === 'light' || value === 'dark') {
      theme.value = value
    }
  }

  function toggle() {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
  }

  return {
    theme,
    isDark,
    setTheme,
    toggle,
  }
}
