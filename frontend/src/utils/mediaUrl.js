const API_URL = import.meta.env.VITE_API_URL || ''

export function getUploadUrl(path) {
  if (!path) return null
  if (typeof path !== 'string') return null
  if (path.startsWith('http://') || path.startsWith('https://')) return path
  if (path.startsWith('data:')) return path
  if (path.startsWith('/')) return path
  return `${API_URL}/uploads/${path}`
}

export function getMotoPhotoUrl(path) {
  return getUploadUrl(path)
}

export function getAvatarUrl(path) {
  return getUploadUrl(path) || '/BaseAvatar.webp'
}

export function getManualImageUrl(path) {
  return getUploadUrl(path) || '/ManualImgDefault.webp'
}
