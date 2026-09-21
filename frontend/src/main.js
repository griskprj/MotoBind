import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router/index.js'
import './styles/index.scss'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.mount('#app')

import { useToast } from './composables/useToast'
if (import.meta.env.DEV) {
  window.__toast = useToast
}

if ('serviceWorker' in navigator && import.meta.env.PROD) {
  window.addEventListener('load', () => {
    navigator.serviceWorker
      .register('/sw.js')
      .then(reg => console.log('[SW] Зарегистрирован:', reg))
      .catch(err => console.error('[SW] Ошибка:', err))
  })
}
