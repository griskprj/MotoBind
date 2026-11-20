<script setup lang="ts">
import type { Notification } from '~/types'

definePageMeta({ middleware: 'auth' })

useSeoMeta({ title: 'Уведомления', robots: 'noindex' })

const api = useApi()
const toast = useToast()

const notifications = ref<Notification[]>([])
const pending = ref(false)
const unreadOnly = ref(false)
const page = ref(1)
const totalPages = ref(1)

async function loadNotifications() {
  pending.value = true
  try {
    const res = await api.notifications.list({
      page: page.value,
      per_page: 20,
      unread_only: unreadOnly.value || undefined,
    })
    notifications.value = res.notifications
    totalPages.value = res.pages
  } catch (e) {
    toast.error('Не удалось загрузить уведомления')
  } finally {
    pending.value = false
  }
}

onMounted(loadNotifications)
watch([unreadOnly, page], loadNotifications)

// Пометить как прочитанное
async function markRead(n: Notification) {
  if (n.is_read) return
  try {
    await api.notifications.markRead(n.id)
    n.is_read = true
    toast.success('Отмечено прочитанным')
  } catch (e) {
    toast.error('Ошибка')
  }
}

// Пометить все
async function markAllRead() {
  try {
    await api.notifications.markAllRead()
    notifications.value.forEach(n => n.is_read = true)
    toast.success('Все уведомления прочитаны')
  } catch (e) {
    toast.error('Ошибка')
  }
}

// Удалить
async function removeNotification(n: Notification) {
  if (!confirm('Удалить уведомление?')) return
  try {
    await api.notifications.remove(n.id)
    notifications.value = notifications.value.filter(x => x.id !== n.id)
    toast.success('Удалено')
  } catch (e) {
    toast.error('Ошибка')
  }
}

// Иконки по типу
const typeIcons: Record<string, string> = {
  system: 'fa-solid fa-bell',
  manual_status: 'fa-solid fa-book',
  social: 'fa-solid fa-comment',
  report_status: 'fa-solid fa-flag',
  moderation: 'fa-solid fa-gavel',
  maintenance: 'fa-solid fa-wrench',
}

// Форматирование даты
const formatDate = (iso: string) => {
  return new Date(iso).toLocaleString('ru-RU', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })
}
</script>

<template>
  <div class="notifications-page">
    <header class="page-header">
      <div>
        <h1 class="page-title">Уведомления</h1>
        <p class="page-subtitle">Ваши оповещения</p>
      </div>
      <BaseButton variant="secondary" size="sm" @click="markAllRead">
        <i class="fa-solid fa-check-double"></i> Прочитать все
      </BaseButton>
    </header>

    <!-- Фильтр -->
    <div class="filters">
      <label class="checkbox-label">
        <input type="checkbox" v-model="unreadOnly" />
        Только непрочитанные
      </label>
    </div>

    <!-- Загрузка -->
    <div v-if="pending" class="loading">
      <BaseSkeleton height="80px" rounded v-for="i in 3" :key="i" />
    </div>

    <!-- Пусто -->
    <div v-else-if="notifications.length === 0" class="empty">
      <i class="fa-solid fa-bell-slash"></i>
      <p>Нет уведомлений</p>
    </div>

    <!-- Список -->
    <div v-else class="notifications-list">
      <div
        v-for="n in notifications"
        :key="n.id"
        class="notification-item"
        :class="{ 'notification-item--unread': !n.is_read }"
      >
        <div class="notif-icon">
          <i :class="typeIcons[n.type] || 'fa-solid fa-bell'"></i>
        </div>

        <div class="notif-content">
          <div class="notif-header">
            <h3 class="notif-title">{{ n.title }}</h3>
            <span class="notif-date">{{ formatDate(n.created_at) }}</span>
          </div>
          <p class="notif-text">{{ n.content }}</p>

          <div class="notif-footer">
            <NuxtLink v-if="n.link" :to="n.link" class="notif-link">Перейти →</NuxtLink>
            <div class="notif-actions">
              <BaseButton
                v-if="!n.is_read"
                variant="ghost"
                size="sm"
                title="Отметить прочитанным"
                @click="markRead(n)"
              >
                <i class="fa-solid fa-check"></i>
              </BaseButton>
              <BaseButton
                variant="ghost"
                size="sm"
                title="Удалить"
                @click="removeNotification(n)"
              >
                <i class="fa-solid fa-trash"></i>
              </BaseButton>
            </div>
          </div>
        </div>
      </div>
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
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.notifications-page {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-3);
  flex-wrap: wrap;
}
.page-title { font-size: var(--text-2xl); font-weight: var(--fw-bold); }
.page-subtitle { color: var(--color-text-secondary); margin-top: var(--space-1); }

