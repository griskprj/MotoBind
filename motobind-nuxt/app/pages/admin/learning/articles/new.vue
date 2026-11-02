<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'admin'] })
const router = useRouter()
</script>

<template>
  <div class="page-new-article">
    <header class="page-header">
      <NuxtLink to="/admin/learning/articles" class="back-link">← Назад к статьям</NuxtLink>
      <h1 class="page-title">Новая статья</h1>
    </header>
    <ArticleForm @success="router.push('/admin/learning/articles')" @cancel="router.push('/admin/learning/articles')" />
  </div>
</template>
