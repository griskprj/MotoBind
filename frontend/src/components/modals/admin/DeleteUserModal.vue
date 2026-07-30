<template>
    <ModalWrapper
        v-if="user"
        :is-open="isOpen"
        title="Удаление пользователя"
        @close="$emit('close')"
        icon="trash"
        iconColor="var(--danger)"
        bgIconColor="var(--danger-trans)"
        subtitle="Вы уверены, что хотите удалить этого пользователя?"
    >
        <div class="user-card">
            <div class="card-icon">
                <i class="fa fa-user"></i>
            </div>
            <div class="card-body">
                <p class="card-title">{{ user.username }}</p>
                <span class="card-subtitle">ID: {{ user.id }}</span> • <span class="card-subtitle">Пользователь с {{ formatDate(user.created_at) }}</span>
            </div>
        </div>
        <div class="danger-block">
            <div class="block-icon">
                <i class="fa fa-exclamation-triangle"></i>
            </div>
            <div class="block-wrappper">
                <p class="block-title">Это действие нельзя отменить</p>
                <p class="block-text">
                    Все данные пользователя будут удалены: обслуживание, мотоциклы и т.д.
                </p>
            </div>
        </div>
        <div class="modal-actions">
            <button @click="$emit('close')" class="outline-btn">Отменить</button>
            <button @click="submit" class="btn-danger"><i class="fa fa-trash"></i> Удалить пользователя</button>
        </div>
    </ModalWrapper>
</template>

<script>
import ModalWrapper from '../ModalWrapper.vue';

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
            if (!dateString) return '--'
            
            try {
                if (dateString instanceof Date) {
                    return dateString.toLocaleDateString('ru-RU', {
                        day: '2-digit',
                        month: 'short',
                        year: 'numeric'
                    })
                }
                
                const date = new Date(dateString)
                
                if (isNaN(date.getTime())) {
                    return '--'
                }
                
                return date.toLocaleDateString('ru-RU', {
                    day: '2-digit',
                    month: 'short',
                    year: 'numeric'
                })
            } catch (error) {
                console.error('Error formatting date:', dateString, error)
                return '--'
            }
        },
    }
}
</script>

<style scoped>
.user-card {
    display: flex;
    flex-direction: row;
    gap: 16px;
    padding: 12px;
    border-radius: 14px;
    align-items: center;

    background-color: var(--bg-card);
}

.card-icon {
    height: 48px;
    width: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background-color: var(--danger-trans);
    color: var(--danger);
}

.card-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 8px;
}

.card-subtitle {
    font-size: 14px;
    color: var(--text-secondary);
    font-weight: 400;
}

.danger-block {
    display: flex;
    padding: 12px;
    background-color: var(--danger-trans);
    border-radius: 10px;
    border: 1px solid var(--danger);
}

.block-icon {
    color: var(--danger);
    font-size: 24px;
    margin-right: 8px;
}

.block-title {
    color: var(--danger);
    font-weight: 600;
    margin-bottom: 4px;
}

.block-text {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 0;
}

.modal-actions {
    flex-direction: row;
}

.modal-actions button {
    width: 100%;
}

.outline-btn {
    border-color: var(--bg-card);
    color: var(--text-muted);
}
.outline-btn:hover {
    color: var(--text-primary);
    background-color: var(--success);
}
</style>