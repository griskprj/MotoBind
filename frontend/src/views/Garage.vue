<template>
    <div class="garage-page">
        <LoadingOverlay :isLoading="loading" text="Загрузка гаража..."/>
        
        <div class="container">
            <!-- Header -->
            <Header
                title="Мой гараж"
                subtitle="Управляйте своими мотоциклами"
            />

            <!-- Статистика гаража -->
            <div v-if="motorcycles.length > 0" class="garage-stats">
                <div class="stat-chip">
                    <i class="fa fa-motorcycle"></i>
                    <span>{{ motorcycles.length }}</span>
                </div>
                <div class="stat-chip">
                    <i class="fa fa-wrench"></i>
                    <span>{{ totalMaintenances }}</span>
                </div>
                <div class="stat-chip">
                    <i class="fa fa-ruble"></i>
                    <span>{{ totalCosts }} ₽</span>
                </div>
            </div>

            <!-- Мотоциклы -->
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
                                </div>
                                <div class="moto-list-meta">
                                    <span class="moto-list-mileage">{{ formatMileage(moto.mileage) }}</span>
                                    <span class="moto-list-volume">{{ moto.volume }} см³</span>
                                    <span class="moto-list-color">
                                        <span class="color-dot-sm" :style="{ background: moto.color }"></span>
                                    </span>
                                    <span class="moto-list-status" :class="getMotoStatusClass(moto)">
                                        {{ getMotoStatusLabel(moto) }}
                                    </span>
                                </div>
                            </div>
                        </div>

                        <div class="moto-list-actions" @click.stop>
                            <button @click="selectMotorcycle(moto); showEditMotoModal = true" class="icon-btn" title="Редактировать">
                                <i class="fa fa-pen"></i>
                            </button>
                            <button @click="showUpdateMotoMileageModal = true" class="icon-btn" title="Обновить пробег">
                                <i class="fa fa-tachometer"></i>
                            </button>
                            <button @click="selectMotorcycle(moto); showPhotoModal = true" class="icon-btn" title="Фото">
                                <i class="fa fa-camera"></i>
                            </button>
                            <button @click="selectMotorcycle(moto); showDeleteMotoModal = true" class="icon-btn danger" title="Удалить">
                                <i class="fa fa-trash"></i>
                            </button>
                        </div>
                    </div>
                    <button @click="showAddMotoModal = true" class="add-btn outline-btn">
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
                <h3>Мотоциклов пока нет</h3>
                <p>Добавьте свой первый мотоцикл и начните вести учёт</p>
                <button @click="showAddMotoModal = true" class="btn-primary">
                    <i class="fa fa-plus"></i>
                    Добавить мотоцикл
                </button>
            </div>

            <!-- Детальная информация -->
            <div v-if="selectedMotorcycle" class="moto-detail">
                <!-- Статистика -->
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-icon">
                            <i class="fa fa-tachometer"></i>
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
                                        {{ Math.round(nextMaintenance.distanceToNext) }} км
                                    </span>
                                </template>
                                <span v-else class="text-muted">Все выполнены</span>
                            </span>
                        </div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-icon">
                            <i class="fa fa-ruble"></i>
                        </div>
                        <div class="stat-info">
                            <span class="stat-label">Расходы</span>
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

                    <div class="detail-card">
                        <div class="detail-header">
                            <h4 class="detail-title">Заметки</h4>
                            <button @click="showEditMotoNoteModal = true" class="icon-btn small">
                                <i class="fa fa-pen"></i>
                            </button>
                        </div>
                        <div class="notes-content">
                            <p v-if="selectedMotorcycle.note" class="notes-text">{{ selectedMotorcycle.note }}</p>
                            <p v-else class="notes-empty">Добавьте заметку о мотоцикле</p>
                        </div>
                    </div>
                </div>

                <!-- Обслуживания -->
                <div class="maintenances-section">
                    <div class="section-header">
                        <h4>Последние обслуживания</h4>
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
import LoadingOverlay from '../components/LoadingOverlay.vue';

