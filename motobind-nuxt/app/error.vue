<script setup lang="ts">
import type { NuxtError } from '#app'

const props = defineProps<{
  error: NuxtError
}>()

const is404 = computed(() => props.error.statusCode === 404)

const title = computed(() => is404.value ? 'Страница не найдена' : 'Произошла ошибка')
const description = computed(() =>
  is404.value
    ? 'Возможно, страница была удалена или вы ввели неверный адрес.'
    : 'Что-то пошло не так. Попробуйте обновить страницу или вернуться на главную.'
)

function goHome() {
  clearError({ redirect: '/' })
}
</script>

<template>
  <div class="error-page">
    <div class="error-content">
      <div class="error-code">{{ error.statusCode }}</div>
      <h1 class="error-title">{{ title }}</h1>
      <p class="error-desc">{{ description }}</p>

      <p v-if="error.message && !is404" class="error-message">
        {{ error.message }}
      </p>

      <div class="error-actions">
        <BaseButton variant="primary" size="lg" @click="goHome">
          <i class="fa-solid fa-house"></i> На главную
        </BaseButton>
        <BaseButton variant="secondary" size="lg" @click="$router.back()">
          <i class="fa-solid fa-arrow-left"></i> Назад
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.error-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100dvh;
  padding: var(--space-4);
  background: var(--color-bg);
}

.error-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  max-width: 500px;
  gap: var(--space-4);
}

.error-code {
  font-size: 120px;
  font-weight: var(--fw-bold);
  line-height: 1;
  color: var(--color-brand);
  opacity: 0.2;
  margin-bottom: var(--space-2);
}

.error-title {
  font-size: var(--text-3xl);
  font-weight: var(--fw-bold);
  color: var(--color-text);
}

.error-desc {
  font-size: var(--text-base);
  color: var(--color-text-secondary);
  line-height: var(--leading-relaxed);
}

.error-message {
  font-size: var(--text-sm);
  color: var(--color-danger);
  background: var(--color-danger-soft);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-md);
  font-family: var(--font-mono);
}

.error-actions {
  display: flex;
  gap: var(--space-3);
  margin-top: var(--space-4);
  flex-wrap: wrap;
  justify-content: center;
}
</style>
