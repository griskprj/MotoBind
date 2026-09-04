// sw.js
const CACHE_NAME = 'motobind-v1.0.0'
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/splash.html',
  '/manifest.json',
  '/offline.html',
  '/assets/',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png',
  '/splash/',
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
      .then(cache => {
        console.log('Caching assets...')
        return cache.addAll(STATIC_ASSETS)
      })
      .then(() => self.skipWaiting())
  )
})

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(key => key !== CACHE_NAME)
          .map(key => {
            console.log('Deleting old cache:', key)
            return caches.delete(key)
          })
      ))
      .then(() => self.clients.claim())
  )
})

self.addEventListener('fetch', event => {
  const request = event.request
  const url = new URL(request.url)
  
  // Skip API and uploads
  if (url.pathname.startsWith('/api/')) return
  if (url.pathname.startsWith('/uploads/')) return
  
  // Special handling for splash page
  if (url.pathname === '/splash.html' || url.pathname === '/') {
    event.respondWith(
      caches.match(request)
        .then(cached => cached || fetch(request))
    )
    return
  }
  
  event.respondWith(
    caches.match(request)
      .then(cached => {
        if (cached) return cached
        
        return fetch(request).then(response => {
          // Cache new assets
          if (response.ok && request.method === 'GET') {
            const clone = response.clone()
            caches.open(CACHE_NAME).then(cache => {
              cache.put(request, clone)
            })
          }
          return response
        })
      })
      .catch(() => {
        if (request.headers.get('accept')?.includes('text/html')) {
          return caches.match('/offline.html')
        }
      })
  )
})