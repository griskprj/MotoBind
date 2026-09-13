<template>
    <div class="garage-page">
        <LoadingOverlay :isLoading="loading" text="Загрузка гаража..."/>
        
        <div class="container">
            <!-- Header -->
            <Header
                title="Мой гараж"
                subtitle="Управляйте своими мотоциклами и следите за их состоянием"
            />

            <!-- Напоминания -->
            <div v-if="hasActiveReminders" class="reminders-banner">
                <div
                    v-for="reminder in activeRemindersForSelected"
                    :key="reminder.id"
                    class="reminder-item"
                    :class="'reminder-' + reminderBannerInfo(reminder).variant"
                >
                    <div class="reminder-icon">
                        <i :class="reminderBannerInfo(reminder).icon"></i>
                    </div>

                    <div class="reminder-body">
                        <div class="reminder-title">{{ reminderBannerInfo(reminder).title }}</div>
                        <div class="reminder-text">{{ reminderBannerInfo(reminder).text }}</div>
                    </div>

                    <div class="reminder-actions">
                        <button
                            class="reminder-btn primary"
                            @click="handleReminderAction(reminder)"
                        >
                            {{ reminderBannerInfo(reminder).cta }}
                        </button>
                        <button
                            class="reminder-btn ghost danger"
                            @click="dismissReminder(reminder)"
                            title="Скрыть навсегда"
                        >
                            <i class="fa fa-times"></i>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Статистика гаража -->
            <div v-if="motorcycles.length > 0" class="garage-stats">
                <div class="stat-chip">
                    <i class="fa fa-motorcycle"></i>
                    <span>{{ motorcycles.length }}</span>
                    {{ declensionMotorcycles(motorcycles.length) }}
                </div>
                <div class="stat-chip">
                    <i class="fa fa-wrench"></i>
                    <span>{{ totalMaintenances }}</span>
                    обслуживаний
                </div>
                <div class="stat-chip">
                    <i class="fa fa-ruble-sign"></i>
                    <span>{{ formatCost(totalCosts) }}</span>
                </div>
            </div>

            <!-- Мотоциклы - Десктопный список -->
            <div class="motorcycles-container">
                <div class="motorcycles-list">
                    <div 
                        v-for="moto in motorcycles" 
                        :key="moto.id"
                        class="moto-list-item"
                        :class="{ active: selectedMotoId === moto.id }"
                        @click="selectMotorcycle(moto)"
                    >   
                        <div class="moto-card-wrapper">
                            <div class="moto-list-preview">
                                <img 
                                    v-if="moto.photo_url" 
                                    :src="getPhotoUrl(moto.photo_url)" 
                                    :alt="moto.name"
                                    @error="handleImageError"
                                    loading="lazy"
                                >
                                <div v-else class="moto-list-placeholder">
                                    <i class="fa fa-motorcycle"></i>
                                </div>
                            </div>
                            
                            <div class="moto-list-info">
                                <div class="moto-list-header">
                                    <h3 class="moto-list-name">{{ moto.name }}</h3>
                                    <span class="moto-list-year">{{ moto.years }}</span>
                                    <span class="moto-list-volume">{{ moto.volume }} см³</span>
                                </div>
                                <div class="moto-list-meta">
                                    <span class="moto-list-mileage">
                                        <i class="fa-solid fa-gauge-high"></i>
                                        {{ formatMileage(moto.mileage) }}
                                    </span>
                                    <span class="moto-list-color">
                                        <span class="color-dot-sm" :style="{ background: moto.color }"></span>
                                    </span>
                                    <span v-if="moto.maintenances?.length" class="moto-list-maintenances">
                                        <i class="fa fa-wrench"></i>
                                        {{ moto.maintenances.length }}
                                    </span>
                                </div>
                            </div>
                        </div>

                        <div class="moto-list-actions" @click.stop>
                            <button @click="selectMotorcycle(moto); showEditMotoModal = true" class="icon-btn" title="Редактировать">
                                <i class="fa fa-pen"></i>
                            </button>
                            <button @click="selectMotorcycle(moto); showUpdateMotoMileageModal = true" class="icon-btn" title="Обновить пробег">
                                <i class="fa-solid fa-gauge-high"></i>
                            </button>
                            <button @click="selectMotorcycle(moto); showPhotoModal = true" class="icon-btn" title="Фото">
                                <i class="fa fa-camera"></i>
                            </button>
                            <button @click="selectMotorcycle(moto); showDeleteMotoModal = true" class="icon-btn danger" title="Удалить">
                                <i class="fa fa-trash"></i>
                            </button>
                        </div>
                    </div>
                    
                    <button @click="showAddMotoModal = true" class="add-btn btn-secondary">
                        <i class="fa fa-plus"></i>
                        <span>Добавить мотоцикл</span>
                    </button>
                </div>
            </div>

            <!-- Empty State -->
            <div v-if="motorcycles.length === 0" class="empty-state">
                <div class="empty-icon">
                    <i class="fa fa-motorcycle"></i>
                </div>
                <h3>Ваш гараж пуст</h3>
                <p>Добавьте свой первый мотоцикл и начните вести учёт обслуживаний</p>
                <button @click="showAddMotoModal = true" class="btn-primary">
                    Добавить мотоцикл
                </button>
            </div>

            <div v-if="selectedMotorcycle && !selectedMotorcycle.maintenances?.length" class="quick-start-promo">
                <div class="promo-icon">
                    <i class="fa fa-rocket"></i>
                </div>
                <div class="promo-content">
                    <h4>Настройте обслуживание за 30 секунд</h4>
                    <p>Мы автоматически создадим базовое расписание на основе пробега и условий эксплуатации</p>
                </div>
                <button @click="showQuickStartModal = true" class="btn-primary">
                    <i class="fa fa-bolt"></i>
                    Быстрый старт
                </button>
            </div>

            <!-- Детальная информация -->
            <div v-if="selectedMotorcycle" class="moto-detail">
                <!-- Статистика -->
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-icon">
                            <i class="fa-solid fa-gauge-high"></i>
                        </div>
                        <div class="stat-info">
                            <span class="stat-label">Пробег</span>
                            <span class="stat-value">{{ formatMileage(selectedMotorcycle.mileage) }}</span>
                        </div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-icon">
                            <i class="fa fa-wrench"></i>
                        </div>
                        <div class="stat-info">
                            <span class="stat-label">Обслуживаний</span>
                            <span class="stat-value">{{ selectedMotorcycle.maintenances?.length || 0 }}</span>
                        </div>
                    </div>

                    <div class="stat-card" :class="{ 'stat-warning': nextMaintenance?.isOverdue }">
                        <div class="stat-icon">
                            <i class="fa fa-calendar-check"></i>
                        </div>
                        <div class="stat-info">
                            <span class="stat-label">Следующее ТО</span>
                            <span class="stat-value">
                                <template v-if="nextMaintenance">
                                    <span v-if="nextMaintenance.isOverdue" class="text-danger">
                                        <i class="fa fa-exclamation-triangle"></i>
                                        {{ Math.round(nextMaintenance.distanceOverdue) }} км просрочено
                                    </span>
                                    <span v-else>
                                        через {{ Math.round(nextMaintenance.distanceToNext) }} км
                                    </span>
                                </template>
                                <span v-else class="text-muted">Все выполнены</span>
                            </span>
                        </div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-icon">
                            <i class="fa fa-ruble-sign"></i>
                        </div>
                        <div class="stat-info">
                            <span class="stat-label">Расходы на ТО</span>
                            <span class="stat-value">{{ formatCost(maintenanceSpends) }}</span>
                        </div>
                    </div>
                </div>

                <!-- Характеристики и заметки -->
                <div class="detail-grid">
                    <div class="detail-card">
                        <h4 class="detail-title">Характеристики</h4>
                        <div class="spec-list">
                            <div class="spec-item">
                                <span class="spec-label">Год выпуска</span>
                                <span class="spec-value">{{ selectedMotorcycle.years }}</span>
                            </div>
                            <div class="spec-item">
                                <span class="spec-label">Двигатель</span>
                                <span class="spec-value">{{ selectedMotorcycle.volume }} см³</span>
                            </div>
                            <div class="spec-item">
                                <span class="spec-label">Цвет</span>
                                <span class="spec-value">
                                    <span class="color-dot" :style="{ background: selectedMotorcycle.color }"></span>
                                </span>
                            </div>
                            <div class="spec-item">
                                <span class="spec-label">Пробег</span>
                                <span class="spec-value">{{ formatMileage(selectedMotorcycle.mileage) }}</span>
                            </div>
                            <div class="spec-item full" v-if="selectedMotorcycle.vin">
                                <span class="spec-label">VIN</span>
                                <span class="spec-value spec-code">{{ selectedMotorcycle.vin }}</span>
                            </div>
                            <div class="spec-item full" v-if="selectedMotorcycle.license_plate">
                                <span class="spec-label">Гос. номер</span>
                                <span class="spec-value spec-code">{{ selectedMotorcycle.license_plate }}</span>
                            </div>
                        </div>
                    </div>

                    <div class="detail-card notes-card">
                        <div class="detail-header">
                            <h4 class="detail-title">Заметки</h4>
                            <button @click="showEditMotoNoteModal = true" class="icon-btn small" title="Редактировать заметку">
                                <i class="fa fa-pen"></i>
                            </button>
                        </div>
                        <div class="notes-content">
                            <p v-if="selectedMotorcycle.note" class="notes-text">{{ selectedMotorcycle.note }}</p>
                            <p v-else class="notes-empty">
                                <i class="fa fa-pen"></i>
                                Добавьте заметку о мотоцикле
                            </p>
                        </div>
                    </div>
                </div>

                <!-- Обслуживания -->
                <div class="maintenances-section">
                    <div class="section-header">
                        <div class="section-header-left">
                            <i class="fa fa-wrench"></i>
                            <h4>Последние обслуживания</h4>
                        </div>
                        <button @click="$router.push('/maintenance')" class="btn-link">
                            Все записи <i class="fa fa-arrow-right"></i>
                        </button>
                    </div>

                    <div v-if="recentMaintenances.length > 0" class="maintenances-list">
                        <div 
                            v-for="item in recentMaintenances" 
                            :key="item.id"
                            class="maintenance-item"
                            @click="openMaintenanceDetails(item)"
                        >
                            <div class="maint-icon" :class="'maint-icon-' + item.status">
                                <i class="fa fa-wrench"></i>
                            </div>
                            <div class="maint-info">
                                <div class="maint-title">{{ item.title }}</div>
                                <div class="maint-meta">
                                    <span>{{ formatDate(item.completed_date || item.planned_date) }}</span>
                                    <span class="dot">•</span>
                                    <span>{{ item.completed_mileage || item.planned_mileage || '—' }} км</span>
                                    <span class="dot">•</span>
                                    <span>{{ item.cost ? formatCost(item.cost) : '—' }}</span>
                                </div>
                            </div>
                            <div class="maint-status">
                                <span :class="'badge ' + getStatusClass(item.status)">
                                    {{ getStatusLabel(item.status) }}
                                </span>
                                <i class="fa fa-chevron-right"></i>
                            </div>
                        </div>
                    </div>

                    <div v-else class="empty-small">
                        <i class="fa fa-wrench"></i>
                        <p>Нет записей обслуживания</p>
                        <span class="hint">Перейдите в раздел "Обслуживание" чтобы добавить</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- MODALS -->
        <AddMotoModal
            :isOpen="showAddMotoModal"
            @submit="addMoto"
            @close="showAddMotoModal = false"
        />

        <EditMotoModal 
            :isOpen="showEditMotoModal" 
            :motorcycle="selectedMotorcycle"
            @submit="updateMoto" 
            @close="showEditMotoModal=false"
        />

        <UpdateMileageModal
            :isOpen="showUpdateMotoMileageModal"
            :motorcycle="selectedMotorcycle"
            @submit="updateMotoMileage"
            @close="showUpdateMotoMileageModal = false"
        />

        <EditMotoNoteModal
            :isOpen="showEditMotoNoteModal"
            :motorcycle="selectedMotorcycle"
            @submit="updateMotoNote"
            @close="showEditMotoNoteModal = false"
        />

        <DeleteMotoModal 
            :isOpen="showDeleteMotoModal" 
            :motorcycle="selectedMotorcycle" 
            @submit="deleteMoto" 
            @close="showDeleteMotoModal = false" 
        />

        <MaintenanceDetailsModal
            v-if="selectedMotorcycle"
            :isOpen="showDetailsMaintenanceModal"
            :maintenance="selectedMaintenance"
            :motorcycle="selectedMotorcycle"
            @mark="markMaintenance"
            @save="saveMaintenance"
            @delete="deleteMaintenance"
            @close="closeMaintenanceDetails"
        />

        <PhotoModal
            :isOpen="showPhotoModal"
            :motorcycle="selectedMotorcycle"
            @upload="uploadPhoto"
            @delete="deletePhoto"
            @close="showPhotoModal = false"
        />

        <QuickStartModal
            :isOpen="showQuickStartModal"
            :motorcycle="selectedMotorcycle"
            @close="showQuickStartModal = false"
            @created="onQuickStartCreated"
        />
    </div>
