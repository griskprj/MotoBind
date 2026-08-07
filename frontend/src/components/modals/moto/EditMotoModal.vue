<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Редактировать мотоцикл"
        icon="pen"
        @close="closeModal"
    >   
        <div class="inputs-group">
            <label>
                Название *
                <input v-model="form.name" type="text" class="modal-input" required>
            </label>
            
            <div class="inputs-wrapper">
                <label>
                    Объем (см³)
                    <input v-model="form.volume" type="number" min="49" max="4000" class="modal-input">
                </label>
                <label>
                    Пробег (км)
                    <input v-model="form.mileage" type="number" min="0" max="1000000" class="modal-input">
                </label>
            </div>
            <div class="inputs-wrapper">
                <label>
                    Год выпуска
                    <input v-model="form.years" type="number" min="1950" :max="currentYear" class="modal-input">
                </label>
                <label>
                    Гос. номер
                    <input v-model="form.licensePlate" type="text" maxlength="9" class="modal-input">
                </label>
            </div>
            <label>
                VIN (17 символов)
                <input v-model="form.vin" type="text" minlength="17" maxlength="17" class="modal-input">
            </label>
            <label>
                Цвет
                <input v-model="form.color" type="color" :style="'background-color:' + form.color">
            </label>
            
            <!-- Блок фото -->
            <div class="photo-upload-section">
                <label>Фото мотоцикла</label>
                
                <!-- Текущее фото -->
                <div v-if="form.existingPhotoUrl" class="current-photo">
                    <img :src="getPhotoUrl(form.existingPhotoUrl)" alt="Текущее фото" />
                    <button 
                        class="remove-existing-btn"
                        @click="removeExistingPhoto"
                    >
                        <i class="fa fa-times"></i> Удалить фото
                    </button>
                </div>
                
                <!-- Загрузка нового фото -->
                <div 
                    class="drop-zone"
                    :class="{ 'drag-over': isDragging, 'has-file': form.newPhotoFile }"
                    @dragover.prevent="isDragging = true"
                    @dragleave.prevent="isDragging = false"
                    @drop.prevent="handleDrop"
                    @click="$refs.fileInput.click()"
                >
                    <!-- Превью нового фото -->
                    <div v-if="form.newPhotoPreview" class="photo-preview">
                        <img :src="form.newPhotoPreview" alt="Новое фото" />
                        <button 
                            class="remove-photo-btn"
                            @click.stop="removeNewPhoto"
                        >
                            <i class="fa fa-times"></i>
                        </button>
                    </div>
                    
                    <!-- Иконка загрузки -->
                    <div v-else class="drop-zone-content">
                        <i class="fa fa-cloud-upload-alt"></i>
                        <p>Нажмите или перетащите новое фото</p>
                        <span>JPG, PNG, GIF, BMP, WEBP до 10 МБ</span>
                    </div>
                    
                    <input
                        ref="fileInput"
                        type="file"
                        accept="image/*"
                        @change="handleFileSelect"
                        style="display: none"
                    />
                </div>
            </div>
        </div>
        <input v-model="form.id" type="hidden">

        <div class="modal-actions">
            <button @click="closeModal" class="cancel-btn">Отменить</button>
            <button @click="submit" class="save-btn" :disabled="loading">
                <span v-if="!loading"><i class="fa fa-save"></i> Сохранить</span>
                <span v-else>Сохранение...</span>
            </button>
        </div>
    </ModalWrapper>
</template>

<script>
import ModalWrapper from '../ModalWrapper.vue';

