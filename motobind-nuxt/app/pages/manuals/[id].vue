<script setup lang="ts">
const { render } = useMarkdown()
const route = useRoute()
const api = useApi()
const auth = useAuthStore()

const { data: manual, pending, error } = await useAsyncData(
  `manual-${route.params.id}`,
  () => api.manuals.get(route.params.id as string)
)

if (error.value || !manual.value) {
  throw createError({ statusCode: 404, statusMessage: 'Мануал не найден' })
}

useSeoMeta({
  title: `${manual.value.title} — MotoBind`,
  description: manual.value.description || 'Инструкция по ремонту мотоцикла',
  ogType: 'article',
})

useHead({
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'HowTo',
        name: manual.value.title,
        description: manual.value.description,
        totalTime: manual.value.time_estimate ? `PT${manual.value.time_estimate.replace(' мин', 'M')}` : undefined,
        tool: manual.value.instruments ? [{ '@type': 'HowToTool', name: manual.value.instruments }] : undefined,
        step: manual.value.steps.map((s, i) => ({
          '@type': 'HowToStep',
          position: i + 1,
          name: s.title,
          text: s.text || '',
        })),
      }),
    },
  ],
})
</script>

<template>
  <div v-if="manual" class="page-manual">
    <header class="manual-header">
      <div class="header-actions">
        <NuxtLink to="/manuals" class="back-link">
          <i class="fa-solid fa-arrow-left"></i> Все мануалы
        </NuxtLink>

        <BaseButton
          v-if="manual.author_id === auth.user?.id || auth.isAdmin"
          :to="`/manuals/edit/${manual.id}`"
          variant="secondary"
          size="sm"
        >
          <i class="fa-solid fa-pen"></i> Редактировать
        </BaseButton>
      </div>

      <div class="meta">
        <span class="category">{{ manual.category }}</span>
        <span v-if="manual.difficult" class="difficulty">
          <i class="fa-solid fa-signal"></i> {{ manual.difficult === 'easy' ? 'Легко' : manual.difficult === 'medium' ? 'Средне' : 'Сложно' }}
        </span>
        <span v-if="manual.time_estimate"><i class="fa-regular fa-clock"></i> {{ manual.time_estimate }}</span>
        <span v-if="manual.motorcycle"><i class="fa-solid fa-motorcycle"></i> {{ manual.motorcycle }}</span>
      </div>

      <h1 class="manual-title">{{ manual.title }}</h1>
      <p class="manual-desc markdown-body" v-html="render(manual.description)" />
    </header>

    <!-- Блок безопасности -->
    <section v-if="manual.safety_tip || manual.warnings || manual.conditions" class="safety-section">
      <h2 class="section-title"><i class="fa-solid fa-shield-halved"></i> Безопасность и подготовка</h2>
      <div class="safety-cards">
        <div v-if="manual.safety_tip" class="safety-card tip">
          <i class="fa-solid fa-lightbulb"></i>
          <p>{{ manual.safety_tip }}</p>
        </div>
        <div v-if="manual.warnings" class="safety-card warning">
          <i class="fa-solid fa-triangle-exclamation"></i>
          <p>{{ manual.warnings }}</p>
        </div>
        <div v-if="manual.conditions" class="safety-card condition">
          <i class="fa-solid fa-check-circle"></i>
          <p>{{ manual.conditions }}</p>
        </div>
      </div>
    </section>

    <!-- Инструменты и материалы -->
    <section v-if="manual.instruments || manual.parts" class="tools-section">
      <h2 class="section-title"><i class="fa-solid fa-screwdriver-wrench"></i> Инструменты и материалы</h2>
      <div class="tools-grid">
        <div v-if="manual.instruments" class="tool-block">
          <h3>Инструменты</h3>
          <p>{{ manual.instruments }}</p>
        </div>
        <div v-if="manual.parts" class="tool-block">
          <h3>Материалы и запчасти</h3>
          <p>{{ manual.parts }}</p>
        </div>
      </div>
    </section>

    <!-- Ссылки на документацию -->
    <section v-if="manual.docs_links && manual.docs_links.length > 0" class="docs-section">
      <h2 class="section-title"><i class="fa-solid fa-link"></i> Ссылки на документацию</h2>
      <ul class="docs-list">
        <li v-for="(link, idx) in manual.docs_links" :key="idx">
          <a :href="link" target="_blank" rel="noopener noreferrer">
            <i class="fa-solid fa-file-pdf"></i> Документация {{ idx + 1 }}
          </a>
        </li>
      </ul>
    </section>

    <!-- Шаги -->
    <section class="steps-section">
      <h2 class="section-title"><i class="fa-solid fa-list-ol"></i> Шаги выполнения</h2>
      <div class="steps-list">
        <div v-for="step in manual.steps" :key="step.id" class="step-card">
          <div class="step-number">{{ step.order }}</div>
          <div class="step-content">
            <h3 class="step-title">{{ step.title }}</h3>
            <p v-if="step.text" class="step-text markdown-body" v-html="render(step.text)" />

            <!-- Картинка шага -->
            <img v-if="step.image" :src="useMediaUrl()(step.image)!" class="step-image" loading="lazy" />

            <!-- Tip и Warning -->
            <div v-if="step.tip" class="step-alert tip">
              <i class="fa-solid fa-lightbulb"></i> {{ step.tip }}
            </div>
            <div v-if="step.warning" class="step-alert warning">
              <i class="fa-solid fa-triangle-exclamation"></i> {{ step.warning }}
            </div>
            <div v-if="step.result" class="step-result">
              <strong>Результат:</strong> {{ step.result }}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- После завершения -->
    <section v-if="manual.aftercare" class="aftercare-section">
      <h2 class="section-title"><i class="fa-solid fa-check"></i> После завершения</h2>
      <p class="markdown-body" v-html="render(manual.aftercare)" />
    </section>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.page-manual {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-8);
  padding-bottom: var(--space-10);
}

