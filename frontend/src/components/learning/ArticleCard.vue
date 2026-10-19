<template>
  <router-link
    :to="{ name: 'learning-article', params: { slug: article.slug } }"
    class="article-card"
  >
    <div class="article-card__cover">
      <img
        v-if="article.cover_url"
        :src="resolveMedia(article.cover_url)"
        :alt="article.title"
        loading="lazy"
      />
      <div v-else class="article-card__cover-placeholder">
        <i class="fa fa-newspaper" />
      </div>
    </div>
    <div class="article-card__body">
      <div class="article-card__category">{{ categoryLabel(article.category) }}</div>
      <div class="article-card__title">{{ article.title }}</div>
      <div v-if="article.short_description" class="article-card__desc">
        {{ article.short_description }}
      </div>
      <div v-if="article.tags?.length" class="article-card__tags">
        <span v-for="tag in article.tags.slice(0, 3)" :key="tag" class="article-card__tag">
          {{ tag }}
        </span>
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { resolveMedia } from '@/utils/mediaUrl'

defineProps({
  article: { type: Object, required: true },
})

function categoryLabel(c) {
  const map = {
    riding: 'Вождение',
    repair: 'Ремонт',
    gear: 'Экипировка',
    first_aid: 'Первая помощь',
    law: 'Право',
    travel: 'Путешествия',
  }
  return map[c] || c
}
</script>

<style scoped>
.article-card {
  display: flex;
  flex-direction: column;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  overflow: hidden;
  text-decoration: none;
  color: inherit;
  transition: all var(--transition-base);
  height: 100%;
}

.article-card:hover {
  transform: translateY(-2px);
  border-color: var(--accent);
  box-shadow: var(--shadow-md);
}

.article-card__cover {
  aspect-ratio: 16 / 9;
  background: var(--bg-secondary);
  overflow: hidden;
}

.article-card__cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.article-card__cover-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
  font-size: 40px;
  opacity: 0.4;
}

.article-card__body {
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
}

.article-card__category {
  font-size: 11px;
  font-weight: var(--fw-semibold);
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: var(--accent-text);
}

.article-card__title {
  font-size: var(--text-base);
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
  line-height: var(--leading-tight);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-card__desc {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: var(--leading-base);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-card__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: auto;
  padding-top: 8px;
}

.article-card__tag {
  font-size: 11px;
  padding: 2px 8px;
  background: var(--accent-trans);
  color: var(--accent-text);
  border-radius: var(--radius-full);
}
</style>
