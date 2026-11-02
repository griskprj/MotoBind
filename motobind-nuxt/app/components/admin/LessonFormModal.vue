<script setup lang="ts">
const props = defineProps<{
  courseId: number
  lesson?: any
}>()

const emit = defineEmits<{
  close: []
  saved: []
}>()

const api = useApi()
const toast = useToast()

const form = reactive({
  title: '',
  slug: '',
  order: 1,
  content: '',
  video_url: '',
  video_duration: 0,
  is_free_preview: false,
})

onMounted(() => {
  if (props.lesson) {
    Object.assign(form, props.lesson)
  }
})

async function onSubmit() {
  try {
    if (props.lesson) {
      await api.admin.adminUpdateLesson(props.lesson.id, form)
    } else {
      await api.admin.adminCreateLesson(props.courseId, form)
    }
    toast.success('Урок сохранён')
    emit('saved')
    emit('close')
  } catch (e: any) {
    toast.error(e.message || 'Ошибка сохранения')
  }
}
</script>

<template>
  <BaseModal :title="lesson ? 'Редактировать урок' : 'Новый урок'" size="md" @close="emit('close')">
    <form @submit.prevent="onSubmit" class="lesson-form">
      <BaseInput v-model="form.title" label="Название" required />
      <BaseInput v-model="form.slug" label="Slug" required />
      <BaseInput v-model="form.order" type="number" label="Порядок" required />

      <BaseInput v-model="form.video_url" label="Видео URL (VK)" />
      <BaseInput v-model="form.video_duration" type="number" label="Длительность видео (сек)" />

      <BaseCheckbox v-model="form.is_free_preview" label="Бесплатный превью-урок" />

      <MarkdownEditor v-model="form.content" label="Контент (Markdown)" />
    </form>
    <template #footer>
      <BaseButton variant="ghost" size="sm" @click="emit('close')">Отмена</BaseButton>
      <BaseButton variant="primary" size="sm" @click="onSubmit">Сохранить</BaseButton>
    </template>
  </BaseModal>
</template>

<style scoped lang="scss">
.lesson-form { display: flex; flex-direction: column; gap: var(--space-4); }
</style>
