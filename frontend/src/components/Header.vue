<template>
    <header>
        <div class="logo">
            <h1 class="logo-left">Moto</h1><h1 class="logo-right">Bind</h1>
        </div>

        <!-- Бургер-кнопка -->
        <button class="burger-btn" @click="toggleMenu" :class="{ active: isMenuOpen }">
            <span class="burger-line"></span>
            <span class="burger-line"></span>
            <span class="burger-line"></span>
        </button>

        <!-- Навигация (адаптивная) -->
        <nav class="header-nav" :class="{ 'nav-open': isMenuOpen }">
            <router-link
                to="/home"
                class="nav-link"
                :class="{ active: $route.path === '/home'}"
                @click="closeMenu"
            >
                <i class="fa fa-home"></i>
                <span>Главная</span>
            </router-link>
            <router-link
                to="/garage"
                class="nav-link"
                :class="{ active: $route.path === '/garage'}"
                @click="closeMenu"
            >
                <i class="fa fa-motorcycle"></i>
                <span>Гараж</span>
            </router-link>
            <router-link
                to="/repair"
                class="nav-link"
                :class="{ active: $route.path === '/repair'}"
                @click="closeMenu"
            >
                <i class="fa fa-wrench"></i>
                <span>Ремонт</span>
            </router-link>
            <router-link
                to="/events"
                class="nav-link"
                :class="{ active: $route.path === '/events'}"
                @click="closeMenu"
            >
                <i class="fa fa-bell"></i>
                <span>События</span>
            </router-link>

            <!-- Кнопки в мобильном меню -->
            <div class="profile-mobile">.
                <router-link
                    v-if="isAdmin"
                    to="/admin"
                    class="nav-link admin-link-desktop"
                    :class="{ active: $route.path === '/admin'}"
                >
                    <i class="fa fa-shield"></i>
                    <span>Админ-панель</span>
                </router-link>
                <router-link
                    to="/profile"
                    class="nav-link"
                    :class="{ active: $route.path === '/profile' }"
                >
                    <img src="/BaseAvatar.jpg" alt="avatar" class="profile-img">
                </router-link>
            </div>
            <button class="btn-logout-mobile" @click="logout">
                <i class="fa fa-sign-out"></i>
                <span>Выйти</span>
            </button>
        </nav>

        <div class="header-actions">
            <div class="profile">
                <router-link
                    to="/profile"
                    class="nav-link"
                    :class="{ active: $route.path === '/profile' }"
                >
                    <img src="/BaseAvatar.jpg" alt="avatar" class="profile-img">
                </router-link>
            </div>
            <!-- Кнопка админ-панели в десктопе (только для админов) -->
            <router-link
                v-if="isAdmin"
                to="/admin"
                class="nav-link admin-link-desktop"
                :class="{ active: $route.path === '/admin'}"
            >
                <i class="fa fa-shield"></i>
                <span>Админ-панель</span>
            </router-link>
            <div class="logout-wrapper">
                <button class="btn btn-logout" @click="logout">
                    <i class="fa fa-sign-out"></i>
                    <span>Выйти</span>
                </button>
            </div>
        </div>

        <!-- Оверлей для закрытия меню -->
        <div class="menu-overlay" v-if="isMenuOpen" @click="closeMenu"></div>
    </header>
</template>

<script>
import api from '../api/api';
import { removeTokens } from '../api/auth';
import router from '../router';

export default {
    data() {
        return {
            isMenuOpen: false,
            isAdmin: false
        }
    },

    mounted() {
        this.checkAdminStatus();
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

        toggleMenu() {
            this.isMenuOpen = !this.isMenuOpen;
            if (this.isMenuOpen) {
                document.body.style.overflow = 'hidden';
            } else {
                document.body.style.overflow = '';
            }
        },

        closeMenu() {
            this.isMenuOpen = false;
            document.body.style.overflow = '';
        },

        async logout() {
            try {
                await api.post('/auth/logout');
            } catch(err) {
                console.error('Logout failed:', err);
            } finally {
                removeTokens();
                this.closeMenu();
                router.push('/login');
            }
        }
    },

    watch: {
        '$route'() {
            this.closeMenu();
            // Обновляем статус админа при смене маршрута
            this.checkAdminStatus();
        }
    },

    beforeUnmount() {
        document.body.style.overflow = '';
    }
}
</script>

<style scoped>
header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;

    padding: 24px;
    margin-bottom: 48px;
    
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 0px;
    border: 1px solid rgba(255, 255, 255, 0);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
    
    position: relative;
    z-index: 1000;
}

