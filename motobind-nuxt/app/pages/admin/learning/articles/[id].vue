<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'admin'] })
const route = useRoute()
const router = useRouter()
const api = useApi()

const { data: article, pending, error } = await useAsyncData(
  `admin-article-${route.params.id}`,
  () => api.admin.adminGetArticle(route.params.id as string)
)

if (error.value || !article.value) {
  throw createError({ statusCode: 404, statusMessage: 'Статья не найдена' })
}
</script>

<template>
  <div class="page-edit-article">
    <header class="page-header">
      <NuxtLink to="/admin/learning/articles" class="back-link">← Назад к статьям</NuxtLink>
      <h1 class="page-title">Редактирование статьи</h1>
    </header>
    <div v-if="pending">Загрузка...</div>
    <ArticleForm
      v-else-if="article"
      :initial-data="article"
      @success="router.push('/admin/learning/articles')"
      @cancel="router.push('/admin/learning/articles')"
    />
  </div>
</template>
