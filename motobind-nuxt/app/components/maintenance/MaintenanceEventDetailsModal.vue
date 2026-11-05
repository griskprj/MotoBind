<script setup lang="ts">
import type { MaintenanceEvent } from '~/types'

const props = defineProps<{
  event: MaintenanceEvent
}>()

const emit = defineEmits<{
  close: []
  edit: []
  delete: []
}>()

const kindLabels: Record<string, string> = {
  replace: 'Замена',
  inspect: 'Осмотр',
  adjust: 'Регулировка',
  repair: 'Ремонт',
  other: 'Другое',
}

function formatDate(iso: string) {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
}

const total = computed(() => props.event.total_cost || props.event.works.reduce((s, w) => s + (w.cost || 0), 0))
</script>

<template>
  <BaseModal title="Детали события" @close="emit('close')">
    <div class="event-details">
      <!-- Шапка -->
      <div class="ed-header">
        <div class="ed-date">
          <i class="fa-solid fa-calendar-day"></i>
          {{ formatDate(event.date) }}
        </div>
        <div v-if="event.mileage" class="ed-mileage">
          <i class="fa-solid fa-gauge-high"></i>
          {{ event.mileage.toLocaleString('ru-RU') }} км
        </div>
      </div>

      <!-- Комментарий -->
      <div v-if="event.comment" class="ed-comment">
        <i class="fa-solid fa-quote-left"></i>
        {{ event.comment }}
      </div>

      <!-- Работы -->
      <div class="ed-works">
        <h3 class="ed-works-title">Выполненные работы</h3>
        <ul class="ed-list">
          <li v-for="w in event.works" :key="w.id" class="ed-item">
            <div class="ed-item-icon">
              <i class="fa-solid fa-wrench"></i>
            </div>
            <div class="ed-item-content">
              <div class="ed-item-title">
                {{ w.title || 'Работа без названия' }}
                <BaseBadge variant="neutral" size="sm">
                  {{ kindLabels[w.kind] || w.kind }}
                </BaseBadge>
              </div>
              <div v-if="w.note" class="ed-item-note">{{ w.note }}</div>
            </div>
            <div v-if="w.cost" class="ed-item-cost">
              {{ w.cost.toLocaleString('ru-RU') }} ₽
            </div>
          </li>
        </ul>
      </div>

      <!-- Итог -->
      <div class="ed-total">
        <span>Итого:</span>
        <strong>{{ total.toLocaleString('ru-RU') }} ₽</strong>
      </div>
    </div>

    <template #footer>
      <div class="ed-footer">
        <BaseButton variant="danger" size="sm" @click="emit('delete')">
          <i class="fa-solid fa-trash"></i> Удалить
        </BaseButton>
        <div class="ed-footer-right">
          <BaseButton variant="ghost" size="sm" @click="emit('close')">Закрыть</BaseButton>
          <BaseButton variant="primary" size="sm" @click="emit('edit')">
            <i class="fa-solid fa-pen"></i> Редактировать
          </BaseButton>
        </div>
      </div>
    </template>
  </BaseModal>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.event-details {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.ed-header {
  display: flex;
  gap: var(--space-4);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);

  i {
    color: var(--color-brand);
    margin-right: var(--space-1);
  }
}

.ed-comment {
  padding: var(--space-3);
  background: var(--color-surface-secondary);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  color: var(--color-text);
  border-left: 3px solid var(--color-brand);

  i {
    color: var(--color-brand);
    opacity: 0.5;
    margin-right: var(--space-2);
  }
}

.ed-works-title {
  font-size: var(--text-base);
  font-weight: var(--fw-semibold);
  margin-bottom: var(--space-2);
}

.ed-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.ed-item {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--color-surface);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
}

.ed-item-icon {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
  background: var(--color-brand-soft, rgba(112, 0, 255, 0.1));
  color: var(--color-brand);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.ed-item-content {
  flex: 1;
  min-width: 0;
}

.ed-item-title {
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  display: flex;
  align-items: center;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.ed-item-note {
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
  margin-top: var(--space-1);
}

.ed-item-cost {
  font-weight: var(--fw-semibold);
  font-size: var(--text-sm);
  white-space: nowrap;
}

.ed-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: var(--space-3);
  border-top: 1px solid var(--color-border);
  font-size: var(--text-lg);
}

.ed-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.ed-footer-right {
  display: flex;
  gap: var(--space-2);
}
</style>
