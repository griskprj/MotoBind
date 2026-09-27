<template>
    <LoadingOverlay :isLoading="loading" text="Загрузка пользователей..."/>

    <!-- === HEADER === -->
    <Header
        title="Пользователи"
        subtitle="Управление пользователями платформы"
    />

    <!-- === STATISTIC === -->
    <section>
        <div class="stat-cards">
            <div class="stat-card">
                <div class="card-icon">
                    <i class="fa fa-users"></i>
                </div>
                <div class="card-body">
                    <p class="card-title">Всего пользователей</p>
                    <p class="card-value">{{ stats.total || 0 }}</p>
                </div>
            </div>

            <div class="stat-card">
                <div class="card-icon success">
                    <i class="fa fa-user-plus"></i>
                </div>
                <div class="card-body">
                    <p class="card-title">Активных</p>
                    <p class="card-value">{{ stats.active || 0 }}</p>
                </div>
            </div>

            <div class="stat-card">
                <div class="card-icon danger">
                    <i class="fa fa-times"></i>
                </div>
                <div class="card-body">
                    <p class="card-title">Заблокированных</p>
                    <p class="card-value">{{ stats.banned || 0 }}</p>
                </div>
            </div>

            <div class="stat-card">
                <div class="card-icon">
                    <i class="fa fa-clock"></i>
                </div>
                <div class="card-body">
                    <p class="card-title">Администраторов</p>
                    <p class="card-value">{{ stats.admin || 0 }}</p>
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
                        <input
                            type="search"
                            v-model="filters.search"
                            @input="debouncedSearch"
                            placeholder="Поиск по имени, email или ID"
                        >
                    </label>
                    <label>
                        Роль
                        <select v-model="filters.role" @change="applyFilters">
                            <option value="">Все роли</option>
                            <option value="motorcyclist">Мотоциклист</option>
                            <option value="club_member">Член мотоклуба</option>
                            <option value="admin">Админ</option>
                        </select>
                    </label>
                </div>
                <div class="inputs-wrapper">
                    <label>
                        Статус
                        <select v-model="filters.status" @change="applyFilters">
                            <option value="">Все статусы</option>
                            <option value="active">Активен</option>
                            <option value="banned">Заблокирован</option>
                        </select>
                    </label>
                    <label>
                        Дата регистрации
                        <input type="date" v-model="filters.date_from" @change="applyFilters">
                    </label>
                </div>
            </div>

            <div class="filters-actions">
                <button class="outline-btn" @click="resetFilters"><i class="fa fa-refresh"></i> Сбросить фильтры</button>
                <button @click="showAddUserModal = true"><i class="fa fa-plus"></i> Добавить пользователя</button>
            </div>
        </div>

        <!-- Loading state -->
        <div v-if="loading" class="loading-state">
            <i class="fa fa-spinner fa-spin"></i> Загрузка...
        </div>

        <div v-else class="users-table-wrapper">
            <div class="table-header">
                <span class="th">Пользователь</span>
                <span class="th">Роль</span>
                <span class="th">Статус</span>
                <span class="th">Дата регистрации</span>
                <span class="th">Последний вход</span>
                <span class="th">Действия</span>
            </div>
            <div class="table-body">
                <div v-if="users.length === 0" class="tr empty-state">
                    <div class="td" style="grid-column: 1 / -1; text-align: center; color: var(--text-secondary);">
                        Пользователи не найдены
                    </div>
                </div>
                <div
                    v-for="user in users"
                    :key="user.id"
                    class="tr"
                >
                    <div class="td user-cell">
                        <img
                            :src="getAvatarUrl(user.avatar)"
                            alt=""
                            class="user-img"
                            @error="(e) => e.target.src = '/BaseAvatar.webp'"
                        >
                        <div class="user-info">
                            <p class="user-name">{{ user.username }}</p>
                            <p class="user-email">{{ user.email }}</p>
                        </div>
                    </div>
                    <div class="td role-cell">
                        <span>{{ getUserRoleName(user.role) }}</span>
                    </div>
                    <div class="td status-cell">
                        <span :class="getStatusClass(user.status)">{{ getUserStatusName(user.status) }}</span>
                    </div>
                    <div class="td date-cell">
                        <span>{{ formatDate(user.created_at) }}</span>
                    </div>
                    <div class="td last-login-cell">
                        <span>{{ formatDate(user.last_login) }}</span>
                    </div>
                    <div class="td table-actions-wrapper">
                        <button class="btn-small" @click="openEditUserModal(user)"><i class="fa fa-pen"></i></button>
                        <button
                            v-if="user.status === 'active'"
                            class="btn-small danger"
                            @click="banUser(user)"
                            title="Заблокировать"
                        >
                            <i class="fa fa-ban"></i>
                        </button>
                        <button
                            v-else-if="user.status === 'banned'"
                            class="btn-small success"
                            @click="unbanUser(user)"
                            title="Разблокировать"
                        >
                            <i class="fa fa-check"></i>
                        </button>
                        <button
                            class="btn-small danger"
                            @click="openDeleteUserModal(user)"
                            title="Удалить"
                        >
                            <i class="fa fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- === PAGINATION === -->
        <div v-if="!loading" class="table-paginate">
            <p class="paginate-show">
                Показано {{ (pagination.current_page - 1) * pagination.per_page + 1 }}-
                {{ Math.min(pagination.current_page * pagination.per_page, pagination.total) }}
                из {{ pagination.total }}
            </p>

            <div class="paginate-ui">
                <button
                    class="outline-btn"
                    @click="goToPage(pagination.current_page - 1)"
                    :disabled="!pagination.has_prev"
                >
                    <i class="fa fa-angle-left"></i>
                </button>
                <div class="paginate-btns">
                    <button
                        v-for="page in visiblePages"
                        :key="page"
                        class="outline-btn paginate"
                        :class="{ active: page === pagination.current_page }"
                        @click="goToPage(page)"
                    >
                        {{ page }}
                    </button>
                    <p v-if="showEllipsisEnd">...</p>
                    <button
                        v-if="showLastPage"
                        class="outline-btn paginate"
                        @click="goToPage(pagination.pages)"
                    >
                        {{ pagination.pages }}
                    </button>
                </div>
                <button
                    class="outline-btn"
                    @click="goToPage(pagination.current_page + 1)"
                    :disabled="!pagination.has_next"
                >
                    <i class="fa fa-angle-right"></i>
                </button>
            </div>

            <div class="show-per-page">
                <select v-model="pagination.per_page" @change="changePerPage">
                    <option :value="10">10</option>
                    <option :value="20">20</option>
                    <option :value="50">50</option>
                    <option :value="100">100</option>
                </select>
            </div>
        </div>
    </section>

    <AddUserModal
        :is-open="showAddUserModal"
        @close="showAddUserModal = false"
        @saved="onUserSaved"
    />

    <EditUserModal
        :is-open="showEditUserModal"
        :user="selectedUser"
        @close="closeEditUserModal"
        @saved="onUserSaved"
    />

    <DeleteUserModal
        :is-open="showDeleteUserModal"
        :user="selectedUser"
        @close="closeDeleteUserModal"
        @submit="deleteUser"
    />
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import api from '@/api/api'
import AddUserModal from '@/components/modals/admin/AddUserModal.vue'
import EditUserModal from '@/components/modals/admin/EditUserModal.vue'
import DeleteUserModal from '@/components/modals/admin/DeleteUserModal.vue'
import Header from '@/components/Header.vue'
import LoadingOverlay from '@/components/LoadingOverlay.vue'
import { useToast } from '@/composables/useToast'
import { getAvatarUrl } from '@/utils/mediaUrl'

