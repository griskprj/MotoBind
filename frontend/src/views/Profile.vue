<template>
  <div class="container">
    <Header title="Мой профиль" subtitle="Управляйте личными данными и настройками" />

    <n-spin :show="loading">
      <div class="profile-grid">
        <!-- ==================== LEFT: CARD ==================== -->
        <aside class="profile-sidebar">
          <n-card class="profile-card" :bordered="false">
            <!-- Аватар с загрузкой -->
            <div class="profile-avatar-wrapper">
              <n-upload
                :show-file-list="false"
                :custom-request="handleAvatarUpload"
                accept="image/*"
              >
                <n-avatar
                  :size="120"
                  :src="getAvatarUrl(user?.avatar)"
                  round
                  class="profile-avatar"
                />
              </n-upload>

              <n-button
                circle
                type="primary"
                class="avatar-edit-btn"
                @click="triggerAvatarUpload"
              >
                <template #icon><i class="fa fa-camera" /></template>
              </n-button>

              <n-button
                v-if="user?.avatar"
                circle
                quaternary
                type="error"
                class="avatar-delete-btn"
                @click="deleteAvatar"
              >
                <template #icon><i class="fa fa-trash" /></template>
              </n-button>
            </div>

            <h3 class="profile-username">{{ user?.username || 'Пользователь' }}</h3>
            <p class="profile-email">{{ user?.email || '—' }}</p>

            <div class="profile-badge">
              <n-tag :type="statusTagType(user?.status)" size="small" round>
                {{ getUserStatusLabel(user?.status) }}
              </n-tag>
              <n-tag type="primary" size="small" round>
                {{ getUserRoleLabel(user?.role) }}
              </n-tag>
            </div>

            <!-- Инфо -->
            <div class="profile-info-items">
              <div v-if="user?.location" class="info-item">
                <i class="fa fa-map-marker" />
                <span>{{ user.location }}</span>
              </div>
              <div v-if="user?.motorcycle" class="info-item">
                <i class="fa fa-motorcycle" />
                <span>{{ user.motorcycle }}</span>
              </div>
              <div v-if="user?.experience" class="info-item">
                <i class="fa fa-signal" />
                <span>{{ getUserExperienceLabel(user.experience) }}</span>
              </div>
              <div class="info-item">
                <i class="fa fa-calendar" />
                <span>С нами с {{ formatDate(user?.created_at) }}</span>
              </div>
            </div>

            <!-- Bio -->
            <div v-if="user?.bio" class="profile-bio" style="margin-top: 8px;">
              <i class="fa fa-quote-left" />
              {{ user.bio }}
            </div>

            <AppButton variant="outline" block @click="showEditProfile = true" style="margin-top: 12px;">
              <template #icon><i class="fa fa-pen" /></template>
              Редактировать профиль
            </AppButton>
          </n-card>
        </aside>

        <!-- ==================== RIGHT: SETTINGS ==================== -->
        <main class="profile-settings">
          <!-- Основная информация -->
          <n-card title="Основная информация" :bordered="false" class="settings-card">
            <template #header-extra>
              <i class="fa fa-user card-header-icon" />
            </template>

            <n-descriptions :column="1" label-placement="left" bordered>
              <n-descriptions-item label="Имя пользователя">
                {{ user?.username || '—' }}
              </n-descriptions-item>
              <n-descriptions-item label="Email">
                {{ user?.email || '—' }}
              </n-descriptions-item>
              <n-descriptions-item label="Город/Регион">
                {{ user?.location || 'Не указан' }}
              </n-descriptions-item>
              <n-descriptions-item label="Мой мотоцикл">
                {{ user?.motorcycle || 'Не указан' }}
              </n-descriptions-item>
              <n-descriptions-item label="Опыт вождения">
                {{ getUserExperienceLabel(user?.experience) || 'Не указан' }}
              </n-descriptions-item>
              <n-descriptions-item label="Роль">
                {{ getUserRoleLabel(user?.role) }}
              </n-descriptions-item>
              <n-descriptions-item label="Статус">
                <n-tag :type="statusTagType(user?.status)" size="small" round>
                  {{ getUserStatusLabel(user?.status) }}
                </n-tag>
              </n-descriptions-item>
              <n-descriptions-item label="Дата регистрации">
                {{ formatDate(user?.created_at) }}
              </n-descriptions-item>
              <n-descriptions-item label="ID пользователя">
                #{{ user?.id || '—' }}
              </n-descriptions-item>
            </n-descriptions>
          </n-card>

          <!-- Безопасность -->
          <n-card title="Безопасность" :bordered="false" class="settings-card">
            <template #header-extra>
              <i class="fa fa-lock card-header-icon" />
            </template>

            <div class="action-stack">
              <AppButton variant="outline" block @click="showChangePassword = true">
                <template #icon><i class="fa fa-key" /></template>
                Сменить пароль
              </AppButton>
              <AppButton variant="danger" block @click="showDeleteAccount = true">
                <template #icon><i class="fa fa-trash" /></template>
                Удалить аккаунт
              </AppButton>
            </div>
          </n-card>

          <!-- Бизнес -->
          <n-card title="Бизнес" :bordered="false" class="settings-card">
            <template #header-extra>
              <i class="fa fa-briefcase card-header-icon" />
            </template>

            <n-alert type="info" :bordered="false" class="business-hint">
              Ведёте обслуживание мотоциклов как мастер или СТО? Создайте бизнес-аккаунт.
            </n-alert>

            <AppButton variant="outline" block @click="goToBusiness">
              <template #icon><i class="fa fa-briefcase" /></template>
              Открыть кабинет бизнеса
            </AppButton>
          </n-card>

          <!-- Уведомления -->
          <n-card title="Уведомления и рассылки" :bordered="false" class="settings-card">
            <template #header-extra>
              <i class="fa fa-envelope card-header-icon" />
            </template>

            <div class="settings-group-title">Почта</div>

            <div class="toggle-row">
              <div class="toggle-info">
                <span class="toggle-label">Уведомления на почту</span>
                <span class="toggle-desc">Главный переключатель. Отключение отключает все письма</span>
              </div>
              <n-switch
                v-model:value="notificationSettings.email_notifications_enabled"
                @update:value="updateNotificationSettings"
              />
            </div>

            <div
              class="toggle-row"
              :class="{ disabled: !notificationSettings.email_notifications_enabled }"
            >
              <div class="toggle-info">
                <span class="toggle-label">Новостная рассылка</span>
                <span class="toggle-desc">Новости, статьи и полезные советы</span>
              </div>
              <n-switch
                v-model:value="notificationSettings.email_newsletter_enabled"
                :disabled="!notificationSettings.email_notifications_enabled"
                @update:value="updateNotificationSettings"
              />
            </div>

            <div
              class="toggle-row"
              :class="{ disabled: !notificationSettings.email_notifications_enabled }"
            >
              <div class="toggle-info">
                <span class="toggle-label">Подтверждение email</span>
                <span class="toggle-desc">Письма для верификации адреса</span>
              </div>
              <n-switch
                v-model:value="notificationSettings.email_verification_enabled"
                :disabled="!notificationSettings.email_notifications_enabled"
                @update:value="updateNotificationSettings"
              />
            </div>

            <div class="settings-group-title">Напоминания</div>

            <div
              class="toggle-row"
              :class="{ disabled: !notificationSettings.email_notifications_enabled }"
            >
              <div class="toggle-info">
                <span class="toggle-label">Напоминать о пробеге</span>
                <span class="toggle-desc">Если пробег не обновлялся 30 дней — пришлём письмо</span>
              </div>
              <n-switch
                v-model:value="notificationSettings.reminders_mileage_enabled"
                :disabled="!notificationSettings.email_notifications_enabled"
                @update:value="updateNotificationSettings"
              />
            </div>

            <div
              class="toggle-row"
              :class="{ disabled: !notificationSettings.email_notifications_enabled }"
            >
              <div class="toggle-info">
                <span class="toggle-label">Напоминать о ТО</span>
                <span class="toggle-desc">Предупредим о приближении или просрочке планового ТО</span>
              </div>
              <n-switch
                v-model:value="notificationSettings.reminders_maintenance_enabled"
                :disabled="!notificationSettings.email_notifications_enabled"
                @update:value="updateNotificationSettings"
              />
            </div>

            <n-alert type="info" :bordered="false" class="email-hint">
              Вы можете отписаться от рассылки в один клик из любого письма
            </n-alert>
          </n-card>

          <!-- Публичный профиль -->
          <n-card title="Публичный профиль" :bordered="false" class="settings-card">
            <template #header-extra>
              <i class="fa fa-globe card-header-icon" />
            </template>

            <p class="hint-text">Ваш публичный профиль доступен по ссылке:</p>

            <n-input-group class="profile-link">
              <n-input
                :value="profileUrl"
                readonly
                @click="copyProfileLink"
              />
              <AppButton variant="secondary" @click="copyProfileLink">
                <template #icon><i class="fa fa-copy" /></template>
                Копировать
              </AppButton>
            </n-input-group>

            <AppButton variant="outline" block @click="viewPublicProfile" class="mt-3">
              <template #icon><i class="fa fa-eye" /></template>
              Посмотреть публичный профиль
            </AppButton>
          </n-card>
        </main>
      </div>
    </n-spin>

    <!-- ==================== MODALS ==================== -->
    <EditProfileModal
      v-if="showEditProfile"
      :is-open="showEditProfile"
      :user="user"
      @close="showEditProfile = false"
    />

    <ChangePasswordModal
      v-if="showChangePassword"
      :is-open="showChangePassword"
      @close="showChangePassword = false"
    />

    <DeleteAccountModal
      :is-open="showDeleteAccount"
      @close="showDeleteAccount = false"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import type { UploadCustomRequestOptions } from 'naive-ui'