</template>

<script>
import Header from '../components/Header.vue';
import AddMotoModal from '../components/modals/moto/AddMotoModal.vue';
import EditMotoModal from '../components/modals/moto/EditMotoModal.vue';
import DeleteMotoModal from '../components/modals/moto/DeleteMotoModal.vue';
import UpdateMileageModal from '../components/modals/moto/UpdateMileageModal.vue';
import EditMotoNoteModal from '../components/modals/moto/EditMotoNoteModal.vue';
import MaintenanceDetailsModal from '../components/modals/maintenance/MaintenanceDetailsModal.vue';
import PhotoModal from '../components/modals/moto/PhotoModal.vue';
import QuickStartModal from '../components/modals/moto/QuickStartModal.vue'
import LoadingOverlay from '../components/LoadingOverlay.vue';

import api from '../api/api.js';
import remindersApi from '../api/reminders.js';
import formatDate from '../utils/DateFormatter.js';

export default {
    components: {
        Header,
        AddMotoModal,
        EditMotoModal,
        DeleteMotoModal,
        UpdateMileageModal,
        EditMotoNoteModal,
        MaintenanceDetailsModal,
        PhotoModal,
        QuickStartModal,
        LoadingOverlay,
    },

    data() {
        return {
            motorcycles: [],
            selectedMotoId: null,
            selectedMaintenance: null,
            loading: false,
            
            showAddMotoModal: false,
            showEditMotoModal: false,
            showDeleteMotoModal: false,
            showUpdateMotoMileageModal: false,
            showEditMotoNoteModal: false,
            showDetailsMaintenanceModal: false,
            showPhotoModal: false,
            showQuickStartModal: false,

            reminders: [],
            loadingReeminders: false,
        }
    },

    computed: {
        selectedMotorcycle() {
            if (!this.selectedMotoId || !this.motorcycles.length) return null;
            return this.motorcycles.find(m => m.id === this.selectedMotoId) || null;
        },

        recentMaintenances() {
            if (!this.selectedMotorcycle?.maintenances) return [];
            return [...this.selectedMotorcycle.maintenances]
                .sort((a, b) => {
                    const da = a.completed_date || a.planned_date || a.created_at;
                    const db = b.completed_date || b.planned_date || b.created_at;
                    return new Date(db) - new Date(da);
                })
                .slice(0, 5);
        },

        nextMaintenance() {
            if (!this.selectedMotorcycle?.maintenances) return null;
            
            const current = this.selectedMotorcycle.mileage || 0;
            const planned = this.selectedMotorcycle.maintenances
                .filter(m => m.status === 'planned' && m.planned_mileage)
                .sort((a, b) => a.planned_mileage - b.planned_mileage);
            
            const overdue = planned.filter(m => m.planned_mileage <= current);
            const upcoming = planned.filter(m => m.planned_mileage > current);
            
            if (overdue.length > 0) {
                const item = overdue[0];
                return {
                    ...item,
                    isOverdue: true,
                    distanceOverdue: current - item.planned_mileage
                };
            }
            
            if (upcoming.length > 0) {
                const item = upcoming[0];
                return {
                    ...item,
                    isOverdue: false,
                    distanceToNext: item.planned_mileage - current
                };
            }
            
            return null;
        },

        maintenanceSpends() {
            if (!this.selectedMotorcycle?.maintenances) return 0;
            return this.selectedMotorcycle.maintenances
                .filter(m => m.status === 'completed')
                .reduce((sum, m) => sum + (m.cost || 0), 0);
        },

        totalMaintenances() {
            return this.motorcycles.reduce((sum, m) => sum + (m.maintenances?.length || 0), 0);
        },

        totalCosts() {
            return this.motorcycles.reduce((sum, m) => {
                return sum + (m.maintenances || [])
                    .filter(mt => mt.status === 'completed')
                    .reduce((s, mt) => s + (mt.cost || 0), 0);
            }, 0);
        },

        activeRemindersForSelected() {
            if (!this.selectedMotoId) return []
            const priority = {
                maintenance_overdue: 0,
                maintenance_soon: 1,
                mileage_update: 2,
            }
            return this.reminders
                .filter(r => r.motorcycle_id === this.selectedMotoId)
                .sort((a, b) => (priority[a.type] ?? 99) - (priority[b.type] ?? 99))
        },

        hasActiveReminders() {
            return this.activeRemindersForSelected.length > 0
        },
    },

    methods: {
        async loadData() {
            try {
                this.loading = true;
                
                const res = await api.get('/motorcycle/');
                this.motorcycles = res.data;
                
                for (const moto of this.motorcycles) {
                    try {
                        const maint = await api.get(`/maintenance/motorcycle/${moto.id}`);
                        moto.maintenances = maint.data || [];
                    } catch {
                        moto.maintenances = [];
                    }
                }
                

                if (this.motorcycles.length > 0 && !this.selectedMotoId) {
                    this.selectedMotoId = this.motorcycles[0].id;
                }

                if (this.selectedMotoId && !this.motorcycles.find(m => m.id === this.selectedMotoId)) {
                    this.selectedMotoId = this.motorcycles[0]?.id || null;
                }

            } catch (err) {
                console.error(err);
            } finally {
                this.loading = false;
            }
        },

        selectMotorcycle(moto) {
            if (!moto || !moto.id) return;
            this.selectedMotoId = moto.id;
        },

        getPhotoUrl(path) {
            if (!path) return null;
            if (path.startsWith('http')) return path;
            return `${import.meta.env.VITE_API_URL || ''}/uploads/${path}`;
        },

        handleImageError(e) {
            e.target.src = '';
            e.target.style.display = 'none';
            const placeholder = e.target.parentElement?.querySelector('.moto-placeholder, .moto-list-placeholder');
            if (placeholder) placeholder.classList.remove('hidden');
        },

        formatMileage(value) {
            if (!value && value !== 0) return '—';
            if (value >= 1000) {
                return (value / 1000).toFixed(1) + ' тыс. км';
            }
            return value + ' км';
        },

        formatCost(value) {
            if (!value) return '0 ₽';
            if (value >= 1000) {
                return (value / 1000).toFixed(1) + ' тыс. ₽';
            }
            return Math.round(value) + ' ₽';
        },

        declensionMotorcycles(count) {
            const last = count % 10;
            const last2 = count % 100;
            if (last2 >= 11 && last2 <= 19) return 'мотоциклов';
            if (last === 1) return 'мотоцикл';
            if (last >= 2 && last <= 4) return 'мотоцикла';
            return 'мотоциклов';
        },

        getMotoStatusClass(moto) {
            if (!moto?.maintenances?.length) return 'status-ok';
            const hasOverdue = moto.maintenances.some(m => m.status === 'overdue');
            if (hasOverdue) return 'status-warning';
            return 'status-ok';
        },

        getMotoStatusLabel(moto) {
            if (!moto?.maintenances?.length) return 'Нет ТО';
            const hasOverdue = moto.maintenances.some(m => m.status === 'overdue');
            if (hasOverdue) return 'Просрочка';
            return 'В порядке';
        },

        async uploadPhoto(formData) {
            try {
                const fd = new FormData();
                fd.append('photo', formData.get('photo'));
                
                const { data } = await api.post(`/motorcycle/${this.selectedMotoId}/photo`, fd, {
                    headers: { 'Content-Type': 'multipart/form-data' }
                });
                
                const idx = this.motorcycles.findIndex(m => m.id === data.id);
                if (idx !== -1) this.motorcycles[idx] = data;
                this.showPhotoModal = false;
                alert('Фото загружено');
            } catch (err) {
                alert(err.response?.data?.error || 'Ошибка загрузки фото');
            }
        },

        async deletePhoto() {
            if (!confirm('Удалить фото?')) return;
            try {
                const { data } = await api.delete(`/motorcycle/${this.selectedMotoId}/photo`);
                const idx = this.motorcycles.findIndex(m => m.id === data.id);
                if (idx !== -1) this.motorcycles[idx] = data;
                this.showPhotoModal = false;
                alert('Фото удалено');
            } catch (err) {
                alert(err.response?.data?.error || 'Ошибка удаления фото');
            }
        },

        async addMoto(formData) {
            try {
                const { photoFile, ...data } = formData;
                const { data: moto } = await api.post('/motorcycle/', data);
                
                if (photoFile) {
                    const fd = new FormData();
                    fd.append('photo', photoFile);
                    await api.post(`/motorcycle/${moto.id}/photo`, fd, {
                        headers: { 'Content-Type': 'multipart/form-data' }
                    });
                }
                
                await this.loadData();
                await this.loadReminders()
                this.selectedMotoId = moto.id;
                this.showAddMotoModal = false;
                alert('Мотоцикл добавлен');
            } catch (err) {
                alert(err.response?.data?.error || 'Ошибка добавления');
            }
        },

        async updateMoto(formData) {
            try {
                this.loading = true;
                const { newPhotoFile, deleteExistingPhoto, ...data } = formData;
                
                await api.put(`/motorcycle/${data.id}`, data);
                
                if (deleteExistingPhoto) {
                    await api.delete(`/motorcycle/${data.id}/photo`);
                }
                
                if (newPhotoFile) {
                    const fd = new FormData();
                    fd.append('photo', newPhotoFile);
                    await api.post(`/motorcycle/${data.id}/photo`, fd, {
                        headers: { 'Content-Type': 'multipart/form-data' }
                    });
                }
                
                await this.loadData();
                await this.loadReminders()
                this.showEditMotoModal = false;
                alert('Мотоцикл обновлен');
            } catch (err) {
                alert(err.response?.data?.error || 'Ошибка обновления');
            } finally {
                this.loading = false;
            }
        },

        async updateMotoMileage(formData) {
            try {
                await api.patch(`/motorcycle/${formData.id}`, formData);
                await this.loadData();
                await this.loadReminders()
                this.showUpdateMotoMileageModal = false;
                alert('Пробег обновлен');
            } catch (err) {
                alert(err.response?.data?.error || 'Ошибка обновления пробега');
            }
        },

        async updateMotoNote(formData) {
            try {
                await api.patch(`/motorcycle/${formData.id}/note`, formData);
                await this.loadData();
                this.showEditMotoNoteModal = false;
                alert('Заметка обновлена');
            } catch (err) {
                alert(err.response?.data?.error || 'Ошибка обновления заметки');
            }
        },

        async deleteMoto(id) {
            try {
                await api.delete(`/motorcycle/${id}`);
                await this.loadData();
                await this.loadReminders()
                if (this.motorcycles.length > 0) {
                    this.selectedMotoId = this.motorcycles[0].id;
                } else {
                    this.selectedMotoId = null;
                }
                this.showDeleteMotoModal = false;
                alert('Мотоцикл удален');
            } catch (err) {
                alert(err.response?.data?.error || 'Ошибка удаления');
            }
        },

        async deleteMaintenance(id) {
            try {
                await api.delete(`/maintenance/${id}`);
                await this.loadData();
                this.showDetailsMaintenanceModal = false;
                alert('Обслуживание удалено');
            } catch (err) {
                alert(err.response?.data?.error || 'Ошибка удаления');
            }
        },

        async markMaintenance(formData) {
            try {
                if (!formData || !formData.id) {
                    console.error('No maintenance ID provided');
                    this.$toast?.error('Ошибка: отсутствует ID обслуживания');
                    return;
                }

                const payload = {
                    completed_mileage: formData.completed_mileage || formData.mileage || 0,
                    completed_date: formData.completed_date || new Date().toISOString().split('T')[0],
                    cost: formData.cost || 0,
                    is_repeat: formData.is_repeat || false,
                    interval: formData.interval || null,
                    interval_days: formData.interval_days || null
                };

                await api.post(`/maintenance/${formData.id}/complete`, payload);
                
                this.$toast?.success('Обслуживание успешно завершено!');
                await this.loadData();
                
                this.selectedMaintenance = null;
            } catch (err) {
                console.error('Failed to complete maintenance:', err);
                const errorMsg = err.response?.data?.error || 'Ошибка при завершении обслуживания';
                this.$toast?.error(errorMsg);
            }
        },

        onQuickStartCreated() {
            this.loadData()
            this.showQuickStartModal = false
        },

        saveMaintenance() {
            this.loadData();
        },

        openMaintenanceDetails(item) {
            this.selectedMaintenance = item;
            this.showDetailsMaintenanceModal = true;
        },

        closeMaintenanceDetails() {
            this.selectedMaintenance = null;
            this.showDetailsMaintenanceModal = false;
        },

        getStatusClass(status) {
            return {
                completed: 'badge-success',
                planned: 'badge-warning',
                overdue: 'badge-danger'
            }[status] || 'badge-gray';
        },

        getStatusLabel(status) {
            return {
                completed: 'Выполнено',
                planned: 'Запланировано',
                overdue: 'Просрочено'
            }[status] || status;
        },

        formatDate(date) {
            return formatDate(date);
        },



        async loadReminders() {
            try {
                this.loadingReminders = true
                const { data } = await remindersApi.getReminders('pending')
                this.reminders = data.reminders || []
            } catch (err) {
                console.error('Failed to load reminders:', err)
            } finally {
                this.loadingReminders = false
            }
        },

        async dismissReminder(reminder) {
            try {
                await remindersApi.dismiss(reminder.id)
                this.reminders = this.reminders.filter(r => r.id !== reminder.id)
            } catch (err) {
                console.error('Failed to dismiss reminder:', err)
                alert('Не удалось скрыть напоминание')
            }
        },

        async snoozeReminder(reminder, days = 7) {
            try {
                const { data } = await remindersApi.snooze(reminder.id, days)
                const idx = this.reminders.findIndex(r => r.id === reminder.id)
                if (idx !== -1) this.reminders[idx] = data.reminder
            } catch (err) {
                console.error('Failed to snooze reminder:', err)
                alert('Не удалось отложить напоминание')
            }
        },

        reminderBannerInfo(reminder) {
            const moto = this.motorcycles.find(m => m.id === reminder.motorcycle_id)
            const motoName = moto?.name || 'мотоцикл'

            switch (reminder.type) {
                case 'mileage_update': {
                    const last = reminder.motorcycle?.mileage || moto?.mileage || 0
                    return {
                        icon: 'fa-solid fa-gauge-high',
                        iconColor: 'warning',
                        title: `Обновите пробег для ${motoName}`,
                        text: `Текущий: ${last} км. Свежие данные помогают точнее напоминать о ТО.`,
                        cta: 'Обновить',
                    }
                }
                case 'maintenance_soon': {
                    const maint = reminder.maintenance
                    return {
                        icon: 'fa fa-wrench',
                        iconColor: 'accent',
                        title: `Скоро ТО: ${maint?.title || 'обслуживание'}`,
                        text: `Запланировано на ${maint?.planned_mileage || '—'} км.`,
                        cta: 'Открыть',
                    }
                }
                case 'maintenance_overdue': {
                    const maint = reminder.maintenance
                    return {
                        icon: 'fa fa-exclamation-triangle',
                        iconColor: 'danger',
                        title: `Просрочено ТО: ${maint?.title || 'обслуживание'}`,
                        text: `Планировалось на ${maint?.planned_mileage || '—'} км.`,
                        cta: 'Открыть',
                    }
                }
                default:
                    return {
                        icon: 'fa fa-bell',
                        iconColor: 'accent',
                        title: 'Напоминание',
                        text: '',
                        cta: 'Открыть',
                    }
            }
        },

        handleReminderAction(reminder) {
            if (reminder.type === 'mileage_update') {
                const moto = this.motorcycles.find(m => m.id === reminder.motorcycle_id)
                if (moto) {
                    this.selectMotorcycle(moto)
                    this.showUpdateMotoMileageModal = true
                }
            } else {
                this.$router.push('/maintenance')
            }
        },
    },

    mounted() {
        this.loadData()
        this.loadReminders()
    }
}
</script>

