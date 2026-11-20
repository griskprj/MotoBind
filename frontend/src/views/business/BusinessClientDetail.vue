<template>
  <div class="container">
    <LoadingOverlay :isLoading="loading" text="Загрузка клиента..."/>

    <div v-if="client" class="detail-page">
      <div class="page-top">
        <router-link to="/business/clients" class="back-link">
          <i class="fa fa-arrow-left"></i> К списку
        </router-link>
      </div>

      <Header :title="client.name" :subtitle="clientSubtitle"/>

      <div class="detail-grid">
        <!-- Левая колонка: инфо о клиенте -->
        <aside class="client-card">
          <div class="client-header">
            <div class="client-avatar-lg">
              <i class="fa fa-user"></i>
            </div>
            <h3>{{ client.name }}</h3>
          </div>

          <div class="info-list">
            <div v-if="client.phone" class="info-row">
              <span class="info-label">Телефон</span>
              <span class="info-value">{{ client.phone }}</span>
            </div>
            <div v-if="client.email" class="info-row">
              <span class="info-label">Email</span>
              <span class="info-value">{{ client.email }}</span>
            </div>
            <div v-if="client.note" class="info-row full">
              <span class="info-label">Заметка</span>
              <span class="info-value">{{ client.note }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Добавлен</span>
              <span class="info-value">{{ formatDate(client.created_at) }}</span>
            </div>
          </div>

          <!-- Блок связи -->
          <div class="link-status">
            <template v-if="client.user_id">
              <div class="link-badge linked">
                <i class="fa fa-check-circle"></i>
                Связан с аккаунтом
              </div>
              <button class="btn-link danger small" @click="askUnlink">
                <i class="fa fa-unlink"></i> Отвязать
              </button>
            </template>
            <template v-else>
              <div class="link-badge">
                <i class="fa fa-user-slash"></i>
                Не связан с аккаунтом
              </div>
              <button class="btn-link small" @click="showLinkModal = true">
                <i class="fa fa-link"></i> Связать
              </button>
            </template>
          </div>

          <BaseButton
            variant="secondary"
            block
            icon="fa fa-pen"
            @click="showEditClientModal = true"
          >
            Редактировать клиента
          </BaseButton>
        </aside>

        <!-- Правая колонка: мотоциклы -->
        <main class="vehicles-main">
          <div class="vehicles-header">
            <h4>
              <i class="fa fa-motorcycle"></i>
              Мотоциклы
              <span v-if="vehicles.length" class="count-badge">{{ vehicles.length }}</span>
            </h4>
            <BaseButton
              variant="primary"
              icon="fa fa-plus"
              @click="openCreateVehicle"
            >
              Добавить
            </BaseButton>
          </div>

          <div v-if="vehicles.length" class="vehicles-grid">
            <div
              v-for="v in vehicles"
              :key="v.id"
              class="vehicle-card"
            >
              <div class="vehicle-top">
                <div class="vehicle-icon">
                  <i class="fa fa-motorcycle"></i>
                </div>
                <div class="vehicle-title">
                  <div class="vehicle-name">{{ v.name }}</div>
                  <div class="vehicle-sub">
                    <span v-if="v.years">{{ v.years }}</span>
                    <span v-if="v.volume">· {{ v.volume }} см³</span>
                  </div>
                </div>
                <div class="vehicle-actions">
                  <button class="icon-btn" @click="openEditVehicle(v)">
                    <i class="fa fa-pen"></i>
                  </button>
                  <button class="icon-btn danger" @click="askDeleteVehicle(v)">
                    <i class="fa fa-trash"></i>
                  </button>
                </div>
              </div>

              <div class="vehicle-meta">
                <div class="meta-item">
                  <i class="fa fa-gauge-high"></i>
                  <span>{{ formatMileage(v.mileage) }}</span>
                </div>
                <div v-if="v.license_plate" class="meta-item">
                  <i class="fa fa-id-card"></i>
                  <span>{{ v.license_plate }}</span>
                </div>
                <div v-if="v.vin" class="meta-item vin">
                  <span class="vin-label">VIN</span>
                  <code>{{ v.vin }}</code>
                </div>
              </div>

              <div v-if="v.note" class="vehicle-note">{{ v.note }}</div>
            </div>
          </div>

          <div v-else class="empty-small">
            <i class="fa fa-motorcycle"></i>
            <p>У клиента пока нет мотоциклов</p>
            <BaseButton
              variant="primary"
              icon="fa fa-plus"
              @click="openCreateVehicle"
            >
              Добавить первый
            </BaseButton>
          </div>
        </main>
      </div>
    </div>

    <!-- Клиент не найден -->
    <div v-else-if="!loading" class="empty">
      <i class="fa fa-user-slash"></i>
      <h3>Клиент не найден</h3>
      <router-link to="/business/clients" class="btn-primary">
        К списку клиентов
      </router-link>
    </div>

    <!-- Модалки -->
    <ClientFormModal
      v-if="client"
      :is-open="showEditClientModal"
      :client="client"
      @close="showEditClientModal = false"
      @saved="onClientSaved"
    />

    <VehicleFormModal
      v-if="client"
      :is-open="showVehicleModal"
      :vehicle="editingVehicle"
      @close="closeVehicleModal"
      @saved="onVehicleSaved"
    />

    <ConfirmModal
      v-if="client"
      :is-open="showDeleteModal"
      title="Удалить мотоцикл?"
      :text="`Мотоцикл «${deletingVehicle?.name}» будет удалён.`"
      confirm-text="Удалить"
      variant="danger"
      @confirm="confirmDeleteVehicle"
      @close="showDeleteModal = false"
    />

    <LinkClientModal
      v-if="client"
      :is-open="showLinkModal"
      :client-id="clientId"
      :client-email="client.email"
      @close="showLinkModal = false"
      @linked="showLinkModal = false"
    />

    <ConfirmModal
      :is-open="showUnlinkModal"
      title="Отвязать клиента?"
      text="Клиент пропадёт из списка «Я клиент у мастеров» на своей стороне. Запись и мотоциклы останутся у вас."
      confirm-text="Отвязать"
      variant="danger"
      @confirm="confirmUnlink"
      @close="showUnlinkModal = false"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useBusinessStore } from '@/stores'
