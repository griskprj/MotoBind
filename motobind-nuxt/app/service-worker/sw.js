import { cleanupOutdatedCaches, matchPrecache, precacheAndRoute } from 'workbox-precaching'

precacheAndRoute(self.__WB_MANIFEST)
cleanupOutdatedCaches()

// Keep API responses and user-specific data out of the precache.
self.addEventListener('push', (event) => {
  let payload = {}

  try {
    payload = event.data ? event.data.json() : {}
  } catch {
    payload = { body: event.data ? event.data.text() : '' }
  }

  const title = payload.title || 'MotoBind'
  const options = {
    body: payload.body || payload.message || 'У вас новое уведомление',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/icon-192x192.png',
    data: {
      url: payload.url || payload.data?.url || '/',
    },
  }

  event.waitUntil(self.registration.showNotification(title, options))
})

self.addEventListener('notificationclick', (event) => {
  event.notification.close()

  const targetUrl = new URL(event.notification.data?.url || '/', self.location.origin)
  if (targetUrl.origin !== self.location.origin) {
    return
  }

  event.waitUntil((async () => {
    const windows = await self.clients.matchAll({ type: 'window', includeUncontrolled: true })
    const existing = windows.find((client) => new URL(client.url).origin === self.location.origin)

    if (existing) {
      await existing.navigate(targetUrl.href)
      return existing.focus()
    }

    return self.clients.openWindow(targetUrl.href)
  })())
})

self.addEventListener('install', (event) => {
  event.waitUntil(self.skipWaiting())
})

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim())
})

self.addEventListener('fetch', (event) => {
  if (event.request.mode !== 'navigate') return

  event.respondWith((async () => {
    try {
      return await fetch(event.request)
    } catch {
      return (await matchPrecache('/offline')) || Response.error()
    }
  })())
})
