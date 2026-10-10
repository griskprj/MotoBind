<template>
  <div class="container">
    <LoadingOverlay :isLoading="loading" text="Загрузка заявок..."/>

    <Header
      title="Заявки"
      subtitle="Управляйте записями клиентов"
    />

    <div v-if="!business.hasAccount && !loading" class="empty">
      <i class="fa fa-info-circle"></i>
      <h3>Сначала создайте бизнес-аккаунт</h3>
      <router-link to="/business" class="btn-primary">Перейти в кабинет</router-link>
    </div>

    <div v-else>
      <div class="tabs">
        <button
          v-for="t in tabs"
          :key="t.id"
          class="tab"
          :class="{ active: activeTab === t.id }"
          @click="changeTab(t.id)"
        >
          {{ t.label }}
          <span v-if="tabCount(t.id)" class="tab-count">{{ tabCount(t.id) }}</span>
        </button>
      </div>

      <div v-if="filtered.length" class="bookings-grid">
        <BookingCard
          v-for="b in filtered"
          :key="b.id"
          :booking="b"
          view="master"
          @click="openDetails"
        />
      </div>

      <div v-else-if="!loading" class="empty">
        <i class="fa fa-calendar"></i>
        <h3>Нет заявок</h3>
        <p>{{ emptyText }}</p>
      </div>
    </div>

    <BookingDetailsModal
      :is-open="showDetails"
      :booking="selected"
      view="master"
      @close="showDetails = false"
      @changed="onChanged"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useBusinessStore, useBookingsStore } from '@/stores'
import { useToast } from '../../composables/useToast'
import { bookingTabList } from '../../utils/bookingHelpers'
import Header from '../../components/Header.vue'
import LoadingOverlay from '../../components/LoadingOverlay.vue'
import BookingCard from '../../components/bookings/BookingCard.vue'
import BookingDetailsModal from '../../components/modals/bookings/BookingDetailsModal.vue'

const toast = useToast()
const business = useBusinessStore()
const bookingsStore = useBookingsStore()

const { masterBookings, loadingMaster: loading } = storeToRefs(bookingsStore)

const tabs = bookingTabList()
const activeTab = ref('pending')

const showDetails = ref(false)
const selected = ref(null)

const filtered = computed(() => {
  if (activeTab.value === 'all') return masterBookings.value
  return masterBookings.value.filter((b) => b.status === activeTab.value)
})

const emptyText = computed(() => activeTab.value === 'pending'
  ? 'Новые заявки появятся здесь'
  : 'Нет заявок в этом статусе'
)

function tabCount(id) {
  return id === 'all'
    ? masterBookings.value.length
    : masterBookings.value.filter((b) => b.status === id).length
}

onMounted(async () => {
  try {
    if (!business.hasAccount) await business.loadAccount()
    if (business.hasAccount) {
      await bookingsStore.loadMasterBookings()
    }
  } catch {
    toast.error('Не удалось загрузить заявки')
  }
})

function changeTab(id) { activeTab.value = id }

function openDetails(b) {
  selected.value = b
  showDetails.value = true
}

function onChanged(updated) {
  const idx = masterBookings.value.findIndex((b) => b.id === updated.id)
  if (idx !== -1) masterBookings.value[idx] = updated
  showDetails.value = false
}
</script>

<style scoped>
.tabs {
  display: flex;
  gap: 4px;
  border-bottom: 1px solid var(--border-light);
  margin-bottom: 20px;
  overflow-x: auto;
  scrollbar-width: none;
  flex-wrap: wrap;
}
.tabs::-webkit-scrollbar { display: none; }

.tab {
  background: none;
  border: none;
  padding: 10px 14px;
  font-size: 13px;
  font-weight: var(--fw-medium);
  color: var(--text-muted);
  cursor: pointer;
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
  min-height: 40px;
}
.tab:hover { color: var(--text-primary); }
.tab.active { color: var(--accent-text); }
.tab.active::after {
  content: '';
  position: absolute;
  bottom: -1px; left: 0; right: 0;
  height: 2px;
  background: var(--accent);
  border-radius: 2px;
}
.tab-count {
  padding: 0 8px;
  border-radius: var(--radius-full);
  background: var(--bg-secondary);
  font-size: 11px;
  font-weight: var(--fw-semibold);
}
.tab.active .tab-count {
  background: var(--accent-trans);
  color: var(--accent-text);
}

.bookings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 12px;
}

.empty {
  text-align: center;
  padding: 60px 20px;
  background: var(--bg-card);
  border: 1px dashed var(--border-color);
  border-radius: var(--radius-lg);
}
.empty i { font-size: 42px; color: var(--accent-text); margin-bottom: 12px; display: block; }
.empty h3 { margin: 0 0 8px; }
.empty p { color: var(--text-secondary); margin: 0 0 20px; }
.empty .btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: var(--accent);
  color: #fff;
  border-radius: var(--radius-md);
  text-decoration: none;
  font-weight: var(--fw-semibold);
}
</style>
