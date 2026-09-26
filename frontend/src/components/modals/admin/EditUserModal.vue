<template>
  <BaseModal
    :is-open="isOpen"
    title="Редактирование пользователя"
    subtitle="Измените данные пользователя. Роль определяет доступ к функциям."
    icon="user-cog"
    variant="default"
    size="md"
    @close="close"
  >
    <!-- Инфо о пользователе -->
    <div v-if="user" class="user-info-card">
      <img :src="getAvatarUrl(user.avatar)" alt="Аватар" class="user-avatar" />
      <div class="user-info">
        <div class="user-name">{{ user.username || 'Пользователь' }}</div>
        <div class="user-meta">
          <span class="user-id">ID: #{{ user.id }}</span>
          <span>{{ formatDate(user.created_at) }}</span>
        </div>
      </div>
    </div>

    <form @submit.prevent="submit" class="form-stack">
      <BaseInput
        v-model="form.username"
        label="Имя пользователя"
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
        <BaseSelect v-model="form.role" label="Роль">
          <option value="motorcyclist">Мотоциклист</option>
          <option value="club_member">Член клуба</option>
          <option value="admin">Администратор</option>
        </BaseSelect>

        <BaseSelect v-model="form.status" label="Статус">
          <option value="active">Активен</option>
          <option value="banned">Заблокирован</option>
          <option value="pending">Ожидает</option>
        </BaseSelect>
      </div>
    </form>

    <template #actions>
      <BaseButton variant="secondary" block type="button" @click="close">
        Отменить
      </BaseButton>
      <BaseButton
        variant="primary"
        icon="fa fa-save"
        block
        type="submit"
        :disabled="!isFormValid"
        :loading="loading"
        @click="submit"
      >
        Сохранить
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { BaseModal, BaseButton, BaseInput, BaseSelect } from '@/components/ui'
import { useToast } from '@/composables/useToast'
import { getAvatarUrl } from '@/utils/mediaUrl'
import api from '@/api/api'

const props = defineProps({
  isOpen: { type: Boolean, required: true, default: false },
  user: { type: Object, default: null },
})

const emit = defineEmits(['close', 'saved'])
const toast = useToast()

const form = reactive({
  id: null,
  username: '',
  email: '',
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
  () => props.user,
  (newVal) => {
    if (newVal && props.isOpen) loadFormData(newVal)
  },
  { immediate: true }
)

watch(
  () => props.isOpen,
  (newVal) => {
    if (newVal && props.user) loadFormData(props.user)
    if (!newVal) loading.value = false
  }
)

function loadFormData(user) {
  form.id = user.id || null
  form.username = user.username || ''
  form.email = user.email || ''
  form.role = user.role || 'motorcyclist'
  form.status = user.status || 'active'
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  try {
    const date = new Date(dateStr)
    if (isNaN(date.getTime())) return '—'
    return date.toLocaleDateString('ru-RU', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    })
  } catch {
    return '—'
  }
}

function close() {
  if (loading.value) return
  emit('close')
}

async function submit() {
  if (!isFormValid.value) {
    toast.warning('Заполните обязательные поля')
    return
  }

  loading.value = true
  try {
    await api.put(`/admin/user/${form.id}`, {
      username: form.username.trim(),
      email: form.email.trim(),
      role: form.role,
      status: form.status,
    })
    emit('saved')
    emit('close')
    toast.success('Пользователь обновлён')
  } catch (err) {
    console.error('Failed to update user:', err)
    toast.error(err.response?.data?.error || 'Ошибка при сохранении')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.user-info-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 16px;
  background: var(--bg-secondary);
  border-radius: 12px;
  border: 1px solid var(--border-light);
  margin-bottom: 18px;
}

.user-avatar {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--accent);
  flex-shrink: 0;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.user-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  font-size: 13px;
  color: var(--text-muted);
}

.user-id {
  background: var(--accent-trans);
  padding: 1px 10px;
  border-radius: 12px;
  color: var(--accent-text);
}

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

@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  .user-info-card {
    flex-direction: column;
    text-align: center;
  }
  .user-meta {
    justify-content: center;
  }
}
</style>
