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
                        <button class="avatar-edit-btn" @click="$refs.avatarInput.click()" title="Изменить аватар">
                            <i class="fa fa-camera"></i>
                        </button>
                        <input
                            ref="avatarInput"
                            type="file"
                            accept="image/*"
                            @change="handleAvatarUpload"
                            style="display: none"
                        />
                    </div>
                    
                    <h3 class="profile-username">{{ user?.username || 'Пользователь' }}</h3>
                    <p class="profile-email">{{ user?.email || '—' }}</p>
                    
                    <div class="profile-badge">
                        <span :class="getStatusClass(user?.status)">
                            {{ getStatusName(user?.status) }}
                        </span>
                        <span class="role-badge">{{ getRoleName(user?.role) }}</span>
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
                            <span>{{ getExperienceLabel(user.experience) }}</span>
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
                            <span class="info-value">{{ getExperienceLabel(user?.experience) || 'Не указан' }}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Роль</span>
                            <span class="info-value">{{ getRoleName(user?.role) }}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Статус</span>
                            <span class="info-value">
                                <span :class="getStatusClass(user?.status)">
                                    {{ getStatusName(user?.status) }}
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

<script>
import api from '../api/api'
import { removeTokens } from '../api/auth'
import EditProfileModal from '../components/modals/user/EditProfileModal.vue'
import ChangePasswordModal from '../components/modals/user/ChangePasswordModal.vue'
import DeleteAccountModal from '../components/modals/user/DeleteAccountModal.vue'
import Header from '../components/Header.vue'
import LoadingOverlay from '../components/LoadingOverlay.vue'

