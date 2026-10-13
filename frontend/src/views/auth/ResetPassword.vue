<template>
  <div class="auth-page">
    <BaseCard class="auth-card">
      <!-- Проверка токена -->
      <div v-if="checking" class="auth-header">
        <div class="spinner" />
        <h1>Проверка ссылки...</h1>
      </div>

      <!-- Токен невалиден -->
      <div v-else-if="!valid" class="auth-header">
        <i class="fa fa-exclamation-triangle" style="color: var(--danger)" />
        <h1>Ссылка недействительна</h1>
        <p>{{ errorMessage }}</p>
        <router-link to="/forgot-password" class="reset-link">
          Запросить новую ссылку
        </router-link>
      </div>

      <!-- Форма смены пароля -->
      <template v-else>
        <div class="auth-header">
          <i class="fa fa-key" />
          <h1>Новый пароль</h1>
          <p>Для аккаунта <strong>{{ email }}</strong></p>
        </div>

        <form @submit.prevent="submit">
          <BaseInput
            v-model="values.newPassword"
            label="Новый пароль"
            type="password"
            placeholder="Минимум 6 символов"
            autocomplete="new-password"
            required
            :error="errors.newPassword"
            @blur="validateNow"
          />

          <BaseInput
            v-model="values.confirmPassword"
            label="Подтвердите пароль"
            type="password"
            placeholder="Повторите пароль"
            autocomplete="new-password"
            required
            :error="errors.confirmPassword"
            @blur="validateNow"
            class="field-gap"
          />

          <BaseButton
            variant="primary"
            type="submit"
            block
            :loading="loading"
            class="submit-btn"
          >
            Сохранить пароль
          </BaseButton>
        </form>
      </template>
    </BaseCard>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import { useForm } from '@/composables/useForm'
import { BaseButton, BaseCard, BaseInput } from '@/components/ui'
import api from '@/api/api'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const toast = useToast()

const token = ref(null)
const email = ref('')
const valid = ref(false)
const checking = ref(true)
const errorMessage = ref('')

const { values, errors, loading, validateNow, submit: submitForm } = useForm({
  initial: { newPassword: '', confirmPassword: '' },
  validate: (v) => {
    const errs = {}
    if (!v.newPassword) errs.newPassword = 'Введите пароль'
    else if (v.newPassword.length < 6) {
      errs.newPassword = 'Минимум 6 символов'
    }

    if (!v.confirmPassword) {
      errs.confirmPassword = 'Повторите пароль'
    } else if (v.confirmPassword !== v.newPassword) {
      errs.confirmPassword = 'Пароли не совпадают'
    }

    return errs
  },
  onSubmit: async (v) => {
    const { data } = await api.post('/auth/reset-password', {
      token: token.value,
      new_password: v.newPassword,
    })
    return data
  },
  onSuccess: (data) => {
    if (data.access_token) {
      auth.setTokens(data.access_token, data.refresh_token)
      auth.setUser(data.user)
      router.push('/garage')
    } else {
      toast.success('Пароль изменён! Войдите с новым паролем.')
      router.push('/login')
    }
  },
  onError: (err) => {
    toast.error(err.response?.data?.error || 'Ошибка смены пароля')
  },
})

onMounted(checkToken)

async function checkToken() {
  token.value = route.params.token || null

  if (!token.value) {
    valid.value = false
    checking.value = false
    errorMessage.value = 'Неверная ссылка сброса.'
    return
  }

  try {
    const { data } = await api.get(`/auth/check-reset-token/${token.value}`)
    email.value = data.email
    valid.value = true
  } catch (err) {
    valid.value = false
    errorMessage.value =
      err.response?.data?.error || 'Ссылка недействительна или истекла.'
  } finally {
    checking.value = false
  }
}

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

.auth-header strong {
  color: var(--text-primary);
}

.spinner {
  width: 42px;
  height: 42px;
  border: 4px solid var(--border-color);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 12px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.reset-link {
  display: inline-block;
  margin-top: 16px;
  color: var(--accent);
  text-decoration: none;
  font-weight: 500;
}

.reset-link:hover {
  text-decoration: underline;
}

.field-gap {
  margin-top: 14px;
}

.submit-btn {
  margin-top: 16px;
}
</style>
