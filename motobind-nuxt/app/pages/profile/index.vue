<script setup lang="ts">
import type { UserProfile, NotificationSettings } from '~/types'

definePageMeta({ middleware: 'auth' })

useSeoMeta({ title: 'Мой профиль', robots: 'noindex' })

const api = useApi()
const auth = useAuthStore()
const toast = useToast()
const mediaUrl = useMediaUrl()

const { data: profileData, pending, refresh } = await useAsyncData(
  'my-profile',
  () => api.user.getMyProfile()
)

const user = computed(() => profileData.value?.user)

const isEditing = ref(false)
const editForm = reactive({ username: '', email: '' })
const savingProfile = ref(false)

function startEdit() {
  if (!user.value) return
  editForm.username = user.value.username
  editForm.email = user.value.email
  isEditing.value = true
}

async function saveProfile() {
  savingProfile.value = true
  try {
    await api.user.updateProfile({ username: editForm.username, email: editForm.email })
    toast.success('Профиль обновлён')
    isEditing.value = false
    await refresh()
  } catch (e) {
    toast.error('Ошибка сохранения')
  } finally {
    savingProfile.value = false
  }
}

const uploadingAvatar = ref(false)
const avatarInput = ref<HTMLInputElement | null>(null)

async function onAvatarChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return

  uploadingAvatar.value = true
  try {
    await api.user.uploadAvatar(file)
    toast.success('Аватар обновлён')
    await refresh()
  } catch (e) {
    toast.error('Ошибка загрузки аватара')
  } finally {
    uploadingAvatar.value = false
  }
}

async function deleteAvatar() {
  if (!confirm('Удалить аватар?')) return
  try {
    await api.user.deleteAvatar()
    toast.success('Аватар удалён')
    await refresh()
  } catch (e) {
    toast.error('Ошибка удаления аватара')
  }
}

const showPasswordModal = ref(false)
const passwordForm = reactive({ current: '', new: '', confirm: '' })
const changingPassword = ref(false)

async function changePassword() {
  if (passwordForm.new !== passwordForm.confirm) {
    toast.error('Пароли не совпадают')
    return
  }
  changingPassword.value = true
  try {
    await api.user.changePassword({
      currentPassword: passwordForm.current,
      newPassword: passwordForm.new,
    })
    toast.success('Пароль изменён')
    showPasswordModal.value = false
    passwordForm.current = ''
    passwordForm.new = ''
    passwordForm.confirm = ''
  } catch (e: any) {
    toast.error(e.message || 'Ошибка смены пароля')
  } finally {
    changingPassword.value = false
  }
}

const settings = ref<NotificationSettings | null>(null)
const savingSettings = ref(false)

onMounted(async () => {
  try {
    settings.value = await api.user.getNotificationSettings()
  } catch (e) {
    console.error(e)
  }
})

async function saveSettings() {
  if (!settings.value) return
  savingSettings.value = true
  try {
    await api.user.updateNotificationSettings(settings.value)
    toast.success('Настройки сохранены')
  } catch (e) {
    toast.error('Ошибка сохранения настроек')
  } finally {
    savingSettings.value = false
  }
}

const showDeleteModal = ref(false)
const deletePassword = ref('')
const deletingAccount = ref(false)

async function deleteAccount() {
  if (!deletePassword.value) {
    toast.error('Введите пароль')
    return
  }
  deletingAccount.value = true
  try {
    await api.user.deleteAccount(deletePassword.value)
    toast.success('Аккаунт удалён')
    await auth.logout()
    navigateTo('/')
  } catch (e: any) {
    toast.error(e.message || 'Ошибка удаления')
  } finally {
    deletingAccount.value = false
  }
}

const formatDate = (iso?: string) => {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('ru-RU')
}
</script>

