import type { H3Event } from 'h3'

export const ACCESS_COOKIE = 'motobind_access'
export const REFRESH_COOKIE = 'motobind_refresh'

function getCookieOptions(token?: string) {
  const options: any = {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    path: '/',
  }

  if (token) {
    try {
      const payload = JSON.parse(
        Buffer.from(token.split('.')[1], 'base64url').toString()
      )
      if (typeof payload.exp === 'number') {
        options.expires = new Date(payload.exp * 1000)
      }
    } catch {}
  }
  return options
}

export function setAuthCookies(event: H3Event, accessToken: string, refreshToken?: string | null) {
  setCookie(event, ACCESS_COOKIE, accessToken, getCookieOptions(accessToken))
  if (refreshToken) {
    setCookie(event, REFRESH_COOKIE, refreshToken, getCookieOptions(refreshToken))
  } else {
    deleteCookie(event, REFRESH_COOKIE, { path: '/' })
  }
}

export function clearAuthCookies(event: H3Event) {
  deleteCookie(event, ACCESS_COOKIE, { path: '/' })
  deleteCookie(event, REFRESH_COOKIE, { path: '/' })
}

export function getAccessToken(event: H3Event) {
  return getCookie(event, ACCESS_COOKIE)
}

export function getRefreshToken(event: H3Event) {
  return getCookie(event, REFRESH_COOKIE)
}
