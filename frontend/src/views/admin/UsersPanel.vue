<template>
    <!-- === HEADER === -->
        <header class="page-header">
            <div class="header-left">
                <h2>Пользователи</h2>
                <p class="header-subtitle">
                    Управление пользователями платформы.
                </p>
            </div>

            <div class="header-right">
                <button><i class="fa fa-plus"></i> Добавить пользователя</button>
                <i class="fa fa-bell notification-icon"></i>
                <div class="profile-wrapper">
                    <img src="/BaseAvatar.jpg" alt="avatar" class="profile-img">
                    <button class="dropdown-trigger" @click="welcomeDropdownActive = !welcomeDropdownActive">
                        <i class="fa" :class="welcomeDropdownActive ? 'fa-angle-up' : 'fa-angle-down'"></i>
                    </button>
                    <div v-if="welcomeDropdownActive" class="dropdown-list">
                        <ul>
                            <li><button class="dropdown-item">Профиль</button></li>
                            <li><button class="dropdown-item">Настройки</button></li>
                            <li><button @click="logout" class="dropdown-item">Выйти</button></li>
                        </ul>
                    </div>
                </div>
            </div>
        </header>

        <!-- === STATISTIC === -->
         <section>
            <div class="stat-cards">
                <div class="stat-card">
                    <div class="card-icon">
                        <i class="fa fa-users"></i>
                    </div>
                    <div class="card-body">
                        <p class="card-title">Всего пользователей</p>
                        <p class="card-value">{{ usersCount }}</p>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="card-icon success">
                        <i class="fa fa-user-plus"></i>
                    </div>
                    <div class="card-body">
                        <p class="card-title">Активных</p>
                        <p class="card-value">{{ activeUsers }}</p>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="card-icon danger">
                        <i class="fa fa-times"></i>
                    </div>
                    <div class="card-body">
                        <p class="card-title">Заблокированных</p>
                        <p class="card-value">{{ blockUsers }}</p>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="card-icon">
                        <i class="fa fa-clock"></i>
                    </div>
                    <div class="card-body">
                        <p class="card-title">Администраторв</p>
                        <p class="card-value">{{ adminUsers }}</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- === TABLE === -->
        <section class="table-section">
            <div class="table-filters">
                <div class="inputs-group">
                    <div class="inputs-wrapper">
                        <label>
                            Поиск
                            <input type="search" placeholder="Поиск по имени, email или ID">
                        </label>
                        <label>
                            Роль
                            <select>
                                <option value="motorcyclist">Мотоциклист</option>
                                <option value="clubMember">Член мотоклуба</option>
                                <option value="amdin">Админ</option>
                            </select>
                        </label>
                    </div>
                    <div class="inputs-wrapper">
                        <label>
                            Статус
                            <select>
                                <option value="active">Активен</option>
                                <option value="ban">Заблокирован</option>
                            </select>
                        </label>
                        <label>
                            Дата регистрации
                            <input type="date">
                        </label>
                    </div>
                </div>

                <button class="outline-btn"><i class="fa fa-refresh"></i> Сброисить фильтры</button>
            </div>

            <div class="users-table-wrapper">
                <div class="table-header">
                    <span class="th">Пользователь</span>
                    <span class="th">Роль</span>
                    <span class="th">Статус</span>
                    <span class="th">Дата регистрации</span>
                    <span class="th">Действия</span>
                </div>
                <div class="table-body">
                    <div class="tr">
                        <div class="td user-cell">
                            <img src="/BaseAvatar.jpg" alt="" class="user-img">
                            <div class="user-info">
                                <p class="user-name">Grisky</p>
                                <p class="user-email">grisky@icloud.com</p>
                            </div>
                        </div>
                        <div class="td role-cell">
                            <span>Администратор</span>
                        </div>
                        <div class="td status-cell">
                            <span>Активен</span>
                        </div>
                        <div class="td date-cell">
                            <span>26.08.2008</span>
                        </div>
                        <div class="td table-actions-wrapper">
                            <button class="btn-small"><i class="fa fa-pen"></i></button>
                            <button class="btn-small danger"><i class="fa fa-trash"></i></button>
                        </div>
                    </div>
                </div>
                <div class="table-footer">
                    <button class="outline-btn" style="width: 100%;">Все записи <i class="fa fa-chevron-right"></i></button>
                </div>
            </div>
            <div class="table-paginate">
                <p class="paginate-show">Показано 1-10 из 1024</p>
                
                <div class="paginate-ui">
                    <button class="outline-btn"><i class="fa fa-angle-left"></i></button>
                    <div class="paginate-btns">
                        <button class="outline-btn paginate active">1</button>
                        <button class="outline-btn paginate">1</button>
                        <button class="outline-btn paginate">1</button>
                        <p>...</p>
                        <button class="outline-btn paginate">125</button>
                    </div>
                    <button class="outline-btn"><i class="fa fa-angle-right"></i></button>
                </div>

                <div class="show-per-page">
                    <select>
                        <option value="10">10</option>
                        <option value="20">20</option>
                        <option value="50">50</option>
                        <option value="100">100</option>
                    </select>
                </div>
            </div>
        </section>
