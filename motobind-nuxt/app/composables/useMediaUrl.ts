/**
 * Превращает относительный путь из бэка (`user_moto/1_photo.webp`)
 * в URL, который отдаёт Nuxt-прокси `/api/uploads/<path>`.
 */
export function useMediaUrl() {
  return (path: string | null | undefined): string | null => {
    if (!path) return null
    if (/^https?:\/\//.test(path)) return path
    return `/api/uploads/${path.replace(/^\/+/, '')}`
  }
}
