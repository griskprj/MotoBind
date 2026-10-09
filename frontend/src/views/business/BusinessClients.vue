<template>
  <div class="container">
    <LoadingOverlay :isLoading="loading" text="Загрузка клиентов..."/>

    <Header title="Мои клиенты" subtitle="Управляйте базой клиентов"/>

    <!-- Если нет бизнес-аккаунта — редирект на дашборд -->
    <div v-if="!business.hasAccount && !loading" class="no-account">
      <i class="fa fa-info-circle"></i>
      <p>Сначала создайте бизнес-аккаунт</p>
      <router-link to="/business" class="btn-primary">Перейти в кабинет</router-link>
    </div>

    <div v-else-if="business.hasAccount" class="clients-page">
      <!-- Тулбар -->
      <div class="toolbar">
        <div class="search-wrap">
          <i class="fa fa-search"></i>
          <input
            v-model="search"
            type="text"
            placeholder="Поиск по имени, телефону, email"
            @input="onSearchInput"
          >
          <button v-if="search" class="clear-search" @click="clearSearch">
            <i class="fa fa-times"></i>
          </button>
        </div>
        <BaseButton
          variant="primary"
          icon="fa fa-plus"
          @click="openCreateModal"
        >
          Добавить клиента
        </BaseButton>
      </div>

      <!-- Список -->
      <div v-if="clients.length > 0" class="clients-grid">
        <div
          v-for="client in clients"
          :key="client.id"
          class="client-card"
          @click="goToClient(client.id)"
        >
          <div class="client-avatar">
            <i class="fa fa-user"></i>
          </div>
          <div class="client-body">
            <div class="client-name">{{ client.name }}</div>
            <div class="client-meta">
              <span v-if="client.phone">
                <i class="fa fa-phone"></i> {{ client.phone }}
              </span>
              <span v-if="client.email">
                <i class="fa fa-envelope"></i> {{ client.email }}
              </span>
            </div>
            <div v-if="client.note" class="client-note">
              {{ client.note }}
            </div>
          </div>
          <div class="client-actions" @click.stop>
            <button
              class="icon-btn"
              title="Редактировать"
              @click="openEditModal(client)"
            >
              <i class="fa fa-pen"></i>
            </button>
            <button
              class="icon-btn danger"
              title="Удалить"
              @click="askDelete(client)"
            >
              <i class="fa fa-trash"></i>
            </button>
          </div>
        </div>
      </div>

      <div v-else-if="!loading" class="empty">
        <div class="empty-icon"><i class="fa fa-users"></i></div>
        <h3>{{ search ? 'Ничего не найдено' : 'Ещё нет клиентов' }}</h3>
        <p v-if="search">Попробуйте изменить запрос</p>
        <p v-else>Добавьте первого клиента, чтобы начать вести учёт</p>
        <BaseButton
          v-if="!search"
          variant="primary"
          icon="fa fa-plus"
          @click="openCreateModal"
        >
          Добавить клиента
        </BaseButton>
      </div>
    </div>

    <!-- Модалки -->
    <ClientFormModal
      :is-open="showFormModal"
      :client="editingClient"
      @close="closeFormModal"
      @saved="onClientSaved"
    />

    <ConfirmModal
      :is-open="showDeleteModal"
      title="Удалить клиента?"
      :text="`Клиент «${deletingClient?.name}» и все его мотоциклы будут удалены безвозвратно.`"
      confirm-text="Удалить"
      variant="danger"
      @confirm="confirmDelete"
      @close="showDeleteModal = false"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useBusinessStore } from '@/stores'
import { useToast } from '../../composables/useToast'
import Header from '../../components/Header.vue'
import LoadingOverlay from '../../components/LoadingOverlay.vue'
import { BaseButton } from '../../components/ui'
import ClientFormModal from '../../components/modals/business/ClientFormModal.vue'
import ConfirmModal from '../../components/ui/ConfirmModal.vue'

const router = useRouter()
const toast = useToast()
const business = useBusinessStore()

const { clients, clientsLoading: loading } = storeToRefs(business)

