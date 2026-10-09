<template>
  <div class="container">
    <LoadingOverlay :isLoading="loading" text="Загрузка услуг..."/>

    <Header
      title="Мои услуги"
      subtitle="Каталог услуг, которые вы предлагаете клиентам"
    />

    <div v-if="!business.hasAccount && !loading" class="empty">
      <i class="fa fa-info-circle"></i>
      <h3>Сначала создайте бизнес-аккаунт</h3>
      <router-link to="/business" class="btn-primary">Перейти в кабинет</router-link>
    </div>

    <div v-else class="services-page">
      <!-- Табы -->
      <div class="tabs">
        <button
          v-for="t in tabs"
          :key="t.id"
          class="tab"
          :class="{ active: activeTab === t.id }"
          @click="activeTab = t.id"
        >
          {{ t.label }}
          <span class="tab-count">{{ tabCount(t.id) }}</span>
        </button>
      </div>

      <!-- Тулбар -->
      <div class="toolbar">
        <div class="toolbar-info">
          <span v-if="activeTab === 'pending' && counts.pending">
            Услуги на модерации появятся в публичном каталоге после одобрения.
          </span>
          <span v-else-if="activeTab === 'rejected' && counts.rejected">
            Отклонённые услуги можно отредактировать и снова отправить на проверку.
          </span>
          <span v-else>
            Всего услуг: {{ counts.all }}
          </span>
        </div>
        <BaseButton
          variant="primary"
          icon="fa fa-plus"
          @click="openCreateModal"
        >
          Добавить услугу
        </BaseButton>
      </div>

      <!-- Список -->
      <div v-if="filteredByTab.length" class="services-grid">
        <div
          v-for="s in filteredByTab"
          :key="s.id"
          class="service-card"
          :class="'status-' + s.status"
        >
          <div class="service-top">
            <div class="service-icon">
              <i :class="categoryIcon(s.category)"></i>
            </div>
            <div class="service-title-wrap">
              <div class="service-title">{{ s.title }}</div>
              <div class="service-category">{{ categoryLabel(s.category) }}</div>
            </div>
            <div class="service-status">
              <span :class="'badge badge-' + statusVariant(s.status)">
                {{ statusLabel(s.status) }}
              </span>
            </div>
          </div>

          <p v-if="s.description" class="service-desc">{{ s.description }}</p>

          <div class="service-meta">
            <div v-if="s.price_from || s.price_to" class="meta-item">
              <i class="fa fa-ruble-sign"></i>
              <span>
                <template v-if="s.price_from && s.price_to">
                  {{ s.price_from }}–{{ s.price_to }} ₽
                </template>
                <template v-else-if="s.price_from">
                  от {{ s.price_from }} ₽
                </template>
                <template v-else>
                  до {{ s.price_to }} ₽
                </template>
              </span>
            </div>
            <div v-if="s.duration_min" class="meta-item">
              <i class="fa fa-clock"></i>
              <span>{{ formatDuration(s.duration_min) }}</span>
            </div>
          </div>

          <div v-if="s.status === 'rejected' && s.rejection_reason" class="reject-box">
            <i class="fa fa-circle-exclamation"></i>
            <div>
              <strong>Причина отклонения:</strong>
              <div>{{ s.rejection_reason }}</div>
            </div>
          </div>

          <div class="service-actions">
            <button class="icon-btn" title="Редактировать" @click="openEditModal(s)">
              <i class="fa fa-pen"></i>
            </button>
            <button class="icon-btn danger" title="Удалить" @click="askDelete(s)">
              <i class="fa fa-trash"></i>
            </button>
          </div>
        </div>
      </div>

      <div v-else class="empty-tab">
        <i class="fa fa-wrench"></i>
        <p>{{ emptyText }}</p>
        <BaseButton
          v-if="activeTab === 'all' || activeTab === 'pending'"
          variant="primary"
          icon="fa fa-plus"
          @click="openCreateModal"
        >
          Добавить услугу
        </BaseButton>
      </div>
    </div>

    <!-- Модалки -->
    <ServiceFormModal
      :is-open="showFormModal"
      :service="editingService"
      @close="closeFormModal"
      @saved="onSaved"
    />

    <ConfirmModal
      :is-open="showDeleteModal"
      title="Удалить услугу?"
      :text="`Услуга «${deletingService?.title}» будет удалена безвозвратно.`"
      confirm-text="Удалить"
      variant="danger"
      @confirm="confirmDelete"
      @close="showDeleteModal = false"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useBusinessStore, useServicesStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import Header from '@/components/Header.vue'
import LoadingOverlay from '@/components/LoadingOverlay.vue'
import { BaseButton } from '@/components/ui'
import ServiceFormModal from '@/components/modals/business/ServiceFormModal.vue'
import ConfirmModal from '@/components/ui/ConfirmModal.vue'

const toast = useToast()
const business = useBusinessStore()
const servicesStore = useServicesStore()

const { myServices, loading, counts } = storeToRefs(servicesStore)

const activeTab = ref('all')
const showFormModal = ref(false)
const editingService = ref(null)
const showDeleteModal = ref(false)
const deletingService = ref(null)

const tabs = [
  { id: 'all', label: 'Все' },
  { id: 'pending', label: 'На модерации' },
  { id: 'approved', label: 'Одобренные' },
  { id: 'rejected', label: 'Отклонённые' },
]

const filteredByTab = computed(() => {
  if (activeTab.value === 'all') return myServices.value
  return myServices.value.filter((s) => s.status === activeTab.value)
})

