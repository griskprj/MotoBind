<template>
  <div class="landing">
    <!-- === HEADER === -->
    <header class="header">
      <div class="container header-container">
        <div class="logo">
          <span class="logo-m">Moto</span><span class="accent">Bind</span>
        </div>

        <div class="header-actions">
          <button @click="this.$router.push('/login')" class="btn-outline">Войти</button>
          <button @click="this.$router.push('/welcome')" class="btn-primary">Начать</button>
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

    <!-- === HERO SECTION === -->
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
            MotoBind — сервис для мотоциклистов, который помогает вести учет обслуживания, хранить мануалы и находить инструкции по ремонту.
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
            <button @click="this.$router.push('/welcome')" class="btn-primary big">Начать бесплатно</button>
          </div>
        </div>

        <!-- Hero Image Placeholder -->
        <div class="hero-image-wrapper">
          <div class="hero-image-placeholder">
            <img src="/16x9Auth-Bg.webp" alt="" class="landing-img">
          </div>
        </div>
      </div>
    </section>

    <!-- === FEATURES SECTION (4 cards) === -->
    <section class="section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Всё, что нужно <span class="accent">мотоциклисту</span></h2>
          <p class="section-desc">Продвинутые инструменты для ухода за мотоциклом и ведения истории обслуживания</p>
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

    <!-- === CATALOG & INTERFACE SECTION === -->
    <section class="section catalog-section">
      <div class="container">
        <div class="catalog-layout">
          <div class="catalog-left">
            <h3>Интерфейс, созданный для мотоциклистов</h3>
            <p class="interface-desc">Лёгкий дизайн, удобная навигация, всё необходимое под рукой. Создан для тех, кто ценит своё время.</p>
          </div>

          <div class="catalog-right">
            <div class="screenshot-placeholder">
              <img src="/MobileUI.webp" alt="" class="landing-img">
            </div>
          </div>
        </div>

        <div class="interface-layout">
          <div class="interface-content">
            <h3>Каталог работ</h3>
            <p class="catalog-desc">Готовые инструкции по обслуживанию и ремонту мотоциклов для разных моделей.</p>
          </div>
          <div class="interface-right">
            <div class="screenshot-placeholder big">
              <img src="/ManualsUI.webp" alt="" class="landing-img">
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- === HOW IT WORKS (3 steps) === -->
    <section class="section steps-section">
      <div class="container">
        <div class="section-header">
          <p class="mini-label">КАК ЭТО РАБОТАЕТ</p>
          <h2 class="section-title">Три простых шага <br>к идеальному порядку в гараже</h2>
        </div>

        <div class="steps-grid">
          <div class="step-card">
            <div class="step-icon"><i class="fa fa-motorcycle"></i></div>
            <div class="step-title">1. Создайте гараж</div>
            <div class="step-desc">Добавьте свои мотоциклы с ключевыми характеристиками и фото.</div>
          </div>

          <div class="step-card">
            <div class="step-icon"><i class="fa fa-calendar-check"></i></div>
            <div class="step-title">2. Планируйте и обслуживайте</div>
            <div class="step-desc">Планируйте ТО, получайте напоминания и записывайте выполненные работы.</div>
          </div>

          <div class="step-card">
            <div class="step-icon"><i class="fa fa-book"></i></div>
            <div class="step-title">3. Храните и создавайте</div>
            <div class="step-desc">Храните мануалы и создавайте свои инструкции по ремонту и обслуживанию.</div>
          </div>
        </div>
      </div>
    </section>

    <!-- === BUILD BY RIDERS === -->
    <section class="section riders-section">
      <div class="container riders-layout">
        <div class="riders-left">
          <div class="riders-image-placeholder">
            <img src="/MotorcForMotorc.webp" alt="" class="landing-img">
          </div>
        </div>
        <div class="riders-right">
          <h2 class="section-title">Создан мотоциклистами <br><span class="accent">для мотоциклистов</span></h2>
          <p class="section-desc left-align">
            Мы создали MotoBind, чтобы каждый мотоциклист мог легко управлять уходом за своим железным конём.
            Никакой сложной логистики и лишнего шума — только нужные инструменты в одном месте.
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

    <!-- === COMMUNITY (Title only, stats removed) === -->
    <section class="section community-section">
      <div class="container">
        <div class="section-header">
          <p class="mini-label">СООБЩЕСТВО</p>
          <h2 class="section-title">Доверие мотоциклистов</h2>
          <p class="section-desc">Присоединяйтесь к растущему сообществу владельцев</p>
        </div>
      </div>
    </section>

    <!-- === CTA (Footer) === -->
    <section class="cta-banner">
      <div class="container cta-layout">
        <div class="cta-left">
          <h2 class="cta-title">Готовы взять контроль <br>над своим мотоциклом?</h2>
          <p class="cta-desc">Присоединяйтесь к MotoBind и сделайте обслуживание простым и понятным.</p>
          <button @click="this.$router.push('/welcome')" class="btn-primary big">Начать бесплатно <i class="fa fa-arrow-right"></i></button>
        </div>
        <div class="cta-right">
          <div class="cta-image-placeholder">
            <img src="/MockupUI.webp" alt="" class="landing-img">
          </div>
        </div>
      </div>
    </section>

    <!-- Кнопка "Наверх" -->
    <button class="back-to-top" @click="scrollToTop" v-show="showBackToTop">
      <i class="fas fa-arrow-up"></i>
    </button>
  </div>
