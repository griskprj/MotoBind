<script setup lang="ts">
import { ref, onMounted } from 'vue'
definePageMeta({ layout: 'landing' })

const auth = useAuthStore()
const { resolvedTheme, toggleTheme } = useTheme()

const ctaLink = computed(() => auth.isAuthenticated ? '/garage' : '/login')

// Плавное появление при скролле
const observer = ref<IntersectionObserver | null>(null)
const animatedElements = ref<HTMLElement[]>([])

onMounted(() => {
  // Настраиваем IntersectionObserver для анимаций
  observer.value = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible')
        observer.value?.unobserve(entry.target)
      }
    })
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' })

  // Находим все элементы с классом .reveal и подписываемся
  document.querySelectorAll('.reveal').forEach((el) => {
    observer.value?.observe(el)
  })
})

onBeforeUnmount(() => {
  observer.value?.disconnect()
})
</script>

<template>
  <div class="landing">
    <!-- ПАРТИКЛЫ (пока заглушка, добавим позже) -->
    <div class="particles-bg"></div>

    <!-- ХЕДЕР -->
    <header class="landing-header">
      <div class="container header-container">
        <NuxtLink to="/" class="logo">
          <span class="logo-m">Moto</span><span class="accent">Bind</span>
        </NuxtLink>

        <div class="header-actions">
          <NuxtLink v-if="!auth.isAuthenticated" to="/login" class="login-link">
            Войти
          </NuxtLink>
          <BaseButton :to="ctaLink" variant="primary" size="sm">
            {{ auth.isAuthenticated ? 'В гараж' : 'Начать' }}
          </BaseButton>
          <button class="theme-toggle" @click="toggleTheme" title="Сменить тему">
            <i :class="resolvedTheme === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon'"></i>
          </button>
        </div>
      </div>
    </header>

    <!-- ГЕРОЙ -->
    <section class="hero">
      <div class="container hero-grid">
        <div class="hero-content">
          <div class="hero-mini-badge">Всё для мотоцикла. В одном месте.</div>
          <h1 class="hero-title">
            Всё для вашего<br>
            <span class="accent">мотоцикла</span><br>
            в одном месте
          </h1>
          <p class="hero-desc">
            MotoBind — сервис для мотоциклистов, который помогает вести учёт обслуживания,
            хранить мануалы и находить инструкции по ремонту.
          </p>
          <div class="hero-tags">
            <div class="tag">
              <div class="tag-icon"><i class="fa-solid fa-check-circle"></i></div>
              <div>
                <div class="tag-title">Удобно</div>
                <div class="tag-desc">Все данные в одном месте</div>
              </div>
            </div>
            <div class="tag">
              <div class="tag-icon"><i class="fa-solid fa-bolt"></i></div>
              <div>
                <div class="tag-title">Надёжно</div>
                <div class="tag-desc">Защита ваших данных</div>
              </div>
            </div>
            <div class="tag">
              <div class="tag-icon"><i class="fa-solid fa-shield-alt"></i></div>
              <div>
                <div class="tag-title">Бесплатно</div>
                <div class="tag-desc">Основные функции</div>
              </div>
            </div>
          </div>
          <div class="hero-buttons">
            <BaseButton :to="ctaLink" variant="primary" size="lg">
              Начать бесплатно
              <template #icon><i class="fa-solid fa-arrow-right"></i></template>
            </BaseButton>
            <BaseButton to="/manuals" variant="secondary" size="lg">
              Смотреть мануалы
            </BaseButton>
          </div>
        </div>
        <div class="hero-image reveal">
          <img src="/hero-moto.webp" alt="Мотоцикл в фиолетовом свете" class="landing-img" />
        </div>
      </div>
    </section>

    <!-- ФИЧИ -->
    <section class="section features reveal">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Всё, что нужно <span class="accent">мотоциклисту</span></h2>
          <p class="section-desc">Продвинутые инструменты для ухода за мотоциклом и ведения истории обслуживания</p>
        </div>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon"><i class="fa-solid fa-motorcycle"></i></div>
            <h3 class="feature-title">Гараж мотоциклов</h3>
            <p class="feature-desc">Добавляйте мотоциклы и храните всю важную информацию о них.</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon"><i class="fa-solid fa-tools"></i></div>
            <h3 class="feature-title">Обслуживание</h3>
            <p class="feature-desc">Планируйте ТО, записывайте работы и контролируйте состояние.</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon"><i class="fa-solid fa-book"></i></div>
            <h3 class="feature-title">Мануалы</h3>
            <p class="feature-desc">Пошаговые инструкции по ремонту от сообщества.</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon"><i class="fa-solid fa-chart-bar"></i></div>
            <h3 class="feature-title">Статистика</h3>
            <p class="feature-desc">Анализируйте затраты и динамику состояния узлов.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ИНТЕРФЕЙС -->
    <section class="section section-alt">
      <div class="container">
        <div class="split-layout reveal">
          <div class="split-left">
            <h3 class="split-title">Интерфейс, созданный для мотоциклистов</h3>
            <p class="split-desc">
              Лёгкий дизайн, удобная навигация, всё необходимое под рукой.
              Создан для тех, кто ценит своё время.
            </p>
          </div>
          <div class="split-right">
            <img src="/app-mockup.webp" alt="Интерфейс MotoBind" class="landing-img" />
          </div>
        </div>
      </div>
    </section>

    <!-- КАТАЛОГ -->
    <section class="section">
      <div class="container">
        <div class="split-layout reverse reveal">
          <div class="split-right">
            <img src="/app-mockup-catalog.webp" alt="Каталог мануалов" class="landing-img" />
          </div>
          <div class="split-left">
            <h3 class="split-title">Каталог работ</h3>
            <p class="split-desc">
              Готовые инструкции по обслуживанию и ремонту мотоциклов
              для разных моделей — от замены масла до полной разборки.
            </p>
            <BaseButton to="/manuals" variant="secondary" size="lg" class="split-button">
              Смотреть мануалы
            </BaseButton>
          </div>
        </div>
      </div>
    </section>

    <!-- КАК ЭТО РАБОТАЕТ -->
    <section class="section section-alt">
      <div class="container">
        <div class="section-header reveal">
          <p class="mini-label">КАК ЭТО РАБОТАЕТ</p>
          <h2 class="section-title">Три простых шага <br>к идеальному порядку в гараже</h2>
        </div>
        <div class="steps-grid reveal">
          <div class="step-card">
            <div class="step-number">1</div>
            <div class="step-icon"><i class="fa-solid fa-motorcycle"></i></div>
            <h3 class="step-title">Создайте гараж</h3>
            <p class="step-desc">Добавьте мотоциклы с ключевыми характеристиками и фото.</p>
          </div>
          <div class="step-card">
            <div class="step-number">2</div>
            <div class="step-icon"><i class="fa-solid fa-calendar-check"></i></div>
            <h3 class="step-title">Планируйте и обслуживайте</h3>
            <p class="step-desc">Планируйте ТО, получайте напоминания и записывайте работы.</p>
          </div>
          <div class="step-card">
            <div class="step-number">3</div>
            <div class="step-icon"><i class="fa-solid fa-book"></i></div>
            <h3 class="step-title">Храните и создавайте</h3>
            <p class="step-desc">Храните мануалы и создавайте свои инструкции по ремонту.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- МОТОЦИКЛИСТЫ -->
    <section class="section">
      <div class="container riders-layout reveal">
        <div class="riders-left">
          <img src="/riders.webp" alt="Мотоциклисты MotoBind" class="landing-img" />
        </div>
        <div class="riders-right">
          <h2 class="section-title left-align">Создан мотоциклистами <br><span class="accent">для мотоциклистов</span></h2>
          <p class="section-desc left-align">
            Мы создали MotoBind, чтобы каждый мотоциклист мог легко управлять уходом за своим железным конём.
          </p>
          <div class="riders-grid">
            <div class="rider-item">
              <div class="rider-icon"><i class="fa-solid fa-road"></i></div>
              <h4 class="rider-title">Без рисков</h4>
              <p class="rider-desc">Никаких сомнений в состоянии мотоцикла</p>
            </div>
            <div class="rider-item">
              <div class="rider-icon"><i class="fa-solid fa-tools"></i></div>
              <h4 class="rider-title">Работает быстро</h4>
              <p class="rider-desc">Оптимизирован для любых устройств</p>
            </div>
            <div class="rider-item">
              <div class="rider-icon"><i class="fa-solid fa-rocket"></i></div>
              <h4 class="rider-title">Постоянное развитие</h4>
              <p class="rider-desc">Новые функции на основе ваших идей</p>
            </div>
            <div class="rider-item">
              <div class="rider-icon"><i class="fa-solid fa-lock"></i></div>
              <h4 class="rider-title">Ваши данные — ваши</h4>
              <p class="rider-desc">Полный контроль над информацией</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="section">
      <div class="container">
        <div class="cta-layout reveal">
          <div class="cta-left">
            <h2 class="cta-title">Готовы взять контроль <br>над своим мотоциклом?</h2>
            <p class="cta-desc">Присоединяйтесь к MotoBind и сделайте обслуживание простым и понятным.</p>
            <BaseButton :to="ctaLink" variant="primary" size="lg">
              Начать бесплатно
              <template #icon><i class="fa-solid fa-arrow-right"></i></template>
            </BaseButton>
          </div>
          <div class="cta-right">
            <img src="/16x9Auth-Bg.webp" alt="Начните бесплатно" class="landing-img" />
          </div>
        </div>
      </div>
    </section>

    <!-- ФУТЕР -->
    <footer class="landing-footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-brand">
            <span class="logo"><span class="logo-m">Moto</span><span class="accent">Bind</span></span>
            <p class="footer-desc">Сервис для тех, кто любит мотоциклы.</p>
          </div>
          <div class="footer-links">
            <NuxtLink to="/manuals">Мануалы</NuxtLink>
            <NuxtLink to="/training">Обучение</NuxtLink>
            <NuxtLink to="/social">MotoSocial</NuxtLink>
            <NuxtLink to="/contacts">Контакты</NuxtLink>
          </div>
        </div>
        <div class="footer-bottom">
          <p>© {{ new Date().getFullYear() }} MotoBind. Все права защищены.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.landing {
  background-color: var(--color-bg);
  color: var(--color-text);
  overflow-x: hidden;
  position: relative;
}

