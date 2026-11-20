<template>
  <div class="article-page">
    <div v-if="learningStore.currentArticleLoading" class="article-page__loading">
      <i class="fa fa-spinner fa-spin" /> Загрузка...
    </div>

    <div v-else-if="!article" class="article-page__empty">
      <i class="fa fa-exclamation-triangle" />
      <p>Статья не найдена</p>
      <router-link :to="{ name: 'learning-articles' }" class="btn btn-secondary">
        К статьям
      </router-link>
    </div>

    <template v-else>
      <nav class="article-breadcrumb">
        <router-link :to="{ name: 'learning-articles' }">Статьи</router-link>
        <i class="fa fa-chevron-right" />
        <span>{{ categoryLabel(article.category) }}</span>
      </nav>

      <article class="article-content">
        <h1 class="article-content__title">{{ article.title }}</h1>

        <div v-if="article.cover_url" class="article-cover">
          <img :src="resolveMedia(article.cover_url)" :alt="article.title" />
        </div>

        <div v-if="article.tags?.length" class="article-tags">
          <span v-for="tag in article.tags" :key="tag" class="article-tag">
            {{ tag }}
          </span>
        </div>

        <MarkdownRenderer :content="article.content" />
      </article>

      <div v-if="article.related?.length" class="related">
        <h2>Похожие статьи</h2>
        <div class="related__grid">
          <ArticleCard
            v-for="r in article.related"
            :key="r.id"
            :article="r"
          />
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue'
import ArticleCard from '@/components/learning/ArticleCard.vue'
import MarkdownRenderer from '@/components/learning/MarkdownRenderer.vue'
import { useLearningStore } from '@/stores'
import { resolveMedia } from '@/utils/mediaUrl'

const props = defineProps({
  slug: { type: String, required: true },
})

const learningStore = useLearningStore()
const article = computed(() => learningStore.currentArticle)

onMounted(load)
watch(() => props.slug, load)

function load() {
  learningStore.loadArticle(props.slug).catch(() => {})
}

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
.article-page {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  max-width: 800px;
  margin: 0 auto;
}

.article-page__loading,
.article-page__empty {
  padding: 40px;
  text-align: center;
  color: var(--text-muted);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.article-breadcrumb {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: var(--text-sm);
  color: var(--text-muted);
}

.article-breadcrumb a {
  color: var(--text-secondary);
  text-decoration: none;
}

.article-breadcrumb a:hover {
  color: var(--accent-text);
}

.article-breadcrumb i {
  font-size: 10px;
  opacity: 0.5;
}

.article-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.article-content__title {
  margin: 0;
  font-size: var(--text-3xl);
  font-weight: var(--fw-bold);
  line-height: var(--leading-tight);
  color: var(--text-primary);
}

.article-cover {
  width: 100%;
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.article-cover img {
  width: 100%;
  height: auto;
  display: block;
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.article-tag {
  font-size: 12px;
  padding: 3px 10px;
  background: var(--accent-trans);
  color: var(--accent-text);
  border-radius: var(--radius-full);
}

.related {
  margin-top: var(--space-5);
  padding-top: var(--space-4);
  border-top: 1px solid var(--border-light);
}

.related h2 {
  margin: 0 0 var(--space-3);
  font-size: var(--text-lg);
}

.related__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: var(--space-3);
}

@media (max-width: 640px) {
  .related__grid {
    grid-template-columns: 1fr;
  }

  .article-content__title {
    font-size: var(--text-2xl);
  }
}
</style>
