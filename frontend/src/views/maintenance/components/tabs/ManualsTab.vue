<template>
  <div class="manuals-tab">
    <div v-if="!motorcycle" class="manuals-tab__empty">
      <i class="fa fa-motorcycle" />
      <p>Выберите мотоцикл, чтобы увидеть подходящие мануалы</p>
    </div>

    <template v-else>
      <div class="manuals-tab__head">
        <h3>Мануалы для {{ motorcycle.name }}</h3>
        <BaseButton
          variant="outline"
          icon="fa fa-plus"
          @click="emit('create-manual')"
        >
          Создать мануал
        </BaseButton>
      </div>

      <div v-if="loading" class="manuals-tab__loading">
        <div class="spinner" />
      </div>

      <div v-else-if="manuals.length === 0" class="manuals-tab__empty">
        <i class="fa fa-book" />
        <p>Мануалов для этой модели пока нет</p>
        <BaseButton variant="primary" @click="emit('create-manual')">
          Создать первый
        </BaseButton>
      </div>

      <div v-else class="manuals-tab__grid">
        <ManualCard
          v-for="m in manuals"
          :key="m.id"
          :manual="m"
        />
      </div>
    </template>
  </div>
</template>

<script setup>
import { BaseButton } from '@/components/ui'
import ManualCard from '@/components/manual/ManualCard.vue'

defineProps({
  motorcycle: { type: Object, default: null },
  manuals: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
})

const emit = defineEmits(['create-manual'])
</script>

<style scoped>
.manuals-tab {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.manuals-tab__head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.manuals-tab__head h3 {
  margin: 0;
  font-size: var(--text-base);
}

.manuals-tab__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: var(--space-3);
}

.manuals-tab__empty,
.manuals-tab__loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-8);
  color: var(--text-muted);
  text-align: center;
}

.manuals-tab__empty i {
  font-size: var(--text-3xl);
  opacity: 0.4;
}

.manuals-tab__empty p {
  margin: 0;
  font-size: var(--text-sm);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--border-color);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
