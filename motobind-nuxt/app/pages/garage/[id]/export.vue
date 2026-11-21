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
          <button type="button" class="print-button" @click="printReport">Сохранить как PDF</button>
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
.report-page { max-width: 960px; margin: 0 auto; color: #20242a; }
.report-toolbar { display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap; margin: 0 0 20px; }
.report-toolbar p { width: 100%; margin: 0; color: #667085; font-size: 13px; }
.toolbar-options { display: flex; align-items: center; gap: 14px; flex-wrap: wrap; }
.toolbar-options label { display: flex; align-items: center; gap: 6px; font-size: 13px; }
.back-link { color: #4855a6; text-decoration: none; }
.print-button { border: 0; border-radius: 8px; padding: 10px 16px; color: #fff; background: #4654aa; font: inherit; font-weight: 600; cursor: pointer; }
.report { background: #fff; padding: 40px 48px; border: 1px solid #e5e7eb; border-radius: 12px; box-shadow: 0 8px 28px #10182812; }
.report-header { display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #4654aa; padding-bottom: 16px; }
.brand { color: #4654aa; font-size: 22px; font-weight: 800; }
.brand span { display: block; color: #667085; font-size: 10px; letter-spacing: .12em; margin-top: 4px; }
.generated { color: #667085; font-size: 12px; margin: 0; }
.vehicle { padding: 20px 0 16px; border-bottom: 1px solid #e5e7eb; }
.vehicle h1 { font-size: 28px; margin: 0 0 16px; }
.vehicle-facts { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px 24px; }
.vehicle-facts div { display: flex; flex-direction: column; gap: 3px; }
.vehicle-facts span, .history-meta, .muted { color: #667085; font-size: 12px; }
.vehicle-facts strong { overflow-wrap: anywhere; }
.report-section { margin-top: 22px; }
.report-section h2 { margin: 0 0 10px; font-size: 17px; }
.history-item { padding: 11px 0; border-top: 1px solid #eaecf0; break-inside: avoid; }
.history-heading { display: flex; justify-content: space-between; gap: 16px; }
.history-heading span { color: #667085; text-align: right; }
.history-meta { display: flex; gap: 5px 16px; flex-wrap: wrap; margin-top: 5px; }
.work-list { margin: 8px 0 0; padding-left: 20px; font-size: 13px; }
.report-disclaimer { border-top: 1px solid #eaecf0; margin-top: 24px; padding-top: 12px; color: #667085; font-size: 11px; line-height: 1.5; }
.screen-message { padding: 32px; }
@media print {
  :global(body), :global(.dashboard-layout), :global(.dashboard-content), :global(.main-content) { background: #fff !important; }
  :global(body) { margin: 0 !important; }
  :global(.app-header), :global(.app-sidebar), .no-print { display: none !important; }
  :global(.dashboard-content) { display: block !important; min-height: 0 !important; }
  :global(.main-content) { padding: 0 !important; }
  .report-page { max-width: none; margin: 0; }
  .report { padding: 12mm 14mm; border: 0; border-radius: 0; box-shadow: none; }
  .report-section, .vehicle { break-inside: avoid; }
  .history-item { break-inside: avoid; }
  @page { size: A4; margin: 10mm; }
}
</style>
