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
                <span class="section-badge">{{ users.length }}</span>
            </div>

            <div class="users-list">
                <div class="user-card" v-for="user in users" :key="user.id">
                    <div class="user-card-header">
                        <div class="user-avatar">
                            <i class="fa fa-user"></i>
                        </div>
                        <div class="user-info">
                            <p class="user-username">{{ user.username }}</p>
                            <span class="user-role">{{ user.role || 'Пользователь' }}</span>
                        </div>
                    </div>
                    
                    <div class="user-card-body">
                        <div class="user-detail">
                            <i class="fa fa-envelope"></i>
                            <span>{{ user.email }}</span>
                        </div>
                        <div class="user-detail">
                            <i class="fa fa-calendar"></i>
                            <span>Зарегистрирован: {{ formatDate(user.created_at) }}</span>
                        </div>
                        <div class="user-detail">
                            <i class="fa fa-motorcycle"></i>
                            <span>Мотоциклов: {{ user.motorcycles?.length || 0 }}</span>
                        </div>
                        <div class="user-status" :class="user.is_banned ? 'status-banned' : 'status-active'">
                            <span class="status-dot"></span>
                            {{ user.is_banned ? 'Заблокирован' : 'Активен' }}
                        </div>
                    </div>

                    <div class="user-card-actions">
                        <button class="btn-action btn-edit" title="Редактировать" @click="editUser(user)">
                            <i class="fa fa-pen"></i>
                        </button>
                        <button class="btn-action" :class="user.is_banned ? 'btn-unban' : 'btn-ban'" 
                                :title="user.is_banned ? 'Разблокировать' : 'Заблокировать'"
                                @click="toggleBanUser(user)">
                            <i :class="user.is_banned ? 'fa fa-check' : 'fa fa-ban'"></i>
                        </button>
                        <button class="btn-action btn-danger" title="Удалить" @click="deleteUser(user)">
                            <i class="fa fa-trash"></i>
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
                <span class="section-badge">{{ pendingManualsCount }}</span>
            </div>

            <div v-if="pendingManualsCount === 0" class="empty-state">
                <i class="fa fa-check-circle"></i>
                <p>Нет мануалов на проверку</p>
            </div>

            <div v-else class="maintenances-list">
                <div class="maintenance-card" v-for="manual in pendingManuals" :key="manual.id">
                    <div class="maintenance-card-header">
                        <div class="maintenance-icon">
                            <i class="fa fa-file"></i>
                        </div>
                        <div class="maintenance-info">
                            <p class="maintenance-title">{{ manual.title }}</p>
                            <span class="maintenance-moto">{{ manual.motorcycle || 'Мотоцикл не указан' }}</span>
                        </div>
                        <span class="maintenance-status status-pending">На проверке</span>
                    </div>

                    <div class="maintenance-card-body">
                        <p class="maintenance-desc">
                            <i class="fa fa-align-left"></i>
                            {{ manual.description || 'Описание отсутствует' }}
                        </p>
                        <div class="maintenance-meta">
                            <span class="meta-item">
                                <i class="fa fa-list-ol"></i>
                                Шагов: {{ manual.steps?.length || 0 }}
                            </span>
                            <span class="meta-item">
                                <i class="fa fa-clock-o"></i>
                                Создан: {{ formatDate(manual.created_at) }}
                            </span>
                            <span class="meta-item">
                                <i class="fa fa-user"></i>
                                Автор: {{ manual.author_username || 'Неизвестен' }}
                            </span>
                        </div>
                    </div>

                    <div class="maintenance-card-actions">
                        <button class="btn-action btn-approve" title="Одобрить" @click="approveManual(manual.id)">
                            <i class="fa fa-check"></i>
                        </button>
                        <button class="btn-action btn-reject" title="Отклонить" @click="openRejectModal(manual.id)">
                            <i class="fa fa-times"></i>
                        </button>
                        <button class="btn-action btn-details" title="Просмотр" @click="openManualModal(manual)">
                            <i class="fa fa-eye"></i>
                        </button>
                        <button class="btn-action btn-danger" title="Удалить" @click="deleteManual(manual.id)">
                            <i class="fa fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        </section>

        <!-- Блок одобренных мануалов -->
        <section class="section section-approved" v-if="approvedManuals.length > 0">
            <div class="section-title-wrapper">
                <i class="fa fa-check-circle" style="color: var(--success);"></i>
                <h2>Одобренные мануалы</h2>
                <span class="section-badge" style="background: rgba(16, 185, 129, 0.15); color: var(--success); border-color: var(--success);">
                    {{ approvedManuals.length }}
                </span>
            </div>

            <div class="maintenances-list">
                <div class="maintenance-card approved-card" v-for="manual in approvedManuals" :key="manual.id">
                    <div class="maintenance-card-header">
                        <div class="maintenance-icon" style="border-color: var(--success);">
                            <i class="fa fa-check" style="color: var(--success);"></i>
                        </div>
                        <div class="maintenance-info">
                            <p class="maintenance-title">{{ manual.title }}</p>
                            <span class="maintenance-moto">{{ manual.motorcycle || 'Мотоцикл не указан' }}</span>
                        </div>
                        <span class="maintenance-status status-approved">Одобрен</span>
                    </div>

                    <div class="maintenance-card-body">
                        <p class="maintenance-desc">
                            <i class="fa fa-align-left"></i>
                            {{ manual.description || 'Описание отсутствует' }}
                        </p>
                        <div class="maintenance-meta">
                            <span class="meta-item">
                                <i class="fa fa-list-ol"></i>
                                Шагов: {{ manual.steps?.length || 0 }}
                            </span>
                            <span class="meta-item">
                                <i class="fa fa-clock-o"></i>
                                Создан: {{ formatDate(manual.created_at) }}
                            </span>
                            <span class="meta-item">
                                <i class="fa fa-user"></i>
                                Автор: {{ manual.author_username || 'Неизвестен' }}
                            </span>
                        </div>
                    </div>

                    <div class="maintenance-card-actions">
                        <button class="btn-action btn-undo" title="Вернуть на проверку" @click="reconsiderManual(manual.id)">
                            <i class="fa fa-undo"></i>
                        </button>
                        <button class="btn-action btn-details" title="Просмотр" @click="openManualModal(manual)">
                            <i class="fa fa-eye"></i>
                        </button>
                        <button class="btn-action btn-danger" title="Удалить" @click="deleteManual(manual.id)">
                            <i class="fa fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        </section>

        <!-- Блок отклоненных мануалов -->
        <section class="section section-rejected" v-if="rejectedManuals.length > 0">
            <div class="section-title-wrapper">
                <i class="fa fa-times-circle" style="color: var(--danger);"></i>
                <h2>Отклоненные мануалы</h2>
                <span class="section-badge" style="background: rgba(239, 68, 68, 0.15); color: var(--danger); border-color: var(--danger);">
                    {{ rejectedManuals.length }}
                </span>
            </div>

            <div class="maintenances-list">
                <div class="maintenance-card rejected-card" v-for="manual in rejectedManuals" :key="manual.id">
                    <div class="maintenance-card-header">
                        <div class="maintenance-icon" style="border-color: var(--danger);">
                            <i class="fa fa-times" style="color: var(--danger);"></i>
                        </div>
                        <div class="maintenance-info">
                            <p class="maintenance-title">{{ manual.title }}</p>
                            <span class="maintenance-moto">{{ manual.motorcycle || 'Мотоцикл не указан' }}</span>
                        </div>
                        <span class="maintenance-status status-rejected">Отклонен</span>
                    </div>

                    <div class="maintenance-card-body">
                        <p class="maintenance-desc">
                            <i class="fa fa-align-left"></i>
                            {{ manual.description || 'Описание отсутствует' }}
                        </p>
                        <div v-if="manual.rejection_reason" class="rejection-reason">
                            <i class="fa fa-info-circle"></i>
                            <span>Причина: {{ manual.rejection_reason }}</span>
                        </div>
                        <div class="maintenance-meta">
                            <span class="meta-item">
                                <i class="fa fa-list-ol"></i>
                                Шагов: {{ manual.steps?.length || 0 }}
                            </span>
                            <span class="meta-item">
                                <i class="fa fa-clock-o"></i>
                                Создан: {{ formatDate(manual.created_at) }}
                            </span>
                            <span class="meta-item">
                                <i class="fa fa-user"></i>
                                Автор: {{ manual.author_username || 'Неизвестен' }}
                            </span>
                        </div>
                    </div>

                    <div class="maintenance-card-actions">
                        <button class="btn-action btn-undo" title="Вернуть на проверку" @click="reconsiderManual(manual.id)">
                            <i class="fa fa-undo"></i>
                        </button>
                        <button class="btn-action btn-details" title="Просмотр" @click="openManualModal(manual)">
                            <i class="fa fa-eye"></i>
                        </button>
                        <button class="btn-action btn-danger" title="Удалить" @click="deleteManual(manual.id)">
                            <i class="fa fa-trash"></i>
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
                        <p class="stat-card-value">{{ users_count }}</p>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-card-icon">
                        <i class="fa fa-motorcycle"></i>
                    </div>
                    <div class="stat-card-content">
                        <p class="stat-card-title">Мотоциклов в системе</p>
                        <p class="stat-card-value">{{ motorcycles_count }}</p>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-card-icon">
                        <i class="fa fa-file-text"></i>
                    </div>
                    <div class="stat-card-content">
                        <p class="stat-card-title">Всего мануалов</p>
                        <p class="stat-card-value">{{ all_manuals_count }}</p>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-card-icon" style="border-color: var(--warning);">
                        <i class="fa fa-clock-o" style="color: var(--warning);"></i>
                    </div>
                    <div class="stat-card-content">
                        <p class="stat-card-title">На проверке</p>
                        <p class="stat-card-value">{{ pendingManualsCount }}</p>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <!-- Модальное окно просмотра мануала -->
    <div v-if="showManualModal" class="modal-wrapper" @click.self="closeManualModal">
        <div class="modal-container modal-large">
            <div class="modal-header">
                <div class="modal-header-info">
                    <i class="fa fa-file-text"></i>
                    <h3 class="modal-title">{{ selectedManual?.title }}</h3>
                </div>
                <button class="modal-close" @click="closeManualModal">
                    <i class="fa fa-times"></i>
                </button>
            </div>

            <div class="modal-body">
                <div class="manual-detail-meta">
                    <span class="detail-item">
                        <i class="fa fa-motorcycle"></i>
                        {{ selectedManual?.motorcycle || 'Не указан' }}
                    </span>
                    <span class="detail-item">
                        <i class="fa fa-user"></i>
                        {{ selectedManual?.author_username || 'Неизвестен' }}
                    </span>
                    <span class="detail-item">
                        <i class="fa fa-clock-o"></i>
                        {{ formatDate(selectedManual?.created_at) }}
                    </span>
                    <span class="detail-item status-badge" :class="'status-' + selectedManual?.status">
                        {{ getStatusLabel(selectedManual?.status) }}
                    </span>
                </div>

                <div class="manual-detail-description">
                    <h4>Описание</h4>
                    <p>{{ selectedManual?.description || 'Описание отсутствует' }}</p>
                </div>

                <div v-if="selectedManual?.rejection_reason" class="manual-detail-rejection">
                    <h4 style="color: var(--danger);">Причина отклонения</h4>
                    <p style="color: var(--danger);">{{ selectedManual.rejection_reason }}</p>
                </div>

                <div class="manual-detail-steps">
                    <h4>Шаги выполнения ({{ selectedManual?.steps?.length || 0 }})</h4>
                    <div v-if="!selectedManual?.steps?.length" class="empty-steps">
                        <p>Шаги отсутствуют</p>
                    </div>
                    <div v-else class="steps-list">
                        <div 
                            v-for="(step, index) in selectedManual?.steps" 
                            :key="step.id || index" 
                            class="step-item"
                        >
                            <div class="step-number">{{ index + 1 }}</div>
                            <div class="step-content">
                                <p class="step-text">{{ step.text || step.content || 'Шаг без описания' }}</p>
                                <div v-if="step.image || step.image_url" class="step-image-wrapper">
                                    <img :src="step.image || step.image_url" :alt="'Шаг ' + (index + 1)" class="step-image" />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="modal-actions">
                    <button v-if="selectedManual?.status === 'moderate' || selectedManual?.status === 'pending'" 
                            class="btn-approve" @click="approveManualFromModal">
                        <i class="fa fa-check"></i> Одобрить
                    </button>
                    <button v-if="selectedManual?.status === 'moderate' || selectedManual?.status === 'pending'" 
                            class="btn-reject" @click="openRejectModalFromModal">
                        <i class="fa fa-times"></i> Отклонить
                    </button>
                    <button v-if="selectedManual?.status === 'rejected'" class="btn-undo" @click="reconsiderManualFromModal">
                        <i class="fa fa-undo"></i> Пересмотреть
                    </button>
                    <button v-if="selectedManual?.status === 'approved'" class="btn-undo" @click="reconsiderManualFromModal">
                        <i class="fa fa-undo"></i> Вернуть на проверку
                    </button>
                    <button class="btn-danger" @click="deleteManualFromModal">
                        <i class="fa fa-trash"></i> Удалить
                    </button>
                    <button class="btn-secondary" @click="closeManualModal">
                        Закрыть
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Модальное окно отклонения -->
    <div v-if="showRejectModal" class="modal-wrapper" @click.self="closeRejectModal">
        <div class="modal-container">
            <div class="modal-header">
                <i class="fa fa-times-circle" style="color: var(--danger);"></i>
                <h3 class="modal-title">Отклонить мануал</h3>
                <button class="modal-close" @click="closeRejectModal">
                    <i class="fa fa-times"></i>
                </button>
            </div>

            <div class="modal-body">
                <p class="modal-text">Укажите причину отклонения мануала:</p>
                <textarea 
                    v-model="rejectReason" 
                    class="modal-textarea" 
                    placeholder="Опишите причину отклонения..."
                    rows="4"
                ></textarea>
            </div>

            <div class="modal-actions">
                <button class="btn-danger" @click="confirmReject" :disabled="isLoading">
                    <i class="fa fa-times"></i> Отклонить
                </button>
                <button class="btn-secondary" @click="closeRejectModal">
                    Отмена
                </button>
            </div>
        </div>
    </div>

    <!-- Модальное окно редактирования пользователя -->
    <div v-if="showEditUserModal" class="modal-wrapper" @click.self="closeEditUserModal">
        <div class="modal-container">
            <div class="modal-header">
                <i class="fa fa-user-edit" style="color: var(--accent);"></i>
                <h3 class="modal-title">Редактирование пользователя</h3>
                <button class="modal-close" @click="closeEditUserModal">
                    <i class="fa fa-times"></i>
                </button>
            </div>

            <div class="modal-body">
                <div class="form-group">
                    <label>Имя пользователя</label>
                    <input v-model="editUserData.username" class="form-input" type="text" />
                </div>
                <div class="form-group">
                    <label>Email</label>
                    <input v-model="editUserData.email" class="form-input" type="email" />
                </div>
                <div class="form-group">
                    <label>Роль</label>
                    <select v-model="editUserData.role" class="form-select">
                        <option value="user">Пользователь</option>
                        <option value="admin">Администратор</option>
                    </select>
                </div>
            </div>

            <div class="modal-actions">
                <button class="btn-primary" @click="saveUserEdit" :disabled="isLoading">
                    <i class="fa fa-save"></i> Сохранить
                </button>
                <button class="btn-secondary" @click="closeEditUserModal">
                    Отмена
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import api from '../api/api'

