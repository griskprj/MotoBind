<template>
  <div class="register-page">
    <BaseCard class="register-card">
      <div class="register-header">
        <i class="fa fa-motorcycle" />
        <h1>Регистрация в MotoBind</h1>
        <p>Создайте аккаунт, чтобы начать вести учёт обслуживания</p>
      </div>

      <form @submit.prevent="submit" class="form-group">
        <BaseInput
          v-model="values.username"
          label="Имя пользователя"
          type="text"
          placeholder="Как к вам обращаться"
          autocomplete="username"
          required
          :error="errors.username"
          @blur="validateNow"
        />

        <BaseInput
          v-model="values.email"
          label="Email"
          type="email"
          placeholder="motorcycle@moto.com"
          autocomplete="email"
          required
          :error="errors.email"
          @blur="validateNow"
          class="field-gap "
        />

        <BaseInput
          v-model="values.password"
          label="Пароль"
          type="password"
          placeholder="Минимум 6 символов"
          autocomplete="new-password"
          required
          :error="errors.password"
          @blur="validateNow"
          class="field-gap"
        />

        <BaseInput
          v-model="values.confirmPassword"
          label="Подтверждение пароля"
          type="password"
          placeholder="Повторите пароль"
          autocomplete="new-password"
          required
          :error="errors.confirmPassword"
          @blur="validateNow"
          class="field-gap"
        />

        <div class="agree-wrap" :class="{ 'has-error': errors.agree }">
          <label class="agree-checkbox">
            <input v-model="values.agree" type="checkbox">
            <span>
              Я согласен с
              <router-link to="/rules" target="_blank">правилами сервиса</router-link>
              и
              <router-link to="/privacy" target="_blank">политикой конфиденциальности</router-link>
            </span>
          </label>
          <p v-if="errors.agree" class="agree-error">{{ errors.agree }}</p>
        </div>

        <BaseButton
          variant="primary"
          type="submit"
          block
          :loading="loading"
          class="submit-btn"
        >
          Зарегистрироваться
        </BaseButton>
      </form>

      <div class="register-footer">
        <span>Уже есть аккаунт?</span>
        <router-link to="/login">Войти</router-link>
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
  initial: {
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    agree: false,
  },
  validate: (v) => {
    const errs = {}
    if (!v.username) errs.username = 'Введите имя'
    else if (v.username.length < 2 || v.username.length > 32) {
      errs.username = 'От 2 до 32 символов'
    }

    if (!v.email) errs.email = 'Введите email'
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.email)) {
      errs.email = 'Некорректный email'
    }

    if (!v.password) errs.password = 'Введите пароль'
    else if (v.password.length < 6) {
      errs.password = 'Минимум 6 символов'
    }

    if (!v.confirmPassword) {
      errs.confirmPassword = 'Повторите пароль'
    } else if (v.confirmPassword !== v.password) {
      errs.confirmPassword = 'Пароли не совпадают'
    }

    if (!v.agree) {
      errs.agree = 'Необходимо согласие с правилами'
    }

    return errs
  },
  onSubmit: async (v) => {
    const { data } = await api.post('/auth/register', {
      email: v.email,
      username: v.username,
      password: v.password,
      role: 'motorcyclist',
    })
    return data
  },
  onSuccess: (data) => {
    auth.setTokens(data.access_token, data.refresh_token)
    auth.setUser(data.user)
    toast.success('Регистрация успешна!')
    router.push('/garage')
  },
  onError: (err) => {
    const detail = err.response?.data?.error || err.response?.data?.detail
    if (Array.isArray(detail)) {
      toast.error(detail.map((d) => d.msg || d).join(', '))
    } else {
      toast.error(detail || 'Ошибка регистрации')
    }
  },
})

async function submit() {
  await submitForm()
}
</script>

<style scoped>
.form-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.register-card {
  max-width: 440px;
  width: 100%;
}

.register-header {
  text-align: center;
  margin-bottom: 24px;
}

.register-header i {
  font-size: 48px;
  line-height: 1;
  color: var(--accent);
  margin-bottom: 12px;
  display: inline-block;
}

.register-header h1 {
  font-size: 1.6rem;
  font-weight: 700;
  margin: 0 0 8px 0;
}

.register-header p {
  color: var(--text-muted);
  margin: 0;
  font-size: 0.95rem;
}

.field-gap {
  margin-top: 14px;
}

.agree-wrap {
  margin-top: 16px;
  margin-bottom: 4px;
}

.agree-checkbox {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  cursor: pointer;
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.4;
  user-select: none;
}

.agree-checkbox input {
  width: 18px;
  height: 18px;
  accent-color: var(--accent);
  cursor: pointer;
  margin: 2px 0 0 0;
  flex-shrink: 0;
}

.agree-checkbox a {
  color: var(--accent);
  text-decoration: none;
}

.agree-checkbox a:hover {
  text-decoration: underline;
}

.agree-wrap.has-error .agree-checkbox {
  color: var(--danger-text);
}

.agree-error {
  font-size: var(--text-xs);
  color: var(--danger-text);
  margin: 4px 0 0;
}

.submit-btn {
  margin-top: 16px;
}

.register-footer {
  text-align: center;
  margin-top: 24px;
  color: var(--text-secondary);
}

.register-footer a {
  color: var(--accent);
  font-weight: 600;
  margin-left: 8px;
  text-decoration: none;
}

.register-footer a:hover {
  text-decoration: underline;
}
</style>
