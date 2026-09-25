<template>
  <BaseModal
    :is-open="isOpen"
    title="Смена пароля"
    subtitle="Для безопасности используйте надёжный пароль"
    icon="lock"
    variant="default"
    size="md"
    @close="close"
  >
    <form @submit.prevent="submit" class="form-stack">
      <BaseInput
        v-model="form.currentPassword"
        type="password"
        label="Текущий пароль"
        placeholder="Введите текущий пароль"
        autocomplete="current-password"
        required
      />

      <BaseInput
        v-model="form.newPassword"
        type="password"
        label="Новый пароль"
        placeholder="Введите новый пароль"
        autocomplete="new-password"
        required
      />

      <BaseInput
        v-model="form.repeatPassword"
        type="password"
        label="Повторите новый пароль"
        placeholder="Повторите новый пароль"
        autocomplete="new-password"
        :error="repeatError"
        required
      />

      <div class="modal-info-block info">
        <div class="modal-info-icon">
          <i class="fa fa-shield-alt"></i>
        </div>
        <div>
          <p class="modal-info-text">
            <strong>Рекомендации по созданию надёжного пароля:</strong>
          </p>
          <ul class="password-tips">
            <li>Минимум 8 символов</li>
            <li>Используйте буквы в разных регистрах</li>
            <li>Добавьте цифры и специальные символы</li>
            <li>Не используйте личную информацию</li>
          </ul>
        </div>
      </div>
    </form>

    <template #actions>
      <BaseButton variant="secondary" block type="button" @click="close">
        Отменить
      </BaseButton>
      <BaseButton
        variant="primary"
        icon="fa fa-key"
        block
        type="submit"
        :disabled="!isFormValid"
        :loading="loading"
        @click="submit"
      >
        Изменить пароль
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { BaseModal, BaseButton, BaseInput } from '@/components/ui'
import { useToast } from '@/composables/useToast'
import { useUserStore } from '@/stores'

const props = defineProps({
  isOpen: { type: Boolean, required: true, default: false },
})

const emit = defineEmits(['close'])
const toast = useToast()
const userStore = useUserStore()

const form = reactive({
  currentPassword: '',
  newPassword: '',
  repeatPassword: '',
})

const loading = ref(false)

const repeatError = computed(() => {
  if (!form.repeatPassword) return ''
  if (form.newPassword !== form.repeatPassword) return 'Пароли не совпадают'
  return ''
})

const isFormValid = computed(() => {
  return (
    form.currentPassword &&
    form.currentPassword.length >= 6 &&
    form.newPassword &&
    form.newPassword.length >= 6 &&
    form.repeatPassword &&
    form.newPassword === form.repeatPassword &&
    form.newPassword !== form.currentPassword
  )
})

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
  if (!form.currentPassword) {
    toast.error('Введите текущий пароль')
    return
  }
  if (!form.newPassword || form.newPassword.length < 6) {
    toast.error('Новый пароль должен содержать минимум 6 символов')
    return
  }
  if (form.newPassword !== form.repeatPassword) {
    toast.error('Новые пароли не совпадают')
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
    toast.success('Пароль успешно изменён')
  } catch (err) {
    console.error('Failed to change password:', err)
    toast.error(err.response?.data?.message || 'Ошибка при смене пароля')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.form-stack {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.modal-info-block {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 10px;
}

.modal-info-block.info {
  background: var(--accent-trans);
  border: 1px solid var(--accent-light);
}

.modal-info-icon {
  font-size: 18px;
  color: var(--accent-text);
  flex-shrink: 0;
  margin-top: 2px;
}

.modal-info-text {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0 0 4px 0;
  line-height: 1.5;
}

.password-tips {
  margin: 4px 0 0 0;
  padding-left: 20px;
  color: var(--text-muted);
  font-size: 13px;
  line-height: 1.8;
}

.password-tips li {
  list-style-type: disc;
}

@media (max-width: 640px) {
  .modal-info-block {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .modal-info-icon {
    margin-top: 0;
  }

  .password-tips {
    text-align: left;
    padding-left: 16px;
  }
}
</style>
