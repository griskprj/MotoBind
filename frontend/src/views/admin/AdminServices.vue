<template>
  <div class="container">
    <LoadingOverlay :isLoading="loading" text="Загрузка услуг..."/>

    <Header
      title="Модерация услуг"
      subtitle="Одобряйте и отклоняйте услуги мастеров и СТО"
    />

    <div class="tabs">
      <button
        v-for="t in tabs"
        :key="t.id"
        class="tab"
        :class="{ active: activeStatus === t.id }"
        @click="changeTab(t.id)"
      >
        {{ t.label }}
      </button>
    </div>

    <div v-if="services.length" class="services-list">
      <div
        v-for="s in services"
        :key="s.id"
        class="service-row"
        :class="'row-' + s.status"
      >
        <div class="row-icon">
          <i :class="categoryIcon(s.category)"></i>
        </div>
        <div class="row-body">
          <div class="row-title">{{ s.title }}</div>
          <div class="row-meta">
            <span><i class="fa fa-tag"></i> {{ categoryLabel(s.category) }}</span>
            <span><i class="fa fa-briefcase"></i> {{ s.business_account_id }}</span>
            <span><i class="fa fa-calendar"></i> {{ formatDate(s.created_at) }}</span>
          </div>
          <p v-if="s.description" class="row-desc">{{ s.description }}</p>
          <div v-if="s.rejection_reason" class="reject-inline">
            <i class="fa fa-circle-exclamation"></i> {{ s.rejection_reason }}
          </div>
        </div>
        <div class="row-actions">
          <span :class="'badge badge-' + statusVariant(s.status)">
            {{ statusLabel(s.status) }}
          </span>
          <template v-if="s.status !== 'approved'">
            <button class="btn-action success" @click="approve(s)">
              <i class="fa fa-check"></i> Одобрить
            </button>
          </template>
          <template v-if="s.status !== 'rejected'">
            <button class="btn-action danger" @click="askReject(s)">
              <i class="fa fa-times"></i> Отклонить
            </button>
          </template>
        </div>
      </div>
    </div>

    <div v-else-if="!loading" class="empty">
      <i class="fa fa-check-circle"></i>
      <h3>Здесь пусто</h3>
      <p>Нет услуг в этом статусе</p>
    </div>

    <!-- Модалка отклонения -->
    <ModalWrapper
      :is-open="showRejectModal"
      title="Отклонить услугу"
      subtitle="Укажите причину — мастер увидит её и сможет исправить"
      icon="circle-exclamation"
      :icon-color="'var(--danger-text)'"
      :bg-icon-color="'var(--danger-trans)'"
      @close="showRejectModal = false"
    >
      <BaseInput
        v-model="rejectReason"
        label="Причина отклонения"
        placeholder="Например: недостаточно подробное описание"
        required
      />

      <template #actions>
        <BaseButton
          variant="danger"
          block
          icon="fa fa-times"
          :disabled="rejectReason.trim().length < 3"
          @click="confirmReject"
        >
          Отклонить
        </BaseButton>
      </template>
    </ModalWrapper>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import api from '@/api/api'
import { useToast } from '../../composables/useToast'
import Header from '../../components/Header.vue'
import LoadingOverlay from '../../components/LoadingOverlay.vue'
import ModalWrapper from '../../components/modals/ModalWrapper.vue'
import { BaseButton, BaseInput } from '@/components/ui'
import formatDate from '../../utils/DateFormatter.js'

const toast = useToast()

const services = ref([])
const loading = ref(false)
const activeStatus = ref('pending')

const showRejectModal = ref(false)
const rejectReason = ref('')
const rejectingService = ref(null)

const tabs = [
  { id: 'pending', label: 'На модерации' },
  { id: 'approved', label: 'Одобренные' },
  { id: 'rejected', label: 'Отклонённые' },
]

onMounted(() => {
  loadServices()
})

