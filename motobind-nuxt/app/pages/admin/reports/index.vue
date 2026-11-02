<script setup lang="ts">
import type { AdminReport, AdminReportsResponse } from '~/types'

definePageMeta({ middleware: ['auth', 'admin'] })

useSeoMeta({ title: 'Жалобы — Админка', robots: 'noindex' })

const api = useApi()
const toast = useToast()

const reports = ref<AdminReport[]>([])
const stats = ref<AdminReportsResponse['stats'] | null>(null)
const pending = ref(false)
const statusFilter = ref('pending')
const page = ref(1)
const totalPages = ref(1)

async function loadReports() {
  pending.value = true
  try {
    const res = await api.admin.getReports({
      page: page.value,
      per_page: 10,
      status: statusFilter.value || undefined,
    })
    reports.value = res.reports
    stats.value = res.stats
    totalPages.value = res.pages
  } catch (e) {
    toast.error('Не удалось загрузить жалобы')
  } finally {
    pending.value = false
  }
}

onMounted(loadReports)
watch([statusFilter, page], loadReports)

// Модалка рассмотрения
const resolvingReport = ref<AdminReport | null>(null)
const resolutionAction = ref<'post_deleted' | 'user_banned' | 'both' | 'none'>('none')
const resolutionNote = ref('')
const isResolving = ref(false)

function openResolve(report: AdminReport) {
  resolvingReport.value = report
  resolutionAction.value = 'none'
  resolutionNote.value = ''
}

async function submitResolve() {
  if (!resolvingReport.value) return

  isResolving.value = true
  try {
    await api.admin.resolveReport(
      resolvingReport.value.id,
      resolutionAction.value,
      resolutionNote.value.trim() || undefined
    )
    toast.success('Жалоба рассмотрена')
    resolvingReport.value = null
    await loadReports()
  } catch (e) {
    toast.error('Ошибка рассмотрения жалобы')
  } finally {
    isResolving.value = false
  }
}

// Форматирование даты
const formatDate = (iso?: string | null) => {
  if (!iso) return '—'
  return new Date(iso).toLocaleString('ru-RU', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })
}

// Категории жалоб (для отображения)
const categoryLabels: Record<string, string> = {
  spam: 'Спам',
  abuse: 'Оскорбления',
  inappropriate: 'Неприемлемый контент',
  fraud: 'Мошенничество',
  other: 'Другое',
}

// Бейджи статусов
const statusConfig = {
  pending: { label: 'На рассмотрении', class: 'badge--warning' },
  resolved: { label: 'Решена', class: 'badge--success' },
  rejected: { label: 'Отклонена', class: 'badge--danger' },
}
</script>

