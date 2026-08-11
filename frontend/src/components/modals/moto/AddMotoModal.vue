<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Добавление мотоцикла"
        subtitle="Заполните информацию о вашем мотоцикле"
        icon="motorcycle"
        bg-icon-color="var(--success-trans)"
        icon-color="var(--success)"
        @close="closeModal"
    >
        <!-- Прогресс-бар -->
        <div class="progress-section">
            <div class="step-indicator">{{ currentStep }} из {{ totalSteps }}</div>
            <div class="progress-bar">
                <div
                    class="progress-fill"
                    :style="{ width: progressPercent + '%' }"
                ></div>
            </div>
        </div>

        <!-- Шаг 1: Основная информация -->
        <div v-if="currentStep === 1" class="step">
            <h3 class="step-title">Основная информация</h3>
            <p class="step-subtitle">Расскажите о своем мотоцикле</p>

            <div class="form-group">
                <label for="motoName">
                    Название <span class="required">*</span>
                </label>
                <input
                    id="motoName"
                    v-model="form.name"
                    type="text"
                    placeholder="Например: Honda CBR600RR"
                    required
                />
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="motoYear">Год выпуска</label>
                    <input
                        id="motoYear"
                        v-model.number="form.years"
                        type="number"
                        placeholder="2020"
                        min="1950"
                        :max="currentYear"
                    />
                </div>
                <div class="form-group">
                    <label for="motoVolume">Объем (см³)</label>
                    <input
                        id="motoVolume"
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
                    <label for="motoMileage">
                        Пробег (км) <span class="required">*</span>
                    </label>
                    <input
                        id="motoMileage"
                        v-model.number="form.mileage"
                        type="number"
                        placeholder="0"
                        min="0"
                        max="1000000"
                        required
                    />
                </div>
                <div class="form-group">
                    <label for="motoColor">Цвет</label>
                    <input
                        id="motoColor"
                        v-model="form.color"
                        type="color"
                        :style="'background-color:' + form.color"
                    />
                </div>
            </div>

            <div class="step-actions">
                <button class="btn btn-secondary" @click="closeModal">
                    Отменить
                </button>
                <button
                    class="btn btn-primary"
                    :disabled="!form.name || !form.mileage || form.mileage <= 0"
                    @click="nextStep"
                >
                    Далее
                </button>
            </div>
        </div>

        <!-- Шаг 2: Документы и фото -->
        <div v-if="currentStep === 2" class="step">
            <h3 class="step-title">Документы и фото</h3>
            <p class="step-subtitle">Добавьте дополнительную информацию</p>

            <div class="form-group">
                <label for="motoPlate">Гос. номер</label>
                <input
                    id="motoPlate"
                    v-model="form.licensePlate"
                    type="text"
                    placeholder="A123BC"
                    maxlength="9"
                />
            </div>

            <div class="form-group">
                <label for="motoVin">VIN (17 символов)</label>
                <input
                    id="motoVin"
                    v-model="form.vin"
                    type="text"
                    placeholder="Введите 17 символов"
                    minlength="17"
                    maxlength="17"
                />
            </div>

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

            <div class="step-actions">
                <button class="btn btn-secondary" @click="prevStep">
                    Назад
                </button>
                <button class="btn btn-primary" @click="nextStep">
                    Далее
                </button>
            </div>
        </div>

        <!-- Шаг 3: Проверка и отправка -->
        <div v-if="currentStep === 3" class="step">
            <h3 class="step-title">Проверьте данные</h3>
            <p class="step-subtitle">Убедитесь, что все верно</p>

            <div class="summary-card">
                <div class="summary-item">
                    <span class="summary-label">Название</span>
                    <span class="summary-value">{{ form.name || '—' }}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Год выпуска</span>
                    <span class="summary-value">{{ form.years || '—' }}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Объем</span>
                    <span class="summary-value">{{ form.volume ? form.volume + ' см³' : '—' }}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Пробег</span>
                    <span class="summary-value">{{ form.mileage ? form.mileage + ' км' : '—' }}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Цвет</span>
                    <span class="summary-value">
                        <span class="color-preview" :style="{ background: form.color }"></span>
                        {{ form.color }}
                    </span>
                </div>
                <div class="summary-item" v-if="form.licensePlate">
                    <span class="summary-label">Гос. номер</span>
                    <span class="summary-value">{{ form.licensePlate }}</span>
                </div>
                <div class="summary-item" v-if="form.vin">
                    <span class="summary-label">VIN</span>
                    <span class="summary-value">{{ form.vin }}</span>
                </div>
                <div class="summary-item" v-if="form.photoFile">
                    <span class="summary-label">Фото</span>
                    <span class="summary-value">✓ Загружено</span>
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

            <div class="step-actions">
                <button class="btn btn-secondary" @click="prevStep">
                    Назад
                </button>
                <button
                    class="btn btn-primary"
                    :disabled="loading"
                    @click="submit"
                >
                    <span v-if="!loading"><i class="fa fa-plus"></i> Добавить</span>
                    <span v-else>Добавление...</span>
                </button>
            </div>
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
            currentStep: 1,
            totalSteps: 3,
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

    computed: {
        progressPercent() {
            return ((this.currentStep - 1) / (this.totalSteps - 1)) * 100;
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
            this.currentStep = 1;
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

        nextStep() {
            if (this.currentStep < this.totalSteps) {
                this.currentStep++;
            }
        },

        prevStep() {
            if (this.currentStep > 1) {
                this.currentStep--;
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
/* Прогресс-бар */
.progress-section {
    margin-bottom: 20px;
}

.step-indicator {
    text-align: center;
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 6px;
}

.progress-bar {
    width: 100%;
    height: 4px;
    background-color: var(--bg-secondary);
    border-radius: 10px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--success), var(--accent));
    transition: width 0.4s ease;
    border-radius: 10px;
}

/* Шаги */
.step {
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.step-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin: 0 0 4px 0;
    color: var(--text-primary);
}

.step-subtitle {
    font-size: 0.9rem;
    color: var(--text-secondary);
    margin: 0 0 12px 0;
}

/* Форма */
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

/* Фото */
.photo-upload-section {
    margin-top: 4px;
}

.photo-upload-section label {
    display: block;
    margin-bottom: 4px;
    font-weight: 600;
    font-size: 0.85rem;
    color: var(--text-secondary);
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

/* Сводка */
.summary-card {
    background: var(--bg-secondary);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
}

.summary-item {
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.summary-item:last-child {
    border-bottom: none;
}

.summary-label {
    font-size: 0.85rem;
    color: var(--text-secondary);
}

.summary-value {
    font-size: 0.9rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 8px;
}

.color-preview {
    width: 24px;
    height: 16px;
    border-radius: 4px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Инфо-блок */
.info-block {
    display: flex;
    padding: 12px;
    background-color: var(--success-trans);
    border-radius: 10px;
    border: 1px solid var(--success-light);
    margin-bottom: 12px;
}

.block-icon {
    color: var(--success);
    font-size: 20px;
    margin-right: 12px;
    flex-shrink: 0;
}

.block-text {
    font-size: 13px;
    color: var(--text-secondary);
    margin: 0;
}

/* Действия */
.step-actions {
    display: flex;
    gap: 10px;
    margin-top: 8px;
}

.step-actions .btn {
    flex: 1;
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

/* ===== АДАПТИВНОСТЬ ===== */

/* Мобильные устройства */
@media (max-width: 640px) {
    .form-row {
        grid-template-columns: 1fr;
        gap: 0;
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

    .step-actions {
        flex-direction: column;
    }

    .step-actions .btn {
        width: 100%;
        padding: 0.8rem;
    }

    .summary-card {
        padding: 12px;
    }

    .summary-item {
        flex-direction: column;
        gap: 2px;
        padding: 8px 0;
    }

    .info-block {
        display: none;
    }

    .block-icon {
        font-size: 18px;
        margin-right: 0;
    }
}

/* Очень маленькие экраны */
@media (max-width: 400px) {
    .step-title {
        font-size: 1rem;
    }

    .step-subtitle {
        font-size: 0.85rem;
    }

    .form-group input {
        font-size: 0.9rem;
        padding: 0.5rem 0.7rem;
    }

    .drop-zone {
        min-height: 70px;
        padding: 10px;
    }
}
</style>