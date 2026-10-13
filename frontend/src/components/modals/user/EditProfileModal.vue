<template>
  <AppModal
    :is-open="isOpen"
    title="Редактирование профиля"
    subtitle="Эти данные будут видны другим пользователям"
    icon="user"
    size="lg"
    @close="close"
  >
    <n-form ref="formRef" :model="form" :rules="rules">
      <n-form-item path="username" label="Имя пользователя">
        <n-input v-model:value="form.username" placeholder="Введите имя" />
      </n-form-item>

      <n-form-item path="email" label="Email">
        <n-input v-model:value="form.email" placeholder="user@example.com" />
      </n-form-item>

      <n-form-item path="bio" label="О себе">
        <n-input
          v-model:value="form.bio"
          type="textarea"
          :rows="3"
          :maxlength="1000"
          show-count
          placeholder="Расскажите о себе..."
        />
      </n-form-item>

      <div class="form-row">
        <n-form-item path="location" label="Город/Регион">
          <n-input v-model:value="form.location" placeholder="Москва" />
        </n-form-item>
        <n-form-item path="motorcycle" label="Мой мотоцикл">
          <n-input v-model:value="form.motorcycle" placeholder="BMW S1000RR" />
        </n-form-item>
      </div>

      <n-form-item path="experience" label="Опыт вождения">
        <n-select
          v-model:value="form.experience"
          :options="experienceOptions"
          placeholder="Не указано"
          clearable
        />
      </n-form-item>
    </n-form>

    <template #actions>
      <AppButton
        variant="secondary"
        block
        @click="close"
        style="margin-bottom: 8px;"
      >
        Отменить
      </AppButton>
      <AppButton
        variant="primary"
        block
        :loading="loading"
        @click="submit"
      >
        Сохранить
      </AppButton>
    </template>
  </AppModal>
</template>

<script setup lang="ts">
import { reactive, ref, watch } from 'vue'
import type { FormInst, FormRules } from 'naive-ui'
import { useUserStore } from '@/stores'
import { useToast } from '@/shared/composables/useToast'
import { AppButton, AppModal } from '@/shared/ui'

const props = defineProps<{
  isOpen: boolean
  user: Record<string, any> | null
}>()

const emit = defineEmits<{ close: [] }>()

const toast = useToast()
const userStore = useUserStore()
const formRef = ref<FormInst | null>(null)

const form = reactive({
  username: '',
  email: '',
  bio: '',
  location: '',
  motorcycle: '',
  experience: 'beginner',
})

const rules: FormRules = {
  username: [
    { required: true, message: 'Введите имя', trigger: 'blur' },
    { min: 2, message: 'Минимум 2 символа', trigger: 'blur' },
  ],
  email: [
    { required: true, message: 'Введите email', trigger: 'blur' },
    { type: 'email', message: 'Некорректный email', trigger: 'blur' },
  ],
}

const experienceOptions = [
  { label: 'Новичок', value: 'beginner' },
  { label: 'Опытный', value: 'intermediate' },
  { label: 'Эксперт', value: 'expert' },
]

const loading = ref(false)

watch(
  () => props.isOpen,
  (newVal) => {
    if (newVal && props.user) loadFormData()
    if (!newVal) loading.value = false
  },
  { immediate: true }
)

function loadFormData() {
  if (!props.user) return
  Object.assign(form, {
    username: props.user.username || '',
    email: props.user.email || '',
    bio: props.user.bio || '',
    location: props.user.location || '',
    motorcycle: props.user.motorcycle || '',
    experience: props.user.experience || 'beginner',
  })
}

function close() {
  if (loading.value) return
  emit('close')
}

async function submit() {
  try {
    await formRef.value?.validate()
  } catch {
    return
  }

  loading.value = true
  try {
    await userStore.updateProfile({
      username: form.username.trim(),
      email: form.email.trim(),
      bio: form.bio?.trim() || '',
      location: form.location?.trim() || '',
      motorcycle: form.motorcycle?.trim() || '',
      experience: form.experience || 'beginner',
    })
    emit('close')
    toast.success('Профиль обновлён')
  } catch (err: any) {
    toast.error(err.response?.data?.message || 'Ошибка обновления')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.social-links-editor {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

.social-link-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.social-link-row > :last-child {
  flex: 1;
}

.social-icon {
  width: 24px;
  font-size: 18px;
  color: var(--text-muted);
  text-align: center;
}

@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
