<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'admin'] })
useSeoMeta({ title: 'Курсы — Админка', robots: 'noindex' })

const api = useApi()
const toast = useToast()

const courses = ref<any[]>([])
const pending = ref(false)
const error = ref<any>(null)

// Загрузка курсов
async function loadCourses() {
  pending.value = true
  error.value = null
  try {
    const res = await api.admin.adminListCourses()
    courses.value = res.courses || []
  } catch (e: any) {
    console.error('Ошибка загрузки курсов:', e)
    error.value = e
    toast.error(e.message || 'Не удалось загрузить список курсов')
  } finally {
    pending.value = false
  }
}

onMounted(loadCourses)

// Удаление
async function deleteCourse(id: number) {
  if (!confirm('Вы уверены, что хотите удалить этот курс? Это действие необратимо.')) return
  try {
    await api.admin.adminDeleteCourse(id)
    toast.success('Курс удалён')
    await loadCourses()
  } catch (e: any) {
    toast.error(e.message || 'Ошибка удаления')
  }
}

// Публикация
async function publishCourse(id: number) {
  try {
    await api.admin.adminPublishCourse(id)
    toast.success('Курс опубликован')
    await loadCourses()
  } catch (e: any) {
    toast.error(e.message || 'Ошибка публикации')
  }
}

// В архив
async function archiveCourse(id: number) {
  try {
    await api.admin.adminArchiveCourse(id)
    toast.success('Курс перемещён в архив')
    await loadCourses()
  } catch (e: any) {
    toast.error(e.message || 'Ошибка архивации')
  }
}

// Статусы для отображения
const statusLabels: Record<string, string> = {
  draft: 'Черновик',
  published: 'Опубликован',
  archived: 'В архиве',
}
</script>

<template>
  <div class="admin-courses-page">
    <header class="page-header">
      <div>
        <h1 class="page-title">Управление курсами</h1>
        <p class="page-subtitle">Создание, редактирование и публикация курсов.</p>
      </div>
      <BaseButton to="/admin/learning/courses/new" variant="primary">
        <template #icon><i class="fa-solid fa-plus"></i></template>
        Новый курс
      </BaseButton>
    </header>

    <!-- Загрузка -->
    <div v-if="pending" class="loading">
      <BaseSkeleton height="60px" rounded v-for="i in 5" :key="i" />
    </div>

    <!-- Ошибка -->
    <div v-else-if="error" class="error-state">
      <i class="fa-solid fa-triangle-exclamation"></i>
      <p>Не удалось загрузить курсы.</p>
      <BaseButton @click="loadCourses">Повторить</BaseButton>
    </div>

    <!-- Пусто -->
    <BaseEmptyState
      v-else-if="courses.length === 0"
      title="Курсов пока нет"
      description="Создайте первый курс, чтобы начать обучение."
    >
      <template #action>
        <BaseButton to="/admin/learning/courses/new" variant="primary">Создать курс</BaseButton>
      </template>
    </BaseEmptyState>

    <!-- Таблица -->
    <BaseCard v-else padding="none" class="table-card">
      <div class="table-wrap">
        <table class="admin-table">
          <thead>
            <tr>
              <th>Название</th>
              <th>Slug</th>
              <th>Уроков</th>
              <th>Статус</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="course in courses" :key="course.id">
              <td class="cell-title">{{ course.title }}</td>
              <td class="text-mono">{{ course.slug }}</td>
              <td>{{ course.lessons_count }}</td>
              <td>
                <span class="badge" :class="`badge--${course.status}`">
                  {{ statusLabels[course.status] || course.status }}
                </span>
              </td>
              <td>
                <div class="actions">
                  <BaseButton
                    size="sm"
                    variant="ghost"
                    title="Опубликовать"
                    @click="publishCourse(course.id)"
                    :disabled="course.status === 'published'"
                  >
                    <i class="fa-solid fa-check"></i>
                  </BaseButton>
                  <BaseButton
                    size="sm"
                    variant="ghost"
                    title="В архив"
                    @click="archiveCourse(course.id)"
                    :disabled="course.status === 'archived'"
                  >
                    <i class="fa-solid fa-box-archive"></i>
                  </BaseButton>
                  <BaseButton
                    size="sm"
                    variant="secondary"
                    :to="`/admin/learning/courses/${course.id}`"
                    title="Редактировать"
                  >
                    <i class="fa-solid fa-pen"></i>
                  </BaseButton>
                  <BaseButton
                    size="sm"
                    variant="danger"
                    @click="deleteCourse(course.id)"
                    title="Удалить"
                  >
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

.admin-courses-page {
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
  color: var(--color-text);
}

.page-subtitle {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin-top: var(--space-1);
}

/* Загрузка */
.loading {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

/* Ошибка */
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

  i { font-size: 32px; }
  p { font-size: var(--text-base); }
}

/* Таблица */
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
    white-space: nowrap;
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

/* Бейджи статусов */
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

/* Действия */
.actions {
  display: flex;
  gap: var(--space-2);
  justify-content: flex-end;
  align-items: center;
}
</style>
