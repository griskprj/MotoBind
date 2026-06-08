<template>
    <header>
        <div class="logo">
            <h1>MotoBind</h1>
        </div>

        <nav class="header-nav">
            <router-link
                to="/"
                class="nav-link"
                :class="{ active: $route.path === '/'}"
            >
                <i class="fa fa-home"></i>
                <span>Главная</span>
            </router-link>
            <router-link
                to="/garage"
                class="nav-link"
                :class="{ active: $route.path === '/garage'}"
            >
                <i class="fa fa-motorcycle"></i>
                <span>Гараж</span>
            </router-link>
            <router-link
                to="/manuals"
                class="nav-link"
                :class="{ active: $route.path === '/manuals'}"
            >
                <i class="fa fa-wrench"></i>
                <span>Ремонт</span>
            </router-link>
            <router-link
                to="/events"
                class="nav-link"
                :class="{ active: $route.path === '/events'}"
            >
                <i class="fa fa-bell"></i>
                <span>События</span>
            </router-link>
        </nav>

        <div class="header-actions">
            <button class="btn btn-logout" @click="logout">
                <i class="fa fa-sign-out"></i>
                <span>Выйти</span>
            </button>
        </div>
    </header>
</template>

<script>
import api from '../api/api';
import { removeTokens } from '../api/auth';
import router from '../router';

export default {
    methods: {
        async logout() {
            try {
                api.post('/auth/logout')
            } catch(err) {
                console.error('Logout failed:', err)
            } finally {
                removeTokens()
                this.router.push('/login')
            }
        }
    }
}
</script>

<style scoped>
header {
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;

    padding: 24px;
    margin-bottom: 48px;
    
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 0px;
    border: 1px solid rgba(255, 255, 255, 0);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
}

.logo h1 {
    color: var(--accent)
}

.header-nav {
    display: flex;
    flex-direction: row;
    gap: 32px;

    padding: 8px;
}
.nav-link {
    font-size: 18px;
    color: var(--text-primary);

    transition: all, 0.3s;
}
.nav-link .active {
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
</style>