<template>
    <div class="container">
        <!-- Заголовок страницы -->
        <section class="section">
            <div class="section-title-wrapper">
                <i class="fa fa-user"></i>
                <h2>Админ-панель</h2>
            </div>
            <p class="subtitle">Управляйте пользователями, обслуживанием и другим контентом. А также смотрите статистику по сайту</p>
        </section>
        
        <!-- Блок пользователей -->
        <section class="section section-users">
            <div class="section-title-wrapper">
                <i class="fa fa-user-circle"></i>
                <h2>Пользователи</h2>
                <span class="section-badge">3</span>
            </div>

            <div class="users-list">
                <div class="user-card" v-for="i in 3" :key="i">
                    <div class="user-card-header">
                        <div class="user-avatar">
                            <i class="fa fa-user"></i>
                        </div>
                        <div class="user-info">
                            <p class="user-username">Grisky</p>
                            <span class="user-role">Администратор</span>
                        </div>
                    </div>
                    
                    <div class="user-card-body">
                        <div class="user-detail">
                            <i class="fa fa-envelope"></i>
                            <span>grisky@icloud.com</span>
                        </div>
                        <div class="user-detail">
                            <i class="fa fa-calendar"></i>
                            <span>Зарегистрирован: 14.07.2026</span>
                        </div>
                        <div class="user-detail">
                            <i class="fa fa-motorcycle"></i>
                            <span>Мотоциклов: 2</span>
                        </div>
                        <div class="user-status status-active">
                            <span class="status-dot"></span>
                            Активен
                        </div>
                    </div>

                    <div class="user-card-actions">
                        <button class="btn-action btn-edit" title="Редактировать">
                            <i class="fa fa-pen"></i>
                        </button>
                        <button class="btn-action btn-ban" title="Заблокировать">
                            <i class="fa fa-ban"></i>
                        </button>
                        <button class="btn-action btn-danger" title="Удалить">
                            <i class="fa fa-trash"></i>
                        </button>
                        <button class="btn-action btn-details">
                            <i class="fa fa-chevron-right"></i>
                        </button>
                    </div>
                </div>
            </div>
        </section>

        <!-- Блок мануалов на проверку -->
        <section class="section section-maintenances">
            <div class="section-title-wrapper">
                <i class="fa fa-wrench"></i>
                <h2>Мануалы на проверку</h2>
                <span class="section-badge">3</span>
            </div>

            <div class="maintenances-list">
                <div class="maintenance-card" v-for="i in 3" :key="i">
                    <div class="maintenance-card-header">
                        <div class="maintenance-icon">
                            <i class="fa fa-file-pdf-o"></i>
                        </div>
                        <div class="maintenance-info">
                            <p class="maintenance-title">Замена масла</p>
                            <span class="maintenance-moto">Bajaj Pulsar NS 125</span>
                        </div>
                        <span class="maintenance-status status-pending">На проверке</span>
                    </div>

                    <div class="maintenance-card-body">
                        <p class="maintenance-desc">
                            <i class="fa fa-align-left"></i>
                            Мануал по замене масла на мотоцикле Bajaj Pulsar NS 125. Подробная инструкция с фото.
                        </p>
                        <div class="maintenance-meta">
                            <span class="meta-item">
                                <i class="fa fa-list-ol"></i>
                                Шагов: 5
                            </span>
                            <span class="meta-item">
                                <i class="fa fa-clock-o"></i>
                                Создан: 14-07-2026 10:00
                            </span>
                            <span class="meta-item">
                                <i class="fa fa-user"></i>
                                Автор: Grisky
                            </span>
                        </div>
                    </div>

                    <div class="maintenance-card-actions">
                        <button class="btn-action btn-edit" title="Редактировать">
                            <i class="fa fa-pen"></i>
                        </button>
                        <button class="btn-action btn-approve" title="Одобрить">
                            <i class="fa fa-check"></i>
                        </button>
                        <button class="btn-action btn-reject" title="Отклонить">
                            <i class="fa fa-times"></i>
                        </button>
                        <button class="btn-action btn-details">
                            <i class="fa fa-eye"></i>
                        </button>
                    </div>
                </div>
            </div>
        </section>

        <!-- Дополнительная статистика -->
        <section class="section section-stats">
            <div class="section-title-wrapper">
                <i class="fa fa-bar-chart"></i>
                <h2>Статистика сайта</h2>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-card-icon">
                        <i class="fa fa-users"></i>
                    </div>
                    <div class="stat-card-content">
                        <p class="stat-card-title">Всего пользователей</p>
                        <p class="stat-card-value">1 247</p>
                        <span class="stat-card-change positive">
                            <i class="fa fa-arrow-up"></i> 12%
                        </span>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-card-icon">
                        <i class="fa fa-motorcycle"></i>
                    </div>
                    <div class="stat-card-content">
                        <p class="stat-card-title">Мотоциклов в системе</p>
                        <p class="stat-card-value">842</p>
                        <span class="stat-card-change positive">
                            <i class="fa fa-arrow-up"></i> 8%
                        </span>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-card-icon">
                        <i class="fa fa-wrench"></i>
                    </div>
                    <div class="stat-card-content">
                        <p class="stat-card-title">Обслуживаний</p>
                        <p class="stat-card-value">3 415</p>
                        <span class="stat-card-change positive">
                            <i class="fa fa-arrow-up"></i> 23%
                        </span>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-card-icon">
                        <i class="fa fa-file-text"></i>
                    </div>
                    <div class="stat-card-content">
                        <p class="stat-card-title">Мануалов</p>
                        <p class="stat-card-value">156</p>
                        <span class="stat-card-change negative">
                            <i class="fa fa-arrow-down"></i> 3%
                        </span>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<style scoped>
