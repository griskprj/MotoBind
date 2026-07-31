<template>
    <div class="container">
        <!-- === HEADER === -->
        <header class="page-header">
            <div class="header-left">
                <h2>Профиль</h2>
                <p class="header-subtitle">
                    Управление личными данными и настройками аккаунта.
                </p>
            </div>

            <div class="header-right">
                <i class="fa fa-bell notification-icon"></i>
                <div class="profile-wrapper">
                    <img :src="user?.avatar || '/BaseAvatar.jpg'" alt="avatar" class="profile-img">
                    <button class="dropdown-trigger" @click="welcomeDropdownActive = !welcomeDropdownActive">
                        <i class="fa" :class="welcomeDropdownActive ? 'fa-angle-up' : 'fa-angle-down'"></i>
                    </button>
                    <div v-if="welcomeDropdownActive" class="dropdown-list">
                        <ul>
                            <li><button class="dropdown-item" disabled>Профиль</button></li>
                            <li><button class="dropdown-item" @click="logout">Выйти</button></li>
                        </ul>
                    </div>
                </div>
            </div>
        </header>

        <!-- === PROFILE CONTENT === -->
        <div class="profile-grid">
            <!-- LEFT COLUMN: Avatar & Info -->
            <aside class="profile-sidebar">
                <div class="profile-card">
                    <div class="profile-avatar-wrapper">
                        <img 
                            :src="user?.avatar || '/BaseAvatar.jpg'" 
                            alt="avatar" 
                            class="profile-avatar"
                        >
                    </div>
                    <h3 class="profile-username">{{ user?.username || 'Пользователь' }}</h3>
                    <p class="profile-email">{{ user?.email || '—' }}</p>
                    <div class="profile-badge">
                        <span :class="getStatusClass(user?.status)">
                            {{ getStatusName(user?.status) }}
                        </span>
                        <span class="role-badge">{{ getRoleName(user?.role) }}</span>
                    </div>

                    <p class="profile-bio">
                        {{ user?.bio }}
                    </p>

                    <div class="profile-actions">
                        <button class="outline-btn" style="width: 100%;" @click="showEditProfile = true">
                            <i class="fa fa-pen"></i> Редактировать
                        </button>
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
            </main>
        </div>
    </div>

    <!-- === MODALS === -->
    <EditUserModal
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
import EditUserModal from '../components/modals/user/EditUserModal.vue';
import ChangePasswordModal from '../components/modals/user/ChangePasswordModal.vue';
import DeleteAccountModal from '../components/modals/user/DeleteAccountModal.vue';

export default {
    name: 'ProfilePage',

    components: {
        EditUserModal,
        ChangePasswordModal,
        DeleteAccountModal
    },

    data() {
        return {
            welcomeDropdownActive: false,
            loading: false,

            user: null,
            stats: {
                motorcycles: 0,
                maintenances: 0,
                manuals: 0
            },
            sessions: [],

            showEditProfile: false,
            showChangePassword: false,
            showDeleteAccount: false
        }
    },

    methods: {
        async loadProfile() {
            this.loading = true
            try {
                const response = await api.get('/auth/me')
                this.user = response.data
            } catch (error) {
                console.error('Error loading profile:', error)
                if (error.response?.status === 401) {
                    this.$router.push('/login')
                }
            } finally {
                this.loading = false
            }
        },

        async updateProfile(formData) {
            try {
                const response = await api.put('/user/profile', formData)
                this.user = response.data
                this.showEditProfile = false
                alert('Профиль обновлен!')
            } catch (error) {
                console.error('Error updating profile:', error)
                alert(error.response?.data?.message || 'Ошибка при обновлении профиля')
            }
        },

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

        async logout() {
            try {
                await api.post('/auth/logout')
            } catch(err) { console.error(err) }
            finally {
                removeTokens()
                this.$router.push('/login')
            }
        },

        // Работа с модальными окнами

        // Вспомогательные методы
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
                'club_member': 'Член клуба'
            }
            return map[role] || role || '—'
        },

        getDeviceIcon(device) {
            const map = {
                'desktop': 'fa-desktop',
                'mobile': 'fa-mobile',
                'tablet': 'fa-tablet',
                'chrome': 'fa-chrome',
                'firefox': 'fa-firefox',
                'safari': 'fa-safari',
                'edge': 'fa-edge'
            }
            return map[device] || 'fa-laptop'
        }
    },

    mounted() {
        this.loadProfile()
    }
}
</script>

