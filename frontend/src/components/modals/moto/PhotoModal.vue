<template>
    <ModalWrapper
        :isOpen="isOpen"
        title="Фото мотоцикла"
        subtitle="Загрузите или измените фото мотоцикла"
        icon="camera"
        bg-icon-color="var(--accent-trans)"
        icon-color="var(--accent-text)"
        size="md"
        @close="close"
    >
        <!-- Текущее фото -->
        <div v-if="motorcycle?.photo_url && !selectedFile" class="current-photo">
            <img :src="getPhotoUrl(motorcycle.photo_url)" alt="Мотоцикл" />
            <button class="btn btn-danger" @click="handleDelete">
                <i class="fa fa-trash"></i> Удалить фото
            </button>
        </div>

        <!-- Загрузка нового фото -->
        <div class="upload-section">
            <div
                class="drop-zone"
                :class="{ 'drag-over': isDragging, 'has-file': selectedFile }"
                @dragover.prevent="isDragging = true"
                @dragleave.prevent="isDragging = false"
                @drop.prevent="handleDrop"
                @click="$refs.fileInput.click()"
            >
                <!-- Превью выбранного файла -->
                <div v-if="selectedFile && previewUrl" class="photo-preview">
                    <img :src="previewUrl" alt="Превью" />
                    <button class="remove-photo-btn" @click.stop="clearFile">
                        <i class="fa fa-times"></i>
                    </button>
                </div>

                <!-- Плейсхолдер -->
                <div v-else class="drop-zone-content">
                    <i class="fa fa-cloud-upload-alt"></i>
                    <p>Перетащите фото сюда или кликните для выбора</p>
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

            <!-- Информация о выбранном файле -->
            <div v-if="selectedFile" class="file-info">
                <div class="file-info-icon">
                    <i class="fa fa-file-image-o"></i>
                </div>
                <div class="file-info-content">
                    <span class="file-name">{{ selectedFile.name }}</span>
                    <span class="file-size">{{ formatFileSize(selectedFile.size) }}</span>
                </div>
                <button class="btn-remove-file" @click="clearFile">
                    <i class="fa fa-times"></i>
                </button>
            </div>
        </div>

        <div class="modal-info-block info">
            <div class="modal-info-icon">
                <i class="fa fa-info-circle"></i>
            </div>
            <p class="modal-info-text">
                Рекомендуемый размер: 1200×800 пикселей. Фото будет отображаться в вашем гараже.
            </p>
        </div>

        <!-- Действия -->
        <template #actions>
            <div class="modal-actions">
                <button class="btn btn-secondary" @click="close">
                    Отменить
                </button>
                <button
                    v-if="selectedFile"
                    class="btn btn-primary"
                    :disabled="uploading"
                    @click="handleUpload"
                >
                    <span v-if="!uploading">
                        <i class="fa fa-upload"></i> Загрузить
                    </span>
                    <span v-else>
                        <i class="fa fa-spinner fa-spin"></i> Загрузка...
                    </span>
                </button>
            </div>
        </template>
    </ModalWrapper>
</template>

<script>
import ModalWrapper from '../ModalWrapper.vue'

