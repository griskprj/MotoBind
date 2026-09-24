<template>
    <div class="container">
        <LoadingOverlay :isLoading="loading || uploadingAvatar" text="Загрузка профиля"/>

        <!-- === HEADER === -->
        <Header
            title="Мой профиль"
            subtitle="Управляйте личными данными и настройками"
        />

        <!-- === PROFILE CONTENT === -->
        <div class="profile-grid">
            <!-- LEFT COLUMN: Avatar & Info -->
            <aside class="profile-sidebar">
                <div class="profile-card">
                    <div class="profile-avatar-wrapper">
                        <img
                            :src="getAvatarUrl(user?.avatar)"
                            alt="avatar"
                            class="profile-avatar"
                            @error="handleAvatarError"
                        >
                        <button class="avatar-edit-btn" @click="triggerAvatarInput" title="Изменить аватар">
                            <i class="fa fa-camera"></i>
                        </button>
                        <input
                            :ref="(el) => (avatarInputRef = el)"
                            type="file"
                            accept="image/*"
                            @change="handleAvatarUpload"
                            style="display: none"
                        />
                    </div>

                    <h3 class="profile-username">{{ user?.username || 'Пользователь' }}</h3>
                    <p class="profile-email">{{ user?.email || '—' }}</p>

                    <div class="profile-badge">
                        <span :class="getUserStatusClass(user?.status)">
                            {{ getUserStatusLabel(user?.status) }}
                        </span>
                        <span class="role-badge">{{ getUserRoleLabel(user?.role) }}</span>
                    </div>

                    <div v-if="user?.avatar" class="avatar-actions">
                        <button class="btn btn-danger btn-sm" @click="deleteAvatar">
                            <i class="fa fa-trash"></i> Удалить аватар
                        </button>
                    </div>

                    <!-- Информация о пользователе -->
                    <div class="profile-info-items">
                        <div v-if="user?.location" class="info-item">
                            <i class="fa fa-map-marker"></i>
                            <span>{{ user.location }}</span>
                        </div>
                        <div v-if="user?.motorcycle" class="info-item">
                            <i class="fa fa-motorcycle"></i>
                            <span>{{ user.motorcycle }}</span>
                        </div>
                        <div v-if="user?.experience" class="info-item">
                            <i class="fa fa-signal"></i>
                            <span>{{ getUserExperienceLabel(user.experience) }}</span>
                        </div>
                        <div class="info-item">
                            <i class="fa fa-calendar"></i>
                            <span>С нами с {{ formatDate(user?.created_at) }}</span>
                        </div>
                    </div>

                    <div v-if="user?.bio" class="profile-bio">
                        <i class="fa fa-quote-left"></i>
                        {{ user.bio }}
                    </div>

                    <!-- Социальные сети -->
                    <div v-if="hasSocialLinks" class="profile-social">
                        <a
                            v-for="(url, platform) in user.social_links"
                            :key="platform"
                            :href="url"
                            target="_blank"
                            rel="noopener noreferrer"
                            class="social-link"
                            :title="platform"
                        >
                            <i :class="getSocialIcon(platform)"></i>
                        </a>
                    </div>

                    <div class="profile-actions">
                        <button class="outline-btn" style="width: 100%;" @click="showEditProfile = true">
                            <i class="fa fa-pen"></i> Редактировать профиль
                        </button>
                    </div>
                </div>

                <!-- Статистика -->
                <div class="stats-card">
                    <div class="stat-item">
                        <span class="stat-value">{{ stats.posts || 0 }}</span>
                        <span class="stat-label">Постов</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value">{{ stats.likes || 0 }}</span>
                        <span class="stat-label">Лайков</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value">{{ stats.comments || 0 }}</span>
                        <span class="stat-label">Комментариев</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value">{{ stats.motorcycles || 0 }}</span>
                        <span class="stat-label">Мотоциклов</span>
                    </div>
                </div>
            </aside>

            <!-- RIGHT COLUMN: Settings -->
            <main class="profile-settings">
                <!-- Основная информация -->
                <div class="settings-card">
                    <div class="settings-card-header">
                        <i class="fa fa-user"></i>
                        <h3>Основная информация</h3>
                    </div>
                    <div class="settings-card-body">
                        <div class="info-row">
                            <span class="info-label">Имя пользователя</span>
                            <span class="info-value">{{ user?.username || '—' }}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Email</span>
                            <span class="info-value">{{ user?.email || '—' }}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Город/Регион</span>
                            <span class="info-value">{{ user?.location || 'Не указан' }}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Мой мотоцикл</span>
                            <span class="info-value">{{ user?.motorcycle || 'Не указан' }}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Опыт вождения</span>
                            <span class="info-value">{{ getUserExperienceLabel(user?.experience) || 'Не указан' }}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Роль</span>
                            <span class="info-value">{{ getUserRoleLabel(user?.role) }}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Статус</span>
                            <span class="info-value">
                                <span :class="getUserStatusClass(user?.status)">
                                    {{ getUserStatusLabel(user?.status) }}
                                </span>
                            </span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Дата регистрации</span>
                            <span class="info-value">{{ formatDate(user?.created_at) }}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">ID пользователя</span>
                            <span class="info-value">#{{ user?.id || '—' }}</span>
                        </div>
                    </div>
                </div>

                <!-- Безопасность -->
                <div class="settings-card">
                    <div class="settings-card-header">
                        <i class="fa fa-lock"></i>
                        <h3>Безопасность</h3>
                    </div>
                    <div class="settings-card-body">
                        <button class="outline-btn" style="width: 100%;" @click="showChangePassword = true">
                            <i class="fa fa-key"></i> Сменить пароль
                        </button>
                        <button class="btn-danger" @click="showDeleteAccount = true">
                            <i class="fa fa-trash"></i> Удалить аккаунт
                        </button>
                    </div>
                </div>

                <div class="settings-card">
                    <div class="settings-card-header">
                        <i class="fa fa-envelope"></i>
                        <h3>Уведомления и рассылки</h3>
                    </div>
                    <div class="settings-card-body">
                        <!-- Группа: Email -->
                        <div class="settings-group-title">Почта</div>

                        <div class="toggle-row">
                            <div class="toggle-info">
                                <span class="toggle-label">Уведомления на почту</span>
                                <span class="toggle-desc">Главный переключатель. Отключение отключает все письма от сервиса</span>
                            </div>
                            <label class="switch">
                                <input
                                    type="checkbox"
                                    v-model="notificationSettings.email_notifications_enabled"
                                    @change="updateNotificationSettings"
                                >
                                <span class="slider"></span>
                            </label>
                        </div>

                        <div class="toggle-row" :class="{ disabled: !notificationSettings.email_notifications_enabled }">
                            <div class="toggle-info">
                                <span class="toggle-label">Новостная рассылка</span>
                                <span class="toggle-desc">Новости, статьи и полезные советы для мотоциклистов</span>
                            </div>
                            <label class="switch">
                                <input
                                    type="checkbox"
                                    v-model="notificationSettings.email_newsletter_enabled"
                                    :disabled="!notificationSettings.email_notifications_enabled"
                                    @change="updateNotificationSettings"
                                >
                                <span class="slider"></span>
                            </label>
                        </div>

                        <div class="toggle-row" :class="{ disabled: !notificationSettings.email_notifications_enabled }">
                            <div class="toggle-info">
                                <span class="toggle-label">Подтверждение email</span>
                                <span class="toggle-desc">Письма для верификации адреса</span>
                            </div>
                            <label class="switch">
                                <input
                                    type="checkbox"
                                    v-model="notificationSettings.email_verification_enabled"
                                    :disabled="!notificationSettings.email_notifications_enabled"
                                    @change="updateNotificationSettings"
                                >
                                <span class="slider"></span>
                            </label>
                        </div>

                        <!-- Группа: Напоминания -->
                        <div class="settings-group-title">Напоминания</div>

                        <div class="toggle-row" :class="{ disabled: !notificationSettings.email_notifications_enabled }">
                            <div class="toggle-info">
                                <span class="toggle-label">Напоминать о пробеге</span>
                                <span class="toggle-desc">Если пробег не обновлялся 30 дней — пришлём письмо</span>
                            </div>
                            <label class="switch">
                                <input
                                    type="checkbox"
                                    v-model="notificationSettings.reminders_mileage_enabled"
                                    :disabled="!notificationSettings.email_notifications_enabled"
                                    @change="updateNotificationSettings"
                                >
                                <span class="slider"></span>
                            </label>
                        </div>

                        <div class="toggle-row" :class="{ disabled: !notificationSettings.email_notifications_enabled }">
                            <div class="toggle-info">
                                <span class="toggle-label">Напоминать о ТО</span>
                                <span class="toggle-desc">Предупредим, когда приблизится плановое обслуживание или оно просрочено</span>
                            </div>
                            <label class="switch">
                                <input
                                    type="checkbox"
                                    v-model="notificationSettings.reminders_maintenance_enabled"
                                    :disabled="!notificationSettings.email_notifications_enabled"
                                    @change="updateNotificationSettings"
                                >
                                <span class="slider"></span>
                            </label>
                        </div>

                        <div class="info-box info">
                            <i class="fa fa-info-circle"></i>
                            <span>
                                Вы можете отписаться от рассылки в один клик из любого письма
                            </span>
                        </div>
                    </div>
                </div>

                <!-- Публичный профиль -->
                <div class="settings-card">
                    <div class="settings-card-header">
                        <i class="fa fa-globe"></i>
                        <h3>Публичный профиль</h3>
                    </div>
                    <div class="settings-card-body">
                        <p class="hint-text">
                            <i class="fa fa-info-circle"></i>
                            Ваш публичный профиль доступен по ссылке:
                        </p>
                        <div class="profile-link">
                            <input
                                :value="profileUrl"
                                readonly
                                @click="copyProfileLink"
                            >
                            <button class="btn btn-secondary btn-sm" @click="copyProfileLink">
                                <i class="fa fa-copy"></i> Копировать
                            </button>
                        </div>
                        <button class="outline-btn" style="width: 100%;" @click="viewPublicProfile">
                            <i class="fa fa-eye"></i> Посмотреть публичный профиль
                        </button>
                    </div>
                </div>
            </main>
        </div>
    </div>

    <!-- === MODALS === -->
    <EditProfileModal
        v-if="showEditProfile"
        :isOpen="showEditProfile"
        :user="user"
        @submit="updateProfile"
        @close="showEditProfile = false"
    />

    <ChangePasswordModal
        v-if="showChangePassword"
        :isOpen="showChangePassword"
        @submit="changePassword"
        @close="showChangePassword = false"
    />

    <DeleteAccountModal
        :isOpen="showDeleteAccount"
        @submit="deleteAccount"
        @close="showDeleteAccount = false"
    />
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useUserStore, useAuthStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import {
  getUserStatusLabel,
  getUserStatusClass,
  getUserRoleLabel,
  getUserExperienceLabel,
  getSocialIcon,
} from '@/utils/formatters'
import { getAvatarUrl } from '@/utils/mediaUrl'
import formatDate from '@/utils/DateFormatter.js'

