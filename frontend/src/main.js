import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'
import '/src/style.scss'
import VueApexCharts from 'vue3-apexcharts'

const app = createApp(App)

app.use(router)
app.use(VueApexCharts)
app.mount('#app')

if ('serviceWorker' in navigator && import.meta.env.PROD) {
  window.addEventListener('load', () => {
    navigator.serviceWorker
      .register('/sw.js')
      .then(reg => console.log('[SW] Зарегистрирован:', reg))
      .catch(err => console.error('[SW] Ошибка:', err))
  })
}