import { useUserStore } from '@/stores'
import { useToast } from '@/shared/composables/useToast'
import {
  getUserStatusLabel,
  getUserRoleLabel,
  getUserExperienceLabel,
  getSocialIcon,
} from '@/utils/formatters'
import { getAvatarUrl } from '@/utils/mediaUrl'
import formatDate from '@/utils/DateFormatter.js'
import Header from '@/components/Header.vue'
import { AppButton } from '@/shared/ui'
import EditProfileModal from '@/components/modals/user/EditProfileModal.vue'
import ChangePasswordModal from '@/components/modals/user/ChangePasswordModal.vue'
import DeleteAccountModal from '@/components/modals/user/DeleteAccountModal.vue'

const router = useRouter()
const toast = useToast()
const userStore = useUserStore()

const {
  profile: user,
  notificationSettings,
  loading,
  hasSocialLinks,
} = storeToRefs(userStore)

const showEditProfile = ref(false)
const showChangePassword = ref(false)
const showDeleteAccount = ref(false)

const profileUrl = computed(
  () => `${window.location.origin}/profile/${user.value?.id || ''}`
)

onMounted(async () => {
  try {
    await Promise.all([
      userStore.loadProfile(),
      userStore.loadNotificationSettings(),
    ])
  } catch (err: any) {
    console.error('Failed to load profile:', err)
    if (err.response?.status === 401) {
      router.push('/login')
      return
    }
    toast.error('Не удалось загрузить профиль')
  }
})

