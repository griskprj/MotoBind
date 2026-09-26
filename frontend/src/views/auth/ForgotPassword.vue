<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h1>Забыли пароль?</h1>
        <p>Введите email, и мы отправим ссылку для сброса</p>
      </div>

      <form @submit.prevent="submit">
        <BaseInput
          v-model="email"
          type="email"
          label="Email"
          placeholder="motorcycle@moto.com"
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
          Отправить
        </BaseButton>

        <div class="auth-links">
          <router-link to="/login">Вспомнили пароль? Войти</router-link>
          <router-link to="/register">Нет аккаунта? Зарегистрироваться</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { BaseButton, BaseInput } from '@/components/ui'
import api from '@/api/api'

const email = ref('')
const loading = ref(false)
const error = ref(null)
const success = ref(null)

async function submit() {
  error.value = null
  success.value = null
  loading.value = true

  try {
    await api.post('/auth/forgot-password', { email: email.value })
    success.value = 'Письмо отправлено! Проверьте почту.'
    email.value = ''
  } catch (err) {
    error.value = err.response?.data?.error || 'Ошибка отправки. Попробуйте позже.'
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

.auth-links {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 20px;
  text-align: center;
}

.auth-links a {
  color: var(--text-muted);
  text-decoration: none;
  font-size: 14px;
  transition: color 0.2s;
}

.auth-links a:hover {
  color: var(--accent);
}
</style>
