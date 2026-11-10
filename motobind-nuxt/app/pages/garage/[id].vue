<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const route = useRoute()
const router = useRouter()
const api = useApi()
const mediaUrl = useMediaUrl()
const isEditModalOpen = ref(false)

const id = computed(() => route.params.id as string)

const { data: motorcycle, pending, error, refresh } = await useAsyncData(
  `moto-${id.value}`,
  () => api.motorcycle.get(id.value)
)

useSeoMeta({
  title: () => motorcycle.value ? `${motorcycle.value.name} — Гараж` : 'Мотоцикл — Гараж',
  robots: 'noindex',
})

const activeTab = ref('overview')
const tabs = [
  { id: 'overview', label: 'Обзор' },
  { id: 'components', label: 'Компоненты' },
  { id: 'maintenance', label: 'Обслуживание' },
  { id: 'history', label: 'История' },
  { id: 'diagnostics', label: 'Диагностика' },
  { id: 'notes', label: 'Заметки' },
]

async function onUpdated() {
  await refresh()
}

const heroBackground = computed(() => {
  if (!motorcycle.value?.photo_url) return 'none'
  const url = mediaUrl(motorcycle.value.photo_url)
  return url ? `url(${url})` : 'none'
})

const pendingComponentId = ref<number | null>(null)
function onOpenComponentEvent(componentId: number) {
  pendingComponentId.value = componentId
  activeTab.value = 'maintenance'
}
</script>

<template>
  <div class="moto-page">
    <!-- Загрузка -->
    <div v-if="pending" class="moto-skeleton">
      <BaseSkeleton height="300px" rounded class="mb-4" />
      <div class="grid-2">
        <BaseSkeleton height="200px" rounded />
        <BaseSkeleton height="200px" rounded />
      </div>
    </div>

    <!-- Ошибка -->
    <BaseEmptyState
      v-else-if="error || !motorcycle"
      title="Мотоцикл не найден"
      description="Возможно, он был удалён или у вас нет доступа."
    >
      <template #action>
        <BaseButton to="/garage" variant="primary">Вернуться в гараж</BaseButton>
      </template>
    </BaseEmptyState>

    <!-- Контент -->
    <template v-else>
      <!-- Шапка-баннер с фото -->
      <div class="hero-header" :style="{ backgroundImage: heroBackground }">
        <div class="hero-overlay">
          <NuxtLink to="/garage" class="back-link light">
            <i class="fa-solid fa-arrow-left"></i>
            Назад в гараж
          </NuxtLink>

          <div class="hero-content">
            <div>
              <h1 class="hero-title">{{ motorcycle.name }}</h1>
              <p class="hero-meta">
                <span v-if="motorcycle.years">{{ motorcycle.years }}</span>
                <span v-if="motorcycle.years && motorcycle.volume" class="dot">•</span>
                <span v-if="motorcycle.volume">{{ motorcycle.volume }} см³</span>
                <span v-if="motorcycle.license_plate" class="dot">•</span>
                <span v-if="motorcycle.license_plate" class="plate">{{ motorcycle.license_plate }}</span>
              </p>
            </div>
            <div class="hero-actions">
              <BaseButton variant="secondary" size="sm" @click="isEditModalOpen = true">
                <i class="fa-solid fa-pen"></i> Редактировать
              </BaseButton>
            </div>
          </div>
        </div>
      </div>

      <!-- Вкладки -->
      <div class="tabs">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          class="tab"
          :class="{ 'tab--active': activeTab === tab.id }"
          @click="activeTab = tab.id"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- Контент вкладок -->
      <div class="tab-content">
        <!-- Обзор -->
        <MotorcycleOverview
          v-if="activeTab === 'overview'"
          :motorcycle="motorcycle"
          @updated="onUpdated"
          @open-components="activeTab = 'components'"
        />

        <!-- Компоненты -->
        <MotorcycleComponentsTab
          v-else-if="activeTab === 'components'"
          :motorcycle="motorcycle"
          @updated="onUpdated"
          @open-event="activeTab = 'maintenance'"
        />

        <!-- Обслуживание -->
        <MotorcycleMaintenanceTab
          v-else-if="activeTab === 'maintenance'"
          :motorcycle="motorcycle"
          :initial-component-id="pendingComponentId"
          @updated="onUpdated"
          @event-saved="pendingComponentId = null"
        />

        <!-- История -->
        <MaintenanceSection
          v-else-if="activeTab === 'history'"
          :motorcycle="motorcycle"
          @updated="onUpdated"
        />

        <!-- Диагностика -->
        <MotorcycleDiagnosticsTab
          v-else-if="activeTab === 'diagnostics'"
          :motorcycle="motorcycle"
        />

        <!-- В шаблоне -->
        <MotorcycleNotesTab
          v-if="activeTab === 'notes'"
          :motorcycle="motorcycle"
          @updated="onUpdated"
        />

        <!-- Редактирование модалка -->
        <EditMotorcycleModal
          v-if="isEditModalOpen"
          :motorcycle="motorcycle"
          @close="isEditModalOpen = false"
          @updated="onUpdated"
        />
      </div>
    </template>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.moto-page {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

/* ============================================================
   Шапка-баннер
   ============================================================ */
.hero-header {
  position: relative;
  width: 100%;
  background-size: cover;
  background-position: center;
  border-radius: var(--radius-lg);
  overflow: hidden;
  display: flex;
  align-items: flex-end;
  background-color: var(--color-surface-secondary);
  background-image: linear-gradient(to top, rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.2));
}

.hero-overlay {
  padding: var(--space-6);
  width: 100%;
  color: #fff;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.back-link.light {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  width: fit-content;
  margin-bottom: var(--space-2);
  transition: color var(--transition-fast);

  &:hover { color: #fff; }
}

.hero-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: var(--space-4);
  flex-wrap: wrap;
}

.hero-title {
  font-size: var(--text-3xl);
  font-weight: var(--fw-bold);
  line-height: var(--leading-tight);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.hero-meta {
  font-size: var(--text-base);
  opacity: 0.9;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
  margin-top: var(--space-1);
}

.hero-meta .dot {
  margin: 0 var(--space-1);
  opacity: 0.6;
}

.hero-meta .plate {
  font-family: var(--font-mono);
  text-transform: uppercase;
}

.hero-actions {
  display: flex;
  gap: var(--space-2);
}

/* ============================================================
   Вкладки
   ============================================================ */
.tabs {
  display: flex;
  gap: var(--space-2);
  border-bottom: 1px solid var(--color-border);
  overflow-x: auto;
  overflow-y: hidden;
  scrollbar-width: none;
  -ms-overflow-style: none;

  &::-webkit-scrollbar { display: none; }
}

.tab {
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-base);
  font-weight: var(--fw-medium);
  color: var(--color-text-secondary);
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  white-space: nowrap;
  background: none;
  border: none;
  cursor: pointer;
  transition: all var(--transition-fast);

  &:hover { color: var(--color-text); }
  &--active {
    color: var(--color-brand);
    border-bottom-color: var(--color-brand);
  }
}

.tab-content {
  padding-top: var(--space-4);
}

/* ============================================================
   Загрузка и сетка
   ============================================================ */
.mb-4 { margin-bottom: var(--space-4); }

.grid-2 {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);
  @include md-up { grid-template-columns: 1fr 1fr; }
}

/* Адаптив для шапки */
@include md-down {
  .hero-header { min-height: 200px; }
  .hero-overlay { padding: var(--space-4); }
  .hero-title { font-size: var(--text-2xl); }
  .hero-content { flex-direction: column; align-items: flex-start; }
}
</style>
