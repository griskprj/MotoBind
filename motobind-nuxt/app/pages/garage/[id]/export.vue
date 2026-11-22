<script setup lang="ts">
import type { Maintenance, MaintenanceEvent, Motorcycle, MotorcycleComponent } from '~/types'

definePageMeta({ middleware: 'auth' })

const route = useRoute()
const api = useApi()
const motoId = computed(() => String(route.params.id))
const includeCosts = ref(false)
const includeIdentifiers = ref(false)

const { data: report, pending, error } = await useAsyncData(
  `garage-export-${motoId.value}`,
  async () => {
    const [motorcycle, maintenance, firstEvents, componentResponse] = await Promise.all([
      api.motorcycle.get(motoId.value),
      api.maintenance.listByMotorcycle(motoId.value),
      api.maintenance.events.list(motoId.value, { page: 1, per_page: 100 }),
      api.components.list(motoId.value),
    ])

    const events: MaintenanceEvent[] = [...firstEvents.events]
    for (let page = 2; page <= firstEvents.pages; page += 1) {
      const nextPage = await api.maintenance.events.list(motoId.value, { page, per_page: 100 })
      events.push(...nextPage.events)
    }

    return {
      motorcycle: motorcycle as Motorcycle,
      maintenance: maintenance as Maintenance[],
      events,
      components: componentResponse.components as MotorcycleComponent[],
    }
  },
)

const history = computed(() => {
  if (!report.value) return []

  const oldRecords = report.value.maintenance
    .filter((item) => item.status === 'completed')
    .map((item) => ({
      key: `maintenance-${item.id}`,
      date: item.completed_date || '',
      mileage: item.completed_mileage,
      title: item.title,
      category: item.category,
      cost: item.cost || 0,
      works: [] as string[],
    }))

  const eventRecords = report.value.events.map((event) => ({
    key: `event-${event.id}`,
    date: event.date,
    mileage: event.mileage,
    title: 'Обслуживание',
    category: '',
    cost: event.total_cost || event.works.reduce((sum, work) => sum + (work.cost || 0), 0),
    works: event.works.map((work) => work.title || 'Работа без названия'),
  }))

  return [...oldRecords, ...eventRecords].sort((a, b) => b.date.localeCompare(a.date))
})

const planned = computed(() =>
  (report.value?.maintenance || [])
    .filter((item) => item.status === 'planned')
    .sort((a, b) => (a.planned_date || '').localeCompare(b.planned_date || '')),
)

const activeComponents = computed(() =>
  (report.value?.components || []).filter((component) => component.is_active),
)

const generatedOn = new Intl.DateTimeFormat('ru-RU', {
  dateStyle: 'long',
  timeZone: 'Europe/Moscow',
}).format(new Date())

useHead(() => ({
  title: report.value
    ? `История ${report.value.motorcycle.name} — MotoBind`
    : 'История мотоцикла — MotoBind',
}))

useSeoMeta({ robots: 'noindex, nofollow' })

function formatDate(value?: string | null) {
  if (!value) return 'Не указана'
  const [year, month, day] = value.slice(0, 10).split('-')
  return year && month && day ? `${day}.${month}.${year}` : value
}

function formatMileage(value?: number | null) {
  return value == null ? 'Не указан' : `${new Intl.NumberFormat('ru-RU').format(value)} км`
}

function formatCost(value?: number | null) {
  return new Intl.NumberFormat('ru-RU').format(value || 0) + ' ₽'
}

function conditionLabel(value?: string | null) {
  const labels: Record<string, string> = {
    good: 'Хорошее (оценка владельца)',
    ok: 'Удовлетворительное (оценка владельца)',
    bad: 'Требует внимания (оценка владельца)',
    unknown: 'Не оценено',
  }
  return value ? labels[value] || 'Не оценено' : 'Не указано'
}

function driveLabel(value?: string | null) {
  const labels: Record<string, string> = { chain: 'цепь', belt: 'ремень', shaft: 'кардан' }
  return value ? labels[value] || value : null
}

function printReport() {
  window.print()
}
</script>

