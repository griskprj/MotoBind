<script setup lang="ts">
import type { Motorcycle } from '~/types'

const props = defineProps<{
  motorcycle: Motorcycle
}>()

const emit = defineEmits<{ updated: [] }>()

const isModalOpen = ref(false)

function formatMileage(val?: number | null) {
  if (!val) return '0'
  return new Intl.NumberFormat('ru-RU').format(val)
}

function onUpdated() {
  isModalOpen.value = false
  emit('updated')
}
</script>

<template>
  <BaseCard padding="lg" class="mileage-card">
    <div class="mileage-header">
      <h2 class="section-title">
        <i class="fa-solid fa-gauge-high"></i> Пробег
      </h2>
      <BaseButton variant="ghost" size="sm" @click="isModalOpen = true">
        <template #icon><i class="fa-solid fa-pen"></i></template>
        Обновить
      </BaseButton>
    </div>

    <div class="mileage-value">
      {{ formatMileage(motorcycle.mileage) }} <span class="unit">км</span>
    </div>

    <UpdateMileageModal
      v-if="isModalOpen"
      :motorcycle="motorcycle"
      @close="isModalOpen = false"
      @updated="onUpdated"
    />
  </BaseCard>
</template>

<style scoped lang="scss">
.mileage-card {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.mileage-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.section-title {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-lg);
  font-weight: var(--fw-semibold);
  color: var(--color-text);

  i {
    color: var(--color-brand);
  }
}

.mileage-value {
  font-size: var(--text-3xl);
  font-weight: var(--fw-bold);
  color: var(--color-text);
  line-height: 1.1;

  .unit {
    font-size: var(--text-lg);
    font-weight: var(--fw-medium);
    color: var(--color-text-tertiary);
    margin-left: var(--space-1);
  }
}
</style>
