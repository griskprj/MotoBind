<script setup lang="ts">
import type { Maintenance, ApiError } from '~/types'

const props = defineProps<{
  maintenance: Maintenance
}>()

const emit = defineEmits<{
  close: []
  deleted: []
}>()

const api = useApi()
const toast = useToast()
const deleting = ref(false)

async function onDelete() {
  deleting.value = true
  try {
    await api.maintenance.remove(props.maintenance.id)
    toast.success('Запись удалена')
    emit('deleted')
    emit('close')
  } catch (e) {
    toast.error((e as ApiError).message || 'Ошибка удаления')
  } finally {
    deleting.value = false
  }
}
</script>

<template>
  <BaseModal title="Удалить запись?" size="sm" @close="emit('close')">
    <div class="delete-content">
      <div class="alert-icon">
        <i class="fa-solid fa-triangle-exclamation"></i>
      </div>
      <p class="delete-text">
        Вы действительно хотите удалить запись <strong>«{{ maintenance.title }}»</strong>?
      </p>
      <p class="delete-warning">
        Это действие нельзя отменить. Вся информация об этой работе будет удалена навсегда.
      </p>
    </div>

    <template #footer>
      <BaseButton variant="ghost" size="sm" @click="emit('close')">
        Отмена
      </BaseButton>
      <BaseButton variant="danger" size="sm" :loading="deleting" @click="onDelete">
        <template #icon><i class="fa-solid fa-trash"></i></template>
        Удалить
      </BaseButton>
    </template>
  </BaseModal>
</template>

<style scoped lang="scss">
.delete-content {
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
  background: var(--color-danger-soft);
  color: var(--color-danger);
  font-size: 24px;
  margin-bottom: var(--space-2);
}

.delete-text {
  font-size: var(--text-base);
  color: var(--color-text);

  strong {
    font-weight: var(--fw-semibold);
  }
}

.delete-warning {
  font-size: var(--text-sm);
  color: var(--color-text-tertiary);
  line-height: var(--leading-relaxed);
}
</style>
