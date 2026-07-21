<template>
    <!-- Кнопка-гамбургер для открытия сайдбара -->
    <button class="sidebar-toggle" @click="toggleSidebar" :class="{ active: isSidebarOpen }">
        <span class="burger-line"></span>
        <span class="burger-line"></span>
        <span class="burger-line"></span>
    </button>

    <!-- Оверлей -->
    <div class="sidebar-overlay" v-if="isSidebarOpen" @click="closeSidebar"></div>

    <!-- Сайдбар -->
    <aside class="sidebar" :class="{ 'sidebar-open': isSidebarOpen }">
        <!-- Логотип -->
        <div class="sidebar-logo">
            <h1 class="logo-left">Moto</h1><h1 class="logo-right">Bind</h1>
        </div>

        <!-- Навигация -->
        <nav class="sidebar-nav">
            <router-link
                to="/home"
                class="nav-link"
                :class="{ active: $route.path === '/home' }"
                @click="closeSidebar"
            >
                <i class="fa fa-home"></i>
                <span>Главная</span>
            </router-link>
            <router-link
                to="/garage"
                class="nav-link"
                :class="{ active: $route.path === '/garage' }"
                @click="closeSidebar"
            >
                <i class="fa fa-motorcycle"></i>
                <span>Гараж</span>
            </router-link>
            <router-link
                to="/repair"
                class="nav-link"
                :class="{ active: $route.path === '/repair' }"
                @click="closeSidebar"
            >
                <i class="fa fa-wrench"></i>
                <span>Ремонт</span>
            </router-link>
            <router-link
                to="/maintenance"
                class="nav-link"
                :class="{ active: $route.path === '/maintenance' }"
                @click="closeSidebar"
            >
                <i class="fa fa-tools"></i>
                <span>Обслуживание</span>
            </router-link>
            <router-link
                to="/events"
                class="nav-link"
                :class="{ active: $route.path === '/events' }"
                @click="closeSidebar"
            >
                <i class="fa fa-bell"></i>
                <span>События</span>
            </router-link>
            <router-link
                to="/statistics"
                class="nav-link"
                :class="{ active: $route.path === '/statistics' }"
                @click="closeSidebar"
            >
                <i class="fa fa-chart-bar"></i>
                <span>Статистика</span>
            </router-link>
            <router-link
                to="/manuals"
                class="nav-link"
                :class="{ active: $route.path === '/manuals' }"
                @click="closeSidebar"
            >
                <i class="fa fa-book"></i>
                <span>Мануалы</span>
            </router-link>
            <router-link
                to="/settings"
                class="nav-link"
                :class="{ active: $route.path === '/settings' }"
                @click="closeSidebar"
            >
                <i class="fa fa-cog"></i>
                <span>Настройки</span>
            </router-link>

            <!-- Админ-панель (только для админов) -->
            <router-link
                v-if="isAdmin"
                to="/admin"
                class="nav-link admin-link"
                :class="{ active: $route.path === '/admin' }"
                @click="closeSidebar"
            >
                <i class="fa fa-shield"></i>
                <span>Админ-панель</span>
            </router-link>
        </nav>

        <!-- Сообщение premium -->
         <div class="premium-wrapper">
            <div class="premium-icon">
                <i class="fa fa-star"></i>
            </div>
            <div class="premium-body">
                <p class="premium-title">
                    Премиум доступ
                </p>
                <p class="premium-text">
                    Расширенная статистика, напоминания, больше места в гараже и другое.
                </p>
                <button>Подробнее</button>
            </div>
         </div>

        <!-- Нижняя часть сайдбара -->
        <div class="sidebar-footer">
            <!-- Кнопка выхода -->
            <button class="btn-logout-sidebar" @click="logout">
                <i class="fa fa-sign-out"></i>
                <span>Выйти</span>
            </button>
        </div>
    </aside>

    <!-- Основной контент -->
    <div class="main-content" :class="{ 'main-content-shifted': isDesktop }">
        <slot></slot>
    </div>
</template>

<script>
import api from '../api/api';
import { removeTokens } from '../api/auth';
import router from '../router';

