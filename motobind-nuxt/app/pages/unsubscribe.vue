<template>
  <div class="unsubscribe-page">
    <BaseCard class="unsubscribe-card">
      <template #header>
        <h1 class="title">Управление рассылкой</h1>
      </template>

      <div v-if="status === 'idle'" class="content">
        <p>Вы действительно хотите отписаться от новостной рассылки MotoBind?</p>
        <div class="actions">
          <BaseButton variant="primary" :loading="isLoading" @click="unsubscribe">
            Да, отписаться
          </BaseButton>
          <NuxtLink to="/" class="cancel-link">Остаться на сайте</NuxtLink>
        </div>
      </div>

      <div v-else-if="status === 'loading'" class="content">
        <BaseSpinner />
        <p>Отписываем вас...</p>
      </div>

      <div v-else-if="status === 'success'" class="content success">
        <h2>Вы успешно отписаны</h2>
        <p>Больше мы не будем присылать вам новости на этот email.</p>
        <NuxtLink to="/" class="base-btn">На главную</NuxtLink>
      </div>

      <div v-else-if="status === 'error'" class="content error">
        <h2>Ошибка</h2>
        <p>{{ errorMessage }}</p>
        <NuxtLink to="/" class="base-btn">На главную</NuxtLink>
      </div>
    </BaseCard>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const token = ref<string | null>(null)
const status = ref<'idle' | 'loading' | 'success' | 'error'>('idle')
const errorMessage = ref('')
const isLoading = ref(false)

onMounted(() => {
    if(route.query.token) {
        token.value = route.query.token as string
    } else {
        status.value = 'error'
        errorMessage.value = 'Ссылка недействительная'
    }
})

const unsubscribe = async () => {
    if (!token.value) return

    isLoading.value = true
    status.value = 'loading'

    try {
        await $fetch('/api/user/unsubscribe', {
            method: 'POST',
            body: { token: token.value },
        })

        status.value = 'success'
    } catch (err: any) {
        status.value = 'error'
        errorMessage.value = err.data?.error || err.data?.message || 'Произошла ошибка при отписке.'
    } finally {
        isLoading.value = false
    }
}

useSeoMeta({
    title: 'Отписка от рассылки | MotoBind',
    robots: 'noindex, nofollow',
})
</script>

<style scoped lang="scss">
.unsubscribe-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  padding: 20px;
}

.unsubscribe-card {
  max-width: 500px;
  width: 100%;
  text-align: center;
}

.title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.content {
  padding: 20px 0;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 25px;
  align-items: center;
}

.cancel-link {
  color: var(--color-text-secondary);
  text-decoration: underline;
  font-size: 0.9rem;
}

.success h2 { color: var(--color-success); }
.error h2 { color: var(--color-error); }
</style>