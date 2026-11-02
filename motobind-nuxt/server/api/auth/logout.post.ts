import { clearAuthCookies } from '../../utils/auth'

export default defineEventHandler((event) => {
  clearAuthCookies(event)
  return { message: 'Вы вышли из системы' }
})