.manual-header {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.header-actions {
  display: flex;
  justify-content: space-between;
  gap: 8px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  width: fit-content;
  text-decoration: none;

  &:hover { color: var(--color-brand); }
}

.meta {
  display: flex;
  gap: var(--space-3);
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  color: var(--color-brand);
}

.manual-title {
  font-size: var(--text-3xl);
  font-weight: var(--fw-bold);
  line-height: var(--leading-tight);
  color: var(--color-text);
}

.manual-desc {
  font-size: var(--text-lg);
  color: var(--color-text-secondary);
  line-height: var(--leading-relaxed);
}

.section-title {
  font-size: var(--text-xl);
  font-weight: var(--fw-semibold);
  color: var(--color-text);
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-4);

  i { color: var(--color-brand); }
}

.tools-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  list-style: none;
  padding: 0;

  li {
    padding: var(--space-1) var(--space-3);
    background: var(--color-surface-secondary);
    border-radius: var(--radius-md);
    font-size: var(--text-sm);
    color: var(--color-text);
  }
}

.safety-cards {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}
.safety-card {
  display: flex;
  gap: var(--space-3);
  padding: var(--space-3);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);

  &.tip { background: var(--color-info-soft); color: var(--color-info-strong); }
  &.warning { background: var(--color-danger-soft); color: var(--color-danger-strong); }
  &.condition { background: var(--color-success-soft); color: var(--color-success-strong); }
}

.tools-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);
  @include sm-up { grid-template-columns: 1fr 1fr; }
}
.tool-block {
  background: var(--color-surface-secondary);
  padding: var(--space-4);
  border-radius: var(--radius-md);

  h3 { font-size: var(--text-sm); text-transform: uppercase; color: var(--color-text-tertiary); margin-bottom: var(--space-1); }
  p { font-size: var(--text-base); }
}

.markdown-body {
  line-height: var(--leading-relaxed);

  :deep(p) {
    margin: 0 0 var(--space-2);
    &:last-child { margin-bottom: 0; }
  }

  :deep(strong) {
    font-weight: var(--fw-semibold);
    color: var(--color-text);
  }

  :deep(em) {
    font-style: italic;
  }

  :deep(a) {
    color: var(--color-brand);
    text-decoration: underline;
    text-underline-offset: 2px;
    &:hover { text-decoration-thickness: 2px; }
  }

  :deep(ul),
  :deep(ol) {
    padding-left: var(--space-5);
    margin-bottom: var(--space-2);
  }

  :deep(li) {
    margin-bottom: var(--space-1);
  }

  :deep(code) {
    padding: 2px 6px;
    border-radius: var(--radius-sm);
    background: var(--color-surface-secondary);
    font-family: var(--font-mono);
    font-size: 0.9em;
  }

  :deep(pre) {
    padding: var(--space-3);
    border-radius: var(--radius-md);
    background: var(--color-surface-secondary);
    overflow-x: auto;
    margin-bottom: var(--space-3);

    code {
      padding: 0;
      background: none;
    }
  }
}

.step-image {
  max-width: 100%;
  border-radius: var(--radius-md);
  margin: var(--space-3) 0;
}

.step-alert {
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  margin-top: var(--space-2);

  &.tip { background: var(--color-info-soft); color: var(--color-info-strong); }
  &.warning { background: var(--color-danger-soft); color: var(--color-danger-strong); }
}

.step-result {
  margin-top: var(--space-2);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  background: var(--color-surface-secondary);
  padding: var(--space-2);
  border-radius: var(--radius-sm);
}

.steps-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.step-card {
  display: flex;
  gap: var(--space-4);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-4);
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-brand);
  color: #fff;
  font-weight: var(--fw-bold);
  flex-shrink: 0;
}

.step-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.step-title {
  font-size: var(--text-base);
  font-weight: var(--fw-semibold);
  color: var(--color-text);
}

.step-text {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  line-height: var(--leading-relaxed);
}
</style>