/* Общие стили для секций */
.section {
    background-color: var(--bg-primary);
    border: 2px solid var(--border-color);
    border-radius: 25px;
    padding: 28px;
    margin-bottom: 32px;
    transition: border-color 0.3s ease;
}

.section:hover {
    border-color: var(--accent-light);
}

.subtitle {
    text-align: center;
    color: var(--text-muted);
    max-width: 600px;
    margin: 0 auto;
    font-size: 1.05rem;
}

.section-title-wrapper {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 18px;
    margin-bottom: 28px;
    flex-wrap: wrap;
}

.section-title-wrapper i {
    font-size: 32px;
    color: var(--accent);
}

.section-title-wrapper h2 {
    margin-bottom: 0;
    font-size: 1.6rem;
}

.section-badge {
    background: var(--accent-light);
    color: var(--accent);
    border: 1px solid var(--border-color);
    border-radius: 20px;
    padding: 2px 14px;
    font-size: 14px;
    font-weight: 600;
    margin-left: 4px;
}

/* ===== USER CARDS ===== */
.users-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
}

.user-card {
    background: var(--bg-secondary);
    border: 2px solid var(--border-color);
    border-radius: 20px;
    padding: 20px;
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
}

.user-card:hover {
    transform: translateY(-4px);
    border-color: var(--accent);
    box-shadow: 0 8px 30px rgba(139, 92, 246, 0.1);
}

.user-card-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 16px;
    padding-bottom: 14px;
    border-bottom: 1px solid var(--border-color);
}

.user-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: var(--accent-light);
    border: 2px solid var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.user-avatar i {
    font-size: 22px;
    color: var(--accent);
}

.user-info {
    flex: 1;
    min-width: 0;
}

.user-username {
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 2px;
}

.user-role {
    font-size: 0.8rem;
    color: var(--accent);
    background: var(--accent-light);
    padding: 2px 12px;
    border-radius: 12px;
    border: 1px solid var(--border-color);
    display: inline-block;
}

.user-card-body {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 16px;
}

.user-detail {
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--text-secondary);
    font-size: 0.9rem;
}

.user-detail i {
    width: 16px;
    color: var(--text-muted);
    font-size: 0.85rem;
}

.user-status {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.8rem;
    font-weight: 500;
    padding: 4px 12px;
    border-radius: 12px;
    margin-top: 4px;
    width: fit-content;
}

.status-active {
    color: var(--success);
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.2);
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--success);
    display: inline-block;
    animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

.user-card-actions {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    padding-top: 14px;
    border-top: 1px solid var(--border-color);
}

/* ===== MAINTENANCE CARDS ===== */
.maintenances-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 20px;
}

.maintenance-card {
    background: var(--bg-secondary);
    border: 2px solid var(--border-color);
    border-radius: 20px;
    padding: 20px;
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
}

.maintenance-card:hover {
    transform: translateY(-4px);
    border-color: var(--warning);
    box-shadow: 0 8px 30px rgba(245, 158, 11, 0.1);
}