<style scoped>
.quick-start-promo {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px 24px;
    background: linear-gradient(135deg, var(--accent-trans), rgba(139, 92, 246, 0.05));
    border: 2px solid var(--accent);
    border-radius: 14px;
    margin-bottom: 24px;
}

.promo-icon {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    background: var(--accent);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 var(--accent-trans); }
    50% { transform: scale(1.05); box-shadow: 0 0 0 10px transparent; }
}

.promo-content {
    flex: 1;
    min-width: 0;
}

.promo-content h4 {
    margin: 0 0 4px;
    font-size: 16px;
    color: var(--text-primary);
}

.promo-content p {
    margin: 0;
    font-size: 14px;
    color: var(--text-secondary);
}

@media (max-width: 1020px) {
    .quick-start-promo {
        flex-direction: column;
        text-align: center;
    }
    
    .quick-start-promo .btn-primary {
        width: 100%;
        justify-content: center;
    }
}

/* ===== REMINDERS BANNER ===== */
.reminders-banner {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 20px;
}

.reminder-item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 16px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-left: 3px solid var(--accent);
    border-radius: 12px;
    transition: all 0.2s ease;
}

.reminder-item:hover {
    background: var(--bg-card-hover);
    border-color: var(--border-color);
    border-left-color: var(--accent);
}

