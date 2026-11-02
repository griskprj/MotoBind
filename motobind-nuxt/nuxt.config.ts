export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',

  devtools: {
    enabled: true
  },

  modules: [
    '@pinia/nuxt'
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

  app: {
    head: {
      titleTemplate: '%s | MotoBind',
      htmlAttrs: {
        lang: 'ru'
      },
      link: [
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
