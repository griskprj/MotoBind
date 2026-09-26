<template>
  <BaseModal
    :is-open="isOpen"
    title="Редактирование профиля"
    subtitle="Измените информацию о себе. Эти данные будут видны другим пользователям."
    icon="user"
    variant="default"
    size="md"
    @close="close"
  >
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

      <BaseTextarea
        v-model="form.bio"
        label="О себе"
        placeholder="Расскажите немного о себе, своём опыте и мотоцикле..."
        :rows="3"
        :maxlength="1000"
      />

      <div class="form-row">
        <BaseInput
          v-model="form.location"
          label="Город/Регион"
          placeholder="Например: Москва"
        />
        <BaseInput
          v-model="form.motorcycle"
          label="Мой мотоцикл"
          placeholder="Например: BMW S1000RR"
        />
      </div>

      <BaseSelect
        v-model="form.experience"
        label="Опыт вождения"
        placeholder="Не указано"
      >
        <option value="beginner">Новичок</option>
        <option value="intermediate">Опытный</option>
        <option value="expert">Эксперт</option>
      </BaseSelect>

      <div class="form-field">
        <label class="form-label">Социальные сети</label>
        <div class="social-links-editor">
          <div
            v-for="platform in socialPlatforms"
            :key="platform"
            class="social-link-row"
          >
            <i :class="getSocialIcon(platform)" class="social-icon"></i>
            <BaseInput
              v-model="form.social_links[platform]"
              :placeholder="`Ссылка на ${platform}`"
            />
            <BaseButton
              v-if="form.social_links[platform]"
              variant="ghost"
              icon="fa fa-times"
              :block="false"
              @click="form.social_links[platform] = ''"
            />
          </div>
        </div>
      </div>

      <div class="modal-info-block info">
        <div class="modal-info-icon">
          <i class="fa fa-info-circle"></i>
        </div>
        <p class="modal-info-text">
          Эти данные будут отображаться в вашем публичном профиле.
        </p>
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
        :loading="loading"
        @click="submit"
      >
        Сохранить
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'
import { BaseModal, BaseButton, BaseInput, BaseTextarea, BaseSelect } from '@/components/ui'
import { useToast } from '@/composables/useToast'
import { useUserStore } from '@/stores'
import { getSocialIcon } from '@/utils/formatters'

const props = defineProps({
  isOpen: { type: Boolean, default: false, required: true },
  user: { type: Object, default: null },
})

const emit = defineEmits(['close'])
const toast = useToast()
const userStore = useUserStore()

const socialPlatforms = ['youtube', 'telegram', 'vk']

const form = reactive({
  username: '',
  email: '',
  bio: '',
  location: '',
  motorcycle: '',
  experience: '',
  social_links: {
    youtube: '',
    telegram: '',
    vk: '',
  },
})

const loading = ref(false)

watch(
  () => props.isOpen,
  (newVal) => {
    if (newVal && props.user) loadFormData()
    if (!newVal) loading.value = false
  },
  { immediate: true }
)

watch(
  () => props.user,
  (newVal) => {
    if (props.isOpen && newVal) loadFormData()
  },
  { deep: true }
)

function loadFormData() {
  if (!props.user) return
  Object.assign(form, {
    username: props.user.username || '',
    email: props.user.email || '',
    bio: props.user.bio || '',
    location: props.user.location || '',
    motorcycle: props.user.motorcycle || '',
    experience: props.user.experience || '',
    social_links: {
      youtube: props.user.social_links?.youtube || '',
      telegram: props.user.social_links?.telegram || '',
      vk: props.user.social_links?.vk || '',
    },
  })
}

function close() {
  if (loading.value) return
  emit('close')
}

async function submit() {
  if (!form.username || form.username.trim().length < 2) {
    toast.error('Имя пользователя должно содержать минимум 2 символа')
    return
  }
  if (!form.email || !form.email.includes('@')) {
    toast.error('Введите корректный email адрес')
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
      experience: form.experience || '',
      social_links: {
        youtube: form.social_links.youtube?.trim() || '',
        telegram: form.social_links.telegram?.trim() || '',
        vk: form.social_links.vk?.trim() || '',
      },
    })
    emit('close')
    toast.success('Профиль обновлён')
  } catch (err) {
    console.error('Failed to update profile:', err)
    toast.error(err.response?.data?.message || 'Ошибка при обновлении профиля')
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

.form-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  color: var(--text-secondary);
}

.social-links-editor {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.social-link-row {
  display: flex;
  align-items: flex-end;
  gap: 10px;
}

.social-link-row > *:nth-child(2) {
  flex: 1;
}

.social-icon {
  width: 24px;
  font-size: 18px;
  color: var(--text-muted);
  padding-bottom: 10px;
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
