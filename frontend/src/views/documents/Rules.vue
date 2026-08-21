<template>
  <div class="rules-page">
    <!-- Хлебные крошки -->
    <div class="breadcrumbs">
      <router-link to="/home" class="breadcrumb-link">
        <i class="fas fa-home"></i> Главная
      </router-link>
      <span class="breadcrumb-separator">/</span>
      <span class="breadcrumb-current">Правила использования</span>
    </div>

    <!-- Заголовок страницы -->
    <div class="page-header">
      <div class="page-header-icon">
        <i class="fas fa-gavel"></i>
      </div>
      <div class="page-header-content">
        <h1>Правила использования сервиса</h1>
        <p class="page-subtitle">
          <strong>MotoBind</strong> &mdash; <span class="domain">motobind.ru</span>
        </p>
        <div class="welcome-message">
          <i class="fas fa-heart"></i>
          <span>Добро пожаловать в MotoBind!</span>
        </div>
        <p class="page-description">
          Мы создаём сервис для мотоциклистов, который помогает следить за обслуживанием техники,
          делиться опытом ремонта и делать эксплуатацию мотоциклов проще и безопаснее.
        </p>
        <div class="rules-badge">
          <i class="fas fa-check-circle"></i>
          Пожалуйста, соблюдайте несколько простых правил
        </div>
      </div>
    </div>

    <!-- Основное содержание -->
    <div class="rules-content">
      <!-- Оглавление -->
      <div class="toc">
        <h3><i class="fas fa-list"></i> Содержание</h3>
        <ul>
          <li v-for="section in sections" :key="section.id">
            <a :href="`#${section.id}`" @click.prevent="scrollTo(section.id)">
              {{ section.number }}. {{ section.title }}
            </a>
          </li>
        </ul>
      </div>

      <!-- Разделы -->
      <div class="sections">
        <div
          v-for="section in sections"
          :key="section.id"
          :id="section.id"
          class="section-card"
        >
          <h2>
            <span class="section-number">{{ section.number }}</span>
            {{ section.title }}
          </h2>

          <div v-if="section.subsections" class="subsection">
            <div
              v-for="sub in section.subsections"
              :key="sub.id"
              class="subsection-item"
            >
              <h3>{{ sub.number }}. {{ sub.title }}</h3>
              <div class="subsection-content" v-html="sub.content"></div>
            </div>
          </div>

          <div v-else class="section-content" v-html="section.content"></div>
        </div>
      </div>

      <!-- Благодарность -->
      <div class="thanks-block">
        <div class="thanks-icon">
          <i class="fas fa-heart"></i>
        </div>
        <div class="thanks-text">
          <h3>Спасибо ❤️</h3>
          <p>
            <strong>MotoBind</strong> создаётся одним разработчиком не как очередная социальная сеть,
            а как полезный инструмент для мотоциклистов.
          </p>
          <p>
            Если у Вас есть идеи по развитию сервиса, предложения по улучшению или Вы нашли ошибку —
            обязательно напишите. Любая обратная связь помогает сделать <strong>MotoBind</strong>
            лучше для всего сообщества.
          </p>
          <div class="thanks-contact">
            <a href="mailto:griskyy@yandex.ru">
              <i class="fas fa-envelope"></i> griskyy@yandex.ru
            </a>
          </div>
        </div>
      </div>

      <!-- Кнопка "Наверх" -->
      <button class="back-to-top" @click="scrollToTop" v-show="showBackToTop">
        <i class="fas fa-arrow-up"></i>
      </button>

      <!-- Печать и скачивание -->
      <div class="action-bar">
        <button class="action-btn print-btn" @click="printPage">
          <i class="fas fa-print"></i> Распечатать
        </button>
        <button class="action-btn download-btn" @click="downloadPDF">
          <i class="fas fa-file-pdf"></i> Скачать PDF
        </button>
      </div>

      <!-- Юридический блок -->
      <div class="legal-footer">
        <p>
          <i class="fas fa-gavel"></i>
          Настоящие Правила являются неотъемлемой частью
          <router-link to="/terms">Пользовательского соглашения</router-link>
          и <router-link to="/privacy">Политики конфиденциальности</router-link>
          сервиса <strong>MotoBind</strong>.
        </p>
      </div>
    </div>
  </div>
