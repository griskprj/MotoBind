<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Добавление мотоцикла"
        subtitle="Заполните информацию о вашем мотоцикле"
        icon="motorcycle"
        bg-icon-color="var(--success-trans)"
        icon-color="var(--success)"
        @close="$emit('close')"
    >
        <div class="modal-group">
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
                
                <!-- Блок загрузки фото -->
                <div class="photo-upload-section">
                    <label>Фото мотоцикла</label>
                    <div 
                        class="drop-zone"
                        :class="{ 'drag-over': isDragging, 'has-file': form.photoFile }"
                        @dragover.prevent="isDragging = true"
                        @dragleave.prevent="isDragging = false"
                        @drop.prevent="handleDrop"
                        @click="$refs.fileInput.click()"
                    >
                        <!-- Превью загруженного фото -->
                        <div v-if="form.photoPreview" class="photo-preview">
                            <img :src="form.photoPreview" alt="Фото мотоцикла" />
                            <button 
                                class="remove-photo-btn"
                                @click.stop="removePhoto"
                            >
                                <i class="fa fa-times"></i>
                            </button>
                        </div>
                        
                        <!-- Иконка загрузки -->
                        <div v-else class="drop-zone-content">
                            <i class="fa fa-cloud-upload-alt"></i>
                            <p>Нажмите или перетащите фото</p>
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
        </div>
        
        <div class="info-block">
            <div class="block-icon">
                <i class="fa fa-info"></i>
            </div>
            <p class="block-text">
                Эта информация поможет точнее строить статистику и подбирать мануалы для вашего мотоцикла.
            </p>
        </div>

        <div class="modal-actions">
            <button @click="closeModal" class="cancel-btn">Отменить</button>
            <button @click="submit" class="accept-btn" :disabled="loading">
                <span v-if="!loading"><i class="fa fa-plus"></i> Добавить</span>
                <span v-else>Добавление...</span>
            </button>
        </div>
    </ModalWrapper>
</template>

<script>
import ModalWrapper from '../ModalWrapper.vue';

export default {
    components: { ModalWrapper },

    props: {
        isOpen: Boolean
    },

    data() {
        return {
            form: {
                name: '',
                volume: null,
                years: null,
                mileage: null,
                licensePlate: null,
                vin: null,
                color: '#8B5CF6',
                photoFile: null,
                photoPreview: null,
            },
            currentYear: new Date().getFullYear(),
            isDragging: false,
            loading: false,
        }
    },

    watch: {
        isOpen(newVal) {
            if (newVal) {
                this.resetForm()
            } else {
                this.cleanupPreview()
            }
        }
    },

    methods: {
        resetForm() {
            this.form = {
                name: '',
                volume: null,
                years: null,
                mileage: null,
                licensePlate: null,
                vin: null,
                color: '#8B5CF6',
                photoFile: null,
                photoPreview: null,
            }
            this.isDragging = false
            this.loading = false
            
            if (this.$refs && this.$refs.fileInput) {
                this.$refs.fileInput.value = ''
            }
        },

        cleanupPreview() {
            if (this.form.photoPreview && this.form.photoPreview.startsWith('blob:')) {
                URL.revokeObjectURL(this.form.photoPreview)
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
            if (file.size > 50 * 1024 * 1024) {
                alert('Файл слишком большой. Максимальный размер 50 МБ.')
                return
            }
            
            const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp', 'image/webp']
            if (!allowedTypes.includes(file.type)) {
                alert('Неподдерживаемый формат. Разрешены: JPG, PNG, GIF, BMP, WEBP')
                return
            }

            this.cleanupPreview()
            
            this.form.photoFile = file
            this.form.photoPreview = URL.createObjectURL(file)
        },

        removePhoto() {
            this.cleanupPreview()
            this.form.photoFile = null
            this.form.photoPreview = null
            
            if (this.$refs && this.$refs.fileInput) {
                this.$refs.fileInput.value = ''
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

            if (!this.form.mileage || this.form.mileage <= 0) {
                alert('Введите корректный пробег')
                return
            }

            if (this.form.years && this.form.years > this.currentYear) {
                alert('Год выпуска не может быть в будущем')
                return
            }

            this.loading = true
            
            try {
                const submitData = {
                    name: this.form.name,
                    volume: this.form.volume || null,
                    years: this.form.years || null,
                    mileage: this.form.mileage || null,
                    licensePlate: this.form.licensePlate || null,
                    vin: this.form.vin || null,
                    color: this.form.color || '#8B5CF6',
                    photoFile: this.form.photoFile,
                }
                
                await this.$emit('submit', submitData)
                this.resetForm()
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

.drop-zone {
    border: 2px dashed rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    min-height: 120px;
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
    font-size: 36px;
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
    max-height: 200px;
    overflow: hidden;
    border-radius: 8px;
}

.photo-preview img {
    width: 100%;
    height: auto;
    max-height: 200px;
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

.info-block {
    display: flex;
    padding: 12px;
    background-color: var(--success-trans);
    border-radius: 10px;
    border: 1px solid var(--success-light);
}

.block-icon {
    color: var(--success);
    font-size: 24px;
    margin-right: 12px;
}

.block-text {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 0;
}

.modal-actions {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
}

.modal-actions button {
    font-weight: 600;
}

.accept-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Адаптивность */
@media (max-width: 640px) {
    .inputs-wrapper {
        grid-template-columns: 1fr;
        gap: 8px;
    }
    
    .drop-zone {
        min-height: 100px;
        padding: 12px;
    }
    
    .drop-zone-content i {
        font-size: 28px;
    }
}
</style>