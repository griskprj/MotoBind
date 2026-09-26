<template>
  <BaseModal
    :is-open="isOpen"
    title="Добавить пользователя"
    subtitle="Заполните информацию о новом пользователе"
    icon="user"
    variant="success"
    size="md"
    @close="close"
  >
    <form @submit.prevent="submit" class="form-stack">
      <BaseInput
        v-model="form.username"
        label="Имя"
        placeholder="Введите имя пользователя"
        required
      />

      <BaseInput
        v-model="form.email"
        type="email"
        label="Email"
        placeholder="user@example.com"
        required
      />

      <div class="form-row">
        <BaseSelect
          v-model="form.role"
          label="Роль"
        >
          <option value="motorcyclist">Мотоциклист</option>
          <option value="club_member">Член мотоклуба</option>
          <option value="admin">Админ</option>
        </BaseSelect>

        <BaseSelect
          v-model="form.status"
          label="Статус"
        >
          <option value="active">Активен</option>
          <option value="banned">Заблокирован</option>
        </BaseSelect>
      </div>

      <BaseInput
        v-model="form.password"
        type="password"
        label="Пароль"
        placeholder="Оставьте пустым для генерации"
        autocomplete="new-password"
      />

      <div class="modal-info-block success">
        <div class="modal-info-icon">
          <i class="fa fa-info-circle"></i>
        </div>
        <p class="modal-info-text">
          Пользователь будет добавлен в систему и получит доступ ко всем функциям.
        </p>
      </div>
    </form>

    <template #actions>
      <BaseButton variant="secondary" block type="button" @click="close">
        Отменить
      </BaseButton>
      <BaseButton
        variant="primary"
        icon="fa fa-plus"
        block
        type="submit"
        :disabled="!isFormValid"
        :loading="loading"
        @click="submit"
      >
        Добавить
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { BaseModal, BaseButton, BaseInput, BaseSelect } from '@/components/ui'
import { useToast } from '@/composables/useToast'
import api from '@/api/api'

const props = defineProps({
  isOpen: { type: Boolean, required: true, default: false },
})

const emit = defineEmits(['close', 'saved'])
const toast = useToast()

const form = reactive({
  username: '',
  email: '',
  password: '',
  role: 'motorcyclist',
  status: 'active',
})

const loading = ref(false)

const isFormValid = computed(() => {
  return (
    form.username.trim().length >= 2 &&
    form.email.includes('@')
  )
})

watch(
  () => props.isOpen,
  (newVal) => {
    if (!newVal) resetForm()
  }
)

function resetForm() {
  form.username = ''
  form.email = ''
  form.password = ''
  form.role = 'motorcyclist'
  form.status = 'active'
  loading.value = false
}

function close() {
  if (loading.value) return
  emit('close')
}

async function submit() {
  if (!isFormValid.value) {
    toast.warning('Заполните все обязательные поля')
    return
  }

  loading.value = true
  try {
    await api.post('/admin/user', { ...form })
    emit('saved')
    emit('close')
    toast.success('Пользователь добавлен')
  } catch (err) {
    console.error('Failed to create user:', err)
    toast.error(err.response?.data?.error || 'Ошибка при добавлении')
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

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.modal-info-block {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 10px;
}

.modal-info-block.success {
  background: var(--success-trans);
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.modal-info-icon {
  font-size: 18px;
  color: var(--success-text);
  flex-shrink: 0;
  margin-top: 2px;
}

.modal-info-text {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
}

@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  .modal-info-block {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  .modal-info-icon {
    margin-top: 0;
  }
}
</style>