</template>

<head>
  <title>MotoBind — Правила использования | Условия сервиса</title>
  <meta name="description" content="Правила использования сервиса MotoBind. Ознакомьтесь с условиями перед началом работы.">
</head>

<script>
export default {
  name: 'Rules',

  data() {
    return {
      showBackToTop: false,

      sections: [
        {
          id: 'general',
          number: '1',
          title: 'Общие положения',
          content: `
            <p>
              Используя <strong>MotoBind</strong>, Вы соглашаетесь соблюдать настоящие Правила,
              <router-link to="/terms">Пользовательское соглашение</router-link> и
              <router-link to="/privacy">Политику конфиденциальности</router-link>.
            </p>
            <div class="highlight-box warning">
              <i class="fas fa-exclamation-triangle"></i>
              <span>
                Если какое-либо из правил нарушается, Администрация вправе ограничить доступ
                к отдельным функциям или аккаунту.
              </span>
            </div>
          `
        },
        {
          id: 'respect',
          number: '2',
          title: 'Уважайте других пользователей',
          content: `
            <p>В сервисе <strong>запрещается</strong>:</p>
            <ul class="prohibited-list">
              <li><i class="fas fa-times-circle text-danger"></i> оскорблять других пользователей;</li>
              <li><i class="fas fa-times-circle text-danger"></i> унижать достоинство людей;</li>
              <li><i class="fas fa-times-circle text-danger"></i> разжигать ненависть;</li>
              <li><i class="fas fa-times-circle text-danger"></i> угрожать;</li>
              <li><i class="fas fa-times-circle text-danger"></i> публиковать материалы, нарушающие законодательство Российской Федерации.</li>
            </ul>
            <div class="highlight-box info">
              <i class="fas fa-heart"></i>
              <span>Мы хотим, чтобы MotoBind оставался дружелюбным сообществом для всех мотоциклистов.</span>
            </div>
          `
        },
        {
          id: 'manuals',
          number: '3',
          title: 'Создание мануалов',
          content: `
            <p>Перед публикацией убедитесь, что инструкция:</p>
            <ul>
              <li>соответствует теме ремонта или обслуживания мотоциклов;</li>
              <li>содержит достоверную информацию;</li>
              <li>написана понятным языком;</li>
              <li>не вводит пользователей в заблуждение.</li>
            </ul>
            <p>По возможности <strong>рекомендуем</strong>:</p>
            <div class="tips-grid">
              <div class="tip-item">
                <i class="fas fa-camera"></i>
                <span>добавлять фотографии</span>
              </div>
              <div class="tip-item">
                <i class="fas fa-list-ol"></i>
                <span>использовать пошаговое описание</span>
              </div>
              <div class="tip-item">
                <i class="fas fa-tools"></i>
                <span>перечислять необходимые инструменты</span>
              </div>
              <div class="tip-item">
                <i class="fas fa-box"></i>
                <span>указывать расходные материалы</span>
              </div>
              <div class="tip-item">
                <i class="fas fa-exclamation-triangle"></i>
                <span>предупреждать о сложных или опасных этапах</span>
              </div>
            </div>
          `
        },
        {
          id: 'prohibited',
          number: '4',
          title: 'Запрещённый контент',
          content: `
            <p>Запрещается публиковать:</p>
            <ul class="prohibited-list">
              <li><i class="fas fa-times-circle text-danger"></i> заведомо ложные инструкции;</li>
              <li><i class="fas fa-times-circle text-danger"></i> материалы, способные причинить вред здоровью или имуществу;</li>
              <li><i class="fas fa-times-circle text-danger"></i> рекламу без согласования с Администрацией;</li>
              <li><i class="fas fa-times-circle text-danger"></i> спам;</li>
              <li><i class="fas fa-times-circle text-danger"></i> вредоносные ссылки;</li>
              <li><i class="fas fa-times-circle text-danger"></i> материалы, нарушающие авторские права;</li>
              <li><i class="fas fa-times-circle text-danger"></i> контент, не относящийся к тематике MotoBind.</li>
            </ul>
          `
        },
        {
          id: 'moderation',
          number: '5',
          title: 'Модерация',
          content: `
            <p>Все опубликованные мануалы могут проходить модерацию.</p>
            <p>По результатам проверки Администрация вправе:</p>
            <ul>
              <li>одобрить публикацию;</li>
              <li>отклонить мануал;</li>
              <li>отправить его на доработку;</li>
              <li>удалить уже опубликованный материал при обнаружении нарушений.</li>
            </ul>
            <p class="note">Решение модератора принимается с целью поддержания качества контента.</p>
          `
        },
        {
          id: 'copyright',
          number: '6',
          title: 'Авторские права',
          content: `
            <p>Публикуя материалы в <strong>MotoBind</strong>, Вы подтверждаете, что:</p>
            <ul>
              <li>являетесь автором опубликованного контента либо имеете право его использовать;</li>
              <li>не нарушаете права третьих лиц;</li>
              <li>несёте ответственность за опубликованные материалы.</li>
            </ul>
            <div class="highlight-box info">
              <i class="fas fa-info-circle"></i>
              <span>
                При использовании чужих изображений, схем или текста необходимо иметь
                соответствующее разрешение либо соблюдать условия лицензии.
              </span>
            </div>
          `
        },
        {
          id: 'safety',
          number: '7',
          title: 'Безопасность ремонта',
          content: `
            <p>
              <strong>MotoBind</strong> предоставляет инструкции исключительно в информационных целях.
            </p>
            <p><strong>Перед выполнением ремонта:</strong></p>
            <ul>
              <li>убедитесь, что инструкция подходит именно для Вашего мотоцикла;</li>
              <li>соблюдайте рекомендации производителя;</li>
              <li>используйте исправный инструмент;</li>
              <li>соблюдайте технику безопасности.</li>
            </ul>
            <div class="highlight-box warning">
              <i class="fas fa-exclamation-triangle"></i>
              <span>
                <strong>Администрация не несёт ответственности за последствия самостоятельного ремонта.</strong>
              </span>
            </div>
          `
        },
        {
          id: 'account',
          number: '8',
          title: 'Использование аккаунта',
          content: `
            <p><strong>Запрещается:</strong></p>
            <ul class="prohibited-list">
              <li><i class="fas fa-times-circle text-danger"></i> передавать аккаунт третьим лицам;</li>
              <li><i class="fas fa-times-circle text-danger"></i> использовать чужие учётные записи;</li>
              <li><i class="fas fa-times-circle text-danger"></i> создавать аккаунты для обхода блокировки;</li>
              <li><i class="fas fa-times-circle text-danger"></i> пытаться получить доступ к чужим данным;</li>
              <li><i class="fas fa-times-circle text-danger"></i> вмешиваться в работу Сервиса.</li>
            </ul>
            <p class="note">Пользователь самостоятельно отвечает за сохранность своих данных для входа.</p>
          `
        },
        {
          id: 'violations',
          number: '9',
          title: 'Нарушение правил',
          content: `
            <p>За нарушение настоящих Правил Администрация вправе:</p>
            <ul>
              <li>вынести предупреждение;</li>
              <li>ограничить отдельные функции аккаунта;</li>
              <li>удалить опубликованный материал;</li>
              <li>временно заблокировать аккаунт;</li>
              <li>полностью удалить аккаунт при систематических или грубых нарушениях.</li>
            </ul>
            <p class="note">Мера воздействия определяется Администрацией исходя из характера нарушения.</p>
          `
        },
        {
          id: 'feedback',
          number: '10',
          title: 'Сообщение об ошибках',
          content: `
            <p>Если Вы:</p>
            <ul>
              <li>нашли ошибку;</li>
              <li>обнаружили некорректный мануал;</li>
              <li>заметили нарушение Правил;</li>
              <li>нашли уязвимость;</li>
            </ul>
            <p>сообщите об этом на:</p>
            <div class="contact-email">
              <a href="mailto:griskyy@yandex.ru">
                <i class="fas fa-envelope"></i> griskyy@yandex.ru
              </a>
            </div>
            <div class="highlight-box info">
              <i class="fas fa-heart"></i>
              <span>Мы будем благодарны за любую обратную связь.</span>
            </div>
          `
        },
        {
          id: 'changes',
          number: '11',
          title: 'Изменение правил',
          content: `
            <p>Администрация вправе изменять настоящие Правила.</p>
            <p>Актуальная версия всегда доступна на сайте <a href="https://motobind.ru" target="_blank">https://motobind.ru</a>.</p>
            <div class="highlight-box info">
              <i class="fas fa-info-circle"></i>
              <span>
                Продолжение использования Сервиса после публикации новой редакции означает
                согласие Пользователя с внесёнными изменениями.
              </span>
            </div>
          `
        }
      ]
    }
  },

  mounted() {
    window.addEventListener('scroll', this.handleScroll)
  },

  beforeDestroy() {
    window.removeEventListener('scroll', this.handleScroll)
  },

  methods: {
    scrollTo(id) {
      const element = document.getElementById(id)
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    },

    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },

    handleScroll() {
      this.showBackToTop = window.scrollY > 600
    },

    printPage() {
      window.print()
    },

    downloadPDF() {
      window.print()
    }
  }
}
</script>

