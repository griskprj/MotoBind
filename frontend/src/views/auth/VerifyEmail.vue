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
        <BaseButton variant="primary" @click="goToApp">
          Перейти в приложение
        </BaseButton>
      </div>

      <div v-else-if="status === 'error'" class="status-error">
        <div class="icon error">
          <i class="fa fa-exclamation-circle"></i>
        </div>
        <h2>Ошибка подтверждения</h2>
        <p>{{ errorMessage }}</p>
        <BaseButton variant="outline" @click="resend">
          Отправить повторно
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { BaseButton } from '@/components/ui'
import { useToast } from '@/composables/useToast'
import { useAuthStore } from '@/stores'
import api from '@/api/api'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const auth = useAuthStore()

const status = ref('loading')
const errorMessage = ref('')
const token = ref(null)

onMounted(() => {
  verify()
})

async function verify() {
  token.value = route.params.token

  if (!token.value) {
    status.value = 'error'
    errorMessage.value = 'Неверная ссылка подтверждения.'
    return
  }

  try {
    const response = await api.get(`/auth/verify-email/${token.value}`)
    const { access_token, refresh_token, user } = response.data

    auth.setTokens(access_token, refresh_token)
    auth.setUser(user)

    status.value = 'success'
  } catch (err) {
    status.value = 'error'
    errorMessage.value = err.response?.data?.error || 'Ссылка недействительна или истекла.'
  }
}

async function resend() {
  try {
    await api.post('/auth/resend-verification')
    toast.success('Письмо отправлено повторно! Проверьте почту.')
  } catch (err) {
    toast.error('Ошибка отправки. Попробуйте позже.')
  }
}

function goToApp() {
  router.push('/garage')
}
</script>

<style scoped>
.verify-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-primary);
  padding: 20px;
}

.verify-card {
  max-width: 420px;
  width: 100%;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 16px;
  padding: 48px 32px;
  text-align: center;
}

.icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.icon.success {
  color: var(--success-text);
}

.icon.error {
  color: var(--danger-text);
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--border-color);
  border-top: 4px solid var(--accent);
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
  color: var(--text-primary);
}

.verify-card p {
  color: var(--text-muted);
  margin: 0 0 24px 0;
  line-height: 1.6;
}
</style>