.reminder-warning {
    border-left-color: var(--warning);
}

.reminder-danger {
    border-left-color: var(--danger);
}

.reminder-accent {
    border-left-color: var(--accent);
}

.reminder-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: var(--accent-trans);
    color: var(--accent-text);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}

.reminder-warning .reminder-icon {
    background: var(--warning-trans);
    color: var(--warning-text);
}

.reminder-danger .reminder-icon {
    background: var(--danger-trans);
    color: var(--danger-text);
}

.reminder-body {
    flex: 1;
    min-width: 0;
}

.reminder-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 2px;
}

.reminder-text {
    font-size: 13px;
    color: var(--text-secondary);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.reminder-actions {
    display: flex;
    gap: 6px;
    flex-shrink: 0;
}

.reminder-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    font-size: 13px;
    font-weight: 500;
    transition: all 0.2s ease;
    white-space: nowrap;
}

.reminder-btn.primary {
    background: var(--accent);
    color: #fff;
}

.reminder-btn.primary:hover {
    background: var(--accent-hover);
}

.reminder-btn.ghost {
    width: 32px;
    height: 32px;
    padding: 0;
    background: transparent;
    color: var(--text-muted);
    border: 1px solid var(--border-color);
}

.reminder-btn.ghost:hover {
    background: var(--border-light);
    color: var(--text-primary);
}

