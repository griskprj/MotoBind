<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Редактирование пользователя"
        subtitle="Измените данные пользователя. Роль определяет доступ к функциям."
        icon="user-cog"
        bg-icon-color="var(--accent-trans)"
        icon-color="var(--accent-text)"
        @close="handleClose"
    >
        <!-- Информация о пользователе -->
        <div class="user-info-card">
            <img :src="getAvatarUrl(user?.avatar)" alt="Аватар" class="user-avatar" />
            <div class="user-info">
                <div class="user-name">{{ user?.username || 'Пользователь' }}</div>
                <div class="user-meta">
                    <span class="user-id">ID: #{{ user?.id }}</span>
                    <span class="user-date">{{ formatDate(user?.created_at) }}</span>
                </div>
            </div>
        </div>

        <!-- Форма -->
        <div class="modal-form-group">
            <label>
                Имя пользователя <span class="required">*</span>
                <input 
                    v-model="form.username" 
                    type="text" 
                    placeholder="Введите имя пользователя"
                    required
                />
            </label>
        </div>

        <div class="modal-form-group">
            <label>
                Email <span class="required">*</span>
                <input 
                    v-model="form.email" 
                    type="email" 
                    placeholder="user@example.com"
                    required
                />
            </label>
        </div>

        <div class="modal-form-row">
            <div class="modal-form-group">
                <label>Роль</label>
                <select v-model="form.role">
                    <option value="motorcyclist">Мотоциклист</option>
                    <option value="club_member">Член клуба</option>
                    <option value="admin">Администратор</option>
                </select>
            </div>

            <div class="modal-form-group">
                <label>Статус</label>
                <select v-model="form.status">
                    <option value="active">Активен</option>
                    <option value="banned">Заблокирован</option>
                    <option value="pending">Ожидает</option>
                </select>
            </div>
        </div>

        <template #actions>
            <div class="modal-actions">
                <button class="btn btn-secondary" @click="handleClose">
                    Отменить
                </button>
                <button class="btn btn-primary" @click="submit" :disabled="loading">
                    <span v-if="!loading">
                        <i class="fa fa-save"></i> Сохранить
                    </span>
                    <span v-else>
                        <i class="fa fa-spinner fa-spin"></i> Сохранение...
                    </span>
                </button>
            </div>
        </template>
    </ModalWrapper>
</template>

<script>
import ModalWrapper from '../ModalWrapper.vue'

export default {
    components: { ModalWrapper },

    props: {
        isOpen: {
            type: Boolean,
            default: false,
            required: true
        },
        user: {
            type: Object,
            default: null
        }
    },

    data() {
        return {
            form: {
                id: null,
                username: '',
                email: '',
                role: 'motorcyclist',
                status: 'active'
            },
            loading: false
        }
    },

    watch: {
        isOpen(newVal) {
            if (newVal && this.user) {
                this.loadFormData()
            }
            if (!newVal) {
                this.loading = false
            }
        },
        user: {
            handler(newVal) {
                if (this.isOpen && newVal) {
                    this.loadFormData()
                }
            },
            deep: true
        }
    },

    methods: {
        loadFormData() {
            if (!this.user) return
            this.form = {
                id: this.user.id || null,
                username: this.user.username || '',
                email: this.user.email || '',
                role: this.user.role || 'motorcyclist',
                status: this.user.status || 'active'
            }
        },

        resetForm() {
            this.form = {
                id: null,
                username: '',
                email: '',
                role: 'motorcyclist',
                status: 'active'
            }
            this.loading = false
        },

        handleClose() {
            this.resetForm()
            this.$emit('close')
        },

        async submit() {
            // Валидация
            if (!this.form.username || this.form.username.trim().length < 2) {
                alert('Имя пользователя должно содержать минимум 2 символа')
                return
            }

            if (!this.form.email || !this.form.email.includes('@')) {
                alert('Введите корректный email адрес')
                return
            }

            this.loading = true
            try {
                await this.$emit('submit', this.form)
                this.resetForm()
                this.$emit('close')
            } catch (error) {
                console.error('Submit error:', error)
            } finally {
                this.loading = false
            }
        },

        getAvatarUrl(avatarPath) {
            if (!avatarPath || typeof avatarPath !== 'string') {
                return '/BaseAvatar.webp'
            }
            if (avatarPath.startsWith('http')) {
                return avatarPath
            }
            const baseUrl = import.meta.env.VITE_API_URL || ''
            return `${baseUrl}/uploads/${avatarPath}`
        },

        formatDate(dateString) {
            if (!dateString) return '—'
            try {
                const date = new Date(dateString)
                if (isNaN(date.getTime())) return '—'
                return date.toLocaleDateString('ru-RU', {
                    day: '2-digit',
                    month: 'short',
                    year: 'numeric'
                })
            } catch {
                return '—'
            }
        }
    },

    mounted() {
        if (this.isOpen && this.user) {
            this.loadFormData()
        }
    }
}
</script>

