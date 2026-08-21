<template>
  <div class="privacy-policy-page">
    <!-- Хлебные крошки -->
    <div class="breadcrumbs">
      <router-link to="/home" class="breadcrumb-link">
        <i class="fas fa-home"></i> Главная
      </router-link>
      <span class="breadcrumb-separator">/</span>
      <span class="breadcrumb-current">Политика конфиденциальности</span>
    </div>

    <!-- Заголовок страницы -->
    <div class="page-header">
      <div class="page-header-icon">
        <i class="fas fa-shield-alt"></i>
      </div>
      <div class="page-header-content">
        <h1>Политика конфиденциальности</h1>
        <p class="page-subtitle">
          Сервис <strong>MotoBind</strong> &mdash; <span class="domain">motobind.ru</span>
        </p>
        <p class="page-description">
          Дата вступления в силу: <strong>03 августа 2026 г.</strong>
        </p>
        <div class="accept-badge">
          <i class="fas fa-check-circle"></i>
          Используя Сервис, Вы подтверждаете своё согласие с настоящей Политикой
        </div>
      </div>
    </div>

    <!-- Основное содержание -->
    <div class="privacy-content">
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
          <i class="fas fa-balance-scale"></i>
          Настоящая Политика конфиденциальности определяет порядок обработки персональных данных
          пользователей сервиса <strong>MotoBind</strong>, расположенного по адресу
          <a href="https://motobind.ru" target="_blank">motobind.ru</a>.
        </p>
      </div>
    </div>
  </div>
</template>

<head>
  <title>MotoBind — Политика конфиденциальности | Защита данных</title>
  <meta name="description" content="Политика конфиденциальности MotoBind. Узнайте, как мы собираем, используем и защищаем ваши персональные данные.">
</head>

