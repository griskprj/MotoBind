<script setup lang="ts">
const route = useRoute()
const id = route.params.id

await navigateTo(`/manuals/${id}`, { redirectCode: 301 })
</script>

<template>
  <div />
</template>
