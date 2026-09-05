<template>
    <!-- === WELCOME SECTION === -->
    <header class="page-header">
        <div class="header-left">
            <h2>{{ title }}</h2>
            <p class="header-subtitle">{{ subtitle }}</p>
        </div>

        <div class="header-right">
            <NotificationBell />
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

    components: { NotificationBell },

    data() {
        return {
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

/* ===== КНОПКА ПЕРЕКЛЮЧЕНИЯ ТЕМЫ ===== */
.theme-toggle {
    min-width: 40px;
    min-height: 40px;
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
    transform: translateY(0px);
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
}


.theme-toggle i {
    transition: transform 0.3s ease;
}

/* ===== АДАПТИВНОСТЬ ===== */
@media(max-width: 720px) {
    .header-right {
        display: flex;
        gap: 12px;
    }
}
</style>