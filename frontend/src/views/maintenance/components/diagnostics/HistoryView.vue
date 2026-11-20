<template>
  <div class="history-view">
    <div class="history-head">
      <button type="button" class="back-btn" @click="emit('back')">
        <i class="fa fa-arrow-left" />
        Назад
      </button>
      <h4>История диагностик</h4>
    </div>

    <div v-if="store.reports.length === 0" class="history-empty">
      <i class="fa fa-inbox" />
      <p>Сохранённых отчётов пока нет</p>
    </div>

    <div v-else class="history-list">
      <div
        v-for="r in store.reports"
        :key="r.id"
        class="history-item"
        @click="emit('open', r.id)"
      >
        <div class="history-item__head">
          <span class="history-item__date">{{ formatDate(r.created_at) }}</span>
          <span v-if="r.locked_group" class="history-item__group">
            {{ groupLabel(r.locked_group) }}
          </span>
          <span v-else class="history-item__group">Общая</span>
        </div>
        <div class="history-item__body">
          <span class="history-item__count">
            Найдено причин: {{ r.results?.length || 0 }}
          </span>
          <span v-if="r.results?.[0]" class="history-item__top">
            Топ: {{ topCause(r) }}
          </span>
        </div>
        <button
          type="button"
          class="history-item__delete"
          @click.stop="onDelete(r.id)"
        >
          <i class="fa fa-trash" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useDiagnosticsStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import { RULES, SYMPTOM_GROUP_BY_ID } from '@/constants/diagnisticsRules'

const emit = defineEmits(['back', 'open'])

const store = useDiagnosticsStore()
const toast = useToast()

const RULES_BY_ID = Object.fromEntries(RULES.map((r) => [r.id, r]))

function formatDate(iso) {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function groupLabel(groupId) {
  return SYMPTOM_GROUP_BY_ID[groupId]?.label || groupId
}

function topCause(report) {
  const top = report.results?.[0]
  if (!top) return '—'
  const rule = RULES_BY_ID[top.rule_id]
  return rule?.title || 'Правило удалено'
}

async function onDelete(id) {
  if (!confirm('Удалить отчёт?')) return
  try {
    await store.deleteReport(id)
    toast.success('Отчёт удалён')
  } catch (err) {
    toast.error('Не удалось удалить')
  }
}
</script>

<style scoped>
.history-view {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

/* ===== Шапка ===== */
.history-head {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.history-head h4 {
  margin: 0;
  font-size: var(--text-base);
}

.history-head .back-btn {
  align-self: flex-start;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 2px;
  background: none;
  border: none;
  color: var(--text-primary);
  font-family: inherit;
  font-size: var(--text-sm);
  cursor: pointer;
  min-height: 0;
  transition: all var(--transition-base);
}

.history-head .back-btn:hover {
  color: var(--accent-text);
}

.history-head .back-btn i {
  font-size: 12px;
}

/* ===== Пусто ===== */
.history-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 48px 16px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  border: 1px dashed var(--border-color);
  color: var(--text-muted);
}

.history-empty i {
  font-size: 36px;
  color: var(--accent);
  opacity: 0.5;
}

.history-empty p {
  margin: 0;
  font-size: var(--text-sm);
}

/* ===== Список ===== */
.history-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.history-item {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 14px 44px 14px 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
  min-height: 60px;
}

.history-item:hover {
  background: var(--bg-card-hover);
  border-color: var(--accent);
}

.history-item__head {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.history-item__date {
  font-size: 13px;
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
}

.history-item__group {
  font-size: 11px;
  font-weight: var(--fw-medium);
  padding: 2px 8px;
  background: var(--accent-trans);
  color: var(--accent-text);
  border-radius: var(--radius-full);
}

.history-item__body {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.history-item__count {
  font-size: 12px;
  color: var(--text-muted);
}

.history-item__top {
  font-size: 13px;
  color: var(--text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100%;
}

.history-item__delete {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 32px;
  height: 32px;
  min-height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: var(--radius-md);
  color: var(--text-muted);
  font-size: 13px;
  cursor: pointer;
  transition: all var(--transition-base);
  padding: 0;
}

.history-item__delete:hover {
  background: var(--danger-trans);
  color: var(--danger-text);
}
</style>
