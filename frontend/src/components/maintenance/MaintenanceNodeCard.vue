<template>
  <div class="maintenance-node-card" :class="{ 'collapsed': isCollapsed }">
    <!-- Заголовок карточки (всегда видим) -->
    <div class="node-header" @click="toggleCollapse">
      <div class="node-header-left">
        <i class="fa fa-chevron-down" :class="{ 'rotated': !isCollapsed }"></i>
        <h3 class="node-title">{{ title }}</h3>
        <span class="node-badge">{{ maintenanceCount }} обслуживаний</span>
      </div>
      
      <div class="node-header-right">
        <span class="node-cost">{{ cost }} ₽</span>
        <i class="fa fa-ellipsis-v node-actions" @click.stop="showActions = !showActions"></i>
        
        <!-- Выпадающее меню действий -->
        <div class="actions-dropdown" v-if="showActions" @click.stop>
          <button @click="editNode"><i class="fa fa-pen"></i> Редактировать</button>
          <button @click="addMaintenance"><i class="fa fa-plus"></i> Добавить обслуживание</button>
          <button @click="deleteNode" class="danger"><i class="fa fa-trash"></i> Удалить</button>
        </div>
      </div>
    </div>

    <!-- Содержимое карточки (скрывается при сворачивании) -->
    <div class="node-content" v-show="!isCollapsed">
      <!-- Рекомендация -->
      <div class="node-recommendation" v-if="recomendation">
        <i class="fa fa-lightbulb-o"></i>
        <span>{{ recomendation }}</span>
      </div>

      <!-- Список обслуживаний -->
      <div class="maintenances-list">
        <div class="maintenances-header">
          <span>Обслуживания</span>
          <span class="maintenances-count">{{ maintenances.length }}</span>
        </div>
        
        <div v-if="maintenances && maintenances.length > 0" class="maintenances-items">
          <div 
            v-for="maintenance in maintenances" 
            :key="maintenance.id"
            class="maintenance-item"
          >
            <div class="maintenance-info">
              <span class="maintenance-title">{{ maintenance.title }}</span>
              <span class="maintenance-mileage" v-if="maintenance.planned_mileage">
                <i class="fa fa-road"></i> {{ maintenance.planned_mileage }} км
              </span>
            </div>
            <button class="maintenance-action" @click="viewMaintenance(maintenance)">
              <i class="fa fa-arrow-right"></i>
            </button>
          </div>
        </div>
        
        <div v-else class="no-maintenances">
          <p>Нет запланированных обслуживаний</p>
        </div>
      </div>

      <!-- Кнопка добавления обслуживания -->
      <button class="add-maintenance-btn" @click="addMaintenance">
        <i class="fa fa-plus"></i> Добавить обслуживание
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MaintenanceNodeCard',
  props: {
    title: {
      type: String,
      required: true
    },
    maintenanceCount: {
      type: [String, Number],
      default: '0'
    },
    cost: {
      type: [String, Number],
      default: '0'
    },
    maintenances: {
      type: Array,
      default: () => []
    },
    recomendation: {
      type: String,
      default: ''
    },
    // Позволяет управлять состоянием из родителя
    collapsed: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      isCollapsed: this.collapsed,
      showActions: false
    }
  },
  watch: {
    collapsed(val) {
      this.isCollapsed = val
    }
  },
  methods: {
    toggleCollapse() {
      this.isCollapsed = !this.isCollapsed
      this.showActions = false
      // Эмитим событие для родителя
      this.$emit('toggle-collapse', this.isCollapsed)
    },
    editNode() {
      this.showActions = false
      this.$emit('edit-node')
      console.log('Редактирование узла:', this.title)
    },
    addMaintenance() {
      this.showActions = false
      this.$emit('add-maintenance')
      console.log('Добавление обслуживания для узла:', this.title)
    },
    deleteNode() {
      this.showActions = false
      if (confirm(`Удалить узел "${this.title}"?`)) {
        this.$emit('delete-node')
        console.log('Удаление узла:', this.title)
      }
    },
    viewMaintenance(maintenance) {
      this.$emit('view-maintenance', maintenance)
      console.log('Просмотр обслуживания:', maintenance)
    }
  }
}
</script>