<template>
  <div class="admin-reports-page">
    <header class="page-header">
      <h1 class="page-title">Жалобы</h1>
      <p class="page-subtitle">Рассмотрение жалоб на посты пользователей.</p>
    </header>

    <!-- Статистика -->
    <div v-if="stats" class="stats-grid">
      <div class="stat-item">
        <span class="stat-label">Всего</span>
        <span class="stat-value">{{ stats.total }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Новых</span>
        <span class="stat-value text-warning">{{ stats.pending }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Решено</span>
        <span class="stat-value text-success">{{ stats.resolved }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Отклонено</span>
        <span class="stat-value text-danger">{{ stats.rejected }}</span>
      </div>
    </div>

    <!-- Фильтр по статусу -->
    <div class="filters">
      <div class="tabs">
        <button
          v-for="(label, key) in { pending: 'Новые', resolved: 'Решённые', rejected: 'Отклонённые', '': 'Все' }"
          :key="key"
          class="tab-btn"
          :class="{ 'tab-btn--active': statusFilter === key }"
          @click="statusFilter = key; page = 1"
        >
          {{ label }}
        </button>
      </div>
    </div>

    <!-- Список жалоб -->
    <div v-if="pending" class="loading">
      <BaseSkeleton height="120px" rounded v-for="i in 3" :key="i" />
    </div>

    <div v-else-if="reports.length === 0" class="empty">
      Жалоб с таким статусом нет.
    </div>

    <div v-else class="reports-list">
      <BaseCard v-for="report in reports" :key="report.id" padding="lg" class="report-card">
        <div class="report-header">
          <div class="report-meta">
            <span class="badge" :class="statusConfig[report.status].class">
              {{ statusConfig[report.status].label }}
            </span>
            <span class="badge badge--neutral">{{ categoryLabels[report.category] || report.category }}</span>
            <span class="date">{{ formatDate(report.created_at) }}</span>
          </div>
          <span class="report-id">#{{ report.id }}</span>
        </div>

        <div class="report-body">
          <div class="report-info">
            <p><strong>Жалоба от:</strong> {{ report.reporter || 'Пользователь' }}</p>
            <p v-if="report.description"><strong>Описание:</strong> {{ report.description }}</p>
            <p v-if="report.post_snapshot">
              <strong>Пост:</strong> {{ report.post_snapshot.content }}
            </p>
          </div>
          <div v-if="report.post_snapshot?.image" class="report-image">
            <img :src="useMediaUrl()(report.post_snapshot.image)!" alt="Пост" />
          </div>
        </div>

        <div v-if="report.status === 'pending'" class="report-actions">
          <BaseButton variant="primary" size="sm" @click="openResolve(report)">
            <i class="fa-solid fa-gavel"></i> Рассмотреть
          </BaseButton>
        </div>
        <div v-else class="report-resolution">
          <p><strong>Действие:</strong> {{ report.resolution_action === 'none' ? 'Жалоба отклонена' : report.resolution_action === 'post_deleted' ? 'Пост удалён' : report.resolution_action === 'user_banned' ? 'Автор забанен' : 'Пост удалён и автор забанен' }}</p>
          <p v-if="report.resolution_note"><strong>Комментарий:</strong> {{ report.resolution_note }}</p>
        </div>
      </BaseCard>
    </div>

    <!-- Пагинация -->
    <div v-if="totalPages > 1" class="pagination">
      <BaseButton variant="secondary" :disabled="page <= 1" @click="page--">
        <i class="fa-solid fa-chevron-left"></i>
      </BaseButton>
      <span>Страница {{ page }} из {{ totalPages }}</span>
      <BaseButton variant="secondary" :disabled="page >= totalPages" @click="page++">
        <i class="fa-solid fa-chevron-right"></i>
      </BaseButton>
    </div>

    <!-- Модалка рассмотрения -->
    <BaseModal v-if="resolvingReport" title="Рассмотреть жалобу" @close="resolvingReport = null">
      <div class="resolve-form">
        <p>Жалоба на пост: <strong>«{{ resolvingReport.post_snapshot?.content?.slice(0, 50) }}...»</strong></p>

        <div class="radio-group">
          <label class="radio-item">
            <input type="radio" v-model="resolutionAction" value="none" />
            <span>Отклонить жалобу (нарушений нет)</span>
          </label>
          <label class="radio-item">
            <input type="radio" v-model="resolutionAction" value="post_deleted" />
            <span>Удалить пост</span>
          </label>
          <label class="radio-item">
            <input type="radio" v-model="resolutionAction" value="user_banned" />
            <span>Забанить автора</span>
          </label>
          <label class="radio-item">
            <input type="radio" v-model="resolutionAction" value="both" />
            <span>Удалить пост и забанить автора</span>
          </label>
        </div>

        <BaseTextarea
          v-model="resolutionNote"
          label="Комментарий (необязательно)"
          placeholder="Например: нарушение правил сообщества..."
        />
      </div>

      <template #footer>
        <BaseButton variant="ghost" size="sm" @click="resolvingReport = null">Отмена</BaseButton>
        <BaseButton variant="primary" size="sm" :loading="isResolving" @click="submitResolve">Применить</BaseButton>
      </template>
    </BaseModal>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.admin-reports-page { display: flex; flex-direction: column; gap: var(--space-5); }
.page-title { font-size: var(--text-2xl); font-weight: var(--fw-bold); }
.page-subtitle { color: var(--color-text-secondary); margin-top: var(--space-1); }

/* Статистика */
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: var(--space-3); }
.stat-item { background: var(--color-surface); padding: var(--space-3); border-radius: var(--radius-md); border: 1px solid var(--color-border); display: flex; flex-direction: column; gap: 2px; }
.stat-label { font-size: var(--text-xs); color: var(--color-text-tertiary); text-transform: uppercase; }
.stat-value { font-size: var(--text-xl); font-weight: var(--fw-bold); }
.text-warning { color: var(--color-warning); }
.text-success { color: var(--color-success); }
.text-danger { color: var(--color-danger); }

/* Фильтры */
.filters { display: flex; justify-content: flex-start; }
.tabs { display: flex; gap: var(--space-2); background: var(--color-surface-secondary); padding: 4px; border-radius: var(--radius-md); }
.tab-btn {
  padding: var(--space-2) var(--space-4); border-radius: var(--radius-sm); font-size: var(--text-sm); font-weight: var(--fw-medium);
  color: var(--color-text-secondary); transition: all var(--transition-fast); border: none; background: transparent; cursor: pointer;
  &--active { background: var(--color-surface); color: var(--color-brand); box-shadow: var(--shadow-sm); }
}

/* Список жалоб */
.reports-list { display: flex; flex-direction: column; gap: var(--space-4); }
.report-card { background: var(--color-surface); }

.report-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--space-3); }
.report-meta { display: flex; align-items: center; gap: var(--space-2); }
.badge { display: inline-block; padding: 2px 8px; border-radius: var(--radius-full); font-size: var(--text-xs); font-weight: var(--fw-medium); }
.badge--warning { background: var(--color-warning-soft); color: var(--color-warning-strong); }
.badge--success { background: var(--color-success-soft); color: var(--color-success-strong); }
.badge--danger { background: var(--color-danger-soft); color: var(--color-danger-strong); }
.badge--neutral { background: var(--color-surface-secondary); color: var(--color-text-secondary); }
.date { font-size: var(--text-xs); color: var(--color-text-tertiary); }
.report-id { font-size: var(--text-xs); font-family: var(--font-mono); color: var(--color-text-tertiary); }