import api from '../api/api.js';
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
        }
    },

    computed: {
        selectedMotorcycle() {
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
        }
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
            const placeholder = e.target.parentElement.querySelector('.moto-placeholder, .moto-list-placeholder');
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
            if (!value) return '0';
            if (value >= 1000) {
                return (value / 1000).toFixed(1) + ' тыс.';
            }
            return value.toString();
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
            if (!moto.maintenances?.length) return 'status-ok';
            const hasOverdue = moto.maintenances.some(m => m.status === 'overdue');
            if (hasOverdue) return 'status-warning';
            return 'status-ok';
        },

        getMotoStatusLabel(moto) {
            if (!moto.maintenances?.length) return 'Нет ТО';
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
            } catch (err) {
                alert(err.response?.data?.error || 'Ошибка обновления заметки');
            }
        },

        async deleteMoto(id) {
            try {
                await api.delete(`/motorcycle/${id}`);
                await this.loadData();
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

                console.log('Sending payload:', payload);

                const { data } = await api.post(`/maintenance/${formData.id}/complete`, payload);
                
                this.showCompleteModal = false;
                this.$toast?.success('Обслуживание успешно завершено!');
                
                await this.loadData();
                
                this.selectedMaintenance = null;
                this.selectedMaintenanceData = null;
            } catch (err) {
                console.error('Failed to complete maintenance:', err);
                const errorMsg = err.response?.data?.error || 'Ошибка при завершении обслуживания';
                this.$toast?.error(errorMsg);
            }
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
        }
    },

    mounted() {
        this.loadData();
    }
}
</script>

<style scoped>
/* ===== BASE ===== */
.garage-page {
    padding: 20px 0 40px;
    max-width: 100%;
    overflow-x: hidden;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 16px;
    overflow-x: hidden;
}

/* ===== HEADER ===== */
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 20px;
}

.header-content {
    flex: 1;
    min-width: 150px;
}

.page-title {
    font-size: 26px;
    font-weight: 700;
    margin: 0;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 10px;
}

.page-title i {
    color: var(--accent-text);
}

.page-subtitle {
    font-size: 14px;
    color: var(--text-muted);
    margin: 2px 0 0;
}

.btn-primary {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    background: var(--accent);
    color: #fff;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    font-size: 14px;
    cursor: pointer;
    transition: 0.2s;
    white-space: nowrap;
}

.btn-primary:hover {
    background: var(--accent-hover);
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(138, 92, 246, 0.25);
}

/* ===== GARAGE STATS ===== */
.garage-stats {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 20px;
}

.stat-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: 20px;
    font-size: 13px;
    color: var(--text-secondary);
}

.stat-chip i {
    color: var(--accent-text);
    font-size: 14px;
}

.stat-chip span {
    font-weight: 600;
    color: var(--text-primary);
}

/* ===== MOTORCYCLES CONTAINER ===== */
.motorcycles-container {
    margin-bottom: 24px;
}

/* ===== ГОРИЗОНТАЛЬНЫЙ СКРОЛЛ (только до 600px) ===== */
.motorcycles-scroll-wrapper {
    display: none;
    overflow-x: auto;
    overflow-y: visible;
    margin: 0 -16px;
    padding: 0 16px 8px;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: thin;
    scrollbar-color: var(--border-color) transparent;
}

.motorcycles-scroll-wrapper::-webkit-scrollbar {
    height: 4px;
}

.motorcycles-scroll-wrapper::-webkit-scrollbar-track {
    background: transparent;
}

.motorcycles-scroll-wrapper::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 4px;
}

.motorcycles-grid {
    display: flex;
    gap: 12px;
    min-width: min-content;
    padding-bottom: 4px;
}

.moto-card {
    display: flex;
    flex-direction: column;
    min-width: 200px;
    max-width: 240px;
    padding: 14px;
    background: var(--bg-secondary);
    border: 2px solid transparent;
    border-radius: 16px;
    cursor: pointer;
    transition: 0.2s;
    flex: 1 0 auto;
}

.moto-card:hover {
    background: var(--bg-card-hover);
    border-color: var(--border-light);
}

.moto-card.active {
    border-color: var(--accent);
    background: var(--accent-trans);
}

.moto-card-wrapper {
    display: flex;
    gap: 12px;
}