import { useToast } from '../../composables/useToast'
import { formatMileage } from '../../utils/formatters'
import formatDate from '../../utils/DateFormatter.js'
import Header from '../../components/Header.vue'
import LoadingOverlay from '../../components/LoadingOverlay.vue'
import { BaseButton } from '../../components/ui'
import ClientFormModal from '../../components/modals/business/ClientFormModal.vue'
import VehicleFormModal from '../../components/modals/business/VehicleFormModal.vue'
import ConfirmModal from '../../components/ui/ConfirmModal.vue'
import LinkClientModal from '@/components/modals/business/LinkClientModal.vue'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const business = useBusinessStore()

const { currentClient: client, currentClientLoading: loading } = storeToRefs(business)

const clientId = computed(() => Number(route.params.id))

const showEditClientModal = ref(false)
const showVehicleModal = ref(false)
const editingVehicle = ref(null)
const showDeleteModal = ref(false)
const deletingVehicle = ref(null)
const showLinkModal = ref(false)
const showUnlinkModal = ref(false)

const vehicles = computed(() => client.value?.vehicles || [])

const clientSubtitle = computed(() => {
  const c = client.value
  if (!c) return ''
  const parts = []
  if (c.phone) parts.push(c.phone)
  if (c.email) parts.push(c.email)
  return parts.join(' · ') || 'Клиент бизнес-аккаунта'
})

onMounted(async () => {
  try {
    if (!business.hasAccount) await business.loadAccount()
    await business.loadClient(clientId.value)
  } catch (err) {
    if (err.response?.status === 404) {
      // просто покажем empty state
    } else {
      toast.error('Не удалось загрузить клиента')
    }
  }
})

async function onClientSaved() {
  showEditClientModal.value = false
  await business.loadClient(clientId.value)
}

function openCreateVehicle() {
  editingVehicle.value = null
  showVehicleModal.value = true
}

function openEditVehicle(v) {
  editingVehicle.value = v
  showVehicleModal.value = true
}

function closeVehicleModal() {
  showVehicleModal.value = false
  editingVehicle.value = null
}

function onVehicleSaved() {
  closeVehicleModal()
  // currentClient обновляется самим стором
}

function askDeleteVehicle(v) {
  deletingVehicle.value = v
  showDeleteModal.value = true
}

async function confirmDeleteVehicle() {
  if (!deletingVehicle.value) return
  try {
    await business.deleteVehicle(clientId.value, deletingVehicle.value.id)
    toast.success('Мотоцикл удалён')
    showDeleteModal.value = false
    deletingVehicle.value = null
  } catch (err) {
    toast.error(err.response?.data?.error || 'Ошибка удаления')
  }
}

function askUnlink() {
  showUnlinkModal.value = true
}

async function confirmUnlink() {
  try {
    await business.unlinkClient(clientId.value)
    toast.success('Связь удалена')
    showUnlinkModal.value = false
  } catch (err) {
    toast.error(err.response?.data?.error || 'Ошибка')
  }
}
</script>

