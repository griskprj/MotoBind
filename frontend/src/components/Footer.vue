<template>
    <footer class="footer">
        <div class="footer-container">
            <!-- Верхняя часть футера -->
            <div class="footer-top">
                <!-- Левая колонка - Логотип -->
                <div class="footer-brand">
                    <router-link to="/garage" class="brand-link">
                        <img class="brand-logo" src="/MotoBindLogo.png" alt="MotoBind">
                        <div class="brand-text">
                            <span class="brand-name">Moto<span class="brand-accent">Bind</span></span>
                            <span class="brand-tagline">Управляй своим мотоциклом</span>
                        </div>
                    </router-link>
                </div>

                <!-- Правая колонка - Навигация -->
                <div class="footer-nav">
                    <div class="nav-section">
                        <h4 class="nav-title">Сервис</h4>
                        <router-link class="nav-link" to="/garage">Гараж</router-link>
                        <router-link class="nav-link" to="/maintenance">Обслуживание</router-link>
                        <router-link class="nav-link" to="/repair">Ремонт</router-link>
                        <router-link class="nav-link" to="/manuals">Мануалы</router-link>
                    </div>

                    <div class="nav-section">
                        <h4 class="nav-title">Документы</h4>
                        <router-link class="nav-link" to="/consent">Согласие на обработку ПД</router-link>
                        <router-link class="nav-link" to="/privacy">Политика конфиденциальности</router-link>
                        <router-link class="nav-link" to="/terms">Пользовательское соглашение</router-link>
                        <router-link class="nav-link" to="/rules">Правила сервиса</router-link>
                    </div>

                    <div class="nav-section">
                        <h4 class="nav-title">Информация</h4>
                        <router-link class="nav-link" to="/landing">О сервисе</router-link>
                        <router-link class="nav-link" to="/contacts">Контакты</router-link>
                    
                    </div>
                </div>
            </div>

            <!-- Разделитель -->
            <div class="footer-divider"></div>

            <!-- Нижняя часть футера -->
            <div class="footer-bottom">
                <p class="footer-copyright">
                    © {{ currentYear }} MotoBind. Все права защищены
                </p>
                
                <div class="footer-social">
                    <a href="https://t.me/motobind" class="social-link" aria-label="Telegram">
                        <i class="fab fa-telegram"></i>
                    </a>
                    <a href="https://youtube.com/@grisky_y?si=RnyFySM6cVXt_YhE" class="social-link" aria-label="YouTube">
                        <i class="fab fa-youtube"></i>
                    </a>
                    <a href="https://github.com/griskprj/MotoBind" class="social-link" aria-label="GitHub">
                        <i class="fab fa-github"></i>
                    </a>
                </div>

                <div class="footer-version">
                    <span class="version-badge">v1.1.2</span>
                </div>
            </div>
        </div>
    </footer>
</template>

<script>
export default {
    computed: {
        currentYear() {
            return new Date().getFullYear();
        }
    }
}
</script>

<style scoped>
/* ===== Переменные футера ===== */
.footer {
    --footer-bg: var(--bg-secondary);
    --footer-border: var(--border-color);
    --footer-text: var(--text-secondary);
    --footer-text-light: var(--text-muted);
    --footer-radius: 16px;
    
    margin-top: 64px;
    background: var(--footer-bg);
    border-top: 1px solid var(--footer-border);
    padding: 48px 0 24px;
    transition: background 0.3s ease;
}

[data-theme="light"] .footer {
    --footer-bg: #f8fafc;
    --footer-border: #e2e8f0;
}

/* ===== Контейнер ===== */
.footer-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 24px;
}

/* ===== Верхняя часть ===== */
.footer-top {
    display: grid;
    grid-template-columns: 280px 1fr;
    gap: 48px;
    padding-bottom: 32px;
}

/* ===== Бренд ===== */
.footer-brand {
    display: flex;
    align-items: flex-start;
}

.brand-link {
    display: flex;
    align-items: center;
    gap: 16px;
    text-decoration: none;
    transition: transform 0.3s ease;
}

.brand-link:hover {
    transform: translateY(-2px);
}

.brand-logo {
    width: 56px;
    height: 56px;
    border-radius: 14px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    transition: all 0.3s ease;
    object-fit: contain;
    background: var(--bg-card);
    padding: 4px;
}

.brand-link:hover .brand-logo {
    box-shadow: 0 4px 30px rgba(124, 58, 237, 0.25);
    transform: scale(1.03);
}

