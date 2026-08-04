<template>
  <div class="consent-page">
    <!-- Хлебные крошки -->
    <div class="breadcrumbs">
      <router-link to="/home" class="breadcrumb-link">
        <i class="fas fa-home"></i> Главная
      </router-link>
      <span class="breadcrumb-separator">/</span>
      <span class="breadcrumb-current">Согласие на обработку персональных данных</span>
    </div>

    <!-- Заголовок страницы -->
    <div class="page-header">
      <div class="page-header-icon">
        <i class="fas fa-handshake"></i>
      </div>
      <div class="page-header-content">
        <h1>Согласие на обработку персональных данных</h1>
        <p class="page-subtitle">
          Сервис <strong>MotoBind</strong> &mdash; <span class="domain">motobind.ru</span>
        </p>
        <p class="page-description">
          Дата вступления в силу: <strong>03 августа 2026 г.</strong>
        </p>
        <div class="accept-badge">
          <i class="fas fa-check-circle"></i>
          Регистрируясь и используя Сервис, Вы выражаете согласие на обработку
          персональных данных на условиях настоящего документа
        </div>
      </div>
    </div>

    <!-- Основное содержание -->
    <div class="consent-content">
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

      <!-- Преамбула -->
      <div class="preamble">
        <p>
          Настоящим, регистрируясь и используя сервис <strong>MotoBind</strong>,
          расположенный по адресу <a href="https://motobind.ru" target="_blank">https://motobind.ru</a>,
          я свободно, своей волей и в своём интересе выражаю согласие оператору
          персональных данных — <strong>Апольскому Григорию Михайловичу</strong> —
          на обработку моих персональных данных в соответствии с Федеральным законом
          Российской Федерации от 27.07.2006 № 152-ФЗ «О персональных данных».
        </p>
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

      <!-- Подтверждение -->
      <div class="confirmation-block">
        <div class="confirmation-icon">
          <i class="fas fa-check-circle"></i>
        </div>
        <div class="confirmation-text">
          <h3>Я подтверждаю, что:</h3>
          <ul>
            <li>ознакомился(ась) с <router-link to="/privacy">Политикой конфиденциальности</router-link> MotoBind;</li>
            <li>ознакомился(ась) с <router-link to="/terms">Пользовательским соглашением</router-link> MotoBind;</li>
            <li>понимаю цели обработки моих персональных данных;</li>
            <li>предоставляю персональные данные добровольно;</li>
            <li>подтверждаю достоверность предоставленных сведений;</li>
            <li>выражаю согласие на обработку моих персональных данных на условиях настоящего документа.</li>
          </ul>
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
          <i class="fas fa-balance-scale"></i>
          Настоящее Согласие регулирует обработку персональных данных пользователей
          сервиса <strong>MotoBind</strong> в соответствии с Федеральным законом
          № 152-ФЗ «О персональных данных».
        </p>
      </div>
    </div>

    <!-- Футер с ссылками -->
    <div class="consent-footer">
      <div class="footer-links">
        <router-link to="/home">Главная</router-link>
        <span class="divider">|</span>
        <router-link to="/privacy">Политика конфиденциальности</router-link>
        <span class="divider">|</span>
        <router-link to="/terms">Пользовательское соглашение</router-link>
        <span class="divider">|</span>
        <a href="mailto:griskyy@yandex.ru">Поддержка</a>
      </div>
      <p class="copyright">© 2026 MotoBind. Все права защищены.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Consent',

  data() {
    return {
      showBackToTop: false,

      sections: [
        {
          id: 'operator',
          number: '1',
          title: 'Оператор персональных данных',
          content: `
            <p>Оператор персональных данных:</p>
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
        },
        {
          id: 'personal-data',
          number: '2',
          title: 'Персональные данные, на обработку которых даётся согласие',
          content: `
            <p>Я соглашаюсь на обработку следующих персональных данных, которые самостоятельно предоставляю при использовании Сервиса.</p>
          `,
          subsections: [
            {
              id: 'personal-data-account',
              number: '2.1',
              title: 'Учётная запись',
              content: `
                <ul>
                  <li>имя пользователя (логин);</li>
                  <li>адрес электронной почты;</li>
                  <li>пароль (в зашифрованном виде);</li>
                  <li>фотография профиля (при наличии).</li>
                </ul>
              `
            },
            {
              id: 'personal-data-moto',
              number: '2.2',
              title: 'Информация о мотоциклах',
              content: `
                <ul>
                  <li>марка;</li>
                  <li>модель;</li>
                  <li>год выпуска;</li>
                  <li>объем двигателя;</li>
                  <li>пробег;</li>
                  <li>цвет;</li>
                  <li>государственный регистрационный номер;</li>
                  <li>VIN-код;</li>
                  <li>пользовательские заметки.</li>
                </ul>
              `
            },
            {
              id: 'personal-data-maintenance',
              number: '2.3',
              title: 'Информация об обслуживании',
              content: `
                <ul>
                  <li>проведенные обслуживания;</li>
                  <li>запланированные обслуживания;</li>
                  <li>стоимость обслуживания;</li>
                  <li>категории работ;</li>
                  <li>пробег на момент обслуживания;</li>
                  <li>история обслуживания.</li>
                </ul>
              `
            },
            {
              id: 'personal-data-content',
              number: '2.4',
              title: 'Пользовательский контент',
              content: `
                <ul>
                  <li>созданные мануалы;</li>
                  <li>инструкции по ремонту;</li>
                  <li>комментарии (если функционал предусмотрен);</li>
                  <li>иные материалы, добровольно размещенные мной в Сервисе.</li>
                </ul>
              `
            },
            {
              id: 'personal-data-other',
              number: '2.5',
              title: 'Иные сведения',
              content: `
                <p>Любая информация, которую я добровольно ввожу при использовании функционала MotoBind.</p>
              `
            }
          ]
        },
        {
          id: 'purposes',
          number: '3',
          title: 'Цели обработки персональных данных',
          content: `
            <p>Персональные данные обрабатываются исключительно для:</p>
            <ul>
              <li>регистрации и авторизации Пользователя;</li>
              <li>предоставления доступа к функционалу MotoBind;</li>
              <li>хранения информации о мотоциклах;</li>
              <li>ведения истории обслуживания;</li>
              <li>отображения статистики;</li>
              <li>публикации пользовательских мануалов;</li>
              <li>обеспечения работы Сервиса;</li>
              <li>исполнения требований законодательства Российской Федерации.</li>
            </ul>
          `
        },
        {
          id: 'actions',
          number: '4',
          title: 'Действия с персональными данными',
          content: `
            <p>Я соглашаюсь на осуществление следующих действий с моими персональными данными:</p>
            <div class="actions-grid">
              <div class="action-item">
                <i class="fas fa-database"></i>
                <span>сбор</span>
              </div>
              <div class="action-item">
                <i class="fas fa-pen"></i>
                <span>запись</span>
              </div>
              <div class="action-item">
                <i class="fas fa-layer-group"></i>
                <span>систематизация</span>
              </div>
              <div class="action-item">
                <i class="fas fa-boxes"></i>
                <span>накопление</span>
              </div>
              <div class="action-item">
                <i class="fas fa-archive"></i>
                <span>хранение</span>
              </div>
              <div class="action-item">
                <i class="fas fa-sync-alt"></i>
                <span>уточнение (обновление, изменение)</span>
              </div>
              <div class="action-item">
                <i class="fas fa-play"></i>
                <span>использование</span>
              </div>
              <div class="action-item">
                <i class="fas fa-user-secret"></i>
                <span>обезличивание (при необходимости)</span>
              </div>
              <div class="action-item">
                <i class="fas fa-trash-alt"></i>
                <span>удаление</span>
              </div>
              <div class="action-item">
                <i class="fas fa-skull"></i>
                <span>уничтожение</span>
              </div>
            </div>
            <p class="note">
              Обработка может осуществляться как автоматизированным способом, так и без использования средств автоматизации.
            </p>
          `
        },
        {
          id: 'transfer',
          number: '5',
          title: 'Передача персональных данных',
          content: `
            <p>Мои персональные данные:</p>
            <ul>
              <li><strong>не продаются;</strong></li>
              <li><strong>не передаются третьим лицам;</strong></li>
              <li><strong>не используются в рекламных целях.</strong></li>
            </ul>
            <p>Исключение составляют случаи, прямо предусмотренные законодательством Российской Федерации.</p>
            <div class="highlight-box success">
              <i class="fas fa-shield-alt"></i>
              <span>Ваши данные в безопасности. Мы не передаём их никому.</span>
            </div>
          `
        },
        {
          id: 'analytics',
          number: '6',
          title: 'Аналитика и отслеживание',
          content: `
            <p><strong>MotoBind:</strong></p>
            <ul class="not-collect-list">
              <li><i class="fas fa-times-circle text-danger"></i> не использует рекламные системы;</li>
              <li><i class="fas fa-times-circle text-danger"></i> не использует системы веб-аналитики;</li>
              <li><i class="fas fa-times-circle text-danger"></i> не собирает статистику поведения Пользователей;</li>
              <li>
                <i class="fas fa-times-circle text-danger"></i> не ведёт журналы пользовательской активности,
                за исключением технической информации, необходимой для обеспечения работы Сервиса.
              </li>
            </ul>
          `
        },
        {
          id: 'term',
          number: '7',
          title: 'Срок обработки персональных данных',
          content: `
            <p>
              Персональные данные обрабатываются до момента удаления учётной записи
              Пользователем либо до отзыва настоящего согласия, если иное не предусмотрено
              законодательством Российской Федерации.
            </p>
            <div class="highlight-box warning">
              <i class="fas fa-exclamation-triangle"></i>
              <span>После удаления аккаунта персональные данные удаляются безвозвратно.</span>
            </div>
          `
        },
        {
          id: 'withdrawal',
          number: '8',
          title: 'Отзыв согласия',
          content: `
            <p>Я вправе в любой момент отозвать настоящее согласие.</p>
            <p>Для этого необходимо:</p>
            <ul>
              <li>удалить учётную запись самостоятельно через настройки профиля;</li>
              <li>либо направить обращение по адресу:</li>
            </ul>
            <div class="contact-email">
              <a href="mailto:griskyy@yandex.ru">
                <i class="fas fa-envelope"></i> griskyy@yandex.ru
              </a>
            </div>
            <p>
              После получения обращения персональные данные будут удалены в сроки,
              предусмотренные законодательством Российской Федерации.
            </p>
          `
        },
        {
          id: 'confirmation',
          number: '9',
          title: 'Подтверждение согласия',
          content: `
            <p>Я подтверждаю, что:</p>
            <ul>
              <li>ознакомился(ась) с <router-link to="/privacy">Политикой конфиденциальности</router-link> MotoBind;</li>
              <li>ознакомился(ась) с <router-link to="/terms">Пользовательским соглашением</router-link> MotoBind;</li>
              <li>понимаю цели обработки моих персональных данных;</li>
              <li>предоставляю персональные данные добровольно;</li>
              <li>подтверждаю достоверность предоставленных сведений;</li>
              <li>выражаю согласие на обработку моих персональных данных на условиях настоящего документа.</li>
            </ul>
            <div class="highlight-box info">
              <i class="fas fa-check-circle"></i>
              <span>Настоящее Согласие действует до момента его отзыва или удаления учётной записи.</span>
            </div>
          `
        },
        {
          id: 'contacts',
          number: '10',
          title: 'Контактная информация',
          content: `
            <p>Оператор персональных данных</p>
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
.consent-page {
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
  margin-bottom: 4px;
}

.domain {
  color: var(--accent);
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
  color: var(--accent);
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

/* --- Преамбула --- */
.preamble {
  background: var(--bg-card);
  border-radius: 16px;
  padding: 24px 32px;
  margin-bottom: 32px;
  border: 2px solid var(--accent-trans);
  font-size: 16px;
  line-height: 1.8;
  color: var(--text-secondary);
}

.preamble strong {
  color: var(--text-primary);
}

.preamble a {
  color: var(--accent);
  text-decoration: none;
}

.preamble a:hover {
  text-decoration: underline;
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
  color: var(--accent);
  text-decoration: none;
}

.contact-value a:hover {
  text-decoration: underline;
}

/* --- Сетка действий --- */
.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 10px;
  margin: 16px 0;
}

.action-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  background: var(--bg-secondary);
  border-radius: 10px;
  border: 1px solid var(--border-color);
}

.action-item i {
  color: var(--accent);
  font-size: 16px;
  width: 24px;
  text-align: center;
  flex-shrink: 0;
}

.action-item span {
  font-size: 14px;
  color: var(--text-secondary);
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

.highlight-box.success {
  background: var(--success-trans);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: var(--text-secondary);
}

.highlight-box.success i {
  color: var(--success);
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

/* --- Not collect list --- */
.not-collect-list {
  list-style: none !important;
  padding-left: 0 !important;
}

.not-collect-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 0;
}

.text-danger {
  color: var(--danger);
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

/* --- Блок подтверждения --- */
.confirmation-block {
  display: flex;
  gap: 24px;
  padding: 32px;
  margin-top: 32px;
  background: var(--bg-card);
  border-radius: 16px;
  border: 2px solid var(--success);
  align-items: flex-start;
}

.confirmation-icon {
  flex-shrink: 0;
  font-size: 48px;
  color: var(--success);
}

.confirmation-text h3 {
  font-size: 18px;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.confirmation-text ul {
  padding-left: 24px;
  color: var(--text-secondary);
  line-height: 2;
}

.confirmation-text ul li {
  margin-bottom: 4px;
}

.confirmation-text ul li a {
  color: var(--accent);
  text-decoration: none;
}

.confirmation-text ul li a:hover {
  text-decoration: underline;
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
.consent-footer {
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
  .consent-page {
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

  .contact-row {
    flex-direction: column;
    gap: 4px;
  }

  .contact-label {
    min-width: unset;
  }

  .confirmation-block {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .actions-grid {
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

  .accept-badge {
    font-size: 13px;
    padding: 6px 12px;
  }

  .highlight-box {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .confirmation-block {
    padding: 20px;
  }

  .confirmation-text ul {
    text-align: left;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }

  .preamble {
    padding: 16px 20px;
  }

  .contact-email a {
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

  .consent-page {
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

  .contact-card {
    background: #f5f5f5 !important;
  }

  .highlight-box {
    background: #f5f5f5 !important;
  }

  .action-item {
    background: #f5f5f5 !important;
  }

  .accept-badge {
    background: #e8f5e9 !important;
    color: #2e7d32 !important;
  }

  .legal-footer {
    background: white !important;
  }

  .confirmation-block {
    border-color: #2e7d32 !important;
    background: white !important;
  }

  .preamble {
    border-color: #ddd !important;
    background: white !important;
  }
}
</style>