.reminder-btn.ghost.danger:hover {
    background: var(--danger-trans);
    color: var(--danger-text);
    border-color: var(--danger-trans);
}

/* Мобильная адаптация */
@media (max-width: 640px) {
    .reminder-item {
        flex-wrap: wrap;
        gap: 10px;
    }

    .reminder-body {
        flex-basis: calc(100% - 54px);
    }

    .reminder-text {
        white-space: normal;
    }

    .reminder-actions {
        flex-basis: 100%;
        justify-content: flex-end;
        padding-top: 8px;
        border-top: 1px solid var(--border-light);
    }

    .reminder-btn.primary {
        flex: 1;
        justify-content: center;
    }
}

/* ===== GARAGE STATS ===== */
.garage-stats {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 24px;
}

.stat-chip {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: 20px;
    font-size: 13px;
    color: var(--text-secondary);
    transition: all 0.2s ease;
}

.stat-chip:hover {
    border-color: var(--border-color);
    background: var(--bg-card-hover);
}

.stat-chip i {
    color: var(--accent-text);
    font-size: 14px;
}

.stat-chip span {
    font-weight: 700;
    color: var(--text-primary);
}

/* ===== MOTORCYCLES LIST ===== */
.motorcycles-container {
    margin-bottom: 28px;
}

