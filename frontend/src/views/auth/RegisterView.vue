<script>
import api from '../../api/api'

export default {
    data() {
        return {
            email: '',
            username: '',
            password: '',
            role: 'motorcyclist',
            error: null,
            isDark: true
        }
    },

    methods: {
        async register() {
        this.error = null
        try {
            await api.post('/auth/register', {
                email: this.email,
                username: this.username,
                password: this.password,
                role: this.role
            })
            this.$router.push('/login?registered=true')
        } catch (err) {
            this.error = err.response?.data?.error || 'Ошибка регистрации'
        }
        }
    }
}
</script>

<template>
    <div class="container">
        <div class="auth-card">
        <div class="auth-header">
            <i class="fa fa-motorcycle"></i>
            <h1>MotoBind - Регистрация</h1>
        </div>
        <form @submit.prevent="register">
            <div class="inputs">
                <div class="form-group">
                    <label>
                        Email
                        <input v-model="email" type="email" placeholder="motorcycle@moto.com" required>
                    </label>
                </div>
                <div class="form-group">
                    <label>
                        Имя пользователя
                        <input v-model="username" type="text" placeholder="Motobat" required>
                    </label>
                </div>
                <div class="form-group">
                    <label>
                        Пароль
                        <input v-model="password" type="password" placeholder="Минимум 6 символов" required>
                    </label>
                </div>
                <div class="form-group">
                    <label>
                        Роль
                        <select v-model="role">
                            <option value="motorcyclist">Мотоциклист</option>
                            <option value="motoclub">Мотоклуб</option>
                        </select>
                    </label>
                </div>
            </div>
            <button class="submit-btn" type="submit">Зарегистрироваться</button>
        </form>
        <div v-if="error" class="error">{{ error }}</div>
            <p>
                Уже есть аккаунт?
                <router-link to="/login">Войти</router-link>
            </p>
        </div>
    </div>
</template>

<style scoped>
i {
    font-size: 64px;
    color: var(--accent);
    margin-bottom: 16px;
}

h1 {
    margin-bottom: 24px;
}

label {
    text-align: left;
}

form {
    margin-bottom: 24px;
}

.inputs {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.submit-btn {
    width: 100%;
    margin-top: 24px;
}

.container {
    max-width: 500px;
    margin: 0 auto;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;

    text-align: center;

    animation: slideInUp 0.5s ease-out forwards;
}

.auth-card {
    display: flex;
    flex-direction: column;
    gap: 24px;
    background-color: var(--bg-card);
    padding: 25px;
    border-radius: 25px;
    width: 100%;

    -webkit-box-shadow:var(--shadow-md);
    -moz-box-shadow: var(--shadow-md);
    box-shadow: var(--shadow-md);

    transition: all, 0.3s;
}

.auth-card:hover {
    transform: translateY(-2px);
}

.error {
    color: #d32f2f;
    margin-top: 10px;
}

@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(5%);
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}
</style>