async function loadServices() {
  loading.value = true
  try {
    const { data } = await api.get('/admin/services', {
      params: { status: activeStatus.value },
    })
    services.value = data
  } catch (err) {
    toast.error('Не удалось загрузить услуги')
  } finally {
    loading.value = false
  }
}

function changeTab(id) {
  if (activeStatus.value === id) return
  activeStatus.value = id
  loadServices()
}

async function approve(s) {
  try {
    await api.post(`/admin/services/${s.id}/approve`)
    toast.success('Услуга одобрена')
    await loadServices()
  } catch (err) {
    toast.error(err.response?.data?.error || 'Ошибка')
  }
}

function askReject(s) {
  rejectingService.value = s
  rejectReason.value = ''
  showRejectModal.value = true
}

async function confirmReject() {
  if (!rejectingService.value) return
  try {
    await api.post(`/admin/services/${rejectingService.value.id}/reject`, {
      reason: rejectReason.value.trim(),
    })
    toast.success('Услуга отклонена')
    showRejectModal.value = false
    rejectingService.value = null
    await loadServices()
  } catch (err) {
    toast.error(err.response?.data?.error || 'Ошибка')
  }
}

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
</script>

<style scoped>
.tabs {
  display: flex;
  gap: 4px;
  border-bottom: 1px solid var(--border-light);
  margin-bottom: 20px;
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
  min-height: 40px;
}
.tab.active { color: var(--accent-text); }
.tab.active::after {
  content: '';
  position: absolute;
  bottom: -1px; left: 0; right: 0;
  height: 2px;
  background: var(--accent);
}

.services-list { display: flex; flex-direction: column; gap: 10px; }

.service-row {
  display: flex;
  gap: 14px;
  padding: 14px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-left: 3px solid var(--border-color);
  border-radius: var(--radius-md);
  align-items: flex-start;
}
.service-row.row-pending { border-left-color: var(--warning); }
.service-row.row-approved { border-left-color: var(--success); }
.service-row.row-rejected { border-left-color: var(--danger); }

.row-icon {
  width: 40px;
  height: 40px;
  min-height: 40px;
  border-radius: var(--radius-md);
  background: var(--accent-trans);
  color: var(--accent-text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}
.row-body { flex: 1; min-width: 0; }
.row-title {
  font-size: 14px;
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
}
.row-meta {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 4px;
}
.row-meta span { display: inline-flex; align-items: center; gap: 4px; }
.row-desc {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 8px 0 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.reject-inline {
  margin-top: 8px;
  padding: 6px 10px;
  background: var(--danger-trans);
  border-radius: var(--radius-sm);
  font-size: 12px;
  color: var(--danger-text);
}

.row-actions {
  display: flex;
  gap: 6px;
  align-items: center;
  flex-shrink: 0;
}
.btn-action {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  border-radius: var(--radius-md);
  border: 1px solid transparent;
  font-size: 12px;
  font-weight: var(--fw-medium);
  cursor: pointer;
  transition: all var(--transition-base);
  min-height: 32px;
}
.btn-action.success {
  background: var(--success-trans);
  color: var(--success-text);
}
.btn-action.success:hover { background: var(--success); color: #fff; }
.btn-action.danger {
  background: var(--danger-trans);
  color: var(--danger-text);
}
.btn-action.danger:hover { background: var(--danger); color: #fff; }

.empty {
  text-align: center;
  padding: 60px 20px;
}
.empty i { font-size: 42px; color: var(--text-muted); margin-bottom: 12px; display: block; }
.empty h3 { margin: 0 0 6px; }
.empty p { color: var(--text-muted); margin: 0; }

@media (max-width: 700px) {
  .service-row { flex-wrap: wrap; }
  .row-body { flex-basis: calc(100% - 54px); }
  .row-actions {
    flex-basis: 100%;
    justify-content: flex-end;
    padding-top: 8px;
    border-top: 1px solid var(--border-light);
  }
}
</style>