// ===== Composable =====
const toast = useToast()

// ===== State =====
const loading = ref(false)
const users = ref([])
const stats = ref({
    total: 0,
    active: 0,
    banned: 0,
    admin: 0,
})

const pagination = ref({
    current_page: 1,
    per_page: 10,
    total: 0,
    pages: 0,
    has_prev: false,
    has_next: false,
})

const filters = ref({
    search: '',
    role: '',
    status: '',
    date_from: '',
    date_to: '',
})

let searchTimeout = null

// Модалки
const showAddUserModal = ref(false)
const showEditUserModal = ref(false)
const showDeleteUserModal = ref(false)
const selectedUser = ref(null)

// ===== Computed =====
const visiblePages = computed(() => {
    const current = pagination.value.current_page
    const total = pagination.value.pages
    const delta = 2
    const range = []

    for (let i = Math.max(2, current - delta); i <= Math.min(total - 1, current + delta); i++) {
        range.push(i)
    }

    if (current - delta > 2) range.unshift('...')
    if (current + delta < total - 1) range.push('...')

    range.unshift(1)

    if (total > 1) range.push(total)

    return range.filter((v, i, a) => a.indexOf(v) === i)
})

const showEllipsisEnd = computed(() => {
    const current = pagination.value.current_page
    const total = pagination.value.pages
    return total > 1 && current + 2 < total - 1
})

