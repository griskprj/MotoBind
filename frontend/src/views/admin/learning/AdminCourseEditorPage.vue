<template>
  <div class="admin-course-editor">
    <div class="admin-course-editor__head">
      <button type="button" class="back-btn" @click="goBack">
        <i class="fa fa-arrow-left" /> К курсам
      </button>
      <h2>{{ isNew ? 'Новый курс' : 'Редактирование курса' }}</h2>
      <div class="admin-course-editor__head-actions">
        <button
          v-if="!isNew && store.currentCourse?.status === 'draft'"
          type="button"
          class="btn btn-secondary"
          :disabled="store.saving"
          @click="publish"
        >
          <i class="fa fa-check" /> Опубликовать
        </button>
        <button
          v-if="!isNew && store.currentCourse?.status === 'published'"
          type="button"
          class="btn btn-secondary"
          :disabled="store.saving"
          @click="archive"
        >
          <i class="fa fa-box-archive" /> В архив
        </button>
      </div>
    </div>

    <div v-if="store.currentCourseLoading" class="admin-course-editor__loading">
      <i class="fa fa-spinner fa-spin" /> Загрузка...
    </div>

    <template v-else>
      <!-- Основные поля курса -->
      <section class="admin-section">
        <h3>Основное</h3>
        <div class="form-grid">
          <div class="form-group form-group--full">
            <label>Название <span class="req">*</span></label>
            <input v-model="form.title" type="text" placeholder="Например: Основы вождения" />
          </div>
          <div class="form-group">
            <label>Slug <span class="req">*</span></label>
            <input v-model="form.slug" type="text" placeholder="osnovy-vozhdeniya" />
          </div>
          <div class="form-group">
            <label>Категория <span class="req">*</span></label>
            <select v-model="form.category">
              <option value="">— выбрать —</option>
              <option value="riding">Вождение</option>
              <option value="repair">Ремонт</option>
              <option value="gear">Экипировка</option>
              <option value="first_aid">Первая помощь</option>
              <option value="law">Право</option>
              <option value="travel">Путешествия</option>
            </select>
          </div>
          <div class="form-group">
            <label>Уровень</label>
            <select v-model="form.level">
              <option value="beginner">Начальный</option>
              <option value="intermediate">Средний</option>
              <option value="advanced">Продвинутый</option>
            </select>
          </div>
          <div class="form-group">
            <label>Цена (₽)</label>
            <input
              :value="priceRub"
              type="number"
              min="0"
              @input="onPriceInput"
            />
            <span class="form-hint">0 — курс бесплатный</span>
          </div>
          <div class="form-group form-group--full">
            <label>Краткое описание</label>
            <input
              v-model="form.short_description"
              type="text"
              maxlength="256"
              placeholder="Одно предложение для карточки"
            />
          </div>
          <div class="form-group form-group--full">
            <label>Обложка</label>
            <div class="cover-upload">
              <div v-if="form.cover_url" class="cover-preview">
                <img :src="resolveMedia(form.cover_url)" alt="Обложка" />
                <button type="button" class="cover-remove" @click="form.cover_url = ''">
                  <i class="fa fa-times" />
                </button>
              </div>
              <label class="cover-drop">
                <input
                  type="file"
                  accept="image/*"
                  style="display: none"
                  @change="onCoverUpload"
                />
                <i class="fa fa-cloud-upload" />
                <span>{{ form.cover_url ? 'Заменить' : 'Загрузить обложку' }}</span>
              </label>
            </div>
          </div>
          <div class="form-group form-group--full">
            <label>Описание (markdown)</label>
            <MdEditor
              v-model="form.description"
              :toolbars="editorToolbars"
              language="ru-RU"
              preview-theme="github"
              style="height: 400px"
            />
          </div>
        </div>

        <div class="admin-section__actions">
          <button
            type="button"
            class="btn btn-primary"
            :disabled="store.saving || !isFormValid"
            @click="save"
          >
            <i class="fa fa-save" />
            {{ isNew ? 'Создать курс' : 'Сохранить' }}
          </button>
        </div>
      </section>

      <!-- Уроки (только для существующего курса) -->
      <section v-if="!isNew" class="admin-section">
        <div class="admin-section__head">
          <h3>Уроки ({{ lessons.length }})</h3>
          <button type="button" class="btn btn-secondary" @click="openLessonModal()">
            <i class="fa fa-plus" /> Добавить урок
          </button>
        </div>

        <div v-if="!lessons.length" class="admin-empty">
          <p>Уроков пока нет. Добавьте первый.</p>
        </div>

        <div v-else class="lesson-admin-list">
          <div
            v-for="l in lessons"
            :key="l.id"
            class="lesson-admin-item"
          >
            <div class="lesson-admin-item__num">{{ l.order }}</div>
            <div class="lesson-admin-item__body">
              <div class="lesson-admin-item__title">{{ l.title }}</div>
              <div class="lesson-admin-item__meta">
                <span class="lesson-admin-item__slug">{{ l.slug }}</span>
                <span v-if="l.is_free_preview" class="badge badge--success">Превью</span>
                <span v-if="l.has_video" class="badge">Видео</span>
              </div>
            </div>
            <div class="lesson-admin-item__actions">
              <button
                type="button"
                class="icon-btn"
                title="Редактировать"
                @click="openLessonModal(l)"
              >
                <i class="fa fa-pen" />
              </button>
              <button
                type="button"
                class="icon-btn icon-btn--danger"
                title="Удалить"
                @click="deleteLesson(l)"
              >
                <i class="fa fa-trash" />
              </button>
            </div>
          </div>
        </div>
      </section>
    </template>

    <!-- Модалка урока -->
    <BaseModal
      :is-open="lessonModalOpen"
      :title="lessonForm.id ? 'Редактирование урока' : 'Новый урок'"
      size="lg"
      @close="closeLessonModal"
    >
      <div class="form-grid">
        <div class="form-group form-group--full">
          <label>Название <span class="req">*</span></label>
          <input v-model="lessonForm.title" type="text" />
        </div>
        <div class="form-group">
          <label>Slug <span class="req">*</span></label>
          <input v-model="lessonForm.slug" type="text" />
        </div>
        <div class="form-group">
          <label>Порядок</label>
          <input
            v-model.number="lessonForm.order"
            type="number"
            min="1"
            placeholder="Авто"
          />
        </div>
        <div class="form-group form-group--full">
          <label>
            <input v-model="lessonForm.is_free_preview" type="checkbox" />
            Бесплатный превью-урок
          </label>
        </div>
        <div class="form-group form-group--full">
          <label>Видео URL (VK Video embed)</label>
          <input
            v-model="lessonForm.video_url"
            type="text"
            placeholder="https://vk.com/video_ext.php?oid=..."
          />
        </div>
        <div class="form-group">
          <label>Длительность видео (сек)</label>
          <input v-model.number="lessonForm.video_duration" type="number" min="0" />
        </div>
        <div class="form-group form-group--full">
          <label>Контент (markdown) <span class="req">*</span></label>
          <MdEditor
            v-model="lessonForm.content"
            :toolbars="editorToolbars"
            language="ru-RU"
            preview-theme="github"
            style="height: 350px"
          />
        </div>
      </div>

      <template #actions>
        <button type="button" class="btn btn-secondary" @click="closeLessonModal">
          Отмена
        </button>
        <button
          type="button"
          class="btn btn-primary"
          :disabled="store.saving || !isLessonValid"
          @click="saveLesson"
        >
          <i class="fa fa-save" />
          Сохранить
        </button>
      </template>
    </BaseModal>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import BaseModal from '@/components/ui/BaseModal.vue'
import { useAdminLearningStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import { resolveMedia } from '@/utils/mediaUrl'

const route = useRoute()
const router = useRouter()
const store = useAdminLearningStore()
const toast = useToast()

const isNew = computed(() => !route.params.id)
const courseId = computed(() => Number(route.params.id))

const form = reactive({
  title: '',
  slug: '',
  short_description: '',
  description: '',
  category: '',
  level: 'beginner',
  cover_url: '',
  price: 0,
})

const priceRub = computed(() => Math.floor(form.price / 100))

const isFormValid = computed(() => {
  return form.title.trim() && form.slug.trim() && form.category
})

const lessons = computed(() => store.currentCourse?.lessons || [])

const editorToolbars = [
  'bold', 'underline', 'italic', '-', 'title', 'strikeThrough', 'sub', 'sup', 'quote', 'unorderedList', 'orderedList', 'task',
  '-', 'code', 'link', 'image', 'table',
  '=', 'preview', 'fullscreen',
]

onMounted(load)

async function load() {
  if (isNew.value) return
  try {
    const data = await store.loadCourse(courseId.value)
    Object.assign(form, {
      title: data.title,
      slug: data.slug,
      short_description: data.short_description || '',
      description: data.description || '',
      category: data.category,
      level: data.level,
      cover_url: data.cover_url || '',
      price: data.price || 0,
    })
  } catch {
    toast.error('Не удалось загрузить курс')
    goBack()
  }
}

function onPriceInput(e) {
  form.price = (Number(e.target.value) || 0) * 100
}

async function onCoverUpload(e) {
  const file = e.target.files?.[0]
  if (!file) return
  try {
    const url = await store.uploadCover(file)
    form.cover_url = url
  } catch {
    toast.error('Не удалось загрузить обложку')
  }
}

async function save() {
  try {
    const payload = {
      title: form.title,
      slug: form.slug,
      short_description: form.short_description || null,
      description: form.description || null,
      category: form.category,
      level: form.level,
      cover_url: form.cover_url || null,
      price: form.price,
      is_free: form.price === 0,
    }

    if (isNew.value) {
      const created = await store.createCourse(payload)
      toast.success('Курс создан')
      router.replace({
        name: 'admin-learning-course',
        params: { id: created.id },
      })
    } else {
      await store.updateCourse(courseId.value, payload)
      toast.success('Сохранено')
    }
  } catch (err) {
    toast.error(err.response?.data?.error || 'Не удалось сохранить')
  }
}

async function publish() {
  try {
    await store.publishCourse(courseId.value)
    toast.success('Курс опубликован')
  } catch (err) {
    toast.error(err.response?.data?.error || 'Ошибка публикации')
  }
}

async function archive() {
  try {
    await store.archiveCourse(courseId.value)
    toast.success('Курс в архиве')
  } catch (err) {
    toast.error('Не удалось архивировать')
  }
}

function goBack() {
  router.push({ name: 'admin-learning-courses' })
}

// ===== Модалка урока =====
const lessonModalOpen = ref(false)
const lessonForm = reactive({
  id: null,
  title: '',
  slug: '',
  order: null,
  content: '',
  video_url: '',
  video_duration: null,
  is_free_preview: false,
})

const isLessonValid = computed(() => {
  return lessonForm.title.trim() && lessonForm.slug.trim() && lessonForm.content.trim()
})

async function openLessonModal(lesson = null) {
  if (lesson) {
    try {
      const full = await store.loadLesson(lesson.id)
      Object.assign(lessonForm, {
        id: full.id,
        title: full.title,
        slug: full.slug,
        order: full.order,
        content: full.content || '',
        video_url: full.video_url || '',
        video_duration: full.video_duration || null,
        is_free_preview: full.is_free_preview,
      })
    } catch {
      toast.error('Не удалось загрузить урок')
      return
    }
  } else {
    Object.assign(lessonForm, {
      id: null,
      title: '',
      slug: '',
      order: null,
      content: '',
      video_url: '',
      video_duration: null,
      is_free_preview: false,
    })
  }
  lessonModalOpen.value = true
}

function closeLessonModal() {
  lessonModalOpen.value = false
}

async function saveLesson() {
  try {
    const payload = {
      title: lessonForm.title,
      slug: lessonForm.slug,
      order: lessonForm.order || null,
      content: lessonForm.content,
      video_url: lessonForm.video_url || null,
      video_duration: lessonForm.video_duration || null,
      is_free_preview: lessonForm.is_free_preview,
    }

    if (lessonForm.id) {
      await store.updateLesson(lessonForm.id, payload)
      await store.loadCourse(courseId.value)
      toast.success('Урок обновлён')
    } else {
      await store.createLesson(courseId.value, payload)
      toast.success('Урок создан')
    }
    closeLessonModal()
  } catch (err) {
    toast.error(err.response?.data?.error || 'Не удалось сохранить урок')
  }
}

async function deleteLesson(lesson) {
  if (!confirm(`Удалить урок «${lesson.title}»?`)) return
  try {
    await store.deleteLesson(courseId.value, lesson.id)
    toast.success('Урок удалён')
  } catch {
    toast.error('Не удалось удалить урок')
  }
}
</script>

<style scoped>
.admin-course-editor {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.admin-course-editor__head {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.admin-course-editor__head h2 {
  margin: 0;
  font-size: var(--text-xl);
  flex: 1;
  min-width: 0;
}

.admin-course-editor__head-actions {
  display: flex;
  gap: 8px;
}

.admin-course-editor__loading {
  padding: 40px;
  text-align: center;
  color: var(--text-muted);
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 0;
  background: none;
  border: none;
  color: var(--text-secondary);
  font-family: inherit;
  font-size: var(--text-sm);
  cursor: pointer;
  min-height: 0;
}

.back-btn:hover {
  color: var(--accent-text);
}

.admin-section {
  padding: var(--space-3);
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.admin-section h3 {
  margin: 0;
  font-size: var(--text-base);
}

.admin-section__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
}

.admin-section__actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  padding-top: var(--space-2);
  border-top: 1px solid var(--border-light);
}

/* Форма */
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.form-group--full {
  grid-column: 1 / -1;
}

.form-group label {
  font-size: var(--text-xs);
  font-weight: var(--fw-semibold);
  color: var(--text-secondary);
}

.form-group input,
.form-group select {
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--bg-input);
  color: var(--text-primary);
  font-family: inherit;
  font-size: var(--text-sm);
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--accent);
}

