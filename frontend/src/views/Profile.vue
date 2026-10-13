<template>
  <div class="container">
    <Header title="Мой профиль" subtitle="Управляйте личными данными и настройками" />

    <div v-if="loading" class="loading-overlay">
      <div class="spinner" />
    </div>

    <div v-else class="profile-grid">
      <!-- ==================== LEFT: CARD ==================== -->
      <aside class="profile-sidebar">
        <BaseCard class="profile-card">
          <!-- Аватар -->
          <div class="profile-avatar-wrapper">
            <input
              ref="avatarInput"
              type="file"
              accept="image/*"
              hidden
              @change="onAvatarChange"
            >

            <AppAvatar
              :src="getAvatarUrl(user?.avatar)"
              :size="120"
              round
              class="profile-avatar"
            />

            <button
              class="avatar-btn avatar-edit-btn"
              title="Загрузить аватар"
              @click="avatarInput?.click()"
            >
              <i class="fa fa-camera" />
            </button>

            <button
              v-if="user?.avatar"
              class="avatar-btn avatar-delete-btn"
              title="Удалить аватар"
              @click="deleteAvatar"
            >
              <i class="fa fa-trash" />
            </button>
          </div>

          <h3 class="profile-username">{{ user?.username || 'Пользователь' }}</h3>
          <p class="profile-email">{{ user?.email || '—' }}</p>

          <div class="profile-badge">
            <span :class="`badge badge--${statusVariant(user?.status)}`">
              {{ getUserStatusLabel(user?.status) }}
            </span>
            <span class="badge badge--accent">
              {{ getUserRoleLabel(user?.role) }}
            </span>
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
          <div v-if="user?.bio" class="profile-bio">
            <i class="fa fa-quote-left" />
            {{ user.bio }}
          </div>

          <BaseButton
            variant="outline"
            block
            icon="fa fa-pen"
            @click="showEditProfile = true"
          >
            Редактировать профиль
          </BaseButton>
        </BaseCard>
      </aside>

      <!-- ==================== RIGHT: SETTINGS ==================== -->
      <main class="profile-settings">
        <!-- Основная информация -->
        <BaseCard title="Основная информация" icon="fa fa-user card-header-icon" class="settings-card">
          <dl class="info-dl">
            <div class="info-dl__row">
              <dt>Имя пользователя</dt>
              <dd>{{ user?.username || '—' }}</dd>
            </div>
            <div class="info-dl__row">
              <dt>Email</dt>
              <dd>{{ user?.email || '—' }}</dd>
            </div>
            <div class="info-dl__row">
              <dt>Город/Регион</dt>
              <dd>{{ user?.location || 'Не указан' }}</dd>
            </div>
            <div class="info-dl__row">
              <dt>Мой мотоцикл</dt>
              <dd>{{ user?.motorcycle || 'Не указан' }}</dd>
            </div>
            <div class="info-dl__row">
              <dt>Опыт вождения</dt>
              <dd>{{ getUserExperienceLabel(user?.experience) || 'Не указан' }}</dd>
            </div>
            <div class="info-dl__row">
              <dt>Роль</dt>
              <dd>{{ getUserRoleLabel(user?.role) }}</dd>
            </div>
            <div class="info-dl__row">
              <dt>Статус</dt>
              <dd>
                <span :class="`badge badge--${statusVariant(user?.status)}`">
                  {{ getUserStatusLabel(user?.status) }}
                </span>
              </dd>
            </div>
            <div class="info-dl__row">
              <dt>Дата регистрации</dt>
              <dd>{{ formatDate(user?.created_at) }}</dd>
            </div>
            <div class="info-dl__row">
              <dt>ID пользователя</dt>
              <dd>#{{ user?.id || '—' }}</dd>
            </div>
          </dl>
        </BaseCard>

        <!-- Безопасность -->
        <BaseCard title="Безопасность" icon="fa fa-lock card-header-icon" class="settings-card">
          <div class="action-stack">
            <BaseButton
              variant="outline"
              block
              icon="fa fa-key"
              @click="showChangePassword = true"
            >
              Сменить пароль
            </BaseButton>
            <BaseButton
              variant="danger"
              block
              icon="fa fa-trash"
              @click="showDeleteAccount = true"
            >
              Удалить аккаунт
            </BaseButton>
          </div>
        </BaseCard>

        <!-- Бизнес -->
        <BaseCard title="Бизнес" icon="fa fa-briefcase card-header-icon" class="settings-card">
          <div class="hint-block hint-block--info">
            <i class="fa fa-info-circle" />
            <p>Ведёте обслуживание мотоциклов как мастер или СТО? Создайте бизнес-аккаунт.</p>
          </div>

          <BaseButton
            variant="outline"
            block
            icon="fa fa-briefcase"
            @click="goToBusiness"
          >
            Открыть кабинет бизнеса
          </BaseButton>
        </BaseCard>

        <!-- Уведомления -->
        <BaseCard
          title="Уведомления и рассылки"
          icon="fa fa-envelope card-header-icon"
          class="settings-card"
        >
          <div class="settings-group-title">Почта</div>

          <div class="toggle-row">
            <div class="toggle-info">
              <span class="toggle-label">Уведомления на почту</span>
              <span class="toggle-desc">Главный переключатель. Отключение отключает все письма</span>
            </div>
            <AppSwitch
              v-model="notificationSettings.email_notifications_enabled"
              @change="updateNotificationSettings"
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
            <AppSwitch
              v-model="notificationSettings.email_newsletter_enabled"
              :disabled="!notificationSettings.email_notifications_enabled"
              @change="updateNotificationSettings"
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
            <AppSwitch
              v-model="notificationSettings.email_verification_enabled"
              :disabled="!notificationSettings.email_notifications_enabled"
              @change="updateNotificationSettings"
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
            <AppSwitch
              v-model="notificationSettings.reminders_mileage_enabled"
              :disabled="!notificationSettings.email_notifications_enabled"
              @change="updateNotificationSettings"
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
            <AppSwitch
              v-model="notificationSettings.reminders_maintenance_enabled"
              :disabled="!notificationSettings.email_notifications_enabled"
              @change="updateNotificationSettings"
            />
          </div>

          <div class="hint-block hint-block--info">
            <i class="fa fa-info-circle" />
            <p>Вы можете отписаться от рассылки в один клик из любого письма</p>
          </div>
        </BaseCard>

        <!-- Публичный профиль -->
        <BaseCard title="Публичный профиль" icon="fa fa-globe card-header-icon" class="settings-card">
          <p class="hint-text">Ваш публичный профиль доступен по ссылке:</p>

          <div class="profile-link">
            <input
              :value="profileUrl"
              readonly
              class="profile-link__input"
              @click="copyProfileLink"
            >
            <BaseButton variant="secondary" icon="fa fa-copy" @click="copyProfileLink">
              Копировать
            </BaseButton>
          </div>

          <BaseButton
            variant="outline"
            block
            icon="fa fa-eye"
            class="mt-3"
            @click="viewPublicProfile"
          >
            Посмотреть публичный профиль
          </BaseButton>
        </BaseCard>
      </main>
    </div>

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

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import {
  getUserStatusLabel,
  getUserRoleLabel,
  getUserExperienceLabel,
} from '@/utils/formatters'
import { getAvatarUrl } from '@/utils/mediaUrl'
import formatDate from '@/utils/DateFormatter.js'
import Header from '@/components/Header.vue'
import { BaseButton, BaseCard, AppSwitch, AppAvatar } from '@/components/ui'
import EditProfileModal from '@/components/modals/user/EditProfileModal.vue'
import ChangePasswordModal from '@/components/modals/user/ChangePasswordModal.vue'
import DeleteAccountModal from '@/components/modals/user/DeleteAccountModal.vue'