<style scoped>
/* --- Общие стили страницы --- */
.rules-page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px 20px 40px;
  animation: slideInUp 0.4s ease-out;
}

/* --- Хлебные крошки --- */
.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--text-muted);
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.breadcrumb-link {
  color: var(--text-secondary);
  text-decoration: none;
  transition: color 0.2s;
}

.breadcrumb-link:hover {
  color: var(--accent);
  text-decoration: none;
}

.breadcrumb-separator {
  color: var(--text-muted);
}

.breadcrumb-current {
  color: var(--text-primary);
  font-weight: 500;
}

/* --- Заголовок страницы --- */
.page-header {
  display: flex;
  align-items: flex-start;
  gap: 24px;
  margin-bottom: 40px;
  padding: 32px;
  background: var(--bg-card);
  border-radius: 24px;
  border: 1px solid var(--border-color);
}

.page-header-icon {
  flex-shrink: 0;
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--accent-trans);
  border-radius: 16px;
  font-size: 32px;
  color: var(--accent);
}

.page-header-content h1 {
  margin-bottom: 4px;
  font-size: 28px;
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 14px;
  margin-bottom: 8px;
}

.domain {
  color: var(--accent);
}

.welcome-message {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 6px 16px;
  background: var(--success-trans);
  border-radius: 20px;
  color: var(--success);
  font-weight: 600;
  font-size: 15px;
  margin-bottom: 10px;
}