.filters { display: flex; gap: var(--space-3); }
.checkbox-label { display: flex; align-items: center; gap: var(--space-2); font-size: var(--text-sm); cursor: pointer; }

.loading { display: flex; flex-direction: column; gap: var(--space-3); }
.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-10);
  color: var(--color-text-tertiary);
  background: var(--color-surface-secondary);
  border-radius: var(--radius-md);
  i { font-size: 48px; opacity: 0.5; }
}

.notifications-list { display: flex; flex-direction: column; gap: var(--space-3); }

.notification-item {
  display: flex;
  gap: var(--space-3);
  padding: var(--space-4);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  transition: background var(--transition-fast);

  &--unread {
    background: var(--color-brand-soft);
    border-color: var(--color-brand);
  }
}

.notif-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--color-surface-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-brand);
  font-size: 18px;
  flex-shrink: 0;
}

.notif-content { flex: 1; min-width: 0; }
.notif-header { display: flex; justify-content: space-between; align-items: flex-start; gap: var(--space-2); margin-bottom: var(--space-1); }
.notif-title { font-size: var(--text-base); font-weight: var(--fw-semibold); }
.notif-date { font-size: var(--text-xs); color: var(--color-text-tertiary); white-space: nowrap; }
.notif-text { font-size: var(--text-sm); color: var(--color-text-secondary); line-height: var(--leading-relaxed); }
.notif-link { margin-top: var(--space-2); font-size: var(--text-sm); }
.notif-link a { color: var(--color-brand); text-decoration: none; &:hover { text-decoration: underline; } }
.notification-item {
  display: flex;
  gap: var(--space-3);
  padding: var(--space-4);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  transition: background var(--transition-fast);

  &--unread {
    background: var(--color-brand-soft);
    border-color: var(--color-brand);
  }
}

.notif-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--color-surface-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-brand);
  font-size: 18px;
  flex-shrink: 0;
}

.notif-content {
  flex: 1;
  min-width: 0; /* Важно, чтобы текст не вылезал */
  display: flex;
  flex-direction: column;
}

.notif-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-2);
  margin-bottom: var(--space-1);
}

.notif-title {
  font-size: var(--text-base);
  font-weight: var(--fw-semibold);
  line-height: var(--leading-tight);
  word-break: break-word; /* Чтобы длинные слова переносились */
}

.notif-date {
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
  white-space: nowrap;
  flex-shrink: 0;
}

.notif-text {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  line-height: var(--leading-relaxed);
  margin-bottom: var(--space-3);
  word-break: break-word;
}

/* Футер с ссылкой и действиями */
.notif-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-2);
  margin-top: auto; /* Прижимает к низу */
}

.notif-link {
  font-size: var(--text-sm);
  color: var(--color-brand);
  text-decoration: none;
  font-weight: var(--fw-medium);

  &:hover {
    text-decoration: underline;
  }
}

.notif-actions {
  display: flex;
  gap: var(--space-1);
  flex-shrink: 0;
}
.notif-actions { display: flex; gap: var(--space-1); flex-shrink: 0; align-items: flex-start; }

.pagination { display: flex; justify-content: center; align-items: center; gap: var(--space-3); }
</style>