<template>
  <main class="report-page">
    <div v-if="pending" class="screen-message">Формируем историю мотоцикла…</div>
    <div v-else-if="error || !report" class="screen-message">
      Не удалось загрузить данные мотоцикла. Проверьте доступ и попробуйте ещё раз.
      <NuxtLink :to="`/garage/${motoId}`">Вернуться к мотоциклу</NuxtLink>
    </div>

    <template v-else>
      <div class="report-toolbar no-print">
        <NuxtLink :to="`/garage/${motoId}`" class="back-link">← К мотоциклу</NuxtLink>
        <div class="toolbar-options">
          <label><input v-model="includeCosts" type="checkbox"> Показать стоимость работ</label>
          <label><input v-model="includeIdentifiers" type="checkbox"> Включить VIN и госномер</label>
          <BaseButton variant="primary" size="sm" @click="printReport">
            Сохранить как PDF
          </BaseButton>
        </div>
        <p>Откроется окно печати — выберите «Сохранить как PDF».</p>
      </div>

      <article class="report">
        <header class="report-header">
          <div class="brand">MotoBind <span>ИСТОРИЯ МОТОЦИКЛА</span></div>
          <p class="generated">Сформировано {{ generatedOn }}</p>
        </header>

        <section class="vehicle">
          <h1>{{ report.motorcycle.name }}</h1>
          <div class="vehicle-facts">
            <div v-if="report.motorcycle.years"><span>Год</span><strong>{{ report.motorcycle.years }}</strong></div>
            <div v-if="report.motorcycle.volume"><span>Объём двигателя</span><strong>{{ report.motorcycle.volume }} см³</strong></div>
            <div><span>Текущий пробег</span><strong>{{ formatMileage(report.motorcycle.mileage) }}</strong></div>
            <div v-if="driveLabel(report.motorcycle.drive_type)"><span>Привод</span><strong>{{ driveLabel(report.motorcycle.drive_type) }}</strong></div>
            <div v-if="includeIdentifiers && report.motorcycle.vin"><span>VIN</span><strong>{{ report.motorcycle.vin }}</strong></div>
            <div v-if="includeIdentifiers && report.motorcycle.license_plate"><span>Госномер</span><strong>{{ report.motorcycle.license_plate }}</strong></div>
          </div>
        </section>

        <section class="report-section">
          <h2>История обслуживания</h2>
          <p v-if="!history.length" class="muted">Записей о выполненном обслуживании пока нет.</p>
          <article v-for="item in history" :key="item.key" class="history-item">
            <div class="history-heading">
              <strong>{{ item.title }}</strong>
              <span>{{ formatDate(item.date) }}</span>
            </div>
            <div class="history-meta">
              <span v-if="item.category">{{ item.category }}</span>
              <span>Пробег: {{ formatMileage(item.mileage) }}</span>
              <span v-if="includeCosts">Стоимость: {{ formatCost(item.cost) }}</span>
            </div>
            <ul v-if="item.works.length" class="work-list">
              <li v-for="(work, index) in item.works" :key="index">{{ work }}</li>
            </ul>
          </article>
        </section>

        <section v-if="planned.length" class="report-section">
          <h2>Запланированное обслуживание</h2>
          <article v-for="item in planned" :key="item.id" class="history-item">
            <div class="history-heading">
              <strong>{{ item.title }}</strong>
              <span>{{ item.category }}</span>
            </div>
            <div class="history-meta">
              <span v-if="item.planned_date">Дата: {{ formatDate(item.planned_date) }}</span>
              <span v-if="item.planned_mileage != null">Пробег: {{ formatMileage(item.planned_mileage) }}</span>
            </div>
          </article>
        </section>

        <section v-if="activeComponents.length" class="report-section">
          <h2>Компоненты</h2>
          <article v-for="component in activeComponents" :key="component.id" class="history-item component-item">
            <div class="history-heading">
              <strong>{{ component.name }}</strong>
              <span>{{ conditionLabel(component.condition_rating) }}</span>
            </div>
            <div class="history-meta">
              <span v-if="component.manufacturer">Производитель: {{ component.manufacturer }}</span>
              <span v-if="component.part_number">Артикул: {{ component.part_number }}</span>
              <span v-if="component.last_service_date">Последнее обслуживание: {{ formatDate(component.last_service_date) }}</span>
              <span v-if="component.last_service_mileage != null">На пробеге: {{ formatMileage(component.last_service_mileage) }}</span>
            </div>
          </article>
        </section>

        <footer class="report-disclaimer">
          Сведения внесены владельцем мотоцикла в MotoBind и не проверялись сервисной организацией.
          Оценка состояния компонентов субъективна и отражает мнение владельца на момент заполнения.
        </footer>
      </article>
    </template>
  </main>
</template>

<style scoped lang="scss">
.report-page {
  max-width: 960px;
  margin: 0 auto;
  color: var(--color-text);
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

/* ---------- Тулбар (не печатается) ---------- */
.report-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  flex-wrap: wrap;
  padding: var(--space-3) var(--space-4);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);

  p {
    width: 100%;
    margin: 0;
    color: var(--color-text-tertiary);
    font-size: var(--text-xs);
  }
}

.back-link {
  color: var(--color-brand);
  text-decoration: none;
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);

  &:hover { color: var(--color-brand-hover); }
}

