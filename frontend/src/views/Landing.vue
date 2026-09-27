<template>
  <div class="landing">
    <!-- === HEADER === -->
    <header class="header">
      <div class="container header-container">
        <div class="logo">
          <span class="logo-m">Moto</span><span class="accent">Bind</span>
        </div>

        <div class="header-actions">
          <BaseButton variant="outline" @click="goTo('/login')">
            Войти
          </BaseButton>
          <BaseButton variant="primary" @click="goTo('/welcome')">
            Начать
          </BaseButton>
          <button
            class="theme-toggle"
            @click="toggleTheme"
            :title="isDark ? 'Включить светлую тему' : 'Включить темную тему'"
          >
            <i :class="isDark ? 'fa fa-sun' : 'fa fa-moon'"></i>
          </button>
        </div>
      </div>
    </header>

    <!-- === HERO === -->
    <section class="hero">
      <div class="container hero-grid">
        <div class="hero-content">
          <div class="hero-mini-badge">
            Всё для мотоцикла. Всё в одном. Без сервисов.
          </div>

          <h1 class="hero-title">
            Всё для вашего<br>
            <span class="accent">мотоцикла</span><br>
            в одном месте
          </h1>

          <p class="hero-desc">
            MotoBind — сервис для мотоциклистов, который помогает вести учёт обслуживания, хранить мануалы и находить инструкции по ремонту.
          </p>

          <div class="hero-tags">
            <div class="tag">
              <div class="tag-icon"><i class="fa fa-check-circle"></i></div>
              <div>
                <div class="tag-title">Удобно</div>
                <div class="tag-desc">Храните все данные в одном месте</div>
              </div>
            </div>
            <div class="tag">
              <div class="tag-icon"><i class="fa fa-bolt"></i></div>
              <div>
                <div class="tag-title">Надежно</div>
                <div class="tag-desc">Ваши данные всегда под защитой</div>
              </div>
            </div>
            <div class="tag">
              <div class="tag-icon"><i class="fa fa-shield-alt"></i></div>
              <div>
                <div class="tag-title">Бесплатно</div>
                <div class="tag-desc">Основные функции всегда доступны</div>
              </div>
            </div>
          </div>

          <div class="hero-buttons">
            <BaseButton
              variant="primary"
              size="lg"
              icon="fa fa-arrow-right"
              @click="goTo('/welcome')"
            >
              Начать бесплатно
            </BaseButton>
          </div>
        </div>

        <div class="hero-image">
          <img
            src="/hero-moto.webp"
            alt="Мотоцикл в фиолетовом свете — MotoBind"
            class="landing-img"
          >
        </div>
      </div>
    </section>

    <!-- === FEATURES === -->
    <section class="section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">
            Всё, что нужно <span class="accent">мотоциклисту</span>
          </h2>
          <p class="section-desc">
            Продвинутые инструменты для ухода за мотоциклом и ведения истории обслуживания
          </p>
        </div>

        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon"><i class="fa fa-motorcycle"></i></div>
            <div class="feature-title">Гараж мотоциклов</div>
            <div class="feature-desc">Добавляйте свои мотоциклы и храните всю важную информацию о них.</div>
          </div>

          <div class="feature-card">
            <div class="feature-icon"><i class="fa fa-tools"></i></div>
            <div class="feature-title">Обслуживание</div>
            <div class="feature-desc">Планируйте ТО, записывайте выполненные работы и контролируйте состояние.</div>
          </div>

          <div class="feature-card">
            <div class="feature-icon"><i class="fa fa-book"></i></div>
            <div class="feature-title">Мануалы и инструкции</div>
            <div class="feature-desc">Храните и создавайте пошаговые инструкции по ремонту и обслуживанию.</div>
          </div>

          <div class="feature-card">
            <div class="feature-icon"><i class="fa fa-chart-bar"></i></div>
            <div class="feature-title">Статистика</div>
            <div class="feature-desc">Анализируйте затраты и отслеживайте динамику состояния узлов мотоцикла.</div>
          </div>
        </div>
      </div>
    </section>

    <!-- === INTERFACE === -->
    <section class="section section-alt">
      <div class="container">
        <div class="split-layout">
          <div class="split-left">
            <h3 class="split-title">Интерфейс, созданный для мотоциклистов</h3>
            <p class="split-desc">
              Лёгкий дизайн, удобная навигация, всё необходимое под рукой.
              Создан для тех, кто ценит своё время.
            </p>
          </div>
          <div class="split-right">
            <img
              src="/app-mockup.webp"
              alt="MotoBind — управление гаражом на телефоне"
              class="landing-img"
            >
          </div>
        </div>
      </div>
    </section>

    <!-- === CATALOG === -->
    <section class="section">
      <div class="container">
        <div class="split-layout reverse">
          <div class="split-right">
            <img
              src="/app-mockup-catalog.webp"
              alt="MotoBind — каталог мануалов"
              class="landing-img"
            >
          </div>
          <div class="split-left">
            <h3 class="split-title">Каталог работ</h3>
            <p class="split-desc">
              Готовые инструкции по обслуживанию и ремонту мотоциклов
              для разных моделей — от замены масла до полной разборки.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- === HOW IT WORKS === -->
    <section class="section section-alt">
      <div class="container">
        <div class="section-header">
          <p class="mini-label">КАК ЭТО РАБОТАЕТ</p>
          <h2 class="section-title">
            Три простых шага <br>к идеальному порядку в гараже
          </h2>
        </div>

        <div class="steps-grid">
          <div class="step-card">
            <div class="step-number">1</div>
            <div class="step-icon"><i class="fa fa-motorcycle"></i></div>
            <div class="step-title">Создайте гараж</div>
            <div class="step-desc">
              Добавьте свои мотоциклы с ключевыми характеристиками и фото.
            </div>
          </div>

          <div class="step-card">
            <div class="step-number">2</div>
            <div class="step-icon"><i class="fa fa-calendar-check"></i></div>
            <div class="step-title">Планируйте и обслуживайте</div>
            <div class="step-desc">
              Планируйте ТО, получайте напоминания и записывайте выполненные работы.
            </div>
          </div>

          <div class="step-card">
            <div class="step-number">3</div>
            <div class="step-icon"><i class="fa fa-book"></i></div>
            <div class="step-title">Храните и создавайте</div>
            <div class="step-desc">
              Храните мануалы и создавайте свои инструкции по ремонту.
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- === RIDERS === -->
    <section class="section">
      <div class="container riders-layout">
        <div class="riders-left">
          <img
            src="/riders.webp"
            alt="Мотоциклисты MotoBind"
            class="landing-img"
          >
        </div>

        <div class="riders-right">
          <h2 class="section-title left-align">
            Создан мотоциклистами <br>
            <span class="accent">для мотоциклистов</span>
          </h2>
          <p class="section-desc left-align">
            Мы создали MotoBind, чтобы каждый мотоциклист мог легко управлять
            уходом за своим железным конём. Никакой сложной логистики и лишнего
            шума — только нужные инструменты в одном месте.
          </p>

          <div class="riders-grid">
            <div class="rider-item">
              <div class="rider-icon"><i class="fa fa-road"></i></div>
              <div class="rider-title">Без рисков и тревог</div>
              <div class="rider-desc">Никаких сомнений в состоянии мотоцикла</div>
            </div>
            <div class="rider-item">
              <div class="rider-icon"><i class="fa fa-tools"></i></div>
              <div class="rider-title">Работает быстро</div>
              <div class="rider-desc">Оптимизирован для любых устройств</div>
            </div>
            <div class="rider-item">
              <div class="rider-icon"><i class="fa fa-mouse-pointer"></i></div>
              <div class="rider-title">Постоянное развитие</div>
              <div class="rider-desc">Новые функции на основе ваших идей</div>
            </div>
            <div class="rider-item">
              <div class="rider-icon"><i class="fa fa-rocket"></i></div>
              <div class="rider-title">Просто и понятно</div>
              <div class="rider-desc">Интуитивный интерфейс без лишнего шума</div>
            </div>
            <div class="rider-item">
              <div class="rider-icon"><i class="fa fa-lock"></i></div>
              <div class="rider-title">Ваши данные — ваши</div>
              <div class="rider-desc">Полный контроль над личной информацией</div>
            </div>
            <div class="rider-item">
              <div class="rider-icon"><i class="fa fa-wifi"></i></div>
              <div class="rider-title">Всегда с вами</div>
              <div class="rider-desc">Доступ с любых устройств</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- === CTA === -->
    <section class="section">
      <div class="container">
        <div class="cta-layout">
          <div class="cta-left">
            <h2 class="cta-title">
              Готовы взять контроль <br>над своим мотоциклом?
            </h2>
            <p class="cta-desc">
              Присоединяйтесь к MotoBind и сделайте обслуживание простым и понятным.
            </p>
            <BaseButton
              variant="primary"
              size="lg"
              icon="fa fa-arrow-right"
              @click="goTo('/welcome')"
            >
              Начать бесплатно
            </BaseButton>
          </div>

          <div class="cta-right">
            <img
              src="/cta-mockup.webp"
              alt="MotoBind — начните бесплатно"
              class="landing-img"
            >
          </div>
        </div>
      </div>
    </section>

    <!-- Кнопка "Наверх" -->
    <button
      v-show="showBackToTop"
      class="back-to-top"
      @click="scrollToTop"
      aria-label="Наверх"
    >
      <i class="fas fa-arrow-up"></i>
    </button>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { BaseButton } from '@/components/ui'

