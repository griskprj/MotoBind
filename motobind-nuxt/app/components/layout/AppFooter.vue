<script setup lang="ts">
const currentYear = new Date().getFullYear()
</script>

<template>
  <footer class="app-footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-brand">
          <NuxtLink to="/" class="logo">
            <span class="logo-m">Moto</span><span class="accent">Bind</span>
          </NuxtLink>
          <p class="footer-desc">Управляй своим мотоциклом.</p>
        </div>

        <div class="footer-links">
          <div class="footer-col">
            <h4>Сервис</h4>
            <NuxtLink to="/garage">Гараж</NuxtLink>
            <NuxtLink to="/maintenance">Обслуживание</NuxtLink>
            <NuxtLink to="/manuals">Мануалы</NuxtLink>
            <NuxtLink to="/training">Обучение</NuxtLink>
            <NuxtLink to="/social">MotoSocial</NuxtLink>
          </div>

          <div class="footer-col">
            <h4>Документы</h4>
            <NuxtLink to="/privacy">Политика конфиденциальности</NuxtLink>
            <NuxtLink to="/terms">Пользовательское соглашение</NuxtLink>
            <NuxtLink to="/consent">Согласие на обработку ПД</NuxtLink>
            <NuxtLink to="/rules">Правила сервиса</NuxtLink>
            <NuxtLink to="/manual-rules">Правила мануалов</NuxtLink>
          </div>

          <div class="footer-col">
            <h4>Информация</h4>
            <NuxtLink to="/contacts">Контакты</NuxtLink>
            <a href="mailto:motobind@yandex.ru">motobind@yandex.ru</a>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <p>© {{ currentYear }} MotoBind. Все права защищены.</p>
        <div class="footer-social">
          <a href="https://t.me/motobind" target="_blank" rel="noopener" title="Telegram">
            <i class="fa-brands fa-telegram"></i>
          </a>
          <a href="https://github.com/griskprj/motobind" target="_blank" rel="noopener" title="GitHub">
            <i class="fa-brands fa-github"></i>
          </a>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.app-footer {
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
  padding: var(--space-8) 0 var(--space-4);
  margin-top: auto;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--space-4);
}

.footer-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-8);
  margin-bottom: var(--space-6);

  @include md-up {
    flex-direction: row;
    justify-content: space-between;
    align-items: flex-start;
  }
}

.footer-brand {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  max-width: 250px;
}

.logo {
  font-size: var(--text-xl);
  font-weight: var(--fw-bold);
  text-decoration: none;
  color: var(--color-text);
}
.logo-m { font-weight: 900; }
.accent { color: var(--color-brand); }

.footer-desc {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.footer-links {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-8);
}

.footer-col {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);

  h4 {
    font-size: var(--text-sm);
    font-weight: var(--fw-semibold);
    color: var(--color-text);
    margin-bottom: var(--space-1);
  }

  a {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    text-decoration: none;
    transition: color var(--transition-fast);

    &:hover {
      color: var(--color-brand);
    }
  }
}

.footer-bottom {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border-light);
  text-align: center;
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);

  @include md-up {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
}

.footer-social {
  display: flex;
  gap: var(--space-3);
  justify-content: center;

  a {
    color: var(--color-text-tertiary);
    font-size: 18px;
    transition: color var(--transition-fast);

    &:hover {
      color: var(--color-brand);
    }
  }
}
</style>
