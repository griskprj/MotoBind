<template>
  <div class="auth-page">
    <BaseCard class="auth-card">
      <div class="auth-header">
        <i class="fa fa-lock" />
        <h1>Забыли пароль?</h1>
        <p>Введите email, и мы отправим ссылку для сброса</p>
      </div>

      <form v-if="!success" @submit.prevent="submit">
        <BaseInput
          v-model="values.email"
          label="Email"
          type="email"
          placeholder="motorcycle@moto.com"
          autocomplete="email"
          required
          :error="errors.email"
          @blur="validateNow"
        />

        <BaseButton
          variant="primary"
          type="submit"
          block
          :loading="loading"
          class="auth-submit"
        >
          Отправить ссылку
        </BaseButton>
      </form>

      <div v-else class="auth-success">
        <i class="fa fa-check-circle" />
        <h3>Письмо отправлено</h3>
        <p>
          Проверьте почту <strong>{{ values.email }}</strong>.
          Ссылка действует 1 час.
        </p>
      </div>

      <div class="auth-footer">
        <router-link to="/login">Вспомнили пароль? Войти</router-link>
        <router-link to="/register">Нет аккаунта? Зарегистрироваться</router-link>
      </div>
    </BaseCard>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useToast } from '@/composables/useToast'
import { useForm } from '@/composables/useForm'
import { BaseButton, BaseCard, BaseInput } from '@/components/ui'
import api from '@/api/api'

const toast = useToast()
const success = ref(false)

const { values, errors, loading, validateNow, submit: submitForm } = useForm({
  initial: { email: '' },
  validate: (v) => {
    const errs = {}
    if (!v.email) errs.email = 'Введите email'
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.email)) {
      errs.email = 'Некорректный email'
    }
    return errs
  },
  onSubmit: async (v) => {
    await api.post('/auth/forgot-password', { email: v.email })
  },
  onSuccess: () => {
    success.value = true
  },
  onError: (err) => {
    toast.error(err.response?.data?.error || 'Ошибка отправки')
  },
})

async function submit() {
  await submitForm()
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.auth-card {
  max-width: 440px;
  width: 100%;
}

.auth-header {
  text-align: center;
  margin-bottom: 24px;
}

.auth-header i {
  font-size: 42px;
  line-height: 1;
  color: var(--accent);
  margin-bottom: 12px;
  display: inline-block;
}

.auth-header h1 {
  font-size: 1.6rem;
  font-weight: 700;
  margin: 0 0 8px 0;
}

.auth-header p {
  color: var(--text-muted);
  margin: 0;
  font-size: 0.95rem;
}

.auth-submit {
  margin-top: 8px;
}

.auth-success {
  text-align: center;
  padding: 16px 0;
}

.auth-success i {
  font-size: 42px;
  color: var(--success);
  margin-bottom: 8px;
  display: inline-block;
}

.auth-success h3 {
  margin: 0 0 8px 0;
  font-size: 1.1rem;
}

.auth-success p {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin: 0;
  line-height: var(--leading-base);
}

.auth-success strong {
  color: var(--text-primary);
}

.auth-footer {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 24px;
  text-align: center;
}

.auth-footer a {
  color: var(--text-muted);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.auth-footer a:hover {
  color: var(--accent);
}
</style>
