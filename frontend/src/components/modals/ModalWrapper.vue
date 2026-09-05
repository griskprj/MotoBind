<template>
    <Transition name="modal-fade">
        <div v-if="isOpen" class="modal-overlay" @click.self="close">
            <div class="modal-container" :class="{ 'modal-sm': size === 'sm', 'modal-lg': size === 'lg' }">
                <!-- Шапка -->
                <div class="modal-header">
                    <div class="modal-header-left">
                        <div 
                            v-if="icon" 
                            class="modal-icon" 
                            :style="{ 
                                background: bgIconColor || 'var(--accent-trans)', 
                                color: iconColor || 'var(--accent-text)' 
                            }"
                        >
                            <i class="fa" :class="'fa-' + icon"></i>
                        </div>
                        <div class="modal-header-text">
                            <h2 class="modal-title">{{ title }}</h2>
                            <p v-if="subtitle" class="modal-subtitle">{{ subtitle }}</p>
                        </div>
                    </div>
                    <button class="modal-close-btn" @click="close" aria-label="Закрыть">
                        <i class="fa fa-times"></i>
                    </button>
                </div>

                <!-- Тело -->
                <div class="modal-body" ref="modalBody">
                    <slot />
                </div>

                <!-- Футер с действиями (опционально) -->
                <div v-if="$slots.actions" class="modal-footer">
                    <slot name="actions" />
                </div>
            </div>
        </div>
    </Transition>
</template>

<script>
export default {
    name: 'ModalWrapper',
    
    props: {
        isOpen: {
            type: Boolean,
            required: true,
            default: false
        },
        title: {
            type: String,
            required: true
        },
        subtitle: {
            type: String,
            default: ''
        },
        icon: {
            type: String,
            default: ''
        },
        iconColor: {
            type: String,
            default: ''
        },
        bgIconColor: {
            type: String,
            default: ''
        },
        size: {
            type: String,
            default: 'md', // sm, md, lg
            validator: (value) => ['sm', 'md', 'lg'].includes(value)
        },
        closeOnOverlay: {
            type: Boolean,
            default: true
        },
        closeOnEscape: {
            type: Boolean,
            default: true
        }
    },

    emits: ['close'],

    mounted() {
        document.addEventListener('keydown', this.handleEscape)
    },

    beforeUnmount() {
        document.removeEventListener('keydown', this.handleEscape)
        document.body.style.overflow = ''
    },

    watch: {
        isOpen(newVal) {
            if (newVal) {
                document.body.style.overflow = 'hidden'
                // Сбрасываем скролл при открытии
                if (this.$refs.modalBody) {
                    this.$refs.modalBody.scrollTop = 0
                }
            } else {
                document.body.style.overflow = ''
            }
        }
    },

    methods: {
        close() {
            this.$emit('close')
        },
        handleEscape(event) {
            if (this.isOpen && this.closeOnEscape && event.key === 'Escape') {
                this.close()
            }
        }
    }
}
</script>

<style scoped>
/* ===== TRANSITIONS ===== */
.modal-fade-enter-active,
.modal-fade-leave-active {
    transition: opacity 0.25s ease;
}

.modal-fade-enter-active .modal-container,
.modal-fade-leave-active .modal-container {
    transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.25s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
    opacity: 0;
}

.modal-fade-enter-from .modal-container,
.modal-fade-leave-to .modal-container {
    transform: scale(0.95) translateY(20px);
    opacity: 0;
}

/* ===== OVERLAY ===== */
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1100;
    padding: 16px;
}

/* ===== CONTAINER ===== */
.modal-container {
    background: var(--bg-card);
    border-radius: 16px;
    width: 100%;
    max-width: 520px;
    max-height: 90vh;
    display: flex;
    flex-direction: column;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    border: 1px solid var(--border-light);
    overflow: hidden;
    position: relative;
}

.modal-container.modal-sm {
    max-width: 400px;
}

.modal-container.modal-lg {
    max-width: 640px;
}

/* ===== HEADER ===== */
.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 16px;
    padding: 20px 24px 16px;
    border-bottom: 1px solid var(--border-light);
    flex-shrink: 0;
}

.modal-header-left {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    min-width: 0;
    flex: 1;
}

.modal-icon {
    width: 44px;
    height: 44px;
    min-width: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}

.modal-header-text {
    min-width: 0;
    flex: 1;
}

.modal-title {
    font-size: 20px;
    font-weight: 700;
    margin: 0;
    color: var(--text-primary);
    line-height: 1.3;
}

.modal-subtitle {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 4px 0 0 0;
    line-height: 1.4;
}

.modal-close-btn {
    min-width: 36px;
    min-height: 36px;
    min-width: 36px;
    border-radius: 50%;
    border: none;
    background: var(--bg-secondary);
    color: var(--text-muted);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    transition: all 0.2s;
    flex-shrink: 0;
    margin-top: 2px;
}

.modal-close-btn:hover {
    background: var(--danger-trans);
    color: var(--danger-text);
}

/* ===== BODY ===== */
.modal-body {
    flex: 1;
    overflow-y: auto;
    padding: 20px 24px;
}

.modal-body::-webkit-scrollbar {
    width: 4px;
}

.modal-body::-webkit-scrollbar-track {
    background: transparent;
}

.modal-body::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 4px;
}

.modal-body::-webkit-scrollbar-thumb:hover {
    background: var(--text-muted);
}

/* ===== FOOTER ===== */
.modal-footer {
    padding: 12px 24px 20px;
    flex-shrink: 0;
    border-top: 1px solid var(--border-light);
    background: var(--bg-card);
}

/* ===== RESPONSIVE ===== */
@media (max-width: 640px) {
    .modal-overlay {
        padding: 8px;
        align-items: flex-end;
    }

    .modal-container {
        max-height: 94vh;
        border-radius: 16px 16px 0 0;
        max-width: 100%;
    }

    .modal-header {
        padding: 16px 16px 12px;
    }

    .modal-icon {
        width: 38px;
        height: 38px;
        min-width: 38px;
        font-size: 17px;
    }

    .modal-title {
        font-size: 18px;
    }

    .modal-subtitle {
        font-size: 13px;
    }

    .modal-body {
        padding: 16px 16px 8px;
    }

    .modal-footer {
        padding: 10px 16px 16px;
    }

    .modal-close-btn {
        width: 32px;
        height: 32px;
        min-width: 32px;
        font-size: 14px;
    }

    .modal-container.modal-sm,
    .modal-container.modal-lg {
        max-width: 100%;
    }
}

@media (max-width: 400px) {
    .modal-header {
        padding: 12px 12px 10px;
    }

    .modal-body {
        padding: 12px 12px 8px;
    }

    .modal-footer {
        padding: 8px 12px 12px;
    }

    .modal-title {
        font-size: 16px;
    }

    .modal-icon {
        width: 34px;
        height: 34px;
        min-width: 34px;
        font-size: 15px;
    }

    .modal-close-btn {
        width: 28px;
        height: 28px;
        min-width: 28px;
        font-size: 12px;
    }
}

/* ===== PRINT ===== */
@media print {
    .modal-overlay {
        position: static;
        background: none;
        backdrop-filter: none;
        padding: 0;
    }

    .modal-container {
        max-height: none;
        box-shadow: none;
        border: 1px solid #ddd;
        border-radius: 0;
    }

    .modal-close-btn {
        display: none;
    }
}
</style>