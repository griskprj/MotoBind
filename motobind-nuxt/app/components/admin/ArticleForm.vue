<script setup lang="ts">
const props = defineProps<{ initialData?: any }>()
const emit = defineEmits<{ success: []; cancel: [] }>()

const api = useApi()
const toast = useToast()

const form = reactive({
  title: '',
  slug: '',
  category: 'repair',
  short_description: '',
  content: '',
  cover_url: '',
  tags: [] as string[],
})

// Теги
const newTag = ref('')
function addTag() {
  const tag = newTag.value.trim()
  if (tag && !form.tags.includes(tag)) {
    form.tags.push(tag)
    newTag.value = ''
  }
}
function removeTag(index: number) {
  form.tags.splice(index, 1)
}

// Инициализация
watch(() => props.initialData, (data) => {
  if (data) {
    Object.assign(form, data)
  }
}, { immediate: true })

// Загрузка обложки
const uploading = ref(false)
async function onFileChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  uploading.value = true
  try {
    const res = await api.admin.adminUploadCover(file)
    form.cover_url = res.url
    toast.success('Обложка загружена')
  } catch (e) {
    toast.error('Ошибка загрузки')
  } finally {
    uploading.value = false
  }
}

async function onSubmit() {
  try {
    if (props.initialData) {
      await api.admin.adminUpdateArticle(props.initialData.id, form)
    } else {
      await api.admin.adminCreateArticle(form)
    }
    toast.success('Статья сохранена')
    emit('success')
  } catch (e: any) {
    toast.error(e.message || 'Ошибка сохранения')
  }
}
</script>

<template>
  <form @submit.prevent="onSubmit" class="article-form">
    <BaseInput v-model="form.title" label="Название" required />
    <BaseInput v-model="form.slug" label="Slug (латиница)" required />

    <div class="form-row">
      <BaseSelect v-model="form.category" label="Категория" :options="[
        { value: 'driving', label: 'Вождение' },
        { value: 'repair', label: 'Ремонт' },
        { value: 'gear', label: 'Экипировка' },
        { value: 'first_aid', label: 'Первая помощь' },
        { value: 'law', label: 'Право' },
        { value: 'travel', label: 'Путешествия' },
      ]" />
    </div>

    <BaseTextarea v-model="form.short_description" label="Краткое описание" />

    <!-- Теги -->
    <div class="tags-section">
      <label class="field-label">Теги</label>
      <div class="tags-list">
        <span v-for="(tag, i) in form.tags" :key="i" class="tag">
          {{ tag }}
          <button type="button" class="tag-remove" @click="removeTag(i)">&times;</button>
        </span>
      </div>
      <div class="tag-add">
        <BaseInput v-model="newTag" placeholder="Добавить тег" @keydown.enter.prevent="addTag" />
        <BaseButton variant="secondary" @click="addTag">Добавить</BaseButton>
      </div>
    </div>

    <!-- Обложка -->
    <div class="cover-upload">
      <label class="field-label">Обложка</label>
      <div class="cover-actions">
        <input type="file" accept="image/*" class="visually-hidden" ref="coverInput" @change="onFileChange" />
        <BaseButton variant="secondary" :loading="uploading" @click="($refs.coverInput as HTMLInputElement)?.click()">
          Загрузить обложку
        </BaseButton>
        <div v-if="form.cover_url" class="cover-preview">
          <img :src="useMediaUrl()(form.cover_url)!" alt="Обложка" />
        </div>
      </div>
    </div>

    <!-- Контент (Markdown) -->
    <MarkdownEditor v-model="form.content" label="Контент статьи" />

    <div class="form-actions">
      <BaseButton variant="ghost" type="button" @click="emit('cancel')">Отмена</BaseButton>
      <BaseButton variant="primary" type="submit">Сохранить</BaseButton>
    </div>
  </form>
</template>

<style scoped lang="scss">
.article-form { display: flex; flex-direction: column; gap: var(--space-4); }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-4); }
.field-label { font-size: var(--text-sm); font-weight: var(--fw-medium); color: var(--color-text); margin-bottom: var(--space-1); display: block; }

.tags-section { display: flex; flex-direction: column; gap: var(--space-2); }
.tags-list { display: flex; flex-wrap: wrap; gap: var(--space-2); }
.tag {
  display: inline-flex; align-items: center; gap: var(--space-1);
  padding: 2px 8px; background: var(--color-brand-soft); color: var(--color-brand);
  border-radius: var(--radius-full); font-size: var(--text-xs);
}
.tag-remove { background: none; border: none; color: var(--color-brand); cursor: pointer; font-size: 14px; line-height: 1; }
.tag-add { display: flex; gap: var(--space-2); align-items: flex-end; }

.cover-upload { display: flex; flex-direction: column; gap: var(--space-2); }
.cover-actions { display: flex; gap: var(--space-3); align-items: flex-end; }
.cover-preview {
  width: 120px; height: 68px; border-radius: var(--radius-md); overflow: hidden; border: 1px solid var(--color-border);
  img { width: 100%; height: 100%; object-fit: cover; }
}

.form-actions { display: flex; justify-content: flex-end; gap: var(--space-3); padding-top: var(--space-4); }
</style>