.maintenance-card-header {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    margin-bottom: 14px;
    padding-bottom: 14px;
    border-bottom: 1px solid var(--border-color);
    flex-wrap: wrap;
}

.maintenance-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: var(--accent-light);
    border: 2px solid var(--border-color);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.maintenance-icon i {
    font-size: 20px;
    color: var(--warning);
}

.maintenance-info {
    flex: 1;
    min-width: 0;
}

.maintenance-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 2px;
}

.maintenance-moto {
    font-size: 0.8rem;
    color: var(--text-muted);
}

.maintenance-status {
    font-size: 0.7rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 12px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    flex-shrink: 0;
    align-self: center;
}

.status-pending {
    color: var(--warning);
    background: rgba(245, 158, 11, 0.15);
    border: 1px solid rgba(245, 158, 11, 0.2);
}

.maintenance-card-body {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 16px;
}

.maintenance-desc {
    color: var(--text-secondary);
    font-size: 0.9rem;
    display: flex;
    gap: 8px;
    align-items: flex-start;
    line-height: 1.4;
    margin-bottom: 0;
}

.maintenance-desc i {
    color: var(--text-muted);
    margin-top: 2px;
    flex-shrink: 0;
}

.maintenance-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.8rem;
    color: var(--text-muted);
}

.meta-item i {
    font-size: 0.75rem;
}

.maintenance-card-actions {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    padding-top: 14px;
    border-top: 1px solid var(--border-color);
}

/* ===== BUTTON ACTIONS ===== */
.btn-action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 8px 14px;
    font-size: 0.8rem;
    font-weight: 500;
    border-radius: 12px;
    border: 1px solid var(--border-color);
    background: var(--bg-primary);
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.25s ease;
    min-width: 36px;
    height: 36px;
}

.btn-action i {
    font-size: 0.9rem;
}

.btn-action:hover {
    transform: translateY(-2px);
}

.btn-action:active {
    transform: translateY(0);
}

.btn-edit:hover {
    border-color: var(--accent);
    color: var(--accent);
    background: var(--accent-light);
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.2);
}

.btn-danger:hover {
    border-color: var(--danger);
    color: var(--danger);
    background: rgba(239, 68, 68, 0.15);
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.2);
}

.btn-ban:hover {
    border-color: var(--warning);
    color: var(--warning);
    background: rgba(245, 158, 11, 0.15);
    box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2);
}

.btn-approve:hover {
    border-color: var(--success);
    color: var(--success);
    background: rgba(16, 185, 129, 0.15);
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
}

.btn-reject:hover {
    border-color: var(--danger);
    color: var(--danger);
    background: rgba(239, 68, 68, 0.15);
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.2);
}

.btn-details:hover {
    border-color: var(--accent);
    color: var(--accent);
    background: var(--accent-light);
}

.btn-details {
    margin-left: auto;
}

/* ===== STATS SECTION ===== */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
}

.stat-card {
    background: var(--bg-secondary);
    border: 2px solid var(--border-color);
    border-radius: 20px;
    padding: 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    transition: all 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-4px);
    border-color: var(--accent);
    box-shadow: 0 8px 30px rgba(139, 92, 246, 0.1);
}

.stat-card-icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: var(--accent-light);
    border: 2px solid var(--border-color);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.stat-card-icon i {
    font-size: 22px;
    color: var(--accent);
}

.stat-card-content {
    flex: 1;
    min-width: 0;
}

.stat-card-title {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-bottom: 2px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

.stat-card-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 2px;
}

