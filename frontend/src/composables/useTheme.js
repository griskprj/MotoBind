import { ref, watch } from 'vue'

const STORAGE_KEY = 'theme'
const isDark = ref(document.documentElement.dataset.theme === 'dark')

watch(
  isDark,
  (dark) => {
    document.documentElement.dataset.theme = dark ? 'dark' : 'light'
    localStorage.setItem(STORAGE_KEY, dark ? 'dark' : 'light')
  },
  { immediate: true }
)

const saved = localStorage.getItem(STORAGE_KEY)
if (saved === 'dark' || saved === 'light') {
  isDark.value = saved === 'dark'
} else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
  isDark.value = true
}

export function useTheme() {
  function toggle() {
    isDark.value = !isDark.value
  }

  return { isDark, toggle }
}