import EditProfileModal from '../components/modals/user/EditProfileModal.vue'
import ChangePasswordModal from '../components/modals/user/ChangePasswordModal.vue'
import DeleteAccountModal from '../components/modals/user/DeleteAccountModal.vue'
import Header from '../components/Header.vue'
import LoadingOverlay from '../components/LoadingOverlay.vue'

const router = useRouter()
const toast = useToast()

const userStore = useUserStore()
const authStore = useAuthStore()

const {
  profile: user,
  notificationSettings,
  loading,
  uploadingAvatar,
  stats,
  hasSocialLinks,
} = storeToRefs(userStore)

// ===== Local UI state =====
const showEditProfile = ref(false)
const showChangePassword = ref(false)
const showDeleteAccount = ref(false)
const avatarInputRef = ref(null)

// ===== Computed =====
const profileUrl = computed(() => {
  return `${window.location.origin}/profile/${user.value?.id || ''}`
})

// ===== Lifecycle =====
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

// ===== Avatar =====
function triggerAvatarInput() {
  avatarInputRef.value?.click()
}

async function handleAvatarUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  if (file.size > 5 * 1024 * 1024) {
    toast.error('Файл слишком большой. Максимальный размер 5 МБ.')
    event.target.value = ''
    return
  }

  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp', 'image/webp']
  if (!allowedTypes.includes(file.type)) {
    toast.error('Неподдерживаемый формат. Разрешены: JPG, PNG, GIF, BMP, WEBP')
    event.target.value = ''
    return
  }

  try {
    await userStore.uploadAvatar(file)
    toast.success('Аватар успешно обновлён!')
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
    toast.error(err.response?.data?.error || 'Ошибка удаления аватара')
  }
}

