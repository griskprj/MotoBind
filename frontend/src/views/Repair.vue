<template>
    <div class="container">
        <!-- Статистика -->
        <div class="section">
            <div class="section-title-wrapper">
                <i class="fa fa-wrench"></i>
                <h2>Отремонтируйте свой мотоцикл</h2>
            </div>

            <div class="statistics-cards">
                <div class="stat-card">
                    <p class="stat-card-title">Просрочено обслуживаний</p>
                    <p class="stat-card-value">{{ overdue_maintenances_count }}</p>
                </div>
                <div class="stat-card">
                    <p class="stat-card-title">Скоро обслуживать</p>
                    <p class="stat-card-value">{{ pending_maintenances_count }}</p>
                </div>
                <div class="stat-card">
                    <p class="stat-card-title">Запланированно</p>
                    <p class="stat-card-value">{{ planned_maintenances_count }}</p>
                </div>
            </div>
        </div>

        <!-- Выбор мотоцикла и обслуживания для ремонта -->
        <div class="section">
            <div class="section-title-wrapper">
                <i class="fa fa-motorcycle"></i>
                <h2>Выберите мотоцикл и обслуживание для ремонта</h2>
            </div>

            <div class="actions-wrapper">
                <select v-model="selectedMoto" class="select-action">
                    <option value="">Выберите мотоцикл</option>
                    <option v-for="m in motorcycles" :key="m.id" :value="m.id">{{ m.name }}</option>
                </select>
                <select v-if="selectedMoto" v-model="selectedMaintenance" class="select-action">
                    <option value="">Выберите обслуживание</option>
                    <option v-for="m in maintenances" :key="m.id" :value="m.id">{{ m.title + ' | ' + m.planned_mileage + 'км' }}</option>
                </select>

                <button
                    v-if="!dataLoad"
                    @click="getRepairData"
                    :disabled="!selectedMoto || !selectedMaintenance"
                    class="select-action"
                >
                    Ремонт
                </button>

                <button
                    v-else
                    @click="removeRepairData"
                    class="select-action"
                >
                    Закрыть
                </button>
            </div>
        </div>

        <!-- Информация по ремонту -->
        <div v-if="dataLoad" class="section">
            <div class="section-title-wrapper">
                <i class="fa fa-file"></i>
                <h2>Инструкция по ремонту</h2>
            </div>

            <!-- Если нет мануала - показываем заглушку -->
            <div v-if="manual === null && dataLoad" class="empty-state">
                <div class="empty-container">
                    <div class="empty-container-item">
                        <p>К сожалению, в нашей базе пока что нет инструкции к вашей проблеме. Мы обязательно скоро ее добавим <br> (Вы можете помочь нам в этом, нажав на кнопку "Помощь").</p>
                        <button>Помощь</button>
                    </div>
                    
                    <div class="empty-container-itme">
                        <p>А пока Вы можете записаться к <br> проверенному мастеру из нашего списка.</p>
                        <button class="accept-btn">Записаться</button>
                    </div>
                </div>
            </div>

            <!-- Если есть мануал - показываем его -->
            <div v-else-if="manual" class="manual">
                <h3 class="manual-title">{{ manual.title }}</h3>
                <div class="steps">
                    <div v-for="(step, index) in manual.steps" :key="step.id" class="manual-step">
                        <div class="step-wrapper">
                            <div class="step-number">{{ index + 1 }}</div>
                            <div class="step-body">
                                <p>{{ step.text }}</p>
                            </div>
                        </div>
                        <div class="step-img-wrapper">
                        </div>
                    </div>
                </div>

                <div class="manual-actions">
                    <button @click="showMarkMaintenanceModal=true" class="accept-btn">Завершить</button>
                </div>

                <div class="record-master">
                    <p>Вы можете записаться к проверенному мастеру из нашего списка.</p>
                    <p>Он поможет Вам в ремонте самым качественным образом</p>
                    <button>Записаться</button>
                </div>
            </div>
        </div>
    </div>
    <MarkPlanMaintenanceModal
        :is-open="showMarkMaintenanceModal"
        :id="selectedMaintenance"
        @close="showMarkMaintenanceModal=false"
        @submit="markMaintenance"
    />
</template>

