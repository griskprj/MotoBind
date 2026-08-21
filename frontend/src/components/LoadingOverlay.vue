<!-- components/LoadingOverlay.vue -->
<template>
    <div v-if="isLoading" class="loading-overlay">
        <div class="loading-spinner">
            <div class="spinner"></div>
            <p class="loading-text">{{ text || 'Загрузка...' }}</p>
        </div>
    </div>
</template>

<script>
export default {
    name: 'LoadingOverlay',
    props: {
        isLoading: {
            type: Boolean,
            default: false
        },
        text: {
            type: String,
            default: 'Загрузка...'
        }
    }
}
</script>

<style scoped>
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(11, 11, 18, 0.85);
    backdrop-filter: blur(8px);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
    animation: fadeIn 0.25s ease;
}

.loading-spinner {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
}

.spinner {
    width: 56px;
    height: 56px;
    border: 4px solid rgba(124, 58, 237, 0.15);
    border-top: 4px solid #7c3aed;
    border-radius: 50%;
    animation: spin 0.9s cubic-bezier(0.6, 0, 0.4, 1) infinite;
    box-shadow: 0 0 40px rgba(124, 58, 237, 0.15);
}

.loading-text {
    color: #a78bfa;
    font-size: 16px;
    font-weight: 500;
    letter-spacing: 0.3px;
    animation: pulseText 1.5s ease-in-out infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

@keyframes pulseText {
    0%, 100% {
        opacity: 0.6;
    }
    50% {
        opacity: 1;
    }
}
</style>