const router = useRouter()

const showBackToTop = ref(false)
const isDark = ref(true)

const currentYear = computed(() => new Date().getFullYear())

onMounted(() => {
  const saved = localStorage.getItem('theme')
  isDark.value = saved !== 'light'
  document.documentElement.setAttribute('data-theme', isDark.value ? 'dark' : 'light')

  window.addEventListener('scroll', handleScroll)
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})

function handleScroll() {
  showBackToTop.value = window.scrollY > 600
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function scrollToSection(id) {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function toggleTheme() {
  isDark.value = !isDark.value
  const theme = isDark.value ? 'dark' : 'light'
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('theme', theme)
}

function goTo(path) {
  router.push(path)
}
</script>

<style scoped>
/* ============================================
   BASE / LAYOUT
   ============================================ */
.landing {
  background-color: var(--bg-primary);
  color: var(--text-primary);
  font-family: var(--font-sans);
  overflow-x: hidden;
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.accent {
  color: var(--accent-text);
}

.landing-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* ============================================
   HEADER
   ============================================ */
.header {
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
  background: color-mix(in srgb, var(--bg-primary) 85%, transparent);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border-light);
  padding: 16px 0;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.logo {
  font-size: 24px;
  font-weight: var(--fw-bold);
  letter-spacing: -0.5px;
}

.logo-m {
  font-weight: 900;
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.theme-toggle {
  width: 44px;
  height: 44px;
  min-height: 44px;
  padding: 0;
  background: transparent;
  border: 2px solid var(--border-color);
  border-radius: 50%;
  color: var(--text-primary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  transition: all var(--transition-base);
}
.theme-toggle:hover {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
  transform: scale(1.05);
  box-shadow: 0 0 20px var(--accent-trans);
}
.theme-toggle:active {
  transform: scale(0.95);
}
.theme-toggle i {
  transition: transform var(--transition-base);
  pointer-events: none;
}

/* ============================================
   HERO
   ============================================ */
.hero {
  padding: 80px 0 64px;
  position: relative;
}

.hero-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  align-items: center;
}

.hero-content {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.hero-mini-badge {
  display: inline-block;
  background: var(--accent-trans);
  color: var(--accent-text);
  padding: 6px 14px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: var(--fw-medium);
  margin-bottom: 20px;
  align-self: flex-start;
  border: 1px solid var(--accent-trans);
}

.hero-title {
  font-size: 52px;
  font-weight: var(--fw-bold);
  line-height: 1.1;
  margin: 0 0 16px 0;
  color: var(--text-primary);
}

.hero-desc {
  font-size: 16px;
  line-height: var(--leading-relaxed);
  color: var(--text-muted);
  margin: 0 0 24px 0;
  max-width: 480px;
}

.hero-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  margin-bottom: 32px;
}

.tag {
  display: flex;
  align-items: center;
  gap: 12px;
}

.tag-icon {
  width: 32px;
  height: 32px;
  min-height: 32px;
  background: var(--accent-trans);
  color: var(--accent-text);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
}

.tag-title {
  font-size: 14px;
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
}

.tag-desc {
  font-size: 12px;
  color: var(--text-muted);
}

.hero-buttons {
  display: flex;
  gap: 12px;
}

.hero-image {
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: var(--radius-xl);
  overflow: hidden;
  border: 1px solid var(--border-light);
  box-shadow: 0 20px 60px -20px var(--accent-trans);
}

/* ============================================
   SECTIONS
   ============================================ */
.section {
  padding: 64px 0;
}

.section-alt {
  background: var(--bg-secondary);
}

.section-header {
  text-align: center;
  margin-bottom: 48px;
}

.section-title {
  font-size: 36px;
  font-weight: var(--fw-semibold);
  margin: 0 0 12px 0;
  line-height: 1.2;
  color: var(--text-primary);
}

.section-title.left-align {
  text-align: left;
}

.section-desc {
  color: var(--text-muted);
  font-size: 16px;
  max-width: 520px;
  margin: 0 auto;
  line-height: var(--leading-relaxed);
}

.section-desc.left-align {
  max-width: 100%;
  margin: 0 0 24px 0;
  text-align: left;
}

.mini-label {
  font-size: 12px;
  font-weight: var(--fw-semibold);
  color: var(--text-muted);
  letter-spacing: 1px;
  text-transform: uppercase;
  margin: 0 0 8px 0;
}

/* ============================================
   FEATURES
   ============================================ */
.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.feature-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 24px;
  transition: all var(--transition-base);
  min-width: 0;
}
.feature-card:hover {
  background: var(--bg-card-hover);
  border-color: var(--accent-trans);
  transform: translateY(-2px);
}

.feature-icon {
  width: 40px;
  height: 40px;
  min-height: 40px;
  background: var(--accent-trans);
  color: var(--accent-text);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  margin-bottom: 16px;
}

.feature-title {
  font-size: 16px;
  font-weight: var(--fw-semibold);
  margin-bottom: 8px;
  color: var(--text-primary);
}

.feature-desc {
  font-size: 14px;
  color: var(--text-muted);
  line-height: var(--leading-base);
}

/* ============================================
   SPLIT LAYOUT (Interface / Catalog)
   ============================================ */
.split-layout {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 48px;
  align-items: center;
}

.split-layout.reverse {
  grid-template-columns: 1.5fr 1fr;
}

.split-title {
  font-size: 28px;
  font-weight: var(--fw-semibold);
  margin: 0 0 12px 0;
  color: var(--text-primary);
  line-height: 1.25;
}

.split-desc {
  font-size: 16px;
  color: var(--text-muted);
  margin: 0;
  line-height: var(--leading-relaxed);
}

.split-right {
  width: 100%;
  aspect-ratio: 16 / 10;
  border-radius: var(--radius-xl);
  overflow: hidden;
  border: 1px solid var(--border-light);
}

/* ============================================
   STEPS
   ============================================ */
.steps-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.step-card {
  position: relative;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 32px 24px;
  text-align: center;
  transition: all var(--transition-base);
}
.step-card:hover {
  background: var(--bg-card-hover);
  transform: translateY(-4px);
  border-color: var(--accent-trans);
}

.step-number {
  position: absolute;
  top: -14px;
  left: 50%;
  transform: translateX(-50%);
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  font-size: 14px;
  font-weight: var(--fw-bold);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 0 4px var(--bg-secondary);
}

.step-icon {
  width: 56px;
  height: 56px;
  min-height: 56px;
  background: var(--accent-trans);
  color: var(--accent-text);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin: 0 auto 16px;
}

.step-title {
  font-size: 18px;
  font-weight: var(--fw-semibold);
  margin-bottom: 8px;
  color: var(--text-primary);
}

.step-desc {
  font-size: 14px;
  color: var(--text-muted);
  line-height: var(--leading-base);
}

/* ============================================
   RIDERS
   ============================================ */
.riders-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  align-items: center;
}

.riders-left {
  width: 100%;
  aspect-ratio: 4 / 3;
  border-radius: var(--radius-xl);
  overflow: hidden;
  border: 1px solid var(--border-light);
}

.riders-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 24px;
}

.rider-item {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.rider-icon {
  width: 32px;
  height: 32px;
  min-height: 32px;
  background: var(--accent-trans);
  color: var(--accent-text);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  margin-bottom: 8px;
  flex-shrink: 0;
}

.rider-title {
  font-size: 14px;
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
}

.rider-desc {
  font-size: 12px;
  color: var(--text-muted);
  line-height: var(--leading-base);
}

/* ============================================
   CTA
   ============================================ */
.cta-layout {
  background: var(--bg-secondary);
  border-radius: var(--radius-xl);
  padding: 48px 56px;
  display: grid;
  grid-template-columns: 1fr 0.8fr;
  gap: 48px;
  align-items: center;
  border: 1px solid var(--accent-trans);
  position: relative;
  overflow: hidden;
}

.cta-layout::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -20%;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, var(--accent-trans) 0%, transparent 70%);
  pointer-events: none;
}

