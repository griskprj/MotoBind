<template>
  <div class="plans">
    <div class="plans__head">
      <h3>Запланированные ТО</h3>
      <BaseButton variant="primary" icon="fa fa-plus" @click="emit('add')">
        Добавить план
      </BaseButton>
    </div>

    <div v-if="plans.length === 0" class="plans__empty">
      <i class="fa fa-calendar-check" />
      <p>Нет запланированных обслуживаний</p>
      <BaseButton variant="outline" icon="fa fa-plus" @click="emit('add')">
        Добавить первое
      </BaseButton>
    </div>

    <div v-else class="plans__list">
      <MaintenanceRow
        v-for="m in plans"
        :key="m.id"
        :item="m"
        @click="emit('open', m)"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { BaseButton } from '@/components/ui'
import MaintenanceRow from '../MaintenanceRow.vue'

const props = defineProps({
  allMaintenances: { type: Array, default: () => [] },
})

const emit = defineEmits(['open', 'add'])

const plans = computed(() =>
  props.allMaintenances.filter((m) => m.status === 'planned' || m.status === 'overdue')
)
</script>

<style scoped>
.plans {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.plans__head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.plans__head h3 {
  margin: 0;
  font-size: var(--text-base);
}

.plans__list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.plans__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-8);
  color: var(--text-muted);
}

.plans__empty i {
  font-size: var(--text-3xl);
  opacity: 0.4;
}

.plans__empty p {
  margin: 0;
  font-size: var(--text-sm);
}
</style>
