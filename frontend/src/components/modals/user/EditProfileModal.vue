<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Редактирование профиля"
        subtitle="Измените информацию о себе. Эти данные будут видны другим пользователям."
        icon="user"
        bg-icon-color="var(--accent-trans)"
        icon-color="var(--accent-text)"
        @close="$emit('close')"
    >
        <!-- Форма -->
        <div class="modal-form-group">
            <label>
                Имя пользователя
                <input 
                    v-model="form.username" 
                    type="text" 
                    placeholder="Введите имя пользователя"
                />
            </label>
        </div>

        <div class="modal-form-group">
            <label>
                Email
                <input 
                    v-model="form.email" 
                    type="email" 
                    placeholder="user@example.com"
                />
            </label>
        </div>

        <div class="modal-form-group">
            <label>
                О себе
                <textarea 
                    v-model="form.bio" 
                    rows="3"
                    placeholder="Расскажите немного о себе, своём опыте и мотоцикле..."
                ></textarea>
            </label>
        </div>

        <div class="modal-form-row">
            <div class="modal-form-group">
                <label>
                    Город/Регион
                    <input 
                        v-model="form.location" 
                        type="text" 
                        placeholder="Например: Москва"
                    />
                </label>
            </div>
            <div class="modal-form-group">
                <label>
                    Мой мотоцикл
                    <input 
                        v-model="form.motorcycle" 
                        type="text" 
                        placeholder="Например: BMW S1000RR"
                    />
                </label>
            </div>
        </div>

        <div class="modal-form-group">
            <label>
                Опыт вождения
                <select v-model="form.experience">
                    <option value="">Не указано</option>
                    <option value="beginner">Новичок</option>
                    <option value="intermediate">Опытный</option>
                    <option value="expert">Эксперт</option>
                </select>
            </label>
        </div>

        <div class="modal-form-group">
            <label>
                Социальные сети
                <div class="social-links-editor">
                    <div 
                        v-for="platform in socialPlatforms" 
                        :key="platform"
                        class="social-link-row"
                    >
                        <i :class="getSocialIcon(platform)" class="social-icon"></i>
                        <input 
                            v-model="form.social_links[platform]" 
                            :placeholder="`Ссылка на ${platform}`"
                        />
                        <button 
                            v-if="form.social_links[platform]" 
                            class="clear-link"
                            @click="form.social_links[platform] = ''"
                            type="button"
                        >
                            <i class="fa fa-times"></i>
                        </button>
                    </div>
                </div>
            </label>
        </div>

        <div class="modal-info-block info">
            <div class="modal-info-icon">
                <i class="fa fa-info-circle"></i>
            </div>
            <p class="modal-info-text">
                Эти данные будут отображаться в вашем публичном профиле.
            </p>
        </div>

        <template #actions>
            <div class="modal-actions">
                <button class="btn btn-secondary" @click="$emit('close')">
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
            default: null,
            required: true
        }
    },

    data() {
        return {
            form: {
                username: '',
                email: '',
                bio: '',
                location: '',
                motorcycle: '',
                experience: '',
                social_links: {
                    youtube: '',
                    telegram: '',
                    vk: '',
                }
            },
            loading: false,
            socialPlatforms: ['youtube', 'telegram', 'vk']
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
                username: this.user.username || '',
                email: this.user.email || '',
                bio: this.user.bio || '',
                location: this.user.location || '',
                motorcycle: this.user.motorcycle || '',
                experience: this.user.experience || '',
                social_links: {
                    youtube: this.user.social_links?.youtube || '',
                    telegram: this.user.social_links?.telegram || '',
                    vk: this.user.social_links?.vk || '',
                }
            }
        },

        resetForm() {
            this.form = {
                username: '',
                email: '',
                bio: '',
                location: '',
                motorcycle: '',
                experience: '',
                social_links: {
                    youtube: '',
                    telegram: '',
                    vk: '',
                }
            }
            this.loading = false
        },

        getSocialIcon(platform) {
            return 'fa fa-link'
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

.modal-form-group input,
.modal-form-group textarea,
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
}

.modal-form-group input:focus,
.modal-form-group textarea:focus,
.modal-form-group select:focus {
    border-color: var(--accent);
    outline: none;
    box-shadow: 0 0 0 3px var(--accent-trans);
}

.modal-form-group input::placeholder,
.modal-form-group textarea::placeholder {
    color: var(--text-muted);
}

.modal-form-group textarea {
    resize: vertical;
    min-height: 80px;
}

.modal-form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}

/* ===== СОЦИАЛЬНЫЕ СЕТИ ===== */
.social-links-editor {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.social-link-row {
    display: flex;
    align-items: center;
    gap: 10px;
}

.social-icon {
    width: 24px;
    font-size: 18px;
    color: var(--text-muted);
}

.social-link-row input {
    flex: 1;
}

.clear-link {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 4px 8px;
}

.clear-link:hover {
    color: var(--danger);
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
    .modal-form-group input,
    .modal-form-group textarea,
    .modal-form-group select {
        font-size: 0.9rem;
        padding: 0.5rem 0.7rem;
    }
}
</style>