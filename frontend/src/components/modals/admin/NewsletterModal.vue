<template>
    <ModalWrapper
        :isOpen="isOpen"
        title="Отправить рассылку"
        subtitle="Всем пользователям или выбранной группе"
        icon="envelope"
        size="lg"
        @close="close"
    >
        <form @submit.prevent="submit" class="newsletter-form">
            <div class="field">
                <label>Тема письма <span>*</span></label>
                <input 
                    v-model="form.subject" 
                    type="text" 
                    placeholder="Новое обновление MotoBind"
                    required
                />
            </div>

            <div class="field">
                <label>Целевая аудитория <span>*</span></label>
                <select v-model="form.target" required>
                    <option value="all">Все пользователи</option>
                    <option value="active">Только активные</option>
                    <option value="admins">Только администраторы</option>
                </select>
            </div>

            <div class="field">
                <label>Содержание письма <span>*</span></label>
                <textarea 
                    v-model="form.content" 
                    rows="8"
                    placeholder="Текст письма. Поддерживается HTML..."
                    required
                ></textarea>
            </div>

            <div class="field">
                <label>Предпросмотр</label>
                <div class="preview" v-html="form.content || 'Текст письма будет здесь...'"></div>
            </div>

            <div class="info-box info">
                <i class="fa fa-info-circle"></i>
                <span>
                    Рассылка будет отправлена асинхронно. 
                    Вы получите уведомление о завершении.
                </span>
            </div>

            <div class="actions">
                <button type="button" class="btn btn-secondary" @click="close">
                    Отмена
                </button>
                <button type="submit" class="btn btn-primary" :disabled="!isValid || loading">
                    <span v-if="!loading">Отправить</span>
                    <span v-else><i class="fa fa-spinner fa-spin"></i> Отправка...</span>
                </button>
            </div>
        </form>
    </ModalWrapper>
</template>

<script>
import api from '../../../api/api'
import ModalWrapper from '../ModalWrapper.vue'

export default {
    components: { ModalWrapper },
    props: {
        isOpen: Boolean
    },
    emits: ['close', 'sent'],
    data() {
        return {
            loading: false,
            form: {
                subject: '',
                content: '',
                target: 'all'
            }
        }
    },
    computed: {
        isValid() {
            return this.form.subject.trim() && this.form.content.trim()
        }
    },
    watch: {
        isOpen(val) {
            if (!val) {
                this.form = { subject: '', content: '', target: 'all' }
                this.loading = false
            }
        }
    },
    methods: {
        close() {
            this.$emit('close')
        },
        async submit() {
            if (!this.isValid) return
            this.loading = true
            try {
                await api.post('/admin/send-newsletter', this.form)
                this.$emit('sent')
                this.$toast?.success('Рассылка запущена!')
                this.close()
            } catch (err) {
                console.error('Failed to send newsletter:', err)
                this.$toast?.error(err.response?.data?.error || 'Ошибка отправки')
            } finally {
                this.loading = false
            }
        }
    }
}
</script>

<style scoped>
.newsletter-form {
    display: flex;
    flex-direction: column;
    gap: 14px;
}

.field {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.field label {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-secondary);
}

.field label span {
    color: var(--danger);
}

.field input,
.field select,
.field textarea {
    padding: 10px 14px;
    background: var(--bg-input);
    border: 2px solid var(--border-color);
    border-radius: 10px;
    color: var(--text-primary);
    font-size: 14px;
    font-family: inherit;
    transition: all 0.2s;
}

.field input:focus,
.field select:focus,
.field textarea:focus {
    border-color: var(--accent);
    outline: none;
    box-shadow: 0 0 0 3px var(--accent-trans);
}

.field textarea {
    resize: vertical;
    min-height: 120px;
}

.preview {
    padding: 12px 16px;
    background: var(--bg-secondary);
    border-radius: 10px;
    border: 1px solid var(--border-light);
    min-height: 60px;
    font-size: 14px;
    color: var(--text-secondary);
    line-height: 1.6;
}

.preview:empty::before {
    content: 'Текст письма будет здесь...';
    color: var(--text-muted);
    font-style: italic;
}

.info-box {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 16px;
    border-radius: 10px;
    font-size: 13px;
}

.info-box.info {
    background: var(--accent-trans);
    color: var(--text-secondary);
}

.info-box i {
    color: var(--accent-text);
    font-size: 18px;
    flex-shrink: 0;
}

.actions {
    display: flex;
    gap: 10px;
    margin-top: 4px;
}

.actions .btn {
    flex: 1;
    padding: 10px;
    border-radius: 10px;
    font-weight: 600;
    font-size: 14px;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
}

.btn-primary {
    background: var(--accent);
    color: #fff;
}

.btn-primary:hover:not(:disabled) {
    background: var(--accent-hover);
    transform: translateY(-2px);
}

.btn-secondary {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}

.btn-secondary:hover {
    background: var(--border-color);
}

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

@media (max-width: 640px) {
    .actions {
        flex-direction: column;
    }
    .actions .btn {
        width: 100%;
    }
}
</style>