<template>
    <ModalWrapper
        :isOpen="isOpen"
        title="Добавить мотоцикл"
        subtitle="Заполните информацию о мотоцикле"
        icon="motorcycle"
        bg-icon-color="var(--success-trans)"
        icon-color="var(--success-text)"
        size="md"
        @close="closeModal"
    >
        <!-- Блок 1: Основная информация -->
        <div class="form-section">
            <div class="form-section-title">
                <i class="fa fa-info-circle"></i>
                Основная информация
            </div>

            <div class="modal-form-group">
                <label>
                    Название <span class="required">*</span>
                    <input
                        v-model="form.name"
                        type="text"
                        placeholder="Например: Honda CBR600RR"
                        required
                    />
                </label>
            </div>

            <div class="modal-form-row">
                <div class="modal-form-group">
                    <label>Год выпуска</label>
                    <input
                        v-model.number="form.years"
                        type="number"
                        placeholder="2020"
                        min="1950"
                        :max="currentYear"
                    />
                </div>
                <div class="modal-form-group">
                    <label>Объем (см³)</label>
                    <input
                        v-model.number="form.volume"
                        type="number"
                        placeholder="600"
                        min="49"
                        max="4000"
                    />
                </div>
            </div>

            <div class="modal-form-row">
                <div class="modal-form-group">
                    <label>
                        Пробег (км) <span class="required">*</span>
                        <input
                            v-model.number="form.mileage"
                            type="number"
                            placeholder="0"
                            min="0"
                            max="1000000"
                            required
                        />
                    </label>
                </div>
                <div class="modal-form-group">
                    <label>Цвет</label>
                    <div class="color-picker-wrapper">
                        <input
                            v-model="form.color"
                            type="color"
                            class="color-input"
                        />
                    </div>
                </div>
            </div>
        </div>

        <!-- Блок 2: Документы -->
        <div class="form-section">
            <div class="form-section-title">
                <i class="fa fa-file-text"></i>
                Документы
            </div>

            <div class="modal-form-row">
                <div class="modal-form-group">
                    <label>Гос. номер</label>
                    <input
                        v-model="form.licensePlate"
                        type="text"
                        placeholder="A123BC"
                        maxlength="9"
                    />
                </div>
                <div class="modal-form-group">
                    <label>VIN (17 символов)</label>
                    <input
                        v-model="form.vin"
                        type="text"
                        placeholder="Введите 17 символов"
                        minlength="17"
                        maxlength="17"
                    />
                </div>
            </div>
        </div>

        <!-- Блок 3: Фото -->
        <div class="form-section">
            <div class="form-section-title">
                <i class="fa fa-image"></i>
                Фото мотоцикла
            </div>

            <div 
                class="drop-zone"
                :class="{ 'drag-over': isDragging, 'has-file': form.photoFile }"
                @dragover.prevent="isDragging = true"
                @dragleave.prevent="isDragging = false"
                @drop.prevent="handleDrop"
                @click="$refs.fileInput.click()"
            >
                <!-- Превью -->
                <div v-if="form.photoPreview" class="photo-preview">
                    <img :src="form.photoPreview" alt="Фото мотоцикла" />
                    <button class="remove-photo-btn" @click.stop="removePhoto">
                        <i class="fa fa-times"></i>
                    </button>
                </div>
                
                <!-- Плейсхолдер -->
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

        <!-- Инфо-блок -->
        <div class="modal-info-block info">
            <div class="modal-info-icon">
                <i class="fa fa-lightbulb"></i>
            </div>
            <p class="modal-info-text">
                Эти данные помогут строить статистику и подбирать мануалы для вашего мотоцикла
            </p>
        </div>

        <!-- Действия -->
        <template #actions>
            <div class="modal-actions">
                <button class="btn btn-secondary" @click="closeModal">
                    Отменить
                </button>
                <button
                    class="btn btn-primary"
                    :disabled="!isFormValid || loading"
                    @click="submit"
                >
                    <span v-if="!loading">
                        <i class="fa fa-plus"></i> Добавить мотоцикл
                    </span>
                    <span v-else>
                        <i class="fa fa-spinner fa-spin"></i> Добавление...
                    </span>
                </button>
            </div>
        </template>
    </ModalWrapper>
</template>

<script>
import ModalWrapper from '../ModalWrapper.vue'

export default {
    components: { ModalWrapper },

    props: {
        isOpen: {
            type: Boolean,
            default: false
        }
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
                photoPreview: null
            },
            currentYear: new Date().getFullYear(),
            isDragging: false,
            loading: false
        }
    },

    computed: {
        isFormValid() {
            return this.form.name && 
                   this.form.name.trim().length >= 2 &&
                   this.form.mileage !== null &&
                   this.form.mileage >= 0
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
                photoPreview: null
            }
            this.isDragging = false
            this.loading = false
            if (this.$refs?.fileInput) {
                this.$refs.fileInput.value = ''
            }
        },

        cleanupPreview() {
            if (this.form.photoPreview?.startsWith('blob:')) {
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
            if (this.$refs?.fileInput) {
                this.$refs.fileInput.value = ''
            }
        },

        closeModal() {
            this.cleanupPreview()
            this.$emit('close')
        },

        async submit() {
            if (!this.form.name || this.form.name.trim().length < 2) {
                alert('Введите название мотоцикла (минимум 2 символа)')
                return
            }

            if (this.form.mileage === null || this.form.mileage < 0) {
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
                    name: this.form.name.trim(),
                    volume: this.form.volume || null,
                    years: this.form.years || null,
                    mileage: this.form.mileage || 0,
                    licensePlate: this.form.licensePlate || null,
                    vin: this.form.vin || null,
                    color: this.form.color || '#8B5CF6',
                    photoFile: this.form.photoFile
                }

                await this.$emit('submit', submitData)
                this.resetForm()
                this.$emit('close')
            } catch (error) {
                console.error('Submit error:', error)
                alert('Ошибка при добавлении мотоцикла')
            } finally {
                this.loading = false
            }
        }
    }
}
</script>

