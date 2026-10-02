<template>
  <div v-if="isAuthenticated" class="notification-bell" @click="toggleDropdown" ref="bellRef">
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
            <router-link to="/notifications" @click="closeDropdown">
              Все уведомления
            </router-link>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useNotificationsStore, useAuthStore } from '@/stores'

const router = useRouter()
const notificationsStore = useNotificationsStore()
const authStore = useAuthStore()

const { items, unreadCount, loading } = storeToRefs(notificationsStore)

const isAuthenticated = computed(() => authStore.isAuthenticated)

const bellRef = ref(null)
const dropdownOpen = ref(false)
const dropdownRef = ref(null)

// ===== Lifecycle =====
onMounted(() => {
  if (isAuthenticated.value) {
    notificationsStore.startPolling()
  }
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  notificationsStore.stopPolling()
  window.removeEventListener('resize', handleResize)
})

// Перезапуск/остановка polling при смене авторизации
watch(isAuthenticated, (val) => {
  if (val) {
    notificationsStore.startPolling()
  } else {
    notificationsStore.stopPolling()
    dropdownOpen.value = false
  }
})

// ===== Actions =====
async function toggleDropdown(event) {
  event.stopPropagation()

  if (!isAuthenticated.value) {
    router.push('/login')
    return
  }

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

function closeDropdown() {
  dropdownOpen.value = false
}

function positionDropdown() {
  const bell = bellRef.value
  const dropdown = dropdownRef.value
  if (!bell || !dropdown) return

  const rect = bell.getBoundingClientRect()
  const dropdownWidth = Math.min(320, window.innerWidth - 24)
  const left = Math.min(rect.right - dropdownWidth, window.innerWidth - dropdownWidth - 12)

  dropdown.style.position = 'fixed'
  dropdown.style.top = `${rect.bottom + 8}px`
  dropdown.style.left = `${Math.max(12, left)}px`
  dropdown.style.width = `${dropdownWidth}px`
  dropdown.style.right = 'auto'
}

function handleResize() {
  if (dropdownOpen.value) {
    positionDropdown()
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
.notification-bell {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 8px;
  min-width: 40px;
  min-height: 40px;
  border-radius: 50%;
  color: var(--text-primary);
  transition: background var(--transition-fast, 0.15s ease);
}

.notification-bell:hover {
  background: var(--border-light);
}

.badge {
  position: absolute;
  top: 2px;
  right: 2px;
  background: #ef4444;
  color: #fff;
  border-radius: 10px;
  padding: 1px 6px;
  font-size: 0.65rem;
  font-weight: 600;
  min-width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  box-shadow: 0 0 0 2px var(--bg-primary);
}

.dropdown-overlay {
  position: fixed;
  inset: 0;
  z-index: 99999;
}

.dropdown {
  width: 320px;
  max-height: min(420px, 80vh);
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  box-shadow: var(--shadow-lg, 0 10px 40px rgba(0, 0, 0, 0.25));
  z-index: 100000;
  overflow-y: auto;
  overscroll-behavior: contain;
}

.dropdown-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-color);
  font-weight: 600;
  position: sticky;
  top: 0;
  background: var(--bg-card);
  z-index: 1;
}

.mark-all-read {
  background: none;
  border: none;
  color: var(--accent);
  cursor: pointer;
  font-size: 0.8rem;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background var(--transition-fast, 0.15s ease);
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
  transition: background var(--transition-fast, 0.15s ease);
}

.dropdown li:last-child {
  border-bottom: none;
}

.dropdown li:hover {
  background: var(--bg-card-hover);
}

.dropdown li.unread {
  background: var(--accent-trans);
  border-left: 3px solid var(--accent);
  padding-left: 13px;
}

.notif-title {
  font-weight: 500;
  margin-bottom: 4px;
  color: var(--text-primary);
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
  position: sticky;
  bottom: 0;
  background: var(--bg-card);
}

.dropdown-footer a {
  color: var(--accent);
  text-decoration: none;
  font-size: 0.9rem;
}

.dropdown-footer a:hover {
  text-decoration: underline;
}

.loading,
.empty {
  padding: 24px 16px;
  text-align: center;
  color: var(--text-muted);
  font-size: 0.9rem;
}

/* ===== Адаптив ===== */
@media (max-width: 480px) {
  .dropdown {
    width: calc(100vw - 24px);
    max-width: 340px;
  }

  .notif-text {
    white-space: normal;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
}
</style>
