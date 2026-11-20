export default defineEventHandler((event) => {
  const config = useRuntimeConfig(event)
  const baseUrl = config.public.siteUrl || 'https://motobind.ru'

  const content = `
User-agent: *
Allow: /
Allow: /manuals
Allow: /training
Allow: /social
Disallow: /garage
Disallow: /admin
Disallow: /profile
Disallow: /business
Disallow: /login
Disallow: /register

Sitemap: ${baseUrl}/sitemap.xml
`.trim()

  setHeader(event, 'Content-Type', 'text/plain')
  return content
})
