<script>
import MaintenanceCard from './PlanMaintenanceNodeCard.vue';

export default {
    components: { MaintenanceCard },

    props: {
        node: {
            type: Object,
            required: true,
            default: null
        },
    },

    data() {
        return {
            showMaintenances: true
        }
    },

    computed: {
        healthColor() {
            const health = this.node.health;
            if (health >= 80) return 'var(--health-green, #4CAF50)';
            if (health >= 50) return 'var(--health-yellow, #FFC107)';
            return 'var(--health-red, #F44336)';
        }
    }
}
</script>

<template>
    <div class="maintenance-node-card">
        <div class="node-header">
            <div class="node-title-wrapper">
                <h3 class="node-title">{{ node.title }}</h3>
                <span class="node-maintenance-count">{{ node.maintenances_count }}</span>
            </div>
            
            <button class="btn-small node-action-btn"><i class="fa fa-arrow-right"></i></button>
        </div>

        <div class="node-body">
            <div class="body-item health-item">
                <div class="health-header">
                    <p class="item-title">Здоровье узла</p>
                    <span class="health-percent" :style="{ color: healthColor }">{{ node.health }}%</span>
                </div>
                <div class="progress-container">
                    <div class="progress-value" :style="{ width: node.health + '%', background: healthColor }"></div>
                </div>
            </div>

            <div class="body-item maintenances-item">
                <div class="maintenances-header">
                    <div class="maintenance-meta">
                        <p class="item-title">Предстоящие обслуживания</p>
                    </div>

                    <div class="maintenance-actions">
                        <button @click="showMaintenances = !showMaintenances" class="btn-small toggle-btn">
                            <i class="fa" :class="showMaintenances ? 'fa-angle-double-up' : 'fa-angle-double-down'"></i>
                        </button>
                    </div>
                </div>

                <div v-if="showMaintenances" class="maintenance-list">
                    <div v-if="node.planned_maintenances.length === 0" class="empty-state">
                        <i class="fa fa-wrench"></i>
                        <p class="empty-state-p">Нет запланированного обслуживания для этого узла</p>
                    </div>
                    
                    <MaintenanceCard
                        v-for="(maintenance, index) in node.planned_maintenances"
                        :key="index"
                        :maintenance="maintenance"
                        class="maintenance-card-item"
                    />
                </div>
            </div>
        </div>
    </div>
    <hr>
</template>

<style scoped>
.maintenance-node-card {
    background: var(--bg-primary);
    border-radius: 16px;
    padding: 20px 24px;
    transition: all 0.2s ease;
}

.maintenance-node-card:hover {
    background: var(--bg-secondary);
}

/* Header */
.node-header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 2px solid var(--border);
}

.node-title-wrapper {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 14px;
}

.node-title {
    font-size: 20px;
    font-weight: 600;
    color: var(--accent, #2c3e50);
    margin: 0;
}

.node-maintenance-count {
    background: var(--accent-light);
    color: var(--accent, #2c3e50);
    border-radius: 20px;
    padding: 2px 14px;
    font-size: 14px;
    font-weight: 600;
    min-width: 28px;
    text-align: center;
}

.node-action-btn {
    opacity: 0.6;
    transition: opacity 0.2s, transform 0.2s;
}

.node-action-btn:hover {
    opacity: 1;
    transform: translateX(3px);
}

/* Body */
.node-body {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.body-item {
    padding: 12px 0;
}

.body-item:not(:last-child) {
    border-bottom: 1px solid var(--border-color);
}

/* Health */
.health-item {
    padding-top: 4px;
}

.health-header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
}

.item-title {
    font-size: 15px;
    font-weight: 500;
    color: var(--text-secondary);
    margin: 0;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}

.health-percent {
    font-size: 18px;
    font-weight: 700;
    transition: color 0.3s ease;
}

.progress-container {
    width: 100%;
    height: 8px;
    background: var(--bg-secondary);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
}

.progress-value {
    height: 100%;
    width: 0;
    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1), background 0.3s ease;
    border-radius: 12px;
}

/* Maintenances header */
.maintenances-item {
    padding-bottom: 4px;
}

.maintenances-header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}

.maintenance-meta {
    display: flex;
    flex-direction: row;
    gap: 12px;
    align-items: center;
}

.maintenance-actions {
    display: flex;
    flex-direction: row;
    gap: 8px;
}

.toggle-btn {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 6px;
    background: var(--bg-secondary);
    border: none;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
    color: var(--text-secondary, #6c757d);
    transition: all 0.2s ease;
    cursor: pointer;
}

.toggle-btn:hover {
    background: var(--accent-light);
    color: var(--accent, #2c3e50);
}

.toggle-btn i {
    font-size: 14px;
}

.toggle-label {
    display: inline;
}

/* Maintenance list */
.maintenance-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    animation: fadeIn 0.25s ease;
}

.maintenance-card-item {
    border-radius: 14px;
    transition: all 0.2s ease;
}

.maintenance-card-item:hover {
    transform: translateX(4px);
}

/* Empty State */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 28px 20px;
    background: var(--bg-secondary, #f1f3f5);
    border-radius: 16px;
    border: 2px dashed var(--border-color, #dee2e6);
    text-align: center;
}

.empty-state i {
    font-size: 28px;
    color: var(--text-muted, #adb5bd);
    margin-bottom: 8px;
}

.empty-state-p {
    font-size: 15px;
    font-weight: 500;
    color: var(--text-secondary, #6c757d);
    margin: 0;
}

/* Animations */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(-8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Responsive */
@media (max-width: 728px) {
    .maintenance-node-card {
        padding: 16px;
    }

    .node-title {
        font-size: 18px;
    }

    .node-maintenance-count {
        font-size: 12px;
        padding: 1px 12px;
    }

    .maintenances-header {
        flex-wrap: wrap;
        gap: 8px;
    }

    .toggle-label {
        display: none;
    }

    .toggle-btn {
        padding: 6px 12px;
    }

    .health-percent {
        font-size: 16px;
    }

    .item-title {
        font-size: 13px;
    }
}

@media (max-width: 480px) {
    .maintenance-node-card {
        padding: 12px 14px;
    }

    .node-title-wrapper {
        gap: 8px;
        flex-wrap: wrap;
    }

    .node-title {
        font-size: 16px;
    }
}
</style>