<script setup lang="ts">
import type { AdminUser, AdminUsersResponse } from '~/types'

definePageMeta({ middleware: ['auth', 'admin'] })
useSeoMeta({ title: 'Пользователи — Админка', robots: 'noindex' })

const api = useApi()
const toast = useToast()
const auth = useAuthStore()

const searchQuery = ref('')
const debouncedSearch = useDebounce(searchQuery, 500)
const roleFilter = ref('')
const statusFilter = ref('')
const page = ref(1)
const data = ref<AdminUsersResponse | null>(null)
const pending = ref(false)

const editingUser = ref<AdminUser | null>(null)
const editForm = reactive({ username: '', email: '', role: 'motorcyclist' as AdminUser['role'], status: 'active' as AdminUser['status'] })
const savingUser = ref(false)
const deletingUserId = ref<number | null>(null)

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
  } catch {
    toast.error('Не удалось загрузить пользователей')
  } finally {
    pending.value = false
  }
}

onMounted(loadUsers)
watch([debouncedSearch, roleFilter, statusFilter, page], loadUsers)

function openEdit(user: AdminUser) {
  editingUser.value = user
  editForm.username = user.username
  editForm.email = user.email
  editForm.role = user.role
  editForm.status = user.status
}

function closeEdit() {
  if (savingUser.value) return
  editingUser.value = null
}

async function saveUser() {
  if (!editingUser.value) return
  savingUser.value = true
  try {
    await api.admin.updateUser(editingUser.value.id, { ...editForm })
    toast.success('Данные пользователя обновлены')
    editingUser.value = null
    await loadUsers()
  } catch (error: any) {
    toast.error(error?.message || 'Не удалось сохранить изменения')
  } finally {
    savingUser.value = false
  }
}

async function deleteUser(user: AdminUser) {
  if (user.id === Number(auth.user?.id)) {
    toast.error('Нельзя удалить собственный аккаунт')
    return
  }
  if (!confirm(`Удалить пользователя «${user.username}»? Это действие нельзя отменить.`)) return
  deletingUserId.value = user.id
  try {
    await api.admin.deleteUser(user.id)
    toast.success('Пользователь удалён')
    if (data.value && data.value.users.length === 1 && page.value > 1) page.value--
    await loadUsers()
  } catch (error: any) {
    toast.error(error?.message || 'Не удалось удалить пользователя')
  } finally {
    deletingUserId.value = null
  }
}

async function toggleBan(user: AdminUser) {
  const action = user.status === 'banned' ? 'unban' : 'ban'
  const actionText = action === 'ban' ? 'заблокировать' : 'разблокировать'
  if (!confirm(`Вы уверены, что хотите ${actionText} пользователя ${user.username}?`)) return
  try {
    if (action === 'ban') await api.admin.banUser(user.id)
    else await api.admin.unbanUser(user.id)
    toast.success(`Пользователь ${action === 'ban' ? 'заблокирован' : 'разблокирован'}`)
    await loadUsers()
  } catch {
    toast.error('Ошибка выполнения действия')
  }
}

const formatDate = (iso?: string | null, withTime = false) => {
  if (!iso) return '—'
  return new Date(iso).toLocaleString('ru-RU', withTime
    ? { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }
    : { day: '2-digit', month: '2-digit', year: 'numeric' })
}

const roleLabels = { motorcyclist: 'Мотоциклист', motoclub: 'Мотоклуб', admin: 'Админ' }
const statusLabels = { active: 'Активен', banned: 'Забанен' }
</script>