function handleAvatarError(event) {
  event.target.src = '/BaseAvatar.webp'
}

// ===== Profile =====
async function updateProfile(formData) {
  try {
    await userStore.updateProfile(formData)
    showEditProfile.value = false
    toast.success('Профиль обновлён!')
  } catch (err) {
    toast.error(err.response?.data?.message || 'Ошибка при обновлении профиля')
  }
}

// ===== Notifications =====
async function updateNotificationSettings() {
  try {
    await userStore.updateNotificationSettings(notificationSettings.value)
    toast.success('Настройки уведомлений обновлены')
  } catch (err) {
    toast.error('Ошибка обновления настроек')
  }
}

// ===== Security =====
async function changePassword(formData) {
  try {
    if (formData.newPassword !== formData.repeatPassword) {
      toast.error('Пароли не совпадают')
      return
    }
    await userStore.changePassword(formData)
    showChangePassword.value = false
    toast.success('Пароль успешно изменён!')
  } catch (err) {
    toast.error(err.response?.data?.message || 'Ошибка при смене пароля')
  }
}

async function deleteAccount(password) {
  try {
    await userStore.deleteAccount(password)
    showDeleteAccount.value = false
    authStore.logout()
    router.push('/login')
  } catch (err) {
    toast.error(err.response?.data?.message || 'Ошибка при удалении аккаунта')
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
    toast.success('Ссылка на профиль скопирована!')
  } catch {
    // fallback для старых браузеров
    const input = document.querySelector('.profile-link input')
    if (input) {
      input.select()
      document.execCommand('copy')
      toast.success('Ссылка на профиль скопирована!')
    }
  }
}
</script>

