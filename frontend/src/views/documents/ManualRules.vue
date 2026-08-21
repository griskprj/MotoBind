<template>
    <div class="container">
        <!-- === HEADER === -->
        <header class="page-header">
            <div class="header-left">
                <h2>📋 Правила оформления мануалов</h2>
                <p class="header-subtitle">
                    Соблюдение этих правил поможет создавать качественные и понятные инструкции для всех пользователей
                </p>
            </div>

            <div class="header-right">
                <i class="fa fa-bell notification-icon"></i>
                <div class="profile-wrapper">
                    <img src="/BaseAvatar.jpg" alt="avatar" class="profile-img">
                    <button class="dropdown-trigger" @click="welcomeDropdownActive = !welcomeDropdownActive">
                        <i class="fa" :class="welcomeDropdownActive ? 'fa-angle-up' : 'fa-angle-down'"></i>
                    </button>
                    <div v-if="welcomeDropdownActive" class="dropdown-list">
                        <ul>
                            <li><button class="dropdown-item">Профиль</button></li>
                            <li><button @click="logout" class="dropdown-item">Выйти</button></li>
                        </ul>
                    </div>
                </div>
            </div>
        </header>

        <!-- === MAIN CONTENT === -->
        <div class="rules-content">
            <!-- Блок 1: Общие требования -->
            <section class="rules-section">
                <div class="section-header">
                    <span class="section-icon">📌</span>
                    <h3>Общие требования</h3>
                </div>
                <div class="rules-list">
                    <div class="rule-item">
                        <div class="rule-icon">1</div>
                        <div class="rule-content">
                            <h4>Структура мануала</h4>
                            <p>Каждый мануал должен содержать следующие разделы:</p>
                            <ul>
                                <li><strong>Название</strong> — краткое, отражающее суть процедуры</li>
                                <li><strong>Описание</strong> — что делает процедура и для каких мотоциклов</li>
                                <li><strong>Материалы и запчасти</strong> — полный список необходимого</li>
                                <li><strong>Инструменты</strong> — все инструменты для выполнения работы</li>
                                <li><strong>Пошаговая инструкция</strong> — подробное описание каждого шага</li>
                                <li><strong>Полезный совет</strong> — дополнительные рекомендации</li>
                            </ul>
                        </div>
                    </div>

                    <div class="rule-item">
                        <div class="rule-icon">2</div>
                        <div class="rule-content">
                            <h4>Форматирование</h4>
                            <ul>
                                <li>Используйте чёткие и краткие заголовки шагов</li>
                                <li>Описания шагов должны быть детальными, но без воды</li>
                                <li>Указывайте точные параметры: моменты затяжки, зазоры, допуски</li>
                                <li>Выделяйте важные предупреждения и советы</li>
                            </ul>
                        </div>
                    </div>

                    <div class="rule-item">
                        <div class="rule-icon">3</div>
                        <div class="rule-content">
                            <h4>Категоризация</h4>
                            <p>Правильно выбирайте категорию для мануала:</p>
                            <div class="categories-grid">
                                <span class="category-tag">Двигатель</span>
                                <span class="category-tag">Привод</span>
                                <span class="category-tag">Рулевое управление</span>
                                <span class="category-tag">Подвеска</span>
                                <span class="category-tag">Электроника</span>
                                <span class="category-tag">Колеса/Шины</span>
                                <span class="category-tag">Тормозная система</span>
                                <span class="category-tag">Топливная система</span>
                                <span class="category-tag">Система охлаждения</span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Блок 2: Содержательные требования -->
            <section class="rules-section">
                <div class="section-header">
                    <span class="section-icon">✍️</span>
                    <h3>Содержательные требования</h3>
                </div>
                <div class="rules-grid">
                    <div class="rule-card">
                        <div class="rule-card-header">
                            <i class="fa fa-bullseye"></i>
                            <h4>Точность</h4>
                        </div>
                        <ul>
                            <li>Указывайте точные технические параметры</li>
                            <li>Используйте официальную терминологию</li>
                            <li>При необходимости ссылайтесь на документацию</li>
                        </ul>
                    </div>

                    <div class="rule-card">
                        <div class="rule-card-header">
                            <i class="fa fa-font"></i>
                            <h4>Язык и стиль</h4>
                        </div>
                        <ul>
                            <li>Пишите ясно и лаконично</li>
                            <li>Избегайте сложных конструкций</li>
                            <li>Используйте профессиональную терминологию</li>
                            <li>Пишите от третьего лица</li>
                        </ul>
                    </div>

                    <div class="rule-card">
                        <div class="rule-card-header">
                            <i class="fa fa-shield-alt"></i>
                            <h4>Безопасность</h4>
                        </div>
                        <ul>
                            <li>Выделяйте меры предосторожности</li>
                            <li>Указывайте средства защиты</li>
                            <li>Предупреждайте об опасных операциях</li>
                        </ul>
                    </div>

                    <div class="rule-card">
                        <div class="rule-card-header">
                            <i class="fa fa-image"></i>
                            <h4>Медиа-контент</h4>
                        </div>
                        <ul>
                            <li>Добавляйте схемы и иллюстрации</li>
                            <li>Используйте формат WEBP или JPEG</li>
                            <li>Максимальный размер — 2 МБ</li>
                            <li>Подписывайте изображения</li>
                        </ul>
                    </div>
                </div>
            </section>

            <!-- Блок 3: Шаблон мануала -->
            <section class="rules-section template-section">
                <div class="section-header">
                    <span class="section-icon">📝</span>
                    <h3>Шаблон мануала</h3>
                    <button class="btn-copy" @click="copyTemplate">
                        <i class="fa fa-copy"></i> Копировать
                    </button>
                </div>
                <div class="template-preview">
                    <pre><code>{{ templateExample }}</code></pre>
                </div>
            </section>

            <!-- Блок 4: Пример оформления -->
            <section class="rules-section example-section">
                <div class="section-header">
                    <span class="section-icon">⭐</span>
                    <h3>Пример оформления</h3>
                </div>
                <div class="example-card">
                    <div class="example-header">
                        <h4>Замена масла в двигателе</h4>
                        <span class="difficulty-badge easy">Легко</span>
                    </div>
                    
                    <div class="example-section">
                        <h5>Описание</h5>
                        <p>Регламентная процедура замены моторного масла и масляного фильтра для двигателей объемом от 500 до 1000 см³.</p>
                    </div>

                    <div class="example-section">
                        <h5>Необходимые материалы</h5>
                        <ul>
                            <li>Моторное масло (10W-40, API SN) — 3.5 литра</li>
                            <li>Масляный фильтр — оригинальный или аналог</li>
                            <li>Медная шайба сливной пробки</li>
                            <li>Ключ для сливной пробки (на 17)</li>
                            <li>Съемник масляного фильтра</li>
                        </ul>
                    </div>

                    <div class="example-section">
                        <h5>Пошаговая инструкция</h5>
                        <div class="example-step">
                            <span class="step-number">Шаг 1</span>
                            <div>
                                <strong>Прогрев двигателя</strong>
                                <p>Запустите двигатель и дайте ему поработать на холостых оборотах 5-7 минут до рабочей температуры (около 90°C). Прогретое масло имеет меньшую вязкость и лучше сливается.</p>
                            </div>
                        </div>
                        <div class="example-step">
                            <span class="step-number">Шаг 2</span>
                            <div>
                                <strong>Слив старого масла</strong>
                                <p>Установите мотоцикл на центральную подставку. Подставьте емкость под сливную пробку. Открутите пробку и дайте маслу стечь (минимум 15 минут).</p>
                            </div>
                        </div>
                        <div class="example-step">
                            <span class="step-number">Шаг 3</span>
                            <div>
                                <strong>Замена масляного фильтра</strong>
                                <p>Используйте съемник для откручивания старого фильтра. Смажьте новое уплотнительное кольцо свежим маслом. Установите новый фильтр рукой.</p>
                            </div>
                        </div>
                    </div>

                    <div class="example-section">
                        <h5>Техника безопасности</h5>
                        <div class="warning-block">
                            <span class="warning-icon">⚠️</span>
                            <span>Работайте с горячим маслом осторожно — используйте термостойкие перчатки</span>
                        </div>
                        <div class="warning-block">
                            <span class="warning-icon">🛡️</span>
                            <span>Используйте защитные очки</span>
                        </div>
                        <div class="warning-block">
                            <span class="warning-icon">🔥</span>
                            <span>Утилизируйте отработанное масло в специальных пунктах приема</span>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    </div>
