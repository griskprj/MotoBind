<template>
    <div class="container">
        <!-- === HEADER === -->
        <Header
            title="Гараж"
            subtitle="Управляйте своими мотоциклами"
        />

        <!-- === TABS === -->
        <div class="header-tabs">
            <button class="tab-btn active disable" disabled>Мои мотоциклы</button>
            <button @click="showAddMotoModal = true" class="tab-btn outline">Добавить мотоцикл</button>
        </div>

        <!-- === MOTORCYCLE SELECTOR === -->
        <section class="moto-selector-wrapper">
            <div class="moto-scroll-container">
                <div @click="changeMoto(moto.id)" class="moto-card"
                    v-for="moto in motorcycles"
                    :key="moto.id"
                    :class="motorcycle?.id === moto.id ? 'active' : ''"
                >
                    <div class="moto-card-icon">
                        <img v-if="moto.photo_url" :src="getPhotoUrl(moto.photo_url)" alt="Фото" class="moto-thumb">
                        <img v-else src="/MotoLandingHero.webp" alt="Фото по умолчанию">
                    </div>
                    <div class="moto-card-info">
                        <div class="moto-name">{{ moto.name }}</div>
                        <div class="moto-meta">{{ moto.years }} • {{ moto.mileage }} км</div>
                    </div>
                    <div v-if="motorcycle.id === moto.id" class="moto-active-badge"><i class="fa fa-check"></i></div>
                </div>
                
                <div @click="showAddMotoModal = true" class="moto-card add-card">
                    <i class="fa fa-plus"></i>
                    <span>Добавить</span>
                </div>
            </div>
        </section>

        <!-- === MAIN GRID === -->
        <div v-if="motorcycle" class="main-grid">
            <!-- LEFT COLUMN: Moto Info -->
            <aside class="moto-details-col">
                <div class="big-moto-card">
                    <div class="big-card-header">
                        <span class="big-title">{{ motorcycle.name }}</span>
                    </div>
                    <div class="big-card-header-actions">
                        <button @click="showEditMotoModal = true" class="icon-btn"><i class="fa fa-pen"></i></button>
                        <button @click="showDeleteMotoModal = true" class="icon-btn"><i class="fa fa-trash"></i></button>
                        <button @click="showUpdateMotoMileageModal = true" class="icon-btn"><i class="fa fa-tachometer"></i></button>
                        <button @click="showPhotoModal = true" class="icon-btn"><i class="fa fa-camera"></i></button>
                    </div>
                    <div class="big-card-img" @click="showPhotoModal = true" style="cursor: pointer;">
                        <img 
                            v-if="motorcycle.photo_url" 
                            :src="getPhotoUrl(motorcycle.photo_url)" 
                            alt="Фото мотоцикла"
                            @error="handleImageError"
                        >
                        <img v-else src="/MotoLandingHero.webp" alt="Фото по умолчанию">
                        <div class="photo-overlay">
                            <i class="fa fa-camera"></i>
                            <span>Изменить фото</span>
                        </div>
                    </div>
                    <div class="big-card-grid">
                        <div class="spec-item"><span class="label">Год выпуска</span><span class="value">{{ motorcycle.years }}</span></div>
                        <div class="spec-item"><span class="label">Двигатель</span><span class="value">{{ motorcycle.volume }} см³</span></div>
                        <div class="spec-item"><span class="label">Пробег</span><span class="value">{{ motorcycle.mileage }} км</span></div>
                        <div class="spec-item"><span class="label">Цвет</span><div class="color-dot" :style="{ 'background': motorcycle.color }"></div></div>
                        <div class="spec-item full-width"><span class="label">VIN</span><span class="value">{{ motorcycle.vin ? motorcycle.vin : '--' }}</span></div>
                        <div class="spec-item full-width"><span class="label">Гос. номер</span><span class="value">{{ motorcycle.license_plate ? motorcycle.license_plate : '--' }}</span></div>
                    </div>
                    <div class="notes-block">
                        <div class="notes-header">
                            <span>Заметки</span>
                            <button @click="showEditMotoNoteModal = true" class="icon-btn"><i class="fa fa-pen"></i></button>
                        </div>
                        <div class="note-body">
                            <p v-if="motorcycle.note" class="notes-text">{{ motorcycle.note }}</p>
                            <div v-else class="empty-note-state">
                                <div class="empty-note-header">
                                    <p class="empty-text">
                                        Добавьте заметку. Например: "Мой любимый мотоцикл..."
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </aside>

            <!-- RIGHT COLUMN: Stats & Table -->
            <main class="stats-col">
                <!-- 4 Stats Cards -->
                <div class="stats-grid-4">
                    <div class="stat-box">
                        <div class="stat-head"><i class="fa fa-tachometer"></i> Пробег</div>
                        <div class="stat-val">{{ motorcycle.mileage }} км</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-head"><i class="fa fa-wrench"></i> Обслуживаний</div>
                        <div class="stat-val">{{ motorcycle.maintenances?.length || 0 }}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-head"><i class="fa fa-calendar"></i> Следующее ТО</div>
                        <div class="stat-val">
                            <span v-if="nextMaintenance">
                                <span v-if="nextMaintenance.isOverdue && nextMaintenance.distanceOverdue > 0" style="color: var(--danger);">
                                    Просрочено на {{ nextMaintenance.distanceOverdue }} км
                                </span>
                                <span v-else-if="nextMaintenance.isOverdue && nextMaintenance.distanceOverdue === 0" style="color: var(--danger);">
                                    Просрочено
                                </span>
                                <span v-else>
                                    {{ nextMaintenance.distanceToNext }} км
                                </span>
                                <small style="font-size: 12px; color: var(--text-muted); display: block; font-weight: 400;">
                                    ({{ nextMaintenance.title || 'ТО' }})
                                </small>
                            </span>
                            <span v-else style="font-size: 18px;">Все ТО выполнены</span>
                        </div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-head"><i class="fa fa-ruble"></i> Общие расходы</div>
                        <div class="stat-val">{{ maintenanceSpends }} ₽</div>
                    </div>
                </div>

                <!-- Table -->
                <div v-if="motorcycle && motorcycle.maintenances && motorcycle.maintenances.length > 0" class="maintenance-table-wrapper">
                    <div class="table-header">
                        <span class="th">Дата</span>
                        <span class="th">Обслуживание</span>
                        <span class="th">Пробег</span>
                        <span class="th">Стоимость</span>
                        <span class="th">Статус</span>
                        <span class="th"></span>
                    </div>
                    <div class="table-body">
                        <div class="tr"
                            v-for="maintenance in getRecentMaintenances()"
                            :key="maintenance.id"
                            @click="openMaintenanceDetailsModal(maintenance)"
                        >
                            <div class="td date-cell">
                                <div class="icon-square purple"><i class="fa fa-wrench"></i></div>
                                <span>{{ formatDate(maintenance.completed_date || maintenance.planned_date) }}</span>
                            </div>
                            <div class="td service-cell">
                                <div class="s-title">{{ maintenance.title }}</div>
                                <div class="s-desc">{{ maintenance.description }}</div>
                            </div>
                            <div class="td">{{ maintenance.completed_mileage || maintenance.planned_mileage || '—' }} км</div>
                            <div class="td">{{ maintenance.cost || 0 }} ₽</div>
                            <div class="td">
                                <span :class="getStatusBadgeClass(maintenance.status)">
                                    {{ getStatusLabel(maintenance.status) }}
                                </span>
                            </div>
                            <div class="td action-cell"><i class="fa fa-chevron-right"></i></div>
                        </div>
                    </div>
                    <div class="table-footer">
                        <button @click="this.$router.push('/maintenance')" class="outline-btn" style="width: 100%;">Все записи <i class="fa fa-chevron-right"></i></button>
                    </div>
                </div>
                <!-- Table empty state -->
                <div v-else class="empty-state">
                    <div class="empty-header">
                        <i class="fa fa-wrench"></i>
                        <p class="empty-title">Здесь буду записи обслуживаний</p>
                    </div>
                    <div class="empty-body">
                        <p class="empty-text">
                            Начните вести обслуживание своего мотоцикла
                        </p>
                        <p class="empty-text">
                            Запланировать или добавить запись ТО вы можете на странице <a href="/maintenance">"Обслуживание"</a>
                        </p>
                    </div>
                </div>
            </main>
        </div>
        <div v-else class="empty-state">
            <div class="empty-header">
                <i class="fa fa-motorcycle"></i>
                <p class="empty-title">Мотоциклов пока нет</p>
            </div>
            <div class="empty-body">
                <p class="empty-text">Добавьте первый мотоцикл</p>

            </div>
        </div>
    </div>

    <!-- === MODALS === -->
    <AddMotoModal
        :isOpen="showAddMotoModal"
        @submit="addMoto"
        @close="showAddMotoModal = false"
    />

    <EditMotoModal 
        :isOpen="showEditMotoModal" 
        :motorcycle="motorcycle"
        @submit="updateMoto" 
        @close="showEditMotoModal=false"
    />

    <UpdateMileageModal
        :isOpen="showUpdateMotoMileageModal"
        :motorcycle="motorcycle"
        @submit="updateMotoMileage"
        @close="showUpdateMotoMileageModal = false"
    />

    <EditMotoNoteModal
        :isOpen="showEditMotoNoteModal"
        :motorcycle="motorcycle"
        @submit="updateMotoNote"
        @close="showEditMotoNoteModal = false"
    />

    <DeleteMotoModal 
        :isOpen="showDeleteMotoModal" 
        :motorcycle="motorcycle" 
        @submit="deleteMoto" 
        @close="showDeleteMotoModal = false" 
    />

    <MaintenanceDetailsModal
        v-if="motorcycle"
        :isOpen="showDetailsMaintenanceModal"
        :maintenance="selectedMaintenance"
        :motoName="motorcycle.name"
        @delete="deleteMaintenance"
        @close="closeMaintenanceDetailsModal"
    />

    <!-- Новый модал для фото -->
    <PhotoModal
        :isOpen="showPhotoModal"
        :motorcycle="motorcycle"
        @upload="uploadPhoto"
        @delete="deletePhoto"
        @close="showPhotoModal = false"
    />
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

