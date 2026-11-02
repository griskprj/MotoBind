<template>
  <div class="markdown-body" v-html="html" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { marked } from 'marked'

const props = defineProps<{
  content: string
}>()

marked.setOptions({
  breaks: true,
  gfm: true,
})

const html = computed(() => {
  if (!props.content) return ''
  return marked.parse(props.content) as string
})
</script>

<style scoped lang="scss">
.markdown-body {
  font-size: var(--text-base);
  line-height: var(--leading-relaxed);
  color: var(--color-text);

  :deep(p) { margin: 0 0 1em; }
  :deep(h1), :deep(h2), :deep(h3) { margin-top: 1.5em; margin-bottom: 0.5em; font-weight: var(--fw-semibold); }
  :deep(ul), :deep(ol) { padding-left: 1.5em; margin-bottom: 1em; }
  :deep(a) { color: var(--color-brand); text-decoration: underline; }
  :deep(code) { background: var(--color-surface-secondary); padding: 2px 6px; border-radius: var(--radius-sm); font-family: var(--font-mono); }
  :deep(pre) { background: var(--color-surface-secondary); padding: 12px 16px; border-radius: var(--radius-md); overflow-x: auto; }
  :deep(img) { max-width: 100%; border-radius: var(--radius-md); margin: 0.5em 0; }
}
</style>