.moto-preview {
    position: relative;
    width: 100%;
    aspect-ratio: 16/10;
    border-radius: 12px;
    overflow: hidden;
    flex-shrink: 0;
    background: var(--bg-card);
    margin-bottom: 10px;
}

.moto-preview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.moto-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    font-size: 32px;
    background: var(--bg-card);
}

.moto-placeholder.hidden {
    display: none;
}

.moto-selected {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: var(--accent);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

.moto-status-badge {
    position: absolute;
    bottom: 8px;
    left: 8px;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 10px;
    font-weight: 600;
    backdrop-filter: blur(8px);
    background: rgba(0,0,0,0.6);
    color: #fff;
}

.moto-status-badge.status-warning {
    background: rgba(239, 68, 68, 0.85);
}

.moto-status-badge.status-ok {
    background: rgba(16, 185, 129, 0.85);
}

.moto-info {
    flex: 1;
    min-width: 0;
}

.moto-name {
    font-size: 15px;
    font-weight: 600;
    margin: 0 0 4px;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.moto-details {
    font-size: 12px;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 4px;
    flex-wrap: wrap;
}

.moto-details .dot {
    opacity: 0.3;
}

.moto-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 4px;
}

.moto-volume {
    font-size: 11px;
    color: var(--text-muted);
    background: var(--bg-primary);
    padding: 2px 10px;
    border-radius: 10px;
}

.color-indicator {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    border: 1px solid var(--border-color);
    flex-shrink: 0;
}

.moto-actions {
    display: flex;
    gap: 2px;
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid var(--border-light);
    justify-content: flex-end;
}

/* ===== СПИСОК (от 600px) ===== */
.motorcycles-list {
    display: block;
}

.moto-list-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 10px 16px;
    background: var(--bg-secondary);
    border: 2px solid transparent;
    border-radius: 12px;
    cursor: pointer;
    transition: 0.2s;
    margin-bottom: 6px;
}

.moto-list-item:hover {
    background: var(--bg-card-hover);
    border-color: var(--border-light);
}

.moto-list-item.active {
    border-color: var(--accent);
    background: var(--accent-trans);
}

.moto-list-preview {
    position: relative;
    width: 52px;
    height: 52px;
    border-radius: 10px;
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
    font-size: 20px;
    background: var(--bg-card);
}

.moto-list-placeholder.hidden {
    display: none;
}

.moto-list-info {
    flex: 1;
    min-width: 0;
}

.moto-list-header {
    display: flex;
    align-items: center;
    gap: 10px;
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

.moto-list-meta {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-top: 2px;
    flex-wrap: wrap;
}

.moto-list-mileage {
    font-size: 13px;
    color: var(--text-secondary);
}

.moto-list-volume {
    font-size: 12px;
    color: var(--text-muted);
    background: var(--bg-primary);
    padding: 1px 10px;
    border-radius: 10px;
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
}

.moto-list-status {
    font-size: 11px;
    font-weight: 500;
    padding: 2px 10px;
    border-radius: 12px;
}

.moto-list-status.status-warning {
    background: var(--danger-trans);
    color: var(--danger-text);
}

.moto-list-status.status-ok {
    background: var(--success-trans);
    color: var(--success-text);
}

.moto-list-actions {
    display: flex;
    gap: 4px;
    flex-shrink: 0;
}

.add-btn {
    width: 100%;
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
}

.empty-icon {
    width: 72px;
    height: 72px;
    border-radius: 50%;
    background: var(--accent-trans);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    color: var(--accent-text);
    margin-bottom: 16px;
}

.empty-state h3 {
    font-size: 20px;
    margin: 0 0 8px;
}

.empty-state p {
    color: var(--text-muted);
    font-size: 14px;
    margin: 0 0 24px;
}

/* ===== DETAIL SECTION ===== */
.moto-detail {
    margin-top: 24px;
}

/* Stats */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 12px;
    margin-bottom: 20px;
}

.stat-card {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 16px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: 12px;
    transition: 0.2s;
}

.stat-card:hover {
    border-color: var(--border-color);
}

.stat-card.stat-warning {
    border-color: var(--danger-trans);
    background: var(--danger-trans);
}

