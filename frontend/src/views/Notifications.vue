<template>
  <div class="container">
    <Header
        title="Уведомления"
        description="Напоминания о ТО, лайки, комментарии, подписки и решения о модерации ваших мануалов."
    />
    <div class="toolbar">
      <button @click="markAllRead" :disabled="!hasUnread" class="btn btn-secondary">
        Отметить все прочитанные
      </button>
    </div>
    <div v-if="loading" class="loading">Загрузка...</div>
    <div v-else-if="notifications.length === 0" class="empty-state">
      <i class="fas fa-bell-slash"></i>
      <p>У вас пока нет уведомлений</p>
    </div>
    <div v-else>
      <div v-for="notif in notifications" :key="notif.id" class="notification-item" :class="{ unread: !notif.is_read }">
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
            <button v-if="!notif.is_read" @click="markRead(notif.id)" class="btn btn-sm btn-outline">Прочитано</button>
            <button @click="deleteNotif(notif.id)" class="btn btn-sm btn-danger">Удалить</button>
            <button v-if="notif.link" @click="goToLink(notif)" class="btn btn-sm btn-primary">Перейти</button>
          </div>
        </div>
      </div>
      <div class="pagination">
        <button @click="prevPage" :disabled="page === 1" class="btn btn-sm btn-secondary">Назад</button>
        <span>Страница {{ page }} из {{ totalPages }}</span>
        <button @click="nextPage" :disabled="page === totalPages" class="btn btn-sm btn-secondary">Вперед</button>
      </div>
    </div>
  </div>
</template>

<script>
import notificationsApi from '../api/notifications'
import Header from '../components/Header.vue';

export default {
  data() {
    return {
      notifications: [],
      page: 1,
      perPage: 10,
      total: 0,
      pages: 0,
      loading: false,
    }
  },
  components: {Header},
  computed: {
    totalPages() { return this.pages },
    hasUnread() { return this.notifications.some(n => !n.is_read) }
  },
  mounted() {
    this.fetchNotifications()
  },
  methods: {
    async fetchNotifications() {
      this.loading = true
      try {
        const res = await notificationsApi.getNotifications(this.page, this.perPage, false)
        this.notifications = res.data.notifications
        this.total = res.data.total
        this.pages = res.data.pages
      } catch (e) {
        console.error('Ошибка загрузки уведомлений', e)
      } finally {
        this.loading = false
      }
    },
    async markRead(id) {
      try {
        await notificationsApi.markAsRead(id)
        const notif = this.notifications.find(n => n.id === id)
        if (notif) notif.is_read = true
      } catch (e) {
        console.error('Ошибка отметки прочитанным', e)
      }
    },
    async markAllRead() {
      try {
        await notificationsApi.markAllRead()
        this.notifications.forEach(n => n.is_read = true)
      } catch (e) {
        console.error('Ошибка', e)
      }
    },
    async deleteNotif(id) {
      if (!confirm('Удалить уведомление?')) return
      try {
        await notificationsApi.deleteNotification(id)
        this.notifications = this.notifications.filter(n => n.id !== id)
        this.total -= 1
        if (this.notifications.length === 0 && this.page > 1) {
          this.page -= 1
          this.fetchNotifications()
        }
      } catch (e) {
        console.error('Ошибка удаления', e)
      }
    },
    goToLink(notif) {
      if (!notif.is_read) {
        this.markRead(notif.id)
      }
      if (notif.link) {
        this.$router.push(notif.link)
      }
    },
    prevPage() {
      if (this.page > 1) {
        this.page--
        this.fetchNotifications()
      }
    },
    nextPage() {
      if (this.page < this.pages) {
        this.page++
        this.fetchNotifications()
      }
    },
    formatTime(dateStr) {
      const date = new Date(dateStr)
      return date.toLocaleString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
h1 {
  margin-bottom: 20px;
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
.btn-sm {
  padding: 4px 12px;
  font-size: 0.8rem;
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
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-muted);
}
.empty-state i {
  font-size: 3rem;
  margin-bottom: 16px;
}
</style>