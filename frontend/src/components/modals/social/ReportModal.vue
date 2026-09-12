<template>
    <div v-if="isOpen" class="modal-wrapper" @click.self="close">
        <div class="modal-container report-modal">
            <div class="modal-header">
                <h3 class="modal-title">
                    <i class="fa fa-flag"></i> Жалоба на пост
                </h3>
                <button class="close-btn" @click="close" :disabled="submitting">
                    <i class="fa fa-times"></i>
                </button>
            </div>

            <p class="modal-hint">
                Выберите причину жалобы. Модератор рассмотрит её в ближайшее время.
            </p>

            <div class="category-list">
                <label
                    v-for="cat in categories"
                    :key="cat.value"
                    class="category-item"
                    :class="{ selected: category === cat.value }"
                >
                    <input type="radio" :value="cat.value" v-model="category" />
                    <div class="category-icon"><i :class="cat.icon"></i></div>
                    <div class="category-info">
                        <span class="category-title">{{ cat.label }}</span>
                        <span class="category-desc">{{ cat.description }}</span>
                    </div>
                </label>
            </div>

            <div class="modal-form-group">
                <label>Комментарий <span class="muted">(необязательно)</span></label>
                <textarea
                    v-model="description"
                    rows="3"
                    maxlength="500"
                    placeholder="Опишите подробнее, что нарушает правила..."
                ></textarea>
                <span class="char-count">{{ description.length }}/500</span>
            </div>

            <div class="modal-actions">
                <button class="btn btn-secondary" @click="close" :disabled="submitting">
                    Отмена
                </button>
                <button
                    class="btn btn-danger"
                    @click="submit"
                    :disabled="!category || submitting"
                >
                    <i v-if="submitting" class="fa fa-spinner fa-spin"></i>
                    <i v-else class="fa fa-flag"></i>
                    {{ submitting ? 'Отправка...' : 'Отправить жалобу' }}
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import socialApi from '../../../api/social'

export default {
    name: 'ReportModal',
    props: {
        isOpen: { type: Boolean, default: false },
        post: { type: Object, default: null },
    },
    emits: ['close', 'reported'],
    data() {
        return {
            category: '',
            description: '',
            submitting: false,
            categories: [
                { value: 'sexual_content', label: 'Контент сексуального характера', icon: 'fa fa-exclamation-triangle', description: 'Порнография, откровенные материалы' },
                { value: 'hate_speech',      label: 'Разжигание межнациональной розни', icon: 'fa fa-users', description: 'Оскорбления по национальному признаку' },
                { value: 'extremism',        label: 'Экстремистская символика', icon: 'fa fa-ban', description: 'Запрещённая символика и материалы' },
                { value: 'violence',         label: 'Насилие и жестокость', icon: 'fa fa-fist-raised', description: 'Сцены насилия, угрозы' },
                { value: 'drugs',            label: 'Пропаганда наркотиков', icon: 'fa fa-pills', description: 'Упоминание и пропаганда запрещённых веществ' },
                { value: 'spam',             label: 'Спам и мошенничество', icon: 'fa fa-bullhorn', description: 'Реклама, обман' },
                { value: 'other',            label: 'Другое', icon: 'fa fa-ellipsis-h', description: 'Иные нарушения' },
            ],
        }
    },
    methods: {
        close() {
            if (this.submitting) return
            this.category = ''
            this.description = ''
            this.$emit('close')
        },
        async submit() {
            if (!this.category || this.submitting || !this.post) return
            this.submitting = true
            try {
                await socialApi.reportPost(this.post.id, {
                    category: this.category,
                    description: this.description.trim() || null,
                })
                this.$emit('reported')
                alert('Жалоба отправлена. Спасибо!')
                this.close()
            } catch (err) {
                alert(err.response?.data?.error || 'Не удалось отправить жалобу')
            } finally {
                this.submitting = false
            }
        },
    },
}
</script>

<style scoped>
.report-modal { max-width: 520px; }

.modal-hint {
    color: var(--text-secondary);
    font-size: 14px;
    margin: 0 0 16px;
    line-height: 1.5;
}

.category-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 16px;
    max-height: 40vh;
    overflow-y: auto;
    padding-right: 4px;
}

.category-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 25px 14px;
    border: 2px solid var(--border-color);
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s;
    background: var(--bg-secondary);
    overflow-y: hidden;
}

.category-item:hover {
    border-color: var(--accent);
    background: var(--accent-trans);
}

.category-item.selected {
    border-color: var(--accent);
    background: var(--accent-trans);
}

.category-item input[type="radio"] {
    display: none;
}

.category-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: var(--bg-card);
    color: var(--accent-text);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-size: 15px;
}

.category-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0;
}

.category-title {
    font-weight: 600;
    font-size: 14px;
    color: var(--text-primary);
}

.category-desc {
    font-size: 12px;
    color: var(--text-muted);
}

.char-count {
    display: block;
    text-align: right;
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 4px;
}

.muted { color: var(--text-muted); font-weight: 400; }
</style>