</template>

<head>
  <title>MotoBind — Правила оформления мануалов | Как создать инструкцию</title>
  <meta name="description" content="Правила оформления мануалов в MotoBind. Узнайте, как создавать качественные инструкции по ремонту и обслуживанию.">
</head>

<script>
import api from '../../api/api'

export default {
    name: 'ManualRules',
    data() {
        return {
            welcomeDropdownActive: false,
            templateExample: `# [Название процедуры]

## Описание
[Краткое описание процедуры: цель, результат, для каких моделей]

## Необходимые материалы
- [Список запчастей]
- [Расходные материалы]
- [Инструменты]

## Пошаговая инструкция

### Шаг 1: [Название шага]
[Подробное описание действия]

### Шаг 2: [Название шага]
[Подробное описание действия]

## Полезный совет
- [Советы по выполнению]
- [Частые ошибки]

## Техника безопасности
⚠️ [Важные предупреждения]
🛡️ [Средства защиты]`
        };
    },
    methods: {
        copyTemplate() {
            navigator.clipboard.writeText(this.templateExample).then(() => {
                alert('Шаблон скопирован в буфер обмена!');
            }).catch(() => {
                alert('Не удалось скопировать шаблон');
            });
        },

        async logout() {
            try {
                await api.post('/auth/logout');
            } catch(err) {
                console.error(err);
            } finally {
                const { removeTokens } = await import('../../api/auth');
                removeTokens();
                this.$router.push('/login');
            }
        }
    }
};
</script>