<script>
import api from '../api/api'
import MarkPlanMaintenanceModal from '../components/modals/maintenance/MarkPlanMaintenanceModal.vue';
export default {
    components: { MarkPlanMaintenanceModal },
    data() {
        return {
            overdue_maintenances_count: 0,
            pending_maintenances_count: 0,
            planned_maintenances_count: 0,

            motorcycles: [],
            maintenances: [],
            repairData: null,
            manual: null,

            selectedMoto: null,
            selectedMaintenance: null,
            dataLoad: false,

            showMarkMaintenanceModal: false
        }
    },

    methods: {
        async loadData() {
            try {
                const response = await api.get('/statistic/repair')

                this.motorcycles = response.data.motorcycles
                this.maintenances = response.data.maintenances
                this.overdue_maintenances_count = response.data.overdue
                this.pending_maintenances_count = response.data.soon
                this.planned_maintenances_count = response.data.planned
            } catch (err) {
                console.error('Failed load repair data: ', err)
            }
        },

        async getRepairData() {
            try {
                const response = await api.get(`/manual/?maintenance_id=${this.selectedMaintenance}&moto_id=${this.selectedMoto}`)

                this.manual = response.data
                this.dataLoad = true
            } catch (err) {
                console.error('Failed get manual: ', err)
            }
        },

        async markMaintenance(formData) {
            try {
                const response = await api.post('/maintenance/plan/mark', formData)
                this.showMarkMaintenanceModal = false
                this.$router.push('/')
            } catch (err) {
                console.log('Failed mark maintenance: ', err)
            }
        },


        removeRepairData() {
            this.selectedMaintenance = null
            this.selectedMoto = null
            this.manual = null
            this.dataLoad = false
        },
    },

    mounted() {
        this.loadData()
    }
}
</script>

<style scoped>
.empty-container-item {
    margin-bottom: 24px;
}
/* Статистика */
.statistics-cards {
  display: flex;
  flex-direction: row;
  gap: 24px;
  justify-content: center;
}

.stat-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
  justify-content: space-evenly;
  padding: 20px 24px;
  min-width: 180px;
  flex: 1;
  background-color: var(--bg-secondary);
  border: 2px solid var(--border-color);
  border-radius: 24px;
  text-align: center;
  transition: all 0.3s;
}
.stat-card:hover {
  border-bottom: 3px solid var(--accent);
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}
.stat-card-title {
  font-weight: 500;
  font-size: 18px;
  color: var(--text-secondary);
}
.stat-card-value {
  font-weight: 700;
  color: var(--accent);
  font-size: 28px;
}
.stat-card.horizontal {
  flex-direction: column;
  align-items: stretch;
  min-width: unset;
  padding: 16px 20px;
}
.stat-card.horizontal h4 {
  margin-bottom: 8px;
  color: var(--text-primary);
}
.stat-card-items {
  display: flex;
  flex-direction: row;
  gap: 16px;
  justify-content: space-around;
  flex-wrap: wrap;
}
.stat-card-item {
  padding: 8px 16px;
  background-color: var(--bg-primary);
  border-radius: 18px;
  min-width: 100px;
}
.stat-card-item .stat-card-title {
  font-size: 14px;
}
.stat-card-item .stat-card-value {
  font-size: 20px;
}

@media (max-width: 800px) {
    .statistics-cards {
        flex-direction: column;
    }
}

/* Выбор мотоцикла и обслуживания */
.actions-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  max-width: 320px;
  margin: 0 auto;
}
.select-action {
  width: 250px;
}

/* Инструкция по ремонту */
.steps {
    margin-bottom: 32px;
}

.manual {
    padding: 18px;
    border-radius: 18px;
    border: 2px solid var(--border-color);
    background-color: var(--bg-secondary);

    margin-bottom: 32px;
}

.manual-title {
    text-align: center;
    margin-bottom: 24px;
}

.manual-step {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.step-wrapper {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 18px;
}

.step-number {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0; /* Не сжимается */

    padding: 24px;
    width: 64px;
    height: 64px;

    background-color: var(--accent);
    border-radius: 50%;

    font-weight: 600;
    font-size: 21px;
}

.step-body {
    width: 100%;
    padding: 18px;
    background-color: var(--bg-primary);

    border-radius: 21px;
    border: 2px solid var(--border-color);
}

.manual-actions {
    margin-top: 24px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;

    margin-bottom: 32px;
}

.manual-actions button {
    width: 100%;
    max-width: 512px;
}

/* Обертка для картинки */
.step-img-wrapper {
    width: 100%;
    max-width: 100%;
    overflow: hidden;
    border-radius: 16px;
}

.step-img {
    width: 100%;
    height: auto;
    max-height: 300px;
    object-fit: cover;
    border-radius: 16px;
    display: block;
}

/* Адаптивность */
@media (max-width: 768px) {
    .step-wrapper {
        flex-direction: column;
        align-items: stretch;
        text-align: center;
    }

    .step-number {
        width: 48px;
        height: 48px;
        padding: 16px;
        font-size: 18px;
        margin: 0 auto;
    }

    .step-img-wrapper {
        max-width: 100%;
    }

    .step-img {
        max-height: 200px;
    }

    .manual {
        padding: 12px;
    }
}

@media (max-width: 480px) {
    .step-number {
        width: 40px;
        height: 40px;
        padding: 12px;
        font-size: 16px;
    }

    .step-body {
        padding: 12px;
        font-size: 14px;
    }

    .step-img {
        max-height: 150px;
    }
}

/* Запись к мастеру */
.record-master {
    padding: 12px;
    border-radius: 21px;
    border: 2px solid var(--border-color);
    background-color: var(--bg-secondary);
    text-align: center;
}

.record-master button {
    width: 100%;
    max-width: 512px;
}
</style>