.welcome-message i {
  font-size: 16px;
}

.page-description {
  color: var(--text-secondary);
  font-size: 15px;
  line-height: 1.6;
  margin-bottom: 12px;
}

.rules-badge {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 8px 16px;
  background: var(--accent-trans);
  border-radius: 12px;
  color: var(--accent);
  font-size: 14px;
  font-weight: 500;
}

.rules-badge i {
  font-size: 18px;
}

/* --- Оглавление --- */
.toc {
  background: var(--bg-card);
  border-radius: 16px;
  padding: 20px 24px;
  margin-bottom: 32px;
  border: 1px solid var(--border-color);
}

.toc h3 {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  color: var(--text-secondary);
  margin-bottom: 12px;
}

.toc ul {
  list-style: none;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px 24px;
  padding: 0;
}

.toc li {
  font-size: 14px;
}

.toc a {
  color: var(--text-secondary);
  text-decoration: none;
  transition: color 0.2s;
  cursor: pointer;
}

.toc a:hover {
  color: var(--accent);
  text-decoration: none;
}

/* --- Секции --- */
.sections {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.section-card {
  background: var(--bg-card);
  border-radius: 16px;
  padding: 28px 32px;
  border: 1px solid var(--border-color);
  transition: border-color 0.2s;
  scroll-margin-top: 80px;
}

.section-card:hover {
  border-color: var(--accent-trans);
}

.section-card h2 {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 22px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 2px solid var(--border-color);
}

.section-number {
  color: var(--accent);
  font-weight: 700;
}

.section-content {
  color: var(--text-secondary);
  line-height: 1.8;
  font-size: 15px;
}

.section-content p {
  margin-bottom: 12px;
}

.section-content ul,
.section-content ol {
  padding-left: 24px;
  margin-bottom: 12px;
}

.section-content li {
  margin-bottom: 6px;
}

.section-content strong {
  color: var(--text-primary);
}

.section-content a {
  color: var(--accent);
  text-decoration: none;
}

.section-content a:hover {
  text-decoration: underline;
}

/* --- Подсекции --- */
.subsection {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.subsection-item {
  padding-left: 4px;
}

.subsection-item h3 {
  font-size: 18px;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.subsection-content {
  color: var(--text-secondary);
  line-height: 1.8;
  font-size: 15px;
}

.subsection-content ul,
.subsection-content ol {
  padding-left: 24px;
  margin-bottom: 12px;
}

.subsection-content li {
  margin-bottom: 6px;
}

/* --- Сетка советов --- */
.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
  margin: 12px 0 4px;
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  background: var(--bg-secondary);
  border-radius: 10px;
  border: 1px solid var(--border-color);
}

.tip-item i {
  color: var(--accent);
  font-size: 16px;
  width: 24px;
  text-align: center;
  flex-shrink: 0;
}

.tip-item span {
  font-size: 14px;
  color: var(--text-secondary);
}

/* --- Запрещённые действия --- */
.prohibited-list {
  list-style: none !important;
  padding-left: 0 !important;
}

.prohibited-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 0;
}

.text-danger {
  color: var(--danger);
}

/* --- Highlight Boxes --- */
.highlight-box {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px 20px;
  border-radius: 12px;
  margin: 16px 0;
  font-size: 14px;
  line-height: 1.6;
}

.highlight-box i {
  font-size: 20px;
  flex-shrink: 0;
  margin-top: 2px;
}

.highlight-box.warning {
  background: var(--warning-trans);
  border: 1px solid rgba(245, 158, 11, 0.3);
  color: var(--text-secondary);
}

.highlight-box.warning i {
  color: var(--warning);
}

.highlight-box.info {
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.2);
  color: var(--text-secondary);
}