export default {
    data() {
        return {
            manuals: [],
            users: [],
            manual_count: 0,
            users_count: 0,
            motorcycles_count: 0,
            all_manuals_count: 0,

            // Модальное окно просмотра
            showManualModal: false,
            selectedManual: null,

            // Модальное окно отклонения
            showRejectModal: false,
            selectedManualId: null,
            rejectReason: '',

            // Модальное окно редактирования пользователя
            showEditUserModal: false,
            editUserData: {
                id: null,
                username: '',
                email: '',
                role: 'user'
            },

            isLoading: false
        }
    },

    computed: {
        pendingManuals() {
            return this.manuals.filter(m => m.status === 'moderate' || m.status === 'pending')
        },
        approvedManuals() {
            return this.manuals.filter(m => m.status === 'approved')
        },
        rejectedManuals() {
            return this.manuals.filter(m => m.status === 'rejected')
        },
        pendingManualsCount() {
            return this.pendingManuals.length
        }
    },

    methods: {
        async loadData() {
            try {
                this.isLoading = true
                const response = await api.get('/admin/get')

                this.manuals = response.data.manuals || []
                this.users = response.data.users || []
                this.manual_count = response.data.manuals_count || 0
                this.users_count = response.data.users_count || 0
                this.motorcycles_count = response.data.motorcycles_count || 0
                this.all_manuals_count = response.data.all_manuals_count || this.manuals.length
            } catch (err) {
                console.error(`Failed load admin data: ${err}`)
                this.showNotification('Ошибка загрузки данных', 'error')
            } finally {
                this.isLoading = false
            }
        },

        formatDate(dateString) {
            if (!dateString) return '—'
            try {
                const date = new Date(dateString)
                return date.toLocaleString('ru-RU', {
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                })
            } catch {
                return dateString
            }
        },

        getStatusLabel(status) {
            const labels = {
                moderate: 'На проверке',
                pending: 'На проверке',
                approved: 'Одобрено',
                rejected: 'Отклонено'
            }
            return labels[status] || status
        },

        showNotification(message, type = 'info') {
            // Можно использовать Vue Toast или другой механизм уведомлений
            alert(message)
        },

        // ===== Управление мануалами =====

        async approveManual(manualId) {
            if (!confirm('Вы уверены, что хотите одобрить этот мануал?')) return

            try {
                this.isLoading = true
                await api.post(`/admin/manual/${manualId}/approve`)
                await this.loadData()
                this.showNotification('Мануал успешно одобрен!', 'success')
            } catch (err) {
                console.error('Error approving manual:', err)
                this.showNotification('Ошибка при одобрении мануала', 'error')
            } finally {
                this.isLoading = false
            }
        },

        approveManualFromModal() {
            if (this.selectedManual) {
                this.approveManual(this.selectedManual.id)
                this.closeManualModal()
            }
        },

        // Отклонение
        openRejectModal(manualId) {
            this.selectedManualId = manualId
            this.rejectReason = ''
            this.showRejectModal = true
            document.body.style.overflow = 'hidden'
        },

        openRejectModalFromModal() {
            if (this.selectedManual) {
                this.openRejectModal(this.selectedManual.id)
                this.closeManualModal()
            }
        },

        closeRejectModal() {
            this.showRejectModal = false
            this.selectedManualId = null
            this.rejectReason = ''
            document.body.style.overflow = ''
        },

        async confirmReject() {
            if (!this.selectedManualId) return

            try {
                this.isLoading = true
                await api.post(`/admin/manual/${this.selectedManualId}/reject`, {
                    reason: this.rejectReason || 'Причина не указана'
                })
                await this.loadData()
                this.showNotification('Мануал отклонен', 'info')
                this.closeRejectModal()
            } catch (err) {
                console.error('Error rejecting manual:', err)
                this.showNotification('Ошибка при отклонении мануала', 'error')
            } finally {
                this.isLoading = false
            }
        },

        // Пересмотр
        async reconsiderManual(manualId) {
            if (!confirm('Вернуть мануал на повторную проверку?')) return

            try {
                this.isLoading = true
                await api.post(`/admin/manual/${manualId}/reconsider`)
                await this.loadData()
                this.showNotification('Мануал возвращен на проверку!', 'success')
            } catch (err) {
                console.error('Error reconsidering manual:', err)
                this.showNotification('Ошибка при возврате мануала', 'error')
            } finally {
                this.isLoading = false
            }
        },

        reconsiderManualFromModal() {
            if (this.selectedManual) {
                this.reconsiderManual(this.selectedManual.id)
                this.closeManualModal()
            }
        },

        // Удаление мануала
        async deleteManual(manualId) {
            if (!confirm('Вы уверены, что хотите удалить этот мануал? Это действие нельзя отменить!')) return

            try {
                this.isLoading = true
                await api.delete(`/admin/manual/${manualId}`)
                await this.loadData()
                this.showNotification('Мануал успешно удален', 'success')
            } catch (err) {
                console.error('Error deleting manual:', err)
                this.showNotification('Ошибка при удалении мануала', 'error')
            } finally {
                this.isLoading = false
            }
        },

        deleteManualFromModal() {
            if (this.selectedManual) {
                this.deleteManual(this.selectedManual.id)
                this.closeManualModal()
            }
        },

        // ===== Просмотр мануала =====

        openManualModal(manual) {
            this.selectedManual = manual
            this.showManualModal = true
            document.body.style.overflow = 'hidden'
        },

        closeManualModal() {
            this.showManualModal = false
            this.selectedManual = null
            document.body.style.overflow = ''
        },

        // ===== Управление пользователями =====

        editUser(user) {
            this.editUserData = {
                id: user.id,
                username: user.username,
                email: user.email,
                role: user.role || 'user'
            }
            this.showEditUserModal = true
            document.body.style.overflow = 'hidden'
        },

        closeEditUserModal() {
            this.showEditUserModal = false
            this.editUserData = { id: null, username: '', email: '', role: 'user' }
            document.body.style.overflow = ''
        },

        async saveUserEdit() {
            try {
                this.isLoading = true
                await api.put(`/admin/user/${this.editUserData.id}`, {
                    username: this.editUserData.username,
                    email: this.editUserData.email,
                    role: this.editUserData.role
                })
                await this.loadData()
                this.showNotification('Данные пользователя обновлены', 'success')
                this.closeEditUserModal()
            } catch (err) {
                console.error('Error updating user:', err)
                this.showNotification('Ошибка при обновлении пользователя', 'error')
            } finally {
                this.isLoading = false
            }
        },

        async toggleBanUser(user) {
            const action = user.is_banned ? 'разблокировать' : 'заблокировать'
            if (!confirm(`Вы уверены, что хотите ${action} пользователя ${user.username}?`)) return

            try {
                this.isLoading = true
                const endpoint = user.is_banned ? `/admin/user/${user.id}/unban` : `/admin/user/${user.id}/ban`
                await api.post(endpoint)
                await this.loadData()
                this.showNotification(`Пользователь ${user.is_banned ? 'разблокирован' : 'заблокирован'}`, 'success')
            } catch (err) {
                console.error('Error toggling user ban:', err)
                this.showNotification('Ошибка при изменении статуса пользователя', 'error')
            } finally {
                this.isLoading = false
            }
        },

        async deleteUser(user) {
            if (!confirm(`Вы уверены, что хотите удалить пользователя ${user.username}? Это действие нельзя отменить!`)) return

            try {
                this.isLoading = true
                await api.delete(`/admin/user/${user.id}`)
                await this.loadData()
                this.showNotification(`Пользователь ${user.username} удален`, 'success')
            } catch (err) {
                console.error('Error deleting user:', err)
                this.showNotification('Ошибка при удалении пользователя', 'error')
            } finally {
                this.isLoading = false
            }
        }
    },

    mounted() {
        this.loadData()
    }
}
</script>

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

