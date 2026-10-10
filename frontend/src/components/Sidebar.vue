<template>
    <button class="sidebar-toggle" @click="toggleSidebar" :class="{ active: isSidebarOpen }">
        <span class="burger-line"></span>
        <span class="burger-line"></span>
        <span class="burger-line"></span>
    </button>

    <div class="sidebar-overlay" v-if="isSidebarOpen && !isDesktop" @click="closeSidebar"></div>

    <aside
        class="sidebar"
        :class="{
            'sidebar-open': isSidebarOpen,
            'sidebar-collapsed': isCollapsed && isDesktop
        }"
    >
        <div class="sidebar-logo">
            <img src="/icons/favicon-remove-bg.png" alt="MotoBind">
            <div class="logo-text" v-if="!isCollapsed || !isDesktop">
                <span class="logo-left">Moto</span><span class="logo-right">Bind</span>
                <span v-if="$route.path.startsWith('/admin')" class="admin-logo">Admin</span>
            </div>
        </div>

        <!-- Пользовательская навигация -->
        <nav class="sidebar-nav">
            <!-- Пользовательская навигация -->
            <template v-if="!$route.path.startsWith('/admin')">
                <!-- === ГАРАЖ === -->
                <div class="nav-group">
                <p v-if="!isCollapsed || !isDesktop" class="nav-group-title">Гараж</p>

                <router-link
                    to="/garage"
                    class="nav-link"
                    :class="{ active: isActive('/garage') }"
                    @click="closeSidebar"
                >
                    <i class="fa fa-motorcycle"></i>
                    <span v-if="!isCollapsed || !isDesktop">Мой гараж</span>
                </router-link>

                <router-link
                    to="/maintenance"
                    class="nav-link"
                    :class="{ active: isActive('/maintenance') }"
                    @click="closeSidebar"
                >
                    <i class="fa fa-tools"></i>
                    <span v-if="!isCollapsed || !isDesktop">Обслуживание</span>
                </router-link>

                <router-link
                    to="/bookings"
                    class="nav-link"
                    :class="{ active: isActive('/bookings') }"
                    @click="closeSidebar"
                >
                    <i class="fa fa-calendar-check"></i>
                    <span v-if="!isCollapsed || !isDesktop">Мои заявки</span>
                    <span
                    v-if="myBookingsBadge > 0 && (!isCollapsed || !isDesktop)"
                    class="nav-badge"
                    >{{ myBookingsBadge }}</span>
                </router-link>
                </div>

                <!-- === СООБЩЕСТВО === -->
                <div class="nav-group">
                <p v-if="!isCollapsed || !isDesktop" class="nav-group-title">Сообщество</p>

                <router-link
                    to="/masters"
                    class="nav-link"
                    :class="{ active: isActive('/masters') }"
                    @click="closeSidebar"
                >
                    <i class="fa fa-user-tie"></i>
                    <span v-if="!isCollapsed || !isDesktop">Мастера и СТО</span>
                </router-link>

                <router-link
                    to="/manuals"
                    class="nav-link"
                    :class="{ active: isActive('/manuals') }"
                    @click="closeSidebar"
                >
                    <i class="fa fa-book"></i>
                    <span v-if="!isCollapsed || !isDesktop">Мануалы</span>
                </router-link>

                <router-link
                    to="/social"
                    class="nav-link"
                    :class="{ active: isActive('/social') }"
                    @click="closeSidebar"
                >
                    <i class="fa fa-users"></i>
                    <span v-if="!isCollapsed || !isDesktop">MotoSocial</span>
                </router-link>
                </div>

                <!-- === МОЙ БИЗНЕС === (только если есть бизнес-аккаунт) -->
                <div v-if="hasBusinessAccount" class="nav-group">
                <p v-if="!isCollapsed || !isDesktop" class="nav-group-title">Мой бизнес</p>

                <router-link
                    to="/business"
                    class="nav-link"
                    :class="{ active: isActive('/business', { exact: true }) }"
                    @click="closeSidebar"
                >
                    <i class="fa fa-suitcase"></i>
                    <span v-if="!isCollapsed || !isDesktop">Кабинет бизнеса</span>
                </router-link>

                <router-link
                    to="/business/clients"
                    class="nav-link"
                    :class="{ active: isActive('/business/clients') }"
                    @click="closeSidebar"
                >
                    <i class="fa fa-users"></i>
                    <span v-if="!isCollapsed || !isDesktop">Клиенты</span>
                </router-link>

                <router-link
                    to="/business/services"
                    class="nav-link"
                    :class="{ active: isActive('/business/services') }"
                    @click="closeSidebar"
                >
                    <i class="fa fa-wrench"></i>
                    <span v-if="!isCollapsed || !isDesktop">Мои услуги</span>
                </router-link>

                <router-link
                    to="/business/bookings"
                    class="nav-link"
                    :class="{ active: isActive('/business/bookings') }"
                    @click="closeSidebar"
                >
                    <i class="fa fa-inbox"></i>
                    <span v-if="!isCollapsed || !isDesktop">Заявки мастеру</span>
                    <span
                    v-if="pendingMasterBookings > 0 && (!isCollapsed || !isDesktop)"
                    class="nav-badge"
                    >{{ pendingMasterBookings }}</span>
                </router-link>
                </div>

                <!-- === Админ-панель (для админа) === -->
                <router-link
                    v-if="isAdmin"
                    to="/admin/panel"
                    class="nav-link admin-link"
                    :class="{ active: isActive('/admin/panel') }"
                    @click="closeSidebar"
                >
                    <i class="fa fa-shield"></i>
                    <span v-if="!isCollapsed || !isDesktop">Админ-панель</span>
                </router-link>
            </template>

            <!-- Админская навигация -->
            <div v-else class="admin-nav">
                <div class="admin-nav-group">
                    <p v-if="!isCollapsed || !isDesktop" class="nav-group-title">ГЛАВНАЯ</p>
                    <router-link
                        to="/admin/panel"
                        class="nav-link"
                        :class="{ active: $route.path === '/admin/panel' }"
                        @click="closeSidebar"
                    >
                        <i class="fa fa-sitemap"></i>
                        <span v-if="!isCollapsed || !isDesktop">Панель управления</span>
                    </router-link>
                </div>

                <div class="admin-nav-group">
                    <p v-if="!isCollapsed || !isDesktop" class="nav-group-title">УПРАВЛЕНИЕ</p>
                    <router-link
                        to="/admin/users"
                        class="nav-link"
                        :class="{ active: $route.path === '/admin/users' }"
                        @click="closeSidebar"
                    >
                        <i class="fa fa-users"></i>
                        <span v-if="!isCollapsed || !isDesktop">Пользователи</span>
                    </router-link>
                    <router-link
                        to="/admin/motorcycles"
                        class="nav-link"
                        :class="{ active: $route.path === '/admin/motorcycles' }"
                        @click="closeSidebar"
                    >
                        <i class="fa fa-motorcycle"></i>
                        <span v-if="!isCollapsed || !isDesktop">Мотоциклы</span>
                    </router-link>
                </div>

                <div class="admin-nav-group">
                    <p v-if="!isCollapsed || !isDesktop" class="nav-group-title">МОДЕРАЦИЯ</p>
                    <router-link
                        to="/admin/manuals"
                        class="nav-link"
                        :class="{ active: $route.path === '/admin/manuals' }"
                        @click="closeSidebar"
                    >
                        <i class="fa fa-tools"></i>
                        <span v-if="!isCollapsed || !isDesktop">Мануалы</span>
                    </router-link>
                    <router-link
                        to="/admin/reports"
                        class="nav-link"
                        :class="{ active: $route.path === '/admin/reports' }"
                        @click="closeSidebar"
                    >
                        <i class="fa fa-flag"></i>
                        <span v-if="!isCollapsed || !isDesktop">Репорты</span>
                    </router-link>
                    <router-link
                        to="/admin/services"
                        class="nav-link"
                        :class="{ active: $route.path === '/admin/services' }"
                        @click="closeSidebar"
                    >
                        <i class="fa fa-wrench"></i>
                        <span v-if="!isCollapsed || !isDesktop">Услуги</span>
                    </router-link>
                </div>

                <router-link
                    v-if="isAdmin"
                    to="/garage"
                    class="nav-link admin-link"
                    @click="closeSidebar"
                >
                    <i class="fa fa-home"></i>
                    <span v-if="!isCollapsed || !isDesktop">Назад к сервису</span>
                </router-link>
            </div>
        </nav>

        <!-- Нижняя часть сайдбара -->
        <div class="sidebar-footer">
            <div v-if="!isDesktop" class="footer-row-mobile">
                <button
                class="theme-toggle"
                @click="toggleTheme"
                :title="isDark ? 'Включить светлую тему' : 'Включить тёмную тему'"
                >
                <i :class="isDark ? 'fa fa-sun' : 'fa fa-moon'"></i>
                </button>
                <button class="theme-toggle" @click="mobileNotif">
                <i class="fa fa-bell"></i>
                </button>
            </div>

            <router-link
                to="/profile"
                class="nav-link profile-link"
                :class="{ active: isActive('/profile') }"
                @click="closeSidebar"
            >
                <i class="fa fa-user"></i>
                <span v-if="!isCollapsed || !isDesktop">Профиль</span>
            </router-link>

            <button class="btn-logout-sidebar" @click="logout">
                <i class="fa fa-sign-out"></i>
                <span v-if="!isCollapsed || !isDesktop">Выйти</span>
            </button>
        </div>
    </aside>