.cta-left {
  position: relative;
  z-index: 1;
  min-width: 0;
}

.cta-title {
  font-size: 32px;
  font-weight: var(--fw-bold);
  margin: 0 0 12px 0;
  color: var(--text-primary);
  line-height: 1.2;
}

.cta-desc {
  font-size: 16px;
  color: var(--text-muted);
  margin: 0 0 24px 0;
  line-height: var(--leading-relaxed);
}

.cta-right {
  position: relative;
  z-index: 1;
  width: 100%;
  aspect-ratio: 16 / 16;
  border-radius: var(--radius-lg);
  overflow: hidden;
  border: 1px solid var(--border-light);
}

/* ============================================
   BACK TO TOP
   ============================================ */
.back-to-top {
  position: fixed;
  bottom: 80px;
  right: 24px;
  width: 48px;
  height: 48px;
  min-height: 48px;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  border: none;
  font-size: 20px;
  cursor: pointer;
  box-shadow: var(--shadow-lg);
  transition: all var(--transition-base);
  z-index: var(--z-sticky);
  display: flex;
  align-items: center;
  justify-content: center;
}
.back-to-top:hover {
  transform: translateY(-4px);
  background: var(--accent-hover);
}

/* ============================================
   АДАПТИВ
   Шкала: 1024 → 820 → 640 → 480 → 400
   ============================================ */