<style scoped>
/* ===== HEADER ===== */
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
    flex-wrap: wrap;
    gap: 16px;
}

.header-left h2 {
    margin: 0 0 8px 0;
    font-size: 26px;
}

.header-subtitle {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
}

.header-right {
    display: flex;
    align-items: center;
    gap: 16px;
}

.notification-icon {
    font-size: 20px;
    color: #8b8b9e;
    cursor: pointer;
}

.profile-wrapper {
    display: flex;
    align-items: center;
    gap: 6px;
    position: relative;
}

.profile-img {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    border: 2px solid #7c3aed;
}

.dropdown-trigger {
    background: transparent;
    border: none;
    color: #8b8b9e;
    cursor: pointer;
}

.dropdown-list {
    position: absolute;
    top: 48px;
    right: 0;
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 8px;
    min-width: 140px;
    box-shadow: var(--shadow-lg);
    z-index: 100;
    animation: slideInUp 0.2s ease;
}

.dropdown-list ul {
    list-style: none;
    margin: 0;
    padding: 0;
}

.dropdown-item {
    width: 100%;
    padding: 8px 12px;
    background: transparent;
    border: none;
    color: var(--text-secondary);
    text-align: left;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
}

.dropdown-item:hover {
    background: var(--bg-secondary);
}

@media (max-width: 720px) {
    .header-right {
        display: none;
    }
}

/* ===== RULES CONTENT ===== */
.rules-content {
    display: flex;
    flex-direction: column;
    gap: 32px;
}

/* ===== RULES SECTION ===== */
.rules-section {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 24px;
}

.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

.section-icon {
    font-size: 28px;
}

.section-header h3 {
    font-size: 18px;
    font-weight: 600;
    margin: 0;
}

/* ===== RULES LIST ===== */
.rules-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.rule-item {
    display: flex;
    gap: 16px;
    padding: 16px;
    background: var(--bg-secondary);
    border-radius: 12px;
    border-left: 3px solid var(--accent);
}

.rule-icon {
    flex-shrink: 0;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--accent-trans);
    color: var(--accent);
    border-radius: 50%;
    font-weight: 700;
    font-size: 14px;
}

.rule-content {
    flex: 1;
}

.rule-content h4 {
    font-size: 15px;
    font-weight: 600;
    margin: 0 0 8px 0;
    color: var(--text-primary);
}

.rule-content p {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0 0 8px 0;
}

.rule-content ul {
    margin: 4px 0 0 0;
    padding-left: 20px;
}

.rule-content ul li {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 4px;
}

.rule-content ul li strong {
    color: var(--text-primary);
}

/* ===== CATEGORIES GRID ===== */
.categories-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 8px;
}

.category-tag {
    padding: 4px 14px;
    background: var(--bg-primary);
    border: 1px solid var(--border-color);
    border-radius: 20px;
    font-size: 13px;
    color: var(--text-secondary);
}

