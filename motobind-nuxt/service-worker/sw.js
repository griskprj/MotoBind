import { cleanupOutdatedCaches, matchPrecache, precacheAndRoute } from 'workbox-precaching'
import { registerRoute, setCatchHandler } from 'workbox-routing'
import { NetworkOnly } from 'workbox-strategies'

cleanupOutdatedCaches()
precacheAndRoute(self.__WB_MANIFEST)

registerRoute(({ request }) => request.mode === 'navigate', new NetworkOnly())
setCatchHandler(async ({ event }) => {
  if (event.request.destination === 'document') {
    return (await matchPrecache('/offline.html')) || Response.error()
  }
  return Response.error()
})

self.addEventListener('push', (event) => {
  let payload = {}
  try {
    payload = event.data ? event.data.json() : {}
  } catch {
    payload = { body: event.data?.text() || '' }
  }

  event.waitUntil(self.registration.showNotification(payload.title || 'MotoBind', {
    body: payload.body || 'У вас новое уведомление',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/icon-192x192.png',
    data: { url: payload.url || '/notifications' },
  }))
})

self.addEventListener('notificationclick', (event) => {
  event.notification.close()
  const destination = new URL(event.notification.data?.url || '/notifications', self.location.origin)
  if (destination.origin !== self.location.origin) return

  event.waitUntil(self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clients) => {
    const existing = clients.find(client => new URL(client.url).origin === self.location.origin)
    if (existing) {
      existing.navigate(destination.href)
      return existing.focus()
    }
    return self.clients.openWindow(destination.href)
  }))
})
