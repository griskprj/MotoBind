<template>
    <ModalWrapper
        v-if="user"
        :is-open="isOpen"
        title="Удаление пользователя"
        subtitle="Вы уверены, что хотите удалить этого пользователя?"
        icon="trash"
        icon-color="var(--danger-text)"
        bg-icon-color="var(--danger-trans)"
        @close="$emit('close')"
    >
        <div class="modal-data-card">
            <div class="modal-data-item">
                <span class="modal-data-label">Пользователь</span>
                <span class="modal-data-value">{{ user.username }}</span>
            </div>
            <div class="modal-data-item">
                <span class="modal-data-label">ID</span>
                <span class="modal-data-value">#{{ user.id }}</span>
            </div>
            <div class="modal-data-item">
                <span class="modal-data-label">Дата регистрации</span>
                <span class="modal-data-value">{{ formatDate(user.created_at) }}</span>
            </div>
        </div>

        <div class="modal-info-block danger">
            <div class="modal-info-icon">
                <i class="fa fa-exclamation-triangle"></i>
            </div>
            <div>
                <p class="modal-info-text" style="font-weight: 600; color: var(--danger-text);">
                    Это действие нельзя отменить!
                </p>
                <p class="modal-info-text">
                    Все данные пользователя будут удалены: мотоциклы, обслуживание, мануалы и личная информация.
                </p>
            </div>
        </div>

        <template #actions>
            <div class="modal-actions">
                <button class="btn btn-secondary" @click="$emit('close')">
                    Отменить
                </button>
                <button class="btn btn-danger" @click="submit">
                    <i class="fa fa-trash"></i> Удалить
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
        isOpen: Boolean,
        user: {
            type: Object,
            default: null
        }
    },

    methods: {
        submit() {
            this.$emit('submit', this.user.id)
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
    }
}
</script>