<style scoped>
/* ===== ИНФО О ПОЛЬЗОВАТЕЛЕ ===== */
.user-info-card {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 14px 16px;
    background: var(--bg-secondary);
    border-radius: 12px;
    border: 1px solid var(--border-light);
    margin-bottom: 18px;
}

.user-avatar {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid var(--accent);
    flex-shrink: 0;
}

.user-info {
    flex: 1;
    min-width: 0;
}

.user-name {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 2px;
}

.user-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    font-size: 13px;
    color: var(--text-muted);
}

.user-id {
    background: var(--accent-trans);
    padding: 1px 10px;
    border-radius: 12px;
    color: var(--accent-text);
}

/* ===== ПОЛЯ ВВОДА ===== */
.modal-form-group {
    margin-bottom: 14px;
}

.modal-form-group:last-child {
    margin-bottom: 0;
}

.modal-form-group label {
    display: block;
    font-weight: 600;
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-bottom: 4px;
}

.modal-form-group label .required {
    color: var(--danger-text);
    font-weight: 700;
}

.modal-form-group input,
.modal-form-group select {
    width: 100%;
    padding: 0.6rem 0.8rem;
    border-radius: 10px;
    border: 2px solid var(--border-color);
    background-color: var(--bg-input);
    color: var(--text-primary);
    font-size: 0.95rem;
    transition: all 0.2s;
    box-sizing: border-box;
    font-family: inherit;
    appearance: auto;
}

.modal-form-group input:focus,
.modal-form-group select:focus {
    border-color: var(--accent);
    outline: none;
    box-shadow: 0 0 0 3px var(--accent-trans);
}

.modal-form-group input::placeholder {
    color: var(--text-muted);
}

.modal-form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}

/* ===== ИНФО-БЛОК ===== */
.modal-info-block {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
    border-radius: 10px;
    margin: 12px 0;
}

.modal-info-block.info {
    background: var(--accent-trans);
    border: 1px solid var(--accent-light);
}

.modal-info-icon {
    font-size: 18px;
    color: var(--accent-text);
    flex-shrink: 0;
    margin-top: 2px;
}

.modal-info-text {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.5;
}

.role-tag {
    display: inline-block;
    padding: 0 6px;
    font-weight: 500;
    color: var(--accent-text);
    background: var(--accent-trans);
    border-radius: 4px;
}

.status-tag {
    display: inline-block;
    padding: 0 6px;
    font-weight: 500;
    border-radius: 4px;
}

.status-tag.active {
    color: var(--success-text);
    background: var(--success-trans);
}

.status-tag.banned {
    color: var(--danger-text);
    background: var(--danger-trans);
}

/* ===== КНОПКИ ===== */
.modal-actions {
    display: flex;
    gap: 10px;
}

.modal-actions .btn {
    flex: 1;
    padding: 0.7rem 1rem;
    border-radius: 40px;
    font-weight: 600;
    font-size: 0.9rem;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.modal-actions .btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.modal-actions .btn-primary {
    background: linear-gradient(135deg, var(--accent), var(--accent-hover));
    color: #fff;
}

.modal-actions .btn-primary:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(138, 92, 246, 0.3);
}

.modal-actions .btn-secondary {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}

.modal-actions .btn-secondary:hover:not(:disabled) {
    background: var(--border-color);
}

/* ============================================ */
/* ===== АДАПТИВНОСТЬ ===== */
/* ============================================ */

@media (max-width: 640px) {
    .user-info-card {
        flex-direction: column;
        text-align: center;
        padding: 16px;
    }

    .user-avatar {
        width: 60px;
        height: 60px;
    }

    .user-meta {
        justify-content: center;
    }

    .modal-form-row {
        grid-template-columns: 1fr;
        gap: 0;
    }

    .modal-actions {
        flex-direction: column;
    }

    .modal-actions .btn {
        width: 100%;
        padding: 0.8rem;
    }

    .modal-info-block {
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .modal-info-icon {
        margin-top: 0;
    }
}

@media (max-width: 400px) {
    .user-avatar {
        width: 48px;
        height: 48px;
    }

    .user-name {
        font-size: 14px;
    }

    .modal-form-group input,
    .modal-form-group select {
        font-size: 0.9rem;
        padding: 0.5rem 0.7rem;
    }
}
</style>