/* Партиклы (пока просто фон) */
.particles-bg {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  background: radial-gradient(circle at 50% 50%, color-mix(in srgb, var(--color-brand) 5%, transparent) 0%, transparent 70%);
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--space-4);
  position: relative;
  z-index: 1;
}

.accent {
  color: var(--color-brand);
}

/* ХЕДЕР */
.landing-header {
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
  background: color-mix(in srgb, var(--color-bg) 85%, transparent);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--color-border-light);
  padding: var(--space-3) 0;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--space-4);
}

.logo {
  font-size: 24px;
  font-weight: var(--fw-bold);
  letter-spacing: -0.5px;
  text-decoration: none;
}
.logo-m { font-weight: 900; }

.header-actions {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.login-link {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  text-decoration: none;
  &:hover { color: var(--color-text); }
}

.theme-toggle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid var(--color-border);
  background: transparent;
  color: var(--color-text);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);

  &:hover {
    background: var(--color-brand);
    border-color: var(--color-brand);
    color: #fff;
  }
}

/* ГЕРОЙ */
.hero {
  padding: var(--space-10) 0 var(--space-8);
  position: relative;
}

.hero-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-8);
  align-items: center;

  @include lg-down {
    grid-template-columns: 1fr;
    text-align: center;
    gap: var(--space-6);
  }
}

