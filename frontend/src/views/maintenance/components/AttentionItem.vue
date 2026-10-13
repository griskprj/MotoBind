<template>
  <article class="att-item" :class="{ 'att-item--overdue': item.isOverdue }">
    <div class="att-item__icon">
      <i :class="item.isOverdue ? 'fa fa-exclamation-triangle' : 'fa fa-clock'" />
    </div>

    <div class="att-item__body">
      <h4 class="att-item__title">{{ item.title }}</h4>
      <p class="att-item__meta">
        <template v-if="item.isOverdue">
          Просрочено на <strong>{{ Math.abs(item.distance) }} км</strong>
        </template>
        <template v-else>
          Через <strong>{{ item.distance }} км</strong>
        </template>
        <span class="att-item__dot">•</span>
        План: {{ item.planned_mileage }} км
      </p>
    </div>

    <div class="att-item__actions">
      <BaseButton
        variant="ghost"
        size="sm"
        icon="fa fa-book"
        title="Открыть мануал"
        @click="emit('open-manual', item)"
      />
      <BaseButton
        variant="ghost"
        size="sm"
        icon="fa fa-check"
        title="Отметить выполненным"
        @click="emit('complete', item)"
      />
      <BaseButton
        variant="ghost"
        size="sm"
        icon="fa fa-user-tie"
        title="Записаться к мастеру"
        @click="emit('find-master')"
      />
      <BaseButton
        variant="primary"
        size="sm"
        @click="emit('open', item)"
      >
        Открыть
      </BaseButton>
    </div>
  </article>
</template>

<script setup>
import { BaseButton } from '@/components/ui'

defineProps({
  item: { type: Object, required: true },
})

const emit = defineEmits(['open', 'complete', 'open-manual', 'find-master'])
</script>

<style scoped>
.att-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-left: 3px solid var(--warning);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.att-item--overdue {
  border-left-color: var(--danger);
  background: var(--danger-trans);
}

.att-item__icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--warning-trans);
  color: var(--warning-text);
  font-size: var(--text-base);
  flex-shrink: 0;
}

.att-item--overdue .att-item__icon {
  background: var(--danger-trans);
  color: var(--danger-text);
}

.att-item__body {
  flex: 1;
  min-width: 0;
}

.att-item__title {
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  margin: 0 0 2px;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.att-item__meta {
  font-size: var(--text-xs);
  color: var(--text-secondary);
  margin: 0;
}

.att-item__meta strong {
  color: var(--text-primary);
}

.att-item__dot {
  opacity: 0.4;
  margin: 0 4px;
}

.att-item__actions {
  display: flex;
  gap: var(--space-1);
  flex-shrink: 0;
}

@media (max-width: 720px) {
  .att-item {
    flex-wrap: wrap;
  }

  .att-item__body {
    flex-basis: calc(100% - 56px);
  }

  .att-item__actions {
    width: 100%;
    justify-content: flex-end;
    padding-top: var(--space-2);
    border-top: 1px solid var(--border-light);
  }
}
</style>