.brand-text {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.brand-name {
    font-size: 22px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.5px;
    line-height: 1.2;
}

.brand-accent {
    color: var(--accent);
    background: linear-gradient(135deg, var(--accent), #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.brand-tagline {
    font-size: 13px;
    color: var(--text-muted);
    font-weight: 400;
    -webkit-text-fill-color: var(--text-muted);
}

/* ===== Навигация футера ===== */
.footer-nav {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 32px;
}

.nav-section {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.nav-title {
    font-size: 12px;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 8px;
    padding-bottom: 6px;
    border-bottom: 2px solid var(--footer-border);
}

.nav-link {
    color: var(--footer-text);
    text-decoration: none;
    font-size: 14px;
    font-weight: 400;
    padding: 4px 0;
    transition: all 0.25s ease;
    position: relative;
    width: fit-content;
}

.nav-link::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 1.5px;
    background: var(--accent);
    transition: width 0.3s ease;
}

.nav-link:hover {
    color: var(--accent);
}

.nav-link:hover::after {
    width: 100%;
}

/* ===== Разделитель ===== */
.footer-divider {
    height: 1px;
    background: linear-gradient(
        to right,
        transparent,
        var(--footer-border) 20%,
        var(--footer-border) 80%,
        transparent
    );
    margin: 8px 0 20px;
}

/* ===== Нижняя часть ===== */
.footer-bottom {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px 24px;
}

.footer-copyright {
    color: var(--footer-text-light);
    font-size: 13px;
    font-weight: 400;
    margin: 0;
}

/* ===== Социальные иконки ===== */
.footer-social {
    display: flex;
    gap: 12px;
}

.social-link {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    color: var(--text-muted);
    background: transparent;
    border: 1px solid var(--footer-border);
    transition: all 0.3s ease;
    text-decoration: none;
    font-size: 16px;
}

.social-link:hover {
    color: var(--accent);
    border-color: var(--accent);
    background: var(--accent-trans);
    transform: translateY(-3px);
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.15);
}

.social-link:active {
    transform: translateY(0);
}

/* ===== Версия ===== */
.footer-version {
    display: flex;
    align-items: center;
}

.version-badge {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-muted);
    background: var(--bg-card);
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid var(--footer-border);
    letter-spacing: 0.3px;
    user-select: none;
}

/* ===== Адаптив ===== */

/* Планшеты */
@media (max-width: 1024px) {
    .footer-top {
        grid-template-columns: 1fr;
        gap: 32px;
    }
    
    .footer-brand {
        justify-content: center;
    }
    
    .footer-nav {
        grid-template-columns: repeat(3, 1fr);
        gap: 24px;
    }
}

/* Мобильные */
@media (max-width: 768px) {
    .footer {
        margin-top: 48px;
        padding: 32px 0 16px;
    }
    
    .footer-container {
        padding: 0 16px;
    }
    
    .footer-nav {
        grid-template-columns: 1fr 1fr;
        gap: 24px 16px;
    }
    
    .footer-bottom {
        flex-direction: column;
        text-align: center;
        gap: 12px;
    }
    
    .brand-logo {
        width: 44px;
        height: 44px;
    }
    
    .brand-name {
        font-size: 19px;
    }
    
    .brand-tagline {
        font-size: 12px;
    }
    
    .footer-social {
        gap: 8px;
    }
    
    .social-link {
        width: 32px;
        height: 32px;
        font-size: 14px;
    }
}

/* Маленькие мобильные */
@media (max-width: 480px) {
    .footer-nav {
        grid-template-columns: 1fr;
        gap: 20px;
        text-align: center;
    }
    
    .nav-link {
        width: 100%;
        text-align: center;
    }
    
    .nav-link::after {
        left: 50%;
        transform: translateX(-50%);
    }
    
    .nav-title {
        text-align: center;
    }
    
    .footer-brand {
        text-align: center;
    }
    
    .brand-link {
        flex-direction: column;
        align-items: center;
    }
    
    .brand-text {
        align-items: center;
    }
}

/* ===== Анимация появления ===== */
.footer {
    opacity: 0;
    animation: footerFadeIn 0.6s ease forwards;
    animation-delay: 0.2s;
}

@keyframes footerFadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* ===== Reduced motion ===== */
@media (prefers-reduced-motion: reduce) {
    .footer {
        animation: none;
        opacity: 1;
        transform: none;
    }
    
    .brand-link,
    .nav-link::after,
    .social-link {
        transition-duration: 0.01ms !important;
    }
}
</style>