<template>
  <div class="dashboard-container">
    <!-- Welcome Section -->
    <section class="welcome-section">
      <div class="welcome-content">
        <h1>Здравствуйте, Александр</h1>
        <p>Готовы к новой поездке? Ваш байк в отличной форме, но есть несколько моментов, требующих внимания.</p>
        <div class="welcome-stats">
          <div class="stat-item">
            <span class="stat-value">1 284</span>
            <span class="stat-label">км за месяц</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">3</span>
            <span class="stat-label">предстоящих обслуживания</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">92%</span>
            <span class="stat-label">здоровье байка</span>
          </div>
        </div>
      </div>
      <div class="welcome-emoji">🏍️</div>
    </section>

    <!-- Maintenance Section (Предстоящее обслуживание) -->
    <section class="maintenance-section">
      <div class="section-header">
        <h2>🔧 Предстоящее обслуживание</h2>
        <button class="btn-outline-small" aria-label="Все обслуживания">Все →</button>
      </div>
      <div class="maintenance-grid">
        <div class="maintenance-card urgent">
          <div class="card-badge">Срочно</div>
          <div class="card-icon">🛞</div>
          <div class="card-content">
            <h3>Замена масла и фильтра</h3>
            <p class="due-date">⏰ 15 мая 2026 • через 3 дня</p>
            <p class="mileage">Пробег: 12 450 км</p>
            <div class="progress-wrapper">
              <div class="progress-bar" :style="{ width: '85%' }"></div>
              <span class="progress-text">85% ресурса</span>
            </div>
          </div>
          <button class="card-btn">Записаться</button>
        </div>

        <div class="maintenance-card warning">
          <div class="card-badge">Рекомендуется</div>
          <div class="card-icon">⛓️</div>
          <div class="card-content">
            <h3>Регулировка цепи</h3>
            <p class="due-date">⏰ 28 мая 2026</p>
            <p class="mileage">Пробег: 11 200 км</p>
            <div class="progress-wrapper">
              <div class="progress-bar" :style="{ width: '60%' }"></div>
              <span class="progress-text">60% ресурса</span>
            </div>
          </div>
          <button class="card-btn">Записаться</button>
        </div>

        <div class="maintenance-card normal">
          <div class="card-badge">Плановое</div>
          <div class="card-icon">🔧</div>
          <div class="card-content">
            <h3>Проверка тормозных колодок</h3>
            <p class="due-date">⏰ 10 июня 2026</p>
            <p class="mileage">Пробег: 13 000 км</p>
            <div class="progress-wrapper">
              <div class="progress-bar" :style="{ width: '40%' }"></div>
              <span class="progress-text">40% ресурса</span>
            </div>
          </div>
          <button class="card-btn">Записаться</button>
        </div>
      </div>
    </section>

    <!-- Motorcycles Info Section (Информация о мотоциклах пользователя) -->
    <section class="motorcycles-section">
      <div class="section-header">
        <h2>🏍️ Мои мотоциклы</h2>
        <button class="btn-outline-small">+ Добавить мотоцикл</button>
      </div>
      <div class="motorcycles-grid">
        <div class="motorcycle-card active">
          <div class="motorcycle-header">
            <span class="status-badge active">В использовании</span>
            <span class="motor-year">2023</span>
          </div>
          <h3>Yamaha MT-09 SP</h3>
          <p class="motor-detail">Объём: 890 см³ • 119 л.с.</p>
          <div class="motor-stats">
            <div class="stat">
              <span class="stat-num">12 450</span>
              <span class="stat-caption">км пробега</span>
            </div>
            <div class="stat">
              <span class="stat-num">6.2 л</span>
              <span class="stat-caption">расход / 100км</span>
            </div>
            <div class="stat">
              <span class="stat-num">92%</span>
              <span class="stat-caption">здоровье</span>
            </div>
          </div>
          <div class="motor-actions">
            <button class="icon-btn">📊 История</button>
            <button class="icon-btn">⚙️ Сервис</button>
          </div>
        </div>

        <div class="motorcycle-card">
          <div class="motorcycle-header">
            <span class="status-badge">В гараже</span>
            <span class="motor-year">2020</span>
          </div>
          <h3>Kawasaki Z900</h3>
          <p class="motor-detail">Объём: 948 см³ • 125 л.с.</p>
          <div class="motor-stats">
            <div class="stat">
              <span class="stat-num">28 340</span>
              <span class="stat-caption">км пробега</span>
            </div>
            <div class="stat">
              <span class="stat-num">6.8 л</span>
              <span class="stat-caption">расход / 100км</span>
            </div>
            <div class="stat">
              <span class="stat-num">78%</span>
              <span class="stat-caption">здоровье</span>
            </div>
          </div>
          <div class="motor-actions">
            <button class="icon-btn">📊 История</button>
            <button class="icon-btn">⚙️ Сервис</button>
          </div>
        </div>

        <div class="motorcycle-card add-card">
          <div class="add-content">
            <div class="add-icon">➕</div>
            <p>Добавить мотоцикл</p>
            <span class="add-sub">VIN, марка, модель</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Quick Tips (бонусная секция - небольшая полезная информация) -->
    <section class="tips-section">
      <div class="tips-card">
        <div class="tips-icon">💡</div>
        <div class="tips-text">
          <h3>Совет по обслуживанию</h3>
          <p>Цепь вашего Yamaha MT-09 нуждается в регулировке через 800 км. Не откладывайте — это продлит срок службы трансмиссии.</p>
        </div>
        <button class="btn-small">Напомнить позже</button>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* Используем глобальные переменные + дополнительные локальные */