.motorcycles-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.moto-list-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 12px 16px;
    background: var(--bg-secondary);
    border: 2px solid transparent;
    border-radius: 14px;
    cursor: pointer;
    transition: all 0.25s ease;
}

.moto-list-item:hover {
    background: var(--bg-card-hover);
    border-color: var(--border-light);
}

.moto-list-item.active {
    border-color: var(--accent);
    background: var(--accent-trans);
    box-shadow: 0 0 0 1px var(--accent-trans);
}

.moto-card-wrapper {
    display: flex;
    align-items: center;
    gap: 16px;
    flex: 1;
    min-width: 0;
}

.moto-list-preview {
    position: relative;
    width: 56px;
    height: 56px;
    border-radius: 12px;
    overflow: hidden;
    flex-shrink: 0;
    background: var(--bg-card);
}

.moto-list-preview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.moto-list-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    font-size: 22px;
    background: var(--bg-card);
}

.moto-status-badge {
    position: absolute;
    bottom: 4px;
    right: 4px;
    padding: 1px 8px;
    border-radius: 10px;
    font-size: 9px;
    font-weight: 600;
    backdrop-filter: blur(8px);
    background: rgba(0, 0, 0, 0.7);
    color: #fff;
}

.moto-status-badge.status-warning {
    background: rgba(239, 68, 68, 0.9);
}

