<script setup lang="ts">
const { resolvedTheme } = useTheme()

useSeoMeta({
  titleTemplate: (title) => title ? `${title} | MotoBind` : 'MotoBind — Сервис для мотоциклистов',
  ogSiteName: 'MotoBind',
  ogType: 'website',
  twitterCard: 'summary_large_image',
})

useHead({
  htmlAttrs: { 'data-theme': resolvedTheme },
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'Organization',
        name: 'MotoBind',
        url: 'https://motobind.ru',
        logo: 'https://motobind.ru/icons/icon-512x512.png',
      })
    }
  ]
})
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
  <PwaInstallPromt />
</template>