// ===== Status tag =====
function statusTagType(status?: string) {
  if (status === 'active') return 'success'
  if (status === 'banned') return 'error'
  if (status === 'pending') return 'warning'
  return 'default'
}

// ===== Avatar =====
function triggerAvatarUpload() {
  const input = document.querySelector<HTMLInputElement>(
    '.profile-avatar-wrapper input[type="file"]'
  )
  input?.click()
}

async function handleAvatarUpload({ file, onFinish, onError }: UploadCustomRequestOptions) {
  if (!file.file) return

  if (file.file.size > 5 * 1024 * 1024) {
    toast.error('Файл слишком большой. Максимум 5 МБ.')
    onError()
    return
  }

  try {
    await userStore.uploadAvatar(file.file)
    toast.success('Аватар обновлён!')
    onFinish()
  } catch (err: any) {
    toast.error(err.response?.data?.error || 'Ошибка загрузки аватара')
    onError()
  }
}

async function deleteAvatar() {
  if (!confirm('Удалить аватар?')) return
  try {
    await userStore.deleteAvatar()
    toast.success('Аватар удалён')
  } catch (err: any) {
    toast.error(err.response?.data?.error || 'Ошибка удаления')
  }
}

// ===== Notifications =====
async function updateNotificationSettings() {
  try {
    await userStore.updateNotificationSettings(notificationSettings.value)
    toast.success('Настройки обновлены')
  } catch {
    toast.error('Ошибка обновления настроек')
  }
}

