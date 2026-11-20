<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'admin'] })
useSeoMeta({ title: 'Статьи — Админка', robots: 'noindex' })

const api = useApi()
const toast = useToast()
const articles = ref<any[]>([])
const pending = ref(false)
const error = ref<any>(null)

async function loadArticles() {
  pending.value = true
  error.value = null
  try {
    const res = await api.admin.adminListArticles()
    articles.value = res.articles || []
  } catch (e: any) {
    console.error(e)
    error.value = e
    toast.error('Ошибка загрузки статей')
  } finally {
    pending.value = false
  }
}

onMounted(loadArticles)

async function deleteArticle(id: number) {
  if (!confirm('Удалить статью?')) return
  try {
    await api.admin.adminDeleteArticle(id)
    toast.success('Статья удалена')
    await loadArticles()
  } catch (e) {
    toast.error('Ошибка удаления')
  }
}

async function publishArticle(id: number) {
  try {
    await api.admin.adminPublishArticle(id)
    toast.success('Статья опубликована')
    await loadArticles()
  } catch (e) {
    toast.error('Ошибка публикации')
  }
}

async function archiveArticle(id: number) {
  try {
    await api.admin.adminArchiveArticle(id)
    toast.success('Статья в архиве')
    await loadArticles()
  } catch (e) {
    toast.error('Ошибка архивации')
  }
}

const statusLabels: Record<string, string> = {
  draft: 'Черновик',
  published: 'Опубликована',
  archived: 'В архиве',
}
</script>

<template>
  <div class="admin-articles-page">
    <header class="page-header">
      <div>
        <h1 class="page-title">Управление статьями</h1>
        <p class="page-subtitle">Создание, редактирование и публикация статей.</p>
      </div>
      <BaseButton to="/admin/learning/articles/new" variant="primary">
        <template #icon><i class="fa-solid fa-plus"></i></template>
        Новая статья
      </BaseButton>
    </header>

    <div v-if="pending" class="loading">
      <BaseSkeleton height="60px" v-for="i in 5" :key="i" />
    </div>

    <div v-else-if="error" class="error-state">
      <i class="fa-solid fa-triangle-exclamation"></i>
      <p>Не удалось загрузить статьи.</p>
      <BaseButton @click="loadArticles">Повторить</BaseButton>
    </div>

    <BaseEmptyState
      v-else-if="articles.length === 0"
      title="Статей пока нет"
      description="Создайте первую статью."
    >
      <template #action>
        <BaseButton to="/admin/learning/articles/new" variant="primary">Создать статью</BaseButton>
      </template>
    </BaseEmptyState>

    <BaseCard v-else padding="none" class="table-card">
      <div class="table-wrap">
        <table class="admin-table">
          <thead>
            <tr>
              <th>Название</th>
              <th>Slug</th>
              <th>Категория</th>
              <th>Статус</th>
              <th>Дата</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="article in articles" :key="article.id">
              <td class="cell-title">{{ article.title }}</td>
              <td class="text-mono">{{ article.slug }}</td>
              <td>{{ article.category }}</td>
              <td>
                <span class="badge" :class="`badge--${article.status}`">
                  {{ statusLabels[article.status] || article.status }}
                </span>
              </td>
              <td class="text-sm">{{ new Date(article.created_at).toLocaleDateString('ru-RU') }}</td>
              <td>
                <div class="actions">
                  <BaseButton size="sm" variant="ghost" title="Опубликовать" @click="publishArticle(article.id)" :disabled="article.status === 'published'">
                    <i class="fa-solid fa-check"></i>
                  </BaseButton>
                  <BaseButton size="sm" variant="ghost" title="В архив" @click="archiveArticle(article.id)" :disabled="article.status === 'archived'">
                    <i class="fa-solid fa-box-archive"></i>
                  </BaseButton>
                  <BaseButton size="sm" variant="secondary" :to="`/admin/learning/articles/${article.id}`" title="Редактировать">
                    <i class="fa-solid fa-pen"></i>
                  </BaseButton>
                  <BaseButton size="sm" variant="danger" @click="deleteArticle(article.id)" title="Удалить">
                    <i class="fa-solid fa-trash"></i>
                  </BaseButton>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </BaseCard>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.admin-articles-page {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.page-header {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  @include sm-up {
    flex-direction: row;
    justify-content: space-between;
    align-items: flex-start;
  }
}

.page-title {
  font-size: var(--text-2xl);
  font-weight: var(--fw-bold);
}

.page-subtitle {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin-top: var(--space-1);
}

.loading {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-8);
  background: var(--color-danger-soft);
  border-radius: var(--radius-md);
  color: var(--color-danger);
  text-align: center;
}

.table-card {
  overflow: hidden;
}

.table-wrap {
  overflow-x: auto;
}

.admin-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--text-sm);

  th {
    text-align: left;
    padding: var(--space-3) var(--space-4);
    font-weight: var(--fw-semibold);
    color: var(--color-text-tertiary);
    border-bottom: 1px solid var(--color-border);
    background: var(--color-surface-secondary);
  }

  td {
    padding: var(--space-3) var(--space-4);
    border-bottom: 1px solid var(--color-border-light);
    vertical-align: middle;
  }

  tr:last-child td {
    border-bottom: none;
  }

  tr:hover td {
    background: var(--color-surface-hover);
  }
}

.cell-title {
  font-weight: var(--fw-medium);
  color: var(--color-text);
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.text-mono {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
}

.text-sm {
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
}

.badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: var(--fw-medium);
  text-transform: capitalize;
}

.badge--draft {
  background: var(--color-surface-secondary);
  color: var(--color-text-secondary);
}

.badge--published {
  background: var(--color-success-soft);
  color: var(--color-success-strong);
}

.badge--archived {
  background: var(--color-warning-soft);
  color: var(--color-warning-strong);
}

.actions {
  display: flex;
  gap: var(--space-2);
  justify-content: flex-end;
}
</style>