<style scoped>
/* ===== HEADER ===== */
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    flex-wrap: wrap;
    gap: 16px;
}
.header-left h2 {
    margin: 0 0 12px 0;
    font-size: 24px;
}
.header-subtitle {
    font-size: 14px;
    color: var(--text-secondary);
}
.header-right {
    display: flex;
    align-items: center;
    gap: 16px;
}
.notification-icon {
    font-size: 20px;
    color: #8b8b9e;
    cursor: pointer;
}
.profile-wrapper {
    display: flex;
    align-items: center;
    gap: 6px;
    position: relative;
}
.profile-img {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    border: 2px solid #7c3aed;
}
.dropdown-trigger {
    background: transparent;
    border: none;
    color: #8b8b9e;
    cursor: pointer;
}
.dropdown-list {
    position: absolute;
    top: 48px;
    right: 0;
    background: #181824;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 8px;
    min-width: 140px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    z-index: 100;
    animation: slideInUp 0.2s ease;
}
.dropdown-list ul {
    list-style: none;
    margin: 0;
    padding: 0;
}
.dropdown-item {
    width: 100%;
    padding: 8px 12px;
    background: transparent;
    border: none;
    color: #ccc;
    text-align: left;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
}
.dropdown-item:hover {
    background: rgba(255,255,255,0.05);
}
.dropdown-item:disabled {
    opacity: 0.6;
    cursor: default;
}

@media (max-width: 720px) {
    .header-right {
        display: none;
    }
}

/* ===== PROFILE GRID ===== */
.profile-grid {
    display: grid;
    grid-template-columns: 320px 1fr;
    gap: 24px;
    align-items: start;
}

/* ===== SIDEBAR ===== */
.profile-sidebar {
    position: sticky;
    top: 24px;
}

.profile-card {
    background: var(--bg-card);
    border: 1px solid rgba(255,255,255,0.05);
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
    width: 32px;
    height: 32px;
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
    background: #6d28d9;
    transform: scale(1.05);
}

.profile-username {
    font-size: 20px;
    font-weight: 600;
    margin: 0 0 4px 0;
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
    margin-bottom: 16px;
}

.status-active {
    display: inline-block;
    padding: 2px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    background: rgba(74, 222, 128, 0.12);
    color: #4ade80;
}

.status-banned {
    display: inline-block;
    padding: 2px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    background: rgba(239, 68, 68, 0.12);
    color: #ef4444;
}

.status-pending {
    display: inline-block;
    padding: 2px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    background: rgba(251, 191, 36, 0.12);
    color: #fbbf24;
}

.role-badge {
    display: inline-block;
    padding: 2px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    background: rgba(124, 58, 237, 0.12);
    color: var(--accent);
}

.profile-bio {
    font-size: 14px;
    color: var(--text-muted);
    margin-bottom: 14px;
    font-style: italic;
}

.profile-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    padding: 16px 0;
    border-top: 1px solid rgba(255,255,255,0.05);
    border-bottom: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 16px;
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

.profile-actions {
    display: flex;
    gap: 8px;
}

.profile-actions .btn {
    flex: 1;
}

/* ===== SETTINGS ===== */
.settings-card {
    background: var(--bg-card);
    border: 1px solid rgba(255,255,255,0.05);
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
    border-bottom: 1px solid rgba(255,255,255,0.05);
    background: rgba(255,255,255,0.02);
}

.settings-card-header i {
    font-size: 18px;
    color: var(--accent);
}

.settings-card-header h3 {
    font-size: 16px;
    font-weight: 600;
    margin: 0;
}

.sessions-count {
    margin-left: auto;
    font-size: 13px;
    color: var(--text-secondary);
    background: rgba(255,255,255,0.05);
    padding: 2px 12px;
    border-radius: 20px;
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
    border-bottom: 1px solid rgba(255,255,255,0.04);
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
}