.moto-status-badge.status-ok {
    background: rgba(16, 185, 129, 0.9);
}

.moto-list-info {
    flex: 1;
    min-width: 0;
}

.moto-list-header {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}

.moto-list-name {
    font-size: 15px;
    font-weight: 600;
    margin: 0;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.moto-list-year {
    font-size: 13px;
    color: var(--text-muted);
    flex-shrink: 0;
}

.moto-list-volume {
    font-size: 12px;
    color: var(--text-muted);
    background: var(--bg-primary);
    padding: 2px 12px;
    border-radius: 12px;
    flex-shrink: 0;
}

.moto-list-meta {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-top: 3px;
    flex-wrap: wrap;
}

.moto-list-mileage {
    font-size: 13px;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 4px;
}

.moto-list-mileage i {
    font-size: 12px;
    color: var(--text-muted);
}

.moto-list-color {
    display: flex;
    align-items: center;
}

.color-dot-sm {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    border: 1px solid var(--border-color);
    display: block;
    transition: transform 0.2s ease;
}

.moto-list-item:hover .color-dot-sm {
    transform: scale(1.15);
}

.moto-list-maintenances {
    font-size: 12px;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 4px;
}

.moto-list-maintenances i {
    font-size: 12px;
}

.moto-list-actions {
    display: flex;
    gap: 2px;
    flex-shrink: 0;
    opacity: 0.6;
    transition: opacity 0.2s ease;
}

.moto-list-item:hover .moto-list-actions {
    opacity: 1;
}

.add-btn {
    padding: 12px;
    border: 2px dashed var(--border-color);
    border-radius: 14px;
    background: transparent;
    color: var(--text-muted);
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.25s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.add-btn:hover {
    border-color: var(--accent);
    color: var(--accent-text);
    background: var(--accent-trans);
}

/* ===== EMPTY STATE ===== */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 60px 24px;
    background: var(--bg-secondary);
    border: 2px dashed var(--border-color);
    border-radius: 24px;
    text-align: center;
    margin-bottom: 32px;
    transition: all 0.3s ease;
}

.empty-state:hover {
    border-color: var(--border-color);
}

.empty-icon {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: var(--accent-trans);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 36px;
    color: var(--accent-text);
    margin-bottom: 20px;
    transition: transform 0.3s ease;
}

.empty-icon i {
    margin-bottom: 0;
}

.empty-state:hover .empty-icon {
    transform: scale(1.05);
}

.empty-state h3 {
    font-size: 22px;
    margin: 0 0 8px;
    color: var(--text-primary);
}

.empty-state p {
    color: var(--text-muted);
    font-size: 14px;
    margin: 0 0 28px;
}

/* ===== DETAIL SECTION ===== */
.moto-detail {
    margin-top: 28px;
    padding-top: 24px;
    border-top: 1px solid var(--border-light);
}

/* Stats */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
    margin-bottom: 24px;
}

.stat-card {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 16px 20px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: 14px;
    transition: all 0.25s ease;
}

.stat-card:hover {
    border-color: var(--border-color);
    transform: translateY(-2px);
    box-shadow: var(--shadow-sm);
}

.stat-card.stat-warning {
    border-color: var(--danger-trans);
    background: var(--danger-trans);
}

.stat-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: var(--accent-trans);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    color: var(--accent-text);
    flex-shrink: 0;
}

.stat-warning .stat-icon {
    background: var(--danger-trans);
    color: var(--danger-text);
}

.stat-info {
    display: flex;
    flex-direction: column;
    min-width: 0;
}

.stat-label {
    font-size: 11px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.4px;
    font-weight: 600;
}

.stat-value {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-primary);
}

.stat-value.text-danger {
    color: var(--danger);
}

.stat-value .text-muted {
    font-size: 13px;
    font-weight: 400;
    color: var(--text-muted);
}

/* Detail Grid */
.detail-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 24px;
}

.detail-card {
    padding: 20px 24px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: 14px;
    transition: all 0.25s ease;
}

.detail-card:hover {
    border-color: var(--border-color);
}

.notes-card {
    display: flex;
    flex-direction: column;
}

.detail-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
}

.detail-title {
    font-size: 14px;
    font-weight: 600;
    margin: 0;
    color: var(--text-primary);
    letter-spacing: 0.3px;
}

.spec-list {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px 20px;
}

.spec-item {
    display: flex;
    flex-direction: column;
    gap: 2px;
    padding: 6px 0;
}

.spec-item.full {
    grid-column: 1 / -1;
}

.spec-label {
    font-size: 11px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.3px;
    font-weight: 500;
}

.spec-value {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-primary);
    word-break: break-all;
}

.spec-value.spec-code {
    font-family: 'Courier New', monospace;
    font-size: 13px;
    letter-spacing: 0.5px;
    background: var(--bg-primary);
    padding: 4px 10px;
    border-radius: 6px;
    display: inline-block;
}

.color-dot {
    display: inline-block;
    width: 32px;
    height: 16px;
    border-radius: 6px;
    border: 1px solid var(--border-color);
    transition: transform 0.2s ease;
}

.color-dot:hover {
    transform: scale(1.1);
}

.notes-content {
    flex: 1;
    display: flex;
    align-items: flex-start;
    padding-top: 4px;
}

.notes-text {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.7;
}