<style scoped>
/* ===== PROFILE GRID ===== */
.profile-grid {
    display: grid;
    grid-template-columns: 320px 1fr;
    gap: 24px;
    align-items: start;
}

/* ===== SIDEBAR ===== */
.profile-sidebar {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.profile-card {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
}

.profile-avatar-wrapper {
    position: relative;
    width: 120px;
    height: 120px;
    margin: 0 auto 16px;
    overflow-y: hidden;
}

.profile-avatar {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid var(--accent);
}

.avatar-edit-btn {
    position: absolute;
    bottom: 4px;
    right: 4px;
    min-width: 38px;
    border-radius: 50%;
    background: var(--accent);
    border: none;
    color: #fff;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.avatar-edit-btn:hover {
    background: var(--accent-hover);
    transform: scale(1.05);
}

.profile-username {
    font-size: 20px;
    font-weight: 600;
    margin: 0 0 4px 0;
    color: var(--text-primary);
}

.profile-email {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0 0 12px 0;
}

.profile-badge {
    display: flex;
    gap: 8px;
    justify-content: center;
    margin-bottom: 12px;
    flex-wrap: wrap;
}

.status-active {
    display: inline-block;
    padding: 2px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    background: var(--success-trans);
    color: var(--success-text);
}

.status-banned {
    display: inline-block;
    padding: 2px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    background: var(--danger-trans);
    color: var(--danger-text);
}

.status-pending {
    display: inline-block;
    padding: 2px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    background: var(--warning-trans);
    color: var(--warning-text);
}

.role-badge {
    display: inline-block;
    padding: 2px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    background: var(--accent-trans);
    color: var(--accent-text);
}

.avatar-actions {
    margin-bottom: 12px;
}

.profile-info-items {
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin-bottom: 12px;
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
    color: var(--accent-text);
}

.profile-bio {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 14px;
    padding: 12px 16px;
    background: var(--bg-secondary);
    border-radius: 10px;
    border-left: 3px solid var(--accent);
    text-align: left;
    line-height: 1.6;
}

.profile-bio i {
    color: var(--accent-text);
    margin-right: 6px;
    opacity: 0.7;
}

.profile-social {
    display: flex;
    gap: 8px;
    justify-content: center;
    margin-bottom: 16px;
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
    color: white;
    border-color: var(--accent);
    transform: translateY(-2px);
}

.profile-actions {
    display: flex;
    gap: 8px;
}

.profile-actions .btn {
    flex: 1;
}

/* ===== STATS CARD ===== */
.stats-card {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: 16px;
    padding: 16px 20px;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
}

.stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.stat-value {
    font-size: 20px;
    font-weight: 700;
    color: var(--accent);
}

.stat-label {
    font-size: 12px;
    color: var(--text-secondary);
}

/* ===== SETTINGS ===== */
.settings-card {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 16px;
}

.settings-card:last-child {
    margin-bottom: 0;
}

.settings-card-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 20px;
    border-bottom: 1px solid var(--border-light);
    background: var(--bg-secondary);
}

.settings-card-header i {
    font-size: 18px;
    color: var(--accent);
}

.settings-card-header h3 {
    font-size: 16px;
    font-weight: 600;
    margin: 0;
    color: var(--text-primary);
}

.settings-card-body {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 20px;
}

.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid var(--border-light);
}

.info-row:last-child {
    border-bottom: none;
}

.info-label {
    font-size: 14px;
    color: var(--text-secondary);
}

.info-value {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-primary);
}