const emptyText = computed(() => {
  const map = {
    all: 'У вас пока нет услуг',
    pending: 'Нет услуг на модерации',
    approved: 'Нет одобренных услуг',
    rejected: 'Нет отклонённых услуг',
  }
  return map[activeTab.value] || 'Пусто'
})

function tabCount(id) {
  return counts.value[id] ?? 0
}

onMounted(async () => {
  try {
    if (!business.hasAccount) await business.loadAccount()
    if (business.hasAccount) {
      await servicesStore.loadMine()
    }
  } catch (err) {
    toast.error('Не удалось загрузить услуги')
  }
})

function openCreateModal() {
  editingService.value = null
  showFormModal.value = true
}

function openEditModal(s) {
  editingService.value = s
  showFormModal.value = true
}

function closeFormModal() {
  showFormModal.value = false
  editingService.value = null
}

function onSaved() {
  closeFormModal()
}

function askDelete(s) {
  deletingService.value = s
  showDeleteModal.value = true
}

async function confirmDelete() {
  if (!deletingService.value) return
  try {
    await servicesStore.remove(deletingService.value.id)
    toast.success('Услуга удалена')
    showDeleteModal.value = false
    deletingService.value = null
  } catch (err) {
    toast.error(err.response?.data?.error || 'Ошибка удаления')
  }
}

// ===== Хелперы =====
function categoryIcon(c) {
  return {
    maintenance: 'fa fa-wrench',
    repair: 'fa fa-screwdriver-wrench',
    diagnostics: 'fa fa-stethoscope',
    tuning: 'fa fa-gauge-high',
    other: 'fa fa-gear',
  }[c] || 'fa fa-gear'
}

function categoryLabel(c) {
  return {
    maintenance: 'Обслуживание',
    repair: 'Ремонт',
    diagnostics: 'Диагностика',
    tuning: 'Тюнинг',
    other: 'Другое',
  }[c] || 'Другое'
}

function statusVariant(s) {
  return { pending: 'warning', approved: 'success', rejected: 'danger' }[s] || 'gray'
}

function statusLabel(s) {
  return { pending: 'На модерации', approved: 'Одобрена', rejected: 'Отклонена' }[s] || s
}

function formatDuration(min) {
  if (min < 60) return `${min} мин`
  const h = Math.floor(min / 60)
  const m = min % 60
  return m ? `${h} ч ${m} мин` : `${h} ч`
}
</script>

<style scoped>
.services-page { display: flex; flex-direction: column; gap: 20px; }

.tabs {
  display: flex;
  gap: 4px;
  border-bottom: 1px solid var(--border-light);
  flex-wrap: wrap;
}
.tab {
  background: none;
  border: none;
  padding: 10px 16px;
  font-size: 13px;
  font-weight: var(--fw-medium);
  color: var(--text-muted);
  cursor: pointer;
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: color var(--transition-base);
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
  display: inline-block;
  padding: 0 8px;
  border-radius: var(--radius-full);
  background: var(--bg-secondary);
  font-size: 11px;
  font-weight: var(--fw-semibold);
  color: var(--text-muted);
}
.tab.active .tab-count {
  background: var(--accent-trans);
  color: var(--accent-text);
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
.toolbar-info {
  font-size: 13px;
  color: var(--text-muted);
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 12px;
}

.service-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-left: 3px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: all var(--transition-base);
  position: relative;
}
.service-card:hover { box-shadow: var(--shadow-sm); }
.service-card.status-pending { border-left-color: var(--warning); }
.service-card.status-approved { border-left-color: var(--success); }
.service-card.status-rejected { border-left-color: var(--danger); }

.service-top {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}
.service-icon {
  width: 42px;
  height: 42px;
  min-height: 42px;
  border-radius: var(--radius-md);
  background: var(--accent-trans);
  color: var(--accent-text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 17px;
  flex-shrink: 0;
}
.service-title-wrap { flex: 1; min-width: 0; }
.service-title {
  font-size: 14px;
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
  line-height: 1.3;
}
.service-category {
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.4px;
  margin-top: 2px;
}
.service-status { flex-shrink: 0; }

.service-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: var(--leading-base);
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.service-meta {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  font-size: 12px;
  color: var(--text-secondary);
}
.meta-item {
  display: inline-flex;
  align-items: center;
  gap: 5px;
}
.meta-item i { color: var(--text-muted); font-size: 11px; }

.reject-box {
  display: flex;
  gap: 8px;
  padding: 8px 10px;
  background: var(--danger-trans);
  border-radius: var(--radius-sm);
  font-size: 12px;
  color: var(--text-secondary);
}
.reject-box i { color: var(--danger-text); margin-top: 2px; }
.reject-box strong { color: var(--danger-text); }

.service-actions {
  display: flex;
  gap: 2px;
  justify-content: flex-end;
  border-top: 1px solid var(--border-light);
  padding-top: 10px;
}

.empty-tab {
  text-align: center;
  padding: 50px 20px;
  background: var(--bg-card);
  border: 1px dashed var(--border-color);
  border-radius: var(--radius-lg);
}
.empty-tab i { font-size: 36px; color: var(--text-muted); margin-bottom: 10px; display: block; }
.empty-tab p { color: var(--text-secondary); margin: 0 0 16px; }

.empty {
  text-align: center;
  padding: 60px 20px;
  background: var(--bg-card);
  border: 1px dashed var(--border-color);
  border-radius: var(--radius-lg);
}
.empty i { font-size: 42px; color: var(--accent-text); margin-bottom: 12px; display: block; }
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

@media (max-width: 640px) {
  .services-grid { grid-template-columns: 1fr; }
}
</style>
