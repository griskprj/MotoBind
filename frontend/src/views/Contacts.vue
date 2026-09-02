<template>
    <div class="container">
        <!-- === HEADER === -->
        <Header
            title="Контакты"
            subtitle="Свяжитесь с нами"
        />

        <!-- === КОНТАКТНАЯ ИНФОРМАЦИЯ === -->
        <div class="contacts-grid">
            <!-- Карточка с контактами -->
            <div class="contacts-card main-card">
                <div class="contacts-header">
                    <i class="fa fa-address-card"></i>
                    <h2>Свяжитесь с нами</h2>
                    <p class="contacts-subtitle">
                        Мы всегда рады помочь! Выберите удобный способ связи
                    </p>
                </div>

                <div class="contacts-list">
                    <!-- Telegram -->
                    <a 
                        :href="telegramLink" 
                        target="_blank"
                        rel="noopener noreferrer"
                        class="contact-item telegram"
                    >
                        <div class="contact-icon">
                            <i class="fa fa-plane"></i>
                        </div>
                        <div class="contact-info">
                            <span class="contact-label">Telegram</span>
                            <span class="contact-value">{{ telegramUsername }}</span>
                            <span class="contact-hint">Нажмите для перехода в Telegram</span>
                        </div>
                        <i class="fa fa-chevron-right contact-arrow"></i>
                    </a>

                    <!-- Email -->
                    <a 
                        :href="emailLink" 
                        class="contact-item email"
                    >
                        <div class="contact-icon">
                            <i class="fa fa-envelope"></i>
                        </div>
                        <div class="contact-info">
                            <span class="contact-label">Email</span>
                            <span class="contact-value">{{ email }}</span>
                            <span class="contact-hint">Нажмите чтобы написать письмо</span>
                        </div>
                        <i class="fa fa-chevron-right contact-arrow"></i>
                    </a>

                    <!-- GitHub (опционально) -->
                    <a 
                        v-if="github"
                        :href="github" 
                        target="_blank"
                        rel="noopener noreferrer"
                        class="contact-item github"
                    >
                        <div class="contact-icon">
                            <i class="fa fa-star"></i>
                        </div>
                        <div class="contact-info">
                            <span class="contact-label">GitHub</span>
                            <span class="contact-value">{{ githubUsername || 'GitHub' }}</span>
                            <span class="contact-hint">Исходный код проекта</span>
                        </div>
                        <i class="fa fa-chevron-right contact-arrow"></i>
                    </a>
                </div>
            </div>

            <!-- Дополнительная информация -->
            <div class="contacts-card info-card">
                <div class="info-header">
                    <i class="fa fa-info-circle"></i>
                    <h3>Обратная связь</h3>
                </div>
                <div class="info-body">
                    <p class="info-text">
                        Если у вас есть вопросы, предложения или вы нашли ошибку — 
                        напишите нам. Мы постараемся ответить как можно быстрее!
                    </p>
                    
                    <div class="info-features">
                        <div class="feature-item">
                            <i class="fa fa-clock"></i>
                            <div>
                                <span class="feature-title">Время ответа</span>
                                <span class="feature-desc">Обычно в течение 24 часов</span>
                            </div>
                        </div>
                        <div class="feature-item">
                            <i class="fa fa-comments"></i>
                            <div>
                                <span class="feature-title">Языки общения</span>
                                <span class="feature-desc">Русский, English</span>
                            </div>
                        </div>
                        <div class="feature-item">
                            <i class="fa fa-shield"></i>
                            <div>
                                <span class="feature-title">Конфиденциальность</span>
                                <span class="feature-desc">Ваши данные в безопасности</span>
                            </div>
                        </div>
                    </div>

                    <div class="info-divider"></div>

                    <div class="response-time">
                        <i class="fa fa-check-circle"></i>
                        <span>Мы ценим каждого пользователя и стараемся помочь всем</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- === КНОПКА НАЗАД === -->
        <div class="back-wrapper">
            <button class="btn btn-secondary" @click="$router.back()">
                <i class="fa fa-arrow-left"></i> Вернуться назад
            </button>
        </div>
    </div>
</template>

<script>
import Header from '../components/Header.vue'

export default {
    name: 'Contacts',
    components: { Header },
    
    data() {
        return {
            telegramUsername: 'griskyy',
            email: 'motobind@yandex.ru',
            github: 'https://github.com/griskprj/motobind',
            githubUsername: 'motobind'
        }
    },
    
    computed: {
        telegramLink() {
            return `https://t.me/${this.telegramUsername}`
        },
        emailLink() {
            return `mailto:${this.email}`
        }
    }
}
</script>

<style scoped>
.container {
    max-width: 900px;
    margin: 0 auto;
    padding: 0 20px 40px;
}

/* ===== КОНТАКТНАЯ СЕТКА ===== */
.contacts-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    margin-top: 20px;
}

/* ===== КАРТОЧКИ ===== */
.contacts-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 28px;
    transition: all 0.2s;
}

.contacts-card:hover {
    border-color: var(--accent-trans);
}

.main-card {
    grid-column: 1 / 2;
}

.info-card {
    grid-column: 2 / 3;
}

/* ===== ЗАГОЛОВОК КАРТОЧКИ ===== */
.contacts-header {
    text-align: center;
    margin-bottom: 28px;
}

