<script setup lang="ts">
import type { ArticleDetail } from '~/types'

const route = useRoute()
const api = useApi()
const mediaUrl = useMediaUrl()

const { data: article, pending, error } = await useAsyncData(
  `article-${route.params.slug}`,
  () => api.training.getArticle(route.params.slug as string)
)

if (error.value || !article.value) {
  throw createError({ statusCode: 404, statusMessage: 'Статья не найдена' })
}

useSeoMeta({
  title: `${article.value.title} — MotoBind`,
  description: article.value.short_description || 'Статья по ремонту и обслуживанию мотоциклов.',
  ogType: 'article',
})

// JSON-LD
useHead({
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'Article',
        headline: article.value.title,
        description: article.value.short_description,
        author: {
          '@type': 'Person',
          name: article.value.author?.username || 'MotoBind',
        },
        datePublished: article.value.published_at || article.value.created_at,
      }),
    },
  ],
})
</script>

<template>
  <div v-if="article" class="page-article">
    <header class="article-header">
      <NuxtLink to="/training" class="back-link">
        <i class="fa-solid fa-arrow-left"></i> Все статьи
      </NuxtLink>
      <div class="meta">
        <span v-if="article.category" class="category">{{ article.category }}</span>
        <span class="date">{{ new Date(article.created_at || '').toLocaleDateString('ru-RU') }}</span>
      </div>
      <h1 class="article-title">{{ article.title }}</h1>
      <p class="article-desc">{{ article.short_description }}</p>
      <div class="author">
        <i class="fa-solid fa-user"></i>
        {{ article.author?.username || 'MotoBind' }}
      </div>
    </header>

    <!-- Обложка -->
    <img
      v-if="article.cover_url"
      :src="mediaUrl(article.cover_url)!"
      class="article-cover"
      alt="Обложка"
    />

    <!-- Контент -->
    <div class="article-content prose">
      <MarkdownRenderer :content="article.content" />
    </div>

    <!-- Похожие статьи -->
    <section v-if="article.related && article.related.length > 0" class="related-section">
      <h2 class="section-title">Читайте также</h2>
      <div class="related-grid">
        <BaseCard
          v-for="rel in article.related"
          :key="rel.id"
          hoverable
          clickable
          :to="`/training/articles/${rel.slug}`"
        >
          <h3 class="rel-title">{{ rel.title }}</h3>
          <p class="rel-desc">{{ rel.short_description }}</p>
        </BaseCard>
      </div>
    </section>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.page-article {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
  padding-bottom: var(--space-10);
}

.article-header { display: flex; flex-direction: column; gap: var(--space-3); }
.back-link { font-size: var(--text-sm); color: var(--color-text-secondary); text-decoration: none; &:hover { color: var(--color-brand); } }
.meta { display: flex; gap: var(--space-3); font-size: var(--text-sm); color: var(--color-brand); font-weight: var(--fw-medium); }
.article-title { font-size: var(--text-3xl); font-weight: var(--fw-bold); line-height: var(--leading-tight); }
.article-desc { font-size: var(--text-lg); color: var(--color-text-secondary); line-height: var(--leading-relaxed); }
.author { font-size: var(--text-sm); color: var(--color-text-tertiary); display: flex; align-items: center; gap: var(--space-2); }

.article-cover {
  width: 100%;
  max-height: 400px;
  object-fit: cover;
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
}

.article-content {
  font-size: var(--text-base);
  line-height: var(--leading-relaxed);
  color: var(--color-text);
}

.related-section { margin-top: var(--space-8); }
.section-title { font-size: var(--text-xl); font-weight: var(--fw-semibold); margin-bottom: var(--space-4); }
.related-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: var(--space-4); }
.rel-title { font-size: var(--text-base); font-weight: var(--fw-semibold); margin-bottom: var(--space-2); }
.rel-desc { font-size: var(--text-sm); color: var(--color-text-secondary); }
</style>