.stat-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: var(--accent-trans);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    color: var(--accent-text);
    flex-shrink: 0;
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
    letter-spacing: 0.3px;
}

.stat-value {
    font-size: 17px;
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
    margin-bottom: 20px;
}

.detail-card {
    padding: 18px 20px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: 12px;
}

.detail-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}

.detail-title {
    font-size: 14px;
    font-weight: 600;
    margin: 0;
    color: var(--text-primary);
}

.spec-list {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px 16px;
}

.spec-item {
    display: flex;
    flex-direction: column;
    gap: 1px;
}

.spec-item.full {
    grid-column: 1 / -1;
}

.spec-label {
    font-size: 11px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.2px;
}

.spec-value {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-primary);
    word-break: break-all;
}

.spec-value.spec-code {
    font-family: monospace;
    font-size: 13px;
    letter-spacing: 0.5px;
}

.color-dot {
    display: inline-block;
    width: 28px;
    height: 14px;
    border-radius: 4px;
    border: 1px solid var(--border-color);
}

.notes-content {
    min-height: 50px;
}

.notes-text {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.6;
}

.notes-empty {
    font-size: 14px;
    color: var(--text-muted);
    font-style: italic;
    margin: 0;
}

.btn-mileage {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-top: 12px;
    padding: 6px 14px;
    background: transparent;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    color: var(--text-secondary);
    font-size: 12px;
    cursor: pointer;
    transition: 0.2s;
}

.btn-mileage:hover {
    background: var(--border-light);
    color: var(--text-primary);
}

/* Maintenances */
.maintenances-section {
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 20px;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
}

.section-header h4 {
    font-size: 14px;
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
    gap: 4px;
    transition: 0.2s;
}

.btn-link:hover {
    color: var(--accent);
    gap: 8px;
}

.maintenances-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.maintenance-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 14px;
    background: var(--bg-primary);
    border-radius: 10px;
    cursor: pointer;
    transition: 0.2s;
}

.maintenance-item:hover {
    background: var(--border-light);
}

.maint-icon {
    width: 34px;
    height: 34px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
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
    font-size: 11px;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 4px;
    flex-wrap: wrap;
}

.maint-meta .dot {
    opacity: 0.3;
}

.maint-status {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-shrink: 0;
}

.maint-status i {
    color: var(--text-muted);
    font-size: 11px;
}

.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 10px;
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
    padding: 28px 16px;
    text-align: center;
}

.empty-small i {
    font-size: 24px;
    color: var(--text-muted);
    margin-bottom: 6px;
}

.empty-small p {
    font-size: 13px;
    color: var(--text-secondary);
    margin: 0;
}

.empty-small .hint {
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 2px;
}

