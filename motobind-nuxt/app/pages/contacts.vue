<script setup lang="ts">
useSeoMeta({
  title: 'Контакты — MotoBind',
  description: 'Свяжитесь с нами по любым вопросам.',
  ogType: 'website',
})
</script>

<template>
  <div class="contacts-page">
    <div class="contacts-content">
      <h1 class="page-title">Контакты</h1>
      <p class="page-subtitle">Есть вопросы или предложения? Напишите нам!</p>

      <div class="contacts-grid">
        <BaseCard padding="lg" class="contact-card">
          <i class="fa-solid fa-envelope"></i>
          <h2>Email</h2>
          <a href="mailto:support@motobind.ru">motobind@yandex.ru</a>
        </BaseCard>
        <BaseCard padding="lg" class="contact-card">
          <i class="fa-brands fa-telegram"></i>
          <h2>Telegram</h2>
          <a href="https://t.me/motobind" target="_blank" rel="noopener">@griskyy</a>
        </BaseCard>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.contacts-page {
  max-width: 800px;
  margin: 0 auto;
  padding: var(--space-10) var(--space-4);
}
.page-title {
  font-size: var(--text-3xl);
  font-weight: var(--fw-bold);
  text-align: center;
}
.page-subtitle {
  text-align: center;
  color: var(--color-text-secondary);
  margin-top: var(--space-2);
  margin-bottom: var(--space-8);
}
.contacts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-4);
}
.contact-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--space-2);

  i {
    font-size: 32px;
    color: var(--color-brand);
    margin-bottom: var(--space-2);
  }
  h2 {
    font-size: var(--text-lg);
    font-weight: var(--fw-semibold);
  }
  a, p {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    text-decoration: none;
  }
  a:hover { color: var(--color-brand); }
}
</style>
