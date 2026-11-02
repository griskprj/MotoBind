<script setup lang="ts">
import type { Motorcycle } from '~/types'

const api = useApi()
const toast = useToast()
const router = useRouter()

const props = defineProps<{
  motorcycle: Motorcycle
}>()

const mediaUrl = useMediaUrl()

const plannedCount = computed(() => {
  return props.motorcycle.maintenances?.filter(m => m.status === 'planned').length || 0
})

const photo = computed(() => mediaUrl(props.motorcycle.photo_url))


const emit = defineEmits<{ updated: [] }>()

const isMileageModalOpen = ref(false)
const isDeleteConfirmOpen = ref(false)
const deleting = ref(false)

async function onDelete() {
  deleting.value = true

  try {
    await api.motorcycle.remove(props.motorcycle.id)
    toast.success('Мотоцикл удален')
    emit('updated')
  } catch (e) {
    toast.error((e as any).message || 'Ошибка удаления')
  }
}
</script>

<template>
  <BaseCard
    padding="none"
    hoverable
    clickable
    :to="`/garage/${motorcycle.id}`"
    class="moto-card"
  >
    <div class="moto-card__image-wrap">
      <img
        v-if="photo"
        :src="photo"
        :alt="motorcycle.name"
        class="moto-card__image"
        loading="lazy"
      />
      <div v-else class="moto-card__image-placeholder">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>

      <!-- Бейдж поверх фото -->
      <div v-if="plannedCount > 0" class="moto-card__badge">
        <BaseBadge variant="warning" size="sm">
          {{ plannedCount }} в плане
        </BaseBadge>
      </div>
    </div>

    <!-- Контент снизу -->
    <div class="moto-card__content">
      <h3 class="moto-card__name">{{ motorcycle.name }}</h3>

      <p class="moto-card__details">
        <span v-if="motorcycle.years">{{ motorcycle.years }}</span>
        <span v-if="motorcycle.years && motorcycle.volume" class="moto-card__dot">•</span>
        <span v-if="motorcycle.volume">{{ motorcycle.volume }} см³</span>
      </p>

      <p v-if="motorcycle.license_plate" class="moto-card__plate">
        {{ motorcycle.license_plate }}
      </p>
    </div>

    <!-- Футер -->
    <div class="footer">
      <BaseButton
        size="sm"
        variant="secondary"
        type="button"
        :icon-only="true"
        v-if="motorcycle.mileage"
        @click.stop.prevent="isMileageModalOpen = true"
        title="Обновить пробег"
      >
        <i class="fa-solid fa-gauge-high"></i>
      </BaseButton>

      <BaseButton
        size="sm"
        variant="danger"
        type="button"
        :icon-only="true"
        title="Удалить мотоцикл"
        @click.stop.prevent="isDeleteConfirmOpen = true"
      >
        <i class="fa-solid fa-trash"></i>
      </BaseButton>
    </div>
  </BaseCard>

  <!-- Модалка обновления пробега -->
  <UpdateMileageModal
    v-if="isMileageModalOpen"
    :motorcycle="motorcycle"
    @close="isMileageModalOpen = false"
    @updated="$emit('updated')"
  />

  <!-- Модалка удаления -->
  <BaseConfirm
    v-if="isDeleteConfirmOpen"
    title="Удалить мотоцикл?"
    :message="`Вы уверены, что хотите удалить ${motorcycle.name}? Это действие необратимо.`"
    confirm-text="Удалить"
    :loading="deleting"
    @confirm="onDelete"
    @cancel="isDeleteConfirmOpen = false"
  />
</template>

<style scoped lang="scss">
.moto-card {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: 100%;
}

.moto-card__image-wrap {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  background: var(--color-surface-secondary);
  flex-shrink: 0;
}

.moto-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  inset: 0;
}

.moto-card__image-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-tertiary);
}

.moto-card__badge {
  display: flex;
  position: absolute;
  top: var(--space-3);
  right: var(--space-3);
  z-index: 1;
}

.moto-card__content {
  display: flex;
  flex-direction: column;
  padding: var(--space-4);
  flex: 1;
}

.moto-card__name {
  font-size: var(--text-lg);
  font-weight: var(--fw-bold);
  color: var(--color-text);
  line-height: var(--leading-tight);
  margin-bottom: var(--space-2);

  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.moto-card__details {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  display: flex;
  align-items: center;
  gap: var(--space-1);
  margin-bottom: var(--space-2);
}

.moto-card__dot {
  color: var(--color-text-tertiary);
}

.moto-card__plate {
  margin-top: auto;
  padding-top: var(--space-2);
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  color: var(--color-text-tertiary);
  text-transform: uppercase;
}

.footer {
  margin: 10px;
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}
</style>