.contacts-header i {
    font-size: 40px;
    color: var(--accent-text);
    margin-bottom: 12px;
    display: block;
}

.contacts-header h2 {
    font-size: 24px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 8px 0;
}

.contacts-subtitle {
    font-size: 15px;
    color: var(--text-secondary);
    margin: 0;
}

/* ===== СПИСОК КОНТАКТОВ ===== */
.contacts-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.contact-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px 20px;
    background: var(--bg-secondary);
    border-radius: 12px;
    border: 1px solid var(--border-light);
    text-decoration: none;
    transition: all 0.2s;
    cursor: pointer;
    position: relative;
}

.contact-item:hover {
    transform: translateX(4px);
    border-color: var(--accent);
    background: var(--bg-card-hover);
}

.contact-item:hover .contact-arrow {
    transform: translateX(4px);
    color: var(--accent-text);
}

.contact-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
}

.contact-item.telegram .contact-icon {
    background: var(--accent-trans);
    color: var(--accent-text);
}

.contact-item.email .contact-icon {
    background: rgba(59, 130, 246, 0.15);
    color: #60a5fa;
}

.contact-item.github .contact-icon {
    background: rgba(255, 255, 255, 0.05);
    color: var(--text-secondary);
}

.contact-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.contact-label {
    font-size: 12px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-muted);
}

.contact-value {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
}

.contact-hint {
    font-size: 13px;
    color: var(--text-muted);
}

.contact-arrow {
    color: var(--text-muted);
    transition: all 0.2s;
    font-size: 16px;
}

.contact-item.telegram .contact-value {
    color: var(--accent-text);
}

.contact-item.email .contact-value {
    color: #60a5fa;
}

.contact-item.github .contact-value {
    color: var(--text-secondary);
}

/* ===== ИНФО-КАРТОЧКА ===== */
.info-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
}

.info-header i {
    font-size: 28px;
    color: var(--accent-text);
}

.info-header h3 {
    font-size: 20px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
}

.info-body {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.info-text {
    font-size: 15px;
    color: var(--text-secondary);
    line-height: 1.7;
    margin: 0;
}

.info-features {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.feature-item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 16px;
    background: var(--bg-secondary);
    border-radius: 10px;
    border: 1px solid var(--border-light);
}

.feature-item i {
    font-size: 18px;
    color: var(--accent-text);
    width: 24px;
    text-align: center;
}

.feature-item div {
    display: flex;
    flex-direction: column;
}

.feature-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
}

.feature-desc {
    font-size: 13px;
    color: var(--text-muted);
}

.info-divider {
    height: 1px;
    background: var(--border-light);
    margin: 4px 0;
}

.response-time {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 16px;
    background: var(--success-trans);
    border-radius: 10px;
    border: 1px solid rgba(16, 185, 129, 0.15);
}

.response-time i {
    font-size: 20px;
    color: var(--success-text);
}

.response-time span {
    font-size: 14px;
    color: var(--text-secondary);
}

/* ===== КНОПКА НАЗАД ===== */
.back-wrapper {
    margin-top: 24px;
    text-align: center;
}

.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 10px 24px;
    border-radius: 10px;
    font-weight: 500;
    font-size: 14px;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-secondary {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}

.btn-secondary:hover {
    background: var(--border-color);
}

/* ============================================ */
/* ===== АДАПТИВНОСТЬ ===== */
/* ============================================ */

@media (max-width: 1024px) {
    .container {
        padding: 0 16px 30px;
    }
    .contacts-grid {
        grid-template-columns: 1fr;
        gap: 16px;
    }
    .main-card {
        grid-column: 1 / 2;
    }

    .info-card {
        grid-column: 1 / 2;
    }
}

@media (max-width: 820px) {
    .contacts-card {
        padding: 20px;
    }

    .contact-item {
        padding: 14px 16px;
    }

    .contact-icon {
        width: 40px;
        height: 40px;
        font-size: 18px;
    }

    .contact-value {
        font-size: 15px;
    }
}

@media (max-width: 480px) {
    .container {
        padding: 0 12px 24px;
    }

    .contacts-card {
        padding: 16px;
    }

    .contacts-header h2 {
        font-size: 20px;
    }

    .contacts-header i {
        font-size: 32px;
    }

    .contact-item {
        padding: 12px 14px;
        gap: 12px;
    }

    .contact-icon {
        width: 36px;
        height: 36px;
        font-size: 16px;
    }

    .contact-value {
        font-size: 14px;
    }

    .contact-hint {
        font-size: 12px;
    }

    .contact-arrow {
        display: none;
    }

    .info-header h3 {
        font-size: 18px;
    }

    .feature-item {
        padding: 10px 14px;
    }

    .feature-title {
        font-size: 13px;
    }

    .feature-desc {
        font-size: 12px;
    }

    .response-time span {
        font-size: 13px;
    }

    .btn {
        width: 100%;
        justify-content: center;
        padding: 12px;
    }
}

/* ===== ДАРК/ЛАЙТ СОВМЕСТИМОСТЬ ===== */
[data-theme="light"] .contact-item.github .contact-icon {
    background: rgba(0, 0, 0, 0.05);
    color: #333;
}

[data-theme="light"] .contact-item.github .contact-value {
    color: #333;
}

[data-theme="light"] .info-features .feature-item {
    background: #f8fafc;
}
</style>