const showLastPage = computed(() => {
    const total = pagination.value.pages
    return total > 1 && pagination.value.current_page + 2 < total
})

// ===== Lifecycle =====
onMounted(() => {
    loadUsers()
})

// ===== Methods =====
async function loadUsers() {
    loading.value = true
    try {
        const params = {
            page: pagination.value.current_page,
            per_page: pagination.value.per_page,
            ...filters.value,
        }

        // Убираем пустые параметры
        Object.keys(params).forEach(key => {
            if (!params[key]) delete params[key]
        })

        const response = await api.get('/admin/users', { params })
        const data = response.data

        users.value = data.users || []
        pagination.value = {
            current_page: data.current_page,
            per_page: data.per_page,
            total: data.total,
            pages: data.pages,
            has_prev: data.has_prev,
            has_next: data.has_next,
        }
        stats.value = data.stats || {
            total: 0,
            active: 0,
            banned: 0,
            admin: 0,
        }
    } catch (error) {
        console.error('Error loading users:', error)
        toast.error(error.response?.data?.message || 'Не удалось загрузить пользователей')
    } finally {
        loading.value = false
    }
}

function onUserSaved() {
    showAddUserModal.value = false
    showEditUserModal.value = false
    selectedUser.value = null
    loadUsers()
}

function goToPage(page) {
    if (page < 1 || page > pagination.value.pages) return
    pagination.value.current_page = page
    loadUsers()
}

function changePerPage() {
    pagination.value.current_page = 1
    loadUsers()
}

function applyFilters() {
    pagination.value.current_page = 1
    loadUsers()
}

function debouncedSearch() {
    clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => {
        applyFilters()
    }, 500)
}

function resetFilters() {
    filters.value = {
        search: '',
        role: '',
        status: '',
        date_from: '',
        date_to: '',
    }
    pagination.value.current_page = 1
    loadUsers()
}

// Вспомогательные методы
function getUserRoleName(role) {
    const roles = {
        'admin': 'Администратор',
        'motorcyclist': 'Мотоциклист',
        'club_member': 'Член клуба',
    }
    return roles[role] || role
}

function getUserStatusName(status) {
    const statuses = {
        'active': 'Активен',
        'banned': 'Заблокирован',
        'pending': 'Ожидает',
    }
    return statuses[status] || status
}

function getStatusClass(status) {
    const classes = {
        'active': 'status-active',
        'banned': 'status-banned',
        'pending': 'status-pending',
    }
    return classes[status] || ''
}

function formatDate(date) {
    if (!date) return '-'
    const d = new Date(date)
    return d.toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
    })
}

// Действия с пользователями
async function banUser(user) {
    if (!confirm(`Заблокировать пользователя ${user.username}?`)) return
    try {
        await api.post(`/admin/user/${user.id}/ban`)
        await loadUsers()
        toast.success('Пользователь заблокирован')
    } catch (error) {
        console.error('Error banning user:', error)
        toast.error(error.response?.data?.message || 'Ошибка при блокировке')
    }
}

async function unbanUser(user) {
    if (!confirm(`Разблокировать пользователя ${user.username}?`)) return
    try {
        await api.post(`/admin/user/${user.id}/unban`)
        await loadUsers()
        toast.success('Пользователь разблокирован')
    } catch (error) {
        console.error('Error unbanning user:', error)
        toast.error(error.response?.data?.message || 'Ошибка при разблокировке')
    }
}