<script>
export default {
  name: 'PrivacyPolicy',

  data() {
    return {
      showBackToTop: false,

      sections: [
        {
          id: 'operator',
          number: '1',
          title: 'Оператор персональных данных',
          content: `
            <p>Оператором персональных данных является:</p>
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
                <span class="contact-label"><i class="fas fa-globe"></i> Домен сайта:</span>
                <span class="contact-value">
                  <a href="https://motobind.ru" target="_blank">motobind.ru</a>
                </span>
              </div>
            </div>
          `
        },
        {
          id: 'what-we-collect',
          number: '2',
          title: 'Какие данные мы собираем',
          content: `
            <p>При использовании Сервиса Пользователь может предоставить следующие данные.</p>
          `,
          subsections: [
            {
              id: 'what-we-collect-account',
              number: '2.1',
              title: 'Данные учётной записи',
              content: `
                <ul>
                  <li>имя пользователя (логин);</li>
                  <li>адрес электронной почты;</li>
                  <li>пароль (хранится исключительно в зашифрованном виде);</li>
                  <li>фотография профиля (необязательно).</li>
                </ul>
              `
            },
            {
              id: 'what-we-collect-moto',
              number: '2.2',
              title: 'Информация о мотоциклах',
              content: `
                <p>Пользователь может хранить информацию о принадлежащих ему мотоциклах:</p>
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
              id: 'what-we-collect-maintenance',
              number: '2.3',
              title: 'Информация об обслуживании',
              content: `
                <p>В рамках работы Сервиса могут храниться:</p>
                <ul>
                  <li>записи о проведенном обслуживании;</li>
                  <li>запланированное обслуживание;</li>
                  <li>категории работ;</li>
                  <li>стоимость обслуживания;</li>
                  <li>пробег на момент обслуживания;</li>
                  <li>история обслуживания.</li>
                </ul>
              `
            },
            {
              id: 'what-we-collect-content',
              number: '2.4',
              title: 'Пользовательский контент',
              content: `
                <p>Пользователь может создавать:</p>
                <ul>
                  <li>мануалы;</li>
                  <li>инструкции по ремонту;</li>
                  <li>иной контент, добровольно размещаемый в Сервисе.</li>
                </ul>
              `
            },
            {
              id: 'what-we-collect-other',
              number: '2.5',
              title: 'Иная информация',
              content: `
                <p>Также Пользователь может добровольно предоставить любую другую информацию, вводимую при использовании функционала Сервиса.</p>
              `
            }
          ]
        },
        {
          id: 'purposes',
          number: '3',
          title: 'Цели обработки персональных данных',
          content: `
            <p>Персональные данные используются исключительно для:</p>
            <ul>
              <li>регистрации и авторизации Пользователя;</li>
              <li>предоставления доступа к функционалу Сервиса;</li>
              <li>хранения информации о мотоциклах;</li>
              <li>ведения истории обслуживания;</li>
              <li>формирования персональной статистики;</li>
              <li>публикации пользовательских мануалов;</li>
              <li>обеспечения корректной работы Сервиса;</li>
              <li>связи с Пользователем по вопросам использования Сервиса;</li>
              <li>исполнения требований законодательства Российской Федерации.</li>
            </ul>
          `
        },
        {
          id: 'what-we-not-collect',
          number: '4',
          title: 'Что мы НЕ собираем',
          content: `
            <p><strong>MotoBind:</strong></p>
            <ul class="not-collect-list">
              <li><i class="fas fa-times-circle text-danger"></i> не записывает пользовательские логи действий;</li>
              <li><i class="fas fa-times-circle text-danger"></i> не использует системы веб-аналитики;</li>
              <li><i class="fas fa-times-circle text-danger"></i> не использует рекламные трекеры;</li>
              <li>
                <i class="fas fa-times-circle text-danger"></i> не использует файлы cookie для отслеживания поведения
                Пользователей (за исключением технически необходимых файлов, если они используются для авторизации);
              </li>
              <li><i class="fas fa-times-circle text-danger"></i> не осуществляет автоматическое профилирование Пользователей.</li>
            </ul>
            <div class="highlight-box success">
              <i class="fas fa-shield-alt"></i>
              <span>Мы ценим вашу приватность и собираем только то, что необходимо для работы Сервиса.</span>
            </div>
          `
        },
        {
          id: 'third-parties',
          number: '5',
          title: 'Передача данных третьим лицам',
          content: `
            <p>
              <strong>MotoBind не продаёт, не передаёт и не предоставляет персональные данные третьим лицам.</strong>
            </p>
            <p>Исключение составляют случаи, предусмотренные законодательством Российской Федерации, когда предоставление информации является обязательным.</p>
            <div class="highlight-box info">
              <i class="fas fa-info-circle"></i>
              <span>Ваши данные в безопасности. Мы не передаём их рекламным сетям, аналитическим сервисам или другим третьим лицам.</span>
            </div>
          `
        },
        {
          id: 'access',
          number: '6',
          title: 'Кто имеет доступ к данным',
          content: `
            <p>Доступ к персональным данным имеют:</p>
            <ul>
              <li><strong>сам Пользователь</strong> — в полном объёме;</li>
              <li><strong>администраторы Сервиса</strong> — в объёме, необходимом для обеспечения работы сайта;</li>
              <li><strong>государственные органы</strong> — исключительно в случаях и порядке, предусмотренных законодательством Российской Федерации.</li>
            </ul>
            <p class="note">Администраторы не используют персональные данные в целях, не связанных с обеспечением работы Сервиса.</p>
          `
        },
        {
          id: 'storage',
          number: '7',
          title: 'Хранение данных',
          content: `
            <p>Персональные данные хранятся только до тех пор, пока существует учётная запись Пользователя.</p>
            <p><strong>После удаления аккаунта:</strong></p>
            <ul>
              <li>персональные данные удаляются;</li>
              <li>информация о мотоциклах удаляется;</li>
              <li>история обслуживания удаляется;</li>
              <li>пользовательские мануалы удаляются (если иной порядок не будет прямо указан в Сервисе);</li>
              <li>фотографии профиля удаляются.</li>
            </ul>
            <div class="highlight-box warning">
              <i class="fas fa-exclamation-triangle"></i>
              <span>Удаление осуществляется безвозвратно. Резервные копии, содержащие удалённые персональные данные, не сохраняются специально для дальнейшего использования.</span>
            </div>
          `
        },
        {
          id: 'protection',
          number: '8',
          title: 'Защита информации',
          content: `
            <p><strong>MotoBind</strong> принимает разумные технические и организационные меры для защиты информации от:</p>
            <ul>
              <li>несанкционированного доступа;</li>
              <li>изменения;</li>
              <li>удаления;</li>
              <li>распространения;</li>
              <li>уничтожения.</li>
            </ul>
            <div class="highlight-box success">
              <i class="fas fa-lock"></i>
              <span>Пароли пользователей никогда не хранятся в открытом виде и защищаются современными криптографическими алгоритмами хеширования.</span>
            </div>
          `
        },
        {
          id: 'user-rights',
          number: '9',
          title: 'Права пользователя',
          content: `
            <p>Пользователь имеет право:</p>
            <div class="rights-grid">
              <div class="right-item">
                <i class="fas fa-info-circle"></i>
                <span>получать информацию об обработке своих данных</span>
              </div>
              <div class="right-item">
                <i class="fas fa-edit"></i>
                <span>изменять свои данные</span>
              </div>
              <div class="right-item">
                <i class="fas fa-trash-alt"></i>
                <span>удалять свои данные</span>
              </div>
              <div class="right-item">
                <i class="fas fa-user-slash"></i>
                <span>удалить учётную запись</span>
              </div>
              <div class="right-item full-width">
                <i class="fas fa-envelope"></i>
                <span>обратиться к Оператору по вопросам обработки персональных данных</span>
              </div>
            </div>
            <p>Для обращения необходимо написать на электронную почту:</p>
            <div class="contact-email">
              <a href="mailto:griskyy@yandex.ru">
                <i class="fas fa-envelope"></i> griskyy@yandex.ru
              </a>
            </div>
          `
        },
        {
          id: 'manuals',
          number: '10',
          title: 'Публикация мануалов',
          content: `
            <p>
              При публикации мануалов Пользователь соглашается с тем, что созданный им контент
              может быть доступен другим Пользователям Сервиса в соответствии с настройками публикации.
            </p>
            <div class="highlight-box warning">
              <i class="fas fa-exclamation-triangle"></i>
              <span>Ответственность за содержание публикуемых материалов несёт Пользователь.</span>
            </div>
          `
        },
        {
          id: 'changes',
          number: '11',
          title: 'Изменение Политики',
          content: `
            <p>Оператор вправе изменять настоящую Политику.</p>
            <p>Актуальная версия всегда публикуется по адресу:</p>
            <div class="policy-url">
              <a href="https://motobind.ru/privacy" target="_blank">
                <i class="fas fa-link"></i> https://motobind.ru/privacy
              </a>
            </div>
            <div class="highlight-box info">
              <i class="fas fa-info-circle"></i>
              <span>Продолжение использования Сервиса после публикации новой редакции означает согласие Пользователя с внесёнными изменениями.</span>
            </div>
          `
        },
        {
          id: 'contacts',
          number: '12',
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
.privacy-policy-page {
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
  color: var(--accent);
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

.right-item.full-width {
  grid-column: 1 / -1;
}

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

.policy-url {
  margin: 12px 0;
}

.policy-url a {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  background: var(--bg-secondary);
  border-radius: 12px;
  color: var(--accent);
  font-size: 15px;
  text-decoration: none;
  border: 1px solid var(--border-color);
  transition: all 0.2s;
}

.policy-url a:hover {
  border-color: var(--accent);
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
.policy-footer {
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
  .privacy-policy-page {
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

  .right-item.full-width {
    grid-column: 1;
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

  .contact-email a {
    width: 100%;
    justify-content: center;
  }

  .policy-url a {
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

  .privacy-policy-page {
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
}
</style>
