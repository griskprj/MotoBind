<template>
  <div class="notification-bell" @click="toggleDropdown" ref="bellRef">
    <i class="fas fa-bell"></i>
    <span v-if="unreadCount > 0" class="badge">{{ unreadCount }}</span>

    <Teleport to="body">
      <div v-if="dropdownOpen" class="dropdown-overlay" @click="closeDropdown">
        <div class="dropdown" ref="dropdownRef" @click.stop>
          <div class="dropdown-header">
            <span>Уведомления</span>
            <button
              v-if="unreadCount > 0"
              @click.stop="handleMarkAllRead"
              class="mark-all-read"
            >
              Все прочитано
            </button>
          </div>
          <div v-if="loading" class="loading">Загрузка...</div>
          <div v-else-if="items.length === 0" class="empty">Нет уведомлений</div>
          <ul v-else>
            <li
              v-for="notif in items"
              :key="notif.id"
              :class="{ unread: !notif.is_read }"
              @click="goToLink(notif)"
            >
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

<script setup>
import { nextTick,onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useNotificationsStore } from '@/stores'

const router = useRouter()
const notificationsStore = useNotificationsStore()

const { items, unreadCount, loading } = storeToRefs(notificationsStore)

const bellRef = ref(null)
const dropdownOpen = ref(false)
const dropdownRef = ref(null)

// ===== Lifecycle =====
onMounted(() => {
  notificationsStore.startPolling()
  document.addEventListener('click', closeDropdownOutside)
})

onBeforeUnmount(() => {
  notificationsStore.stopPolling()
  document.removeEventListener('click', closeDropdownOutside)
})

// ===== Actions =====
async function toggleDropdown(event) {
  event.stopPropagation()
  dropdownOpen.value = !dropdownOpen.value
  if (dropdownOpen.value) {
    try {
      await notificationsStore.loadRecent(5)
    } catch (err) {
      console.error('Failed to load recent notifications:', err)
    }
    await nextTick()
    positionDropdown()
  }
}

async function handleMarkAllRead() {
  try {
    await notificationsStore.markAllRead()
  } catch (err) {
    console.error('Failed to mark all read:', err)
  }
}

function goToLink(notif) {
  if (!notif.is_read) {
    notificationsStore.markAsRead(notif.id).catch(() => {})
  }
  if (notif.link) {
    router.push(notif.link)
  }
  dropdownOpen.value = false
}

function closeDropdownOutside(e) {
  if (dropdownOpen.value && bellRef.value && !bellRef.value.contains(e.target)) {
    dropdownOpen.value = false
  }
}

function closeDropdown() {
  dropdownOpen.value = false
}

function positionDropdown() {
  const bell = bellRef.value
  const dropdown = dropdownRef.value
  if (!bell || !dropdown) return

  const rect = bell.getBoundingClientRect()
  const dropdownWidth = 320
  const left = Math.min(rect.right - dropdownWidth, window.innerWidth - 20)

  dropdown.style.position = 'fixed'
  dropdown.style.top = (rect.bottom + 8) + 'px'
  dropdown.style.left = Math.max(10, left) + 'px'
  dropdown.style.width = dropdownWidth + 'px'
  dropdown.style.right = 'auto'  // ← важно: сбросить CSS right
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