export default {
    name: 'ProfilePage',

    components: {
        EditProfileModal,
        ChangePasswordModal,
        DeleteAccountModal,
        Header,
        LoadingOverlay
    },

    data() {
        return {
            loading: false,
            uploadingAvatar: false,

            user: null,
            stats: {
                posts: 0,
                likes: 0,
                comments: 0,
                motorcycles: 0
            },

            showEditProfile: false,
            showChangePassword: false,
            showDeleteAccount: false
        }
    },

    computed: {
        profileUrl() {
            const baseUrl = window.location.origin
            return `${baseUrl}/profile/${this.user?.id || ''}`
        },
        hasSocialLinks() {
            return this.user?.social_links && 
                   Object.values(this.user.social_links).some(url => url && url.trim())
        }
    },

    methods: {
        // ===== АВАТАР =====
        getAvatarUrl(avatarPath) {
            if (!avatarPath || typeof avatarPath !== 'string') {
                return '/BaseAvatar.jpg'
            }
            if (avatarPath.startsWith('http')) {
                return avatarPath
            }
            const baseUrl = import.meta.env.VITE_API_URL || ''
            return `${baseUrl}/uploads/${avatarPath}`
        },

        handleAvatarError(event) {
            event.target.src = '/BaseAvatar.jpg'
        },

        async handleAvatarUpload(event) {
            const file = event.target.files[0]
            if (!file) return

            if (file.size > 5 * 1024 * 1024) {
                alert('Файл слишком большой. Максимальный размер 5 МБ.')
                this.$refs.avatarInput.value = ''
                return
            }

            const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp', 'image/webp']
            if (!allowedTypes.includes(file.type)) {
                alert('Неподдерживаемый формат. Разрешены: JPG, PNG, GIF, BMP, WEBP')
                this.$refs.avatarInput.value = ''
                return
            }

            this.uploadingAvatar = true
            try {
                const formData = new FormData()
                formData.append('avatar', file)

                const { data } = await api.post('/user/avatar', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                })

                localStorage.setItem('user', JSON.stringify(data))
                this.user = data
                alert('Аватар успешно обновлен!')
            } catch (error) {
                console.error('Error uploading avatar:', error)
                alert(error.response?.data?.error || 'Ошибка загрузки аватара')
            } finally {
                this.uploadingAvatar = false
                this.$refs.avatarInput.value = ''
            }
        },

        async deleteAvatar() {
            if (!confirm('Удалить аватар?')) return

            try {
                const { data } = await api.delete('/user/avatar')
                this.user = data
                alert('Аватар удален')
            } catch (error) {
                console.error('Error deleting avatar:', error)
                alert(error.response?.data?.error || 'Ошибка удаления аватара')
            }
        },

        // ===== ЗАГРУЗКА ПРОФИЛЯ =====
        async loadProfile() {
            this.loading = true
            try {
                const response = await api.get('/user/profile/me')
                this.user = response.data.user
                this.stats = {
                    posts: response.data.user.stats?.posts_count || 0,
                    likes: response.data.user.stats?.likes_received || 0,
                    comments: response.data.user.stats?.comments_received || 0,
                    motorcycles: response.data.user.motorcycles?.length || 0
                }
            } catch (error) {
                console.error('Error loading profile:', error)
                if (error.response?.status === 401) {
                    this.$router.push('/login')
                }
            } finally {
                this.loading = false
            }
        },

        // ===== ОБНОВЛЕНИЕ ПРОФИЛЯ =====
        async updateProfile(formData) {
            try {
                const response = await api.put('/user/profile', formData)
                localStorage.setItem('user', JSON.stringify(response.data))
                this.user = response.data
                this.showEditProfile = false
                alert('Профиль обновлен!')
            } catch (error) {
                console.error('Error updating profile:', error)
                alert(error.response?.data?.message || 'Ошибка при обновлении профиля')
            }
        },

        // ===== БЕЗОПАСНОСТЬ =====
        async changePassword(formData) {
            try {
                if (formData.newPassword !== formData.repeatPassword) {
                    alert('Пароли не совпадают')
                    return
                }

                await api.patch('/user/change-password', formData)
                this.showChangePassword = false
                alert('Пароль успешно изменен!')
            } catch (error) {
                console.error('Error changing password:', error)
                alert(error.response?.data?.message || 'Ошибка при смене пароля')
            }
        },

        async deleteAccount(password) {
            try {
                await api.delete('/user/account', {
                    data: { password }
                })
                this.showDeleteAccount = false
                removeTokens()
                this.$router.push('/login')
            } catch (error) {
                console.error('Error deleting account:', error)
                alert(error.response?.data?.message || 'Ошибка при удалении аккаунта')
            }
        },

        // ===== ПУБЛИЧНЫЙ ПРОФИЛЬ =====
        viewPublicProfile() {
            this.$router.push(`/profile/${this.user.id}`)
        },

        copyProfileLink() {
            navigator.clipboard.writeText(this.profileUrl).then(() => {
                alert('Ссылка на профиль скопирована!')
            }).catch(() => {
                const input = document.querySelector('.profile-link input')
                input.select()
                document.execCommand('copy')
                alert('Ссылка на профиль скопирована!')
            })
        },

        // ===== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ =====
        formatDate(dateString) {
            if (!dateString) return '—'
            try {
                const date = new Date(dateString)
                if (isNaN(date.getTime())) return '—'
                return date.toLocaleDateString('ru-RU', {
                    day: '2-digit',
                    month: 'short',
                    year: 'numeric'
                })
            } catch {
                return '—'
            }
        },

        getStatusName(status) {
            const map = {
                'active': 'Активен',
                'banned': 'Заблокирован',
                'pending': 'Ожидает'
            }
            return map[status] || status || '—'
        },

        getStatusClass(status) {
            const map = {
                'active': 'status-active',
                'banned': 'status-banned',
                'pending': 'status-pending'
            }
            return map[status] || ''
        },

        getRoleName(role) {
            const map = {
                'admin': 'Администратор',
                'motorcyclist': 'Мотоциклист',
                'motoclub': 'Мотоклуб'
            }
            return map[role] || role || '—'
        },

        getExperienceLabel(experience) {
            const map = {
                'beginner': 'Новичок',
                'intermediate': 'Опытный',
                'expert': 'Эксперт'
            }
            return map[experience] || experience || 'Не указан'
        },

        getSocialIcon(platform) {
            const icons = {
                'instagram': 'fa fa-instagram',
                'youtube': 'fa fa-youtube',
                'telegram': 'fa fa-telegram',
                'vk': 'fa fa-vk',
                'facebook': 'fa fa-facebook',
                'twitter': 'fa fa-twitter',
                'tiktok': 'fa fa-tiktok'
            }
            return icons[platform] || 'fa fa-link'
        },

        async logout() {
            try {
                await api.post('/auth/logout')
            } catch(err) { console.error(err) }
            finally {
                removeTokens()
                this.$router.push('/login')
            }
        }
    },

    mounted() {
        this.loadProfile()
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
    }

    .profile-sidebar {
        display: grid;
        grid-template-columns: 1fr 1fr;
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