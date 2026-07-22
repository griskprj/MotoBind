<script>
export default {
    props: {
        maintenance: {
            type: Object,
            default: null,
            required: true
        }
    },
    computed: {
        progressPercent() {
            if (!this.maintenance.planned_mileage) return 0;
            const current = this.maintenance.current_mileage || 7500; 
            const planned = this.maintenance.planned_mileage;
            // Не даем проценту уйти за 100%
            return Math.min((current / planned) * 100, 100);
        }
    }
}
</script>

<template>
    <div class="maintenance-card">
        <div class="card-icon">
            <i class="fa fa-motorcycle"></i>
        </div>

        <div class="card-info">
            <div class="info-header">
                <span class="moto-name">{{ maintenance.moto_name || 'Мотоцикл' }}</span>
                <span class="distance-badge">через {{ maintenance.planned_mileage }} км</span>
            </div>
            <div class="info-desc">{{ maintenance.title || 'Обслуживание' }}</div>
            
            <div class="info-progress">
                <div class="progress-track">
                    <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
                </div>
                <span class="progress-text">{{ maintenance.current_mileage || 7500 }} / {{ maintenance.planned_mileage || 10000 }} км</span>
            </div>
        </div>

        <div class="card-action">
            <i class="fa fa-chevron-right"></i>
        </div>
    </div>
</template>

<style scoped>
/* Общий контейнер - строка */
.maintenance-card {
    display: flex;
    align-items: center;
    padding: 12px 16px;
    background-color: var(--bg-card);
    border-radius: 12px;
    gap: 16px;
    transition: background 0.2s ease;
    cursor: pointer;

    transition: all 0.3s ease;
}

.maintenance-card:hover {
    background-color: var(--bg-card-hover);
}

/* Иконка слева */
.card-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.05);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #8b8b9e;
    font-size: 18px;
    flex-shrink: 0;
}

/* Центральная часть с информацией */
.card-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.info-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.moto-name {
    font-size: 14px;
    font-weight: 600;
    color: #ffffff;
}

.distance-badge {
    font-size: 11px;
    font-weight: 500;
    color: #fbbf24; /* Желтый цвет, как на скриншоте */
    background: rgba(251, 191, 36, 0.1);
    padding: 2px 8px;
    border-radius: 6px;
}

.info-desc {
    font-size: 13px;
    color: #8b8b9e; /* Серый цвет описания */
    margin-bottom: 2px;
}

/* Прогресс-бар */
.info-progress {
    display: flex;
    align-items: center;
    gap: 12px;
}

.progress-track {
    flex: 1;
    height: 4px;
    background: #2d2d3d; /* Цвет фона трека */
    border-radius: 4px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: #7c3aed; /* Фиолетовый цвет заполнения */
    border-radius: 4px;
    transition: width 0.3s ease;
}

.progress-text {
    font-size: 11px;
    color: #8b8b9e;
    white-space: nowrap;
    min-width: 70px;
    text-align: right;
}

/* Стрелка справа */
.card-action {
    color: #4b4b5e;
    font-size: 14px;
    transition: color 0.2s ease;
    margin-left: 4px;
}

.maintenance-card:hover .card-action {
    color: #a78bfa;
}

/* Адаптив для маленьких экранов */
@media (max-width: 480px) {
    .maintenance-card {
        flex-wrap: wrap;
        padding: 12px;
    }
    
    .card-info {
        width: 100%;
        order: 2;
    }
    
    .card-icon {
        order: 1;
    }
    
    .card-action {
        order: 3;
        margin-left: auto;
    }

    .info-header {
        flex-wrap: wrap;
        gap: 4px;
    }
}
</style>