<template>
  <div class="admin-users-page">
    <header class="page-header">
      <div>
        <h1 class="page-title">Пользователи</h1>
        <p class="page-subtitle">Управление аккаунтами и ролями.</p>
      </div>
    </header>

    <div class="filters">
      <div class="search-wrap">
        <i class="fa-solid fa-magnifying-glass search-icon"></i>
        <input v-model="searchQuery" type="text" placeholder="Поиск по имени или email..." class="search-input" />
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

    <div v-if="data" class="stats-grid">
      <div class="stat-item"><span class="stat-label">Всего</span><span class="stat-value">{{ data.stats.total }}</span></div>
      <div class="stat-item"><span class="stat-label">Активных</span><span class="stat-value text-success">{{ data.stats.active }}</span></div>
      <div class="stat-item"><span class="stat-label">Забаненных</span><span class="stat-value text-danger">{{ data.stats.banned }}</span></div>
      <div class="stat-item"><span class="stat-label">Админов</span><span class="stat-value text-brand">{{ data.stats.admin }}</span></div>
    </div>

    <BaseCard padding="none" class="table-card">
      <div v-if="pending" class="loading"><BaseSkeleton v-for="i in 5" :key="i" height="60px" /></div>
      <div v-else-if="!data?.users.length" class="empty">Пользователи не найдены.</div>
      <div v-else class="table-wrap">
        <table class="users-table">
          <thead>
            <tr><th>ID</th><th>Пользователь</th><th>Email</th><th>Роль</th><th>Статус</th><th>Регистрация</th><th>Последний вход</th><th>Действия</th></tr>
          </thead>
          <tbody>
            <tr v-for="user in data.users" :key="user.id">
              <td class="text-mono">{{ user.id }}</td>
              <td><div class="user-cell"><div class="avatar"><i class="fa-solid fa-user"></i></div><span class="username">{{ user.username }}</span></div></td>
              <td class="text-mono">{{ user.email }}</td>
              <td><span class="badge" :class="`badge--${user.role}`">{{ roleLabels[user.role] }}</span></td>
              <td><span class="badge" :class="user.status === 'active' ? 'badge--success' : 'badge--danger'">{{ statusLabels[user.status] }}</span></td>
              <td class="text-sm">{{ formatDate(user.created_at) }}</td>
              <td class="text-sm">{{ formatDate(user.last_login, true) }}</td>
              <td>
                <div class="actions">
                  <BaseButton variant="secondary" size="sm" @click="openEdit(user)"><i class="fa-solid fa-pen"></i> Изменить</BaseButton>
                  <BaseButton :variant="user.status === 'banned' ? 'secondary' : 'danger'" size="sm" @click="toggleBan(user)">
                    <i :class="user.status === 'banned' ? 'fa-solid fa-unlock' : 'fa-solid fa-ban'"></i>
                    {{ user.status === 'banned' ? 'Разбанить' : 'Забанить' }}
                  </BaseButton>
                  <BaseButton variant="danger" size="sm" :disabled="user.id === Number(auth.user?.id) || deletingUserId === user.id" @click="deleteUser(user)">
                    <i class="fa-solid fa-trash"></i> Удалить
                  </BaseButton>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </BaseCard>

    <div v-if="data && data.pages > 1" class="pagination">
      <BaseButton variant="secondary" :disabled="page <= 1" @click="page--"><i class="fa-solid fa-chevron-left"></i></BaseButton>
      <span>Страница {{ page }} из {{ data.pages }}</span>
      <BaseButton variant="secondary" :disabled="page >= data.pages" @click="page++"><i class="fa-solid fa-chevron-right"></i></BaseButton>
    </div>

    <Teleport to="body">
      <div v-if="editingUser" class="modal-backdrop" @click.self="closeEdit">
        <section class="edit-modal" role="dialog" aria-modal="true" aria-labelledby="edit-user-title">
          <header class="modal-header">
            <div><h2 id="edit-user-title">Редактирование пользователя</h2><p>ID: {{ editingUser.id }}</p></div>
            <button class="close-button" type="button" aria-label="Закрыть" @click="closeEdit"><i class="fa-solid fa-xmark"></i></button>
          </header>
          <form class="edit-form" @submit.prevent="saveUser">
            <label>Имя пользователя<input v-model.trim="editForm.username" required minlength="2" maxlength="32" /></label>
            <label>Email<input v-model.trim="editForm.email" type="email" required /></label>
            <label>Роль
              <select v-model="editForm.role">
                <option value="motorcyclist">Мотоциклист</option><option value="motoclub">Мотоклуб</option><option value="admin">Администратор</option>
              </select>
            </label>
            <label>Статус
              <select v-model="editForm.status"><option value="active">Активен</option><option value="banned">Заблокирован</option></select>
            </label>
            <footer class="modal-actions">
              <BaseButton variant="secondary" type="button" :disabled="savingUser" @click="closeEdit">Отмена</BaseButton>
              <BaseButton type="submit" :disabled="savingUser || !editForm.username || !editForm.email">{{ savingUser ? 'Сохранение...' : 'Сохранить' }}</BaseButton>
            </footer>
          </form>
        </section>
      </div>
    </Teleport>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;