import api from '../api/api.js'
import formatDate from '../utils/DateFormatter.js'

export default {
    components: {
        AddMotoModal,
        EditMotoModal,
        DeleteMotoModal,
        UpdateMileageModal,
        EditMotoNoteModal,
        MaintenanceDetailsModal,
        PhotoModal,
        Header
    },

    data() {
        return {
            // --- motorcycle ---
            motorcycles: [],
            motorcycle: null,
            selectedMotoId: null,

            // --- maintenance ---
            nextMaintenance: null,
            selectedMaintenance: null,

            // --- modals ---
            showAddMotoModal: false,
            showEditMotoModal: false,
            showDeleteMotoModal: false,
            showUpdateMotoMileageModal: false,
            showEditMotoNoteModal: false,
            showDetailsMaintenanceModal: false,
            showPhotoModal: false,
        }
    },

    methods: {
        async loadData() {
            try {
                const motorcycleResponse = await api.get('/motorcycle/')
                this.motorcycles = motorcycleResponse.data
                
                for (const moto of this.motorcycles) {
                    try {
                        const maintResponse = await api.get(`/maintenance/motorcycle/${moto.id}`)
                        moto.maintenances = maintResponse.data || []
                    } catch (err) {
                        console.error(`Failed load maintenances for moto ${moto.id}:`, err)
                        moto.maintenances = []
                    }
                }
                
                if (this.motorcycles.length > 0) {
                    this.motorcycle = this.motorcycles[0]
                }
            } catch (err) {
                console.error(err)
            }
        },


        async logout() {
            try {
                await api.post('/auth/logout');
            } catch(err) { console.error(err) }
            finally {
                const { removeTokens } = await import('../api/auth');
                removeTokens();
                this.$router.push('/login');
            }
        },

        // === PHOTO ===
        getPhotoUrl(photoPath) {
            if (!photoPath) return null;
            if (photoPath.startsWith('http')) return photoPath;
            const baseUrl = import.meta.env.VITE_API_URL || '';
            return `${baseUrl}/uploads/${photoPath}`;
        },

        handleImageError(event) {
            event.target.src = '/moto_default.jpg';
        },

        async uploadPhoto(formData) {
            try {
                const file = formData.get('photo');
                const uploadFormData = new FormData();
                uploadFormData.append('photo', file);

                const { data } = await api.post(
                    `/motorcycle/${this.motorcycle.id}/photo`,
                    uploadFormData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data',
                        },
                    }
                );

                // Обновляем данные
                const index = this.motorcycles.findIndex(m => m.id === data.id);
                if (index !== -1) {
                    this.motorcycles[index] = data;
                }
                this.motorcycle = data;
                this.showPhotoModal = false;
                alert('Фото успешно загружено!');
            } catch (err) {
                console.error('Failed upload photo:', err);
                alert(err.response?.data?.error || 'Ошибка загрузки фото');
            }
        },

        async deletePhoto() {
            if (!confirm('Удалить фото?')) return;
            
            try {
                const { data } = await api.delete(`/motorcycle/${this.motorcycle.id}/photo`);
                
                const index = this.motorcycles.findIndex(m => m.id === data.id);
                if (index !== -1) {
                    this.motorcycles[index] = data;
                }
                this.motorcycle = data;
                this.showPhotoModal = false;
                alert('Фото удалено');
            } catch (err) {
                console.error('Failed delete photo:', err);
                alert(err.response?.data?.error || 'Ошибка удаления фото');
            }
        },

        // === MOTORCYCLE ===
        async addMoto(formData) {
            try {
                const { photoFile, ...motoData } = formData
                
                const { data } = await api.post('/motorcycle/', motoData)
                
                if (photoFile) {
                    const uploadFormData = new FormData()
                    uploadFormData.append('photo', photoFile)
                    
                    await api.post(`/motorcycle/${data.id}/photo`, uploadFormData, {
                        headers: {
                            'Content-Type': 'multipart/form-data',
                        },
                    })
                    
                    const updatedResponse = await api.get(`/motorcycle/`)
                    this.motorcycles = updatedResponse.data
                    this.motorcycle = this.motorcycles.find(m => m.id === data.id) || this.motorcycles[0]
                } else {
                    this.motorcycles.push(data)
                    this.motorcycle = data
                }

                this.showAddMotoModal = false
                alert('Мотоцикл добавлен!')
            } catch(err) {
                console.error('Failed add moto:', err)
                alert(err.response?.data?.error || 'Ошибка добавления мотоцикла')
            }
        },

        async updateMoto(formData) {
            try {
                this.loading = true
                
                const { newPhotoFile, deleteExistingPhoto, ...motoData } = formData
                
                const { data } = await api.put(`/motorcycle/${motoData.id}`, motoData)
                
                if (deleteExistingPhoto) {
                    await api.delete(`/motorcycle/${motoData.id}/photo`)
                }
                
                if (newPhotoFile) {
                    const uploadFormData = new FormData()
                    uploadFormData.append('photo', newPhotoFile)
                    
                    await api.post(`/motorcycle/${motoData.id}/photo`, uploadFormData, {
                        headers: {
                            'Content-Type': 'multipart/form-data',
                        },
                    })
                }
                
                const index = this.motorcycles.findIndex(m => m.id === motoData.id)
                if (index !== -1) {
                    const updatedResponse = await api.get('/motorcycle/')
                    this.motorcycles = updatedResponse.data
                    this.motorcycle = this.motorcycles.find(m => m.id === motoData.id)
                }
                
                this.showEditMotoModal = false
                alert("Мотоцикл обновлен")
            } catch (err) {
                console.error('Failed update moto:', err)
                alert(err.response?.data?.error || 'Ошибка обновления мотоцикла')
            } finally {
                this.loading = false
            }
        },

        async updateMotoMileage (formData) {
            try {
                const { data } = await api.patch(`motorcycle/${formData.id}`, formData)

                const index = this.motorcycles.findIndex(m => m.id === formData.id)
                if (index !== -1) {
                    this.motorcycles[index] = data
                }

                this.motorcycle = data

                this.showUpdateMotoMileageModal = false
                alert('Пробег мотоцикла обновлен!')
            } catch(err) {
                console.error('Failed update moto mileage', err)
                alert(err.response?.data?.error || 'Ошибка обновления пробега')
            }
        },

        async updateMotoNote(formData) {
            try {
                const { data } = await api.patch(`/motorcycle/${formData.id}/note`, formData)
                
                const index = this.motorcycles.findIndex(m => m.id === formData.id)
                if (index !== -1) {
                    this.motorcycles[index] = data
                }

                this.motorcycle = data

                this.showEditMotoNoteModal = false
            } catch(err) {
                console.error('Failed update moto note', err)
                alert(err.response?.data?.error || 'Ошибка обновления заметки')
            }
        },

        async deleteMoto(motoId) {
            try {
                await api.delete(`/motorcycle/${motoId}`)

                const index = this.motorcycles.findIndex(m => m.id === motoId)
                if (index !== -1) {
                    this.motorcycles.splice(index, 1)
                }

                if (this.motorcycles.length > 0) {
                    this.motorcycle = this.motorcycles[0];
                } else {
                    this.motorcycle = null;
                }
                this.showDeleteMotoModal = false;
                alert("Мотоцикл удален");
            } catch (err) {
                console.error(`Failed delete moto: ${err}`);
                alert(err.response?.data?.error || "Ошибка при удалении мотоцикла");
            } finally {
                this.loading = false;
            }
        },


        async deleteMaintenance(id) {
            try {
                await api.delete(`/maintenance/${id}`);
                
                await this.loadData();
                this.showDetailsMaintenanceModal = false;
                alert("Обслуживание успешно удалено");
            } catch (err) {
                console.error(`Failed delete maintenance: ${err}`);
                alert(err.response?.data?.error || "Ошибка удаления обслуживания");
            }
        },

        getRecentMaintenances() {
            if (!this.motorcycle || !this.motorcycle.maintenances) return [];
            return this.motorcycle.maintenances
                .sort((a, b) => {
                    const dateA = a.completed_date || a.planned_date || a.created_at;
                    const dateB = b.completed_date || b.planned_date || b.created_at;
                    return new Date(dateB) - new Date(dateA);
                })
                .slice(0, 6);
        },

        getStatusBadgeClass(status) {
            const classes = {
                'completed': 'badge-green',
                'planned': 'badge-gray',
                'overdue': 'badge-danger'
            };
            return classes[status] || 'badge-gray';
        },

        getStatusLabel(status) {
            const labels = {
                'completed': 'Выполнено',
                'planned': 'Запланировано',
                'overdue': 'Просрочено'
            };
            return labels[status] || status;
        },

        changeMoto(motoId) {
            this.motorcycle = this.motorcycles.find(m => m.id === motoId) || this.motorcycles[0]
        },

        // === MODALS ===
        openMaintenanceDetailsModal(maintenance) {
            this.selectedMaintenance = maintenance
            this.showDetailsMaintenanceModal = true
        },
        closeMaintenanceDetailsModal() {
            this.selectedMaintenance = null
            this.showDetailsMaintenanceModal = false
        },

        // === UTILS ===
        formatDate(dateString) {
            return formatDate(dateString)
        }
    },

    computed: {
        nextMaintenance() {
            if (!this.motorcycle || !this.motorcycle.maintenances) {
                return null;
            }

            const currentMileage = this.motorcycle.mileage || 0;
            
            const upcomingMaintenances = this.motorcycle.maintenances
                .filter(m => m.status === 'planned' && m.planned_mileage && m.planned_mileage > currentMileage)
                .sort((a, b) => a.planned_mileage - b.planned_mileage);

            const overdueMaintenances = this.motorcycle.maintenances
                .filter(m => m.status === 'planned' && m.planned_mileage && m.planned_mileage <= currentMileage)
                .sort((a, b) => a.planned_mileage - b.planned_mileage);

            if (overdueMaintenances.length > 0) {
                const overdue = overdueMaintenances[0];
                const distanceOverdue = currentMileage - overdue.planned_mileage;
                
                return {
                    ...overdue,
                    distanceOverdue: distanceOverdue,
                    planned_mileage: overdue.planned_mileage,
                    isOverdue: true,
                    title: overdue.title
                };
            }

            if (upcomingMaintenances.length > 0) {
                const next = upcomingMaintenances[0];
                const distanceToNext = next.planned_mileage - currentMileage;
                
                return {
                    ...next,
                    distanceToNext: distanceToNext,
                    planned_mileage: next.planned_mileage,
                    isOverdue: false,
                    title: next.title
                };
            }

            return null;
        },

        maintenanceSpends() {
            if (!this.motorcycle || !this.motorcycle.maintenances) {
                return 0;
            }
            return this.motorcycle.maintenances
                .filter(m => m.status === 'completed')
                .reduce((sum, item) => sum + (item.cost || 0), 0);
        },

    },
    mounted() {
        this.loadData()
    }
}
</script>