async function deleteUser(userId) {
    try {
        await api.delete(`/admin/user/${userId}`)
        await loadUsers()
        closeDeleteUserModal()
        toast.success('Пользователь удалён')
    } catch (error) {
        console.error('Error deleting user:', error)
        toast.error(error.response?.data?.message || 'Ошибка при удалении')
    }
}

function openDeleteUserModal(user) {
    showDeleteUserModal.value = true
    selectedUser.value = user
}

function closeDeleteUserModal() {
    showDeleteUserModal.value = false
    selectedUser.value = null
}

function openEditUserModal(user) {
    showEditUserModal.value = true
    selectedUser.value = user
}

function closeEditUserModal() {
    showEditUserModal.value = false
    selectedUser.value = null
}
</script>

<style scoped>
/* ============================================
   STATISTIC CARDS
   ============================================ */
.stat-cards {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
}

.stat-card {
    display: flex;
    gap: 16px;
    align-items: center;
    padding: 12px 14px;
    background-color: var(--bg-card);
    border-radius: var(--radius-md);
    border: 1px solid var(--border-light);
    transition: all var(--transition-base);
    min-width: 0;
}
.stat-card:hover {
    background-color: var(--accent-trans);
    border-color: var(--accent);
}

.card-icon {
    width: 48px;
    height: 48px;
    min-height: 48px; /* перебиваем reset.scss */
    font-size: 18px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: var(--radius-md);
    background-color: var(--accent-trans);
    color: var(--accent);
    flex-shrink: 0;
}
.card-icon.success { background-color: var(--success-trans); color: var(--success-text); }
.card-icon.danger  { background-color: var(--danger-trans);  color: var(--danger-text); }

.card-body { min-width: 0; }

.card-title {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.card-value {
    font-size: 21px;
    font-weight: var(--fw-semibold);
    color: var(--text-primary);
    margin: 0;
}

/* ============================================
   TABLE SECTION
   ============================================ */
.table-section {
    padding: 14px 16px;
    background-color: var(--bg-card);
    border-radius: var(--radius-md);
    border: 1px solid var(--border-light);
    min-width: 0;
}

/* ============================================
   FILTERS
   ============================================ */
.table-filters {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 16px;
    gap: 16px;
    flex-wrap: wrap;
}

.inputs-group {
    display: flex;
    gap: 14px;
    align-items: flex-end;
    flex-wrap: wrap;
    min-width: 0;
}

.inputs-wrapper {
    display: flex;
    gap: 14px;
    flex-wrap: wrap;
    min-width: 0;
}

.inputs-wrapper label {
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 13px;
    font-weight: var(--fw-medium);
    color: var(--text-secondary);
    min-width: 0;
}

.inputs-wrapper input,
.inputs-wrapper select {
    padding: 8px 14px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: var(--radius-md);
    color: var(--text-primary);
    font-size: 14px;
    outline: none;
    transition: border var(--transition-fast), box-shadow var(--transition-fast);
    min-width: 150px;
    max-width: 100%;
}
.inputs-wrapper input:focus,
.inputs-wrapper select:focus {
    border-color: var(--accent);
    box-shadow: var(--shadow-focus);
}
.inputs-wrapper input::placeholder { color: var(--text-muted); }

.inputs-wrapper select {
    appearance: none;
    background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2364748B' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: right 10px center;
    background-size: 14px;
    padding-right: 36px;
    cursor: pointer;
}
.inputs-wrapper select option {
    background: var(--bg-input);
    color: var(--text-primary);
}

.filters-actions {
    display: flex;
    gap: 8px;
    flex-shrink: 0;
}

/* ============================================
   TABLE
   ============================================ */
.users-table-wrapper {
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-lg);
    overflow-x: auto;
    margin-bottom: 16px;
    -webkit-overflow-scrolling: touch;
}

.table-header {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1.2fr 1.2fr 1fr;
    gap: 8px;
    padding: 12px 16px;
    border-bottom: 1px solid var(--border-light);
    font-size: 13px;
    color: var(--text-muted);
    font-weight: var(--fw-medium);
    min-width: 760px;
}

