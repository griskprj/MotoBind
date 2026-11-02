<script setup lang="ts">
import type { Manual } from '~/types'

definePageMeta({ middleware: ['auth', 'admin'] })

useSeoMeta({ title: 'Модерация мануалов — Админка', robots: 'noindex' })

const api = useApi()
const toast = useToast()

const manuals = ref<Manual[]>([])
const pending = ref(false)

async function loadManuals() {
  pending.value = true
  try {
    const res = await api.admin.getDashboard()
    manuals.value = res.manuals.filter((m: any) => m.status === 'moderate')
  } catch (e) {
    toast.error('Не удалось загрузить мануалы')
  } finally {
    pending.value = false
  }
}

onMounted(loadManuals)

async function approveManual(manual: Manual) {
  try {
    await api.admin.approveManual(manual.id)
    toast.success(`Мануал "${manual.title}" одобрен`)
    await loadManuals()
  } catch (e) {
    toast.error('Ошибка одобрения')
  }
}

const rejectingManual = ref<Manual | null>(null)
const rejectionReason = ref('')
const isRejecting = ref(false)

function openReject(manual: Manual) {
  rejectingManual.value = manual
  rejectionReason.value = ''
}

async function submitReject() {
  if (!rejectingManual.value || !rejectionReason.value.trim()) {
    toast.error('Укажите причину отклонения')
    return
  }

  isRejecting.value = true
  try {
    await api.admin.rejectManual(rejectingManual.value.id, rejectionReason.value.trim())
    toast.success('Мануал отклонён')
    rejectingManual.value = null
    await loadManuals()
  } catch (e) {
    toast.error('Ошибка отклонения')
  } finally {
    isRejecting.value = false
  }
}

const formatDate = (iso?: string | null) => {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('ru-RU')
}
</script>

<template>
  <div class="admin-manuals-page">
    <header class="page-header">
      <h1 class="page-title">Модерация мануалов</h1>
      <p class="page-subtitle">Одобряйте или отклоняйте мануалы от пользователей.</p>
    </header>

    <BaseCard padding="none" class="table-card">
      <div v-if="pending" class="loading">
        <BaseSkeleton height="60px" v-for="i in 5" :key="i" />
      </div>

      <div v-else-if="manuals.length === 0" class="empty">
        Нет мануалов на модерации.
      </div>

      <div v-else class="table-wrap">
        <table class="manuals-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Название</th>
              <th>Автор</th>
              <th>Мотоцикл</th>
              <th>Дата</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="manual in manuals" :key="manual.id">
              <td class="text-mono">{{ manual.id }}</td>
              <td>
                <NuxtLink :to="`/manuals/${manual.id}`" class="manual-link" target="_blank">
                  {{ manual.title }}
                </NuxtLink>
              </td>
              <td>{{ manual.author_username || '—' }}</td>
              <td>{{ manual.motorcycle }}</td>
              <td class="text-sm">{{ formatDate(manual.created_at) }}</td>
              <td>
                <div class="actions">
                  <BaseButton variant="primary" size="sm" @click="approveManual(manual)">
                    <i class="fa-solid fa-check"></i> Одобрить
                  </BaseButton>
                  <BaseButton variant="danger" size="sm" @click="openReject(manual)">
                    <i class="fa-solid fa-xmark"></i> Отклонить
                  </BaseButton>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </BaseCard>

    <!-- Модалка отклонения -->
    <BaseModal v-if="rejectingManual" title="Отклонить мануал" @close="rejectingManual = null">
      <div class="reject-form">
        <p>Вы отклоняете мануал <strong>«{{ rejectingManual.title }}»</strong>.</p>
        <BaseTextarea
          v-model="rejectionReason"
          label="Причина отклонения"
          placeholder="Например: недостаточно информации, нарушает правила..."
          required
        />
      </div>
      <template #footer>
        <BaseButton variant="ghost" size="sm" @click="rejectingManual = null">Отмена</BaseButton>
        <BaseButton variant="danger" size="sm" :loading="isRejecting" @click="submitReject">Отклонить</BaseButton>
      </template>
    </BaseModal>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.admin-manuals-page { display: flex; flex-direction: column; gap: var(--space-5); }
.page-title { font-size: var(--text-2xl); font-weight: var(--fw-bold); }
.page-subtitle { color: var(--color-text-secondary); margin-top: var(--space-1); }

.table-card { overflow: hidden; }
.table-wrap { overflow-x: auto; }
.manuals-table {
  width: 100%; border-collapse: collapse; font-size: var(--text-sm);
  th { text-align: left; padding: var(--space-3); font-weight: var(--fw-semibold); color: var(--color-text-tertiary); border-bottom: 1px solid var(--color-border); white-space: nowrap; }
  td { padding: var(--space-3); border-bottom: 1px solid var(--color-border-light); vertical-align: middle; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: var(--color-surface-hover); }
}

.manual-link { color: var(--color-text); font-weight: var(--fw-medium); text-decoration: none; &:hover { color: var(--color-brand); text-decoration: underline; } }
.text-mono { font-family: var(--font-mono); font-size: var(--text-xs); }
.text-sm { font-size: var(--text-xs); color: var(--color-text-secondary); }

.actions { display: flex; gap: var(--space-2); }

.loading { display: flex; flex-direction: column; gap: var(--space-2); padding: var(--space-4); }
.empty { padding: var(--space-8); text-align: center; color: var(--color-text-secondary); }

.reject-form { display: flex; flex-direction: column; gap: var(--space-4); }
</style>