<style scoped>
.maintenance-node-card {
  background-color: var(--bg-secondary, #ffffff);
  border: 2px solid var(--border-color, #e0e0e0);
  border-radius: 16px;
  margin-bottom: 16px;
  transition: all 0.3s ease;
  overflow: hidden;
}

.maintenance-node-card:hover {
  border-color: var(--accent, #FF6B35);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* Заголовок карточки */
.node-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s;
}

.node-header:hover {
  background-color: rgba(0, 0, 0, 0.02);
}

.node-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.node-header-left .fa-chevron-down {
  transition: transform 0.3s ease;
  font-size: 14px;
  color: #999;
}

.node-header-left .fa-chevron-down.rotated {
  transform: rotate(-90deg);
}

.node-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.node-badge {
  background-color: var(--accent, #FF6B35);
  color: white;
  padding: 2px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
}

.node-header-right {
  display: flex;
  align-items: center;
  gap: 16px;
  position: relative;
}

.node-cost {
  font-weight: 600;
  color: var(--accent, #FF6B35);
  font-size: 18px;
  white-space: nowrap;
}

.node-actions {
  color: #999;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s;
}

.node-actions:hover {
  background-color: rgba(0, 0, 0, 0.05);
  color: #333;
}

/* Выпадающее меню */
.actions-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background-color: white;
  border: 1px solid var(--border-color, #e0e0e0);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  min-width: 200px;
  z-index: 1000;
  padding: 4px 0;
  animation: slideDown 0.2s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.actions-dropdown button {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 10px 16px;
  background: none;
  border: none;
  text-align: left;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  transition: background-color 0.2s;
}

.actions-dropdown button:hover {
  background-color: #f5f5f5;
}

.actions-dropdown button.danger {
  color: #dc3545;
}

.actions-dropdown button.danger:hover {
  background-color: #fee;
}

/* Содержимое карточки */
.node-content {
  padding: 0 20px 20px 20px;
  animation: expandContent 0.3s ease;
}

@keyframes expandContent {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Свернутое состояние */
.maintenance-node-card.collapsed .node-content {
  display: none;
}

.maintenance-node-card.collapsed .node-header {
  border-bottom: none;
}

/* Рекомендация */
.node-recommendation {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background-color: #fff3e0;
  border-radius: 12px;
  margin-bottom: 16px;
  color: #e65100;
  font-size: 14px;
}

.node-recommendation i {
  font-size: 18px;
  color: #ff9800;
}

/* Список обслуживаний */
.maintenances-list {
  margin-bottom: 16px;
}

.maintenances-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  font-weight: 500;
  color: #666;
  font-size: 14px;
}

.maintenances-count {
  background-color: #e0e0e0;
  padding: 0 10px;
  border-radius: 12px;
  font-size: 12px;
  color: #666;
}

.maintenances-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.maintenance-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  background-color: #f8f9fa;
  border-radius: 10px;
  border-left: 3px solid var(--accent, #FF6B35);
  transition: all 0.2s;
}

.maintenance-item:hover {
  background-color: #f0f0f0;
  transform: translateX(4px);
}

.maintenance-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.maintenance-title {
  font-weight: 500;
  font-size: 14px;
  color: #333;
}

.maintenance-mileage {
  font-size: 12px;
  color: #999;
}

.maintenance-mileage i {
  margin-right: 4px;
}

.maintenance-action {
  background: none;
  border: none;
  color: var(--accent, #FF6B35);
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s;
}

.maintenance-action:hover {
  background-color: rgba(255, 107, 53, 0.1);
  transform: translateX(2px);
}

.no-maintenances {
  text-align: center;
  padding: 20px;
  color: #999;
  font-size: 14px;
}

/* Кнопка добавления */
.add-maintenance-btn {
  width: 100%;
  padding: 10px;
  background: none;
  border: 2px dashed var(--border-color, #e0e0e0);
  border-radius: 10px;
  color: #666;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.add-maintenance-btn:hover {
  border-color: var(--accent, #FF6B35);
  color: var(--accent, #FF6B35);
  background-color: rgba(255, 107, 53, 0.05);
}

/* Адаптивность */
@media (max-width: 768px) {
  .node-header {
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .node-header-left {
    width: 100%;
  }
  
  .node-header-right {
    width: 100%;
    justify-content: flex-end;
  }
  
  .node-title {
    font-size: 16px;
  }
  
  .node-badge {
    font-size: 10px;
    padding: 1px 10px;
  }
  
  .node-cost {
    font-size: 16px;
  }
  
  .maintenance-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 6px;
  }
  
  .maintenance-action {
    align-self: flex-end;
  }
}

/* Темная тема */
@media (prefers-color-scheme: dark) {
  .maintenance-node-card {
    background-color: #1a1a1a;
    border-color: #333;
  }
  
  .node-header:hover {
    background-color: rgba(255, 255, 255, 0.05);
  }
  
  .node-title {
    color: #e0e0e0;
  }
  
  .node-actions:hover {
    background-color: rgba(255, 255, 255, 0.05);
  }
  
  .actions-dropdown {
    background-color: #2a2a2a;
    border-color: #444;
  }
  
  .actions-dropdown button {
    color: #e0e0e0;
  }
  
  .actions-dropdown button:hover {
    background-color: #3a3a3a;
  }
  
  .maintenance-item {
    background-color: #252525;
  }
  
  .maintenance-item:hover {
    background-color: #2a2a2a;
  }
  
  .maintenance-title {
    color: #e0e0e0;
  }
  
  .node-recommendation {
    background-color: #2a1f0a;
    color: #ffa726;
  }
}
</style>