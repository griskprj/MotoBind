<template>
    <ModalWrapper
        :isOpen="isOpen"
        :title="'Жалоба #' + report.id"
        @close="this.$emit('close')"
    >
        <!-- Инфо о жалобе -->
        <div class="info-block">
            <div class="info-row">
                <span class="info-label">Категория:</span>
                <span class="info-value danger">{{ report.category_label }}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Отправитель:</span>
                <span class="info-value">{{ report.reporter || '—' }}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Дата:</span>
                <span class="info-value">{{ formatDate(report.created_at) }}</span>
            </div>
            <div v-if="report.description" class="info-row full">
                <span class="info-label">Комментарий:</span>
                <p class="info-description">{{ report.description }}</p>
            </div>
        </div>

        <!-- Пост -->
        <div class="post-block">
            <h4 class="block-title">
                <i class="fa fa-file-text"></i> Пост
                <span v-if="report.post?.is_deleted" class="deleted-tag">удалён</span>
            </h4>
            <div class="post-preview">
                <div class="post-author">
                    <img :src="getAvatarUrl(report.post?.author_avatar)" class="avatar" @error="onAvatarError">
                    <span>{{ report.post?.author || 'Неизвестный автор' }}</span>
                </div>
                <p class="post-content">{{ report.post?.content || '—' }}</p>
                <img v-if="report.post?.image" :src="getImageUrl(report.post.image)" class="post-image" alt="Post">
            </div>
        </div>

        <!-- Действия (только для pending) -->
        <template v-if="report.status === 'pending'">
            <h4 class="block-title"><i class="fa fa-gavel"></i> Решение модератора</h4>

            <div class="action-options">
                <label class="action-item" :class="{ selected: action === 'post_deleted' }">
                    <input type="radio" value="post_deleted" v-model="action">
                    <i class="fa fa-trash"></i>
                    <span>Удалить пост</span>
                </label>
                <label class="action-item" :class="{ selected: action === 'user_banned' }">
                    <input type="radio" value="user_banned" v-model="action">
                    <i class="fa fa-ban"></i>
                    <span>Заблокировать автора</span>
                </label>
                <label class="action-item" :class="{ selected: action === 'both' }">
                    <input type="radio" value="both" v-model="action">
                    <i class="fa fa-times-circle"></i>
                    <span>Удалить и заблокировать</span>
                </label>
                <label class="action-item reject" :class="{ selected: action === 'none' }">
                    <input type="radio" value="none" v-model="action">
                    <i class="fa fa-check-circle"></i>
                    <span>Отклонить жалобу</span>
                </label>
            </div>

            <div class="modal-form-group">
                <label>Примечание <span class="muted">(необязательно)</span></label>
                <textarea v-model="note" rows="2" maxlength="300" placeholder="Причина решения..."></textarea>
            </div>

            <div class="modal-actions">
                <button class="btn btn-secondary" @click="close" :disabled="submitting">Отмена</button>
                <button
                    class="btn"
                    :class="action === 'none' ? 'btn-success' : 'btn-danger'"
                    :disabled="!action || submitting"
                    @click="submit"
                >
                    <i v-if="submitting" class="fa fa-spinner fa-spin"></i>
                    <i v-else class="fa fa-check"></i>
                    {{ submitting ? 'Отправка...' : 'Применить' }}
                </button>
            </div>
        </template>

        <!-- Итог (для resolved/rejected) -->
        <div v-else class="resolved-info">
            <p><strong>Статус:</strong> {{ statusLabel(report.status) }}</p>
            <p v-if="report.resolution_action"><strong>Действие:</strong> {{ actionLabel(report.resolution_action) }}</p>
            <p v-if="report.resolution_note"><strong>Примечание:</strong> {{ report.resolution_note }}</p>
            <p v-if="report.resolved_at"><strong>Рассмотрено:</strong> {{ formatDate(report.resolved_at) }}</p>
            <p v-if="report.resolver"><strong>Модератор:</strong> {{ report.resolver }}</p>
        </div>
    </ModalWrapper>
</template>

<script>
import api from '../../../api/api'
import ModalWrapper from '../ModalWrapper.vue';