<style scoped>
/* Добавляем стили для фото */
.moto-thumb {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    object-fit: cover;
}

.moto-card-icon {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    background: rgba(124, 58, 237, 0.15);
    color: #a78bfa;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    overflow: hidden;
}

.moto-card-icon i {
    font-size: 18px;
}

/* Стили для фото на большой карточке */
.big-card-img {
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 16px;
    cursor: pointer;
}

.big-card-img img {
    width: 100%;
    height: auto;
    display: block;
}

.photo-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
    opacity: 0;
    transition: opacity 0.3s ease;
    color: white;
}

.photo-overlay i {
    font-size: 32px;
}

.photo-overlay span {
    font-size: 14px;
}

.big-card-img:hover .photo-overlay {
    opacity: 1;
}

/* === TABS === */
.header-tabs {
    display: flex;
    gap: 8px;
    margin-bottom: 14px;
}
.tab-btn {
    padding: 8px 20px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    background: transparent;
    color: #8b8b9e;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: 0.2s;
}
.tab-btn.active {
    background: rgba(124, 58, 237, 0.2);
    border-color: #7c3aed;
    color: #a78bfa;
}
.tab-btn.disable {
    cursor: default;
}
.tab-btn.outline:hover {
    background: rgba(124, 58, 237, 0.1);
}
.header-right {
    display: flex;
    align-items: center;
    gap: 16px;
}
.notification-icon {
    font-size: 20px;
    color: #8b8b9e;
    cursor: pointer;
}
.profile-wrapper {
    display: flex;
    align-items: center;
    gap: 6px;
    position: relative;
}
.profile-img {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    border: 2px solid #7c3aed;
}
.dropdown-trigger {
    background: transparent;
    border: none;
    color: #8b8b9e;
    cursor: pointer;
}
.dropdown-list {
    position: absolute;
    top: 48px;
    right: 0;
    background: var(--bg-primary);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 8px;
    min-width: 140px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    z-index: 100;
    animation: slideInUp 0.2s ease;
}
.dropdown-list ul {
    list-style: none;
    margin: 0;
    padding: 0;
}
.dropdown-item {
    width: 100%;
    padding: 8px 12px;
    background: transparent;
    border: none;
    color: #ccc;
    text-align: left;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
}
.dropdown-item:hover {
    background: rgba(255,255,255,0.05);
}

