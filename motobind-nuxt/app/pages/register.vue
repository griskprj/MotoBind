<script setup lang="ts">
import type { ApiError } from '~/types'

definePageMeta({
  layout: 'auth',
  middleware: 'guest',
})

useSeoMeta({
  title: 'Регистрация',
  description: 'Создайте аккаунт MotoBind, чтобы управлять гаражом и общаться с сообществом.',
  robots: 'noindex',
})

const auth = useAuthStore()
const route = useRoute()
const toast = useToast()
const { errors, setFromApiError, clear } = useFormErrors()

const form = reactive({
  email: '',
  username: '',
  password: '',
  confirmPassword: '',
})

const submitting = ref(false)

async function onSubmit() {
  clear()

  if (form.password !== form.confirmPassword) {
    toast.error('Пароли не совпадают')
    return
  }

  submitting.value = true
  try {
    await auth.register({
      email: form.email,
      username: form.username,
      password: form.password,
    })
    toast.success('Добро пожаловать в MotoBind!')
    const redirect = typeof route.query.redirect === 'string'
      ? route.query.redirect
      : '/garage'
    await navigateTo(redirect)
  } catch (e) {
    const err = e as ApiError
    setFromApiError(err)
    if (!err.fieldErrors) {
      toast.error(err.message || 'Не удалось зарегистрироваться')
    }
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <BaseCard padding="lg" class="auth-card">
      <header class="auth-header">
        <h1 class="auth-title">Регистрация в MotoBind</h1>
        <p class="auth-subtitle">Создайте аккаунт, чтобы управлять гаражом.</p>
      </header>

      <form class="auth-form" novalidate @submit.prevent="onSubmit">
        <BaseInput
          v-model="form.email"
          type="email"
          label="Email"
          placeholder="you@example.com"
          autocomplete="email"
          required
          :error="errors.email"
        />

        <BaseInput
          v-model="form.username"
          type="text"
          label="Имя пользователя"
          placeholder="MotoRider"
          autocomplete="username"
          required
          :error="errors.username"
        />

        <BaseInput
          v-model="form.password"
          type="password"
          label="Пароль"
          placeholder="••••••••"
          autocomplete="new-password"
          required
          :error="errors.password"
        />

        <BaseInput
          v-model="form.confirmPassword"
          type="password"
          label="Повторите пароль"
          placeholder="••••••••"
          required
        />

        <p v-if="errors._form" class="auth-form-error" role="alert">
          {{ errors._form }}
        </p>

        <BaseButton
          type="submit"
          variant="primary"
          size="lg"
          block
          :loading="submitting"
        >
          Зарегистрироваться
        </BaseButton>
      </form>

      <p class="auth-footer">
        Уже есть аккаунт?
        <NuxtLink to="/login" class="auth-link">Войти</NuxtLink>
      </p>
    </BaseCard>
  </div>
</template>

<style scoped lang="scss">
.auth-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100dvh;
  padding: var(--space-4);
  background: var(--color-bg);
}

.auth-card {
  width: 100%;
  max-width: 420px;
}

.auth-header {
  margin-bottom: var(--space-5);
  text-align: center;
}

.auth-title {
  font-size: var(--text-2xl);
  font-weight: var(--fw-bold);
  color: var(--color-text);
}

.auth-subtitle {
  margin-top: var(--space-2);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.auth-form-error {
  font-size: var(--text-sm);
  color: var(--color-danger);
}

.auth-footer {
  margin-top: var(--space-5);
  text-align: center;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.auth-link {
  color: var(--color-brand);
  font-weight: var(--fw-medium);

  &:hover {
    color: var(--color-brand-hover);
    text-decoration: underline;
  }
}
</style>