</template>

<script>
import api from '../api/api';
import router from '../router';
import { useAuthStore } from '../stores/auth';
import { useBusinessStore } from '../stores/business'
import { useBookingsStore } from '../stores/bookings'

export default {
    data() {
        return {
            isSidebarOpen: false,
            isCollapsed: false,
            isDesktop: window.innerWidth > 770,
            isDark: true,
            myBookingsCount: 0,
            pendingBookingsCount: 0,
        }
    },

    computed: {
        isAdmin() {
            return useAuthStore().isAdmin
        },
        hasBusinessAccount() {
            return useBusinessStore().hasAccount
        },
        myBookingsBadge() {
            return this.myBookingsCount
        },
        pendingMasterBookings() {
            return this.pendingBookingsCount
        },
    },

    async mounted() {
        window.addEventListener('resize', this.handleResize);

        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            this.isDark = savedTheme === 'dark';
            document.documentElement.setAttribute('data-theme', savedTheme);
        } else {
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            this.isDark = prefersDark;
            document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
        }

        const auth = useAuthStore()
        if (auth.isAuthenticated) {
            try {
                const business = useBusinessStore()
                await business.loadAccount()
            } catch {
            }
            this.loadBadges()
        }
    },

    beforeDestroy() {
        window.removeEventListener('resize', this.handleResize);
    },

    methods: {
        isActive(path, { exact = false } = {}) {
            const current = this.$route.path
            if (exact) return current === path
            return current === path || current.startsWith(path + '/')
        },

        async loadBadges() {
            const bookings = useBookingsStore()
            try {
                const mine = await bookings.loadMyBookings()
                this.myBookingsCount = mine.filter(
                    (b) => b.status === 'pending' || b.status === 'confirmed'
                ).length

                if (this.hasBusinessAccount) {
                    const master = await bookings.loadMasterBookings()
                    this.pendingBookingsCount = master.filter(
                        (b) => b.status === 'pending'
                    ).length
                }
            } catch {
            }
        },

        mobileNotif() {
            this.$router.push('/notifications')
            this.closeSidebar()
        },
        handleResize() {
            this.isDesktop = window.innerWidth > 770;
            if (this.isDesktop) {
                this.isSidebarOpen = true;
            } else {
                if (!this.isDesktop) {
                    this.isSidebarOpen = false;
                }
            }
        },

        toggleSidebar() {
            this.isSidebarOpen = !this.isSidebarOpen;
        },

        closeSidebar() {
            if (!this.isDesktop) {
                this.isSidebarOpen = false;
            }
        },

        toggleTheme() {
            this.isDark = !this.isDark
            const theme = this.isDark ? 'dark' : 'light'
            document.documentElement.setAttribute('data-theme', theme)
            localStorage.setItem('theme', theme)
        },

        async logout() {
            try {
                await api.post('/auth/logout');
            } catch(err) {
                console.error('Logout failed:', err);
            } finally {
                useAuthStore().logout()
                this.closeSidebar();
                router.push('/login');
            }
        }
    },
}
</script>