/* ===== Модальное окно просмотра ===== */
.modal-large {
    max-width: 700px;
}

.modal-header-info {
    display: flex;
    align-items: center;
    gap: 12px;
}

.modal-header-info i {
    font-size: 24px;
    color: var(--accent);
}

.modal-close {
    background: var(--bg-secondary);
    border: 2px solid var(--border-color);
    border-radius: 50%;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: var(--text-secondary);
    transition: all 0.3s;
}

.modal-close:hover {
    border-color: var(--danger);
    color: var(--danger);
    background: rgba(239, 68, 68, 0.1);
}

.modal-body {
    max-height: 70vh;
    overflow-y: auto;
    padding-right: 4px;
}

.modal-body::-webkit-scrollbar {
    width: 4px;
}

.modal-body::-webkit-scrollbar-track {
    background: var(--bg-primary);
    border-radius: 10px;
}

.modal-body::-webkit-scrollbar-thumb {
    background: var(--accent);
    border-radius: 10px;
}

.manual-detail-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 2px solid var(--border-color);
}

.detail-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.85rem;
    color: var(--text-secondary);
}

.detail-item i {
    color: var(--text-muted);
}

.manual-detail-description {
    margin-bottom: 20px;
}

.manual-detail-description h4 {
    font-size: 0.9rem;
    color: var(--text-secondary);
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

.manual-detail-description p {
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.5;
    margin-bottom: 0;
}

.manual-detail-steps h4 {
    font-size: 0.9rem;
    color: var(--text-secondary);
    margin-bottom: 12px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

.steps-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.step-item {
    display: flex;
    gap: 14px;
    padding: 14px 16px;
    background: var(--bg-primary);
    border-radius: 14px;
    border: 1px solid var(--border-color);
}

.step-number {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--accent-light);
    border: 2px solid var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 14px;
    color: var(--accent);
    flex-shrink: 0;
}

.step-content {
    flex: 1;
    min-width: 0;
}

.step-text {
    font-size: 0.9rem;
    color: var(--text-primary);
    margin-bottom: 0;
    line-height: 1.4;
}

.step-image-wrapper {
    margin-top: 10px;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid var(--border-color);
}

.step-image {
    width: 100%;
    height: auto;
    max-height: 250px;
    object-fit: cover;
    display: block;
}

/* Модальное окно отклонения */
.modal-text {
    color: var(--text-secondary);
    margin-bottom: 12px;
}

.modal-textarea {
    width: 100%;
    padding: 12px 16px;
    background: var(--bg-secondary);
    border: 2px solid var(--border-color);
    border-radius: 14px;
    color: var(--text-primary);
    font-size: 0.9rem;
    font-family: inherit;
    resize: vertical;
    transition: all 0.3s;
}

.modal-textarea:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15);
}

