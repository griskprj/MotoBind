<script setup lang="ts">
import type { Motorcycle, MotorcycleComponent } from '~/types'

const props = defineProps<{ motorcycle: Motorcycle }>()
const emit = defineEmits<{ updated: [] }>()

const api = useApi()
const toast = useToast()

const components = ref<MotorcycleComponent[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

const isFormOpen = ref(false)
const editingComponent = ref<MotorcycleComponent | null>(null)
const deletingComponent = ref<MotorcycleComponent | null>(null)
const applyingTemplate = ref(false)

const includeInactive = ref(false)

const activeCount = computed(
  () => components.value.filter((c) => c.is_active).length,
)

async function load() {
  loading.value = true
  error.value = null
  try {
    const res = await api.components.list(props.motorcycle.id, includeInactive.value)
    components.value = res.components
  } catch (e: any) {
    error.value = e?.message || 'Не удалось загрузить компоненты'
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(includeInactive, load)

function openCreate() {
  editingComponent.value = null
  isFormOpen.value = true
}

function openEdit(c: MotorcycleComponent) {
  editingComponent.value = c
  isFormOpen.value = true
}

function onFormDone() {
  isFormOpen.value = false
  editingComponent.value = null
  load()
  emit('updated')
}

async function applyTemplate() {
  applyingTemplate.value = true
  try {
    const res = await api.components.applyTemplate(props.motorcycle.id, {
      style: 'normal',
      terrain: 'mixed',
    })
    if (res.counts.created > 0) {
      toast.success(`Создано компонентов: ${res.counts.created}`)
    } else {
      toast.info('Базовый набор уже создан')
    }
    await load()
    emit('updated')
  } catch (e: any) {
    toast.error(e?.message || 'Не удалось создать базовый набор')
  } finally {
    applyingTemplate.value = false
  }
}

async function removeComponent(c: MotorcycleComponent) {
  deletingComponent.value = null
  try {
    await api.components.remove(props.motorcycle.id, c.id)
    toast.success('Компонент удалён из списка')
    await load()
    emit('updated')
  } catch (e: any) {
    toast.error(e?.message || 'Не удалось удалить компонент')
  }
}

async function reactivate(c: MotorcycleComponent) {
  try {
    await api.components.reactivate(props.motorcycle.id, c.id)
    toast.success('Компонент возвращён')
    await load()
    emit('updated')
  } catch (e: any) {
    toast.error(e?.message || 'Не удалось вернуть компонент')
  }
}
</script>

<template>
  <div class="components-tab">
    <div class="ct-header">
      <div>
        <h2 class="ct-title">Компоненты</h2>
        <p class="ct-subtitle">
          Расходники и узлы мотоцикла. Оценки ресурса ориентировочные.
        </p>
      </div>
      <div class="ct-actions">
        <BaseButton variant="secondary" :loading="applyingTemplate" @click="applyTemplate">
          <template #icon><i class="fa-solid fa-wand-magic-sparkles"></i></template>
          Создать базовый набор
        </BaseButton>
        <BaseButton variant="primary" @click="openCreate">
          <template #icon><i class="fa-solid fa-plus"></i></template>
          Добавить компонент
        </BaseButton>
      </div>
    </div>

    <div class="ct-toolbar">
      <label class="ct-toggle">
        <input v-model="includeInactive" type="checkbox" />
        Показывать удалённые
      </label>
      <span class="ct-count">Активных: {{ activeCount }}</span>
    </div>

    <div v-if="loading" class="ct-skeleton">
      <BaseSkeleton v-for="i in 3" :key="i" height="80px" rounded />
    </div>

    <BaseEmptyState
      v-else-if="error"
      title="Ошибка загрузки"
      :description="error"
    >
      <template #action>
        <BaseButton variant="secondary" @click="load">Повторить</BaseButton>
      </template>
    </BaseEmptyState>

    <BaseEmptyState
      v-else-if="components.length === 0"
      title="Компонентов пока нет"
      description="Создайте базовый набор или добавьте компонент вручную."
    >
      <template #action>
        <BaseButton variant="primary" @click="applyTemplate">
          Создать базовый набор
        </BaseButton>
      </template>
    </BaseEmptyState>

    <div v-else class="ct-list">
      <ComponentCard
        v-for="c in components"
        :key="c.id"
        :component="c"
        :motorcycle-id="motorcycle.id"
        @edit="openEdit(c)"
        @delete="deletingComponent = c"
        @reactivate="reactivate(c)"
        @open-event="(componentId) => $emit('open-event', componentId)"
      />
    </div>

    <BaseModal
      v-if="isFormOpen"
      :title="editingComponent ? 'Редактировать компонент' : 'Новый компонент'"
      @close="isFormOpen = false"
    >
      <ComponentFormModal
        :motorcycle-id="motorcycle.id"
        :component="editingComponent"
        @saved="onFormDone"
        @cancel="isFormOpen = false"
      />
    </BaseModal>

    <BaseModal
      v-if="deletingComponent"
      title="Удалить компонент?"
      @close="deletingComponent = null"
    >
      <p>
        Компонент <strong>{{ deletingComponent.name }}</strong> будет скрыт из списка.
        История работ сохранится, и его можно будет вернуть.
      </p>
      <template #footer>
        <BaseButton variant="ghost" size="sm" @click="deletingComponent = null">
          Отмена
        </BaseButton>
        <BaseButton variant="danger" size="sm" @click="removeComponent(deletingComponent!)">
          Удалить
        </BaseButton>
      </template>
    </BaseModal>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.components-tab {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.ct-header {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-3);
}

.ct-title {
  font-size: var(--text-xl);
  font-weight: var(--fw-bold);
}

.ct-subtitle {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin-top: var(--space-1);
}

.ct-actions {
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.ct-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-2) 0;
  border-bottom: 1px solid var(--color-border);
}

.ct-toggle {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  cursor: pointer;
}

.ct-count {
  font-size: var(--text-sm);
  color: var(--color-text-tertiary);
}

.ct-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.ct-skeleton {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}
</style>