export default {
    data() {
        return {
            isSidebarOpen: false,
            isAdmin: false,
            isDesktop: window.innerWidth > 770,
            userName: 'Grisky' // Можно загружать из localStorage
        }
    },

    mounted() {
        this.checkAdminStatus();
        this.handleResize();
        window.addEventListener('resize', this.handleResize);
        
        // Загружаем имя пользователя
        const user = localStorage.getItem('user');
        if (user) {
            try {
                const userData = JSON.parse(user);
                this.userName = userData.name || userData.username || 'Grisky';
            } catch {
                this.userName = 'Grisky';
            }
        }
    },

    beforeUnmount() {
        document.body.style.overflow = '';
        window.removeEventListener('resize', this.handleResize);
    },

    methods: {
        checkAdminStatus() {
            try {
                const token = localStorage.getItem('access_token');
                if (token) {
                    const payload = JSON.parse(atob(token.split('.')[1]));
                    this.isAdmin = payload.role === 'admin';
                } else {
                    this.isAdmin = false;
                }
            } catch {
                this.isAdmin = false;
            }
        },

        toggleSidebar() {
            this.isSidebarOpen = !this.isSidebarOpen;
            document.body.style.overflow = this.isSidebarOpen ? 'hidden' : '';
        },

        closeSidebar() {
            this.isSidebarOpen = false;
            document.body.style.overflow = '';
        },

        handleResize() {
            this.isDesktop = window.innerWidth > 770;
            if (this.isDesktop) {
                this.isSidebarOpen = true;
                document.body.style.overflow = '';
            } else {
                this.isSidebarOpen = false;
                document.body.style.overflow = '';
            }
        },

        async logout() {
            try {
                await api.post('/auth/logout');
            } catch(err) {
                console.error('Logout failed:', err);
            } finally {
                removeTokens();
                this.closeSidebar();
                router.push('/login');
            }
        }
    },

    watch: {
        '$route'() {
            this.closeSidebar();
            this.checkAdminStatus();
        }
    }
}
</script>

<style scoped>
/* ===== Кнопка-гамбургер ===== */
.sidebar-toggle {
    position: fixed;
    top: 20px;
    left: 320px;
    z-index: 1001;
    display: none;
    flex-direction: column;
    justify-content: space-between;
    width: 30px;
    height: 21px;
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 0;
}

.sidebar-toggle .burger-line {
    width: 100%;
    height: 3px;
    background-color: var(--text-primary, #333);
    border-radius: 3px;
    transition: all 0.3s ease;
}

.sidebar-toggle.active .burger-line:nth-child(1) {
    transform: translateY(9px) rotate(45deg);
}

.sidebar-toggle.active .burger-line:nth-child(2) {
    opacity: 0;
}

.sidebar-toggle.active .burger-line:nth-child(3) {
    transform: translateY(-9px) rotate(-45deg);
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
    padding: 24px 20px;
    transition: transform 0.3s ease;
    box-shadow: 4px 0 20px rgba(0, 0, 0, 0.3);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    transform: translateX(0);
}

/* На мобильных сайдбар скрыт по умолчанию */
@media (max-width: 770px) {
    .sidebar {
        transform: translateX(-100%);
    }

    .sidebar.sidebar-open {
        transform: translateX(0);
    }

    .sidebar-toggle {
        display: flex;
    }
}

/* ===== Логотип ===== */
.sidebar-logo {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    margin-bottom: 16px;
}

.sidebar-logo h1 {
    font-size: 24px;
    font-weight: 700;
    margin: 0;
    color: var(--text-primary, #fff);
}

.logo-left {
    color: var(--text-primary);
}

.logo-right {
    color: var(--accent) !important;
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
}

.nav-link i {
    width: 20px;
    font-size: 16px;
    text-align: center;
    color: var(--text-secondary);
    transition: color 0.2s ease;
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

/* === ПРЕМИУМ СООБЩЕНИЕ === */
.premium-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 12px;
    background-color: var(--bg-secondary);
    border: 2px solid var(--border-color);
    border-radius: 20px;
    font-size: 14px;

    text-align: center;
}

.premium-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--accent);
    min-height: 48px;
    min-width: 48px;
    text-align: center;
    border-radius: 12px;
    margin-bottom: 12px;
}

.premium-title {
    font-weight: 600;
    margin-bottom: 8px;
}

.premium-text {
    color: var(--text-muted);
}

.premium-wrapper button {
    width: 100%;
    font-weight: 600;
}

/* Админ-ссылка */
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

/* ===== Нижняя часть сайдбара ===== */
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
    border-radius: 10px;
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
}

/* ===== Основной контент ===== */
.main-content {
    transition: margin-left 0.3s ease;
    min-height: 100vh;
}

/* На десктопе добавляем отступ для сайдбара */
@media (min-width: 771px) {
    .main-content {
        margin-left: 260px;
        padding: 20px 30px;
    }
}

/* На мобильных отступа нет */
@media (max-width: 770px) {
    .main-content {
        margin-left: 0;
        padding: 80px 16px 20px;
    }
}

/* Для очень маленьких экранов */
@media (max-width: 480px) {
    .sidebar {
        width: 85%;
        max-width: 280px;
    }
}

/* Оверлей показываем только на мобильных */
@media (min-width: 771px) {
    .sidebar-overlay {
        display: none;
    }
}

/* Стилизация скролла */
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