.notes-empty {
    font-size: 14px;
    color: var(--text-muted);
    font-style: italic;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.notes-empty i {
    color: var(--text-muted);
    font-size: 14px;
}

/* Maintenances */
.maintenances-section {
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 24px;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.section-header-left {
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-header-left i {
    color: var(--accent-text);
    font-size: 18px;
}

.section-header h4 {
    font-size: 15px;
    font-weight: 600;
    margin: 0;
}

.btn-link {
    background: none;
    border: none;
    color: var(--accent-text);
    font-weight: 500;
    font-size: 13px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: all 0.25s ease;
    padding: 6px 12px;
    border-radius: 8px;
}

.btn-link:hover {
    color: var(--accent);
    gap: 10px;
    background: var(--accent-trans);
}

.maintenances-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.maintenance-item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 16px;
    background: var(--bg-primary);
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.maintenance-item:hover {
    background: var(--bg-card-hover);
    transform: translateX(4px);
}

.maint-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-size: 14px;
}

.maint-icon-completed {
    background: var(--success-trans);
    color: var(--success-text);
}

.maint-icon-planned {
    background: var(--warning-trans);
    color: var(--warning-text);
}

.maint-icon-overdue {
    background: var(--danger-trans);
    color: var(--danger-text);
}

.maint-info {
    flex: 1;
    min-width: 0;
}

.maint-title {
    font-weight: 500;
    font-size: 13px;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.maint-meta {
    font-size: 12px;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
}

.maint-meta .dot {
    opacity: 0.3;
}

.maint-status {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
}

.maint-status i {
    color: var(--text-muted);
    font-size: 12px;
    opacity: 0.5;
}

.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 500;
    white-space: nowrap;
}

.badge-success {
    background: var(--success-trans);
    color: var(--success-text);
}

.badge-warning {
    background: var(--warning-trans);
    color: var(--warning-text);
}

.badge-danger {
    background: var(--danger-trans);
    color: var(--danger-text);
}

.badge-gray {
    background: rgba(107, 114, 128, 0.15);
    color: #9ca3af;
}

/* Empty small */
.empty-small {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 32px 16px;
    text-align: center;
}

.empty-small i {
    font-size: 28px;
    color: var(--text-muted);
    margin-bottom: 8px;
    opacity: 0.4;
}

.empty-small p {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
}

.empty-small .hint {
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 4px;
}

/* ===== ICON BTN ===== */
.icon-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    padding: 0;
    border: none;
    border-radius: 8px;
    background: transparent;
    color: var(--text-muted);
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 14px;
    line-height: 1;
    flex-shrink: 0;
}

.icon-btn:hover {
    background: var(--border-light);
    color: var(--text-primary);
}

.icon-btn.danger:hover {
    background: var(--danger-trans);
    color: var(--danger);
}

.icon-btn.small {
    width: 28px;
    height: 28px;
    font-size: 12px;
}

.icon-btn i {
    pointer-events: none;
}

/* ===== MEDIA QUERIES ===== */
@media (max-width: 820px) {
    .page-header {
        flex-direction: column;
        align-items: stretch;
        gap: 12px;
    }
    
    .page-title {
        font-size: 24px;
    }
    
    .btn-primary {
        width: 100%;
        justify-content: center;
        padding: 12px;
    }
    
    .stats-grid {
        grid-template-columns: 1fr 1fr;
    }
    
    .detail-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 600px) {
    .reminder-item {
        flex-wrap: wrap;
        gap: 10px;
    }

    .reminder-body {
        flex-basis: calc(100% - 54px);
    }

    .reminder-text {
        white-space: normal;
    }

    .reminder-actions {
        flex-basis: 100%;
        justify-content: flex-end;
        padding-top: 8px;
        border-top: 1px solid var(--border-light);
    }

    .reminder-btn.primary {
        flex: 1;
        justify-content: center;
    }

    .garage-stats {
        gap: 6px;
    }

    .stat-chip {
        width: 100%;
        font-size: 12px;
        padding: 6px 12px;
    }

    .stats-grid {
        grid-template-columns: 1fr 1fr;
        gap: 8px;
    }
    
    .stat-card {
        padding: 12px 14px;
        gap: 10px;
    }
    
    .stat-icon {
        width: 36px;
        height: 36px;
        font-size: 15px;
    }

    .stat-value {
        font-size: 15px;
    }
    
    .detail-card {
        padding: 14px 16px;
    }
    
    .spec-list {
        grid-template-columns: 1fr 1fr;
        gap: 4px 12px;
    }
    
    .spec-value {
        font-size: 13px;
    }

    .maintenances-section {
        padding: 14px 16px;
    }

    .maintenance-item {
        padding: 10px 12px;
        gap: 10px;
        flex-wrap: wrap;
    }

    .maint-icon {
        width: 32px;
        height: 32px;
        font-size: 12px;
    }

    .maint-title {
        font-size: 12px;
    }

    .maint-meta {
        font-size: 11px;
    }

    .moto-list-item {
        padding: 10px 12px;
        flex-wrap: wrap;
        gap: 10px;
    }

    .moto-list-preview {
        width: 48px;
        height: 48px;
    }

    .moto-list-name {
        font-size: 14px;
    }

    .moto-list-actions {
        opacity: 1;
        width: 100%;
        justify-content: flex-end;
        padding-top: 6px;
        border-top: 1px solid var(--border-light);
    }

    .empty-state {
        padding: 40px 16px;
    }
    
    .empty-icon {
        width: 60px;
        height: 60px;
        font-size: 26px;
    }
    
    .empty-state h3 {
        font-size: 18px;
    }
}

@media (max-width: 400px) {
    .stats-grid {
        grid-template-columns: 1fr;
    }

    .spec-list {
        grid-template-columns: 1fr;
    }

    .moto-list-meta {
        gap: 8px;
    }

    .moto-list-volume {
        font-size: 11px;
        padding: 1px 10px;
    }

    .stat-card {
        padding: 10px 12px;
    }
}
</style>