.admin-users-page { display: flex; flex-direction: column; gap: var(--space-5); }
.page-title { font-size: var(--text-2xl); font-weight: var(--fw-bold); }
.page-subtitle { color: var(--color-text-secondary); margin-top: var(--space-1); }
.filters { display: flex; flex-direction: column; gap: var(--space-3); background: var(--color-surface); padding: var(--space-3); border-radius: var(--radius-md); border: 1px solid var(--color-border); @include md-up { flex-direction: row; align-items: center; } }
.search-wrap { position: relative; flex: 1; }
.search-icon { position: absolute; left: var(--space-3); top: 50%; transform: translateY(-50%); color: var(--color-text-tertiary); }
.search-input { width: 100%; padding: var(--space-2) var(--space-3) var(--space-2) var(--space-8); border: 1px solid var(--color-border); border-radius: var(--radius-md); background: var(--color-surface); color: var(--color-text); &:focus { outline: none; border-color: var(--color-brand); box-shadow: var(--shadow-focus); } }
.filter-select { padding: var(--space-2) var(--space-3); border: 1px solid var(--color-border); border-radius: var(--radius-md); background: var(--color-surface); color: var(--color-text); font-size: var(--text-sm); }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: var(--space-3); }
.stat-item { background: var(--color-surface); padding: var(--space-3); border-radius: var(--radius-md); border: 1px solid var(--color-border); display: flex; flex-direction: column; gap: 2px; }
.stat-label { font-size: var(--text-xs); color: var(--color-text-tertiary); text-transform: uppercase; }
.stat-value { font-size: var(--text-xl); font-weight: var(--fw-bold); }
.text-success { color: var(--color-success); }.text-danger { color: var(--color-danger); }.text-brand { color: var(--color-brand); }
.table-card { overflow: hidden; }.table-wrap { overflow-x: auto; }
.users-table { width: 100%; border-collapse: collapse; font-size: var(--text-sm); th { text-align: left; padding: var(--space-3); font-weight: var(--fw-semibold); color: var(--color-text-tertiary); border-bottom: 1px solid var(--color-border); white-space: nowrap; } td { padding: var(--space-3); border-bottom: 1px solid var(--color-border-light); vertical-align: middle; } tr:last-child td { border-bottom: none; } tr:hover td { background: var(--color-surface-hover); } }
.user-cell { display: flex; align-items: center; gap: var(--space-2); }.avatar { width: 28px; height: 28px; border-radius: 50%; background: var(--color-surface-secondary); display: flex; align-items: center; justify-content: center; color: var(--color-text-tertiary); font-size: 12px; }.username { font-weight: var(--fw-medium); }
.text-mono { font-family: var(--font-mono); font-size: var(--text-xs); }.text-sm { font-size: var(--text-xs); color: var(--color-text-secondary); }
.badge { display: inline-block; padding: 2px 8px; border-radius: var(--radius-full); font-size: var(--text-xs); font-weight: var(--fw-medium); text-transform: capitalize; }
.badge--admin { background: var(--color-brand-soft); color: var(--color-brand); }.badge--motoclub { background: var(--color-info-soft); color: var(--color-info); }.badge--motorcyclist { background: var(--color-surface-secondary); color: var(--color-text-secondary); }.badge--success { background: var(--color-success-soft); color: var(--color-success-strong); }.badge--danger { background: var(--color-danger-soft); color: var(--color-danger-strong); }
.actions { display: flex; flex-wrap: wrap; gap: var(--space-2); min-width: 260px; }
.loading { display: flex; flex-direction: column; gap: var(--space-2); padding: var(--space-4); }.empty { padding: var(--space-8); text-align: center; color: var(--color-text-secondary); }
.pagination { display: flex; justify-content: center; align-items: center; gap: var(--space-3); }
.modal-backdrop { position: fixed; inset: 0; z-index: 1000; display: flex; align-items: center; justify-content: center; padding: var(--space-4); background: rgb(0 0 0 / 60%); }
.edit-modal { width: min(100%, 480px); background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-lg); box-shadow: var(--shadow-lg); }
.modal-header { display: flex; justify-content: space-between; align-items: flex-start; padding: var(--space-4); border-bottom: 1px solid var(--color-border); h2 { font-size: var(--text-lg); font-weight: var(--fw-semibold); } p { color: var(--color-text-tertiary); font-size: var(--text-xs); margin-top: 4px; } }
.close-button { color: var(--color-text-secondary); padding: 4px 8px; }
.edit-form { display: flex; flex-direction: column; gap: var(--space-3); padding: var(--space-4); label { display: flex; flex-direction: column; gap: var(--space-1); font-size: var(--text-sm); font-weight: var(--fw-medium); } input, select { width: 100%; padding: var(--space-2) var(--space-3); border: 1px solid var(--color-border); border-radius: var(--radius-md); background: var(--color-surface); color: var(--color-text); } }
.modal-actions { display: flex; justify-content: flex-end; gap: var(--space-2); margin-top: var(--space-2); }
</style>