const router = useRouter()
const toast = useToast()
const userStore = useUserStore()

const { profile: user, notificationSettings, loading } = storeToRefs(userStore)

const showEditProfile = ref(false)
const showChangePassword = ref(false)
const showDeleteAccount = ref(false)
const avatarInput = ref(null)

const profileUrl = computed(
  () => `${window.location.origin}/profile/${user.value?.id || ''}`
)

onMounted(async () => {
  try {
    await Promise.all([
      userStore.loadProfile(),
      userStore.loadNotificationSettings(),
    ])
  } catch (err) {
    console.error('Failed to load profile:', err)
    if (err.response?.status === 401) {
      router.push('/login')
      return
    }
    toast.error('Не удалось загрузить профиль')
  }
})

function statusVariant(status) {
  return {
    active: 'success',
    banned: 'danger',
    pending: 'warning',
  }[status] || 'gray'
}

// ===== Avatar =====
async function onAvatarChange(event) {
  const file = event.target.files?.[0]
  if (!file) return

  if (file.size > 5 * 1024 * 1024) {
    toast.error('Файл слишком большой. Максимум 5 МБ.')
    event.target.value = ''
    return
  }

  try {
    await userStore.uploadAvatar(file)
    toast.success('Аватар обновлён!')
  } catch (err) {
    toast.error(err.response?.data?.error || 'Ошибка загрузки аватара')
  } finally {
    event.target.value = ''
  }
}