export default {
    name: 'PhotoModal',

    components: { ModalWrapper },

    props: {
        isOpen: {
            type: Boolean,
            required: true
        },
        motorcycle: {
            type: Object,
            required: true
        }
    },

    data() {
        return {
            selectedFile: null,
            previewUrl: null,
            isDragging: false,
            uploading: false
        }
    },

    watch: {
        isOpen(val) {
            if (!val) {
                this.clearFile()
                this.isDragging = false
            }
        }
    },

    methods: {
        getPhotoUrl(photoPath) {
            if (!photoPath) return null
            if (photoPath.startsWith('http')) return photoPath
            const baseUrl = import.meta.env.VITE_API_URL || ''
            return `${baseUrl}/uploads/${photoPath}`
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

            if (this.previewUrl) {
                URL.revokeObjectURL(this.previewUrl)
            }

            this.selectedFile = file
            this.previewUrl = URL.createObjectURL(file)
        },

        clearFile() {
            if (this.previewUrl) {
                URL.revokeObjectURL(this.previewUrl)
            }
            this.selectedFile = null
            this.previewUrl = null
            if (this.$refs.fileInput) {
                this.$refs.fileInput.value = ''
            }
        },

        formatFileSize(bytes) {
            if (bytes < 1024) return bytes + ' B'
            if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
            return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
        },

        async handleUpload() {
            if (!this.selectedFile) return

            this.uploading = true
            const formData = new FormData()
            formData.append('photo', this.selectedFile)

            try {
                await this.$emit('upload', formData)
                this.clearFile()
            } catch (error) {
                console.error('Upload error:', error)
            } finally {
                this.uploading = false
            }
        },

        async handleDelete() {
            await this.$emit('delete')
        },

        close() {
            this.clearFile()
            this.isDragging = false
            this.$emit('close')
        }
    }
}
</script>

<style scoped>
/* ===== ТЕКУЩЕЕ ФОТО ===== */
.current-photo {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    margin-bottom: 18px;
}

.current-photo img {
    max-width: 100%;
    max-height: 260px;
    border-radius: 12px;
    object-fit: cover;
    border: 1px solid var(--border-light);
}

.current-photo .btn {
    padding: 8px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.btn-danger {
    background: var(--danger-trans);
    color: var(--danger-text);
    border: 1px solid rgba(239, 68, 68, 0.2);
}

.btn-danger:hover {
    background: var(--danger-trans);
    border-color: rgba(239, 68, 68, 0.4);
}

/* ===== DROP ZONE ===== */
.upload-section {
    margin-top: 4px;
}

.drop-zone {
    border: 2px dashed var(--border-color);
    border-radius: 12px;
    padding: 32px 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    min-height: 140px;
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
    min-height: 100px;
}

.drop-zone-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
}

.drop-zone-content i {
    font-size: 40px;
    color: var(--text-muted);
}

.drop-zone-content p {
    margin: 0;
    font-size: 15px;
    color: var(--text-secondary);
}

.drop-zone-content span {
    font-size: 13px;
    color: var(--text-muted);
}

/* ===== ПРЕВЬЮ ===== */
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

/* ===== ИНФО О ФАЙЛЕ ===== */
.file-info {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 14px;
    margin-top: 10px;
    background: var(--bg-secondary);
    border-radius: 8px;
    border: 1px solid var(--border-light);
}

.file-info-icon {
    font-size: 20px;
    color: var(--accent-text);
}

.file-info-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0;
}

.file-name {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.file-size {
    font-size: 12px;
    color: var(--text-muted);
}

.btn-remove-file {
    border-radius: 50%;
    border: none;
    background: var(--danger-trans);
    color: var(--danger-text);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: 0.2s;
    flex-shrink: 0;
}

.btn-remove-file:hover {
    background: var(--danger-trans);
    opacity: 0.8;
}

/* ===== ИНФО-БЛОК ===== */
.modal-info-block {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
    border-radius: 10px;
    margin: 14px 0 4px;
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
    .drop-zone {
        padding: 24px 16px;
        min-height: 110px;
    }

    .drop-zone-content i {
        font-size: 32px;
    }

    .drop-zone-content p {
        font-size: 14px;
    }

    .drop-zone-content span {
        font-size: 12px;
    }

    .photo-preview {
        max-height: 160px;
    }

    .photo-preview img {
        max-height: 160px;
    }

    .current-photo img {
        max-height: 200px;
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

    .file-info {
        flex-wrap: wrap;
        justify-content: center;
        text-align: center;
    }

    .file-info-content {
        width: 100%;
    }

    .file-name {
        white-space: normal;
        text-align: center;
    }
}

@media (max-width: 400px) {
    .drop-zone {
        padding: 16px 12px;
        min-height: 90px;
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
        max-height: 130px;
    }

    .photo-preview img {
        max-height: 130px;
    }

    .current-photo img {
        max-height: 160px;
    }
}
</style>