<style scoped>
/* ===== Кнопка-гамбургер ===== */
.sidebar-toggle {
    position: fixed;
    top: 20px;
    left: 20px;
    z-index: 1001;
    display: none;
    flex-direction: column;
    gap: 12px;
    width: 30px;
    height: 21px;
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 0;
    border-radius: 0px !important;
}

@media (max-width: 770px) {
    .sidebar-toggle {
        display: flex;
    }
}

.sidebar-toggle .burger-line {
    width: 100%;
    height: 3px;
    background-color: var(--text-primary, #fff);
    transition: all 0.3s ease;
}

.sidebar-toggle.active .burger-line:nth-child(1) {
    transform: translateY(7px) rotate(35deg);
}

.sidebar-toggle.active .burger-line:nth-child(2) {
    opacity: 0;
}

.sidebar-toggle.active .burger-line:nth-child(3) {
    transform: translateY(-7px) rotate(-35deg);
}

/* ===== Оверлей ===== */
.sidebar-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 999;
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* ===== Сайдбар ===== */
.sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: 260px;
    height: 100vh;
    background: var(--bg-primary, #0f0f1a);
    z-index: 1000;
    display: flex;
    flex-direction: column;
    padding: 24px 16px;
    transition: all 0.3s ease;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    transform: translateX(0);
}

/* Свернутый сайдбар — только иконки */
.sidebar-collapsed {
    width: 64px;
    padding: 24px 10px;
}

.sidebar-collapsed .nav-link span,
.sidebar-collapsed .logo-text:not(.logo-collapsed),
.sidebar-collapsed .nav-group-title,
.sidebar-collapsed .btn-logout-sidebar span {
    display: none;
}

.sidebar-collapsed .nav-link {
    justify-content: center;
    padding: 10px 0;
}

.sidebar-collapsed .nav-link i {
    font-size: 18px;
    margin: 0;
}

.sidebar-collapsed .btn-logout-sidebar {
    justify-content: center;
}

/* На мобильных */
@media (max-width: 770px) {
    .sidebar {
        transform: translateX(-100%);
        width: 280px;
        padding: 24px 20px;
    }

    .sidebar.sidebar-open {
        transform: translateX(0);
    }

    /* На мобильных сворачивание отключено */
    .sidebar-collapsed {
        width: 280px;
        padding: 24px 20px;
    }

    .sidebar-collapsed .nav-link span,
    .sidebar-collapsed .logo-text,
    .sidebar-collapsed .btn-logout-sidebar span {
        display: inline !important;
    }

    .sidebar-collapsed .nav-link {
        justify-content: flex-start;
        padding: 10px 14px;
    }

    .sidebar-collapsed .nav-link i {
        margin: 0 14px 0 0;
    }
}

/* ===== Логотип с кнопкой сворачивания ===== */
.sidebar-logo {
    display: flex;
    flex-direction: row;
    align-items: center;
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    margin-bottom: 16px;
    gap: 10px;
    position: relative;
}

.sidebar-logo img {
    width: 40px;
    height: 40px;
    flex-shrink: 0;
}

.logo-text {
    font-size: 22px;
    font-weight: 700;
    white-space: nowrap;
    flex: 1;
}

.logo-left {
    color: var(--text-primary);
}

.logo-right {
    color: var(--accent) !important;
}

.admin-logo {
    font-size: 14px;
    color: var(--accent);
    margin-left: 4px;
}

.collapse-toggle {
    width: 28px;
    height: 28px;
    background: var(--bg-secondary);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    flex-shrink: 0;
}

.collapse-toggle:hover {
    background: var(--bg-card-hover);
    color: var(--text-primary);
    border-color: var(--accent);
}

.sidebar-collapsed .sidebar-logo {
    justify-content: center;
    padding-bottom: 16px;
}

.sidebar-collapsed .sidebar-logo img {
    display: none;
}

.sidebar-collapsed .logo-text {
    display: none;
}

.sidebar-collapsed .collapse-toggle {
    position: absolute;
    right: -14px;
    top: 50%;
    transform: translateY(-50%);
    background: var(--bg-primary);
    width: 24px;
    height: 24px;
    font-size: 10px;
}

/* На мобильных кнопка сворачивания скрыта */
@media (max-width: 770px) {
    .collapse-toggle {
        display: none !important;
    }
}

/* === Группы навигации === */
.nav-group {
    display: flex;
    flex-direction: column;
    gap: 2px;
    margin-bottom: 14px;
}

.nav-group:last-child {
    margin-bottom: 0;
}

.nav-group-title {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-muted);
    margin: 0 0 4px 14px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    opacity: 0.6;
}

