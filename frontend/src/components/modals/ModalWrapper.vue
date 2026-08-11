<template>
    <div v-if="isOpen" class="modal-overlay" @click.self="$emit('close')">
        <div class="modal-container">
            <div class="modal-header">
                <div class="header-wrapper actions">
                    <div class="header-icon" :style="{background: bgIconColor, color: iconColor}">
                        <i class="fa" :class="'fa-' + icon"></i>
                    </div>
                    <button @click="$emit('close')" class="btn-small">
                        <i class="fa fa-close"></i>
                    </button>
                </div>
                <div class="header-wrapper">
                    <p class="modal-title">{{ title }}</p>
                    <p class="modal-subtitle">{{ subtitle }}</p>
                </div>
            </div>

            <div class="modal-scroll-area">
                <div class="modal-body">
                    <div class="modal-group">
                        <slot />
                    </div>
                </div>
            </div>

            <!-- Слот для действий внизу -->
            <div v-if="$slots.actions" class="modal-footer">
                <slot name="actions" />
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        isOpen: Boolean,
        title: String,
        subtitle: String,
        icon: String,
        bgIconColor: String,
        iconColor: String
    },

    watch: {
        isOpen(newVal) {
            if (newVal) {
                // Блокируем прокрутку страницы
                document.body.style.overflow = 'hidden'
            } else {
                // Восстанавливаем прокрутку
                document.body.style.overflow = ''
            }
        }
    },

    beforeUnmount() {
        // Восстанавливаем прокрутку при уничтожении компонента
        document.body.style.overflow = ''
    }
}
</script>

<style scoped>
/* ===== ОВЕРЛЕЙ ===== */
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1100;
    padding: 16px;
    animation: fadeIn 0.25s ease;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* ===== КОНТЕЙНЕР МОДАЛКИ ===== */
.modal-container {
    background-color: var(--bg-primary);
    border-radius: 16px;
    max-width: 560px;
    width: 100%;
    max-height: 90vh;
    display: flex;
    flex-direction: column;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.05);
    animation: slideUp 0.3s ease;
    overflow: hidden;
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px) scale(0.98);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

/* ===== ЗАГОЛОВОК ===== */
.modal-header {
    display: flex;
    flex-direction: column;
    padding: 20px 24px 16px;
    flex-shrink: 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.header-wrapper.actions {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    margin-bottom: 12px;
}

.header-icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--accent-trans);
    color: var(--accent);
    border-radius: 12px;
    font-size: 20px;
}

.btn-small {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: none;
    background: var(--bg-secondary);
    color: var(--text-secondary);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    transition: all 0.2s;
}

.btn-small:hover {
    background: var(--danger-trans);
    color: var(--danger);
}

.modal-title {
    font-size: 20px;
    font-weight: 700;
    margin: 0 0 4px 0;
    color: var(--text-primary);
}

.modal-subtitle {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
}

/* ===== ОБЛАСТЬ ПРОКРУТКИ ===== */
.modal-scroll-area {
    flex: 1;
    overflow-y: auto;
    padding: 0 24px;
}

.modal-scroll-area::-webkit-scrollbar {
    width: 4px;
}

.modal-scroll-area::-webkit-scrollbar-track {
    background: transparent;
}

.modal-scroll-area::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
}

.modal-scroll-area::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.2);
}

.modal-body {
    padding: 16px 0 8px;
}

/* ===== ФУТЕР С ДЕЙСТВИЯМИ ===== */
.modal-footer {
    padding: 12px 24px 20px;
    flex-shrink: 0;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    background: var(--bg-primary);
}

/* ============================================ */
/* ===== АДАПТИВНОСТЬ ===== */
/* ============================================ */

/* Мобильные устройства */
@media (max-width: 640px) {
    .modal-overlay {
        padding: 8px;
        align-items: flex-end;
    }

    .modal-container {
        max-height: 94vh;
        border-radius: 16px 16px 0 0;
        animation: slideUpMobile 0.3s ease;
    }

    @keyframes slideUpMobile {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .modal-header {
        padding: 16px 16px 12px;
        margin-bottom: 10px;
    }

    .header-icon {
        display: none;
    }

    .modal-title {
        font-size: 18px;
    }

    .modal-scroll-area {
        padding: 0 16px;
    }

    .modal-body {
        padding: 12px 0 8px;
    }

    .modal-footer {
        padding: 10px 16px 16px;
    }
}

/* Очень маленькие экраны */
@media (max-width: 400px) {
    .modal-overlay {
        padding: 4px;
    }

    .modal-container {
        max-height: 96vh;
    }

    .modal-header {
        padding: 12px 12px 10px;
    }

    .modal-scroll-area {
        padding: 0 12px;
    }

    .modal-footer {
        padding: 8px 12px 12px;
    }

    .btn-small {
        width: 32px;
        height: 32px;
        font-size: 14px;
    }
}
</style>