.modal-textarea::placeholder {
    color: var(--text-muted);
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

    .modal-large {
        max-width: 90%;
        margin: 20px;
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

    .modal-large {
        max-width: 95%;
        margin: 12px;
        padding: 16px;
    }

    .modal-body {
        max-height: 60vh;
    }

    .step-item {
        flex-direction: column;
        align-items: stretch;
        padding: 12px;
    }

    .step-number {
        align-self: flex-start;
    }
}

/* Дополнительные стили для новых элементов */

.empty-state {
    text-align: center;
    padding: 40px 20px;
    color: var(--text-muted);
}

.empty-state i {
    font-size: 48px;
    color: var(--success);
    margin-bottom: 16px;
    display: block;
}

.empty-state p {
    font-size: 1.1rem;
    margin: 0;
}

/* Статусы для мануалов */
.status-approved {
    color: var(--success);
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.2);
}

.status-rejected {
    color: var(--danger);
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.2);
}

.status-badge {
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 600;
}

/* Карточки с разными статусами */
.approved-card {
    border-color: rgba(16, 185, 129, 0.3);
}

.approved-card:hover {
    border-color: var(--success);
    box-shadow: 0 8px 30px rgba(16, 185, 129, 0.15);
}

.rejected-card {
    border-color: rgba(239, 68, 68, 0.3);
}

