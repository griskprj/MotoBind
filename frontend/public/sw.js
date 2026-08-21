// sw.js
const CACHE_NAME = 'motobind-v1.0.0'
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/assets/',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png',
  '/16x9Auth-Bg.webp',
  '/9x16Auth-Bg.webp',
  '/BaseAvatar.jpg',
  '/MotoLandingHero.webp',
  '/ManualImgDefault.webp',
  '/moto_default.jpg'
]

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(STATIC_ASSETS))
      .then(() => self.skipWaiting())
  )
})

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(key => key !== CACHE_NAME)
          .map(key => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  )
})

self.addEventListener('fetch', event => {
  const request = event.request
  
  if (request.url.includes('/api/')) return
  if (request.url.includes('/uploads/')) return
  
  event.respondWith(
    caches.match(request)
      .then(cached => cached || fetch(request))
      .catch(() => {
        if (request.headers.get('accept').includes('text/html')) {
          return caches.match('/offline.html')
        }
      })
  )
})