/* ===== MOTORCYCLE SELECTOR ===== */
.moto-selector-wrapper {
    margin-bottom: 24px;
}
.moto-scroll-container {
    display: flex;
    gap: 12px;
    overflow-x: auto;
    padding: 4px 0 8px 0;
    scrollbar-width: thin;
    scrollbar-color: #2d2d3d transparent;
}
.moto-scroll-container::-webkit-scrollbar {
    height: 4px;
}
.moto-scroll-container::-webkit-scrollbar-thumb {
    background: #2d2d3d;
    border-radius: 4px;
}
.moto-card {
    flex: 0 0 220px;
    background: #181824;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 14px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    transition: 0.2s;
}
.moto-card:hover {
    background: #202036;
}
.moto-card.active {
    border-color: #7c3aed;
    background: rgba(124, 58, 237, 0.1);
}
.moto-card.add-card {
    border: 2px dashed rgba(255,255,255,0.1);
    background: transparent;
    justify-content: center;
    color: #7c3aed;
}
.moto-card-info {
    flex: 1;
    overflow: hidden;
}
.moto-name {
    font-size: 14px;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.moto-meta {
    font-size: 12px;
    color: #8b8b9e;
}
.moto-active-badge {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #7c3aed;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    color: #fff;
}

/* ===== MAIN GRID (Adaptive) ===== */
.main-grid {
    display: grid;
    grid-template-columns: 320px 1fr;
    gap: 24px;
    align-items: start;
}

/* LEFT COLUMN */
.big-moto-card {
    background: #181824;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 16px;
    padding: 20px;
}
.big-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}
.big-title {
    font-size: 20px;
    font-weight: 600;
}
.big-card-header-actions {
    display: flex;
    gap: 4px;
    margin-bottom: 16px;
}
.icon-btn {
    background: rgba(255,255,255,0.05);
    border: none;
    color: #8b8b9e;
    width: 32px;
    height: 32px;
    border-radius: 8px;
    cursor: pointer;
    transition: 0.2s;
}
.icon-btn:hover {
    background: rgba(255,255,255,0.1);
    color: #fff;
}
.big-card-img {
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 16px;
    position: relative;
}
.big-card-img img {
    width: 100%;
    height: 200px;
    object-fit: cover;
}
.big-card-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px 16px;
    margin-bottom: 16px;
}
.spec-item {
    display: flex;
    flex-direction: column;
    gap: 2px;
}
.spec-item.full-width {
    grid-column: 1 / -1;
}
.spec-item .label {
    font-size: 12px;
    color: #8b8b9e;
}
.spec-item .value {
    font-size: 14px;
    font-weight: 500;
}
.color-dot {
    width: 40px;
    height: 14px;
    border-radius: 4px;
}
.notes-block {
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    padding: 14px;
}
.notes-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 500;
    font-size: 14px;
    margin-bottom: 6px;
}
.notes-text {
    font-size: 13px;
    color: #8b8b9e;
    margin: 0;
}

