<template>
  <BaseModal
    v-if="user"
    :is-open="isOpen"
    title="Удаление пользователя"
    subtitle="Вы уверены, что хотите удалить этого пользователя?"
    icon="trash"
    variant="danger"
    size="sm"
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
        <p class="modal-info-text modal-info-text--strong">
          Это действие нельзя отменить!
        </p>
        <p class="modal-info-text">
          Все данные пользователя будут удалены: мотоциклы, обслуживание, мануалы и личная информация.
        </p>
      </div>
    </div>

    <template #actions>
      <BaseButton variant="secondary" block @click="$emit('close')">
        Отменить
      </BaseButton>
      <BaseButton
        variant="danger"
        icon="fa fa-trash"
        block
        @click="$emit('submit', user.id)"
      >
        Удалить
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup>
import { BaseModal, BaseButton } from '@/components/ui'

defineProps({
  isOpen: Boolean,
  user: { type: Object, default: null },
})

defineEmits(['close', 'submit'])

function formatDate(dateString) {
  if (!dateString) return '—'
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) return '—'
    return date.toLocaleDateString('ru-RU', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    })
  } catch {
    return '—'
  }
}
</script>

<style scoped>
.modal-data-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 16px 18px;
  margin-bottom: 16px;
}

.modal-data-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid var(--border-light);
}

.modal-data-item:last-child {
  border-bottom: none;
}

.modal-data-label {
  font-size: 13px;
  color: var(--text-muted);
}

.modal-data-value {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.modal-info-block {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 10px;
}

.modal-info-block.danger {
  background: var(--danger-trans);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.modal-info-icon {
  font-size: 20px;
  color: var(--danger-text);
  flex-shrink: 0;
  margin-top: 2px;
}

.modal-info-text {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
}

.modal-info-text--strong {
  font-weight: 600;
  color: var(--danger-text);
}

@media (max-width: 640px) {
  .modal-info-block {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  .modal-info-icon {
    margin-top: 0;
  }
  .modal-data-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 2px;
  }
}
</style>