<style scoped>
.page-top { margin-bottom: 12px; }
.back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--text-secondary);
  text-decoration: none;
}
.back-link:hover { color: var(--accent-text); }

.detail-grid {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 24px;
  align-items: start;
}

/* === Client card === */
.client-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 24px;
  position: sticky;
  top: 24px;
}
.client-header { text-align: center; margin-bottom: 18px; }
.client-avatar-lg {
  width: 76px;
  height: 76px;
  border-radius: 50%;
  background: var(--accent-trans);
  color: var(--accent-text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
  margin: 0 auto 10px;
}
.client-header h3 { margin: 0; font-size: 18px; }

.info-list { display: flex; flex-direction: column; gap: 10px; margin-bottom: 18px; }
.info-row { display: flex; flex-direction: column; gap: 2px; }
.info-row.full { grid-column: 1 / -1; }
.info-label {
  font-size: 11px;
  font-weight: var(--fw-semibold);
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.4px;
}
.info-value {
  font-size: 14px;
  color: var(--text-primary);
  word-break: break-word;
}

/* === Link status === */
.link-status {
  display: flex;
  flex-direction: column;
  gap: 6px;
  align-items: center;
  padding: 10px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  margin-bottom: 14px;
}

.link-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-muted);
}
.link-badge.linked {
  color: var(--success-text);
}
.link-badge i { font-size: 14px; }

.btn-link.small {
  font-size: 12px;
  padding: 4px 10px;
  min-height: 28px;
}
.btn-link.danger { color: var(--danger-text); }

/* === Vehicles === */
.vehicles-main { min-width: 0; }
.vehicles-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 10px;
}
.vehicles-header h4 {
  margin: 0;
  font-size: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.vehicles-header h4 i { color: var(--accent-text); }
.count-badge {
  display: inline-block;
  padding: 1px 8px;
  border-radius: var(--radius-full);
  background: var(--accent-trans);
  color: var(--accent-text);
  font-size: 11px;
  font-weight: var(--fw-semibold);
}

.vehicles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
}
.vehicle-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 16px 18px;
  transition: all var(--transition-base);
}
.vehicle-card:hover { border-color: var(--accent); box-shadow: var(--shadow-sm); }

.vehicle-top {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}
.vehicle-icon {
  width: 42px;
  height: 42px;
  min-height: 42px;
  border-radius: var(--radius-md);
  background: var(--accent-trans);
  color: var(--accent-text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}
.vehicle-title { flex: 1; min-width: 0; }
.vehicle-name {
  font-size: 14px;
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.vehicle-sub { font-size: 12px; color: var(--text-muted); }
.vehicle-actions { display: flex; gap: 2px; flex-shrink: 0; }

.vehicle-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  font-size: 12px;
  color: var(--text-muted);
}
.meta-item {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
.meta-item.vin {
  flex-basis: 100%;
  gap: 6px;
  padding-top: 6px;
  border-top: 1px solid var(--border-light);
}
.vin-label {
  font-size: 10px;
  font-weight: var(--fw-semibold);
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: var(--text-muted);
}
.meta-item code {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--text-primary);
  background: var(--bg-secondary);
  padding: 1px 6px;
  border-radius: var(--radius-sm);
}

.vehicle-note {
  margin-top: 8px;
  font-size: 12px;
  color: var(--text-secondary);
  padding: 6px 10px;
  background: var(--bg-secondary);
  border-radius: var(--radius-sm);
  line-height: 1.4;
}

.empty-small {
  text-align: center;
  padding: 40px 20px;
  background: var(--bg-card);
  border: 1px dashed var(--border-color);
  border-radius: var(--radius-lg);
}
.empty-small i { font-size: 36px; color: var(--text-muted); margin-bottom: 10px; display: block; }
.empty-small p { color: var(--text-secondary); margin: 0 0 14px; }

.icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  min-height: 34px;
  padding: 0;
  border: none;
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  transition: all var(--transition-base);
  font-size: 13px;
}
.icon-btn:hover { background: var(--border-light); color: var(--text-primary); }
.icon-btn.danger:hover { background: var(--danger-trans); color: var(--danger-text); }

.empty {
  text-align: center;
  padding: 60px 20px;
  background: var(--bg-card);
  border: 1px dashed var(--border-color);
  border-radius: var(--radius-lg);
}
.empty i { font-size: 42px; color: var(--text-muted); margin-bottom: 12px; display: block; }
.empty h3 { margin: 0 0 16px; }
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

@media (max-width: 900px) {
  .detail-grid { grid-template-columns: 1fr; }
  .client-card { position: static; }
}
@media (max-width: 640px) {
  .vehicles-grid { grid-template-columns: 1fr; }
}
</style>
