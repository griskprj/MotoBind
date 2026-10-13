<template>
  <AppModal
    :is-open="isOpen"
    title="Удаление аккаунта"
    subtitle="Это действие нельзя отменить"
    icon="user-slash"
    variant="danger"
    @close="close"
  >
    <n-alert type="error" :bordered="false" title="Внимание!">
      Будут удалены все ваши данные: мотоциклы, записи об обслуживании, мануалы, фото.
      Восстановление невозможно.
    </n-alert>

    <n-form ref="formRef" :model="form" :rules="rules" class="mt-3">
      <n-form-item path="password" label="Введите пароль для подтверждения">
        <n-input
          v-model:value="form.password"
          type="password"
          show-password-on="click"
          placeholder="Текущий пароль"
          @keydown.enter="submit"
        />
      </n-form-item>
    </n-form>

    <template #actions>
      <AppButton variant="secondary" block @click="close">Отменить</AppButton>
      <AppButton
        variant="danger"
        block
        :loading="loading"
        @click="submit"
      >
        Удалить аккаунт
      </AppButton>
    </template>
  </AppModal>
</template>

<script setup lang="ts">
import { reactive, ref, watch } from 'vue'
import type { FormInst, FormRules } from 'naive-ui'
import { useRouter } from 'vue-router'
import { useUserStore, useAuthStore } from '@/stores'
import { useToast } from '@/shared/composables/useToast'
import { AppButton, AppModal } from '@/shared/ui'

const props = defineProps<{ isOpen: boolean }>()
const emit = defineEmits<{ close: [] }>()

const router = useRouter()
const toast = useToast()
const userStore = useUserStore()
const authStore = useAuthStore()
const formRef = ref<FormInst | null>(null)

const form = reactive({ password: '' })

const rules: FormRules = {
  password: [
    { required: true, message: 'Введите пароль', trigger: 'blur' },
    { min: 6, message: 'Минимум 6 символов', trigger: 'blur' },
  ],
}

const loading = ref(false)

watch(
  () => props.isOpen,
  (newVal) => {
    if (!newVal) {
      form.password = ''
      loading.value = false
    }
  }
)

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

  if (!confirm('Вы действительно хотите удалить аккаунт? Это действие нельзя отменить!')) {
    return
  }

  loading.value = true
  try {
    await userStore.deleteAccount(form.password)
    emit('close')
    authStore.logout()
    router.push('/landing')
  } catch (err: any) {
    toast.error(err.response?.data?.message || 'Ошибка удаления аккаунта')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.mt-3 {
  margin-top: 16px;
}
</style>