/* --- Планшет --- */
@media (max-width: 1024px) {
  .hero-grid {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 40px;
  }
  .hero-content { align-items: center; }
  .hero-mini-badge { align-self: center; }
  .hero-desc {
    margin-left: auto;
    margin-right: auto;
  }
  .hero-tags { justify-content: center; }
  .hero-buttons { justify-content: center; }

  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .split-layout,
  .split-layout.reverse {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 32px;
  }
  .split-layout.reverse .split-right { order: -1; }

  .riders-layout {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .cta-layout {
    grid-template-columns: 1fr;
    text-align: center;
    padding: 40px 32px;
  }
  .cta-layout .btn,
  .cta-left :deep(.btn) {
    margin: 0 auto;
  }

  .footer-container {
    grid-template-columns: 1fr;
    gap: 32px;
  }
}

/* --- Мобильный планшет --- */
@media (max-width: 820px) {
  .section { padding: 48px 0; }
  .hero { padding: 56px 0 40px; }

  .hero-title { font-size: 40px; }
  .section-title { font-size: 28px; }
  .split-title { font-size: 24px; }
  .cta-title { font-size: 26px; }

  .steps-grid {
    grid-template-columns: 1fr;
    max-width: 420px;
    margin: 0 auto;
    gap: 28px;
  }

  .riders-grid {
    grid-template-columns: 1fr 1fr;
  }

  .footer-cols {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
}

/* --- Мобильные --- */
@media (max-width: 640px) {
  .container { padding: 0 16px; }

  .header { padding: 12px 0; }
  .header-container { gap: 10px; }
  .logo { font-size: 20px; }
  .header-actions { gap: 8px; }

  .hero-title { font-size: 32px; }
  .section-title { font-size: 24px; }
  .split-title { font-size: 22px; }
  .cta-title { font-size: 22px; }

  .features-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .feature-card { padding: 20px; }

  .hero-tags {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  .hero-buttons { width: 100%; }
  .hero-buttons > * { width: 100%; }

  .cta-layout { padding: 32px 20px; }
  .cta-left :deep(.btn),
  .cta-layout :deep(.btn) { width: 100%; justify-content: center; }

  .footer { padding: 32px 0 20px; }
  .footer-bottom {
    flex-direction: column;
    text-align: center;
    align-items: center;
  }
  .footer-links { justify-content: center; }

  .back-to-top {
    bottom: 20px;
    right: 16px;
    width: 44px;
    height: 44px;
    min-height: 44px;
    font-size: 18px;
  }
}

/* --- Узкие мобильные --- */
@media (max-width: 480px) {
  .hero { padding: 40px 0 32px; }
  .hero-title { font-size: 28px; }
  .hero-desc { font-size: 14px; }
  .section-title { font-size: 22px; }
  .cta-title { font-size: 20px; }
  .cta-desc { font-size: 14px; }

  .hero-mini-badge {
    font-size: 11px;
    padding: 5px 12px;
  }

  .feature-icon {
    width: 36px;
    height: 36px;
    min-height: 36px;
    font-size: 16px;
  }
  .feature-title { font-size: 15px; }
  .feature-desc { font-size: 13px; }

  .step-card { padding: 24px 18px; }
  .step-icon {
    width: 48px;
    height: 48px;
    min-height: 48px;
    font-size: 20px;
  }
  .step-title { font-size: 16px; }
  .step-desc { font-size: 13px; }

  .rider-icon {
    width: 28px;
    height: 28px;
    min-height: 28px;
  }
  .rider-title { font-size: 13px; }
  .rider-desc { font-size: 11px; }

  .footer-cols { grid-template-columns: 1fr; }
}

/* --- Экстра-узкие --- */
@media (max-width: 400px) {
  .logo { font-size: 18px; }
  .header-actions :deep(.btn) {
    padding: 0.6rem 0.9rem;
    font-size: 13px;
  }
  .theme-toggle {
    width: 38px;
    height: 38px;
    min-height: 38px;
    font-size: 15px;
  }

  .hero-title { font-size: 26px; }
  .section-title { font-size: 20px; }
  .split-title { font-size: 19px; }
  .cta-title { font-size: 18px; }
}
</style>
