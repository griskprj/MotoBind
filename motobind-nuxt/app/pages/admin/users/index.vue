<script setup lang="ts">
import type { AdminUser, AdminUsersResponse } from '~/types'

definePageMeta({ middleware: ['auth', 'admin'] })

useSeoMeta({ title: 'Пользователи — Админка', robots: 'noindex' })

const api = useApi()
const toast = useToast()

// Состояние фильтров
const searchQuery = ref('')
const debouncedSearch = useDebounce(searchQuery, 500)
const roleFilter = ref('')
const statusFilter = ref('')
const page = ref(1)

const data = ref<AdminUsersResponse | null>(null)
const pending = ref(false)

// Загрузка пользователей
async function loadUsers() {
  pending.value = true
  try {
    data.value = await api.admin.getUsers({
      page: page.value,
      per_page: 20,
      search: debouncedSearch.value || undefined,
      role: roleFilter.value || undefined,
      status: statusFilter.value || undefined,
    })
  } catch (e) {
    toast.error('Не удалось загрузить пользователей')
  } finally {
    pending.value = false
  }
}

onMounted(loadUsers)
watch([debouncedSearch, roleFilter, statusFilter, page], loadUsers)

// Бан / Разбан
async function toggleBan(user: AdminUser) {
  const action = user.status === 'banned' ? 'unban' : 'ban'
  const actionText = action === 'ban' ? 'заблокировать' : 'разблокировать'

  if (!confirm(`Вы уверены, что хотите ${actionText} пользователя ${user.username}?`)) return

  try {
    if (action === 'ban') {
      await api.admin.banUser(user.id)
    } else {
      await api.admin.unbanUser(user.id)
    }
    toast.success(`Пользователь ${action === 'ban' ? 'заблокирован' : 'разблокирован'}`)
    await loadUsers()
  } catch (e) {
    toast.error('Ошибка выполнения действия')
  }
}

// Форматирование даты
const formatDate = (iso?: string) => {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('ru-RU')
}

// Бейджи ролей и статусов
const roleLabels = {
  motorcyclist: 'Мотоциклист',
  motoclub: 'Мотоклуб',
  admin: 'Админ',
}

const statusLabels = {
  active: 'Активен',
  banned: 'Забанен',
}
</script>

