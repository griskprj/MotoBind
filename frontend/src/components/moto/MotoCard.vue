<template>
    
    <div class="moto-card" :style="cardStyle">
        <div class="moto-card-header">
            <p>{{ moto.name }}</p>
            <div class="moto-actions">
                <button @click="$emit('editMoto', moto)" class="moto-action"><i class="fa fa-pen"></i></button>
                <button @click="$emit('deleteMoto', moto.id)" class="moto-action"><i class="fa fa-trash"></i></button>
            </div>
        </div>
        <div class="moto-card-body">
            <div class="moto-card-meta">
                <div class="meta-items">
                    <div class="meta-item">
                        <p class="meta-text">Объем:</p> <p>{{ moto.volume }} см3</p>
                    </div>
                    <div class="meta-item">
                        <p class="meta-text">Год выпуска:</p> <p>{{ moto.years ? moto.years : '--не указан--' }} г.</p>
                    </div>
                    <div class="meta-item">
                        <p class="meta-text">Пробег:</p> <p>{{ moto.mileage ? moto.mileage : 0 }} км</p>
                    </div>
                    <div class="meta-item">
                        <p class="meta-text">Гос. номер</p> <p>{{ moto.license_plate ? moto.license_plate : '--не указан--' }}</p>
                    </div>
                    <div class="meta-item">
                        <p class="meta-text">Цвет:</p> <div v-if="moto.color" class="moto-color" :style="{ background: moto.color }"></div> <p v-else>'--не указан--'</p>
                    </div>
                </div>
            </div>
            <div class="img-wrapper">
                <img src="/moto_default.jpg" alt="Motorcycle" class="moto-img">
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        moto: {
            type: Object,
            required: true
        }
    },

    computed: {
        cardStyle() {
            if (this.moto.color) {
                return {
                    '--moto-color': this.moto.color || 'var(--accent)'
                }
            }
        }
    }
}
</script>

<style scoped>
p {
    margin-bottom: 0;
}

.moto-card {
    padding: 15px;
    margin-bottom: 24px;
    border-radius: 18px;

    border: 2px solid var(--accent-light);

    transition: all 0.3s;
}

.moto-card:hover {
    transform: translateX(2px);
    border-left: 4px solid var(--moto-color);
}

.moto-card-header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-bottom: 24px;
}

.moto-card-header p {
    font-size: 24px;
    color: var(--accent);
    font-weight: 600;
}

.moto-actions {
    display: flex;
    flex-direction: row;
    gap: 12px;
}

.moto-actions button {
    max-height: 32px;
    max-width: 32px;
}

.moto-card-body {
    display: flex;
    width: 100%;
    justify-content: space-between;
    gap: 24px;

    overflow: hidden;
}

.img-wrapper {
    flex: 0 0 40%;
    max-height: 284px;
}
.moto-img {
  width: 100%;
  height: 100%;
  object-fit: cover; 
  border-radius: 25px;
  object-position: center center;
  filter: brightness(0.5);
}

.moto-card-meta {
    flex: 1;
    padding: 20px;

    background-color: var(--bg-secondary);
    border-radius: 25px;
}

.meta-items {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 8px;
}

.meta-item {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    
    padding: 8px 14px 8px 14px;

    background-color: var(--bg-primary);

    border-radius: 50px;
}

.meta-text {
    color: var(--accent);
    font-weight: 500;
}

.moto-color {
    width: 48px;
    height: 16px;
    border-radius: 16px;
}


@media (max-width: 728px) {
    .moto-card {
        padding: 8px;
    }

    .moto-card-body {
        flex-direction: column-reverse;
    }

    .moto-card-header {
        flex-direction: column;
        gap: 12px;
        align-items: center;
    }

    .moto-actions {
        flex-direction: column;
        width: 100%;
    }

    .moto-action {
        min-width: 100%;    
    }
}
</style>