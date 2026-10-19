<template>
  <div class="admin-article-editor">
    <div class="admin-article-editor__head">
      <button type="button" class="back-btn" @click="goBack">
        <i class="fa fa-arrow-left" /> К статьям
      </button>
      <h2>{{ isNew ? 'Новая статья' : 'Редактирование статьи' }}</h2>
      <div class="admin-article-editor__head-actions">
        <button
          v-if="!isNew && store.currentArticle?.status === 'draft'"
          type="button"
          class="btn btn-secondary"
          :disabled="store.saving"
          @click="publish"
        >
          <i class="fa fa-check" /> Опубликовать
        </button>
        <button
          v-if="!isNew && store.currentArticle?.status === 'published'"
          type="button"
          class="btn btn-secondary"
          :disabled="store.saving"
          @click="archive"
        >
          <i class="fa fa-box-archive" /> В архив
        </button>
        <a
          v-if="!isNew && store.currentArticle?.status === 'published'"
          :href="`/learning/articles/${form.slug}`"
          target="_blank"
          class="btn btn-outline"
        >
          <i class="fa fa-external-link" /> Открыть
        </a>
      </div>
    </div>

    <div v-if="store.currentArticleLoading" class="admin-article-editor__loading">
      <i class="fa fa-spinner fa-spin" /> Загрузка...
    </div>

    <template v-else>
      <section class="admin-section">
        <h3>Основное</h3>
        <div class="form-grid">
          <div class="form-group form-group--full">
            <label>Название <span class="req">*</span></label>
            <input v-model="form.title" type="text" placeholder="Например: Как выбрать шлем" />
          </div>
          <div class="form-group">
            <label>Slug <span class="req">*</span></label>
            <input v-model="form.slug" type="text" placeholder="kak-vybrat-shlem" />
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
            <label>Теги</label>
            <div class="tags-input">
              <span v-for="(tag, idx) in form.tags" :key="idx" class="tag-chip">
                {{ tag }}
                <button type="button" class="tag-chip__remove" @click="removeTag(idx)">
                  <i class="fa fa-times" />
                </button>
              </span>
              <input
                v-model="tagInput"
                type="text"
                placeholder="Добавить тег и Enter"
                class="tags-input__field"
                @keydown.enter.prevent="addTag"
                @keydown.,.prevent="addTag"
              />
            </div>
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
            <label>Контент (markdown) <span class="req">*</span></label>
            <MdEditor
              v-model="form.content"
              :toolbars="editorToolbars"
              language="ru-RU"
              preview-theme="github"
              style="height: 500px"
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
            {{ isNew ? 'Создать статью' : 'Сохранить' }}
          </button>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { useAdminLearningStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import { resolveMedia } from '@/utils/mediaUrl'

const route = useRoute()
const router = useRouter()
const store = useAdminLearningStore()
const toast = useToast()

const isNew = computed(() => !route.params.id)
const articleId = computed(() => Number(route.params.id))

const form = reactive({
  title: '',
  slug: '',
  short_description: '',
  content: '',
  category: '',
  tags: [],
  cover_url: '',
})

const tagInput = ref('')

const isFormValid = computed(() => {
  return form.title.trim() && form.slug.trim() && form.category && form.content.trim()
})

const editorToolbars = [
  'bold', 'underline', 'italic', '-', 'title', 'strikeThrough', 'sub', 'sup', 'quote', 'unorderedList', 'orderedList', 'task',
  '-', 'code', 'link', 'image', 'table',
  '=', 'preview', 'fullscreen',
]

onMounted(load)

async function load() {
  if (isNew.value) return
  try {
    const data = await store.loadArticle(articleId.value)
    Object.assign(form, {
      title: data.title,
      slug: data.slug,
      short_description: data.short_description || '',
      content: data.content || '',
      category: data.category,
      tags: Array.isArray(data.tags) ? [...data.tags] : [],
      cover_url: data.cover_url || '',
    })
  } catch {
    toast.error('Не удалось загрузить статью')
    goBack()
  }
}

function addTag() {
  const val = tagInput.value.trim()
  if (!val) return
  if (!form.tags.includes(val)) {
    form.tags.push(val)
  }
  tagInput.value = ''
}

function removeTag(idx) {
  form.tags.splice(idx, 1)
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
      content: form.content,
      category: form.category,
      tags: form.tags,
      cover_url: form.cover_url || null,
    }

    if (isNew.value) {
      const created = await store.createArticle(payload)
      toast.success('Статья создана')
      router.replace({
        name: 'admin-learning-article',
        params: { id: created.id },
      })
    } else {
      await store.updateArticle(articleId.value, payload)
      toast.success('Сохранено')
    }
  } catch (err) {
    toast.error(err.response?.data?.error || 'Не удалось сохранить')
  }
}

async function publish() {
  try {
    await store.publishArticle(articleId.value)
    toast.success('Статья опубликована')
  } catch (err) {
    toast.error(err.response?.data?.error || 'Ошибка публикации')
  }
}

async function archive() {
  try {
    await store.archiveArticle(articleId.value)
    toast.success('Статья в архиве')
  } catch {
    toast.error('Не удалось архивировать')
  }
}

function goBack() {
  router.push({ name: 'admin-learning-articles' })
}
</script>

<style scoped>
.admin-article-editor {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.admin-article-editor__head {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.admin-article-editor__head h2 {
  margin: 0;
  font-size: var(--text-xl);
  flex: 1;
  min-width: 0;
}

.admin-article-editor__head-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.admin-article-editor__loading {
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

.form-hint {
  font-size: 11px;
  color: var(--text-muted);
}

.req {
  color: var(--danger-text);
}

/* Теги */
.tags-input {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  padding: 6px 8px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--bg-input);
  min-height: 40px;
  align-items: center;
}

.tags-input:focus-within {
  border-color: var(--accent);
}

.tag-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 8px 3px 10px;
  background: var(--accent-trans);
  color: var(--accent-text);
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: var(--fw-medium);
}

.tag-chip__remove {
  width: 16px;
  height: 16px;
  min-height: 16px;
  padding: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: inherit;
  cursor: pointer;
  opacity: 0.6;
  font-size: 9px;
  border-radius: 50%;
}

.tag-chip__remove:hover {
  opacity: 1;
  background: rgba(0, 0, 0, 0.1);
}

.tags-input__field {
  flex: 1;
  min-width: 150px;
  border: none;
  background: transparent;
  padding: 4px;
  font-size: var(--text-sm);
  color: var(--text-primary);
  outline: none;
  font-family: inherit;
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

@media (max-width: 640px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
