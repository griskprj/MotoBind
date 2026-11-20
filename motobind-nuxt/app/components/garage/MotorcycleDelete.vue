<script setup lang="ts">
import type { Motorcycle, ApiError } from '~/types'

const props = defineProps<{ motorcycle: Motorcycle }>()
const api = useApi()
const router = useRouter()
const toast = useToast()

const showConfirm = ref(false)
const deleting = ref(false)

async function onDelete() {
  deleting.value = true
  try {
    await api.motorcycle.remove(props.motorcycle.id)
    toast.success('Мотоцикл удалён')
    router.push('/garage')
  } catch (e) {
    toast.error((e as ApiError).message || 'Ошибка удаления')
    showConfirm.value = false
  } finally {
    deleting.value = false
  }
}
</script>

<template>
  <BaseCard padding="lg" class="danger-card">
    <h2 class="danger-title">Опасная зона</h2>
    <p class="danger-desc">Удаление мотоцикла также удалит всю историю его обслуживания и фотографии.</p>
    <BaseButton variant="danger" block @click="showConfirm = true">
      Удалить мотоцикл
    </BaseButton>
  </BaseCard>

  <BaseConfirm
    v-if="showConfirm"
    title="Удалить мотоцикл?"
    :message="`Вы уверены, что хотите удалить ${motorcycle.name}? Это действие необратимо.`"
    confirm-text="Удалить"
    :loading="deleting"
    @confirm="onDelete"
    @cancel="showConfirm = false"
  />
</template>

<style scoped lang="scss">
.danger-card {
  border-color: var(--color-danger-soft);
  background: color-mix(in srgb, var(--color-danger-soft) 30%, var(--color-surface));
}

.danger-title {
  font-size: var(--text-lg);
  font-weight: var(--fw-semibold);
  color: var(--color-danger);
  margin-bottom: var(--space-2);
}

.danger-desc {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-4);
  line-height: var(--leading-relaxed);
}
</style>