async function deleteAvatar() {
  if (!confirm('Удалить аватар?')) return
  try {
    await userStore.deleteAvatar()
    toast.success('Аватар удалён')
  } catch (err) {
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
.profile-card :deep(.base-card__body) {
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

.avatar-btn {
  position: absolute;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: var(--accent);
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  transition: all var(--transition-fast);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.avatar-btn:hover {
  background: var(--accent-hover);
  transform: scale(1.05);
}

.avatar-edit-btn {
  bottom: 4px;
  right: 4px;
}

.avatar-delete-btn {
  top: 4px;
  right: 4px;
  background: var(--danger);
}

.avatar-delete-btn:hover {
  background: var(--danger-hover);
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

.badge {
  display: inline-block;
  padding: 3px 12px;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: var(--fw-semibold);
  white-space: nowrap;
}

.badge--success { background: var(--success-trans); color: var(--success-text); }
.badge--danger { background: var(--danger-trans); color: var(--danger-text); }
.badge--warning { background: var(--warning-trans); color: var(--warning-text); }
.badge--gray { background: var(--border-light); color: var(--text-muted); }
.badge--accent { background: var(--accent-trans); color: var(--accent-text); }

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

/* ===== Info list (замена n-descriptions) ===== */
.info-dl {
  margin: 0;
  display: flex;
  flex-direction: column;
}

.info-dl__row {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 16px;
  padding: 10px 0;
  border-bottom: 1px solid var(--border-light);
  align-items: center;
}

.info-dl__row:last-child {
  border-bottom: none;
}

.info-dl__row dt {
  font-size: 13px;
  color: var(--text-muted);
}

.info-dl__row dd {
  margin: 0;
  font-size: 14px;
  color: var(--text-primary);
  word-break: break-word;
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

/* ===== Hint blocks ===== */
.hint-block {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 14px;
  border-radius: var(--radius-md);
  margin-bottom: 12px;
  font-size: 13px;
}

.hint-block p {
  margin: 0;
  line-height: 1.5;
}

.hint-block i {
  margin-top: 2px;
  flex-shrink: 0;
}

.hint-block--info {
  background: var(--accent-trans);
  color: var(--text-secondary);
}

.hint-block--info i {
  color: var(--accent-text);
}

.hint-text {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0 0 8px;
}

/* ===== Profile link ===== */
.profile-link {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.profile-link__input {
  flex: 1;
  padding: 0.625rem 0.75rem;
  font-size: 13px;
  font-family: var(--font-mono);
  background: var(--bg-input);
  border: 1px solid var(--border-input);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  cursor: pointer;
  min-height: 40px;
}

.profile-link__input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: var(--shadow-focus);
}

.mt-3 { margin-top: 12px; }

/* ===== Loading ===== */
.loading-overlay {
  display: flex;
  justify-content: center;
  padding: 60px 0;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--border-color);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ===== Adaptive ===== */
@media (max-width: 1024px) {
  .profile-grid { grid-template-columns: 1fr; }
}

@media (max-width: 640px) {
  .info-dl__row {
    grid-template-columns: 1fr;
    gap: 2px;
  }

  .toggle-row { flex-wrap: wrap; }
  .toggle-info { flex-basis: 100%; }

  .profile-link { flex-direction: column; }
}
</style>