<template>
  <div v-if="user" class="profile-page">
    <!-- Шапка профиля -->
    <BaseCard padding="lg" class="profile-header">
      <div class="avatar-section">
        <div class="avatar-col">
            <div class="avatar-wrap">
              <img
                v-if="user.avatar"
                :src="mediaUrl(user.avatar)!"
                alt="Аватар"
                class="avatar-img"
              />
              <div v-else class="avatar-placeholder"><i class="fa-solid fa-user"></i></div>
            </div>
            <div class="avatar-actions">
              <input type="file" accept="image/*" class="visually-hidden" ref="avatarInput" @change="onAvatarChange" />
              <BaseButton size="sm" variant="secondary" :loading="uploadingAvatar" @click="avatarInput?.click()">
                <i class="fa-solid fa-camera"></i>
              </BaseButton>
              <BaseButton v-if="user.avatar" size="sm" variant="danger" @click="deleteAvatar">
                <i class="fa-solid fa-trash"></i>
              </BaseButton>
            </div>
        </div>

        <div class="user-info">
          <h1 class="username">{{ user.username }}</h1>
          <p class="email">{{ user.email }}</p>
          <div class="meta">
            <span class="badge" :class="`badge--${user.role}`">{{ user.role === 'admin' ? 'Админ' : user.role === 'motoclub' ? 'Мотоклуб' : 'Мотоциклист' }}</span>
            <span class="date">С нами с {{ formatDate(user.created_at) }}</span>
          </div>
        </div>
      </div>

      <!-- Статистика -->
      <div v-if="user.stats" class="stats-row">
        <div class="stat-item">
          <span class="stat-value">{{ user.stats.posts_count }}</span>
          <span class="stat-label">Постов</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">{{ user.stats.likes_received }}</span>
          <span class="stat-label">Лайков</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">{{ user.stats.comments_received }}</span>
          <span class="stat-label">Комментариев</span>
        </div>
      </div>
    </BaseCard>

    <!-- Основная информация -->
    <BaseCard padding="lg">
      <div class="card-header">
        <h2 class="section-title">Основная информация</h2>
        <BaseButton v-if="!isEditing" variant="ghost" size="sm" @click="startEdit">
          <i class="fa-solid fa-pen"></i> Редактировать
        </BaseButton>
      </div>

      <div v-if="!isEditing" class="info-list">
        <div class="info-row"><span>Имя:</span> <strong>{{ user.username }}</strong></div>
        <div class="info-row"><span>Email:</span> <strong>{{ user.email }}</strong></div>
      </div>

      <form v-else @submit.prevent="saveProfile" class="edit-form">
        <BaseInput v-model="editForm.username" label="Имя пользователя" required />
        <BaseInput v-model="editForm.email" type="email" label="Email" required />
        <div class="form-actions">
          <BaseButton variant="ghost" type="button" @click="isEditing = false">Отмена</BaseButton>
          <BaseButton variant="primary" type="submit" :loading="savingProfile">Сохранить</BaseButton>
        </div>
      </form>
    </BaseCard>

    <!-- Безопасность -->
    <BaseCard padding="lg">
      <h2 class="section-title">Безопасность</h2>
      <BaseButton variant="secondary" @click="showPasswordModal = true">
        <i class="fa-solid fa-lock"></i> Сменить пароль
      </BaseButton>
    </BaseCard>

    <!-- Уведомления -->
    <BaseCard v-if="settings" padding="lg">
      <h2 class="section-title">Уведомления</h2>
      <div class="settings-list">
        <BaseCheckbox v-model="settings.email_notifications_enabled" label="Email-уведомления" />
        <BaseCheckbox v-model="settings.email_newsletter_enabled" label="Рассылка новостей" />
        <BaseCheckbox v-model="settings.reminders_mileage_enabled" label="Напоминания о пробеге" />
        <BaseCheckbox v-model="settings.reminders_maintenance_enabled" label="Напоминания об обслуживании" />
      </div>
      <div class="form-actions">
        <BaseButton variant="primary" :loading="savingSettings" @click="saveSettings">Сохранить настройки</BaseButton>
      </div>
    </BaseCard>

    <!-- Опасная зона -->
    <BaseCard padding="lg" class="danger-zone">
      <h2 class="section-title text-danger">Опасная зона</h2>
      <p class="danger-desc">Удаление аккаунта приведёт к потере всех данных: мотоциклов, мануалов, постов и комментариев.</p>
      <BaseButton variant="danger" @click="showDeleteModal = true">Удалить аккаунт</BaseButton>
    </BaseCard>

    <!-- Модалка смены пароля -->
    <BaseModal v-if="showPasswordModal" title="Сменить пароль" size="sm" @close="showPasswordModal = false">
      <form @submit.prevent="changePassword" class="modal-form">
        <BaseInput v-model="passwordForm.current" type="password" label="Текущий пароль" required />
        <BaseInput v-model="passwordForm.new" type="password" label="Новый пароль" required />
        <BaseInput v-model="passwordForm.confirm" type="password" label="Подтвердите новый пароль" required />
      </form>
      <template #footer>
        <BaseButton variant="ghost" size="sm" @click="showPasswordModal = false">Отмена</BaseButton>
        <BaseButton variant="primary" size="sm" :loading="changingPassword" @click="changePassword">Сменить</BaseButton>
      </template>
    </BaseModal>

    <!-- Модалка удаления аккаунта -->
    <BaseModal v-if="showDeleteModal" title="Удалить аккаунт?" size="sm" @close="showDeleteModal = false">
      <div class="delete-form">
        <p>Это действие необратимо. Введите пароль для подтверждения:</p>
        <BaseInput v-model="deletePassword" type="password" label="Пароль" required />
      </div>
      <template #footer>
        <BaseButton variant="ghost" size="sm" @click="showDeleteModal = false">Отмена</BaseButton>
        <BaseButton variant="danger" size="sm" :loading="deletingAccount" @click="deleteAccount">Удалить</BaseButton>
      </template>
    </BaseModal>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.profile-page {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

/* Шапка */
.profile-header {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-4);
  text-align: center;

  @include sm-up {
    flex-direction: row;
    text-align: left;
    align-items: flex-start;
  }
}