</template>

<script>
export default {
  name: 'Landing',

  data() {
    showBackToTop: false
  },

  mounted() {
    window.addEventListener('scroll', this.handleScroll)
  },

  beforeDestroy() {
    window.removeEventListener('scroll', this.handleScroll)
  },

  methods: {
    toggleTheme() {
      this.isDark = !this.isDark;
      const theme = this.isDark ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('theme', theme);
      
      const icon = this.$el.querySelector('.theme-toggle i');
      if (icon) {
          icon.className = this.isDark ? 'fa fa-sun' : 'fa fa-moon';
      }
    },

    handleScroll() {
      this.showBackToTop = window.scrollY > 600
    },

    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },
  }
}
</script>

<style scoped>
/* ===== Базовые стили ===== */
section {
    border: none;
    border-radius: 0px;
}

.landing {
  background-color: var(--bg-primary);
  color: var(--text-primary);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  overflow-x: hidden;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.accent {
  color: var(--accent-text);
}

/* ===== HEADER ===== */
.header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--bg-primary);
  backdrop-filter: blur(12px);
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
  font-weight: 700;
  letter-spacing: -0.5px;
}
.logo-m {
  font-weight: 900;
}

.nav {
  display: flex;
  gap: 32px;
}
.nav a {
  color: var(--text-muted);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.2s;
}
.nav a:hover {
  color: var(--text-primary);
}

.header-actions {
  display: flex;
  gap: 12px;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 20px;
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}
.btn-primary:hover {
  background: var(--accent-hover);
  transform: translateY(-2px);
}
.btn-primary.big {
  padding: 14px 28px;
  font-size: 16px;
  border-radius: 12px;
}

.btn-outline {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 20px;
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}
.btn-outline:hover {
  background: var(--border-light);
  border-color: var(--text-muted);
}

.btn-ghost {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: transparent;
  color: var(--text-secondary);
  border: none;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.2s;
}
.btn-ghost:hover {
  color: var(--text-primary);
}

/* ===== КНОПКА ПЕРЕКЛЮЧЕНИЯ ТЕМЫ ===== */
.theme-toggle {
    min-width: 45px;
    padding: 0;
    background: var(--bg-primary);
    border: 2px solid var(--border-color);
    border-radius: 50%;
    color: var(--text-primary);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    transition: all 0.3s ease;
}

