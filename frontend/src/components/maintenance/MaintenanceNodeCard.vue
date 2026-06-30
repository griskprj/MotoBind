<script setup lang="ts">
import MaintenanceCard from './MaintenanceCard.vue';

</script>

<template>
    <div class="maintenance-node-card">
        <div class="node-header">
            <h3 class="node-title">Двигатель</h3>

            <p class="node-maintenance-count">3</p>
        </div>

        <div class="node-body">
            <div class="body-item">
                <p class="item-title">Здоровье узла: 75%</p>
                <div class="progress-container">
                    <div class="progress-value" style="width: 75%"></div>
                </div>
            </div>

            <div class="body-item">
                <p class="item-title">Предстоящие обслуживания</p>

                <div class="maintenance-list">
                    <MaintenanceCard
                        :maintenance="{
                            'id': 1,
                            'title': 'Замена масла',
                            'planned_mileage': 21000
                        }"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
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
</style>