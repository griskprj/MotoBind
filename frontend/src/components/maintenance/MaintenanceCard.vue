<script>
export default {
    props: {
        maintenance: {
            type: Object,
            default: null,
            required: true
        }
    }
}
</script>

<template>
    <div class="maintenance-card">
        <div class="maintenance-header">
            <div class="maintenance-icon">
                <i class="fa fa-wrench"></i>
            </div>
            <p class="maintenance-title">{{ maintenance.title }}</p>
        </div>
        <div class="maintenance-body">
            <div class="maintenance-meta">
                <p>{{ maintenance.moto_name }}</p>
                <p v-if="maintenance.planned_mileage" class="maintenance-meta-item">Пробег: {{ maintenance.planned_mileage}}</p>
            </div>
            <div class="maintenance-actions">
                <div class="actions-wrapper">
                    <button @click="$emit('edit', maintenance)" class="maintenance-action"><i class="fa fa-pen"></i></button>
                    <button @click="$emit('delete', maintenance.id)" class="maintenance-action"><i class="fa fa-trash"></i></button>
                </div>
                <button @click="$emit('mark', maintenance.id)" class="accept-btn"><i class="fa fa-check"></i></button>
            </div>
        </div>
    </div>
</template>

<style scoped>
p {
    margin-bottom: 0;
}

.maintenance-card {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    padding: 18px;
    background-color: var(--bg-secondary);
    border: 2px solid var(--border-color);
    border-radius: 25px;

    transition: all 0.3s;
}

.maintenance-card:hover {
    transform: translateX(2px);
    border-left: 4px solid var(--accent);
}

.maintenance-header {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 8px;
}

.maintenance-icon i {
    text-align: center;
    border-radius: 8px;
    padding: 12px;
    background-color: var(--accent);
    margin-right: 12px;
}

.maintenance-title {
    font-size: 20px;
    font-weight: 500;
    color: var(--text-primary)
}

.maintenance-body {
    display: flex;
    flex-direction: row;
    align-items: center;

    gap: 32px;
}

.maintenance-meta {
    background-color: var(--bg-primary);
    padding: 12px;
    border-radius: 8px;
}

.maintenance-actions {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.actions-wrapper {
    display: flex;
    flex-direction: row;
    gap: 8px;
}

@media (max-width: 728px) {
    .maintenance-card {
        flex-direction: column;
    }

    .maintenance-header {
        margin-bottom: 18px;
    }

    .maintenance-body {
        flex-direction: column;
    }

    .maintenance-meta {
        width: 100%;
        text-align: center;
    }

    .maintenance-actions {
        flex-direction: column;
        width: 100%;
    }

    .maintenance-action {
        width: 100%;
    }
}
</style>