<template>
  <AppModal
    :is-open="isOpen"
    title="Смена пароля"
    subtitle="Для безопасности используйте надёжный пароль"
    icon="lock"
    @close="close"
  >
    <n-form ref="formRef" :model="form" :rules="rules">
      <n-form-item path="currentPassword" label="Текущий пароль">
        <n-input
          v-model:value="form.currentPassword"
          type="password"
          show-password-on="click"
          placeholder="Введите текущий пароль"
        />
      </n-form-item>

      <n-form-item path="newPassword" label="Новый пароль">
        <n-input
          v-model:value="form.newPassword"
          type="password"
          show-password-on="click"
          placeholder="Введите новый пароль"
        />
      </n-form-item>

      <n-form-item path="repeatPassword" label="Повторите новый пароль">
        <n-input
          v-model:value="form.repeatPassword"
          type="password"
          show-password-on="click"
          placeholder="Повторите новый пароль"
        />
      </n-form-item>

      <n-alert type="info" :bordered="false" title="Рекомендации:">
        <ul class="password-tips">
          <li>Минимум 8 символов</li>
          <li>Буквы в разных регистрах</li>
          <li>Цифры и специальные символы</li>
        </ul>
      </n-alert>
    </n-form>

    <template #actions>
      <AppButton variant="secondary" block @click="close">Отменить</AppButton>
      <AppButton variant="primary" block :loading="loading" @click="submit">
        Изменить пароль
      </AppButton>
    </template>
  </AppModal>
</template>

<script setup lang="ts">
import { reactive, ref, watch } from 'vue'
import type { FormInst, FormRules } from 'naive-ui'
import { useUserStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import { AppButton, AppModal } from '@/shared/ui'

const props = defineProps<{ isOpen: boolean }>()
const emit = defineEmits<{ close: [] }>()

const toast = useToast()
const userStore = useUserStore()
const formRef = ref<FormInst | null>(null)

const form = reactive({
  currentPassword: '',
  newPassword: '',
  repeatPassword: '',
})

const rules: FormRules = {
  currentPassword: [
    { required: true, message: 'Введите текущий пароль', trigger: 'blur' },
  ],
  newPassword: [
    { required: true, message: 'Введите новый пароль', trigger: 'blur' },
    { min: 6, message: 'Минимум 6 символов', trigger: 'blur' },
  ],
  repeatPassword: [
    { required: true, message: 'Повторите пароль', trigger: 'blur' },
    {
      validator: (_rule, value) => {
        if (value !== form.newPassword) return new Error('Пароли не совпадают')
        return true
      },
      trigger: ['blur', 'password-change'],
    },
  ],
}

const loading = ref(false)

watch(
  () => props.isOpen,
  (newVal) => {
    if (!newVal) resetForm()
  }
)

function resetForm() {
  form.currentPassword = ''
  form.newPassword = ''
  form.repeatPassword = ''
  loading.value = false
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

  if (form.newPassword === form.currentPassword) {
    toast.error('Новый пароль должен отличаться от текущего')
    return
  }

  loading.value = true
  try {
    await userStore.changePassword({
      currentPassword: form.currentPassword,
      newPassword: form.newPassword,
    })
    resetForm()
    emit('close')
    toast.success('Пароль изменён')
  } catch (err: any) {
    toast.error(err.response?.data?.message || 'Ошибка смены пароля')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.password-tips {
  margin: 4px 0 0;
  padding-left: 20px;
  font-size: 13px;
  line-height: 1.8;
}
</style>