/* RIGHT COLUMN */
.stats-grid-4 {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 20px;
}
.stat-box {
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    background: #181824;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}
.stat-head {
    font-size: 13px;
    color: #8b8b9e;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
}
.stat-head i {
    font-size: 16px;
    color: #a78bfa;
}
.stat-val {
    font-size: 22px;
    font-weight: 700;
}

/* ===== TABLE (Fully Responsive) ===== */
.maintenance-table-wrapper {
    background: #181824;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 16px;
    overflow: hidden;
}
.table-header {
    display: grid;
    grid-template-columns: 160px 1fr 90px 100px 120px 40px;
    padding: 12px 16px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 13px;
    color: #8b8b9e;
    font-weight: 500;
}
.table-body {
    display: flex;
    flex-direction: column;
}
.tr {
    display: grid;
    grid-template-columns: 160px 1fr 90px 100px 120px 40px;
    padding: 14px 16px;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.03);
    transition: background-color 0.2s;
    cursor: pointer;
}
.tr:hover {
    background-color: rgba(255,255,255,0.02);
}
.td {
    font-size: 14px;
}
.date-cell {
    display: flex;
    align-items: center;
    gap: 10px;
}
.icon-square {
    width: 30px;
    height: 30px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
}
.icon-square.purple { background: rgba(124, 58, 237, 0.15); color: #a78bfa; }
.icon-square.green { background: rgba(34, 197, 94, 0.15); color: #4ade80; }
.icon-square.blue { background: rgba(59, 130, 246, 0.15); color: #93c5fd; }
.service-cell {
    display: flex;
    flex-direction: column;
}
.s-title { font-weight: 500; }
.s-desc { font-size: 13px; color: #8b8b9e; }
.badge-green {
    display: inline-block;
    padding: 3px 12px;
    background: rgba(34, 197, 94, 0.15);
    color: #4ade80;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
}
.action-cell {
    display: flex;
    justify-content: flex-end;
    color: #4b4b5e;
    transition: color 0.2s;
}
.tr:hover .action-cell { color: #a78bfa; }
.table-footer {
    padding: 16px;
    text-align: center;
}
.show-more {
    background: transparent;
    border: none;
    color: #7c3aed;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}
.show-more:hover { opacity: 0.8; }

/* === EMPTY STATE === */
.empty-note-state {
    background-color: var(--bg-secondary);
    border-radius: 10px;
    border: 2px dashed var(--border-color);
    color: var(--text-secondary);
    font-size: 14px;
    padding: 12px;
    text-align: center;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* ===== MEDIA QUERIES ===== */

/* Планшеты и небольшие ноутбуки (до 1220px) - превращаем в 1 колонку */
@media (max-width: 1220px) {
    .main-grid {
        grid-template-columns: 1fr;
    }
    .moto-details-col {
        max-width: 100%;
    }
    .big-moto-card {
        display: grid;
        grid-template-columns: 240px 1fr;
        gap: 20px;
    }
    .big-card-img {
        grid-row: span 2;
        margin-bottom: 0;
    }
    .big-card-img img {
        height: 100%;
        object-fit: cover;
        margin-bottom: 0;
    }
    .big-card-grid {
        margin-bottom: 0;
    }
    .notes-block {
        grid-column: 1 / -1;
    }
    .stats-grid-4 {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* Телефоны (до 820px) */
@media (max-width: 820px) {
    .header-right {
        display: none;
    }

    .container { padding: 16px; }
    .page-header {
        flex-direction: column;
        align-items: stretch;
        gap: 12px;
    }
    .header-left h2 { margin-bottom: 8px; }
    .header-tabs { flex-wrap: wrap; }
    .header-right {
        justify-content: flex-end;
    }
    .moto-card {
        flex: 0 0 160px;
        padding: 10px 12px;
    }
    .moto-card-icon { 
        width: 32px;
        height: 32px;
    }
    .moto-thumb {
        width: 32px;
        height: 32px;
    }
    .moto-name { font-size: 13px; }
    
    .big-moto-card {
        grid-template-columns: 1fr;
    }
    .big-card-img {
        grid-row: auto;
        margin-bottom: 16px;
    }
    .big-card-img img {
        height: 160px;
        width: 100%;
    }
    .stats-grid-4 {
        grid-template-columns: 1fr 1fr;
    }
    
    /* Мобильная таблица (превращается в карточки) */
    .table-header { display: none; }
    .tr {
        grid-template-columns: 1fr;
        gap: 4px;
        padding: 16px;
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px;
        margin-bottom: 8px;
        background: #0f0f1a;
        position: relative;
    }
    .tr:hover { background: #0f0f1a; }
    .date-cell {
        order: 1;
        margin-bottom: 4px;
    }
    .service-cell {
        order: 2;
        padding-left: 40px;
    }
    .td:not(.date-cell):not(.service-cell):not(.action-cell) {
        order: 3;
        padding-left: 40px;
        font-size: 13px;
    }
    .td:not(.date-cell):not(.service-cell):not(.action-cell)::before {
        content: attr(data-label);
        color: #8b8b9e;
        font-weight: 400;
        margin-right: 4px;
    }
    .td.action-cell {
        order: 4;
        position: absolute;
        right: 16px;
        top: 20px;
    }
    .td.action-cell i { font-size: 16px; }
}

/* Очень маленькие экраны (до 480px) */
@media (max-width: 480px) {
    .stats-grid-4 { grid-template-columns: 1fr; }
    .moto-scroll-container { gap: 8px; }
    .moto-card { flex: 0 0 140px; }
}
</style>