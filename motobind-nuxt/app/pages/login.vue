<script setup lang="ts">
import type { ApiError } from '~/types'

definePageMeta({
  layout: 'auth',
  middleware: 'guest',
})

useSeoMeta({
  title: 'Вход',
  description: 'Войдите в MotoBind, чтобы управлять гаражом, обслуживанием и обучением.',
  robots: 'noindex',
})

const auth = useAuthStore()
const route = useRoute()
const toast = useToast()
const { errors, setFromApiError, clear } = useFormErrors()

const form = reactive({
  email: '',
  password: '',
  rememberMe: false,
})

const submitting = ref(false)

async function onSubmit() {
  clear()
  submitting.value = true
  try {
    await auth.login({
      email: form.email,
      password: form.password,
      rememberMe: form.rememberMe,
    })
    toast.success('Добро пожаловать!')
    const redirect = typeof route.query.redirect === 'string'
      ? route.query.redirect
      : '/garage'
    await navigateTo(redirect)
  } catch (e) {
    const err = e as ApiError
    setFromApiError(err)
    if (!err.fieldErrors) {
      toast.error(err.message || 'Не удалось войти')
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
        <h1 class="auth-title">Вход в MotoBind</h1>
        <p class="auth-subtitle">
          Управляйте гаражом, обслуживанием и обучением в одном месте.
        </p>
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
          v-model="form.password"
          type="password"
          label="Пароль"
          placeholder="••••••••"
          autocomplete="current-password"
          required
          :error="errors.password"
        />

        <BaseCheckbox
          v-model="form.rememberMe"
          label="Запомнить меня"
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
          Войти
        </BaseButton>
      </form>

      <p class="auth-footer">
        Нет аккаунта?
        <NuxtLink to="/register" class="auth-link">Зарегистрироваться</NuxtLink>
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
