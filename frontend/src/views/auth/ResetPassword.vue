<template>
  <div class="auth-container">
    <div class="auth-card">
      <div v-if="valid" class="auth-header">
        <h1>Новый пароль</h1>
        <p>Введите новый пароль для {{ email }}</p>
      </div>

      <div v-else-if="checking" class="auth-header">
        <h1>Проверка...</h1>
        <p>Пожалуйста, подождите</p>
      </div>

      <div v-else class="auth-header">
        <h1>Ошибка</h1>
        <p>{{ errorMessage }}</p>
        <router-link to="/forgot-password" class="btn btn-primary" style="display: block; text-align: center; text-decoration: none; margin-top: 16px;">
          Запросить сброс
        </router-link>
      </div>

      <form v-if="valid" @submit.prevent="submit">
        <div class="form-group">
          <label for="password">Новый пароль</label>
          <input
            id="password"
            v-model="newPassword"
            type="password"
            placeholder="Минимум 6 символов"
            required
          />
        </div>

        <div class="form-group">
          <label for="confirm">Подтвердите пароль</label>
          <input
            id="confirm"
            v-model="confirmPassword"
            type="password"
            placeholder="Повторите пароль"
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
          {{ loading ? 'Сохранение...' : 'Сохранить пароль' }}
        </button>
      </form>
    </div>
  </div>
</template>

<head>
  <title>MotoBind — Сброс пароля</title>
  <meta name="description" content="Установите новый пароль для своего аккаунта в MotoBind.">
</head>

<script>
import api from '../../api/api'
import { setTokens, setUser } from '../../api/auth'

export default {
  name: 'ResetPassword',
  data() {
    return {
      token: null,
      email: '',
      valid: false,
      checking: true,
      errorMessage: '',
      newPassword: '',
      confirmPassword: '',
      loading: false,
      error: null,
      success: null
    }
  },
  methods: {
    async checkToken() {
      this.token = this.$route.params.token
      
      if (!this.token) {
        this.valid = false
        this.checking = false
        this.errorMessage = 'Неверная ссылка сброса.'
        return
      }
      
      try {
        const response = await api.get(`/auth/check-reset-token/${this.token}`)
        this.email = response.data.email
        this.valid = true
      } catch (err) {
        this.valid = false
        this.errorMessage = err.response?.data?.error || 'Ссылка недействительна или истекла.'
      } finally {
        this.checking = false
      }
    },
    async submit() {
      this.error = null
      this.success = null
      
      if (this.newPassword.length < 6) {
        this.error = 'Пароль должен быть минимум 6 символов'
        return
      }
      
      if (this.newPassword !== this.confirmPassword) {
        this.error = 'Пароли не совпадают'
        return
      }
      
      this.loading = true
      
      try {
        const response = await api.post('/auth/reset-password', {
          token: this.token,
          new_password: this.newPassword
        })
        
        // Автоматически логиним пользователя
        if (response.data.access_token) {
          setTokens(response.data.access_token, response.data.refresh_token)
          setUser(response.data.user)
          this.$router.push('/garage')
        } else {
          this.success = 'Пароль успешно изменён!'
          setTimeout(() => {
            this.$router.push('/login')
          }, 3000)
        }
      } catch (err) {
        this.error = err.response?.data?.error || 'Ошибка смены пароля'
      } finally {
        this.loading = false
      }
    }
  },
  mounted() {
    this.checkToken()
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