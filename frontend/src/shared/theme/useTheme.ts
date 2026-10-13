import { ref, watch } from 'vue'

const STORAGE_KEY = 'theme'

type Theme = 'dark' | 'light'

const isDark = ref<boolean>(getInitialTheme() === 'dark')

function getInitialTheme(): Theme {
  const saved = localStorage.getItem(STORAGE_KEY) as Theme | null
  if (saved === 'dark' || saved === 'light') return saved

  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  return prefersDark ? 'dark' : 'light'
}

function applyTheme(theme: Theme) {
  document.documentElement.setAttribute('data-theme', theme)
}

applyTheme(isDark.value ? 'dark' : 'light')

watch(isDark, (val) => {
  const theme: Theme = val ? 'dark' : 'light'
  applyTheme(theme)
  localStorage.setItem(STORAGE_KEY, theme)
})

export function useTheme() {
  function toggle() {
    isDark.value = !isDark.value
  }

  function set(theme: Theme) {
    isDark.value = theme === 'dark'
  }

  return { isDark, toggle, set }
}
