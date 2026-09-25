<template>
  <BaseModal
    :is-open="isOpen"
    title="Удаление обслуживания"
    subtitle="Вы уверены, что хотите удалить эту запись?"
    icon="trash"
    variant="danger"
    size="sm"
    @close="$emit('close')"
  >
    <div class="modal-info-block danger">
      <div class="modal-info-icon">
        <i class="fa fa-exclamation-triangle"></i>
      </div>
      <div>
        <p class="modal-info-text modal-info-text--strong">
          Это действие нельзя отменить!
        </p>
        <p class="modal-info-text">
          Запись об обслуживании будет удалена безвозвратно.
          Все связанные данные будут потеряны.
        </p>
      </div>
    </div>

    <template #actions>
      <BaseButton variant="secondary" block @click="$emit('close')">
        Отменить
      </BaseButton>
      <BaseButton variant="danger" icon="fa fa-trash" block @click="$emit('submit')">
        Удалить
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup>
import { BaseModal, BaseButton } from '@/components/ui'

defineProps({
  isOpen: { type: Boolean, default: false },
  maintenanceId: { type: [Number, null], default: null },
})

defineEmits(['close', 'submit'])
</script>

<style scoped>
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
}
</style>