.highlight-box.info i {
  color: #3B82F6;
}

/* --- Контактный email --- */
.contact-email {
  margin: 12px 0 4px;
}

.contact-email a {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  background: var(--accent-trans);
  border-radius: 12px;
  color: var(--accent);
  font-size: 16px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s;
}

.contact-email a:hover {
  background: var(--accent);
  color: white;
  text-decoration: none;
}

/* --- Благодарность --- */
.thanks-block {
  display: flex;
  gap: 24px;
  padding: 32px;
  margin-top: 32px;
  background: var(--bg-card);
  border-radius: 16px;
  border: 2px solid var(--accent-trans);
  align-items: flex-start;
}

.thanks-icon {
  flex-shrink: 0;
  font-size: 48px;
  color: var(--danger);
}

.thanks-text h3 {
  font-size: 24px;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.thanks-text p {
  color: var(--text-secondary);
  line-height: 1.8;
  margin-bottom: 12px;
}

.thanks-text strong {
  color: var(--text-primary);
}

.thanks-contact {
  margin-top: 12px;
}

.thanks-contact a {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  background: var(--accent-trans);
  border-radius: 12px;
  color: var(--accent);
  font-size: 16px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s;
}

.thanks-contact a:hover {
  background: var(--accent);
  color: white;
  text-decoration: none;
}

/* --- Важные заметки --- */
.note {
  background: var(--bg-secondary);
  padding: 12px 16px;
  border-radius: 8px;
  border-left: 3px solid var(--warning);
  color: var(--text-secondary);
  font-size: 14px;
  margin-top: 12px;
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
  color: white;
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

/* --- Панель действий --- */
.action-bar {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 32px;
  flex-wrap: wrap;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  background: var(--bg-card);
  color: var(--text-secondary);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background: var(--bg-secondary);
  border-color: var(--accent);
  color: var(--text-primary);
}

.action-btn i {
  font-size: 16px;
}

/* --- Юридический футер --- */
.legal-footer {
  margin-top: 40px;
  padding: 20px 24px;
  background: var(--bg-card);
  border-radius: 16px;
  border: 1px solid var(--border-color);
  text-align: center;
}

.legal-footer p {
  color: var(--text-secondary);
  font-size: 14px;
  margin: 0;
  line-height: 1.6;
}

.legal-footer i {
  color: var(--accent);
  margin-right: 8px;
}

.legal-footer strong {
  color: var(--text-primary);
}

.legal-footer a {
  color: var(--accent);
  text-decoration: none;
}

.legal-footer a:hover {
  text-decoration: underline;
}

/* --- Футер страницы --- */
.rules-footer {
  margin-top: 40px;
  padding-top: 24px;
  border-top: 1px solid var(--border-color);
  text-align: center;
}

.footer-links {
  display: flex;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}

.footer-links a {
  color: var(--text-muted);
  text-decoration: none;
  font-size: 14px;
  transition: color 0.2s;
}

.footer-links a:hover {
  color: var(--accent);
  text-decoration: none;
}

.footer-links .divider {
  color: var(--border-color);
}

.copyright {
  color: var(--text-muted);
  font-size: 13px;
  margin: 0;
}

/* --- Адаптивность --- */
@media (max-width: 992px) {
  .rules-page {
    padding: 16px 12px 32px;
  }

  .page-header {
    padding: 24px;
  }

  .section-card {
    padding: 20px;
  }

  .toc ul {
    grid-template-columns: 1fr;
  }

  .thanks-block {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .tips-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 640px) {
  .page-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 20px;
  }

  .page-header h1 {
    font-size: 22px;
  }

  .section-card h2 {
    font-size: 18px;
  }

  .subsection-item h3 {
    font-size: 16px;
  }

  .back-to-top {
    bottom: 70px;
    right: 16px;
    width: 44px;
    height: 44px;
    font-size: 18px;
  }

  .action-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .action-btn {
    justify-content: center;
  }

  .rules-badge {
    font-size: 13px;
    padding: 6px 12px;
  }

  .welcome-message {
    font-size: 13px;
    padding: 4px 12px;
  }

  .highlight-box {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .tips-grid {
    grid-template-columns: 1fr;
  }

  .thanks-block {
    padding: 20px;
  }

  .contact-email a,
  .thanks-contact a {
    width: 100%;
    justify-content: center;
  }
}

/* --- Печать --- */
@media print {
  .back-to-top,
  .action-bar {
    display: none !important;
  }

  .rules-page {
    padding: 0;
    max-width: 100%;
  }

  .section-card {
    break-inside: avoid;
    border: 1px solid #ddd;
    background: white !important;
    color: black !important;
  }

  .section-card h2,
  .section-content,
  .subsection-content {
    color: black !important;
  }

  .page-header {
    background: white !important;
    border: 1px solid #ddd;
  }

  .toc {
    background: white !important;
    border: 1px solid #ddd;
  }

  .highlight-box {
    background: #f5f5f5 !important;
  }

  .tip-item {
    background: #f5f5f5 !important;
  }

  .rules-badge {
    background: #e8f5e9 !important;
    color: #2e7d32 !important;
  }

  .welcome-message {
    background: #e8f5e9 !important;
    color: #2e7d32 !important;
  }

  .legal-footer {
    background: white !important;
  }

  .thanks-block {
    border-color: #ddd !important;
    background: white !important;
  }

  .contact-email a,
  .thanks-contact a {
    background: #f5f5f5 !important;
    color: #333 !important;
  }
}
</style>