.dashboard-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* ========= WELCOME SECTION ========= */
.welcome-section {
  background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
  border-radius: 28px;
  padding: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1.5rem;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-md);
}

.welcome-content h1 {
  font-size: 1.9rem;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #fff, var(--accent));
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
}

.welcome-content p {
  color: var(--text-secondary);
  max-width: 500px;
  margin-bottom: 1.5rem;
}

.welcome-stats {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--accent);
  line-height: 1;
}

.stat-label {
  font-size: 0.8rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.welcome-emoji {
  font-size: 5rem;
  filter: drop-shadow(0 8px 12px rgba(0,0,0,0.3));
}

/* ========= SECTION HEADER ========= */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  flex-wrap: wrap;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.section-header h2 {
  margin-bottom: 0;
  font-size: 1.6rem;
}

.btn-outline-small {
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  padding: 0.5rem 1rem;
  border-radius: 40px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-outline-small:hover {
  background: var(--accent-light);
  border-color: var(--accent);
  color: var(--accent);
}

/* ========= MAINTENANCE GRID ========= */
.maintenance-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.maintenance-card {
  background: var(--bg-card);
  border-radius: 24px;
  padding: 1.5rem;
  border: 1px solid var(--border-color);
  transition: transform 0.2s, box-shadow 0.2s;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.maintenance-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.card-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-size: 0.7rem;
  background: var(--bg-secondary);
  padding: 0.25rem 0.75rem;
  border-radius: 40px;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.maintenance-card.urgent .card-badge {
  background: rgba(239, 68, 68, 0.2);
  color: var(--danger);
  border-color: var(--danger);
}

.maintenance-card.warning .card-badge {
  background: rgba(245, 158, 11, 0.2);
  color: var(--warning);
  border-color: var(--warning);
}

.card-icon {
  font-size: 2.5rem;
}

.card-content h3 {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.due-date, .mileage {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 0.25rem;
}

.progress-wrapper {
  margin-top: 0.75rem;
  background: var(--bg-secondary);
  border-radius: 20px;
  height: 6px;
  position: relative;
  width: 100%;
}

.progress-bar {
  height: 6px;
  background: var(--accent);
  border-radius: 20px;
  width: 0%;
  transition: width 0.3s;
}

.progress-text {
  position: absolute;
  right: 0;
  top: -18px;
  font-size: 0.7rem;
  color: var(--text-muted);
}

.card-btn {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  padding: 0.6rem;
  border-radius: 40px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-primary);
  margin-top: 0.5rem;
}

.card-btn:hover {
  background: var(--accent);
  border-color: var(--accent);
}

/* ========= MOTORCYCLES GRID ========= */
.motorcycles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.motorcycle-card {
  background: var(--bg-card);
  border-radius: 24px;
  padding: 1.5rem;
  border: 1px solid var(--border-color);
  transition: all 0.2s;
}

.motorcycle-card.active {
  border-left: 4px solid var(--accent);
  background: linear-gradient(145deg, var(--bg-card), var(--bg-secondary));
}

.motorcycle-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.status-badge {
  font-size: 0.7rem;
  padding: 0.2rem 0.7rem;
  border-radius: 40px;
  background: var(--bg-secondary);
  color: var(--text-muted);
}

.status-badge.active {
  background: rgba(139, 92, 246, 0.2);
  color: var(--accent);
}

.motor-year {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.motorcycle-card h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.motor-detail {
  color: var(--text-secondary);
  font-size: 0.85rem;
  margin-bottom: 1.2rem;
}

.motor-stats {
  display: flex;
  justify-content: space-between;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.motor-stats .stat {
  text-align: center;
  flex: 1;
  background: var(--bg-secondary);
  padding: 0.5rem;
  border-radius: 16px;
}

.stat-num {
  display: block;
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--accent);
}

.stat-caption {
  font-size: 0.7rem;
  color: var(--text-muted);
}

.motor-actions {
  display: flex;
  gap: 0.75rem;
}

.icon-btn {
  background: transparent;
  border: 1px solid var(--border-color);
  padding: 0.5rem 1rem;
  border-radius: 40px;
  font-size: 0.8rem;
  cursor: pointer;
  color: var(--text-secondary);
  transition: 0.2s;
}

.icon-btn:hover {
  background: var(--accent-light);
  border-color: var(--accent);
  color: var(--accent);
}

/* ADD CARD */
.motorcycle-card.add-card {
  background: transparent;
  border: 2px dashed var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  cursor: pointer;
  transition: 0.2s;
  min-height: 220px;
}

.motorcycle-card.add-card:hover {
  border-color: var(--accent);
  background: var(--accent-light);
}

.add-content .add-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.add-content p {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.add-sub {
  font-size: 0.7rem;
  color: var(--text-muted);
}

/* TIPS SECTION */
.tips-section {
  margin-top: 0.5rem;
}

.tips-card {
  background: linear-gradient(105deg, var(--bg-secondary), var(--bg-card));
  border-radius: 20px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  border: 1px solid var(--border-color);
  justify-content: space-between;
}

.tips-icon {
  font-size: 2.2rem;
}

.tips-text {
  flex: 2;
  min-width: 200px;
}

.tips-text h3 {
  margin-bottom: 0.2rem;
  font-size: 1.1rem;
}

.tips-text p {
  margin-bottom: 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.btn-small {
  background: transparent;
  border: 1px solid var(--accent);
  padding: 0.5rem 1rem;
  border-radius: 40px;
  color: var(--accent);
  cursor: pointer;
  transition: 0.2s;
}

.btn-small:hover {
  background: var(--accent);
  color: white;
}

/* ========= ADAPTIVE ========= */
@media (max-width: 768px) {
  .dashboard-container {
    padding: 1rem;
    gap: 1.5rem;
  }
  
  .welcome-section {
    flex-direction: column;
    text-align: center;
    padding: 1.5rem;
  }
  
  .welcome-content p {
    margin-left: auto;
    margin-right: auto;
  }
  
  .welcome-stats {
    justify-content: center;
  }
  
  .welcome-emoji {
    font-size: 3.5rem;
  }
  
  .section-header h2 {
    font-size: 1.3rem;
  }
  
  .maintenance-grid, .motorcycles-grid {
    grid-template-columns: 1fr;
  }
  
  .motor-stats {
    flex-direction: row;
  }
  
  .tips-card {
    flex-direction: column;
    text-align: center;
  }
  
  .card-badge {
    font-size: 0.65rem;
    padding: 0.2rem 0.6rem;
  }
}

@media (max-width: 480px) {
  .welcome-content h1 {
    font-size: 1.5rem;
  }
  
  .stat-value {
    font-size: 1.3rem;
  }
  
  .motorcycle-card h3 {
    font-size: 1.2rem;
  }
  
  .motor-stats .stat {
    font-size: 0.8rem;
  }
}
</style>