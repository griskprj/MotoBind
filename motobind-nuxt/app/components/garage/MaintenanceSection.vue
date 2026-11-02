<script setup lang="ts">
import type { Motorcycle, Maintenance, ApiError } from '~/types'

const props = defineProps<{ motorcycle: Motorcycle }>()
const emit = defineEmits<{ updated: [] }>()

const api = useApi()
const toast = useToast()

const activeTab = ref<'planned' | 'history'>('planned')
const isFormOpen = ref(false)
const editingMaintenance = ref<Maintenance | null>(null)
const selectedMaintenance = ref<Maintenance | null>(null)
const completingMaintenance = ref<Maintenance | null>(null)
const deletingMaintenance = ref<Maintenance | null>(null)

// Разделяем на планы и историю
const planned = computed(() =>
  (props.motorcycle.maintenances || [])
    .filter(m => m.status === 'planned')
    .sort((a, b) => {
      if (a.planned_date && b.planned_date) return a.planned_date.localeCompare(b.planned_date)
      return 0
    })
)

const history = computed(() =>
  (props.motorcycle.maintenances || [])
    .filter(m => m.status === 'completed')
    .sort((a, b) => {
      if (a.completed_date && b.completed_date) return b.completed_date.localeCompare(a.completed_date)
      return b.id - a.id
    })
)

// Обработчики
function openCreate() {
  editingMaintenance.value = null
  isFormOpen.value = true
}

function openEdit(m: Maintenance) {
  selectedMaintenance.value = null
  editingMaintenance.value = m
  isFormOpen.value = true
}

function openDetails(m: Maintenance) {
  selectedMaintenance.value = m
}

function openComplete(m: Maintenance) {
  selectedMaintenance.value = null
  completingMaintenance.value = m
}

function openDelete(m: Maintenance) {
  selectedMaintenance.value = null
  deletingMaintenance.value = m
}

function onFormDone() {
  isFormOpen.value = false
  editingMaintenance.value = null
  emit('updated')
}

function onCompleted() {
  completingMaintenance.value = null
  emit('updated')
}

function onDeleteDone() {
  deletingMaintenance.value = null
  emit('updated')
}
</script>

<template>
  <div class="m-section stack" style="--stack-gap: var(--space-5)">
    <!-- Заголовок и кнопка -->
    <div class="m-header">
      <h2 class="m-title">Обслуживание</h2>
      <BaseButton v-if="!isFormOpen" variant="primary" size="sm" @click="openCreate">
        <template #icon>
          <i class="fa-solid fa-plus"></i>
        </template>
        Добавить
      </BaseButton>
    </div>

    <MaintenanceStats :maintenances="motorcycle.maintenances || []" />

    <!-- Форма добавления/редактирования (встроенная или в модалке - решай сам) -->
    <BaseModal
      v-if="isFormOpen"
      :title="editingMaintenance ? 'Редактировать запись' : 'Новая запись'"
      @close="isFormOpen = false"
    >
      <MaintenanceForm
        :motorcycles="[motorcycle]"
        :default-motorcycle-id="motorcycle.id"
        :initial-data="editingMaintenance"
        @created="onFormDone"
        @updated="onFormDone"
        @cancel="isFormOpen = false"
      />
    </BaseModal>

    <!-- Модалка деталей -->
    <MaintenanceDetailsModal
      v-if="selectedMaintenance"
      :maintenance="{ ...selectedMaintenance, motorcycle: motorcycle }"
      @close="selectedMaintenance = null"
      @updated="emit('updated'); selectedMaintenance = null"
      @edit="openEdit(selectedMaintenance!)"
      @complete="openComplete(selectedMaintenance!)"
      @delete="openDelete(selectedMaintenance!)"
    />

    <!-- Модалка завершения -->
    <CompleteMaintenanceModal
      v-if="completingMaintenance"
      :maintenance="completingMaintenance"
      @close="completingMaintenance = null"
      @completed="onCompleted"
    />

    <!-- Модалка удаления -->
    <DeleteMaintenanceModal
      v-if="deletingMaintenance"
      :maintenance="deletingMaintenance"
      @close="deletingMaintenance = null"
      @deleted="onDeleteDone"
    />

    <!-- Табы -->
    <div v-if="!isFormOpen" class="m-tabs">
      <button
        class="m-tab-btn"
        :class="{ 'm-tab-btn--active': activeTab === 'planned' }"
        @click="activeTab = 'planned'"
      >
        Планы
        <span v-if="planned.length" class="badge">{{ planned.length }}</span>
      </button>
      <button
        class="m-tab-btn"
        :class="{ 'm-tab-btn--active': activeTab === 'history' }"
        @click="activeTab = 'history'"
      >
        История
        <span v-if="history.length" class="badge">{{ history.length }}</span>
      </button>
    </div>

    <!-- Контент табов -->
    <div v-if="!isFormOpen" class="m-content">
      <!-- Планы -->
      <template v-if="activeTab === 'planned'">
        <div v-if="planned.length === 0" class="m-empty">
          <p>Нет запланированных работ.</p>
        </div>
        <div v-else class="m-list">
          <MaintenanceItem
            v-for="m in planned"
            :key="m.id"
            :maintenance="m"
            @click="openDetails(m)"
            @complete="openComplete(m)"
            @delete="openDelete(m)"
          />
        </div>
      </template>

      <!-- История -->
      <template v-else>
        <div v-if="history.length === 0" class="m-empty">
          <p>История обслуживания пуста.</p>
        </div>
        <div v-else class="m-list">
          <MaintenanceItem
            v-for="m in history"
            :key="m.id"
            :maintenance="m"
            @click="openDetails(m)"
            @delete="openDelete(m)"
          />
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped lang="scss">
.m-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.m-title {
  font-size: var(--text-xl);
  font-weight: var(--fw-bold);
  color: var(--color-text);
}

.m-tabs {
  display: flex;
  border-bottom: 1px solid var(--color-border);
  gap: var(--space-4);
}

.m-tab-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) 0;
  font-size: var(--text-base);
  font-weight: var(--fw-medium);
  color: var(--color-text-secondary);
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  transition: all var(--transition-fast);

  &--active {
    color: var(--color-brand);
    border-bottom-color: var(--color-brand);
  }
}

.badge {
  background: var(--color-surface-secondary);
  padding: 2px 8px;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
}

.m-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.m-empty {
  padding: var(--space-6);
  text-align: center;
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  background: var(--color-surface-secondary);
  border-radius: var(--radius-md);
}
</style>