.theme-toggle:hover {
    background: var(--accent);
    border-color: var(--accent);
    color: white;
    transform: rotate(30deg);
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
}

.theme-toggle:active {
    transform: rotate(60deg) scale(0.9);
}

.theme-toggle i {
    transition: transform 0.3s ease;
}

/* ===== HERO ===== */
.hero {
  padding: 80px 0 60px;
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
}

.hero-mini-badge {
  display: inline-block;
  background: var(--accent-trans);
  color: var(--accent-text);
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  margin-bottom: 20px;
  align-self: flex-start;
  border: 1px solid rgba(139, 92, 246, 0.2);
}

.hero-title {
  font-size: 52px;
  font-weight: 700;
  line-height: 1.1;
  margin: 0 0 16px 0;
  color: var(--text-primary);
}
.hero-desc {
  font-size: 16px;
  line-height: 1.6;
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
  background: var(--accent-trans);
  color: var(--accent-text);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}
.tag-title {
  font-size: 14px;
  font-weight: 600;
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

.hero-image-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}
.hero-image-placeholder {
  width: 100%;
  aspect-ratio: 4/3;
  background: var(--bg-secondary);
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  font-size: 48px;
  gap: 12px;
  text-align: center;
}
.landing-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 16px;
  display: block;
  background-color: var(--bg-secondary);
  border: 1px solid var(--border-light);
}
.hero-image-placeholder p {
  font-size: 16px;
  margin: 0;
}

/* ===== SECTIONS ===== */
.section {
  padding: 64px 0;
}

.section-header {
  text-align: center;
  margin-bottom: 48px;
}
.section-title {
  font-size: 36px;
  font-weight: 600;
  margin: 0 0 12px 0;
  line-height: 1.2;
  color: var(--text-primary);
}
.section-desc {
  color: var(--text-muted);
  font-size: 16px;
  max-width: 520px;
  margin: 0 auto;
}
.section-desc.left-align {
  max-width: 100%;
  margin: 0 0 24px 0;
}
.mini-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  letter-spacing: 1px;
  text-transform: uppercase;
  margin: 0 0 8px 0;
}

/* ===== FEATURES ===== */
.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
.feature-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s;
}
.feature-card:hover {
  background: var(--bg-card-hover);
  border-color: var(--accent-trans);
}
.feature-icon {
  width: 40px;
  height: 40px;
  background: var(--accent-trans);
  color: var(--accent-text);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  margin-bottom: 16px;
}
.feature-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-primary);
}
.feature-desc {
  font-size: 14px;
  color: var(--text-muted);
  line-height: 1.5;
}

/* ===== CATALOG & INTERFACE ===== */
.catalog-section {
  background: var(--border-light);
}

.catalog-layout {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 48px;
  align-items: center;
  margin-bottom: 64px;
}
.catalog-left h3 {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--text-primary);
}
.catalog-desc {
  font-size: 16px;
  color: var(--text-muted);
  margin-bottom: 24px;
}

.interface-layout {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 48px;
  align-items: center;
}
.interface-content h3 {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--text-primary);
}
.interface-desc {
  font-size: 16px;
  color: var(--text-muted);
  margin-bottom: 24px;
}

.screenshot-placeholder {
  width: 100%;
  aspect-ratio: 16/10;
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  font-size: 32px;
  gap: 8px;
}
.screenshot-placeholder.big {
  aspect-ratio: 21/9;
}
.screenshot-placeholder span {
  font-size: 14px;
}

/* ===== STEPS ===== */
.steps-section {
  background: var(--border-light);
}
.steps-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
}
.step-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 16px;
  padding: 32px 24px;
  text-align: center;
  transition: all 0.3s;
}
.step-card:hover {
  background: var(--bg-card-hover);
  transform: translateY(-4px);
  border-color: var(--accent-trans);
}
.step-icon {
  width: 56px;
  height: 56px;
  background: var(--accent-trans);
  color: var(--accent-text);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin: 0 auto 16px;
}
.step-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-primary);
}
.step-desc {
  font-size: 14px;
  color: var(--text-muted);
  line-height: 1.5;
}

