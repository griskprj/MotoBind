import { createRouter, createWebHistory } from 'vue-router'
import { setupAuthGuards, setupMetaUpdates } from './guards'

import authRoutes from './routes/auth'
import documentsRoutes from './routes/documents'
import adminRoutes from './routes/admin'
import mainRoutes from './routes/main'

const routes = [
  ...mainRoutes,
  ...authRoutes,
  ...documentsRoutes,
  ...adminRoutes,
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0 }
  },
  routes,
})

setupAuthGuards(router)
setupMetaUpdates(router)

export default router