/* ===== ICON BTN ===== */
.icon-btn {
    width: 32px;
    height: 32px;
    border: none;
    border-radius: 8px;
    background: transparent;
    color: var(--text-muted);
    cursor: pointer;
    transition: 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
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

/* ===== MEDIA QUERIES ===== */
@media (max-width: 599px) {
    .moto-card {
        min-width: 180px;
        max-width: 210px;
        padding: 12px;
    }

    .moto-list-item {
        display: flex;
        flex-direction: column-reverse;
    }

    .moto-card-wrapper {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .moto-list-actions {
        width: 100%;
    }

    .moto-list-actions .icon-btn {
        width: 100%;
    }

    .moto-preview {
        aspect-ratio: 16/11;
    }

    .moto-name {
        font-size: 14px;
    }

    .moto-details {
        font-size: 11px;
    }

    .moto-actions .icon-btn {
        width: 28px;
        height: 28px;
        font-size: 12px;
    }

    .page-title {
        font-size: 22px;
    }
}

@media (max-width: 500px) {

    .maintenance-item {
        flex-direction: column;
    }

    .maint-icon {
        min-width: 100%;
    }
}

@media (max-width: 480px) {
    .moto-card {
        min-width: 160px;
        max-width: 180px;
        padding: 10px;
    }

    .moto-preview {
        aspect-ratio: 16/12;
        border-radius: 10px;
    }

    .moto-status-badge {
        font-size: 8px;
        padding: 1px 8px;
        bottom: 6px;
        left: 6px;
    }

    .moto-placeholder {
        font-size: 24px;
    }

    .moto-name {
        font-size: 13px;
    }

    .moto-details {
        font-size: 10px;
    }

    .moto-volume {
        font-size: 10px;
        padding: 1px 8px;
    }

    .color-indicator {
        width: 12px;
        height: 12px;
    }
}

@media (min-width: 600px) {
    .moto-list-item {
        padding: 8px 14px;
    }

    .moto-list-preview {
        width: 44px;
        height: 44px;
    }

    .moto-list-placeholder {
        font-size: 16px;
    }

    .moto-list-name {
        font-size: 14px;
    }

    .moto-list-year {
        font-size: 12px;
    }

    .moto-list-mileage {
        font-size: 12px;
    }

    .moto-list-volume {
        font-size: 11px;
        padding: 1px 8px;
    }

    .moto-list-status {
        font-size: 10px;
        padding: 1px 8px;
    }

    .moto-list-actions .icon-btn {
        width: 28px;
        height: 28px;
        font-size: 12px;
    }
}

@media (min-width: 768px) {
    .moto-list-item {
        padding: 10px 18px;
    }

    .moto-list-preview {
        width: 52px;
        height: 52px;
    }

    .moto-list-name {
        font-size: 15px;
    }
}

@media (max-width: 1024px) {
    .detail-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 820px) {
    .page-header {
        flex-direction: column;
        align-items: stretch;
        gap: 10px;
    }
    
    .page-title {
        font-size: 22px;
    }
    
    .btn-primary {
        width: 100%;
        justify-content: center;
        padding: 12px;
    }

    .btn-primary span {
        display: inline;
    }
    
    .stats-grid {
        grid-template-columns: 1fr 1fr;
    }
    
    .stat-card {
        padding: 12px 14px;
    }
    
    .stat-value {
        font-size: 15px;
    }
    
    .spec-list {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 600px) {
    .container {
        padding: 0 12px;
    }
    
    .garage-page {
        padding: 12px 0 24px;
    }
    
    .page-title {
        font-size: 20px;
    }
    
    .page-subtitle {
        font-size: 13px;
    }

    .garage-stats {
        gap: 6px;
    }

    .stat-chip {
        font-size: 12px;
        padding: 4px 12px;
    }

    .stats-grid {
        grid-template-columns: 1fr 1fr;
        gap: 8px;
    }
    
    .stat-card {
        padding: 10px 12px;
        gap: 10px;
    }
    
    .stat-icon {
        width: 34px;
        height: 34px;
        font-size: 14px;
    }

    .stat-value {
        font-size: 14px;
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
        padding: 8px 12px;
        gap: 10px;
    }

    .maint-icon {
        width: 30px;
        height: 30px;
        font-size: 12px;
    }

    .maint-title {
        font-size: 12px;
    }

    .maint-meta {
        font-size: 10px;
    }

    .empty-state {
        padding: 40px 16px;
    }
    
    .empty-icon {
        width: 56px;
        height: 56px;
        font-size: 24px;
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

    .moto-card {
        min-width: 140px;
        max-width: 160px;
        padding: 8px;
    }

    .moto-preview {
        aspect-ratio: 16/13;
        border-radius: 8px;
    }

    .moto-actions .icon-btn {
        width: 24px;
        height: 24px;
        font-size: 10px;
    }

    .moto-actions {
        gap: 0;
    }

    .stat-card {
        padding: 8px 10px;
    }

    .moto-list-item {
    }
}

/* ===== SCROLLBAR STYLING ===== */
.motorcycles-scroll-wrapper {
    scrollbar-width: thin;
    scrollbar-color: var(--border-color) transparent;
}

.motorcycles-scroll-wrapper::-webkit-scrollbar {
    height: 3px;
}

.motorcycles-scroll-wrapper::-webkit-scrollbar-track {
    background: transparent;
}

.motorcycles-scroll-wrapper::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 4px;
}

@media (hover: hover) {
    .motorcycles-scroll-wrapper::-webkit-scrollbar-thumb:hover {
        background: var(--text-muted);
    }
}
</style>