/* ===== RULES GRID ===== */
.rules-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
}

.rule-card {
    padding: 16px;
    background: var(--bg-secondary);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.05);
}

.rule-card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
}

.rule-card-header i {
    font-size: 18px;
    color: var(--accent);
}

.rule-card-header h4 {
    font-size: 15px;
    font-weight: 600;
    margin: 0;
}

.rule-card ul {
    margin: 0;
    padding-left: 20px;
}

.rule-card ul li {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 4px;
}

/* ===== TEMPLATE SECTION ===== */
.template-section .section-header {
    margin-bottom: 16px;
}

.btn-copy {
    margin-left: auto;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 16px;
    background: var(--accent-trans);
    border: 1px solid var(--accent);
    border-radius: 8px;
    color: var(--accent);
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-copy:hover {
    background: var(--accent);
    color: #fff;
}

.template-preview {
    background: var(--bg-primary);
    border-radius: 12px;
    padding: 16px;
    overflow-x: auto;
}

.template-preview pre {
    margin: 0;
    font-family: 'Fira Code', 'Courier New', monospace;
    font-size: 13px;
    line-height: 1.6;
    color: var(--text-secondary);
    white-space: pre-wrap;
    word-wrap: break-word;
}

.template-preview code {
    display: block;
}

/* ===== EXAMPLE SECTION ===== */
.example-card {
    padding: 20px;
    background: var(--bg-secondary);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.05);
}

.example-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border-color);
}

.example-header h4 {
    font-size: 18px;
    font-weight: 600;
    margin: 0;
}

.difficulty-badge {
    padding: 2px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
}

.difficulty-badge.easy {
    background: rgba(16, 185, 129, 0.15);
    color: var(--success);
}

.difficulty-badge.medium {
    background: rgba(245, 158, 11, 0.15);
    color: var(--warning);
}

.difficulty-badge.hard {
    background: rgba(239, 68, 68, 0.15);
    color: var(--danger);
}

.example-section {
    margin-bottom: 16px;
}

.example-section:last-child {
    margin-bottom: 0;
}

.example-section h5 {
    font-size: 14px;
    font-weight: 600;
    color: var(--accent);
    margin: 0 0 8px 0;
}

.example-section p {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0 0 8px 0;
}

.example-section ul {
    margin: 4px 0 0 0;
    padding-left: 20px;
}

.example-section ul li {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 4px;
}

.example-step {
    display: flex;
    gap: 12px;
    padding: 12px;
    background: var(--bg-primary);
    border-radius: 8px;
    margin-bottom: 8px;
}

.example-step:last-child {
    margin-bottom: 0;
}

.example-step .step-number {
    flex-shrink: 0;
    padding: 2px 12px;
    background: var(--accent-trans);
    color: var(--accent);
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    height: fit-content;
}

.example-step div {
    flex: 1;
}

.example-step strong {
    display: block;
    font-size: 14px;
    color: var(--text-primary);
    margin-bottom: 4px;
}

.example-step p {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
}

.warning-block {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 14px;
    background: rgba(245, 158, 11, 0.05);
    border-radius: 8px;
    margin-bottom: 6px;
}

.warning-block:last-child {
    margin-bottom: 0;
}

.warning-icon {
    font-size: 18px;
}

.warning-block span {
    font-size: 14px;
    color: var(--text-secondary);
}

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
    .rules-grid {
        grid-template-columns: 1fr;
    }

    .rule-item {
        flex-direction: column;
        gap: 8px;
    }

    .section-header {
        flex-wrap: wrap;
    }

    .btn-copy {
        margin-left: 0;
        width: 100%;
        justify-content: center;
    }

    .example-header {
        flex-direction: column;
        gap: 8px;
        align-items: flex-start;
    }

    .example-step {
        flex-direction: column;
        gap: 6px;
    }

    .example-step .step-number {
        width: fit-content;
    }
}

@media (max-width: 480px) {
    .rules-section {
        padding: 16px;
    }

    .rule-item {
        padding: 12px;
    }

    .example-card {
        padding: 16px;
    }
}

/* ===== ANIMATIONS ===== */
@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* ===== SCROLL ===== */
.template-preview::-webkit-scrollbar {
    height: 6px;
}

.template-preview::-webkit-scrollbar-track {
    background: var(--bg-secondary);
    border-radius: 3px;
}

.template-preview::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 3px;
}
</style>