.settings-card-body .btn {
    width: 100%;
    margin-bottom: 8px;
    justify-content: center;
}

.settings-card-body .btn:last-child {
    margin-bottom: 0;
}

/* ===== SESSIONS ===== */
.session-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}

.session-item:last-child {
    border-bottom: none;
}

.session-info {
    display: flex;
    align-items: center;
    gap: 12px;
}

.session-info i {
    font-size: 20px;
    color: var(--text-secondary);
    width: 24px;
    text-align: center;
}

.session-device {
    font-size: 14px;
    font-weight: 500;
    margin: 0;
}

.session-meta {
    font-size: 12px;
    color: var(--text-secondary);
    margin: 0;
}

.btn-remove-session {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 6px;
    transition: all 0.2s;
}

.btn-remove-session:hover {
    background: rgba(239, 68, 68, 0.1);
    color: var(--danger);
}

.current-badge {
    font-size: 12px;
    color: #4ade80;
    background: rgba(74, 222, 128, 0.12);
    padding: 2px 12px;
    border-radius: 20px;
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

.btn-primary {
    background: var(--accent);
    color: #fff;
}

.btn-primary:hover {
    background: #6d28d9;
    transform: translateY(-2px);
}

.btn-secondary {
    background: transparent;
    color: var(--text-secondary);
    border: 1px solid rgba(255,255,255,0.08);
}

.btn-secondary:hover {
    background: rgba(255,255,255,0.05);
}

.btn-danger {
    background: rgba(239, 68, 68, 0.12);
    color: var(--danger);
    border: 1px solid transparent;
    padding: 10px 16px;
}

.btn-danger:hover {
    background: rgba(239, 68, 68, 0.2);
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

/* ===== EMPTY STATE ===== */
.empty-state.small {
    padding: 20px;
    text-align: center;
}

.empty-state.small p {
    margin: 0;
    color: var(--text-secondary);
    font-size: 14px;
}

/* ===== ANIMATIONS ===== */
@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* ===== RESPONSIVE ===== */
@media (max-width: 1024px) {
    .profile-grid {
        grid-template-columns: 1fr;
    }

    .profile-sidebar {
        position: static;
    }

    .profile-card {
        display: grid;
        grid-template-columns: 120px 1fr;
        gap: 16px 24px;
        text-align: left;
        align-items: start;
    }

    .profile-avatar-wrapper {
        margin: 0;
        grid-row: span 4;
    }

    .profile-username {
        grid-column: 2;
        margin-top: 8px;
    }

    .profile-email {
        grid-column: 2;
    }

    .profile-badge {
        grid-column: 2;
        justify-content: flex-start;
    }

    .profile-stats {
        grid-column: 2;
        grid-template-columns: repeat(3, auto);
        gap: 24px;
        border-top: none;
        border-bottom: none;
        padding: 0;
        margin: 0;
    }

    .profile-actions {
        grid-column: 2;
    }
}

@media (max-width: 768px) {
    .profile-card {
        grid-template-columns: 1fr;
        text-align: center;
    }

    .profile-avatar-wrapper {
        margin: 0 auto;
        grid-row: auto;
    }

    .profile-username {
        grid-column: auto;
    }

    .profile-email {
        grid-column: auto;
    }

    .profile-badge {
        grid-column: auto;
        justify-content: center;
    }

    .profile-stats {
        grid-column: auto;
        grid-template-columns: repeat(3, 1fr);
        border-top: 1px solid rgba(255,255,255,0.05);
        border-bottom: 1px solid rgba(255,255,255,0.05);
        padding: 16px 0;
        margin: 0 0 16px 0;
    }

    .profile-actions {
        grid-column: auto;
        flex-direction: column;
    }

    .info-row {
        flex-direction: column;
        align-items: flex-start;
        gap: 4px;
    }
}

@media (max-width: 480px) {
    .settings-card-body {
        padding: 16px;
    }

    .profile-stats {
        gap: 8px;
    }

    .stat-value {
        font-size: 18px;
    }
}
</style>