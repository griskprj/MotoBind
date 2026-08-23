<template>
  <div class="repair-page">
    <LoadingOverlay :isLoading="loading" text="Загрузка данных..." />

    <!-- ХЕДЕР -->
    <Header
      title="Ремонт и обслуживание"
      subtitle="Проводите обслуживание мотоцикла с нашими мануалами"
    />

    <!-- СТАТИСТИКА -->
    <section class="stats-section">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon warning">
            <i class="fa fa-exclamation-triangle"></i>
          </div>
          <div class="stat-info">
            <span class="stat-value">{{ overdueCount }}</span>
            <span class="stat-label">Просроченных ТО</span>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon info">
            <i class="fa fa-clock"></i>
          </div>
          <div class="stat-info">
            <span class="stat-value">{{ pendingCount }}</span>
            <span class="stat-label">Скоро ТО</span>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon success">
            <i class="fa fa-calendar-check"></i>
          </div>
          <div class="stat-info">
            <span class="stat-value">{{ plannedCount }}</span>
            <span class="stat-label">Плановых ТО</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ВЫБОР МОТОЦИКЛА И ОБСЛУЖИВАНИЯ -->
    <section class="selection-section">
      <div class="selection-flow">
        <!-- Шаг 1: Мотоцикл -->
        <div class="selection-step">
          <div class="step-indicator">
            <span class="step-number">1</span>
          </div>
          <div class="step-content">
            <label class="step-label">Выберите мотоцикл</label>
            <div class="select-wrapper">
              <select 
                v-model="selectedMoto" 
                @change="onMotoChange"
                class="styled-select"
              >
                <option value="">Выберите мотоцикл</option>
                <option 
                  v-for="moto in motorcycles" 
                  :key="moto.id" 
                  :value="moto.id"
                >
                  {{ moto.name }}
                </option>
              </select>
              <i class="fa fa-chevron-down select-arrow"></i>
            </div>
            <div v-if="selectedMotoData" class="moto-info">
              <span class="moto-mileage">
                <i class="fa fa-road"></i> {{ selectedMotoData.mileage }} км
              </span>
            </div>
          </div>
        </div>

        <!-- Шаг 2: Обслуживание -->
        <div class="selection-step" :class="{ disabled: !selectedMoto }">
          <div class="step-indicator">
            <span class="step-number">2</span>
          </div>
          <div class="step-content">
            <label class="step-label">Выберите обслуживание</label>
            <div class="select-wrapper">
              <select 
                v-model="selectedMaintenance" 
                @change="onMaintenanceChange"
                class="styled-select"
                :disabled="!selectedMoto"
              >
                <option value="">Выберите обслуживание</option>
                <option 
                  v-for="m in availableMaintenances" 
                  :key="m.id" 
                  :value="m.id"
                >
                  {{ m.title }}
                  <span v-if="m.status === 'overdue'" class="badge-overdue">Просрочено</span>
                </option>
              </select>
              <i class="fa fa-chevron-down select-arrow"></i>
            </div>
            <div v-if="selectedMaintenanceData" class="maintenance-info">
              <span class="info-badge" :class="maintenanceStatusClass">
                <i :class="maintenanceStatusIcon"></i>
                {{ maintenanceStatusText }}
              </span>
              <span class="info-mileage" v-if="selectedMaintenanceData.planned_mileage">
                <i class="fa fa-flag-checkered"></i> 
                {{ selectedMaintenanceData.planned_mileage }} км
              </span>
            </div>
          </div>
        </div>

        <!-- Шаг 3: Результат -->
        <div class="selection-step result-step" :class="{ 
          disabled: !selectedMoto || !selectedMaintenance,
          found: manual,
          notfound: !manual && selectedMoto && selectedMaintenance
        }">
          <div class="step-indicator">
            <span class="step-number">3</span>
          </div>
          <div class="step-content">
            <div class="result-status">
              <div class="result-icon" v-if="manual">
                <i class="fa fa-check-circle"></i>
              </div>
              <div class="result-icon empty" v-else-if="selectedMoto && selectedMaintenance">
                <i class="fa fa-search"></i>
              </div>
              <div class="result-icon waiting" v-else>
                <i class="fa fa-hourglass-half"></i>
              </div>
              
              <div class="result-text">
                <h4 v-if="manual">Мануал найден</h4>
                <h4 v-else-if="selectedMoto && selectedMaintenance">Мануал не найден</h4>
                <h4 v-else>Ожидание выбора</h4>
                <p v-if="manual">Инструкция автоматически подобрана</p>
                <p v-else-if="selectedMoto && selectedMaintenance">
                  Мы не нашли подходящий мануал. Вы можете создать его сами.
                </p>
                <p v-else>Выберите мотоцикл и обслуживание</p>
              </div>
            </div>

            <div class="result-actions">
              <button 
                v-if="manual" 
                @click="resetSelection" 
                class="btn btn-secondary btn-sm"
              >
                <i class="fa fa-refresh"></i> Сменить
              </button>
              <button 
                v-else-if="selectedMoto && selectedMaintenance && !manual"
                @click="openCreateManual" 
                class="btn btn-outline btn-sm"
              >
                <i class="fa fa-plus"></i> Создать мануал
              </button>
              <button 
                v-else
                class="btn btn-secondary btn-sm" 
                disabled
              >
                <i class="fa fa-hourglass-start"></i> Ожидание
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- МАНУАЛ -->
    <section v-if="manual" class="manual-section">
      <div class="manual-container">
        <!-- Левая колонка: Инструкция -->
        <div class="manual-content">
          <div class="manual-header">
            <h2 class="manual-title">{{ manual.title }}</h2>
            <p class="manual-description">{{ manual.description || 'Инструкция по выполнению обслуживания' }}</p>
            <div class="manual-meta-tags">
              <span class="tag" v-if="manual.category">
                <i class="fa fa-tag"></i> {{ getCategoryName(manual.category) }}
              </span>
              <span class="tag" v-if="manual.difficult">
                <i class="fa fa-signal"></i> {{ getDifficultyName(manual.difficult) }}
              </span>
              <span class="tag">
                <i class="fa fa-motorcycle"></i> {{ manual.motorcycle }}
              </span>
            </div>
          </div>

          <!-- Шаги -->
          <div class="steps-wrapper">
            <h3 class="steps-title">
              <i class="fa fa-list-ol"></i> 
              Инструкция по шагам
              <span class="steps-count">{{ manualSteps.length }} шаг{{ manualSteps.length > 1 ? 'а' : '' }}</span>
            </h3>

            <div class="steps-list">
              <div 
                v-for="(step, index) in manualSteps" 
                :key="step.order || index"
                class="step-item"
              >
                <div class="step-marker">
                  <span class="step-number">{{ step.order || index + 1 }}</span>
                  <div class="step-connector" v-if="index < manualSteps.length - 1"></div>
                </div>

                <div class="step-body">
                  <h4 class="step-title">{{ step.title || `Шаг ${index + 1}` }}</h4>
                  <p v-if="step.text" class="step-text">{{ step.text }}</p>
                  
                  <div v-if="step.tip" class="step-tip info">
                    <i class="fa fa-info-circle"></i>
                    <span>{{ step.tip }}</span>
                  </div>
                  
                  <div v-if="step.warning" class="step-tip warning">
                    <i class="fa fa-exclamation-triangle"></i>
                    <span>{{ step.warning }}</span>
                  </div>

                  <div v-if="step.image" class="step-image">
                    <img :src="step.image" :alt="step.title || 'Шаг'" loading="lazy" />
                  </div>
                </div>
              </div>
            </div>

            <div v-if="manual.tip" class="manual-tip">
              <i class="fa fa-lightbulb-o"></i>
              <div>
                <strong>Совет:</strong>
                <span>{{ manual.tip }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Правая колонка: Инструменты и завершение -->
        <div class="manual-sidebar">
          <!-- Инструменты -->
          <div class="sidebar-card">
            <h4><i class="fa fa-wrench"></i> Инструменты</h4>
            <ul v-if="instrumentsList.length" class="items-list">
              <li v-for="item in instrumentsList" :key="item">
                <i class="fa fa-check-circle"></i> {{ item }}
              </li>
            </ul>
            <p v-else class="empty-text">Не указаны</p>
          </div>

          <!-- Материалы -->
          <div class="sidebar-card">
            <h4><i class="fa fa-cogs"></i> Материалы</h4>
            <ul v-if="partsList.length" class="items-list">
              <li v-for="item in partsList" :key="item">
                <i class="fa fa-check-circle"></i> {{ item }}
              </li>
            </ul>
            <p v-else class="empty-text">Не указаны</p>
          </div>

          <!-- Завершение -->
          <div class="sidebar-card complete-card">
            <h4><i class="fa fa-flag-checkered"></i> Завершить обслуживание</h4>
            <p class="complete-text">После завершения вы сможете:</p>
            <ul class="complete-benefits">
              <li><i class="fa fa-check"></i> Записать в историю</li>
              <li><i class="fa fa-check"></i> Создать следующее ТО</li>
            </ul>
            <button @click="openCompleteModal" class="btn btn-success btn-block">
              <i class="fa fa-check"></i> Завершить обслуживание
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- ПУСТОЕ СОСТОЯНИЕ -->
    <section v-else-if="!selectedMoto || !selectedMaintenance" class="empty-section">
      <div class="empty-state">
        <div class="empty-icon">
          <i class="fa fa-motorcycle"></i>
        </div>
        <h3>Выберите данные для начала</h3>
        <p>Выберите мотоцикл и необходимое обслуживание, чтобы получить инструкцию</p>
      </div>
    </section>

    <!-- МАНУАЛ НЕ НАЙДЕН -->
    <section v-else-if="selectedMoto && selectedMaintenance && !manual" class="empty-section">
      <div class="empty-state">
        <div class="empty-icon warning">
          <i class="fa fa-file-text-o"></i>
        </div>
        <h3>Мануал не найден</h3>
        <p>К сожалению, мы не нашли подходящий мануал в базе. Вы можете создать его сами.</p>
        <button @click="openCreateManual">
          <i class="fa fa-plus"></i> Создать мануал
        </button>
        <button @click="openCompleteModal">
          <i class="fa fa-plus"></i> Завершить обслуживание
        </button>
      </div>
    </section>

    <!-- МОДАЛ ЗАВЕРШЕНИЯ -->
    <MarkPlanMaintenanceModal
      :is-open="showCompleteModal"
      :motorcycle="selectedMotoData"
      :maintenance="selectedMaintenanceData"
      @close="showCompleteModal = false"
      @submit="handleComplete"
    />
  </div>
</template>

<script>
import api from '../api/api'
import MarkPlanMaintenanceModal from '../components/modals/maintenance/MarkPlanMaintenanceModal.vue'
import Header from '../components/Header.vue'
import LoadingOverlay from '../components/LoadingOverlay.vue'

export default {
  name: 'RepairPage',
  
  components: {
    MarkPlanMaintenanceModal,
    Header,
    LoadingOverlay
  },

  data() {
    return {
      loading: false,
      
      // Данные
      motorcycles: [],
      maintenances: [],
      manual: null,
      
      // Выбранные значения
      selectedMoto: null,
      selectedMaintenance: null,
      
      // Производные данные
      selectedMotoData: null,
      selectedMaintenanceData: null,
      
      // Модалки
      showCompleteModal: false,
      
      // Статистика
      overdueCount: 0,
      pendingCount: 0,
      plannedCount: 0,
    }
  },

  computed: {
    availableMaintenances() {
      if (!this.selectedMoto) return []
      return this.maintenances.filter(m => 
        m.moto_id === this.selectedMoto &&
        (m.status === 'planned' || m.status === 'overdue')
      )
    },

    manualSteps() {
      if (!this.manual || !this.manual.steps) return []
      if (Array.isArray(this.manual.steps)) {
        return [...this.manual.steps].sort((a, b) => (a.order || 0) - (b.order || 0))
      }
      return []
    },

    instrumentsList() {
      if (!this.manual?.instruments) return []
      if (typeof this.manual.instruments === 'string') {
        return this.manual.instruments.split(/[,;]\s*/).filter(s => s.trim())
      }
      if (Array.isArray(this.manual.instruments)) {
        return this.manual.instruments
      }
      return []
    },

    partsList() {
      if (!this.manual?.parts) return []
      if (typeof this.manual.parts === 'string') {
        return this.manual.parts.split(/[,;]\s*/).filter(s => s.trim())
      }
      if (Array.isArray(this.manual.parts)) {
        return this.manual.parts
      }
      return []
    },

    maintenanceStatusClass() {
      if (!this.selectedMaintenanceData) return ''
      if (this.selectedMaintenanceData.status === 'overdue') return 'status-overdue'
      if (this.selectedMaintenanceData.status === 'planned') return 'status-planned'
      return ''
    },

    maintenanceStatusIcon() {
      if (!this.selectedMaintenanceData) return ''
      if (this.selectedMaintenanceData.status === 'overdue') return 'fa fa-exclamation-circle'
      if (this.selectedMaintenanceData.status === 'planned') return 'fa fa-clock-o'
      return 'fa fa-circle'
    },

    maintenanceStatusText() {
      if (!this.selectedMaintenanceData) return ''
      if (this.selectedMaintenanceData.status === 'overdue') return 'Просрочено'
      if (this.selectedMaintenanceData.status === 'planned') return 'Запланировано'
      return this.selectedMaintenanceData.status
    }
  },

  watch: {
    selectedMoto(val) {
      if (val) {
        this.selectedMotoData = this.motorcycles.find(m => m.id === val) || null
      } else {
        this.selectedMotoData = null
      }
      this.selectedMaintenance = null
      this.selectedMaintenanceData = null
      this.manual = null
    }
  },

  mounted() {
    this.loadData()
  },

  methods: {
    async loadData() {
      this.loading = true
      try {
        const response = await api.get('/statistic/repair')
        this.motorcycles = response.data.motorcycles || []
        this.maintenances = response.data.maintenances || []
        this.overdueCount = response.data.overdue || 0
        this.pendingCount = response.data.soon || 0
        this.plannedCount = response.data.planned || 0
      } catch (err) {
        console.error('Failed to load repair data:', err)
        this.$toast?.error('Не удалось загрузить данные')
      } finally {
        this.loading = false
      }
    },

    onMotoChange() {
      this.selectedMaintenance = null
      this.selectedMaintenanceData = null
      this.manual = null
    },

    async onMaintenanceChange() {
      if (!this.selectedMaintenance) {
        this.manual = null
        this.selectedMaintenanceData = null
        return
      }

      this.selectedMaintenanceData = this.maintenances.find(
        m => m.id === this.selectedMaintenance
      ) || null

      // Сбрасываем мануал перед загрузкой
      this.manual = null
      
      if (this.selectedMoto && this.selectedMaintenance) {
        await this.fetchManual()
      }
    },

    async fetchManual() {
      try {
        const response = await api.get('/manual/', {
          params: {
            maintenance_id: this.selectedMaintenance,
            moto_id: this.selectedMoto
          }
        })

        // Обработка ответа
        if (response.data) {
          if (Array.isArray(response.data)) {
            this.manual = response.data.length > 0 ? response.data[0] : null
          } else if (response.data.id) {
            this.manual = response.data
          } else {
            this.manual = null
          }
        } else {
          this.manual = null
        }

        // Валидация данных мануала
        if (this.manual) {
          if (!this.manual.steps) {
            this.manual.steps = []
          }
          if (!Array.isArray(this.manual.steps)) {
            this.manual.steps = []
          }
        }
      } catch (err) {
        console.error('Failed to fetch manual:', err)
        this.manual = null
      }
    },

    resetSelection() {
      this.selectedMoto = null
      this.selectedMaintenance = null
      this.selectedMotoData = null
      this.selectedMaintenanceData = null
      this.manual = null
    },

    openCompleteModal() {
      if (!this.selectedMaintenanceData) {
        this.$toast?.warning('Выберите обслуживание')
        return
      }
      this.showCompleteModal = true
    },

    async handleComplete(formData) {
      try {
        await api.post(`/maintenance/${formData.id}/complete`, {
          completed_mileage: formData.mileage,
          completed_date: formData.date,
          cost: formData.cost,
          is_repeat: formData.isRepeat,
          interval: formData.interval
        })
        
        this.showCompleteModal = false
        this.$toast?.success('Обслуживание успешно завершено!')
        
        // Обновляем данные
        await this.loadData()
        
        // Сбрасываем выбор
        this.selectedMaintenance = null
        this.selectedMaintenanceData = null
        this.manual = null
      } catch (err) {
        console.error('Failed to complete maintenance:', err)
        this.$toast?.error(err.response?.data?.error || 'Ошибка при завершении обслуживания')
      }
    },

    openCreateManual() {
      // TODO: Открыть страницу создания мануала с предзаполненными данными
      this.$router.push('/manual-creator')
    },

    getCategoryName(category) {
      const map = {
        engine: 'Двигатель',
        drive: 'Привод',
        steering: 'Рулевое управление',
        suspension: 'Подвеска',
        electronics: 'Электроника',
        wheel: 'Колеса / Шины',
        brakes: 'Тормозная система',
        fuel: 'Топливная система',
        cooling: 'Система охлаждения'
      }
      return map[category] || category || 'Другое'
    },

    getDifficultyName(difficult) {
      const map = {
        easy: 'Лёгкая',
        medium: 'Средняя',
        hard: 'Сложная'
      }
      return map[difficult] || difficult || 'Средняя'
    }
  }
}
</script>

<style scoped>
.repair-page {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px 40px;
}

/* ===== STATS ===== */
.stats-section {
  margin-bottom: 32px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  background: var(--bg-card);
  border-radius: 16px;
  border: 1px solid var(--border-color);
  transition: all 0.2s;
}

.stat-card:hover {
  border-color: var(--accent);
  transform: translateY(-2px);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.stat-icon.warning {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.stat-icon.info {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.stat-icon.success {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  line-height: 1.2;
}

.stat-label {
  font-size: 14px;
  color: var(--text-muted);
}

/* ===== SELECTION FLOW ===== */
.selection-section {
  margin-bottom: 32px;
}

.selection-flow {
  display: grid;
  grid-template-columns: 1fr 1fr 1.2fr;
  gap: 16px;
  background: var(--bg-card);
  border-radius: 16px;
  border: 1px solid var(--border-color);
  padding: 24px;
}

.selection-step {
  display: flex;
  gap: 16px;
  position: relative;
}

.selection-step.disabled {
  opacity: 0.5;
  pointer-events: none;
}

.selection-step.result-step {
  opacity: 1;
  pointer-events: auto;
}

.selection-step.result-step.found {
  border-left: 3px solid var(--success);
  padding-left: 16px;
}

.selection-step.result-step.notfound {
  border-left: 3px solid var(--warning);
  padding-left: 16px;
}

.step-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
  padding-top: 4px;
}

.step-number {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--accent);
  color: white;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}

.step-line {
  width: 2px;
  flex: 1;
  min-height: 20px;
  background: var(--border-color);
  margin: 4px 0;
}

.selection-step:last-child .step-line {
  display: none;
}

.step-content {
  flex: 1;
  min-width: 0;
}

.step-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.select-wrapper {
  position: relative;
}

.styled-select {
  width: 100%;
  padding: 10px 36px 10px 14px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  color: var(--text-primary);
  font-size: 14px;
  appearance: none;
  cursor: pointer;
  transition: border-color 0.2s;
}

.styled-select:focus {
  outline: none;
  border-color: var(--accent);
}

.styled-select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.select-arrow {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  pointer-events: none;
  font-size: 12px;
}

.moto-info,
.maintenance-info {
  margin-top: 8px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.moto-mileage {
  font-size: 13px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 4px;
}

.info-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 2px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.status-overdue {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.status-planned {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.info-mileage {
  font-size: 13px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 4px;
}

.badge-overdue {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
  font-size: 10px;
  font-weight: 600;
  padding: 1px 8px;
  border-radius: 10px;
  margin-left: 6px;
}

/* Result step */
.result-status {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}

.result-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.result-icon {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.result-icon.empty {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.result-icon.waiting {
  background: rgba(100, 116, 139, 0.15);
  color: #94a3b8;
}

.result-text h4 {
  margin: 0 0 4px 0;
  font-size: 15px;
  font-weight: 600;
}

.result-text p {
  margin: 0;
  font-size: 13px;
  color: var(--text-muted);
}

.result-actions {
  display: flex;
  gap: 8px;
}

.btn-sm {
  padding: 6px 14px;
  font-size: 13px;
}

.btn-block {
  width: 100%;
}

.btn-success {
  background: var(--success);
  color: white;
}

.btn-success:hover {
  background: var(--success-hover);
}

/* ===== MANUAL SECTION ===== */
.manual-section {
  margin-top: 8px;
}

.manual-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

.manual-content {
  background: var(--bg-card);
  border-radius: 16px;
  border: 1px solid var(--border-color);
  padding: 24px;
}

.manual-header {
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border-color);
}

.manual-title {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 700;
}

.manual-description {
  margin: 0 0 12px 0;
  font-size: 15px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.manual-meta-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 12px;
  background: var(--bg-secondary);
  border-radius: 12px;
  font-size: 12px;
  color: var(--text-secondary);
}

.tag i {
  font-size: 12px;
}

/* Steps */
.steps-wrapper {
  margin-top: 8px;
}

.steps-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 16px 0;
  font-size: 17px;
  font-weight: 600;
}

.steps-count {
  font-size: 13px;
  font-weight: 400;
  color: var(--text-muted);
  margin-left: auto;
}

.steps-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.step-item {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: var(--bg-secondary);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  transition: all 0.2s;
}

.step-item:hover {
  border-color: var(--accent);
  background: var(--bg-card-hover);
}

.step-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.step-number {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--accent);
  color: white;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}

.step-connector {
  width: 2px;
  flex: 1;
  min-height: 20px;
  background: var(--border-color);
  margin: 4px 0;
}

.step-item:last-child .step-connector {
  display: none;
}

.step-body {
  flex: 1;
  min-width: 0;
}

.step-title {
  margin: 0 0 4px 0;
  font-size: 15px;
  font-weight: 600;
}

.step-text {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.step-tip {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 8px;
  margin-top: 8px;
  font-size: 13px;
}

.step-tip.info {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.step-tip.warning {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}

.step-tip i {
  margin-top: 2px;
}

.step-image {
  margin-top: 12px;
  border-radius: 8px;
  overflow: hidden;
}

.step-image img {
  width: 100%;
  max-height: 200px;
  object-fit: cover;
  border-radius: 8px;
}

.manual-tip {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: rgba(245, 158, 11, 0.08);
  border-radius: 12px;
  border: 1px solid rgba(245, 158, 11, 0.15);
  margin-top: 20px;
}

.manual-tip i {
  color: #f59e0b;
  font-size: 20px;
  flex-shrink: 0;
  margin-top: 2px;
}

.manual-tip div {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.manual-tip strong {
  color: var(--text-primary);
}

/* Sidebar */
.manual-sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.sidebar-card {
  background: var(--bg-card);
  border-radius: 16px;
  border: 1px solid var(--border-color);
  padding: 20px;
}

.sidebar-card h4 {
  margin: 0 0 12px 0;
  font-size: 15px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.items-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.items-list li {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--text-secondary);
}

.items-list li i {
  color: var(--success);
  font-size: 14px;
}

.empty-text {
  font-size: 14px;
  color: var(--text-muted);
  font-style: italic;
  margin: 0;
}

.complete-card {
  background: rgba(16, 185, 129, 0.05);
  border-color: rgba(16, 185, 129, 0.2);
}

.complete-card h4 {
  color: var(--success);
}

.complete-text {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0 0 8px 0;
}

.complete-benefits {
  list-style: none;
  padding: 0;
  margin: 0 0 16px 0;
}

.complete-benefits li {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-secondary);
  padding: 4px 0;
}

.complete-benefits li i {
  color: var(--success);
}

/* Empty states */
.empty-section {
  margin-top: 8px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 40px;
  background: var(--bg-card);
  border-radius: 16px;
  border: 2px dashed var(--border-color);
  text-align: center;
}

.empty-icon {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: rgba(59, 130, 246, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  color: #3b82f6;
  margin-bottom: 16px;
}

.empty-icon.warning {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}

.empty-state h3 {
  margin: 0 0 8px 0;
  font-size: 20px;
  font-weight: 600;
}

.empty-state p {
  margin: 0 0 20px 0;
  font-size: 15px;
  color: var(--text-secondary);
  max-width: 400px;
}

/* ===== RESPONSIVE ===== */
@media (max-width: 1200px) {
  .manual-container {
    grid-template-columns: 1fr;
  }

  .manual-sidebar {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
  }
}

@media (max-width: 992px) {
  .selection-flow {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .selection-step {
    padding-left: 0;
  }

  .selection-step.result-step {
    border-left: none;
    padding-left: 0;
    border-top: 1px solid var(--border-color);
    padding-top: 20px;
  }

  .step-line {
    display: none !important;
  }

  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .repair-page {
    padding: 0 12px 32px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .stat-card {
    padding: 16px 20px;
  }

  .stat-value {
    font-size: 22px;
  }

  .manual-sidebar {
    grid-template-columns: 1fr;
  }

  .manual-content {
    padding: 16px;
  }

  .manual-title {
    font-size: 20px;
  }

  .step-item {
    flex-direction: column;
    gap: 12px;
  }

  .step-marker {
    flex-direction: row;
    gap: 8px;
  }

  .step-connector {
    display: none !important;
  }

  .step-number {
    width: 28px;
    height: 28px;
    font-size: 12px;
  }

  .result-status {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .result-actions {
    flex-direction: column;
  }

  .result-actions .btn {
    width: 100%;
    justify-content: center;
  }

  .selection-flow {
    padding: 16px;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .manual-meta-tags {
    flex-direction: column;
    align-items: flex-start;
  }

  .steps-title {
    flex-wrap: wrap;
  }

  .steps-count {
    margin-left: 0;
    width: 100%;
  }

  .empty-state {
    padding: 40px 20px;
  }

  .empty-icon {
    width: 56px;
    height: 56px;
    font-size: 24px;
  }

  .empty-state h3 {
    font-size: 18px;
  }

  .complete-card .btn {
    font-size: 14px;
    padding: 12px;
  }
}
</style>