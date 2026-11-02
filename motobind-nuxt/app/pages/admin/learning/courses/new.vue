<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'admin'] })
const router = useRouter()
</script>

<template>
  <div class="page-new-course">
    <header class="page-header">
      <NuxtLink to="/admin/learning/courses" class="back-link">← Назад к курсам</NuxtLink>
      <h1 class="page-title">Новый курс</h1>
    </header>
    <CourseForm @success="router.push('/admin/learning/courses')" @cancel="router.push('/admin/learning/courses')" />
  </div>
</template>