.report-body { display: flex; gap: var(--space-4); margin-bottom: var(--space-4); }
.report-info { flex: 1; display: flex; flex-direction: column; gap: var(--space-1); font-size: var(--text-sm); line-height: var(--leading-relaxed); }
.report-image { flex-shrink: 0; max-width: 200px; border-radius: var(--radius-md); overflow: hidden; img { width: 100%; height: auto; display: block; } }

.report-actions { display: flex; justify-content: flex-end; padding-top: var(--space-3); border-top: 1px solid var(--color-border-light); }
.report-resolution { padding-top: var(--space-3); border-top: 1px solid var(--color-border-light); font-size: var(--text-sm); color: var(--color-text-secondary); display: flex; flex-direction: column; gap: var(--space-1); }

.loading { display: flex; flex-direction: column; gap: var(--space-3); }
.empty { padding: var(--space-8); text-align: center; color: var(--color-text-secondary); background: var(--color-surface-secondary); border-radius: var(--radius-md); }
.pagination { display: flex; justify-content: center; align-items: center; gap: var(--space-3); }

/* Модалка */
.resolve-form { display: flex; flex-direction: column; gap: var(--space-4); }
.radio-group { display: flex; flex-direction: column; gap: var(--space-2); }
.radio-item { display: flex; align-items: center; gap: var(--space-2); font-size: var(--text-sm); cursor: pointer; }
</style>
