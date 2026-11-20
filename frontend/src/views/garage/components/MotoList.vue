<template>
  <section class="motorcycles-section">
    <div v-if="motorcycles.length > 0" class="motorcycles-list">
      <MotoListItem
        v-for="moto in motorcycles"
        :key="moto.id"
        :moto="moto"
        :selected="selectedId === moto.id"
        @select="emit('select', $event)"
        @edit="emit('edit', $event)"
        @update-mileage="emit('update-mileage', $event)"
        @photo="emit('photo', $event)"
        @delete="emit('delete', $event)"
      />

      <button class="add-btn btn-secondary" @click="emit('add')">
        <i class="fa fa-plus"></i>
        <span>Добавить мотоцикл</span>
      </button>
    </div>

    <div v-if="motorcycles.length === 0 && !loading" class="empty-state">
      <div class="empty-icon">
        <i class="fa fa-motorcycle"></i>
      </div>
      <h3>Ваш гараж пуст</h3>
      <p>Добавьте свой первый мотоцикл и начните вести учёт обслуживаний</p>
      <button class="btn-primary" @click="emit('add')">
        Добавить мотоцикл
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
import MotoListItem from './MotoListItem.vue'

defineProps<{
  motorcycles: any[]
  selectedId: number | null
  loading: boolean
}>()

const emit = defineEmits<{
  select: [any]
  edit: [any]
  'update-mileage': [any]
  photo: [any]
  delete: [any]
  add: []
}>()
</script>

<style scoped>
.motorcycles-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.add-btn {
  padding: 12px;
  border: 2px dashed var(--border-color);
  border-radius: var(--radius-lg);
  background: transparent;
  color: var(--text-muted);
  font-size: 14px;
  font-weight: var(--fw-medium);
  cursor: pointer;
  transition: all var(--transition-base);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.add-btn:hover {
  border-color: var(--accent);
  color: var(--accent-text);
  background: var(--accent-trans);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 24px;
  background: var(--bg-secondary);
  border: 2px dashed var(--border-color);
  border-radius: var(--radius-xl);
  text-align: center;
  transition: all var(--transition-base);
}

.empty-state:hover {
  border-color: var(--border-color);
}

.empty-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: var(--accent-trans);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  color: var(--accent-text);
  margin-bottom: 20px;
  transition: transform var(--transition-base);
}

.empty-icon i {
  margin-bottom: 0;
}

.empty-state:hover .empty-icon {
  transform: scale(1.05);
}

.empty-state h3 {
  font-size: 22px;
  margin: 0 0 8px;
  color: var(--text-primary);
}

.empty-state p {
  color: var(--text-muted);
  font-size: 14px;
  margin: 0 0 28px;
}

@media (max-width: 640px) {
  .empty-state {
    padding: 40px 16px;
  }

  .empty-icon {
    width: 60px;
    height: 60px;
    font-size: 26px;
  }

  .empty-state h3 {
    font-size: 18px;
  }
}
</style>
