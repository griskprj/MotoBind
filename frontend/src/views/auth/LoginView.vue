<template>
  <div class="login-page">
    <BaseCard class="login-card">
      <div class="login-header">
        <i class="fa fa-motorcycle" />
        <h1>Вход в MotoBind</h1>
        <p>Войдите в свой аккаунт, чтобы продолжить</p>
      </div>

      <form @submit.prevent="submit">
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

        <BaseInput
          v-model="values.password"
          label="Пароль"
          type="password"
          placeholder="Введите пароль"
          autocomplete="current-password"
          required
          :error="errors.password"
          @blur="validateNow"
          class="login-field"
        />

        <div class="login-options">
          <label class="checkbox">
            <input v-model="values.rememberMe" type="checkbox">
            <span>Запомнить меня</span>
          </label>
          <router-link to="/forgot-password">Забыли пароль?</router-link>
        </div>

        <BaseButton
          variant="primary"
          type="submit"
          block
          :loading="loading"
        >
          Войти
        </BaseButton>
      </form>

      <div class="login-footer">
        <span>Нет аккаунта?</span>
        <router-link to="/register">Зарегистрироваться</router-link>
      </div>
    </BaseCard>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import { useForm } from '@/composables/useForm'
import { BaseButton, BaseCard, BaseInput } from '@/components/ui'
import api from '@/api/api'

const router = useRouter()
const auth = useAuthStore()
const toast = useToast()

const { values, errors, loading, validateNow, submit: submitForm } = useForm({
  initial: { email: '', password: '', rememberMe: true },
  validate: (v) => {
    const errs = {}
    if (!v.email) errs.email = 'Введите email'
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.email)) {
      errs.email = 'Некорректный email'
    }
    if (!v.password) errs.password = 'Введите пароль'
    return errs
  },
  onSubmit: async (v) => {
    const { data } = await api.post('/auth/login', {
      email: v.email,
      password: v.password,
      rememberMe: v.rememberMe,
    })
    return data
  },
  onSuccess: (data) => {
    auth.setTokens(data.access_token, data.refresh_token)
    auth.setUser(data.user)
    router.push(data.user.role === 'admin' ? '/admin/panel' : '/garage')
  },
  onError: (err) => {
    toast.error(err.response?.data?.error || 'Ошибка входа')
  },
})

async function submit() {
  await submitForm()
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.login-card {
  max-width: 440px;
  width: 100%;
}

.login-header {
  text-align: center;
  margin-bottom: 24px;
}

.login-header i {
  font-size: 48px;
  color: var(--accent);
  margin-bottom: 12px;
  display: inline-block;
}

.login-header h1 {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0 0 8px 0;
}

.login-header p {
  color: var(--text-muted);
  margin: 0;
}

.login-field {
  margin-top: 14px;
}

.login-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 16px 0;
  font-size: 0.9rem;
  gap: 12px;
  flex-wrap: wrap;
}

.checkbox {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: var(--text-secondary);
  user-select: none;
}

.checkbox input {
  width: 18px;
  height: 18px;
  accent-color: var(--accent);
  cursor: pointer;
  margin: 0;
}

.login-options a {
  color: var(--accent);
  text-decoration: none;
}

.login-options a:hover {
  text-decoration: underline;
}

.login-footer {
  text-align: center;
  margin-top: 24px;
  color: var(--text-secondary);
}

.login-footer a {
  color: var(--accent);
  font-weight: 600;
  margin-left: 8px;
  text-decoration: none;
}

.login-footer a:hover {
  text-decoration: underline;
}
</style>
