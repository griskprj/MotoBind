<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Редактировать мотоцикл"
        subtitle="Измените информацию о вашем мотоцикле"
        icon="pen"
        bg-icon-color="var(--accent-trans)"
        icon-color="var(--accent)"
        @close="closeModal"
    >   
        <!-- Основной контент -->
        <div class="form-group">
            <label for="editMotoName">
                Название <span class="required">*</span>
            </label>
            <input
                id="editMotoName"
                v-model="form.name"
                type="text"
                placeholder="Например: Honda CBR600RR"
                required
            />
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="editMotoYear">Год выпуска</label>
                <input
                    id="editMotoYear"
                    v-model.number="form.years"
                    type="number"
                    placeholder="2020"
                    min="1950"
                    :max="currentYear"
                />
            </div>
            <div class="form-group">
                <label for="editMotoVolume">Объем (см³)</label>
                <input
                    id="editMotoVolume"
                    v-model.number="form.volume"
                    type="number"
                    placeholder="600"
                    min="49"
                    max="4000"
                />
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="editMotoMileage">
                    Пробег (км)
                </label>
                <input
                    id="editMotoMileage"
                    v-model.number="form.mileage"
                    type="number"
                    placeholder="0"
                    min="0"
                    max="1000000"
                />
            </div>
            <div class="form-group">
                <label for="editMotoColor">Цвет</label>
                <input
                    id="editMotoColor"
                    v-model="form.color"
                    type="color"
                    :style="'background-color:' + form.color"
                />
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="editMotoPlate">Гос. номер</label>
                <input
                    id="editMotoPlate"
                    v-model="form.licensePlate"
                    type="text"
                    placeholder="A123BC"
                    maxlength="9"
                />
            </div>
            <div class="form-group">
                <label for="editMotoVin">VIN (17 символов)</label>
                <input
                    id="editMotoVin"
                    v-model="form.vin"
                    type="text"
                    placeholder="Введите 17 символов"
                    minlength="17"
                    maxlength="17"
                />
            </div>
        </div>

        <!-- Блок фото -->
        <div class="photo-upload-section">
            <label>Фото мотоцикла</label>
            
            <!-- Текущее фото -->
            <div v-if="form.existingPhotoUrl && !form.deleteExistingPhoto" class="current-photo">
                <img :src="getPhotoUrl(form.existingPhotoUrl)" alt="Текущее фото" />
                <button 
                    class="remove-existing-btn"
                    @click="removeExistingPhoto"
                >
                    <i class="fa fa-trash"></i> Удалить фото
                </button>
            </div>
            
            <!-- Сообщение об удалении -->
            <div v-else-if="form.deleteExistingPhoto" class="photo-deleted-message">
                <i class="fa fa-check-circle"></i>
                <span>Фото будет удалено при сохранении</span>
                <button class="undo-delete-btn" @click="undoDeletePhoto">
                    Отменить
                </button>
            </div>
            
            <!-- Загрузка нового фото -->
            <div 
                class="drop-zone"
                :class="{ 
                    'drag-over': isDragging, 
                    'has-file': form.newPhotoFile,
                    'has-existing': form.existingPhotoUrl && !form.deleteExistingPhoto
                }"
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
                    <p>
                        {{ form.existingPhotoUrl && !form.deleteExistingPhoto 
                            ? 'Нажмите чтобы заменить фото' 
                            : 'Нажмите или перетащите фото' 
                        }}
                    </p>
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

        <input v-model="form.id" type="hidden">

        <!-- Действия в футере -->
        <div class="modal-actions">
            <button @click="closeModal" class="btn btn-secondary">
                Отменить
            </button>
            <button @click="submit" class="btn btn-primary" :disabled="loading">
                <span v-if="!loading"><i class="fa fa-save"></i> Сохранить</span>
                <span v-else>Сохранение...</span>
            </button>
        </div class="modal-actions">
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
            if (photoPath.startsWith('/uploads/')) {
                return photoPath
            }
            return `${baseUrl}/uploads/${photoPath}`
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
            if (file.size > 10 * 1024 * 1024) {
                alert('Файл слишком большой. Максимальный размер 10 МБ.')
                return
            }
            
            const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp', 'image/webp']
            if (!allowedTypes.includes(file.type)) {
                alert('Неподдерживаемый формат. Разрешены: JPG, PNG, GIF, BMP, WEBP')
                return
            }

            this.cleanupPreview()
            
            this.form.newPhotoFile = file
            this.form.newPhotoPreview = URL.createObjectURL(file)
            this.form.deleteExistingPhoto = false
        },

        removeNewPhoto() {
            this.cleanupPreview()
            this.form.newPhotoFile = null
            this.form.newPhotoPreview = null
            if (this.$refs.fileInput) {
                this.$refs.fileInput.value = ''
            }
        },

        removeExistingPhoto() {
            if (!confirm('Удалить текущее фото мотоцикла?')) return
            this.form.deleteExistingPhoto = true
            this.removeNewPhoto()
        },

        undoDeletePhoto() {
            this.form.deleteExistingPhoto = false
            if (this.motorcycle) {
                this.form.existingPhotoUrl = this.motorcycle.photo_url || null
            }
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
/* ===== ФОРМА ===== */
.form-group {
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin-bottom: 12px;
}

.form-group label {
    font-weight: 600;
    font-size: 0.85rem;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 4px;
}

.required {
    color: var(--danger);
}

.form-group input {
    padding: 0.6rem 0.8rem;
    border-radius: 8px;
    border: 2px solid var(--border-color);
    background-color: var(--bg-secondary);
    color: var(--text-primary);
    font-size: 0.95rem;
    transition: border 0.2s;
    width: 100%;
    box-sizing: border-box;
}

.form-group input:focus {
    border-color: var(--accent);
    outline: none;
    box-shadow: 0 0 0 3px rgba(138, 92, 246, 0.15);
}

.form-group input[type="color"] {
    padding: 2px;
    height: 40px;
    cursor: pointer;
}

.form-group input::placeholder {
    color: var(--text-muted);
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}

/* ===== ФОТО ===== */
.photo-upload-section {
    margin-top: 4px;
}

.photo-upload-section > label {
    display: block;
    margin-bottom: 4px;
    font-weight: 600;
    font-size: 0.85rem;
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
    padding: 6px 14px;
    background: rgba(239, 68, 68, 0.12);
    border: 1px solid rgba(239, 68, 68, 0.25);
    border-radius: 8px;
    color: #ef4444;
    cursor: pointer;
    font-size: 13px;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 6px;
}

.remove-existing-btn:hover {
    background: rgba(239, 68, 68, 0.2);
    border-color: rgba(239, 68, 68, 0.4);
}

.photo-deleted-message {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 14px;
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.2);
    border-radius: 8px;
    margin-bottom: 12px;
    color: #ef4444;
    font-size: 14px;
}