export default {
    components: { ModalWrapper },
    name: 'ReportDetailsModal',
    props: {
        isOpen: Boolean,
        report: Object,
    },
    emits: ['close', 'resolved'],
    data() {
        return { action: '', note: '', submitting: false }
    },
    methods: {
        close() { if (!this.submitting) this.$emit('close') },

        async submit() {
            if (!this.action || this.submitting) return
            this.submitting = true
            try {
                await api.post(`/admin/reports/${this.report.id}/resolve`, {
                    action: this.action,
                    note: this.note.trim() || null,
                })
                this.$emit('resolved')
            } catch (err) {
                alert(err.response?.data?.error || 'Не удалось рассмотреть жалобу')
            } finally {
                this.submitting = false
            }
        },

        statusLabel(s) {
            return { pending: 'На рассмотрении', resolved: 'Рассмотрено', rejected: 'Отклонено' }[s] || s
        },
        actionLabel(a) {
            return {
                post_deleted: 'Пост удалён',
                user_banned: 'Автор заблокирован',
                both: 'Пост удалён, автор заблокирован',
                none: 'Жалоба отклонена',
            }[a] || a
        },
        formatDate(d) {
            return d ? new Date(d).toLocaleString('ru-RU') : '—'
        },
        getAvatarUrl(p) {
            if (!p) return '/BaseAvatar.webp'
            if (p.startsWith('http')) return p
            return `${import.meta.env.VITE_API_URL || ''}/uploads/${p}`
        },
        getImageUrl(p) {
            if (!p) return ''
            if (p.startsWith('http')) return p
            return `${import.meta.env.VITE_API_URL || ''}/uploads/${p}`
        },
        onAvatarError(e) { e.target.src = '/BaseAvatar.webp' },
    },
}
</script>

<style scoped>
.report-details-modal { max-width: 640px; }

.info-block {
    background: var(--bg-secondary);
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.info-row { display: flex; gap: 8px; font-size: 14px; }
.info-row.full { flex-direction: column; }
.info-label { color: var(--text-muted); min-width: 100px; }
.info-value { color: var(--text-primary); font-weight: 500; }
.info-value.danger { color: var(--danger-text); }
.info-description {
    color: var(--text-secondary);
    margin: 4px 0 0;
    line-height: 1.5;
    background: var(--bg-input);
    padding: 8px 12px;
    border-radius: 8px;
}

.block-title {
    font-size: 15px;
    color: var(--text-primary);
    margin: 16px 0 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.block-title i { color: var(--accent-text); }
.deleted-tag {
    font-size: 11px;
    background: var(--danger-trans);
    color: var(--danger-text);
    padding: 2px 8px;
    border-radius: 10px;
    margin-left: auto;
}

.post-preview {
    background: var(--bg-secondary);
    border-radius: 12px;
    padding: 12px 14px;
    border: 1px solid var(--border-light);
}
.post-author {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    font-size: 13px;
    color: var(--text-primary);
    margin-bottom: 8px;
}
.avatar { width: 28px; height: 28px; border-radius: 50%; object-fit: cover; }
.post-content { font-size: 14px; color: var(--text-secondary); margin: 0 0 8px; white-space: pre-wrap; }
.post-image { max-width: 100%; border-radius: 8px; max-height: 240px; object-fit: cover; }

.action-options {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-bottom: 14px;
}
.action-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 12px;
    border: 2px solid var(--border-color);
    border-radius: 10px;
    background: var(--bg-secondary);
    cursor: pointer;
    transition: all 0.2s;
    font-size: 13px;
    font-weight: 500;
    color: var(--text-secondary);
}
.action-item input { display: none; }
.action-item i { color: var(--text-muted); width: 16px; }
.action-item:hover { border-color: var(--accent); }
.action-item.selected { border-color: var(--accent); background: var(--accent-trans); color: var(--text-primary); }
.action-item.selected i { color: var(--accent-text); }
.action-item.reject.selected { border-color: var(--success); background: var(--success-trans); color: var(--success-text); }
.action-item.reject.selected i { color: var(--success-text); }

.resolved-info {
    background: var(--bg-secondary);
    border-radius: 12px;
    padding: 14px 16px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    font-size: 14px;
    color: var(--text-secondary);
}
.muted { color: var(--text-muted); font-weight: 400; }

@media (max-width: 520px) {
    .action-options { grid-template-columns: 1fr; }
}
</style>