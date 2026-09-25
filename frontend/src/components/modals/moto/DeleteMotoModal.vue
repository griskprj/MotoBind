<template>
  <BaseModal
    v-if="motorcycle"
    :is-open="isOpen"
    title="Удалить мотоцикл"
    subtitle="Вы уверены, что хотите удалить этот мотоцикл?"
    icon="trash"
    variant="danger"
    size="sm"
    @close="$emit('close')"
  >
    <div class="moto-info-card">
      <div class="moto-info-icon">
        <i class="fa fa-motorcycle"></i>
      </div>
      <div class="moto-info-content">
        <div class="moto-info-name">{{ motorcycle.name || '—' }}</div>
        <div class="moto-info-meta">
          <span v-if="motorcycle.years">{{ motorcycle.years }}</span>
          <span v-if="motorcycle.years && motorcycle.mileage !== undefined">•</span>
          <span v-if="motorcycle.mileage !== undefined">{{ motorcycle.mileage }} км</span>
          <span v-if="!motorcycle.years && motorcycle.mileage === undefined">Нет данных</span>
        </div>
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
          Будут удалены все данные, связанные с этим мотоциклом:
          обслуживание, файлы, статистика и история.
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
        @click="$emit('submit', motorcycle.id)"
      >
        Удалить
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup>
import { BaseModal, BaseButton } from '@/components/ui'

defineProps({
  isOpen: { type: Boolean, default: false },
  motorcycle: { type: Object, default: null },
})

defineEmits(['close', 'submit'])
</script>

<style scoped>
.moto-info-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 16px;
  background: var(--bg-secondary);
  border-radius: 12px;
  border: 1px solid var(--border-light);
  margin-bottom: 16px;
}

.moto-info-icon {
  width: 44px;
  height: 44px;
  min-width: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background: var(--accent-trans);
  color: var(--accent-text);
  font-size: 20px;
}

.moto-info-content { flex: 1; min-width: 0; }

.moto-info-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.moto-info-meta { font-size: 13px; color: var(--text-muted); }

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
  .moto-info-card {
    flex-direction: column;
    text-align: center;
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
</style>
