<template>
  <div class="container">
    <Header
      title="Уведомления"
      subtitle="Напоминания о ТО, лайки, комментарии, подписки и решения о модерации ваших мануалов."
    />

    <div class="toolbar">
      <BaseButton
        variant="secondary"
        :disabled="!hasUnread"
        @click="handleMarkAllRead"
      >
        Отметить все прочитанные
      </BaseButton>
    </div>

    <div v-if="loading" class="loading">Загрузка...</div>

    <BaseEmptyState
      v-else-if="items.length === 0"
      icon="fa fa-bell-slash"
      title="У вас пока нет уведомлений"
    />

    <div v-else>
      <div
        v-for="notif in items"
        :key="notif.id"
        class="notification-item"
        :class="{ unread: !notif.is_read }"
      >
        <div class="notif-icon">
          <i v-if="notif.type === 'manual_status'" class="fas fa-file-alt"></i>
          <i v-else-if="notif.type === 'social'" class="fas fa-users"></i>
          <i v-else class="fas fa-bell"></i>
        </div>
        <div class="notif-body">
          <div class="notif-header">
            <span class="notif-title">{{ notif.title }}</span>
            <span class="notif-time">{{ formatTime(notif.created_at) }}</span>
          </div>
          <p class="notif-content">{{ notif.content }}</p>
          <div class="notif-actions">
            <BaseButton
              v-if="!notif.is_read"
              variant="outline"
              size="sm"
              @click="handleMarkRead(notif.id)"
            >
              Прочитано
            </BaseButton>
            <BaseButton
              variant="danger"
              size="sm"
              @click="handleDelete(notif.id)"
            >
              Удалить
            </BaseButton>
            <BaseButton
              v-if="notif.link"
              variant="primary"
              size="sm"
              @click="goToLink(notif)"
            >
              Перейти
            </BaseButton>
          </div>
        </div>
      </div>

      <div class="pagination">
        <BaseButton
          variant="secondary"
          size="sm"
          :disabled="pagination.current_page === 1"
          @click="prevPage"
        >
          Назад
        </BaseButton>
        <span>Страница {{ pagination.current_page }} из {{ pagination.pages || 1 }}</span>
        <BaseButton
          variant="secondary"
          size="sm"
          :disabled="pagination.current_page === pagination.pages"
          @click="nextPage"
        >
          Вперед
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useNotificationsStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import { BaseButton, BaseEmptyState } from '@/components/ui'

import Header from '../components/Header.vue'

const router = useRouter()
const toast = useToast()
const notificationsStore = useNotificationsStore()

const { items, loading, pagination, hasUnread } = storeToRefs(notificationsStore)

// ===== Lifecycle =====
onMounted(async () => {
  try {
    await notificationsStore.loadList(pagination.value.current_page || 1)
  } catch (err) {
    console.error('Failed to load notifications:', err)
    toast.error('Не удалось загрузить уведомления')
  }
})

// ===== Actions =====
async function handleMarkRead(id) {
  try {
    await notificationsStore.markAsRead(id)
  } catch (err) {
    console.error('Failed to mark as read:', err)
    toast.error('Не удалось отметить уведомление')
  }
}

async function handleMarkAllRead() {
  try {
    await notificationsStore.markAllRead()
    toast.success('Все уведомления отмечены как прочитанные')
  } catch (err) {
    console.error('Failed to mark all read:', err)
    toast.error('Не удалось отметить уведомления')
  }
}

async function handleDelete(id) {
  if (!confirm('Удалить уведомление?')) return
  try {
    await notificationsStore.remove(id)
    // Если удалили последний на странице и она не первая — перейти на предыдущую
    if (items.value.length === 0 && pagination.value.current_page > 1) {
      await notificationsStore.loadList(pagination.value.current_page - 1)
    }
  } catch (err) {
    console.error('Failed to delete notification:', err)
    toast.error('Не удалось удалить уведомление')
  }
}

async function goToLink(notif) {
  if (!notif.is_read) {
    notificationsStore.markAsRead(notif.id).catch(() => {})
  }
  if (notif.link) {
    router.push(notif.link)
  }
}

async function prevPage() {
  if (pagination.value.current_page > 1) {
    await notificationsStore.loadList(pagination.value.current_page - 1)
  }
}

async function nextPage() {
  if (pagination.value.current_page < pagination.value.pages) {
    await notificationsStore.loadList(pagination.value.current_page + 1)
  }
}

function formatTime(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.notification-item {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: var(--bg-card);
  border-radius: 12px;
  margin-bottom: 12px;
  border: 1px solid var(--border-color);
  transition: background 0.2s;
}

.notification-item.unread {
  border-left: 4px solid var(--accent);
  background: var(--accent-trans);
}

.notif-icon {
  font-size: 1.5rem;
  color: var(--accent);
}

.notif-body {
  flex: 1;
}

.notif-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notif-title {
  font-weight: 600;
}

.notif-time {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.notif-content {
  margin: 8px 0 12px;
  color: var(--text-secondary);
}

.notif-actions {
  display: flex;
  gap: 8px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 24px;
}

.loading {
  text-align: center;
  padding: 40px;
  color: var(--text-muted);
}
</style>