</template>

<script>
export default {
    data() {
        return {
            usersCount: 0,
            activeUsers: 0,
            blockUsers: 0,
            adminUsers: 0
        }
    }
}
</script>

<style scoped>
/* ===== HEADER ===== */
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    flex-wrap: wrap;
    gap: 16px;
}
.header-left h2 {
    margin: 0 0 12px 0;
    font-size: 24px;
}

.header-subtitle {
    font-size: 14px;
    color: var(--text-secondary);
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
    background: #181824;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 8px;
    min-width: 140px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.5);
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
    color: #ccc;
    text-align: left;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
}
.dropdown-item:hover {
    background: rgba(255,255,255,0.05);
}

@media (max-width: 720px) {
    .header-right {
        display: none;
    }
}


/* === STATISTIC === */
.stat-cards {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(1, 1fr);
    gap: 16px;
}

.stat-card {
    display: flex;
    gap: 16px;
    justify-content: center;
    padding: 12px 14px;
    background-color: var(--bg-card);
    border-radius: 10px;
    transition: all 0.3s ease;
}
.stat-card:hover {
    background-color: var(--accent-trans);
}

.card-icon {
    width: 48px;
    height: 48px;
    font-size: 18px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 10px;
    background-color: var(--accent-trans);
    color: var(--accent);
}
.card-icon.success {
    background-color: var(--success-trans);
    color: var(--success);
}
.card-icon.danger {
    background-color: var(--danger-trans);
    color: var(--danger);
}

.card-title {
    font-size: 14px;
    color: var(--text-secondary);
}

.card-value {
    font-size: 21px;
    font-weight: 600;
}

@media (max-width: 1000px) {
    .stat-cards {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(2, 1fr);
    }
}

@media (max-width: 1580px) {
    .stat-cards {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(2, 1fr);
    }
}

@media (max-width: 520px) {
    .stat-cards {
        grid-template-columns: repeat(1, 1fr);
        grid-template-rows: repeat(3, 1fr);
    }
    .stat-card {
        justify-content: center;
        align-items: center;
    }
}


/* === TABLE FILTERS AND TABLE === */
.table-section {
    padding: 14px 16px;
    background-color: var(--bg-card);
    border-radius: 10px;
}

/* filters */

.table-filters {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.inputs-group {
    display: flex;
    gap: 14px;
    justify-content: center;
    align-items: center;
}

@media (max-width: 1200px) {
    .table-filters {
        flex-direction: column;
        gap: 4px;
    }
    .table-filters button {
        width: 100%;
    }
}

@media (max-width: 1000px) {
    .inputs-group {
        flex-direction: column;
        align-items: normal;
    }
    .inputs-wrapper {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(1, 1fr);
        gap: 10px;
    }

    .table-paginate {
        flex-direction: column;
        gap: 10px;
    }
}

@media (max-width: 520px) {
    .inputs-wrapper {
        grid-template-columns: repeat(1, 1fr);
    }
}

/* table */
.users-table-wrapper {
    background: #181824;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 16px;
    overflow-x: auto;
    margin-bottom: 16px;
}

.table-header {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 8px;
    padding: 12px 16px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 13px;
    color: #8b8b9e;
    font-weight: 500;
    min-width: 700px;
}

.table-body {
    display: flex;
    flex-direction: column;
}

.tr {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 8px;
    padding: 14px 16px;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.03);
    transition: background 0.2s;
    cursor: pointer;
    min-width: 700px;
}

.tr:hover {
    background: rgba(255,255,255,0.02);
}

.td {
    font-size: 14px;
}

.last-reg-cards {
    display: flex;
    flex-direction: column;
}

.user-cell {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
}

.user-info {
    display: flex;
    flex-direction: column;
    margin-bottom: 8px;
}

.user-name {
    font-weight: 600;
}
.user-email {
    font-size: 14px;
    color: var(--text-secondary);
}

.user-img {
    width: 38px;
    height: 38px;
    border-radius: 50%;
}

.table-actions-wrapper {
    display: flex;
    gap: 10px;
}

.icon-square {
    width: 30px;
    height: 30px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
}

.tr:hover .action-cell { color: #a78bfa; }

.table-footer {
    padding: 16px;
    text-align: center;
}

.btn-small.danger {
    background-color: var(--danger-trans);
    color: var(--danger);
}

/* paginate */
.table-paginate {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.paginate-show {
    color: var(--text-secondary);
}

.paginate-ui {
    display: flex;
    align-items: center;
    gap: 14px;
}

.paginate-btns {
    display: flex;
    gap: 8px;
}

.outline-btn.paginate {
    border: none;
}

.outline-btn.paginate.active {
    background-color: var(--accent-trans);
}

.show-per-page {
    display: flex;
    gap: 16px;
}

/* === ANIMATIONS === */
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
</style>