<template>
  <BaseModal
    :is-open="isOpen"
    title="Удаление аккаунта"
    subtitle="Это действие нельзя отменить. Все данные будут удалены безвозвратно"
    icon="user-slash"
    variant="danger"
    size="md"
    @close="close"
  >
    <div class="modal-info-block danger">
      <div class="modal-info-icon">
        <i class="fa fa-exclamation-triangle"></i>
      </div>
      <div>
        <p class="modal-info-text modal-info-text--strong">
          Вы уверены, что хотите удалить аккаунт?
        </p>
        <p class="modal-info-text">
          Будут удалены все ваши данные: мотоциклы, записи об обслуживании,
          мануалы, фотографии и личная информация. Восстановление невозможно.
        </p>
      </div>
    </div>

    <div class="danger-input">
      <BaseInput
        v-model="password"
        type="password"
        label="Введите пароль для подтверждения"
        placeholder="Введите текущий пароль"
        autocomplete="current-password"
        required
        @keydown.enter="submit"
      />
    </div>

    <template #actions>
      <BaseButton variant="secondary" block @click="close">
        Отменить
      </BaseButton>
      <BaseButton
        variant="danger"
        icon="fa fa-trash"
        block
        :disabled="!isFormValid"
        :loading="loading"
        @click="submit"
      >
        Удалить аккаунт
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { BaseModal, BaseButton, BaseInput } from '@/components/ui'
import { useToast } from '@/composables/useToast'
import { useUserStore, useAuthStore } from '@/stores'
import { useRouter } from 'vue-router'

const props = defineProps({
  isOpen: { type: Boolean, default: false, required: true },
})

const emit = defineEmits(['close'])
const toast = useToast()
const router = useRouter()
const userStore = useUserStore()
const authStore = useAuthStore()

const password = ref('')
const loading = ref(false)

const isFormValid = computed(() => password.value && password.value.length >= 6)

watch(
  () => props.isOpen,
  (newVal) => {
    if (!newVal) {
      password.value = ''
      loading.value = false
    }
  }
)

function close() {
  if (loading.value) return
  emit('close')
}

async function submit() {
  if (!password.value || password.value.length < 6) {
    toast.error('Введите корректный пароль (минимум 6 символов)')
    return
  }

  if (!confirm('Вы действительно хотите удалить аккаунт? Это действие нельзя отменить!')) {
    return
  }

  loading.value = true
  try {
    await userStore.deleteAccount(password.value)
    emit('close')
    authStore.logout()
    router.push('/login')
  } catch (err) {
    console.error('Failed to delete account:', err)
    toast.error(err.response?.data?.message || 'Ошибка при удалении аккаунта')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.modal-info-block {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 10px;
  margin-bottom: 16px;
}

.modal-info-block.danger {
  background: var(--danger-trans);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.modal-info-icon {
  font-size: 20px;
  color: var(--danger-text);
  flex-shrink: 0;
  margin-top: 2px;
}

.modal-info-text {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
}

.modal-info-text--strong {
  font-weight: 600;
  color: var(--danger-text);
}

.danger-input {
  padding: 14px 16px;
  background: var(--danger-trans);
  border: 2px solid rgba(239, 68, 68, 0.3);
  border-radius: 10px;
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

  .danger-input {
    padding: 12px 14px;
  }
}
</style>