.avatar-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  flex-shrink: 0;
}

.avatar-wrap {
  width: 96px;
  height: 96px;
}

.avatar-img, .avatar-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  background: var(--color-surface-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  color: var(--color-text-tertiary);
  border: 2px solid var(--color-border);
}

.avatar-actions {
  display: flex;
  gap: var(--space-2);
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.username { font-size: var(--text-2xl); font-weight: var(--fw-bold); }
.email { color: var(--color-text-secondary); }
.meta { display: flex; flex-wrap: wrap; align-items: center; gap: var(--space-2); margin-top: var(--space-1); }
.badge { display: inline-block; padding: 2px 8px; border-radius: var(--radius-full); font-size: var(--text-xs); font-weight: var(--fw-medium); }
.badge--admin { background: var(--color-brand-soft); color: var(--color-brand); }
.badge--motoclub { background: var(--color-info-soft); color: var(--color-info); }
.badge--motorcyclist { background: var(--color-surface-secondary); color: var(--color-text-secondary); }
.date { font-size: var(--text-xs); color: var(--color-text-tertiary); }

/* Статистика */
.stats-row {
  display: flex;
  gap: var(--space-6);
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border-light);
}
.stat-item { display: flex; flex-direction: column; }
.stat-value { font-size: var(--text-xl); font-weight: var(--fw-bold); }
.stat-label { font-size: var(--text-xs); color: var(--color-text-tertiary); text-transform: uppercase; }

/* Общие стили */
.section-title { font-size: var(--text-lg); font-weight: var(--fw-semibold); margin-bottom: var(--space-3); }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--space-3); }

.info-list { display: flex; flex-direction: column; gap: var(--space-2); }
.info-row { display: flex; gap: var(--space-2); font-size: var(--text-base); }
.info-row span { color: var(--color-text-secondary); }

.edit-form { display: flex; flex-direction: column; gap: var(--space-4); }
.form-actions { display: flex; justify-content: flex-end; gap: var(--space-2); margin-top: var(--space-3); }

.settings-list { display: flex; flex-direction: column; gap: var(--space-2); margin-bottom: var(--space-4); }

.danger-zone { border-color: var(--color-danger-soft); background: color-mix(in srgb, var(--color-danger-soft) 30%, var(--color-surface)); }
.text-danger { color: var(--color-danger); }
.danger-desc { font-size: var(--text-sm); color: var(--color-text-secondary); margin-bottom: var(--space-4); }

.modal-form { display: flex; flex-direction: column; gap: var(--space-4); }
.delete-form { display: flex; flex-direction: column; gap: var(--space-4); }
</style>
