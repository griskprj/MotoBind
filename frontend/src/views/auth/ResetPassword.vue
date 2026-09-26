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
        <router-link to="/forgot-password" class="reset-link">
          Запросить сброс
        </router-link>
      </div>

      <form v-if="valid" @submit.prevent="submit">
        <BaseInput
          v-model="newPassword"
          type="password"
          label="Новый пароль"
          placeholder="Минимум 6 символов"
          required
        />

        <BaseInput
          v-model="confirmPassword"
          type="password"
          label="Подтвердите пароль"
          placeholder="Повторите пароль"
          required
        />

        <div v-if="error" class="message message-error">
          <i class="fa fa-exclamation-circle"></i> {{ error }}
        </div>

        <div v-if="success" class="message message-success">
          <i class="fa fa-check-circle"></i> {{ success }}
        </div>

        <BaseButton
          type="submit"
          variant="primary"
          block
          :loading="loading"
        >
          Сохранить пароль
        </BaseButton>
      </form>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { BaseButton, BaseInput } from '@/components/ui'
import { useAuthStore } from '@/stores'
import api from '@/api/api'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const token = ref(null)
const email = ref('')
const valid = ref(false)
const checking = ref(true)
const errorMessage = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref(null)
const success = ref(null)

onMounted(() => {
  checkToken()
})

async function checkToken() {
  token.value = route.params.token

  if (!token.value) {
    valid.value = false
    checking.value = false
    errorMessage.value = 'Неверная ссылка сброса.'
    return
  }

  try {
    const response = await api.get(`/auth/check-reset-token/${token.value}`)
    email.value = response.data.email
    valid.value = true
  } catch (err) {
    valid.value = false
    errorMessage.value = err.response?.data?.error || 'Ссылка недействительна или истекла.'
  } finally {
    checking.value = false
  }
}

async function submit() {
  error.value = null
  success.value = null

  if (newPassword.value.length < 6) {
    error.value = 'Пароль должен быть минимум 6 символов'
    return
  }

  if (newPassword.value !== confirmPassword.value) {
    error.value = 'Пароли не совпадают'
    return
  }

  loading.value = true

  try {
    const response = await api.post('/auth/reset-password', {
      token: token.value,
      new_password: newPassword.value,
    })

    if (response.data.access_token) {
      auth.setTokens(response.data.access_token, response.data.refresh_token)
      auth.setUser(response.data.user)
      router.push('/garage')
    } else {
      success.value = 'Пароль успешно изменён!'
      setTimeout(() => {
        router.push('/login')
      }, 3000)
    }
  } catch (err) {
    error.value = err.response?.data?.error || 'Ошибка смены пароля'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-primary);
  padding: 20px;
}

.auth-card {
  max-width: 400px;
  width: 100%;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
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
  color: var(--text-primary);
}

.auth-header p {
  color: var(--text-muted);
  margin: 0;
}

.reset-link {
  display: block;
  margin-top: 16px;
  color: var(--accent);
  text-decoration: none;
  font-weight: 500;
}

.reset-link:hover {
  color: var(--accent-hover);
  text-decoration: underline;
}

.message {
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 14px;
  margin: 12px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.message-error {
  background: var(--danger-trans);
  border: 1px solid var(--danger);
  color: var(--danger-text);
}

.message-success {
  background: var(--success-trans);
  border: 1px solid var(--success);
  color: var(--success-text);
}
</style>
