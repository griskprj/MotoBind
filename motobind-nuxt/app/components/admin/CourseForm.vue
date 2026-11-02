<script setup lang="ts">
const props = defineProps<{ initialData?: any }>()
const emit = defineEmits<{ success: []; cancel: [] }>()

const api = useApi()
const toast = useToast()

const form = reactive({
  title: '',
  slug: '',
  category: 'Вождение',
  level: 'beginner',
  price: 0,
  short_description: '',
  description: '',
  cover_url: '',
})

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
      await api.admin.adminUpdateCourse(props.initialData.id, form)
    } else {
      await api.admin.adminCreateCourse(form)
    }
    toast.success('Курс сохранён')
    emit('success')
  } catch (e) {
    toast.error('Ошибка сохранения')
  }
}
</script>

<template>
  <form @submit.prevent="onSubmit" class="course-form">
    <BaseInput v-model="form.title" label="Название" required />
    <BaseInput v-model="form.slug" label="Slug (URL)" required />

    <div class="form-row">
      <BaseSelect
        v-model="form.category"
        label="Категория"
        :options="[
          { value: 'driving', label: 'Вождение' },
          { value: 'repair', label: 'Ремонт' },
          { value: 'gear', label: 'Экипировка' },
          { value: 'first_aid', label: 'Первая помощь' },
          { value: 'law', label: 'Право' },
          { value: 'travel', label: 'Путешествия' },
        ]"
      />

      <BaseSelect v-model="form.level" label="Уровень" :options="[
        { value: 'beginner', label: 'Начальный' },
        { value: 'intermediate', label: 'Средний' },
        { value: 'advanced', label: 'Продвинутый' },
      ]" />
    </div>

    <BaseInput v-model="form.price" type="number" label="Цена (₽)" />

    <BaseTextarea v-model="form.short_description" label="Краткое описание" />

    <!-- Обложка -->
    <div class="cover-upload">
      <label class="field-label">Обложка</label>
      <div class="cover-actions">
        <input type="file" accept="image/*" class="visually-hidden" @change="onFileChange" />
        <BaseButton variant="secondary" :loading="uploading" @click="($event.target as HTMLInputElement).click()">
          Загрузить обложку
        </BaseButton>
        <div v-if="form.cover_url" class="cover-preview">
          <img :src="useMediaUrl()(form.cover_url)!" alt="Обложка" />
        </div>
      </div>
    </div>

    <!-- Описание (Markdown) -->
    <MarkdownEditor v-model="form.description" label="Полное описание" />

    <div class="form-actions">
      <BaseButton variant="ghost" type="button" @click="emit('cancel')">Отмена</BaseButton>
      <BaseButton variant="primary" type="submit">Сохранить</BaseButton>
    </div>
  </form>
</template>

<style scoped lang="scss">
.course-form { display: flex; flex-direction: column; gap: var(--space-4); }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-4); }
.cover-upload { display: flex; flex-direction: column; gap: var(--space-2); }
.cover-actions { display: flex; gap: var(--space-3); align-items: flex-end; }
.cover-preview {
  width: 120px;
  height: 68px;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--color-border);
  img { width: 100%; height: 100%; object-fit: cover; }
}
.form-actions { display: flex; justify-content: flex-end; gap: var(--space-3); padding-top: var(--space-4); }
</style>
