<template>
  <div class="notification-bell" @click="toggleDropdown" ref="bellRef">
    <i class="fas fa-bell"></i>
    <span v-if="unreadCount > 0" class="badge">{{ unreadCount }}</span>
    
    <Teleport to="body">
      <div v-if="dropdownOpen" class="dropdown-overlay" @click="closeDropdown">
        <div class="dropdown" @click.stop>
          <div class="dropdown-header">
            <span>Уведомления</span>
            <button v-if="unreadCount > 0" @click.stop="markAllRead" class="mark-all-read">Все прочитано</button>
          </div>
          <div v-if="loading" class="loading">Загрузка...</div>
          <div v-else-if="notifications.length === 0" class="empty">Нет уведомлений</div>
          <ul v-else>
            <li v-for="notif in notifications" :key="notif.id" :class="{ unread: !notif.is_read }" @click="goToLink(notif)">
              <div class="notif-content">
                <div class="notif-title">{{ notif.title }}</div>
                <div class="notif-text">{{ notif.content }}</div>
                <span class="notif-time">{{ formatTime(notif.created_at) }}</span>
              </div>
            </li>
          </ul>
          <div class="dropdown-footer">
            <router-link to="/notifications">Все уведомления</router-link>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script>
import notificationsApi from '../api/notifications'

export default {
  data() {
    return {
      dropdownOpen: false,
      unreadCount: 0,
      notifications: [],
      loading: false,
      timer: null,
    }
  },
  mounted() {
    this.fetchUnreadCount()
    this.timer = setInterval(this.fetchUnreadCount, 30000)
    document.addEventListener('click', this.closeDropdownOutside)
  },
  beforeUnmount() {
    clearInterval(this.timer)
    document.removeEventListener('click', this.closeDropdownOutside)
  },
  methods: {
    async fetchUnreadCount() {
      try {
        const res = await notificationsApi.getUnreadCount()
        this.unreadCount = res.data.unread_count
      } catch (e) {
        console.error('Ошибка получения количества уведомлений', e)
      }
    },
    async toggleDropdown(event) {
      event.stopPropagation()
      this.dropdownOpen = !this.dropdownOpen
      if (this.dropdownOpen) {
        await this.fetchNotifications()
        this.$nextTick(() => {
          this.positionDropdown()
        })
      }
    },
    positionDropdown() {
      const bell = this.$refs.bellRef
      const dropdown = document.querySelector('.dropdown')
      if (!bell || !dropdown) return
      
      const rect = bell.getBoundingClientRect()
      const dropdownWidth = 320
      const left = Math.min(rect.right - dropdownWidth, window.innerWidth - 20)
      
      dropdown.style.position = 'fixed'
      dropdown.style.top = (rect.bottom + 8) + 'px'
      dropdown.style.left = Math.max(10, left) + 'px'
      dropdown.style.width = dropdownWidth + 'px'
    },
    async fetchNotifications() {
      this.loading = true
      try {
        const res = await notificationsApi.getNotifications(1, 5, false)
        this.notifications = res.data.notifications
      } catch (e) {
        console.error('Ошибка загрузки уведомлений', e)
      } finally {
        this.loading = false
      }
    },
    async markAllRead() {
      try {
        await notificationsApi.markAllRead()
        this.unreadCount = 0
        this.notifications.forEach(n => n.is_read = true)
      } catch (e) {
        console.error('Ошибка отметки всех прочитанных', e)
      }
    },
    goToLink(notif) {
      if (!notif.is_read) {
        notificationsApi.markAsRead(notif.id).catch(() => {})
        notif.is_read = true
        this.unreadCount = Math.max(0, this.unreadCount - 1)
      }
      if (notif.link) {
        this.$router.push(notif.link)
      }
      this.dropdownOpen = false
    },
    closeDropdownOutside(e) {
      if (this.dropdownOpen && !this.$refs.bellRef.contains(e.target)) {
        this.dropdownOpen = false
      }
    },
    closeDropdown() {
      this.dropdownOpen = false
    },
    formatTime(dateStr) {
      const date = new Date(dateStr)
      return date.toLocaleString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
    }
  }
}
</script>

<style scoped>
.notification-bell {
  position: relative;
  display: inline-block;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 8px;
}

.badge {
  position: absolute;
  top: 0;
  right: 0;
  background: #ef4444;
  color: white;
  border-radius: 50%;
  padding: 2px 6px;
  font-size: 0.7rem;
  min-width: 18px;
  text-align: center;
}

.dropdown-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 99999;
}

.dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  width: 320px;
  max-height: 400px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  z-index: 100000;
  overflow-y: auto;
}

.dropdown-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-color);
  font-weight: 600;
}

.mark-all-read {
  background: none;
  border: none;
  color: var(--accent);
  cursor: pointer;
  font-size: 0.8rem;
  padding: 4px 8px;
  border-radius: 4px;
}

.mark-all-read:hover {
  background: var(--accent-trans);
}

.dropdown ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.dropdown li {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-light);
  cursor: pointer;
  transition: background 0.2s;
}

.dropdown li:hover {
  background: var(--bg-card-hover);
}

.dropdown li.unread {
  background: var(--accent-trans);
  border-left: 3px solid var(--accent);
}

.notif-title {
  font-weight: 500;
  margin-bottom: 4px;
}

.notif-text {
  font-size: 0.85rem;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.notif-time {
  font-size: 0.7rem;
  color: var(--text-muted);
  margin-top: 4px;
  display: block;
}

.dropdown-footer {
  padding: 10px 16px;
  text-align: center;
  border-top: 1px solid var(--border-color);
}

.dropdown-footer a {
  color: var(--accent);
  text-decoration: none;
  font-size: 0.9rem;
}

.dropdown-footer a:hover {
  text-decoration: underline;
}

.loading, .empty {
  padding: 24px 16px;
  text-align: center;
  color: var(--text-muted);
}
</style>