.form-group input[type="checkbox"] {
  width: auto;
  margin-right: 6px;
}

.form-hint {
  font-size: 11px;
  color: var(--text-muted);
}

.req {
  color: var(--danger-text);
}

/* Обложка */
.cover-upload {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  flex-wrap: wrap;
}

.cover-preview {
  position: relative;
  width: 200px;
  aspect-ratio: 16/9;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--border-light);
}

.cover-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-remove {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 24px;
  height: 24px;
  min-height: 24px;
  background: rgba(0, 0, 0, 0.6);
  border: none;
  border-radius: 50%;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.cover-drop {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border: 1px dashed var(--border-color);
  border-radius: var(--radius-md);
  cursor: pointer;
  color: var(--text-secondary);
  font-size: var(--text-sm);
  min-height: 44px;
}

.cover-drop:hover {
  border-color: var(--accent);
  color: var(--accent-text);
}

/* Список уроков в админке */
.lesson-admin-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.lesson-admin-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
}

.lesson-admin-item__num {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: var(--fw-semibold);
  color: var(--text-secondary);
  flex-shrink: 0;
}

.lesson-admin-item__body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.lesson-admin-item__title {
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.lesson-admin-item__meta {
  display: flex;
  gap: 8px;
  font-size: 11px;
  color: var(--text-muted);
  align-items: center;
  flex-wrap: wrap;
}

.lesson-admin-item__slug {
  font-family: var(--font-mono);
}

.lesson-admin-item__actions {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
}

.admin-empty {
  padding: 24px;
  text-align: center;
  color: var(--text-muted);
  font-size: var(--text-sm);
  border: 1px dashed var(--border-color);
  border-radius: var(--radius-md);
}

.badge {
  display: inline-flex;
  padding: 2px 8px;
  border-radius: var(--radius-full);
  font-size: 10px;
  font-weight: var(--fw-semibold);
  background: var(--bg-primary);
  color: var(--text-secondary);
}

.badge--success {
  background: var(--success-trans);
  color: var(--success-text);
}

@media (max-width: 640px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