export default {
    components: { ModalWrapper },

    props: {
        isOpen: Boolean,
        motorcycle: {
            type: Object,
            default: null
        }
    },

    data() {
        return {
            form: {
                id: null,
                name: '',
                volume: null,
                years: null,
                mileage: null,
                licensePlate: null,
                vin: null,
                color: '#8B5CF6',
                existingPhotoUrl: null,
                newPhotoFile: null,
                newPhotoPreview: null,
                deleteExistingPhoto: false,
            },
            currentYear: new Date().getFullYear(),
            isDragging: false,
            loading: false,
        }
    },

    watch: {
        isOpen(newVal) {
            if (newVal && this.motorcycle) {
                this.loadMotorcycleData()
            }
            if (!newVal) {
                this.cleanupPreview()
            }
        },

        motorcycle: {
            handler(newVal) {
                if (this.isOpen && newVal) {
                    this.loadMotorcycleData()
                }
            },
            deep: true
        }
    },

    methods: {
        getPhotoUrl(photoPath) {
            if (!photoPath) return null
            if (photoPath.startsWith('http')) return photoPath
            const baseUrl = import.meta.env.VITE_API_URL || ''
            return `/uploads/${photoPath}`
        },

        loadMotorcycleData() {
            if (!this.motorcycle) return
            
            this.form = {
                id: this.motorcycle.id,
                name: this.motorcycle.name || '',
                volume: this.motorcycle.volume || null,
                years: this.motorcycle.years || null,
                mileage: this.motorcycle.mileage || null,
                licensePlate: this.motorcycle.license_plate || null,
                vin: this.motorcycle.vin || null,
                color: this.motorcycle.color || '#8B5CF6',
                existingPhotoUrl: this.motorcycle.photo_url || null,
                newPhotoFile: null,
                newPhotoPreview: null,
                deleteExistingPhoto: false,
            }
            this.isDragging = false
            this.loading = false
        },

        cleanupPreview() {
            if (this.form.newPhotoPreview && this.form.newPhotoPreview.startsWith('blob:')) {
                URL.revokeObjectURL(this.form.newPhotoPreview)
            }
        },

        handleFileSelect(event) {
            const file = event.target.files[0]
            if (file) {
                this.processFile(file)
            }
        },

        handleDrop(event) {
            this.isDragging = false
            const file = event.dataTransfer.files[0]
            if (file) {
                this.processFile(file)
            }
        },

        processFile(file) {
            // Проверка размера (10 МБ)
            if (file.size > 10 * 1024 * 1024) {
                alert('Файл слишком большой. Максимальный размер 10 МБ.')
                return
            }
            
            // Проверка типа
            const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp', 'image/webp']
            if (!allowedTypes.includes(file.type)) {
                alert('Неподдерживаемый формат. Разрешены: JPG, PNG, GIF, BMP, WEBP')
                return
            }

            // Очищаем старый preview
            this.cleanupPreview()
            
            this.form.newPhotoFile = file
            this.form.newPhotoPreview = URL.createObjectURL(file)
            // Если загружаем новое фото, отменяем удаление существующего
            this.form.deleteExistingPhoto = false
        },

        removeNewPhoto() {
            this.cleanupPreview()
            this.form.newPhotoFile = null
            this.form.newPhotoPreview = null
            this.$refs.fileInput.value = ''
        },

        removeExistingPhoto() {
            if (!confirm('Удалить текущее фото мотоцикла?')) return
            this.form.deleteExistingPhoto = true
            this.form.existingPhotoUrl = null
        },

        closeModal() {
            this.cleanupPreview()
            this.$emit('close')
        },

        async submit() {
            if (!this.form.name) {
                alert('Введите название мотоцикла')
                return
            }

            if (this.form.years && this.form.years > this.currentYear) {
                alert('Год выпуска не может быть в будущем')
                return
            }

            this.loading = true
            
            try {
                const submitData = {
                    id: this.form.id,
                    name: this.form.name,
                    volume: this.form.volume || null,
                    years: this.form.years || null,
                    mileage: this.form.mileage || null,
                    licensePlate: this.form.licensePlate || null,
                    vin: this.form.vin || null,
                    color: this.form.color || '#8B5CF6',
                    // Фото данные
                    newPhotoFile: this.form.newPhotoFile,
                    deleteExistingPhoto: this.form.deleteExistingPhoto,
                }
                
                await this.$emit('submit', submitData)
                this.closeModal()
            } catch (error) {
                console.error('Submit error:', error)
            } finally {
                this.loading = false
            }
        }
    }
}
</script>

<style scoped>
.inputs-group {
    display: grid;
    grid-template-columns: repeat(1, 1fr);
    gap: 8px;
}

.inputs-wrapper {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
}

/* Стили для фото */
.photo-upload-section {
    margin-top: 4px;
}

.photo-upload-section label {
    display: block;
    margin-bottom: 4px;
    font-weight: 600;
    font-size: 0.9rem;
    color: var(--text-secondary);
}

.current-photo {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 12px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 10px;
    margin-bottom: 12px;
}

.current-photo img {
    width: 80px;
    height: 80px;
    border-radius: 8px;
    object-fit: cover;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.remove-existing-btn {
    padding: 6px 12px;
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 8px;
    color: #ef4444;
    cursor: pointer;
    font-size: 13px;
    transition: 0.2s;
}

.remove-existing-btn:hover {
    background: rgba(239, 68, 68, 0.25);
}

.drop-zone {
    border: 2px dashed rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    min-height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.drop-zone:hover {
    border-color: rgba(124, 58, 237, 0.5);
    background: rgba(124, 58, 237, 0.05);
}

.drop-zone.drag-over {
    border-color: #7c3aed;
    background: rgba(124, 58, 237, 0.1);
}

.drop-zone.has-file {
    border-color: var(--success);
    background: rgba(34, 197, 94, 0.05);
    padding: 8px;
}

.drop-zone-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
}

.drop-zone-content i {
    font-size: 32px;
    color: var(--text-muted);
}

.drop-zone-content p {
    margin: 0;
    font-size: 14px;
    color: var(--text-secondary);
}

.drop-zone-content span {
    font-size: 12px;
    color: var(--text-muted);
}

.photo-preview {
    position: relative;
    width: 100%;
    max-height: 180px;
    overflow: hidden;
    border-radius: 8px;
}

.photo-preview img {
    width: 100%;
    height: auto;
    max-height: 180px;
    object-fit: contain;
    border-radius: 8px;
}

.remove-photo-btn {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: rgba(239, 68, 68, 0.9);
    border: none;
    color: white;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: 0.2s;
}

.remove-photo-btn:hover {
    background: #ef4444;
    transform: scale(1.1);
}

.modal-actions {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
}

.modal-actions button {
    font-weight: 600;
}

.save-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Адаптивность */
@media (max-width: 640px) {
    .inputs-wrapper {
        grid-template-columns: 1fr;
        gap: 8px;
    }
    
    .current-photo {
        flex-direction: column;
        align-items: stretch;
        text-align: center;
    }
    
    .current-photo img {
        width: 100%;
        height: auto;
        max-height: 120px;
    }
    
    .drop-zone {
        min-height: 80px;
        padding: 12px;
    }
    
    .drop-zone-content i {
        font-size: 24px;
    }
}
</style>