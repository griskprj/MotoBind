<template>
  <div class="unsubscribe-page">
    <div class="container">
      <div class="unsubscribe-card">
        <div v-if="loading" class="loading-state">
          <i class="fa fa-spinner fa-spin"></i>
          <span>Обработка запроса...</span>
        </div>

        <div v-else-if="success" class="success-state">
          <div class="icon success">
            <i class="fa fa-check-circle"></i>
          </div>
          <h2>Вы отписались от рассылки</h2>
          <p>Вы больше не будете получать новостные письма от MotoBind</p>
          <BaseButton variant="primary" @click="goHome">
            На главную
          </BaseButton>
        </div>

        <div v-else-if="error" class="error-state">
          <div class="icon error">
            <i class="fa fa-exclamation-circle"></i>
          </div>
          <h2>Ошибка</h2>
          <p>{{ errorMessage }}</p>
          <BaseButton variant="primary" @click="goProfile">
            В профиль
          </BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { BaseButton } from '@/components/ui'
import api from '@/api/api'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const success = ref(false)
const error = ref(false)
const errorMessage = ref('')

onMounted(() => {
  const token = route.params.token
  if (token) {
    unsubscribe(token)
  } else {
    error.value = true
    errorMessage.value = 'Недействительная ссылка'
    loading.value = false
  }
})

async function unsubscribe(token) {
  try {
    await api.get(`/unsubscribe/${token}`)
    success.value = true
  } catch (err) {
    error.value = true
    errorMessage.value = err.response?.data?.error || 'Ошибка при отписке'
  } finally {
    loading.value = false
  }
}

function goHome() {
  router.push('/')
}

function goProfile() {
  router.push('/profile')
}
</script>

<style scoped>
.unsubscribe-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 80vh;
  padding: 20px;
}

.unsubscribe-card {
  max-width: 500px;
  width: 100%;
  padding: 40px;
  background: var(--bg-secondary);
  border-radius: 16px;
  border: 1px solid var(--border-color);
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

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  color: var(--text-secondary);
}

.loading-state i {
  font-size: 40px;
  color: var(--accent);
}

h2 {
  margin: 0 0 8px 0;
  color: var(--text-primary);
}

p {
  color: var(--text-secondary);
  margin: 0 0 24px 0;
}
</style>
