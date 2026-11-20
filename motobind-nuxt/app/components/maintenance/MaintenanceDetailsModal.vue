<script setup lang="ts">
import type { Maintenance, Motorcycle, ApiError } from '~/types'

const props = defineProps<{
  maintenance: Maintenance & { motorcycle: Motorcycle }
}>()

const emit = defineEmits<{
  close: []
  updated: []
  edit: []
  complete: []
  delete: []
}>()

const api = useApi()
const toast = useToast()

const deleting = ref(false)
const completing = ref(false)

const formatDate = (isoStr?: string | null) => {
  if (!isoStr) return '—'
  return new Date(isoStr).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })
}

const formatMileage = (val?: number | null) => {
  if (!val) return '—'
  return new Intl.NumberFormat('ru-RU').format(val) + ' км'
}

const formatCost = (val?: number | null) => {
  if (!val) return '—'
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', maximumFractionDigits: 0 }).format(val)
}
</script>

<template>
  <BaseModal :title="maintenance.title" @close="emit('close')">
    <div class="details-grid">
      <div class="detail-item span-2">
        <span class="detail-label">Мотоцикл</span>
        <NuxtLink :to="`/garage/${maintenance.motorcycle.id}`" class="moto-link">
          {{ maintenance.motorcycle.name }}
        </NuxtLink>
      </div>

      <div class="detail-item">
        <span class="detail-label">Статус</span>
        <BaseBadge :variant="maintenance.status === 'planned' ? 'warning' : 'success'">
          {{ maintenance.status === 'planned' ? 'В плане' : 'Выполнено' }}
        </BaseBadge>
      </div>

      <div class="detail-item">
        <span class="detail-label">Категория</span>
        <MaintenanceCategoryBadge :category="maintenance.category" />
      </div>

      <!-- Данные для Плана -->
      <template v-if="maintenance.status === 'planned'">
        <div class="detail-item">
          <span class="detail-label">Дата (план)</span>
          <span class="detail-value"><i class="fa-regular fa-calendar"></i> {{ formatDate(maintenance.planned_date) }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Пробег (план)</span>
          <span class="detail-value"><i class="fa-solid fa-gauge-high"></i> {{ formatMileage(maintenance.planned_mileage) }}</span>
        </div>
      </template>

      <!-- Данные для Выполнено -->
      <template v-else>
        <div class="detail-item">
          <span class="detail-label">Дата выполнения</span>
          <span class="detail-value"><i class="fa-regular fa-calendar-check"></i> {{ formatDate(maintenance.completed_date) }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Пробег</span>
          <span class="detail-value"><i class="fa-solid fa-gauge-high"></i> {{ formatMileage(maintenance.completed_mileage) }}</span>
        </div>
        <div class="detail-item span-2">
          <span class="detail-label">Стоимость</span>
          <span class="detail-value cost-value">{{ formatCost(maintenance.cost) }}</span>
        </div>
      </template>

      <div v-if="maintenance.description" class="detail-item span-2">
        <span class="detail-label">Описание</span>
        <p class="detail-desc">{{ maintenance.description }}</p>
      </div>
    </div>

    <template #footer>
      <div class="footer-actions">
        <div class="footer-row footer-row--left">
          <BaseButton variant="danger" size="sm" @click="emit('delete')">
            <template #icon><i class="fa-solid fa-trash"></i></template>
            Удалить
          </BaseButton>
          <BaseButton variant="secondary" size="sm" @click="emit('edit')">
            <template #icon><i class="fa-solid fa-pen"></i></template>
            Редактировать
          </BaseButton>
        </div>

        <div class="footer-row footer-row--right">
          <BaseButton
            v-if="maintenance.status === 'planned'"
            variant="primary"
            size="sm"
            @click="emit('complete')"
          >
            <template #icon><i class="fa-solid fa-check"></i></template>
            Выполнено
          </BaseButton>
        </div>
      </div>
    </template>
  </BaseModal>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.details-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);

  @include sm-up {
    grid-template-columns: 1fr 1fr;
  }
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.span-2 {
  @include sm-up { grid-column: span 2; }
}

.detail-label {
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-tertiary);
  font-weight: var(--fw-medium);
}

.detail-value {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-base);
  font-weight: var(--fw-medium);
  color: var(--color-text);

  i {
    color: var(--color-text-secondary);
    width: 16px;
    text-align: center;
  }
}

.cost-value {
  font-size: var(--text-lg);
  font-weight: var(--fw-bold);
  color: var(--color-success);
}

.detail-desc {
  font-size: var(--text-sm);
  line-height: var(--leading-relaxed);
  color: var(--color-text-secondary);
  background: var(--color-surface-secondary);
  padding: var(--space-3);
  border-radius: var(--radius-md);
  margin-top: var(--space-1);
  white-space: pre-wrap;
}

.moto-link {
  font-size: var(--text-base);
  font-weight: var(--fw-semibold);
  color: var(--color-brand);
  text-decoration: none;

  &:hover { text-decoration: underline; }
}

:deep(.modal-footer) {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.footer-actions {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  width: 100%;

  @include sm-up {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
}

.footer-row {
  display: flex;
  gap: var(--space-2);
  width: 100%;

  @include sm-up {
    width: auto;
  }

  @media (max-width: 639px) {
    > button {
      flex: 1;
    }
  }
}
</style>