.rejected-card:hover {
    border-color: var(--danger);
    box-shadow: 0 8px 30px rgba(239, 68, 68, 0.15);
}

/* Причина отклонения */
.rejection-reason {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    padding: 8px 12px;
    background: rgba(239, 68, 68, 0.08);
    border-radius: 8px;
    font-size: 0.85rem;
    color: var(--danger);
}

.rejection-reason i {
    margin-top: 2px;
}

/* Кнопка разблокировки */
.btn-unban {
    border-color: var(--success);
    color: var(--success);
}

.btn-unban:hover {
    border-color: var(--success);
    color: var(--success);
    background: rgba(16, 185, 129, 0.15);
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
}

.btn-undo:hover {
    border-color: var(--warning);
    color: var(--warning);
    background: rgba(245, 158, 11, 0.15);
    box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2);
}

/* Статус пользователя забанен */
.status-banned {
    color: var(--danger);
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.2);
}

.status-banned .status-dot {
    background: var(--danger);
    animation: none;
}

/* Формы в модалках */
.form-group {
    margin-bottom: 16px;
}

.form-group label {
    display: block;
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--text-secondary);
    margin-bottom: 4px;
}

.form-input,
.form-select {
    width: 100%;
    padding: 10px 14px;
    background: var(--bg-secondary);
    border: 2px solid var(--border-color);
    border-radius: 12px;
    color: var(--text-primary);
    font-size: 0.95rem;
    font-family: inherit;
    transition: all 0.3s;
}

.form-input:focus,
.form-select:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15);
}

.form-select {
    appearance: none;
    cursor: pointer;
}

/* Пустые шаги */
.empty-steps {
    padding: 20px;
    text-align: center;
    color: var(--text-muted);
    background: var(--bg-primary);
    border-radius: 12px;
    border: 1px dashed var(--border-color);
}

/* Адаптив для новых элементов */
@media (max-width: 768px) {
    .form-group {
        margin-bottom: 12px;
    }

    .form-input,
    .form-select {
        padding: 8px 12px;
        font-size: 0.85rem;
    }

    .rejection-reason {
        font-size: 0.8rem;
        padding: 6px 10px;
    }
}

@media (max-width: 480px) {
    .empty-state {
        padding: 30px 16px;
    }

    .empty-state i {
        font-size: 36px;
    }

    .status-badge {
        font-size: 0.7rem;
        padding: 2px 8px;
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

    .step-text {
        font-size: 0.8rem;
    }

    .step-number {
        width: 28px;
        height: 28px;
        font-size: 12px;
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

    .modal-actions {
        flex-direction: column;
    }

    .modal-actions button {
        width: 100%;
    }
}
</style>