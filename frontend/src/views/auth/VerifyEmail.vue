<template>
  <div class="verify-container">
    <div class="verify-card">
      <div class="icon" :class="status">
        <i :class="iconClass"></i>
      </div>
      <h2>{{ title }}</h2>
      <p>{{ message }}</p>
      <button v-if="status === 'success'" class="btn btn-primary" @click="goToApp">
        Войти в приложение
      </button>
      <button v-else class="btn btn-outline" @click="resend">
        Отправить повторно
      </button>
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
      title: 'Подтверждение email...',
      message: 'Пожалуйста, подождите...',
      token: null
    }
  },
  computed: {
    iconClass() {
      return {
        'loading': 'fa fa-spinner fa-spin',
        'success': 'fa fa-check-circle',
        'error': 'fa fa-exclamation-circle'
      }[this.status]
    }
  },
  methods: {
    async verify() {
      this.token = this.$route.params.token
      
      if (!this.token) {
        this.status = 'error'
        this.title = 'Ошибка'
        this.message = 'Неверная ссылка подтверждения.'
        return
      }
      
      try {
        const response = await api.get(`/auth/verify-email/${this.token}`)
        const { access_token, refresh_token, user } = response.data
        
        setTokens(access_token, refresh_token)
        setUser(user)
        
        this.status = 'success'
        this.title = 'Email подтвержден!'
        this.message = 'Добро пожаловать в MotoBind!'
      } catch (err) {
        this.status = 'error'
        this.title = 'Ошибка подтверждения'
        this.message = err.response?.data?.error || 'Ссылка недействительна или истекла.'
      }
    },
    async resend() {
      try {
        await api.post('/auth/resend-verification')
        alert('Письмо отправлено повторно!')
      } catch (err) {
        alert('Ошибка отправки письма. Попробуйте позже.')
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
  max-width: 400px;
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

.icon.loading {
  color: #8B5CF6;
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