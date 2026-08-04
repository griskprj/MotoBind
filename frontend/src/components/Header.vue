<template>
    <!-- === WELCOME SECTION === -->
    <header class="page-header">
        <div class="header-left">
            <h2>{{ title }}</h2>
            <p class="header-subtitle">{{ subtitle }}</p>
        </div>

        <div class="header-right">
                <i class="fa fa-bell notification-icon"></i>
                <div class="profile-wrapper">
                    <img src="/BaseAvatar.jpg" alt="avatar" class="profile-img">
                    <button class="dropdown-trigger" @click="welcomeDropdownActive = !welcomeDropdownActive">
                        <i class="fa" :class="welcomeDropdownActive ? 'fa-angle-up' : 'fa-angle-down'"></i>
                    </button>
                    <div v-if="welcomeDropdownActive" class="dropdown-list">
                        <ul>
                            <li><button @click="this.$router.push('/profile')" class="dropdown-item">Профиль</button></li>
                            <li><button @click="logout" class="dropdown-item">Выйти</button></li>
                        </ul>
                    </div>
                </div>
            </div>
    </header>
</template>

<script>
export default {
    name: 'Header',

    data() {
        return {
            welcomeDropdownActive: false
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