// ===== Public profile =====
function viewPublicProfile() {
  if (!user.value?.id) return
  router.push(`/profile/${user.value.id}`)
}

async function copyProfileLink() {
  try {
    await navigator.clipboard.writeText(profileUrl.value)
    toast.success('Ссылка скопирована')
  } catch {
    toast.error('Не удалось скопировать')
  }
}

// ===== Business =====
function goToBusiness() {
  router.push('/business')
}
</script>

<style scoped>
.profile-grid {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 24px;
  align-items: start;
}

/* ===== Profile card ===== */
.profile-card :deep(.n-card__content) {
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
}

.profile-avatar-wrapper {
  position: relative;
  display: inline-block;
}

.profile-avatar {
  border: 3px solid var(--accent);
}

.avatar-edit-btn {
  position: absolute;
  bottom: 4px;
  right: 4px;
}

.avatar-delete-btn {
  position: absolute;
  top: 4px;
  right: 4px;
}

.profile-username {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  word-break: break-word;
}

.profile-email {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
  word-break: break-word;
}

.profile-badge {
  display: flex;
  gap: 6px;
  justify-content: center;
  flex-wrap: wrap;
}

.profile-info-items {
  display: flex;
  flex-direction: column;
  gap: 6px;
  width: 100%;
  text-align: left;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--text-secondary);
}

.info-item i {
  width: 18px;
  color: var(--accent);
  flex-shrink: 0;
}

.info-item span {
  overflow: hidden;
  text-overflow: ellipsis;
}

.profile-bio {
  font-size: 14px;
  color: var(--text-secondary);
  width: 100%;
  padding: 12px 16px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  border-left: 3px solid var(--accent);
  text-align: left;
  line-height: 1.6;
}

.profile-bio i {
  color: var(--accent);
  margin-right: 6px;
  opacity: 0.7;
}

.profile-social {
  display: flex;
  gap: 8px;
  justify-content: center;
  flex-wrap: wrap;
}

.social-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  transition: all 0.2s;
}

.social-link:hover {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
  transform: translateY(-2px);
}

/* ===== Stats ===== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}

/* ===== Settings cards ===== */
.settings-card {
  margin-bottom: 16px;
}

.settings-card:last-child {
  margin-bottom: 0;
}

.card-header-icon {
  color: var(--accent);
  font-size: 18px;
}

.action-stack {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* ===== Toggles ===== */
.settings-group-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.4px;
  margin: 12px 0 4px;
}

.settings-group-title:first-child {
  margin-top: 0;
}

.toggle-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 12px 0;
  border-bottom: 1px solid var(--border-light);
}

.toggle-row:last-child {
  border-bottom: none;
}

.toggle-row.disabled {
  opacity: 0.5;
  pointer-events: none;
}

.toggle-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.toggle-label {
  font-size: 14px;
  font-weight: 500;
}

.toggle-desc {
  font-size: 13px;
  color: var(--text-muted);
  line-height: 1.5;
}

/* ===== Hints ===== */
.business-hint,
.email-hint {
  margin-bottom: 12px;
}

.hint-text {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0 0 8px;
}

.profile-link {
  margin-bottom: 12px;
}

.mt-3 {
  margin-top: 12px;
}

/* ===== Adaptive ===== */
@media (max-width: 1024px) {
  .profile-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .toggle-row {
    flex-wrap: wrap;
  }

  .toggle-info {
    flex-basis: 100%;
  }
}
</style>
