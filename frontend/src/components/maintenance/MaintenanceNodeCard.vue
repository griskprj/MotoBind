<script>
import MaintenanceCard from './MaintenanceCard.vue';

export default {
    components: {MaintenanceCard},

    props: {
        node: {
            type: Object,
            required: true,
            default: null
        }
    }
}
</script>

<template>
    <div class="maintenance-node-card">
        <div class="node-header">
            <h3 class="node-title">{{ node.title }}</h3>

            <p class="node-maintenance-count">{{ node.maintenances_count}}</p>
        </div>

        <div class="node-body">
            <div class="body-item">
                <p class="item-title">Здоровье узла: {{ node.health }}%</p>
                <div class="progress-container">
                    <div class="progress-value" :style="{ width: node.health + '%' }"></div>
                </div>
            </div>

            <div class="body-item">
                <p class="item-title">Предстоящие обслуживания</p>

                <div class="maintenance-list">
                    <div v-if="node.planned_maintenances.length === 0" class="empty-state">
                        <i class="fa fa-wrench"></i>
                        <p class="empty-state-p">Нет запланированного обслуживания для этого узла</p>
                    </div>
                    
                    <MaintenanceCard
                        v-for="maintenance in node.planned_maintenances"
                        :maintenance="maintenance"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.node-header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;

    margin-bottom: 12px;
}

.node-maintenance-count {
    background-color: var(--text-muted);
    border-radius: 12px;
    text-align: center;
    min-width: 32px;
}

.node-title {
    font-size: 21px;
    color: var(--accent);
}


.body-item {
    margin-bottom: 24px;
}

.item-title {
    font-size: 18px;
    font-weight: 500;
}

.progress-container {
    width: 100%;
    background: #ddd;
    border-radius: 12px;
}

.progress-value {
    height: 20px;
    background: var(--accent);
    width: 0;
    transition: width 0.5s;
    border-radius: 12px;
}

/* Empty State */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 32px;
    background-color: var(--bg-secondary);
    border-radius: 24px;
    border: 2px dashed var(--border-color);

    text-align: center;
}

.empty-state i {
    font-size: 32px;
    color: var(--accent);
    margin-bottom: 12px;
}

.empty-state-p {
    font-size: 18px;
    font-weight: 500;
    color: var(--text-secondary);

    margin-bottom: 12px;
}
</style>