<template>
  <div class="admin-users-page">
    <header class="page-header">
      <div>
        <h1 class="page-title">Пользователи</h1>
        <p class="page-subtitle">Управление аккаунтами и ролями.</p>
      </div>
    </header>

    <!-- Фильтры -->
    <div class="filters">
      <div class="search-wrap">
        <i class="fa-solid fa-magnifying-glass search-icon"></i>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Поиск по имени или email..."
          class="search-input"
        />
      </div>

      <select v-model="roleFilter" class="filter-select">
        <option value="">Все роли</option>
        <option value="motorcyclist">Мотоциклисты</option>
        <option value="motoclub">Мотоклубы</option>
        <option value="admin">Админы</option>
      </select>

      <select v-model="statusFilter" class="filter-select">
        <option value="">Все статусы</option>
        <option value="active">Активные</option>
        <option value="banned">Забаненные</option>
      </select>
    </div>

    <!-- Статистика -->
    <div v-if="data" class="stats-grid">
      <div class="stat-item">
        <span class="stat-label">Всего</span>
        <span class="stat-value">{{ data.stats.total }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Активных</span>
        <span class="stat-value text-success">{{ data.stats.active }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Забаненных</span>
        <span class="stat-value text-danger">{{ data.stats.banned }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Админов</span>
        <span class="stat-value text-brand">{{ data.stats.admin }}</span>
      </div>
    </div>

    <!-- Таблица -->
    <BaseCard padding="none" class="table-card">
      <div v-if="pending" class="loading">
        <BaseSkeleton height="60px" v-for="i in 5" :key="i" />
      </div>

      <div v-else-if="!data?.users.length" class="empty">
        Пользователи не найдены.
      </div>

      <div v-else class="table-wrap">
        <table class="users-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Пользователь</th>
              <th>Email</th>
              <th>Роль</th>
              <th>Статус</th>
              <th>Дата</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in data.users" :key="user.id">
              <td class="text-mono">{{ user.id }}</td>
              <td>
                <div class="user-cell">
                  <div class="avatar"><i class="fa-solid fa-user"></i></div>
                  <span class="username">{{ user.username }}</span>
                </div>
              </td>
              <td class="text-mono">{{ user.email }}</td>
              <td>
                <span class="badge" :class="`badge--${user.role}`">
                  {{ roleLabels[user.role] }}
                </span>
              </td>
              <td>
                <span class="badge" :class="user.status === 'active' ? 'badge--success' : 'badge--danger'">
                  {{ statusLabels[user.status] }}
                </span>
              </td>
              <td class="text-sm">{{ formatDate(user.created_at) }}</td>
              <td>
                <BaseButton
                  :variant="user.status === 'banned' ? 'secondary' : 'danger'"
                  size="sm"
                  @click="toggleBan(user)"
                >
                  <i :class="user.status === 'banned' ? 'fa-solid fa-unlock' : 'fa-solid fa-ban'"></i>
                  {{ user.status === 'banned' ? 'Разбанить' : 'Забанить' }}
                </BaseButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </BaseCard>

    <!-- Пагинация -->
    <div v-if="data && data.pages > 1" class="pagination">
      <BaseButton variant="secondary" :disabled="page <= 1" @click="page--">
        <i class="fa-solid fa-chevron-left"></i>
      </BaseButton>
      <span>Страница {{ page }} из {{ data.pages }}</span>
      <BaseButton variant="secondary" :disabled="page >= data.pages" @click="page++">
        <i class="fa-solid fa-chevron-right"></i>
      </BaseButton>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.admin-users-page { display: flex; flex-direction: column; gap: var(--space-5); }
.page-title { font-size: var(--text-2xl); font-weight: var(--fw-bold); }
.page-subtitle { color: var(--color-text-secondary); margin-top: var(--space-1); }

/* Фильтры */
.filters {
  display: flex; flex-direction: column; gap: var(--space-3);
  background: var(--color-surface); padding: var(--space-3); border-radius: var(--radius-md); border: 1px solid var(--color-border);
  @include md-up { flex-direction: row; align-items: center; }
}
.search-wrap { position: relative; flex: 1; }
.search-icon { position: absolute; left: var(--space-3); top: 50%; transform: translateY(-50%); color: var(--color-text-tertiary); }
.search-input {
  width: 100%; padding: var(--space-2) var(--space-3) var(--space-2) var(--space-8);
  border: 1px solid var(--color-border); border-radius: var(--radius-md); background: var(--color-surface); color: var(--color-text);
  &:focus { outline: none; border-color: var(--color-brand); box-shadow: var(--shadow-focus); }
}
.filter-select {
  padding: var(--space-2) var(--space-3); border: 1px solid var(--color-border); border-radius: var(--radius-md);
  background: var(--color-surface); color: var(--color-text); font-size: var(--text-sm);
}

/* Статистика */
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: var(--space-3); }
.stat-item { background: var(--color-surface); padding: var(--space-3); border-radius: var(--radius-md); border: 1px solid var(--color-border); display: flex; flex-direction: column; gap: 2px; }
.stat-label { font-size: var(--text-xs); color: var(--color-text-tertiary); text-transform: uppercase; }
.stat-value { font-size: var(--text-xl); font-weight: var(--fw-bold); }
.text-success { color: var(--color-success); }
.text-danger { color: var(--color-danger); }
.text-brand { color: var(--color-brand); }

/* Таблица */
.table-card { overflow: hidden; }
.table-wrap { overflow-x: auto; }
.users-table {
  width: 100%; border-collapse: collapse; font-size: var(--text-sm);
  th { text-align: left; padding: var(--space-3); font-weight: var(--fw-semibold); color: var(--color-text-tertiary); border-bottom: 1px solid var(--color-border); white-space: nowrap; }
  td { padding: var(--space-3); border-bottom: 1px solid var(--color-border-light); vertical-align: middle; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: var(--color-surface-hover); }
}

.user-cell { display: flex; align-items: center; gap: var(--space-2); }
.avatar { width: 28px; height: 28px; border-radius: 50%; background: var(--color-surface-secondary); display: flex; align-items: center; justify-content: center; color: var(--color-text-tertiary); font-size: 12px; }
.username { font-weight: var(--fw-medium); }
.text-mono { font-family: var(--font-mono); font-size: var(--text-xs); }
.text-sm { font-size: var(--text-xs); color: var(--color-text-secondary); }

.badge { display: inline-block; padding: 2px 8px; border-radius: var(--radius-full); font-size: var(--text-xs); font-weight: var(--fw-medium); text-transform: capitalize; }
.badge--admin { background: var(--color-brand-soft); color: var(--color-brand); }
.badge--motoclub { background: var(--color-info-soft); color: var(--color-info); }
.badge--motorcyclist { background: var(--color-surface-secondary); color: var(--color-text-secondary); }
.badge--success { background: var(--color-success-soft); color: var(--color-success-strong); }
.badge--danger { background: var(--color-danger-soft); color: var(--color-danger-strong); }

.loading { display: flex; flex-direction: column; gap: var(--space-2); padding: var(--space-4); }
.empty { padding: var(--space-8); text-align: center; color: var(--color-text-secondary); }

.pagination { display: flex; justify-content: center; align-items: center; gap: var(--space-3); }
</style>
