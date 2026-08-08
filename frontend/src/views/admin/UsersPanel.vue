<template>
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
                            @error="(e) => e.target.src = '/BaseAvatar.jpg'"
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
        @submit="addUser"
    />

    <EditUserModal
        :is-open="showEditUserModal"
        :user="selectedUser"
        @close="closeEditUserModal"
        @submit="editUser"
    />

    <DeleteUserModal
        :is-open="showDeleteUserModal"
        :user="selectedUser"
        @close="closeDeleteUserModal"
        @submit="deleteUser"
    />
</template>

<script>
import api from '../../api/api'
import AddUserModal from '../../components/modals/admin/AddUserModal.vue';
import EditUserModal from '../../components/modals/admin/EditUserModal.vue';
import DeleteUserModal from '../../components/modals/admin/DeleteUserModal.vue';
import Header from '../../components/Header.vue';

export default {
    components: {
        AddUserModal,
        EditUserModal,
        DeleteUserModal,
        Header
    },
    
    data() {
        return {
            loading: false,
            users: [],
            stats: {
                total: 0,
                active: 0,
                banned: 0,
                admin: 0
            },
            pagination: {
                current_page: 1,
                per_page: 10,
                total: 0,
                pages: 0,
                has_prev: false,
                has_next: false
            },
            filters: {
                search: '',
                role: '',
                status: '',
                date_from: '',
                date_to: ''
            },
            searchTimeout: null,

            showAddUserModal: false,
            showEditUserModal: false,
            showDeleteUserModal: false,
            selectedUser: null,
        }
    },
    computed: {
        visiblePages() {
            const current = this.pagination.current_page
            const total = this.pagination.pages
            const delta = 2
            const range = []
            
            for (let i = Math.max(2, current - delta); i <= Math.min(total - 1, current + delta); i++) {
                range.push(i)
            }
            
            if (current - delta > 2) {
                range.unshift('...')
            }
            
            if (current + delta < total - 1) {
                range.push('...')
            }
            
            range.unshift(1)
            
            if (total > 1) {
                range.push(total)
            }
            
            return range.filter((v, i, a) => a.indexOf(v) === i)
        },
        showEllipsisEnd() {
            const current = this.pagination.current_page
            const total = this.pagination.pages
            return total > 1 && current + 2 < total - 1
        },
        showLastPage() {
            const total = this.pagination.pages
            return total > 1 && this.pagination.current_page + 2 < total
        }
    },
    created() {
        this.loadUsers()
    },
    methods: {
        getAvatarUrl(avatarPath) {
            if (!avatarPath || typeof avatarPath !== 'string') {
                return '/BaseAvatar.jpg';
            }
            if (avatarPath.startsWith('http')) {
                return avatarPath;
            }
            return `/uploads/${avatarPath}`;
        },
        async loadUsers() {
            this.loading = true
            try {
                const params = {
                    page: this.pagination.current_page,
                    per_page: this.pagination.per_page,
                    ...this.filters
                }
                
                // Убираем пустые параметры
                Object.keys(params).forEach(key => {
                    if (!params[key]) delete params[key]
                })
                
                const response = await api.get('/admin/users', { params })
                const data = response.data
                
                this.users = data.users || []
                this.pagination = {
                    current_page: data.current_page,
                    per_page: data.per_page,
                    total: data.total,
                    pages: data.pages,
                    has_prev: data.has_prev,
                    has_next: data.has_next
                }
                this.stats = data.stats || {
                    total: 0,
                    active: 0,
                    banned: 0,
                    admin: 0
                }
            } catch (error) {
                console.error('Error loading users:', error)
                if (error.response?.status === 401) {
                    this.$router.push('/login')
                }
            } finally {
                this.loading = false
            }
        },

        async addUser(formData) {
            try {
                const response = await api.post('/admin/user', formData)
                this.showAddUserModal = false
                this.loadUsers()
            } catch (err) {
                console.error(`Failed add user: ${err}`)
            }
        },
        
        goToPage(page) {
            if (page < 1 || page > this.pagination.pages) return
            this.pagination.current_page = page
            this.loadUsers()
        },
        
        changePerPage() {
            this.pagination.current_page = 1
            this.loadUsers()
        },
        
        applyFilters() {
            this.pagination.current_page = 1
            this.loadUsers()
        },
        
        debouncedSearch() {
            clearTimeout(this.searchTimeout)
            this.searchTimeout = setTimeout(() => {
                this.applyFilters()
            }, 500)
        },
        
        resetFilters() {
            this.filters = {
                search: '',
                role: '',
                status: '',
                date_from: '',
                date_to: ''
            }
            this.pagination.current_page = 1
            this.loadUsers()
        },
        
        loadAllUsers() {
            this.pagination.per_page = 10000 // Большое число для загрузки всех
            this.pagination.current_page = 1
            this.loadUsers()
        },
        
        // Вспомогательные методы
        getUserRoleName(role) {
            const roles = {
                'admin': 'Администратор',
                'motorcyclist': 'Мотоциклист',
                'club_member': 'Член клуба'
            }
            return roles[role] || role
        },
        
        getUserStatusName(status) {
            const statuses = {
                'active': 'Активен',
                'banned': 'Заблокирован',
                'pending': 'Ожидает'
            }
            return statuses[status] || status
        },
        
        getStatusClass(status) {
            const classes = {
                'active': 'status-active',
                'banned': 'status-banned',
                'pending': 'status-pending'
            }
            return classes[status] || ''
        },
        
        formatDate(date) {
            if (!date) return '-'
            const d = new Date(date)
            return d.toLocaleDateString('ru-RU', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric'
            })
        },
        
        // Действия с пользователями
        async banUser(user) {
            if (!confirm(`Заблокировать пользователя ${user.username}?`)) return
            try {
                await api.post(`/admin/user/${user.id}/ban`)
                await this.loadUsers()
            } catch (error) {
                console.error('Error banning user:', error)
                alert(error.response?.data?.message || 'Ошибка при блокировке')
            }
        },
        
        async unbanUser(user) {
            if (!confirm(`Разблокировать пользователя ${user.username}?`)) return
            try {
                await api.post(`/admin/user/${user.id}/unban`)
                await this.loadUsers()
                
            } catch (error) {
                console.error('Error unbanning user:', error)
                alert(error.response?.data?.message || 'Ошибка при разблокировке')
            }
        },
        
        async deleteUser(userId) {
            try {
                await api.delete(`/admin/user/${userId}`)
                await this.loadUsers()
                this.closeDeleteUserModal()
            } catch (error) {
                console.error('Error deleting user:', error)
                alert(error.response?.data?.message || 'Ошибка при удалении')
            }
        },
        openDeleteUserModal(user) {
            this.showDeleteUserModal = true
            this.selectedUser = user
        },
        closeDeleteUserModal() {
            this.showDeleteUserModal = false
            this.selectedUser = null
        },
        
        async editUser(formData) {
            try {
                const { data } = await api.put(`/admin/user/${formData.id}`, formData)

                const index = this.users.findIndex(u => u.id === formData.id)
                if (index !== -1) {
                    this.users[index] = data
                }

                this.closeEditUserModal()
            } catch (error) {
                console.error('Failed update user:', error)
                alert(error.response?.data?.message || 'Ошибка при редактировании')
            }
        },
        openEditUserModal(user) {
            this.showEditUserModal = true
            this.selectedUser = user
        },
        closeEditUserModal() {
            this.showEditUserModal = false
            this.selectedUser = null
        },
        
        openCreateUserModal() {
            // TODO: Открыть модалку создания
            console.log('Open create user modal')
        },
        
        logout() {
            // TODO: Реализовать выход
            console.log('Logout')
        }
    }
}
</script>

<style scoped>
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
    align-items: last baseline;
    margin-bottom: 16px;
    gap: 16px;
}

.inputs-group {
    display: flex;
    gap: 14px;
    justify-content: center;
    align-items: center;
}

.inputs-wrapper {
    display: flex;
    gap: 14px;
}

.filters-actions {
    display: flex;
    gap: 8px;
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
    .filters-actions {
        flex-direction: column;
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
.btn-small.success{ 
    background-color: var(--success-trans);
    color: var(--success);
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