.logo {
    display: flex;
    flex-direction: row;
    z-index: 1000;
}

.logo-right {
    color: var(--accent);
}

/* Бургер-кнопка */
.burger-btn {
    display: none;
    flex-direction: column;
    justify-content: space-between;
    width: 30px;
    height: 21px;
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 0;
    z-index: 1001;
}

.burger-line {
    width: 100%;
    height: 3px;
    background-color: var(--text-primary);
    border-radius: 3px;
    transition: all 0.3s ease;
}

.burger-btn.active .burger-line:nth-child(1) {
    transform: translateY(9px) rotate(45deg);
}

.burger-btn.active .burger-line:nth-child(2) {
    opacity: 0;
}

.burger-btn.active .burger-line:nth-child(3) {
    transform: translateY(-9px) rotate(-45deg);
}

/* Десктопная навигация */
.header-nav {
    display: flex;
    flex-direction: row;
    gap: 32px;
    padding: 8px;
}

.nav-link {
    font-size: 18px;
    color: var(--text-primary);
    transition: all 0.3s ease;
    white-space: nowrap;
}

.nav-link.active {
    color: var(--accent);
}

.nav-link i {
    margin-right: 8px;
}

.nav-link:hover {
    transform: translateY(-5px);
    color: var(--accent);
    text-decoration: none;
}

/* Стиль для ссылки на админ-панель */
.admin-link {
    color: var(--warning);
    border-left: 2px solid var(--border-color);
    padding-left: 16px;
}

.admin-link:hover {
    color: var(--warning);
}

.admin-link.active {
    color: var(--warning);
}

.admin-link-desktop {
    font-size: 16px;
    color: var(--warning);
    transition: all 0.3s ease;
    white-space: nowrap;
    padding: 6px 12px;
    border-radius: 8px;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

.admin-link-desktop:hover {
    transform: translateY(-2px);
    color: var(--warning);
    text-decoration: none;
    background: rgba(245, 158, 11, 0.1);
    border-color: var(--warning);
}

.admin-link-desktop.active {
    color: var(--warning);
    background: rgba(245, 158, 11, 0.15);
    border-color: var(--warning);
}

.admin-link-desktop i {
    margin-right: 6px;
}

.header-actions {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 18px;
    z-index: 1001;
}

.profile-img {
    border-radius: 50%;
    overflow: hidden;
    border: 2px solid var(--accent);

    max-width: 40px;
    max-height: 40px;
}

.profile-mobile {
    display: none;
}

.btn-logout {
    white-space: nowrap;
}

.btn-logout-mobile {
    display: none;
}

.menu-overlay {
    display: none;
}

/* ===== АДАПТИВ ДЛЯ ТЕЛЕФОНОВ ===== */
@media (max-width: 1024px) {
    .admin-link-desktop {
        display: none;
    }
}

@media (max-width: 770px) {
    header {
        justify-content: space-between;
    }

    /* Показываем бургер */
    .burger-btn {
        display: flex;
    }

    /* Скрываем десктопные элементы */
    .header-actions {
        display: none;
    }

    /* Мобильное меню */
    .header-nav {
        position: fixed;
        top: 0;
        right: -100%;
        width: 80%;
        max-width: 300px;
        height: 100vh;
        background: var(--bg-primary);
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 32px;
        transition: right 0.3s ease;
        z-index: 1000;
        box-shadow: -5px 0 20px rgba(0, 0, 0, 0.3);
        margin: 0;
        padding: 80px 20px;
    }

    .header-nav.nav-open {
        right: 0;
    }

    .nav-link {
        font-size: 20px;
        padding: 12px;
        width: 100%;
        text-align: center;
    }

    .admin-link {
        border-left: none;
        padding-left: 0;
        border-top: 1px solid var(--border-color);
        padding-top: 16px;
        margin-top: 0;
    }

    .profile-mobile {
        display: block;
    }

    /* Мобильная кнопка выхода */
    .btn-logout-mobile {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        background: var(--accent);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        font-size: 18px;
        cursor: pointer;
        width: 100%;
        margin-top: 20px;
        transition: all 0.3s ease;
    }

    .btn-logout-mobile:hover {
        transform: translateY(-2px);
        filter: brightness(0.9);
    }

    /* Оверлей */
    .menu-overlay {
        display: block;
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
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
}

/* Для очень маленьких экранов */
@media (max-width: 480px) {
    .header-nav {
        width: 85%;
    }
    
    .nav-link {
        font-size: 18px;
    }
}
</style>