const search = ref('')
const showFormModal = ref(false)
const editingClient = ref(null)

const showDeleteModal = ref(false)
const deletingClient = ref(null)

let searchTimer = null

onMounted(async () => {
  try {
    await business.loadAccount()
    if (business.hasAccount) {
      await business.loadClients()
    }
  } catch (err) {
    toast.error('Не удалось загрузить клиентов')
  }
})

function onSearchInput() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    business.setClientSearch(search.value)
    business.loadClients()
  }, 350)
}

function clearSearch() {
  search.value = ''
  business.setClientSearch('')
  business.loadClients()
}

function openCreateModal() {
  editingClient.value = null
  showFormModal.value = true
}

function openEditModal(client) {
  editingClient.value = client
  showFormModal.value = true
}

function closeFormModal() {
  showFormModal.value = false
  editingClient.value = null
}

async function onClientSaved() {
  closeFormModal()
  await business.loadClients()
}

function goToClient(id) {
  router.push(`/business/clients/${id}`)
}

function askDelete(client) {
  deletingClient.value = client
  showDeleteModal.value = true
}

async function confirmDelete() {
  if (!deletingClient.value) return
  try {
    await business.deleteClient(deletingClient.value.id)
    toast.success('Клиент удалён')
    showDeleteModal.value = false
    deletingClient.value = null
  } catch (err) {
    toast.error(err.response?.data?.error || 'Ошибка удаления')
  }
}
</script>

<style scoped>
.no-account {
  text-align: center;
  padding: 60px 20px;
  background: var(--bg-card);
  border: 1px dashed var(--border-color);
  border-radius: var(--radius-lg);
}
.no-account i { font-size: 42px; color: var(--accent-text); margin-bottom: 12px; }
.no-account p { color: var(--text-secondary); margin: 8px 0 16px; }
.no-account .btn-primary {
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

.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  align-items: center;
}
.search-wrap {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
}
.search-wrap > i {
  position: absolute;
  left: 14px;
  color: var(--text-muted);
  font-size: 14px;
  pointer-events: none;
}
.search-wrap input {
  width: 100%;
  padding: 10px 40px 10px 40px;
  border: 1px solid var(--border-input);
  border-radius: var(--radius-md);
  background: var(--bg-input);
  color: var(--text-primary);
  font-size: 14px;
  transition: all var(--transition-base);
}
.search-wrap input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: var(--shadow-focus);
}
.clear-search {
  position: absolute;
  right: 8px;
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 6px;
  min-height: 28px;
  border-radius: var(--radius-sm);
}
.clear-search:hover { color: var(--danger-text); background: var(--danger-trans); }

.clients-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 12px;
}

.client-card {
  display: flex;
  gap: 14px;
  padding: 16px 18px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-base);
  align-items: flex-start;
}
.client-card:hover {
  border-color: var(--accent);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.client-avatar {
  width: 44px;
  height: 44px;
  min-height: 44px;
  border-radius: 50%;
  background: var(--accent-trans);
  color: var(--accent-text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.client-body { flex: 1; min-width: 0; }
.client-name {
  font-size: 15px;
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
  margin-bottom: 4px;
}
.client-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  font-size: 12px;
  color: var(--text-muted);
}
.client-meta span { display: inline-flex; align-items: center; gap: 4px; }
.client-meta i { font-size: 10px; }
.client-note {
  margin-top: 8px;
  font-size: 12px;
  color: var(--text-secondary);
  padding: 6px 10px;
  background: var(--bg-secondary);
  border-radius: var(--radius-sm);
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.client-actions {
  display: flex;
  gap: 2px;
  flex-shrink: 0;
}
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
.empty-icon {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: var(--accent-trans);
  color: var(--accent-text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
  margin: 0 auto 16px;
}
.empty h3 { margin: 0 0 8px; color: var(--text-primary); }
.empty p { color: var(--text-secondary); margin: 0 0 20px; font-size: 14px; }

@media (max-width: 640px) {
  .toolbar { flex-direction: column; align-items: stretch; }
  .clients-grid { grid-template-columns: 1fr; }
}
</style>