.sidebar-collapsed .nav-group {
    margin-bottom: 10px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}

.sidebar-collapsed .nav-group:last-child {
    border-bottom: none;
}

/* === Бейджи === */
.nav-badge {
    margin-left: auto;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 20px;
    height: 20px;
    padding: 0 6px;
    border-radius: var(--radius-full, 9999px);
    background: var(--accent);
    color: #fff;
    font-size: 11px;
    font-weight: 600;
    flex-shrink: 0;
}

.nav-link.active .nav-badge {
    background: #fff;
    color: var(--accent);
}

/* === Футер === */
.footer-row-mobile {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-bottom: 8px;
}

.footer-row-mobile .theme-toggle {
    margin-bottom: 0;
}

.profile-link {
    margin-bottom: 8px;
    /* чтобы не сливался с «Выйти» */
}

/* На мобильных группы не нужны — там вертикальный список короткий */
@media (max-width: 770px) {
    .nav-group {
        margin-bottom: 8px;
    }

    .nav-group:not(:first-child)::before {
        content: '';
        display: block;
        height: 1px;
        background: rgba(255, 255, 255, 0.05);
        margin: 8px 0;
    }

    .nav-group-title {
        margin-left: 4px;
    }
}

/* ===== Навигация ===== */
.sidebar-nav {
    display: flex;
    flex-direction: column;
    gap: 2px;
    flex: 1;
    overflow-y: auto;
}