.toggle-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
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

.settings-group-title {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.4px;
    margin: 12px 0 4px 0;
    padding-left: 2px;
}

.settings-group-title:first-child {
    margin-top: 0;
}

.toggle-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.toggle-label {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-primary);
}

.toggle-desc {
    font-size: 13px;
    color: var(--text-muted);
}

/* Переключатель */
.switch {
    position: relative;
    display: inline-block;
    width: 48px;
    height: 26px;
    flex-shrink: 0;
}

.switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.switch .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--bg-secondary);
    border: 2px solid var(--border-color);
    border-radius: 26px;
    transition: all 0.3s ease;
}

.switch .slider::before {
    content: '';
    position: absolute;
    height: 18px;
    width: 18px;
    left: 2px;
    bottom: 2px;
    background: var(--text-muted);
    border-radius: 50%;
    transition: all 0.3s ease;
}

.switch input:checked + .slider {
    background: var(--accent);
    border-color: var(--accent);
}

.switch input:checked + .slider::before {
    transform: translateX(22px);
    background: white;
}

.switch input:disabled + .slider {
    opacity: 0.5;
    cursor: not-allowed;
}

.info-box {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 16px;
    border-radius: 10px;
    font-size: 13px;
    margin-top: 12px;
}

.info-box.info {
    background: var(--accent-trans);
    color: var(--text-secondary);
}

.info-box i {
    color: var(--accent-text);
    font-size: 18px;
    flex-shrink: 0;
}

.hint-text {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0 0 8px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.hint-text i {
    color: var(--accent-text);
}

.profile-link {
    display: flex;
    gap: 8px;
    margin-bottom: 12px;
}

.profile-link input {
    flex: 1;
    padding: 8px 12px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: 8px;
    color: var(--text-primary);
    font-size: 13px;
    cursor: pointer;
    font-family: monospace;
}

.profile-link input:focus {
    outline: none;
    border-color: var(--accent);
}

.btn-sm {
    padding: 6px 14px;
    font-size: 13px;
}

/* ===== BUTTONS ===== */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 500;
    border-radius: 10px;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.btn-primary {
    background: var(--accent);
    color: #fff;
}

.btn-primary:hover {
    background: var(--accent-hover);
    transform: translateY(-2px);
}

.btn-secondary {
    background: transparent;
    color: var(--text-secondary);
    border: 1px solid var(--border-input);
}

.btn-secondary:hover {
    background: var(--border-light);
}

.btn-danger {
    background: var(--danger-trans);
    color: var(--danger);
    border: 1px solid transparent;
    padding: 10px 16px;
}

.btn-danger:hover {
    background: rgba(239, 68, 68, 0.2);
}

.btn-sm {
    padding: 6px 14px;
    font-size: 13px;
    min-height: 36px;
}

.outline-btn {
    background: transparent;
    border: 1px solid var(--accent);
    color: var(--accent);
    padding: 10px 16px;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s;
    font-weight: 500;
}

.outline-btn:hover {
    background: var(--accent);
    color: #fff;
}

/* ============================================ */
/* ===== АДАПТИВНОСТЬ ===== */
/* ============================================ */

@media (max-width: 1024px) {
    .profile-grid {
        grid-template-columns: 1fr;
        grid-template-rows: repeat(1, 2fr);
    }

    .profile-sidebar {
        display: flex;
        flex-direction: column;
        gap: 16px;
    }

    .stats-card {
        grid-template-columns: repeat(4, 1fr);
    }
}

@media (max-width: 768px) {
    .profile-sidebar {
        grid-template-columns: 1fr;
    }

    .profile-card {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .profile-info-items {
        width: 100%;
    }

    .profile-bio {
        width: 100%;
    }

    .profile-social {
        width: 100%;
        justify-content: center;
    }

    .profile-actions {
        width: 100%;
        flex-direction: column;
    }

    .profile-actions .btn {
        width: 100%;
    }

    .stats-card {
        grid-template-columns: repeat(4, 1fr);
    }

    .info-row {
        flex-direction: column;
        align-items: flex-start;
        gap: 4px;
    }

    .profile-link {
        flex-direction: column;
    }

    .profile-link input {
        width: 100%;
    }
}

@media (max-width: 480px) {
    .stats-card {
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
    }

    .settings-card-body {
        padding: 16px;
    }

    .profile-card {
        padding: 16px;
    }

    .profile-avatar-wrapper {
        width: 100px;
        height: 100px;
    }

    .stat-value {
        font-size: 18px;
    }
}
</style>
