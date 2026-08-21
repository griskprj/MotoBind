<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h1>Забыли пароль?</h1>
        <p>Введите email, и мы отправим ссылку для сброса</p>
      </div>

      <form @submit.prevent="submit">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="motorcycle@moto.com"
            required
          />
        </div>

        <div v-if="error" class="error-message">
          <i class="fa fa-exclamation-circle"></i> {{ error }}
        </div>

        <div v-if="success" class="success-message">
          <i class="fa fa-check-circle"></i> {{ success }}
        </div>

        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Отправка...' : 'Отправить' }}
        </button>

        <div class="auth-links">
          <router-link to="/login">Вспомнил пароль? Войти</router-link>
          <router-link to="/register">Нет аккаунта? Зарегистрироваться</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import api from '../../api/api'

export default {
  name: 'ForgotPassword',
  data() {
    return {
      email: '',
      loading: false,
      error: null,
      success: null
    }
  },
  methods: {
    async submit() {
      this.error = null
      this.success = null
      this.loading = true

      try {
        await api.post('/auth/forgot-password', { email: this.email })
        this.success = 'Письмо отправлено! Проверьте почту.'
        this.email = ''
      } catch (err) {
        this.error = err.response?.data?.error || 'Ошибка отправки. Попробуйте позже.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0A0A0F;
  padding: 20px;
}

.auth-card {
  max-width: 400px;
  width: 100%;
  background: #181824;
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 16px;
  padding: 40px 32px;
}

.auth-header {
  text-align: center;
  margin-bottom: 32px;
}

.auth-header h1 {
  font-size: 28px;
  margin: 0 0 8px 0;
}

.auth-header p {
  color: #8b8b9e;
  margin: 0;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-weight: 600;
  font-size: 14px;
  color: #8b8b9e;
  margin-bottom: 4px;
}

.form-group input {
  width: 100%;
  padding: 12px 16px;
  background: #0f0f1a;
  border: 2px solid #2d2d3d;
  border-radius: 10px;
  color: #fff;
  font-size: 16px;
  transition: border 0.2s;
}

.form-group input:focus {
  border-color: #8B5CF6;
  outline: none;
}

.btn {
  width: 100%;
  padding: 12px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
  font-size: 16px;
}

.btn-primary {
  background: #8B5CF6;
  color: #fff;
}

.btn-primary:hover {
  background: #7C3AED;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-message {
  padding: 10px 14px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid #ef4444;
  border-radius: 8px;
  color: #ef4444;
  font-size: 14px;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.success-message {
  padding: 10px 14px;
  background: rgba(74, 222, 128, 0.1);
  border: 1px solid #4ade80;
  border-radius: 8px;
  color: #4ade80;
  font-size: 14px;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.auth-links {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 20px;
  text-align: center;
}

.auth-links a {
  color: #8b8b9e;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.2s;
}

.auth-links a:hover {
  color: #8B5CF6;
}
</style>