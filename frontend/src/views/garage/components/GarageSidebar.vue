<template>
  <aside class="garage-sidebar">
    <!-- Запись к мастеру -->
    <div class="sidebar-card appointment-card">
      <div class="sidebar-card-header">
        <i class="fa fa-calendar-plus"></i>
        <h4>Запись к мастеру</h4>
      </div>

      <div class="appointment-success">
        <p>Запишитесь к проверенному мастеру в вашем городе.</p>
      </div>

      <router-link class="btn-primary appointment-submit" to="/masters">
        <i class="fa fa-search"></i>
        Найти мастера
      </router-link>
    </div>

    <!-- Я клиент у мастеров -->
    <div v-if="myMasters.length > 0" class="sidebar-card my-masters-card">
      <div class="sidebar-card-header">
        <i class="fa fa-user-tie"></i>
        <h4>Я клиент у мастеров</h4>
      </div>

      <div class="master-list-mini">
        <div
          v-for="m in myMasters"
          :key="m.client_id"
          class="master-mini-item"
        >
          <div class="master-mini-avatar">
            <img
              v-if="m.business?.logo_url"
              :src="getBusinessLogoUrl(m.business.logo_url)"
              alt=""
              @error="(e) => (e.target.style.display = 'none')"
            >
            <i
              v-else
              class="fa"
              :class="m.business?.type === 'station' ? 'fa-warehouse' : 'fa-user-gear'"
            ></i>
          </div>
          <div class="master-mini-body">
            <div class="master-mini-name">{{ m.business?.name || 'Мастер' }}</div>
            <div class="master-mini-meta">
              <span v-if="m.business?.city">
                <i class="fa fa-map-marker"></i> {{ m.business.city }}
              </span>
              <span v-if="m.vehicles?.length">
                <i class="fa fa-motorcycle"></i> {{ m.vehicles.length }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <router-link to="/masters" class="btn-outline discover-masters">
        <i class="fa fa-search"></i> Найти мастера
      </router-link>
    </div>

    <!-- Совет дня -->
    <div class="sidebar-card tip-card">
      <div class="sidebar-card-header">
        <i class="fa fa-lightbulb"></i>
        <h4>Совет дня</h4>
      </div>
      <p class="tip-text">{{ tip }}</p>
      <button class="btn-link small" @click="emit('refresh-tip')">
        <i class="fa fa-rotate-right"></i>
        Другой совет
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { getBusinessLogoUrl } from '@/utils/mediaUrl'

defineProps<{
  myMasters: any[]
  tip: string
}>()

const emit = defineEmits<{ 'refresh-tip': [] }>()
</script>

<style scoped>
.garage-sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
  position: sticky;
  top: 24px;
}

/* ============================================
   SIDEBAR CARD
   ============================================ */
.sidebar-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 18px 20px;
  transition: all var(--transition-base);
}

.sidebar-card:hover {
  border-color: var(--border-color);
}

.sidebar-card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}

.sidebar-card-header i {
  color: var(--accent-text);
  font-size: 16px;
}

.sidebar-card-header h4 {
  font-size: 14px;
  font-weight: var(--fw-semibold);
  margin: 0;
}

/* ============================================
   APPOINTMENT
   ============================================ */
.appointment-success {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 8px;
  padding: 8px 0;
  margin-bottom: 12px;
}

.appointment-success p {
  margin: 0;
  font-size: 13px;
  color: var(--text-secondary);
}

.appointment-submit {
  width: 100%;
  padding: 10px 16px;
  border-radius: var(--radius-md);
  background: var(--accent);
  color: #fff;
  border: none;
  font-size: 13px;
  font-weight: var(--fw-semibold);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all var(--transition-base);
  min-height: 40px;
  text-decoration: none;
}

.appointment-submit:hover {
  background: var(--accent-hover);
  transform: translateY(-1px);
  color: #fff;
}

/* ============================================
   MY MASTERS
   ============================================ */
.my-masters-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.master-list-mini {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.master-mini-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  background: var(--bg-primary);
  border-radius: var(--radius-md);
  transition: all var(--transition-base);
}

.master-mini-item:hover {
  background: var(--bg-card-hover);
}

.master-mini-avatar {
  width: 36px;
  height: 36px;
  min-height: 36px;
  border-radius: 50%;
  background: var(--accent-trans);
  color: var(--accent-text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
  overflow: hidden;
  flex-shrink: 0;
}

.master-mini-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.master-mini-body {
  flex: 1;
  min-width: 0;
}

.master-mini-name {
  font-size: 13px;
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.master-mini-meta {
  display: flex;
  gap: 10px;
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 2px;
}

.master-mini-meta span {
  display: inline-flex;
  align-items: center;
  gap: 3px;
}

.discover-masters {
  width: 100%;
  padding: 10px 16px;
  background: transparent;
  border: 1px solid var(--accent);
  color: var(--accent);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
  font-weight: var(--fw-medium);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 13px;
  text-decoration: none;
  min-height: 40px;
}

.discover-masters:hover {
  background: var(--accent);
  color: #fff;
}

/* ============================================
   TIP
   ============================================ */
.tip-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tip-text {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
  margin: 0;
}

.btn-link {
  background: none;
  border: none;
  color: var(--accent-text);
  font-weight: var(--fw-medium);
  font-size: 13px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all var(--transition-base);
  padding: 6px 12px;
  border-radius: var(--radius-md);
  min-height: 32px;
}

.btn-link:hover {
  color: var(--accent);
  gap: 10px;
  background: var(--accent-trans);
}

.btn-link.small {
  font-size: 12px;
  padding: 4px 8px;
}

@media (max-width: 1100px) {
  .garage-sidebar {
    position: static;
  }
}
</style>