.hero-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  align-items: flex-start;

  @include lg-down {
    align-items: center;
  }
}

.hero-mini-badge {
  display: inline-block;
  background: var(--color-brand-soft);
  color: var(--color-brand);
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: var(--fw-medium);
  border: 1px solid var(--color-brand-soft);
}

.hero-title {
  font-size: 52px;
  font-weight: var(--fw-bold);
  line-height: 1.1;
  color: var(--color-text);

  @include md-down { font-size: 40px; }
  @include sm-down { font-size: 32px; }
}

.hero-desc {
  font-size: var(--text-lg);
  color: var(--color-text-secondary);
  line-height: var(--leading-relaxed);
  max-width: 480px;
}

.hero-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
  margin: var(--space-2) 0;

  @include lg-down { justify-content: center; }
}

.tag {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.tag-icon {
  width: 32px;
  height: 32px;
  background: var(--color-brand-soft);
  color: var(--color-brand);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.tag-title { font-size: var(--text-sm); font-weight: var(--fw-semibold); }
.tag-desc { font-size: var(--text-xs); color: var(--color-text-tertiary); }

.hero-buttons {
  display: flex;
  gap: var(--space-3);
  flex-wrap: wrap;

  @include lg-down { justify-content: center; }
}

.hero-image {
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: var(--radius-xl);
  overflow: hidden;
  border: 1px solid var(--color-border-light);
  box-shadow: 0 20px 60px -20px var(--color-brand-soft);
}

.landing-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* СЕКЦИИ */
.section { padding: var(--space-10) 0; }
.section-alt { background: var(--color-surface-secondary); }

.section-header {
  text-align: center;
  margin-bottom: var(--space-8);
}

.section-title {
  font-size: var(--text-3xl);
  font-weight: var(--fw-semibold);
  margin-bottom: var(--space-3);
  line-height: 1.2;

  &.left-align { text-align: left; }
}

.section-desc {
  color: var(--color-text-secondary);
  font-size: var(--text-base);
  max-width: 520px;
  margin: 0 auto;
  line-height: var(--leading-relaxed);

  &.left-align {
    max-width: 100%;
    margin: 0 0 var(--space-4) 0;
    text-align: left;
  }
}

.mini-label {
  font-size: var(--text-xs);
  font-weight: var(--fw-semibold);
  color: var(--color-text-tertiary);
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: var(--space-2);
}

/* ФИЧИ */
.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);

  @include md-down { grid-template-columns: repeat(2, 1fr); }
  @include sm-down { grid-template-columns: 1fr; }
}

