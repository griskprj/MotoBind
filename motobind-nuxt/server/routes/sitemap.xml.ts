export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event)
  const baseUrl = config.public.siteUrl || 'https://motobind.ru'

  const urls = [
    { loc: '/', changefreq: 'daily', priority: '1.0' },
    { loc: '/manuals', changefreq: 'weekly', priority: '0.9' },
    { loc: '/training', changefreq: 'weekly', priority: '0.9' },
  ]

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  ${urls.map(u => `
  <url>
    <loc>${baseUrl}${u.loc}</loc>
    <changefreq>${u.changefreq}</changefreq>
    <priority>${u.priority}</priority>
  </url>`).join('')}
</urlset>`

  setHeader(event, 'Content-Type', 'application/xml')
  return xml
})