.nav-link {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 10px 14px;
    border-radius: 10px;
    color: var(--text-secondary, #888899);
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s ease;
    text-decoration: none;
    white-space: nowrap;
}

.nav-link i {
    width: 20px;
    font-size: 16px;
    text-align: center;
    color: var(--text-secondary);
    transition: color 0.2s ease;
    flex-shrink: 0;
}

.nav-link:hover {
    background: rgba(255, 255, 255, 0.05);
    color: var(--text-primary);
}

.nav-link:hover i {
    color: var(--text-primary);
}

.nav-link.active {
    background: var(--accent-trans);
    color: var(--accent);
}

.nav-link.active i {
    color: var(--accent);
}

.admin-nav-group {
    margin-bottom: 10px;
}

.nav-group-title {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-muted);
    margin: 0 0 6px 14px;
    letter-spacing: 0.5px;
}

.nav-link.admin-link {
    margin-top: 4px;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    padding-top: 12px;
    color: var(--warning);
}

.nav-link.admin-link i {
    color: var(--warning);
}

.nav-link.admin-link:hover {
    background: rgba(245, 158, 11, 0.05);
}

.nav-link.admin-link.active {
    background: rgba(245, 158, 11, 0.12);
}

/* ===== Футер ===== */
.sidebar-footer {
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    padding-top: 12px;
}

.btn-logout-sidebar {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 10px;
    border: none;
    background: rgba(239, 68, 68, 0.08);
    color: #ef4444;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    width: 100%;
}

.btn-logout-sidebar:hover {
    background: rgba(239, 68, 68, 0.18);
}

.btn-logout-sidebar i {
    font-size: 16px;
    flex-shrink: 0;
}

/* ===== КНОПКА ПЕРЕКЛЮЧЕНИЯ ТЕМЫ ===== */
.theme-toggle {
    width: 100%;
    padding: 0;
    background: var(--bg-primary);
    border: 2px solid var(--border-color);
    color: var(--text-primary);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    transition: all 0.3s ease;
    margin-bottom: 12px;
}

.theme-toggle:hover {
    background: var(--accent);
    border-color: var(--accent);
    color: white;
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
}

.theme-toggle i {
    transition: transform 0.3s ease;
}

@media (max-width: 480px) {
    .sidebar {
        width: 85%;
        max-width: 300px;
    }
}

@media (min-width: 771px) {
    .sidebar-overlay {
        display: none;
    }
}

.sidebar-nav::-webkit-scrollbar {
    width: 4px;
}

.sidebar-nav::-webkit-scrollbar-track {
    background: transparent;
}

.sidebar-nav::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
}

.sidebar-nav::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.2);
}
</style>