.photo-deleted-message i {
    font-size: 18px;
}

.undo-delete-btn {
    margin-left: auto;
    padding: 4px 12px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    color: var(--text-secondary);
    cursor: pointer;
    font-size: 12px;
    transition: all 0.2s;
}

.undo-delete-btn:hover {
    background: rgba(255, 255, 255, 0.1);
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

.drop-zone.has-existing {
    border-color: rgba(255, 255, 255, 0.1);
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

/* ===== КНОПКИ ДЕЙСТВИЙ ===== */
.modal-actions {
    display: flex;
    gap: 10px;
    margin-top: 4px;
}

.modal-actions .btn {
    width: 100%;
    padding: 0.7rem 1rem;
    border-radius: 40px;
    font-weight: 600;
    font-size: 0.9rem;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
}

.btn-primary {
    background: linear-gradient(135deg, var(--accent), var(--accent-hover));
    color: white;
}

.btn-primary:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(138, 92, 246, 0.3);
}

.btn-primary:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.btn-secondary {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}

.btn-secondary:hover {
    background: var(--border-color);
}

/* ============================================ */
/* ===== АДАПТИВНОСТЬ ===== */
/* ============================================ */

@media (max-width: 640px) {
    .form-row {
        grid-template-columns: 1fr;
        gap: 0;
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
        object-fit: contain;
    }

    .remove-existing-btn {
        justify-content: center;
    }

    .photo-deleted-message {
        flex-wrap: wrap;
        justify-content: center;
        text-align: center;
    }

    .undo-delete-btn {
        margin: 0;
        width: 100%;
        padding: 6px;
    }

    .drop-zone {
        min-height: 80px;
        padding: 12px;
    }

    .drop-zone-content i {
        font-size: 28px;
    }

    .drop-zone-content p {
        font-size: 13px;
    }

    .drop-zone-content span {
        font-size: 11px;
    }

    .photo-preview {
        max-height: 140px;
    }

    .photo-preview img {
        max-height: 140px;
    }

    .modal-actions {
        flex-direction: column;
    }

    .modal-actions .btn {
        width: 100%;
        padding: 0.8rem;
    }
}

@media (max-width: 400px) {
    .form-group input {
        font-size: 0.9rem;
        padding: 0.5rem 0.7rem;
    }

    .drop-zone {
        min-height: 70px;
        padding: 10px;
    }
}

@media (min-width: 641px) and (max-width: 1024px) {
    .form-row {
        gap: 10px;
    }
}
</style>