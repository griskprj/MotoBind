type SitemapItem = {
  id?: number | string
  slug?: string
  updated_at?: string | null
  published_at?: string | null
}

type PaginatedResponse = {
  manuals?: SitemapItem[]
  courses?: SitemapItem[]
  articles?: SitemapItem[]
  pages?: number
  pagination?: { pages?: number }
}

export default defineSitemapEventHandler(async (event) => {
  const config = useRuntimeConfig(event)
  const baseURL = String(config.flaskApiBase).replace(/\/$/, '')
  const apiPrefix = String(config.flaskApiPrefix || '/api').replace(/\/$/, '')

  async function collect(path: string, collection: 'manuals' | 'courses' | 'articles') {
    const entries: SitemapItem[] = []
    const perPage = 100
    const first = await $fetch<PaginatedResponse>(`${baseURL}${apiPrefix}/${path}`, {
      query: { page: 1, per_page: perPage },
    })
    entries.push(...(first[collection] || []))

    const totalPages = first.pages || first.pagination?.pages || 1
    for (let page = 2; page <= Math.min(totalPages, 100); page += 1) {
      const result = await $fetch<PaginatedResponse>(`${baseURL}${apiPrefix}/${path}`, {
        query: { page, per_page: perPage },
      })
      entries.push(...(result[collection] || []))
    }

    return entries
  }

  const [manuals, courses, articles] = await Promise.all([
    collect('manual/list', 'manuals'),
    collect('learning/courses', 'courses'),
    collect('learning/articles', 'articles'),
  ])

  return [
    ...manuals.filter(item => item.id).map(item => ({
      loc: `/manuals/${item.id}`,
      lastmod: item.updated_at || item.published_at || undefined,
      changefreq: 'weekly' as const,
      priority: 0.8,
    })),
    ...courses.filter(item => item.slug).map(item => ({
      loc: `/training/courses/${item.slug}`,
      lastmod: item.updated_at || undefined,
      changefreq: 'weekly' as const,
      priority: 0.8,
    })),
    ...articles.filter(item => item.slug).map(item => ({
      loc: `/training/articles/${item.slug}`,
      lastmod: item.updated_at || item.published_at || undefined,
      changefreq: 'weekly' as const,
      priority: 0.8,
    })),
  ]
})