.table-body { display: flex; flex-direction: column; }

.tr {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1.2fr 1.2fr 1fr;
    gap: 8px;
    padding: 14px 16px;
    align-items: center;
    border-bottom: 1px solid var(--border-light);
    transition: background var(--transition-fast);
    cursor: pointer;
    min-width: 760px;
}
.tr:hover { background: var(--border-light); }
.tr:last-child { border-bottom: none; }

.td {
    font-size: 14px;
    color: var(--text-primary);
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* User cell */
.user-cell {
    display: flex;
    align-items: center;
    gap: 12px;
    min-width: 0;
}
.user-img {
    width: 38px;
    height: 38px;
    min-height: 38px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid var(--border-color);
    flex-shrink: 0;
}
.user-info {
    display: flex;
    flex-direction: column;
    min-width: 0;
}
.user-name {
    font-weight: var(--fw-semibold);
    color: var(--text-primary);
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.user-email {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* Actions */
.table-actions-wrapper {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
}

/* btn-small: перебиваем reset.scss */
.btn-small {
    width: 32px;
    height: 32px;
    min-height: 32px;
    padding: 0;
    border-radius: var(--radius-md);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    background-color: var(--bg-secondary);
    border: none;
    cursor: pointer;
    transition: all var(--transition-base);
    color: var(--text-secondary);
    flex-shrink: 0;
}
.btn-small:hover {
    background-color: var(--bg-card);
    color: var(--accent-text);
    box-shadow: 0 0 0 1px var(--accent);
}
.btn-small.danger {
    background-color: var(--danger-trans);
    color: var(--danger-text);
}
.btn-small.danger:hover {
    background-color: var(--danger-trans);
    opacity: 0.8;
    box-shadow: none;
}
.btn-small.success {
    background-color: var(--success-trans);
    color: var(--success-text);
}
.btn-small.success:hover {
    background-color: var(--success-trans);
    opacity: 0.8;
    box-shadow: none;
}

/* Status badges */
.status-active,
.status-banned,
.status-pending {
    display: inline-block;
    padding: 2px 14px;
    border-radius: var(--radius-full);
    font-size: 12px;
    font-weight: var(--fw-medium);
    white-space: nowrap;
}
.status-active  { background: var(--success-trans); color: var(--success-text); }
.status-banned  { background: var(--danger-trans);  color: var(--danger-text); }
.status-pending { background: var(--warning-trans); color: var(--warning-text); }

/* ============================================
   PAGINATION
   ============================================ */
.table-paginate {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
}

.paginate-show {
    color: var(--text-secondary);
    font-size: 14px;
    margin: 0;
}

.paginate-ui {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
}

.paginate-btns {
    display: flex;
    gap: 6px;
    align-items: center;
    flex-wrap: wrap;
}
.paginate-btns p { margin: 0; color: var(--text-muted); }

.outline-btn.paginate {
    border: none;
    min-width: 36px;
    height: 36px;
    min-height: 36px;
    padding: 0 8px;
    border-radius: var(--radius-md);
    background: transparent;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all var(--transition-base);
    font-size: 14px;
}
.outline-btn.paginate.active {
    background-color: var(--accent-trans);
    color: var(--accent-text);
}
.outline-btn.paginate:hover:not(.active) {
    background-color: var(--border-light);
}

.paginate-ui button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.show-per-page { display: flex; gap: 16px; }
.show-per-page select {
    padding: 8px 14px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: var(--radius-md);
    color: var(--text-primary);
    font-size: 14px;
    outline: none;
    cursor: pointer;
    transition: border var(--transition-fast), box-shadow var(--transition-fast);
}
.show-per-page select:focus {
    border-color: var(--accent);
    box-shadow: var(--shadow-focus);
}

/* ============================================
   LOADING
   ============================================ */
.loading-state {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 40px 0;
    color: var(--text-secondary);
    gap: 12px;
}
.loading-state .fa-spinner { font-size: 24px; color: var(--accent); }

/* ============================================
   АДАПТИВ
   Шкала: 1200 → 1000 → 820 → 640 → 480 → 400
   ============================================ */

/* --- Планшет: фильтры в колонку, stat-cards 2×2 --- */
@media (max-width: 1200px) {
    .stat-cards { grid-template-columns: repeat(2, 1fr); }

    .table-filters { flex-direction: column; align-items: stretch; gap: 12px; }
    .table-filters button { width: 100%; }

    .inputs-group { width: 100%; }
    .inputs-wrapper { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; width: 100%; }
    .inputs-wrapper input,
    .inputs-wrapper select { min-width: 0; width: 100%; }

    .filters-actions { flex-direction: row; }
    .filters-actions button { flex: 1; }
}

/* --- Мобильный планшет: карточки таблицы --- */
@media (max-width: 820px) {
    .table-header { display: none; }

    .tr {
        grid-template-columns: 1fr;
        gap: 6px;
        padding: 14px;
        border: 1px solid var(--border-light);
        border-radius: var(--radius-md);
        margin-bottom: 8px;
        background: var(--bg-primary);
        min-width: unset;
    }
    .tr:hover { background: var(--bg-primary); }

    .user-cell {
        order: 1;
        margin-bottom: 4px;
    }

    /* Все информационные ячейки — с подписью */
    .td:not(.user-cell):not(.table-actions-wrapper) {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 8px;
        padding: 2px 0;
        font-size: 13px;
    }

    /* Подписи через ::before (data-label в разметке не задан) */
    .role-cell::before      { content: "Роль";              color: var(--text-muted); font-weight: var(--fw-normal); }
    .status-cell::before    { content: "Статус";            color: var(--text-muted); font-weight: var(--fw-normal); }
    .date-cell::before      { content: "Дата регистрации";  color: var(--text-muted); font-weight: var(--fw-normal); }
    .last-login-cell::before{ content: "Последний вход";    color: var(--text-muted); font-weight: var(--fw-normal); }

    .role-cell      { order: 2; }
    .status-cell    { order: 3; }
    .date-cell      { order: 4; }
    .last-login-cell{ order: 5; }

    /* Кнопки — отдельной строкой */
    .table-actions-wrapper {
        order: 6;
        margin-top: 8px;
        padding-top: 10px;
        border-top: 1px solid var(--border-light);
        justify-content: flex-end;
    }

    /* Пустое состояние */
    .tr.empty-state .td { justify-content: center; }
}

/* --- Мобильные --- */
@media (max-width: 640px) {
    .table-section { padding: 12px; }

    .inputs-wrapper { grid-template-columns: 1fr; gap: 8px; }

    .filters-actions { flex-direction: column; }
    .filters-actions button { width: 100%; }

    .table-paginate {
        flex-direction: column;
        align-items: stretch;
        gap: 12px;
    }
    .paginate-show { text-align: center; font-size: 13px; }
    .paginate-ui { justify-content: center; }
    .show-per-page { justify-content: center; }
    .show-per-page select { width: 100%; }

    /* Ограничиваем пагинацию, чтобы не разрасталась */
    .paginate-btns { gap: 4px; }
    .outline-btn.paginate { min-width: 32px; height: 32px; min-height: 32px; padding: 0 6px; font-size: 13px; }
}

/* --- Очень узкие --- */
@media (max-width: 480px) {
    .stat-card { padding: 10px 12px; gap: 12px; }
    .card-icon { width: 40px; height: 40px; min-height: 40px; font-size: 16px; }
    .card-title { font-size: 12px; }
    .card-value { font-size: 18px; }

    .user-img { width: 34px; height: 34px; min-height: 34px; }
    .user-name { font-size: 14px; }
    .user-email { font-size: 12px; }

    /* Скрываем пагинацию с точками на очень узких — оставляем только стрелки и текущую */
    .paginate-btns .outline-btn.paginate:not(.active) { display: none; }
    .paginate-btns p { display: none; }
}

/* --- Экстра-узкие --- */
@media (max-width: 400px) {
    .stat-cards { grid-template-columns: 1fr; gap: 10px; }
    .stat-card { padding: 10px; }

    .table-actions-wrapper { justify-content: space-between; }
    .btn-small { width: 36px; height: 36px; min-height: 36px; }
}
</style>
