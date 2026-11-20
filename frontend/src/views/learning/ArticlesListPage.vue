<template>
  <div class="articles-list">
    <div class="articles-list__head">
      <h3>Статьи</h3>
      <p>Полезные материалы: от выбора экипа до первой помощи</p>
    </div>

    <div class="article-filters">
      <div class="article-filters__search">
        <i class="fa fa-search" />
        <input
          v-model="filters.search"
          type="text"
          placeholder="Поиск статей..."
          @input="onSearch"
        />
      </div>
      <select v-model="filters.category" class="article-filters__select" @change="onFilter">
        <option value="">Все категории</option>
        <option value="riding">Вождение</option>
        <option value="repair">Ремонт</option>
        <option value="gear">Экипировка</option>
        <option value="first_aid">Первая помощь</option>
        <option value="law">Право</option>
        <option value="travel">Путешествия</option>
      </select>
    </div>

    <div v-if="learningStore.articlesLoading" class="articles-list__loading">
      <i class="fa fa-spinner fa-spin" /> Загрузка...
    </div>

    <div v-else-if="!learningStore.hasArticles" class="empty-state">
      <i class="fa fa-newspaper" />
      <p class="empty-text">Статей пока нет</p>
    </div>

    <div v-else class="articles-list__grid">
      <ArticleCard
        v-for="a in learningStore.articles"
        :key="a.id"
        :article="a"
      />
    </div>

    <BasePagination
      v-if="learningStore.articlesPagination?.pages > 1"
      :pagination="learningStore.articlesPagination"
      @change="onPageChange"
    />
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import ArticleCard from '@/components/learning/ArticleCard.vue'
import BasePagination from '@/components/learning/BasePagination.vue'
import { useLearningStore } from '@/stores'

const learningStore = useLearningStore()
const page = ref(1)
const filters = reactive({ search: '', category: '' })

onMounted(load)

function load() {
  learningStore
    .loadArticles({ ...filters, page: page.value, per_page: 12 })
    .catch(() => {})
}

function onSearch() {
  page.value = 1
  load()
}

function onFilter() {
  page.value = 1
  load()
}

function onPageChange(p) {
  page.value = p
  load()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<style scoped>
.articles-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.articles-list__head h3 {
  margin: 0 0 4px;
  font-size: var(--text-lg);
}

.articles-list__head p {
  margin: 0;
  font-size: var(--text-sm);
  color: var(--text-muted);
}

.articles-list__loading {
  padding: 40px;
  text-align: center;
  color: var(--text-muted);
  font-size: var(--text-sm);
}

.articles-list__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: var(--space-3);
}

.article-filters {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.article-filters__search {
  position: relative;
  flex: 1;
  min-width: 200px;
  display: flex;
  align-items: center;
}

.article-filters__search i {
  position: absolute;
  left: 12px;
  color: var(--text-muted);
  font-size: 13px;
  pointer-events: none;
}

.article-filters__search input {
  width: 100%;
  padding: 10px 12px 10px 34px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--bg-input);
  color: var(--text-primary);
  font-family: inherit;
  font-size: var(--text-sm);
}

.article-filters__search input:focus {
  outline: none;
  border-color: var(--accent);
}

.article-filters__select {
  padding: 10px 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--bg-input);
  color: var(--text-primary);
  font-family: inherit;
  font-size: var(--text-sm);
  cursor: pointer;
  min-width: 160px;
}

@media (max-width: 640px) {
  .articles-list__grid {
    grid-template-columns: 1fr;
  }
}
</style>
