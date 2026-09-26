<template>
  <LoadingOverlay :is-loading="loading" text="Вход..."/>
  <div class="login-container">
    <div class="login-card animate-slide-in">
      <div class="left-side"></div>
      <div class="image-overlay"></div>

      <div class="right-side">
        <div class="login-header">
          <i class="fa fa-motorcycle"></i>
          <h1 class="login-title">Вход в MotoBind</h1>
          <p class="login-subtitle">Войдите в свой аккаунт, чтобы продолжить</p>
        </div>

        <form @submit.prevent="login" class="login-form">
          <div class="form-group">
            <label for="email">
              <i class="fa fa-envelope"></i> Email
            </label>
            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="motorcycle@moto.com"
              required
              autocomplete="email"
            />
          </div>

          <div class="form-group">
            <label for="password">
              <i class="fa fa-lock"></i> Пароль
            </label>
            <input
              id="password"
              v-model="password"
              type="password"
              placeholder="Введите пароль"
              required
              autocomplete="current-password"
            />
          </div>

          <div class="form-options">
            <div class="checkbox-group">
              <input v-model="rememberMe" type="checkbox" id="remember" />
              <label for="remember" class="checkbox-label">Запомнить меня</label>
            </div>
            <router-link to="/forgot-password" class="forgot-link">
              Забыли пароль?
            </router-link>
          </div>

          <BaseButton
            type="submit"
            variant="primary"
            block
            icon="fa fa-sign-in-alt"
          >
            Войти
          </BaseButton>
        </form>

        <div v-if="error" class="error-message">
          <i class="fa fa-exclamation-circle"></i> {{ error }}
        </div>

        <div v-if="$route.query.registered" class="success-message">
          <i class="fa fa-check-circle"></i> Регистрация успешна! Теперь войдите.
        </div>

        <div class="register-link">
          <span>Нет аккаунта?</span>
          <router-link to="/register" class="register-btn">
            Зарегистрироваться
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import LoadingOverlay from '@/components/LoadingOverlay.vue'
import { BaseButton } from '@/components/ui'
import { useAuthStore } from '@/stores'
import api from '@/api/api'

const router = useRouter()
const auth = useAuthStore()

const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const error = ref(null)
const loading = ref(false)

async function login() {
  error.value = null
  loading.value = true
  try {
    const response = await api.post('/auth/login', {
      email: email.value,
      password: password.value,
      rememberMe: rememberMe.value,
    })
    const { access_token, refresh_token } = response.data
    auth.setTokens(access_token, refresh_token)
    auth.setUser(response.data.user)

    const role = response.data.user.role
    if (role === 'admin') {
      router.push('/admin/panel')
    } else {
      router.push('/garage')
    }
  } catch (err) {
    error.value = err.response?.data?.error || 'Ошибка входа. Проверьте email и пароль.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.login-card {
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 1100px;
  width: 100%;
  border-radius: var(--radius);
  overflow: hidden;
  background-color: var(--bg-card);
  box-shadow: var(--shadow-lg);
  position: relative;
  min-height: 600px;
}

.animate-slide-in {
  animation: slideInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
  transform: translateY(30px);
}

.left-side {
  position: relative;
  min-height: 400px;
  background-image: url('/16x9Auth-Bg.webp');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 50%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.right-side {
  padding: 48px 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background-color: var(--bg-card);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-header i {
  font-size: 48px;
  color: var(--accent);
  margin-bottom: 12px;
}

.login-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0 0 8px 0;
  color: var(--text-primary);
}

.login-subtitle {
  color: var(--text-muted);
  font-size: 0.95rem;
  margin: 0;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 6px;
}

.form-group label i {
  font-size: 14px;
  color: var(--accent);
  margin: 0;
}

.form-group input {
  padding: 0.75rem 1rem;
  border-radius: 10px;
  border: 2px solid var(--border-color);
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 0.95rem;
  transition: all 0.3s;
}

.form-group input:focus {
  border-color: var(--accent);
  box-shadow: var(--shadow-focus);
  outline: none;
}

.form-group input::placeholder {
  color: var(--text-muted);
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 4px 0 8px 0;
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.checkbox-group input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: var(--accent);
  cursor: pointer;
}

.checkbox-label {
  font-size: 0.875rem;
  font-weight: 400;
  color: var(--text-secondary);
  cursor: pointer;
  margin: 0;
}

.forgot-link {
  font-size: 0.875rem;
  color: var(--accent);
  text-decoration: none;
  transition: color 0.2s;
}

.forgot-link:hover {
  color: var(--accent-hover);
  text-decoration: underline;
}

.error-message {
  margin-top: 16px;
  padding: 12px 16px;
  background-color: var(--danger-trans);
  border: 1px solid var(--danger);
  border-radius: 10px;
  color: var(--danger-text);
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.success-message {
  margin-top: 16px;
  padding: 12px 16px;
  background-color: var(--success-trans);
  border: 1px solid var(--success);
  border-radius: 10px;
  color: var(--success-text);
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.register-link {
  margin-top: 24px;
  text-align: center;
  font-size: 0.95rem;
  color: var(--text-secondary);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
}

.register-btn {
  color: var(--accent);
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.register-btn:hover {
  color: var(--accent-hover);
  text-decoration: underline;
}

@media (max-width: 820px) {
  .login-container {
    padding: 0;
    align-items: stretch;
  }

  .login-card {
    grid-template-columns: 1fr;
    max-width: 100%;
    border-radius: 0;
    min-height: 100vh;
    box-shadow: none;
  }

  .left-side {
    position: absolute;
    inset: 0;
    min-height: unset;
    background-image: url('/9x16Auth-Bg.webp');
    background-size: cover;
    background-position: center;
    z-index: 0;
  }

  .image-overlay {
    width: 100%;
    height: 100%;
    z-index: 1;
  }

  .right-side {
    position: relative;
    z-index: 2;
    background: rgba(10, 10, 15, 0.75);
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    padding: 32px 24px;
    margin: 16px;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.06);
    min-height: auto;
    max-height: 90vh;
    overflow-y: auto;
  }

  .login-header i {
    font-size: 40px;
  }

  .login-title {
    font-size: 1.6rem;
  }
}

@media (max-width: 480px) {
  .right-side {
    padding: 24px 16px;
    margin: 12px;
  }

  .login-title {
    font-size: 1.4rem;
  }

  .form-options {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
}
</style>
