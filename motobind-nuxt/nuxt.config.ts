import { validateDiagnosticRuleData } from './app/utils/constants/diagnosticsRules'

const diagnosticRuleIssues = validateDiagnosticRuleData()
const diagnosticRuleErrors = diagnosticRuleIssues.filter(issue => issue.severity === 'error')
const diagnosticRuleWarnings = diagnosticRuleIssues.filter(issue => issue.severity === 'warning')

if (diagnosticRuleErrors.length) {
  throw new Error(`Некорректная база диагностики:\n${diagnosticRuleErrors.map(issue => `- [${issue.code}] ${issue.message}`).join('\n')}`)
}
if (diagnosticRuleWarnings.length) {
  console.warn(`Покрытие базы диагностики:\n${diagnosticRuleWarnings.map(issue => `- [${issue.code}] ${issue.message}`).join('\n')}`)
}

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',

  devtools: {
    enabled: true
  },

  modules: [
    '@pinia/nuxt',
    '@nuxtjs/seo',
    '@nuxt/image',
    '@vite-pwa/nuxt',
  ],

  css: [
    '~/assets/styles/main.scss'
  ],

  components: [
    { path: '~/components', pathPrefix: false },
  ],

  plugins: [
    '~/plugins/auth.server.ts',
  ],

  build: {
    transpile: ['vue3-apexcharts', 'apexcharts']
  },

  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: `@use "~/assets/styles/breakpoints" as *;`,
        }
      }
    }
  },

  runtimeConfig: {
    flaskApiBase: 'http://localhost:5000',
    flaskApiPrefix: '/api',
    flaskAuthPrefix: '/api/auth',
    siteUrl: process.env.NUXT_PUBLIC_SITE_URL || 'http://localhost:3000',

    public: {
      appName: 'MotoBind'
    }
  },

  // --- SEO: Site Config (для @nuxtjs/seo) ---
  site: {
    url: process.env.NUXT_PUBLIC_SITE_URL || 'http://localhost:3000',
    name: 'MotoBind',
    description: 'Сервис для мотоциклистов: гараж, обслуживание, мануалы и диагностика',
    defaultLocale: 'ru',
    identity: { type: 'Organization' },
  },

  // --- PWA: Manifest & Workbox ---
  pwa: {
    registerType: 'autoUpdate',
    manifest: {
      name: 'MotoBind',
      short_name: 'MotoBind',
      description: 'Сервис для мотоциклистов: гараж, обслуживание, мануалы и диагностика',
      theme_color: '#7000ff',
      background_color: '#0f0f14',
      display: 'standalone',
      orientation: 'portrait',
      start_url: '/',
      scope: '/',
      icons: [
        { src: '/icons/icon-192x192.png', sizes: '192x192', type: 'image/png' },
        { src: '/icons/icon-512x512.png', sizes: '512x512', type: 'image/png' },
        { src: '/icons/icon-512x512-maskable.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' },
        { src: '/icons/icon-192x192.png', sizes: '192x192', type: 'image/png' }
      ],
      shortcuts: [
        { name: 'Мой гараж', url: '/garage', icons: [{ src: '/icons/icon-192x192.png', sizes: '192x192' }] },
        { name: 'Мануалы', url: '/manuals', icons: [{ src: '/icons/icon-192x192.png', sizes: '192x192' }] },
        { name: 'Диагностика', url: '/maintenance', icons: [{ src: '/icons/icon-192x192.png', sizes: '192x192' }] }
      ]
    },
    strategies: 'injectManifest',
    srcDir: 'service-worker',
    filename: 'sw.js',
    injectManifest: {
      globPatterns: ['**/*.{js,css,html,png,svg,ico,webp,woff2}'],
    },
    devOptions: {
      enabled: false
    }
  },

  robots: {
    disallow: ['/admin', '/login', '/register', '/api']
  },
  sitemap: {
    sources: ['/api/__sitemap__/urls'],
    exclude: [
      '/login', '/register', '/garage/**', '/maintenance/**', '/profile/**',
      '/notifications/**', '/admin/**', '/business/**', '/social/**',
      '/training/my', '/training/courses/**/lessons/**',
    ],
  },

  app: {
    head: {
      titleTemplate: '%s | MotoBind',
      htmlAttrs: {
        lang: 'ru'
      },
      meta: [
        { name: 'theme-color', content: '#7000ff' },
        { name: 'apple-mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-status-bar-style', content: 'black-translucent' },
        { name: 'apple-mobile-web-app-title', content: 'MotoBind' },
        { name: 'format-detection', content: 'telephone=no' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'apple-touch-icon', href: '/icons/icon-192x192.png' },
        { rel: 'manifest', href: '/manifest.webmanifest' },
        {
          rel: 'stylesheet',
          href: 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css',
        },
      ],
      script: [
        {
          innerHTML: `
            (function() {
              try {
                var m = document.cookie.match(/(?:^|; )motobind-theme=([^;]*)/);
                var t = m ? decodeURIComponent(m[1]) : 'system';
                var actual = t;
                if (t === 'system') {
                  actual = window.matchMedia('(prefers-color-scheme: dark)').matches
                    ? 'dark' : 'light';
                }
                document.documentElement.setAttribute('data-theme', actual);
              } catch (e) {}
            })();
          `,
          type: 'text/javascript',
          tagPosition: 'head',
        }
      ]
    }
  }
})
