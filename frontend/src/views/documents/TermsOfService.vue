<template>
  <div class="terms-page">
    <Header
      title="Пользовательское соглашение"
    />

    <!-- Заголовок страницы -->
    <div class="page-header">
      <div class="page-header-icon">
        <i class="fas fa-file-contract"></i>
      </div>
      <div class="page-header-content">
        <h1>Пользовательское соглашение</h1>
        <p class="page-subtitle">
          Сервис <strong>MotoBind</strong> &mdash; <span class="domain">motobind.ru</span>
        </p>
        <p class="page-description">
          Дата вступления в силу: <strong>03 августа 2026 г.</strong>
        </p>
        <div class="accept-badge">
          <i class="fas fa-check-circle"></i>
          Используя Сервис, Вы подтверждаете, что ознакомились с настоящим Соглашением
          и принимаете его условия в полном объёме
        </div>
      </div>
    </div>

    <!-- Основное содержание -->
    <div class="terms-content">
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
          Настоящее Пользовательское соглашение регулирует отношения между владельцем
          сервиса <strong>MotoBind</strong> и пользователями сайта
          <a href="https://motobind.ru" target="_blank">motobind.ru</a>.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import Header from '../../components/Header.vue';

export default {
  name: 'TermsOfService',

  components: { Header },

  data() {
    return {
      showBackToTop: false,

      sections: [
        {
          id: 'terms',
          number: '1',
          title: 'Термины',
          content: `
            <dl class="terms-definitions">
              <dt><strong>Сервис</strong></dt>
              <dd>— интернет-платформа MotoBind, доступная по адресу <a href="https://motobind.ru" target="_blank">https://motobind.ru</a>.</dd>

              <dt><strong>Пользователь</strong></dt>
              <dd>— физическое лицо, использующее Сервис.</dd>

              <dt><strong>Администрация</strong></dt>
              <dd>— владелец Сервиса либо лица, уполномоченные осуществлять его поддержку и администрирование.</dd>

              <dt><strong>Аккаунт</strong></dt>
              <dd>— учётная запись Пользователя.</dd>

              <dt><strong>Контент</strong></dt>
              <dd>— любая информация, размещаемая Пользователем в Сервисе, включая текст, фотографии, мануалы, инструкции, комментарии и иные материалы.</dd>
            </dl>
          `
        },
        {
          id: 'purpose',
          number: '2',
          title: 'Назначение сервиса',
          content: `
            <p><strong>MotoBind</strong> предназначен для:</p>
            <ul>
              <li>ведения информации о мотоциклах;</li>
              <li>учёта обслуживания;</li>
              <li>хранения истории ремонтов;</li>
              <li>публикации пользовательских мануалов;</li>
              <li>обмена опытом между мотоциклистами.</li>
            </ul>
          `
        },
        {
          id: 'registration',
          number: '3',
          title: 'Регистрация',
          content: `
            <p>Для использования отдельных функций требуется регистрация.</p>
            <p>При регистрации Пользователь обязуется:</p>
            <ul>
              <li>предоставить достоверную информацию;</li>
              <li>обеспечить конфиденциальность пароля;</li>
              <li>не передавать доступ к аккаунту третьим лицам;</li>
              <li>своевременно обновлять свои данные при их изменении.</li>
            </ul>
            <div class="highlight-box warning">
              <i class="fas fa-exclamation-triangle"></i>
              <span>Пользователь самостоятельно несёт ответственность за действия, совершённые с использованием его аккаунта.</span>
            </div>
          `
        },
        {
          id: 'usage',
          number: '4',
          title: 'Использование сервиса',
          content: `
            <p>Пользователь вправе:</p>
            <div class="rights-grid">
              <div class="right-item">
                <i class="fas fa-check-circle text-success"></i>
                <span>пользоваться всеми доступными функциями</span>
              </div>
              <div class="right-item">
                <i class="fas fa-check-circle text-success"></i>
                <span>создавать мануалы</span>
              </div>
              <div class="right-item">
                <i class="fas fa-check-circle text-success"></i>
                <span>вести учёт обслуживания</span>
              </div>
              <div class="right-item">
                <i class="fas fa-check-circle text-success"></i>
                <span>добавлять мотоциклы</span>
              </div>
              <div class="right-item">
                <i class="fas fa-check-circle text-success"></i>
                <span>просматривать опубликованные материалы</span>
              </div>
            </div>
          `
        },
        {
          id: 'content',
          number: '5',
          title: 'Пользовательский контент',
          content: `
            <p>Пользователь сохраняет права на созданные им материалы.</p>
            <p>
              Размещая мануал или иной публичный контент, Пользователь предоставляет
              <strong>MotoBind</strong> неисключительное право отображать, хранить и
              распространять этот контент в рамках работы Сервиса.
            </p>
            <div class="highlight-box info">
              <i class="fas fa-info-circle"></i>
              <span>Пользователь гарантирует, что обладает необходимыми правами на публикуемые материалы.</span>
            </div>
          `
        },
        {
          id: 'prohibited',
          number: '6',
          title: 'Запрещается',
          content: `
            <p>При использовании Сервиса <strong>запрещается</strong>:</p>
            <ul class="prohibited-list">
              <li><i class="fas fa-times-circle text-danger"></i> публиковать материалы, нарушающие законодательство Российской Федерации;</li>
              <li><i class="fas fa-times-circle text-danger"></i> нарушать авторские права;</li>
              <li><i class="fas fa-times-circle text-danger"></i> размещать ложные инструкции, способные причинить вред здоровью людей или имуществу;</li>
              <li><i class="fas fa-times-circle text-danger"></i> публиковать рекламу без согласования с Администрацией;</li>
              <li><i class="fas fa-times-circle text-danger"></i> размещать вредоносное программное обеспечение;</li>
              <li><i class="fas fa-times-circle text-danger"></i> пытаться получить несанкционированный доступ к данным других пользователей;</li>
              <li><i class="fas fa-times-circle text-danger"></i> использовать автоматизированные средства для массового сбора информации;</li>
              <li><i class="fas fa-times-circle text-danger"></i> нарушать работу Сервиса.</li>
            </ul>
          `
        },
        {
          id: 'moderation',
          number: '7',
          title: 'Модерация',
          content: `
            <p>Администрация вправе:</p>
            <ul>
              <li>проверять публикуемые мануалы;</li>
              <li>отклонять материалы;</li>
              <li>отправлять материалы на доработку;</li>
              <li>удалять материалы, нарушающие настоящее Соглашение;</li>
              <li>ограничивать доступ к функционалу;</li>
              <li>временно или бессрочно блокировать аккаунты при наличии нарушений.</li>
            </ul>
            <p class="note">
              Администрация не обязана объяснять причины отклонения материалов, однако по возможности
              предоставляет рекомендации по их доработке.
            </p>
          `
        },
        {
          id: 'responsibility',
          number: '8',
          title: 'Ответственность за мануалы',
          content: `
            <p><strong>MotoBind</strong> является платформой для публикации инструкций.</p>
            <p>
              Несмотря на модерацию, Администрация не гарантирует абсолютную точность, полноту
              или актуальность всех опубликованных материалов.
            </p>
            <p>
              Перед выполнением любых ремонтных работ Пользователь обязан самостоятельно оценить
              применимость инструкции к своему мотоциклу.
            </p>
            <div class="highlight-box warning">
              <i class="fas fa-exclamation-triangle"></i>
              <span><strong>Все ремонтные работы Пользователь выполняет на свой страх и риск.</strong></span>
            </div>
            <p>Администрация <strong>не несёт ответственности</strong> за:</p>
            <ul>
              <li>ошибки в пользовательских инструкциях;</li>
              <li>последствия самостоятельного ремонта;</li>
              <li>повреждение техники;</li>
              <li>причинение вреда здоровью;</li>
              <li>финансовые убытки.</li>
            </ul>
          `
        },
        {
          id: 'availability',
          number: '9',
          title: 'Доступность сервиса',
          content: `
            <p>Администрация стремится обеспечивать бесперебойную работу <strong>MotoBind</strong>.</p>
            <p>При этом <strong>не гарантируется</strong>:</p>
            <ul>
              <li>постоянная доступность сайта;</li>
              <li>отсутствие ошибок;</li>
              <li>отсутствие технических работ;</li>
              <li>совместимость со всеми устройствами и браузерами.</li>
            </ul>
            <p class="note">
              Администрация вправе проводить техническое обслуживание без предварительного уведомления Пользователей.
            </p>
          `
        },
        {
          id: 'account-deletion',
          number: '10',
          title: 'Удаление аккаунта',
          content: `
            <p>Пользователь вправе удалить аккаунт в любое время через настройки профиля.</p>
            <p><strong>После удаления:</strong></p>
            <ul>
              <li>учётная запись удаляется;</li>
              <li>персональные данные удаляются в соответствии с Политикой конфиденциальности;</li>
              <li>восстановление удалённого аккаунта невозможно.</li>
            </ul>
          `
        },
        {
          id: 'liability',
          number: '11',
          title: 'Ограничение ответственности',
          content: `
            <p>Администрация <strong>не несёт ответственности</strong> за:</p>
            <ul>
              <li>невозможность использования Сервиса по причинам, не зависящим от неё;</li>
              <li>действия третьих лиц;</li>
              <li>потерю данных вследствие действий Пользователя;</li>
              <li>временную недоступность сайта;</li>
              <li>ущерб, возникший вследствие использования опубликованных инструкций.</li>
            </ul>
          `
        },
        {
          id: 'intellectual-property',
          number: '12',
          title: 'Интеллектуальная собственность',
          content: `
            <p>
              Дизайн, программный код, логотип <strong>MotoBind</strong>, элементы интерфейса
              и иные материалы, созданные Администрацией, являются объектами интеллектуальной собственности.
            </p>
            <div class="highlight-box warning">
              <i class="fas fa-exclamation-triangle"></i>
              <span>Их копирование, распространение и использование без письменного разрешения запрещается.</span>
            </div>
          `
        },
        {
          id: 'changes',
          number: '13',
          title: 'Изменение соглашения',
          content: `
            <p>Администрация вправе изменять настоящее Соглашение.</p>
            <p>Новая редакция публикуется на сайте и вступает в силу с момента публикации, если не указано иное.</p>
            <div class="highlight-box info">
              <i class="fas fa-info-circle"></i>
              <span>Продолжение использования Сервиса означает согласие Пользователя с новой редакцией.</span>
            </div>
          `
        },
        {
          id: 'disputes',
          number: '14',
          title: 'Разрешение споров',
          content: `
            <p>Все споры разрешаются путём переговоров.</p>
            <p>
              При невозможности урегулирования спор подлежит рассмотрению в соответствии
              с законодательством Российской Федерации.
            </p>
          `
        },
        {
          id: 'contacts',
          number: '15',
          title: 'Контактная информация',
          content: `
            <p>Владелец сервиса</p>
            <div class="contact-card operator-card">
              <div class="contact-row">
                <span class="contact-label"><i class="fas fa-user-tie"></i> ФИО:</span>
                <span class="contact-value"><strong>Апольский Григорий Михайлович</strong></span>
              </div>
              <div class="contact-row">
                <span class="contact-label"><i class="fas fa-envelope"></i> Email:</span>
                <span class="contact-value">
                  <a href="mailto:griskyy@yandex.ru">griskyy@yandex.ru</a>
                </span>
              </div>
              <div class="contact-row">
                <span class="contact-label"><i class="fas fa-globe"></i> Сайт:</span>
                <span class="contact-value">
                  <a href="https://motobind.ru" target="_blank">https://motobind.ru</a>
                </span>
              </div>
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
.terms-page {
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
  color: var(--text-primary);
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 14px;
  margin-bottom: 4px;
}

.domain {
  color: var(--accent-text);
}

.page-description {
  color: var(--text-muted);
  font-size: 15px;
  margin-bottom: 12px;
}

.accept-badge {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 8px 16px;
  background: var(--accent-trans);
  border-radius: 12px;
  color: var(--accent-text);
  font-size: 14px;
  font-weight: 500;
}

.accept-badge i {
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
  color: var(--text-primary);
}

.section-number {
  color: var(--accent-text);
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

/* --- Определения терминов --- */
.terms-definitions {
  margin: 0;
}

.terms-definitions dt {
  font-weight: 600;
  color: var(--text-primary);
  margin-top: 12px;
  margin-bottom: 4px;
}

.terms-definitions dt:first-child {
  margin-top: 0;
}

.terms-definitions dd {
  margin-left: 0;
  padding-left: 20px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.terms-definitions dd a {
  color: var(--accent-text);
  text-decoration: none;
}

.terms-definitions dd a:hover {
  text-decoration: underline;
}

/* --- Контактная карточка --- */
.contact-card {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 20px 24px;
  margin: 12px 0;
  border: 1px solid var(--border-color);
}

.operator-card {
  border-color: var(--accent-trans);
  border-width: 2px;
}

.contact-row {
  display: flex;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid var(--border-color);
}

.contact-row:last-child {
  border-bottom: none;
}

.contact-label {
  min-width: 140px;
  font-weight: 600;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 8px;
}

.contact-value {
  color: var(--text-primary);
}

.contact-value a {
  color: var(--accent-text);
  text-decoration: none;
}

.contact-value a:hover {
  text-decoration: underline;
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
  color: var(--warning-text);
}

.highlight-box.info {
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.2);
  color: var(--text-secondary);
}

.highlight-box.info i {
  color: #3B82F6;
}

/* --- Сетка прав --- */
.rights-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin: 16px 0;
}

.right-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: var(--bg-secondary);
  border-radius: 12px;
  border: 1px solid var(--border-color);
}

.right-item i {
  font-size: 18px;
  width: 24px;
  text-align: center;
  flex-shrink: 0;
}

.right-item span {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.4;
}

.text-success {
  color: var(--success-text);
}

.text-danger {
  color: var(--danger-text);
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

/* --- Важные заметки --- */
.note {
  background: var(--bg-secondary);
  padding: 12px 16px;
  border-radius: 8px;
  border-left: 3px solid var(--warning-text);
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
  color: var(--accent-text);
  text-decoration: none;
}

.legal-footer a:hover {
  text-decoration: underline;
}

/* --- Футер страницы --- */
.terms-footer {
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
  .terms-page {
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

  .rights-grid {
    grid-template-columns: 1fr;
  }

  .contact-row {
    flex-direction: column;
    gap: 4px;
  }

  .contact-label {
    min-width: unset;
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

  .accept-badge {
    font-size: 13px;
    padding: 6px 12px;
  }

  .highlight-box {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .terms-definitions dd {
    padding-left: 12px;
  }
}

/* --- Печать --- */
@media print {
  .back-to-top,
  .action-bar {
    display: none !important;
  }

  .terms-page {
    padding: 0;
    max-width: 100%;
  }

  .section-card {
    break-inside: avoid;
    border: 1px solid #ddd !important;
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
    border: 1px solid #ddd !important;
  }

  .page-header-content h1 {
    color: black !important;
  }

  .toc {
    background: white !important;
    border: 1px solid #ddd !important;
  }

  .contact-card {
    background: #f5f5f5 !important;
  }

  .highlight-box {
    background: #f5f5f5 !important;
  }

  .right-item {
    background: #f5f5f5 !important;
  }

  .accept-badge {
    background: #e8f5e9 !important;
    color: #2e7d32 !important;
  }

  .legal-footer {
    background: white !important;
  }

  .terms-definitions dt {
    color: black !important;
  }

  .terms-definitions dd {
    color: #333 !important;
  }

  .toc a,
  .terms-definitions dd a,
  .legal-footer a {
    color: #1a73e8 !important;
  }
}
</style>