<style scoped>
/* ===== СЕКЦИИ ФОРМЫ ===== */
.form-section {
    margin-bottom: 18px;
}

.form-section:last-child {
    margin-bottom: 0;
}

.form-section-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    font-weight: 600;
    color: var(--text-muted);
    margin-bottom: 10px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.form-section-title i {
    color: var(--accent-text);
    font-size: 14px;
}

/* ===== ПОЛЯ ВВОДА ===== */
.modal-form-group {
    margin-bottom: 12px;
}

.modal-form-group:last-child {
    margin-bottom: 0;
}

.modal-form-group label {
    display: block;
    font-weight: 600;
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-bottom: 4px;
}

.modal-form-group label .required {
    color: var(--danger-text);
    font-weight: 700;
}

.modal-form-group input {
    width: 100%;
    padding: 0.6rem 0.8rem;
    border-radius: 10px;
    border: 2px solid var(--border-color);
    background-color: var(--bg-input);
    color: var(--text-primary);
    font-size: 0.95rem;
    transition: all 0.2s;
    box-sizing: border-box;
}

.modal-form-group input:focus {
    border-color: var(--accent);
    outline: none;
    box-shadow: 0 0 0 3px var(--accent-trans);
}

.modal-form-group input::placeholder {
    color: var(--text-muted);
}

.modal-form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}

/* ===== ВЫБОР ЦВЕТА ===== */
.color-picker-wrapper {
    display: flex;
    align-items: center;
    gap: 10px;
}

.color-input {
    width: 44px;
    height: 44px;
    padding: 2px;
    border-radius: 10px;
    border: 2px solid var(--border-color);
    cursor: pointer;
    background: none;
    flex-shrink: 0;
}

.color-hex {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-secondary);
    font-family: monospace;
}

/* ===== ЗАГРУЗКА ФОТО ===== */
.drop-zone {
    border: 2px dashed var(--border-color);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    min-height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    background: var(--bg-secondary);
}

.drop-zone:hover {
    border-color: var(--accent);
    background: var(--accent-trans);
}

.drop-zone.drag-over {
    border-color: var(--accent);
    background: var(--accent-trans);
}

.drop-zone.has-file {
    border-color: var(--success-text);
    background: var(--success-trans);
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
    border-radius: 50%;
    background: rgba(239, 68, 68, 0.9);
    border: none;
    color: #fff;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: 0.2s;
}

.remove-photo-btn:hover {
    background: var(--danger);
    transform: scale(1.1);
}

/* ===== ИНФО-БЛОК ===== */
.modal-info-block {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
    border-radius: 10px;
    margin: 16px 0 4px;
}

.modal-info-block.info {
    background: var(--accent-trans);
    border: 1px solid var(--accent-light);
}

.modal-info-icon {
    font-size: 18px;
    color: var(--accent-text);
    flex-shrink: 0;
    margin-top: 2px;
}

.modal-info-text {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.5;
}

/* ===== КНОПКИ ===== */
.modal-actions {
    display: flex;
    gap: 10px;
}

.modal-actions .btn {
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
    gap: 8px;
}

.modal-actions .btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.btn-primary {
    background: linear-gradient(135deg, var(--accent), var(--accent-hover));
    color: #fff;
}

.btn-primary:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px var(--accent-trans);
}

.btn-secondary {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}

.btn-secondary:hover:not(:disabled) {
    background: var(--border-color);
}

/* ============================================ */
/* ===== АДАПТИВНОСТЬ ===== */
/* ============================================ */

@media (max-width: 640px) {
    .modal-form-row {
        grid-template-columns: 1fr;
        gap: 0;
    }

    .drop-zone {
        min-height: 80px;
        padding: 14px;
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

    .modal-info-block {
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .modal-info-icon {
        margin-top: 0;
    }

    .color-picker-wrapper {
        justify-content: center;
    }

    .form-section-title {
        font-size: 12px;
    }
}

@media (max-width: 400px) {
    .form-section-title {
        font-size: 11px;
    }

    .modal-form-group input {
        font-size: 0.9rem;
        padding: 0.5rem 0.7rem;
    }

    .drop-zone {
        min-height: 70px;
        padding: 10px;
    }

    .color-input {
        width: 38px;
        height: 38px;
    }

    .color-hex {
        font-size: 12px;
    }
}
</style>