.stat-card-change {
    font-size: 0.75rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

.stat-card-change.positive {
    color: var(--success);
}

.stat-card-change.negative {
    color: var(--danger);
}

/* ===== RESPONSIVE ===== */

/* Планшеты и маленькие ноутбуки */
@media (max-width: 1024px) {
    .container {
        max-width: 92%;
        padding: 0 16px;
    }

    .section {
        padding: 22px;
    }

    .stats-grid {
        grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    }
}

/* Планшеты (вертикальная ориентация) */
@media (max-width: 768px) {
    .container {
        max-width: 96%;
        padding: 0 12px;
    }

    .section {
        padding: 18px;
        border-radius: 20px;
        margin-bottom: 24px;
    }

    .section-title-wrapper {
        gap: 12px;
        margin-bottom: 22px;
    }

    .section-title-wrapper i {
        font-size: 26px;
    }

    .section-title-wrapper h2 {
        font-size: 1.3rem;
    }

    .subtitle {
        font-size: 0.95rem;
        padding: 0 8px;
    }

    .users-list {
        grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
        gap: 16px;
    }

    .maintenances-list {
        grid-template-columns: 1fr;
    }

    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 14px;
    }

    .user-card {
        padding: 16px;
    }

    .maintenance-card {
        padding: 16px;
    }

    .stat-card {
        padding: 16px;
        gap: 12px;
    }

    .stat-card-icon {
        width: 40px;
        height: 40px;
    }

    .stat-card-icon i {
        font-size: 18px;
    }

    .stat-card-value {
        font-size: 1.3rem;
    }

    .btn-action {
        padding: 6px 10px;
        font-size: 0.75rem;
        height: 32px;
        min-width: 32px;
    }

    .btn-action i {
        font-size: 0.8rem;
    }

    .section-badge {
        font-size: 12px;
        padding: 1px 10px;
    }
}

/* Мобильные телефоны */
@media (max-width: 480px) {
    .container {
        max-width: 100%;
        padding: 0 10px;
    }

    .section {
        padding: 14px;
        border-radius: 16px;
        margin-bottom: 18px;
    }

    .section-title-wrapper {
        gap: 10px;
        margin-bottom: 18px;
    }

    .section-title-wrapper i {
        font-size: 20px;
    }

    .section-title-wrapper h2 {
        font-size: 1.1rem;
    }

    .subtitle {
        font-size: 0.85rem;
    }

    .users-list {
        grid-template-columns: 1fr;
        gap: 14px;
    }

    .maintenances-list {
        grid-template-columns: 1fr;
        gap: 14px;
    }

    .stats-grid {
        grid-template-columns: 1fr 1fr;
        gap: 10px;
    }

    .user-card {
        padding: 14px;
        border-radius: 16px;
    }

    .user-card-header {
        gap: 10px;
        margin-bottom: 12px;
        padding-bottom: 10px;
    }

    .user-avatar {
        width: 40px;
        height: 40px;
    }

    .user-avatar i {
        font-size: 18px;
    }

    .user-username {
        font-size: 0.95rem;
    }

    .user-role {
        font-size: 0.7rem;
        padding: 1px 10px;
    }

    .user-detail {
        font-size: 0.8rem;
        gap: 8px;
    }

    .user-card-actions {
        gap: 6px;
        padding-top: 10px;
    }

    .maintenance-card {
        padding: 14px;
        border-radius: 16px;
    }

    .maintenance-card-header {
        gap: 10px;
        margin-bottom: 10px;
        padding-bottom: 10px;
    }

    .maintenance-icon {
        width: 36px;
        height: 36px;
    }

    .maintenance-icon i {
        font-size: 16px;
    }

    .maintenance-title {
        font-size: 0.9rem;
    }

    .maintenance-desc {
        font-size: 0.8rem;
    }

    .maintenance-meta {
        gap: 8px;
    }

    .meta-item {
        font-size: 0.7rem;
    }

    .maintenance-card-actions {
        gap: 6px;
        padding-top: 10px;
    }

    .stat-card {
        padding: 12px;
        gap: 10px;
        border-radius: 16px;
        flex-direction: column;
        align-items: flex-start;
    }

    .stat-card-icon {
        width: 36px;
        height: 36px;
    }

    .stat-card-icon i {
        font-size: 16px;
    }

    .stat-card-title {
        font-size: 0.7rem;
    }

    .stat-card-value {
        font-size: 1.1rem;
    }

    .stat-card-change {
        font-size: 0.65rem;
    }

    .btn-action {
        padding: 5px 8px;
        font-size: 0.7rem;
        height: 28px;
        min-width: 28px;
        border-radius: 10px;
    }

    .btn-action i {
        font-size: 0.7rem;
    }

    .section-badge {
        font-size: 10px;
        padding: 1px 8px;
    }
}

/* Очень маленькие экраны */
@media (max-width: 360px) {
    .stats-grid {
        grid-template-columns: 1fr;
    }

    .section {
        padding: 10px;
    }

    .user-card-actions {
        flex-wrap: wrap;
        justify-content: center;
    }

    .maintenance-card-actions {
        flex-wrap: wrap;
        justify-content: center;
    }

    .btn-details {
        margin-left: 0;
    }
}
</style>