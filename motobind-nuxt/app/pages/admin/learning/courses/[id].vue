<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'admin'] })
const route = useRoute()
const router = useRouter()
const api = useApi()
const toast = useToast()

const courseId = computed(() => Number(route.params.id))

const { data: course, pending, error, refresh } = await useAsyncData(
  `admin-course-${courseId.value}`,
  () => api.admin.adminGetCourse(courseId.value)
)

if (error.value || !course.value) {
  throw createError({ statusCode: 404, statusMessage: 'Курс не найден' })
}

const isLessonModalOpen = ref(false)
const editingLesson = ref<any>(null)

function openCreateLesson() {
  editingLesson.value = null
  isLessonModalOpen.value = true
}

function openEditLesson(lesson: any) {
  editingLesson.value = lesson
  isLessonModalOpen.value = true
}

async function onLessonSaved() {
  isLessonModalOpen.value = false
  await refresh()
}

async function deleteLesson(id: number) {
  if (!confirm('Удалить урок?')) return
  try {
    await api.admin.adminDeleteLesson(id)
    toast.success('Урок удалён')
    await refresh()
  } catch (e) {
    toast.error('Ошибка удаления')
  }
}
</script>

<template>
  <div class="page-edit-course">
    <header class="page-header">
      <NuxtLink to="/admin/learning/courses" class="back-link">← Назад к курсам</NuxtLink>
      <h1 class="page-title">Редактирование курса</h1>
    </header>

    <div v-if="pending">Загрузка...</div>
    <template v-else-if="course">
      <!-- Форма самого курса -->
      <CourseForm
        :initial-data="course"
        @success="router.push('/admin/learning/courses')"
        @cancel="router.push('/admin/learning/courses')"
      />

      <!-- Секция уроков -->
      <BaseCard padding="lg" class="lessons-section">
        <div class="section-header">
          <h2 class="section-title">Уроки ({{ course.lessons?.length || 0 }})</h2>
          <BaseButton variant="secondary" @click="openCreateLesson">
            <i class="fa-solid fa-plus"></i> Добавить урок
          </BaseButton>
        </div>

        <div v-if="!course.lessons || course.lessons.length === 0" class="empty-lessons">
          Уроков пока нет.
        </div>

        <div v-else class="lessons-list">
          <div v-for="lesson in course.lessons" :key="lesson.id" class="lesson-item">
            <div class="lesson-number">{{ lesson.order }}</div>
            <div class="lesson-info">
              <h3 class="lesson-title">{{ lesson.title }}</h3>
              <span class="lesson-slug">{{ lesson.slug }}</span>
            </div>
            <div class="lesson-actions">
              <BaseButton size="sm" variant="ghost" @click="openEditLesson(lesson)">
                <i class="fa-solid fa-pen"></i>
              </BaseButton>
              <BaseButton size="sm" variant="danger" @click="deleteLesson(lesson.id)">
                <i class="fa-solid fa-trash"></i>
              </BaseButton>
            </div>
          </div>
        </div>
      </BaseCard>
    </template>

    <!-- Модалка урока -->
    <LessonFormModal
      v-if="isLessonModalOpen"
      :course-id="courseId"
      :lesson="editingLesson"
      @close="isLessonModalOpen = false"
      @saved="onLessonSaved"
    />
  </div>
</template>

<style scoped lang="scss">
.page-edit-course {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.page-header { display: flex; flex-direction: column; gap: var(--space-2); }
.back-link { font-size: var(--text-sm); color: var(--color-text-secondary); text-decoration: none; &:hover { color: var(--color-brand); } }
.page-title { font-size: var(--text-2xl); font-weight: var(--fw-bold); }

.lessons-section { margin-top: var(--space-4); }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--space-4); }
.section-title { font-size: var(--text-lg); font-weight: var(--fw-semibold); }

.empty-lessons { padding: var(--space-6); text-align: center; color: var(--color-text-tertiary); background: var(--color-surface-secondary); border-radius: var(--radius-md); }

.lessons-list { display: flex; flex-direction: column; gap: var(--space-2); }

.lesson-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.lesson-number {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--color-surface-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-sm);
  font-weight: var(--fw-bold);
  flex-shrink: 0;
}

.lesson-info { flex: 1; display: flex; flex-direction: column; }
.lesson-title { font-size: var(--text-base); font-weight: var(--fw-medium); }
.lesson-slug { font-size: var(--text-xs); color: var(--color-text-tertiary); font-family: var(--font-mono); }

.lesson-actions { display: flex; gap: var(--space-2); }
</style>
