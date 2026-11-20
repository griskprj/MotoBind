export default defineSitemapEventHandler(async () => {
  const manuals = await $fetch<any[]>('http://localhost:5000/api/manual/list?per_page=1000')

  return manuals.map((manual) => ({
    loc: `/manuals/${manual.id}`,
    lastmod: manual.updated_at || new Date().toISOString(),
    changefreq: 'weekly',
    priority: 0.8,
  }))
})
