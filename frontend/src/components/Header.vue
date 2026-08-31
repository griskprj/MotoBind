<template>
    <!-- === WELCOME SECTION === -->
    <header class="page-header">
        <div class="header-left">
            <h2>{{ title }}</h2>
            <p class="header-subtitle">{{ subtitle }}</p>
        </div>

        <div class="header-right">
            <NotificationBell/>
            <button 
                class="theme-toggle" 
                @click="toggleTheme"
                :title="isDark ? 'Включить светлую тему' : 'Включить темную тему'"
            >
                <i :class="isDark ? 'fa fa-sun' : 'fa fa-moon'"></i>
            </button>
        </div>
    </header>
</template>

<script>
import NotificationBell from './NotificationBell.vue';

export default {
    name: 'Header',

    components: {NotificationBell},

    data() {
        return {
            welcomeDropdownActive: false,
            isDark: true
        }
    },

    props: {
        title: {
            type: String,
            default: '',
            required: true
        },

        subtitle: {
            type: String,
            default: '',
            required: true
        }
    },

    mounted() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            this.isDark = savedTheme === 'dark';
            document.documentElement.setAttribute('data-theme', savedTheme);
        } else {
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            this.isDark = prefersDark;
            document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
        }
    },

    methods: {
        toggleTheme() {
            this.isDark = !this.isDark;
            const theme = this.isDark ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            
            // Обновляем иконку солнца/луны на кнопке
            const icon = this.$el.querySelector('.theme-toggle i');
            if (icon) {
                icon.className = this.isDark ? 'fa fa-sun' : 'fa fa-moon';
            }
        },
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
    padding: 10px 12px;
    font-size: 20px;
    color: var(--text-muted);
    cursor: pointer;
    background-color: var(--bg-primary);
    border-radius: 10px;
    transition: all 0.3s ease;
}

.notification-icon:hover {
    background-color: var(--border-color);
    color: var(--accent);
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

/* ===== КНОПКА ПЕРЕКЛЮЧЕНИЯ ТЕМЫ ===== */
.theme-toggle {
    width: 40px;
    height: 40px;
    padding: 0;
    background: var(--bg-primary);
    border: 2px solid var(--border-color);
    border-radius: 50%;
    color: var(--text-primary);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    transition: all 0.3s ease;
}

.theme-toggle:hover {
    background: var(--accent);
    border-color: var(--accent);
    color: white;
    transform: rotate(30deg);
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
}

.theme-toggle:active {
    transform: rotate(60deg) scale(0.9);
}

.theme-toggle i {
    transition: transform 0.3s ease;
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

@media(max-width: 720px) {
    .header-right {
        display: none;
    }
}

/* === ANIMATIONS === */
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
</style>