/* ===== RIDERS ===== */
.riders-section {
  background: var(--border-light);
}
.riders-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  align-items: center;
}
.riders-image-placeholder {
  width: 100%;
  aspect-ratio: 4/3;
  background: var(--bg-secondary);
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  font-size: 48px;
  gap: 12px;
}
.riders-image-placeholder p {
  font-size: 16px;
  margin: 0;
}
.riders-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-top: 16px;
}
.rider-item {
  display: flex;
  flex-direction: column;
}
.rider-icon {
  width: 32px;
  height: 32px;
  background: var(--accent-trans);
  color: var(--accent-text);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  margin-bottom: 8px;
}
.rider-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}
.rider-desc {
  font-size: 12px;
  color: var(--text-muted);
}

/* ===== COMMUNITY ===== */
.community-section {
  background: var(--bg-primary);
}

/* ===== CTA BANNER ===== */
.cta-banner {
  padding: 64px 0;
  background: var(--bg-primary);
}
.cta-layout {
  background: var(--bg-secondary);
  border-radius: 24px;
  padding: 48px 56px;
  display: grid;
  grid-template-columns: 1fr 0.8fr;
  gap: 48px;
  align-items: center;
  border: 1px solid var(--border-color);
}
.cta-title {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 12px 0;
  color: var(--text-primary);
}
.cta-desc {
  font-size: 16px;
  color: var(--text-muted);
  margin: 0 0 24px 0;
}
.cta-image-placeholder {
  width: 100%;
  aspect-ratio: 3/4;
  background: rgba(0,0,0,0.3);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  font-size: 48px;
  gap: 8px;
  border: 1px solid var(--border-light);
}
.cta-image-placeholder p {
  font-size: 14px;
  margin: 0;
}

/* --- Кнопка "Наверх" --- */
.back-to-top {
  position: fixed;
  bottom: 80px;
  right: 24px;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  border: none;
  font-size: 20px;
  cursor: pointer;
  box-shadow: var(--shadow-lg);
  transition: all 0.3s;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
}

.back-to-top:hover {
  transform: translateY(-4px);
  background: var(--accent-hover);
}

/* ===== MEDIA QUERIES ===== */
@media (max-width: 1024px) {
  .hero-grid {
    grid-template-columns: 1fr;
    text-align: center;
  }
  .hero-content {
    align-items: center;
  }
  .hero-mini-badge {
    align-self: center;
  }
  .hero-desc {
    margin-left: auto;
    margin-right: auto;
  }
  .hero-tags {
    justify-content: center;
  }
  .features-grid {
    grid-template-columns: 1fr 1fr;
  }
  .catalog-layout,
  .interface-layout {
    grid-template-columns: 1fr;
    text-align: center;
  }
  .riders-layout {
    grid-template-columns: 1fr;
  }
  .cta-layout {
    grid-template-columns: 1fr;
    text-align: center;
    padding: 32px 24px;
  }
}

@media (max-width: 768px) {
  .nav {
    display: none;
  }
  .hero-title {
    font-size: 32px;
  }
  .features-grid {
    grid-template-columns: 1fr;
  }
  .steps-grid {
    grid-template-columns: 1fr;
    max-width: 400px;
    margin: 0 auto;
  }
  .riders-grid {
    grid-template-columns: 1fr;
  }
  .cta-title {
    font-size: 24px;
  }
}

@media (max-width: 480px) {
  .hero {
    padding: 40px 0 32px;
  }
  .hero-tags {
    flex-direction: column;
    align-items: center;
  }
  .hero-buttons {
    flex-direction: column;
    width: 100%;
  }
  .btn-primary.big, .btn-ghost {
    width: 100%;
    justify-content: center;
  }
  .cta-layout {
    padding: 24px 16px;
  }
}
</style>