.toolbar-options {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  flex-wrap: wrap;

  label {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    cursor: pointer;
    user-select: none;

    input[type='checkbox'] {
      accent-color: var(--color-brand);
      width: 16px;
      height: 16px;
      cursor: pointer;
    }
  }
}

/* ---------- Сам отчёт ---------- */
.report {
  background: var(--color-surface);
  padding: var(--space-8) var(--space-10);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 2px solid var(--color-brand);
  padding-bottom: var(--space-4);
}

.brand {
  color: var(--color-brand);
  font-size: var(--text-xl);
  font-weight: var(--fw-bold);

  span {
    display: block;
    color: var(--color-text-tertiary);
    font-size: 10px;
    letter-spacing: 0.12em;
    margin-top: var(--space-1);
    font-weight: var(--fw-semibold);
  }
}

.generated {
  color: var(--color-text-tertiary);
  font-size: var(--text-xs);
  margin: 0;
}

.vehicle {
  padding: var(--space-5) 0 var(--space-4);
  border-bottom: 1px solid var(--color-border-light);

  h1 {
    font-size: var(--text-2xl);
    font-weight: var(--fw-bold);
    color: var(--color-text);
    margin: 0 0 var(--space-4);
  }
}

.vehicle-facts {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-3) var(--space-6);

  div {
    display: flex;
    flex-direction: column;
    gap: 3px;
  }

  span {
    color: var(--color-text-tertiary);
    font-size: var(--text-xs);
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }

  strong {
    color: var(--color-text);
    font-size: var(--text-sm);
    font-weight: var(--fw-medium);
    overflow-wrap: anywhere;
  }
}

.report-section {
  margin-top: var(--space-5);

  h2 {
    margin: 0 0 var(--space-3);
    font-size: var(--text-lg);
    font-weight: var(--fw-semibold);
    color: var(--color-text);
  }
}

.muted {
  color: var(--color-text-tertiary);
  font-size: var(--text-sm);
  margin: 0;
}

.history-item {
  padding: var(--space-3) 0;
  border-top: 1px solid var(--color-border-light);
  break-inside: avoid;
}

.history-heading {
  display: flex;
  justify-content: space-between;
  gap: var(--space-4);
  align-items: baseline;

  strong {
    color: var(--color-text);
    font-weight: var(--fw-semibold);
    font-size: var(--text-sm);
  }

  span {
    color: var(--color-text-tertiary);
    font-size: var(--text-xs);
    text-align: right;
    white-space: nowrap;
  }
}

.history-meta {
  display: flex;
  gap: var(--space-1) var(--space-4);
  flex-wrap: wrap;
  margin-top: var(--space-1);
  color: var(--color-text-secondary);
  font-size: var(--text-xs);

  span {
    display: inline-flex;
    align-items: center;
  }
}

.work-list {
  margin: var(--space-2) 0 0;
  padding-left: var(--space-4);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);

  li + li { margin-top: 2px; }
}

.component-item .history-heading span {
  color: var(--color-brand);
  font-weight: var(--fw-medium);
}

.report-disclaimer {
  border-top: 1px solid var(--color-border-light);
  margin-top: var(--space-5);
  padding-top: var(--space-3);
  color: var(--color-text-tertiary);
  font-size: var(--text-xs);
  line-height: var(--leading-relaxed);
}

.screen-message {
  padding: var(--space-8);
  text-align: center;
  color: var(--color-text-secondary);

  a {
    display: inline-block;
    margin-top: var(--space-3);
    color: var(--color-brand);
    text-decoration: none;
    font-weight: var(--fw-medium);

    &:hover { text-decoration: underline; }
  }
}

/* ---------- Печать ---------- */
@media print {
  :global(body),
  :global(.dashboard-layout),
  :global(.layout-body),
  :global(.layout-main),
  :global(.main-content),
  :global(.default-layout) {
    background: #fff !important;
  }

  :global(body) { margin: 0 !important; }

  :global(.app-header),
  :global(.app-sidebar),
  :global(.desktop-sidebar),
  :global(.public-header),
  :global(.app-footer),
  .no-print {
    display: none !important;
  }

  :global(.layout-body),
  :global(.dashboard-content) {
    display: block !important;
    min-height: 0 !important;
  }

  :global(.layout-main),
  :global(.main-content) {
    padding: 0 !important;
    max-width: none !important;
  }

  .report-page {
    max-width: none;
    margin: 0;
  }

  .report {
    padding: 12mm 14mm;
    border: 0;
    border-radius: 0;
    box-shadow: none;
  }

  .report-section,
  .vehicle,
  .history-item {
    break-inside: avoid;
  }

  @page { size: A4; margin: 10mm; }
}
</style>