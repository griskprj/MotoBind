<template>
    <div class="unsubscribe-page">
        <div class="container">
            <div class="unsubscribe-card">
                <div v-if="loading" class="loading-state">
                    <i class="fa fa-spinner fa-spin"></i>
                    <span>Обработка запроса...</span>
                </div>
                
                <div v-else-if="success" class="success-state">
                    <div class="icon success">
                        <i class="fa fa-check-circle"></i>
                    </div>
                    <h2>Вы отписались от рассылки</h2>
                    <p>Вы больше не будете получать новостные письма от MotoBind</p>
                    <button @click="$router.push('/')" class="btn-primary">
                        На главную
                    </button>
                </div>
                
                <div v-else-if="error" class="error-state">
                    <div class="icon error">
                        <i class="fa fa-exclamation-circle"></i>
                    </div>
                    <h2>Ошибка</h2>
                    <p>{{ errorMessage }}</p>
                    <button @click="$router.push('/profile')" class="btn-primary">
                        В профиль
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import api from '../api/api';

export default {
    name: 'UnsubscribePage',
    data() {
        return {
            loading: true,
            success: false,
            error: false,
            errorMessage: ''
        }
    },
    mounted() {
        const token = this.$route.params.token;
        if (token) {
            this.unsubscribe(token);
        } else {
            this.error = true;
            this.errorMessage = 'Недействительная ссылка';
            this.loading = false;
        }
    },
    methods: {
        async unsubscribe(token) {
            try {
                await api.get(`/unsubscribe/${token}`);
                this.success = true;
            } catch (err) {
                this.error = true;
                this.errorMessage = err.response?.data?.error || 'Ошибка при отписке';
            } finally {
                this.loading = false;
            }
        }
    }
}
</script>

<style scoped>
.unsubscribe-page {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 80vh;
    padding: 20px;
}

.unsubscribe-card {
    max-width: 500px;
    width: 100%;
    padding: 40px;
    background: var(--bg-secondary);
    border-radius: 16px;
    border: 1px solid var(--border-color);
    text-align: center;
}

.icon {
    font-size: 64px;
    margin-bottom: 16px;
}

.icon.success {
    color: var(--success-text);
}

.icon.error {
    color: var(--danger-text);
}

.loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    color: var(--text-secondary);
}

.loading-state i {
    font-size: 40px;
    color: var(--accent);
}

h2 {
    margin: 0 0 8px 0;
    color: var(--text-primary);
}

p {
    color: var(--text-secondary);
    margin: 0 0 24px 0;
}

.btn-primary {
    padding: 10px 32px;
    background: var(--accent);
    color: #fff;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-primary:hover {
    background: var(--accent-hover);
    transform: translateY(-2px);
}
</style>