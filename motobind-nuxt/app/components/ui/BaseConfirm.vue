<script setup lang="ts">
interface Props {
  title?: string
  message: string
  confirmText?: string
  cancelText?: string
  variant?: 'danger' | 'primary'
  loading?: boolean
}

withDefaults(defineProps<Props>(), {
  title: 'Подтверждение',
  confirmText: 'Подтвердить',
  cancelText: 'Отмена',
  variant: 'danger',
  loading: false,
})

const emit = defineEmits<{
  confirm: []
  cancel: []
}>()
</script>

<template>
  <BaseModal :title="title" size="sm" @close="emit('cancel')">
    <div class="confirm-content">
      <div class="alert-icon" :class="`alert-icon--${variant}`">
        <i class="fa-solid fa-triangle-exclamation"></i>
      </div>
      <p class="confirm-text">{{ message }}</p>
    </div>

    <template #footer>
      <BaseButton variant="ghost" size="sm" :disabled="loading" @click="emit('cancel')">
        {{ cancelText }}
      </BaseButton>
      <BaseButton :variant="variant" size="sm" :loading="loading" @click="emit('confirm')">
        {{ confirmText }}
      </BaseButton>
    </template>
  </BaseModal>
</template>

<style scoped lang="scss">
.confirm-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--space-3);
  padding: var(--space-2) 0;
}

.alert-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  font-size: 24px;
  margin-bottom: var(--space-2);

  &--danger {
    background: var(--color-danger-soft);
    color: var(--color-danger);
  }
  &--primary {
    background: var(--color-brand-soft);
    color: var(--color-brand);
  }
}

.confirm-text {
  font-size: var(--text-base);
  color: var(--color-text);
  line-height: var(--leading-relaxed);
}
</style>