.feature-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  transition: all var(--transition-fast);

  &:hover {
    background: var(--color-surface-hover);
    border-color: var(--color-brand-soft);
    transform: translateY(-4px);
  }
}

.feature-icon {
  width: 40px;
  height: 40px;
  background: var(--color-brand-soft);
  color: var(--color-brand);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  margin-bottom: var(--space-4);
}

.feature-title {
  font-size: var(--text-base);
  font-weight: var(--fw-semibold);
  margin-bottom: var(--space-2);
}

.feature-desc {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  line-height: var(--leading-base);
}

/* SPLIT LAYOUT */
.split-layout {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: var(--space-8);
  align-items: center;

  &.reverse { grid-template-columns: 1.5fr 1fr; }

  @include lg-down {
    grid-template-columns: 1fr;
    text-align: center;
    gap: var(--space-6);
  }
}

.split-title {
  font-size: var(--text-2xl);
  font-weight: var(--fw-semibold);
  margin-bottom: var(--space-3);
}

.split-desc {
  font-size: var(--text-base);
  color: var(--color-text-secondary);
  line-height: var(--leading-relaxed);
}

.split-right {
  width: 100%;
  aspect-ratio: 16 / 10;
  border-radius: var(--radius-xl);
  overflow: hidden;
  border: 1px solid var(--color-border);
}

/* ШАГИ */
.steps-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-6);

  @include md-down { grid-template-columns: 1fr; max-width: 420px; margin: 0 auto; }
}

.step-card {
  position: relative;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-8) var(--space-6);
  text-align: center;
  transition: all var(--transition-fast);

  &:hover {
    background: var(--color-surface-hover);
    transform: translateY(-4px);
  }
}

.step-number {
  position: absolute;
  top: -14px;
  left: 50%;
  transform: translateX(-50%);
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--color-brand);
  color: #fff;
  font-size: var(--text-sm);
  font-weight: var(--fw-bold);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 0 4px var(--color-surface-secondary);
}

.step-icon {
  width: 56px;
  height: 56px;
  background: var(--color-brand-soft);
  color: var(--color-brand);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin: 0 auto var(--space-4);
}

.step-title {
  font-size: var(--text-lg);
  font-weight: var(--fw-semibold);
  margin-bottom: var(--space-2);
}

.step-desc {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

/* RIDERS */
.riders-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-8);
  align-items: center;

  @include lg-down { grid-template-columns: 1fr; gap: var(--space-6); }
}

.riders-left {
  width: 100%;
  aspect-ratio: 4 / 3;
  border-radius: var(--radius-xl);
  overflow: hidden;
  border: 1px solid var(--color-border);
}

.riders-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-5);
  margin-top: var(--space-6);
}

.rider-icon {
  width: 32px;
  height: 32px;
  background: var(--color-brand-soft);
  color: var(--color-brand);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--space-2);
}

.rider-title { font-size: var(--text-sm); font-weight: var(--fw-semibold); }
.rider-desc { font-size: var(--text-xs); color: var(--color-text-tertiary); }

/* CTA */
.cta-layout {
  background: var(--color-surface-secondary);
  border-radius: var(--radius-xl);
  padding: var(--space-8);
  display: grid;
  grid-template-columns: 1fr 0.8fr;
  gap: var(--space-8);
  align-items: center;
  border: 1px solid var(--color-brand-soft);
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, var(--color-brand-soft) 0%, transparent 70%);
    pointer-events: none;
  }

  @include lg-down {
    grid-template-columns: 1fr;
    text-align: center;
    padding: var(--space-6);
  }
}

.cta-title {
  font-size: var(--text-3xl);
  font-weight: var(--fw-bold);
  margin-bottom: var(--space-3);
}

.cta-desc {
  font-size: var(--text-base);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-4);
}

.cta-right {
  aspect-ratio: 16 / 10;
  border-radius: var(--radius-lg);
  overflow: hidden;
  border: 1px solid var(--color-border);
}

/* ФУТЕР */
.landing-footer {
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
  padding: var(--space-8) 0 var(--space-4);
}

.footer-content {
  display: flex;
  justify-content: space-between;
  gap: var(--space-6);
  margin-bottom: var(--space-6);

  @include md-down { flex-direction: column; }
}

.footer-brand {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.footer-desc {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.footer-links {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);

  a {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    text-decoration: none;
    &:hover { color: var(--color-brand); }
  }
}

.footer-bottom {
  border-top: 1px solid var(--color-border-light);
  padding-top: var(--space-4);
  text-align: center;
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
}

/* АНИМАЦИИ */
.reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}

.reveal.is-visible {
  opacity: 1;
  transform: translateY(0);
}
</style>
