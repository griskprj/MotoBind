<template>
    <div class="container">
        <!-- === WELCOME SECTION === -->
        <div class="welcome-section">
            <div class="welcome-wrapper">
                <h2>Здравствуйте,</h2> <h2 class="welcome-title">name</h2>
            </div>
            <p class="welcome-subtitle">Ваш мотоцикл в отличной форме, но есть пару моментов, на которые стоит обратить внимание</p>
        </div>
      
        <!-- === MOTORCYCLE SECTION === -->
        <div class="motorcycle-section">
            <div class="moto-card">
                <div class="moto-card-header">
                    <p>Yamaha MT-09</p>
                    <div class="moto-actions">
                        <button class="moto-action"><i class="fa fa-pen"></i></button>
                        <button class="moto-action"><i class="fa fa-trash"></i></button>
                    </div>
                </div>
                <div class="moto-card-body">
                    <div class="moto-card-meta">
                        <div class="meta-items">
                            <div class="meta-item">
                                <p class="meta-text">Объем:</p> <p>790</p>
                            </div>
                            <div class="meta-item">
                                <p class="meta-text">Год выпуска:</p> <p>2020</p>
                            </div>
                            <div class="meta-item">
                                <p class="meta-text">Пробег:</p> <p>17000км</p>
                            </div>
                            <div class="meta-item">
                                <p class="meta-text">Здоровье:</p> <p>95%</p>
                            </div>
                        </div>
      
                        <button class="follow-btn btn">Подробнее</button>
                    </div>
                    <div class="img-wrapper">
                        <img src="/bmw1000.webp" alt="Motorcycle" class="moto-img">
                    </div>
                </div>
            </div>
        </div>
        
        <!-- === PENDING MAINTENANCE SECTION === -->
        <div class="maintenance-section">
            <h2 class="maintenance-section-title">Предстоящее обслуживание</h2>
            <div class="maintenance-cards">
                <div class="maintenance-card">
                    <div class="maintenance-header">
                        <div class="maintenance-icon">
                            <i class="fa fa-wrench"></i>
                        </div>
                        <p class="maintenance-title">Замена масла</p>
                    </div>
                    <div class="maintenance-body">
                        <div class="maintenance-meta">
                            <p class="maintenance-meta-item">Дата: 11.06.2026</p>
                            <p class="maintenance-meta-item">Пробег: 17000</p>
                        </div>
                        <div class="maintenance-actions">
                            <button class="maintenance-action"><i class="fa fa-pen"></i></button>
                            <button class="maintenance-action"><i class="fa fa-trash"></i></button>
                        </div>
                    </div>
                </div>
                <div class="maintenance-card">
                    <div class="maintenance-header">
                        <div class="maintenance-icon">
                            <i class="fa fa-wrench"></i>
                        </div>
                        <p class="maintenance-title">Замена масла</p>
                    </div>
                    <div class="maintenance-body">
                        <div class="maintenance-meta">
                            <p class="maintenance-meta-item">Дата: 11.06.2026</p>
                            <p class="maintenance-meta-item">Пробег: 17000</p>
                        </div>
                        <div class="maintenance-actions">
                            <button class="maintenance-action"><i class="fa fa-pen"></i></button>
                            <button class="maintenance-action"><i class="fa fa-trash"></i></button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
p {
    margin-bottom: 0;
}

/* Welcome Section */
.welcome-section {
    background-color: var(--bg-primary);
    border: 2px solid var(--border-color);
    border-radius: 25px;

    padding: 28px;
    margin-bottom: 32px;

}

.welcome-wrapper {
    display: flex;
    flex-direction: row;
    gap: 12px;
}

.welcome-title {
    color: var(--accent);
}


/* Motorcycle Section */
.motorcycle-section {
    background-color: var(--bg-primary);
    border: 2px solid var(--border-color);
    border-radius: 25px;

    margin-bottom: 32px;
    padding: 28px;
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
    margin-bottom: 24px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.meta-item {
    display: flex;
    flex-direction: row;
    justify-content: space-between;

    padding: 8px 14px 8px 14px;

    background-color: var(--bg-primary);

    border-radius: 50px;
}

.meta-text {
    color: var(--accent);
    font-weight: 500;
}

.follow-btn {
    width: 100%;
}



@media (max-width: 728px) {
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



/* Pending Maintenance Section */
.maintenance-section {
    background-color: var(--bg-primary);
    border: 2px solid var(--border-color);
    border-radius: 25px;

    margin-bottom: 32px;
    padding: 28px;
}

.maintenance-cards {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.maintenance-card {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    padding: 18px;
    background-color: var(--bg-secondary);
    border: 2px solid var(--border-color);
    border-radius: 25px;
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
        flex-direction: row;
        width: 100%;
    }

    .maintenance-action {
        width: 100%;
    }
}
</style>