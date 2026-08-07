<template>
    <div v-if="isOpen" class="modal-overlay" @click.self="close">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Фото мотоцикла</h2>
                <button class="close-btn" @click="close"><i class="fa fa-times"></i></button>
            </div>

            <div class="modal-body">
                <!-- Текущее фото -->
                <div v-if="motorcycle?.photo_url" class="current-photo">
                    <img :src="getPhotoUrl(motorcycle.photo_url)" alt="Мотоцикл" />
                    <button class="delete-photo-btn" @click="handleDelete">
                        <i class="fa fa-trash"></i> Удалить фото
                    </button>
                </div>

                <!-- Загрузка нового фото -->
                <div class="upload-section">
                    <div 
                        class="drop-zone"
                        :class="{ 'drag-over': isDragging }"
                        @dragover.prevent="isDragging = true"
                        @dragleave.prevent="isDragging = false"
                        @drop.prevent="handleDrop"
                        @click="$refs.fileInput.click()"
                    >
                        <div class="drop-zone-content">
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

                    <!-- Превью выбранного файла -->
                    <div v-if="selectedFile" class="file-preview">
                        <img :src="previewUrl" alt="Превью" />
                        <div class="file-info">
                            <p><strong>{{ selectedFile.name }}</strong></p>
                            <p>{{ formatFileSize(selectedFile.size) }}</p>
                            <button class="btn btn-danger btn-small" @click="clearFile">
                                <i class="fa fa-times"></i>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Кнопки действий -->
                <div v-if="selectedFile" class="modal-actions">
                    <button class="btn btn-secondary" @click="clearFile">Отмена</button>
                    <button class="btn btn-primary" @click="handleUpload" :disabled="uploading">
                        <span v-if="!uploading"><i class="fa fa-upload"></i> Загрузить</span>
                        <span v-else>Загрузка...</span>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'PhotoModal',
    props: {
        isOpen: {
            type: Boolean,
            required: true,
        },
        motorcycle: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {
            selectedFile: null,
            previewUrl: null,
            isDragging: false,
            uploading: false,
        };
    },
    methods: {
        getPhotoUrl(photoPath) {
            if (!photoPath) return null;
            if (photoPath.startsWith('http')) return photoPath;
            const baseUrl = import.meta.env.VITE_API_URL || '';
            return `${baseUrl}/uploads/${photoPath}`;
        },
        handleFileSelect(event) {
            const file = event.target.files[0];
            if (file) {
                this.processFile(file);
            }
        },
        handleDrop(event) {
            this.isDragging = false;
            const file = event.dataTransfer.files[0];
            if (file) {
                this.processFile(file);
            }
        },
        processFile(file) {
            // Проверка размера (10 МБ)
            if (file.size > 10 * 1024 * 1024) {
                alert('Файл слишком большой. Максимальный размер 10 МБ.');
                return;
            }
            
            // Проверка типа
            const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp', 'image/webp'];
            if (!allowedTypes.includes(file.type)) {
                alert('Неподдерживаемый формат. Разрешены: JPG, PNG, GIF, BMP, WEBP');
                return;
            }

            this.selectedFile = file;
            this.previewUrl = URL.createObjectURL(file);
        },
        clearFile() {
            this.selectedFile = null;
            this.previewUrl = null;
            this.$refs.fileInput.value = '';
        },
        formatFileSize(bytes) {
            if (bytes < 1024) return bytes + ' B';
            if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
            return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
        },
        async handleUpload() {
            if (!this.selectedFile) return;
            
            this.uploading = true;
            const formData = new FormData();
            formData.append('photo', this.selectedFile);
            
            try {
                await this.$emit('upload', formData);
                this.clearFile();
            } catch (error) {
                console.error('Upload error:', error);
            } finally {
                this.uploading = false;
            }
        },
        async handleDelete() {
            await this.$emit('delete');
        },
        close() {
            this.clearFile();
            this.isDragging = false;
            this.$emit('close');
        },
    },
    watch: {
        isOpen(val) {
            if (!val) {
                this.clearFile();
                this.isDragging = false;
            }
        },
    },
};
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(8px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 20px;
}

.modal-content {
    background: #181824;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 16px;
    max-width: 600px;
    width: 100%;
    max-height: 90vh;
    overflow-y: auto;
    animation: slideIn 0.3s ease;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 24px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.modal-header h2 {
    margin: 0;
    font-size: 20px;
}

.close-btn {
    background: transparent;
    border: none;
    color: #8b8b9e;
    font-size: 20px;
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 8px;
    transition: 0.2s;
}

.close-btn:hover {
    background: rgba(255,255,255,0.05);
    color: #fff;
}

.modal-body {
    padding: 24px;
}

.current-photo {
    margin-bottom: 24px;
    text-align: center;
}

.current-photo img {
    max-width: 100%;
    max-height: 300px;
    border-radius: 12px;
    object-fit: cover;
    border: 1px solid rgba(255,255,255,0.05);
}

.delete-photo-btn {
    margin-top: 12px;
    padding: 8px 16px;
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 8px;
    color: #ef4444;
    cursor: pointer;
    transition: 0.2s;
    font-size: 14px;
}

.delete-photo-btn:hover {
    background: rgba(239, 68, 68, 0.25);
}

.upload-section {
    margin-top: 16px;
}

.drop-zone {
    border: 2px dashed rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 40px 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
}

.drop-zone:hover {
    border-color: rgba(124, 58, 237, 0.5);
    background: rgba(124, 58, 237, 0.05);
}

.drop-zone.drag-over {
    border-color: #7c3aed;
    background: rgba(124, 58, 237, 0.1);
}

.drop-zone-content i {
    font-size: 48px;
    color: #7c3aed;
    margin-bottom: 12px;
}

.drop-zone-content p {
    margin: 0 0 4px 0;
    font-size: 16px;
    color: var(--text-primary);
}

.drop-zone-content span {
    font-size: 14px;
    color: var(--text-muted);
}

.file-preview {
    margin-top: 16px;
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 12px;
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
}

.file-preview img {
    width: 64px;
    height: 64px;
    border-radius: 8px;
    object-fit: cover;
}

.file-info {
    flex: 1;
}

.file-info p {
    margin: 2px 0;
}

.modal-actions {
    display: flex;
    gap: 12px;
    margin-top: 20px;
    justify-content: flex-end;
}

.btn {
    padding: 10px 20px;
    border-radius: 10px;
    border: none;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: 0.2s;
}

.btn-primary {
    background: #7c3aed;
    color: #fff;
}

.btn-primary:hover:not(:disabled) {
    background: #6d28d9;
}

.btn-primary:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.btn-secondary {
    background: rgba(255,255,255,0.05);
    color: #8b8b9e;
}

.btn-secondary:hover {
    background: rgba(255,255,255,0.1);
}

.btn-danger {
    background: rgba(239, 68, 68, 0.15);
    color: #ef4444;
}

.btn-danger:hover {
    background: rgba(239, 68, 68, 0.25);
}

.btn-small {
    padding: 4px 10px;
    font-size: 12px;
    border-radius: 6px;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(-20px) scale(0.95);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

@media (max-width: 640px) {
    .modal-content {
        max-width: 100%;
        border-radius: 12px;
        margin: 10px;
    }
    
    .modal-header {
        padding: 16px 20px;
    }
    
    .modal-body {
        padding: 16px 20px;
    }
    
    .drop-zone {
        padding: 24px 16px;
    }
    
    .drop-zone-content i {
        font-size: 32px;
    }
}
</style>