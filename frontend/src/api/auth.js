const TOKEN_KEY = 'access_token'
const REFRESH_TOKEN_KEY = 'refresh_token'
const USER_KEY = 'user'

export const AUTH_CHANGE_EVENT = 'auth-status-change'

export function getAccessToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function getRefreshToken() {
  return localStorage.getItem(REFRESH_TOKEN_KEY)
}

export function setTokens(accessToken, refreshToken) {
  localStorage.setItem(TOKEN_KEY, accessToken)
  localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken)
  window.dispatchEvent(new CustomEvent(AUTH_CHANGE_EVENT, { detail: { isAuthenticated: true } }))
}

export function setUser(user) {
  localStorage.setItem(USER_KEY, user)
}

export function removeTokens() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(REFRESH_TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
  window.dispatchEvent(new CustomEvent(AUTH_CHANGE_EVENT, { detail: { isAuthenticated: false } }))
}

export function isAuthenticated() {
  return !!getAccessToken()
}