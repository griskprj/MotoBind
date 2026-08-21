<template>
  <div class="verify-container">
    <div class="verify-card">
      <div v-if="status === 'loading'" class="status-loading">
        <div class="spinner"></div>
        <h2>Подтверждение email...</h2>
        <p>Пожалуйста, подождите</p>
      </div>

      <div v-else-if="status === 'success'" class="status-success">
        <div class="icon success">
          <i class="fa fa-check-circle"></i>
        </div>
        <h2>Email подтверждён! 🎉</h2>
        <p>Добро пожаловать в MotoBind!</p>
        <button class="btn btn-primary" @click="goToApp">Перейти в приложение</button>
      </div>

      <div v-else-if="status === 'error'" class="status-error">
        <div class="icon error">
          <i class="fa fa-exclamation-circle"></i>
        </div>
        <h2>Ошибка подтверждения</h2>
        <p>{{ errorMessage }}</p>
        <button class="btn btn-outline" @click="resend">Отправить повторно</button>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../api/api'
import { setTokens, setUser } from '../../api/auth'

export default {
  name: 'VerifyEmail',
  data() {
    return {
      status: 'loading', // loading | success | error
      errorMessage: '',
      token: null
    }
  },
  methods: {
    async verify() {
      this.token = this.$route.params.token
      
      if (!this.token) {
        this.status = 'error'
        this.errorMessage = 'Неверная ссылка подтверждения.'
        return
      }
      
      try {
        const response = await api.get(`/auth/verify-email/${this.token}`)
        const { access_token, refresh_token, user } = response.data
        
        // Сохраняем токены
        setTokens(access_token, refresh_token)
        setUser(user)
        
        this.status = 'success'
      } catch (err) {
        this.status = 'error'
        this.errorMessage = err.response?.data?.error || 'Ссылка недействительна или истекла.'
      }
    },
    async resend() {
      try {
        await api.post('/auth/resend-verification')
        alert('Письмо отправлено повторно! Проверьте почту.')
      } catch (err) {
        alert('Ошибка отправки. Попробуйте позже.')
      }
    },
    goToApp() {
      this.$router.push('/garage')
    }
  },
  mounted() {
    this.verify()
  }
}
</script>

<style scoped>
.verify-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0A0A0F;
  padding: 20px;
}

.verify-card {
  max-width: 420px;
  width: 100%;
  background: #181824;
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 16px;
  padding: 48px 32px;
  text-align: center;
}

.icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.icon.success {
  color: #4ade80;
}

.icon.error {
  color: #ef4444;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #2d2d3d;
  border-top: 4px solid #8B5CF6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.verify-card h2 {
  font-size: 24px;
  margin: 0 0 8px 0;
}

.verify-card p {
  color: #8b8b9e;
  margin: 0 0 24px 0;
  line-height: 1.6;
}

.btn {
  padding: 12px 32px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn-primary {
  background: #8B5CF6;
  color: #fff;
}

.btn-primary:hover {
  background: #7C3AED;
}

.btn-outline {
  background: transparent;
  border: 2px solid #2d2d3d;
  color: #8b8b9e;
}

.btn-outline:hover {
  border-color: #8B5CF6;
  color: #8B5CF6;
}
</style>