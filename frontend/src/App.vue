<template>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

  <div v-if="isLoading" class="loading-overlay">
      <div class="spinner"></div>
  </div>
  <div class="animated-bg"></div>

  <!-- Страницы с сайдбаром -->
  <div v-if="$route.meta.showHeader" class="app-with-sidebar">
    <!-- Сайдбар рендерится сам, без слота, а контент идет после него -->
    <Sidebar ref="sidebar" />
    
    <!-- Основной контент -->
    <div class="app-content" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
      <div class="page-content">
        <router-view />
      </div>
      
      <!-- Футер внутри контента, чтобы учитывать отступы -->
      <Footer v-if="$route.meta.showFooter" />
    </div>
  </div>
  
  <!-- Страницы без сайдбара -->
  <template v-else>
    <router-view />
    <Footer v-if="$route.meta.showFooter" />
  </template>
</template>

<script>
import Sidebar from './components/Sidebar.vue';
import Footer from './components/Footer.vue';

export default {
  components: {
    Sidebar,
    Footer,
  },

  data() {
    return {
      user: false,
      isLoading: false,
      isSidebarCollapsed: false, // Добавляем состояние
    }
  },

  mounted() {
      const user = localStorage.getItem('user')
      if (user) {
        this.user = true
      }
      
      // Подписываемся на изменения состояния сайдбара
      this.$nextTick(() => {
        if (this.$refs.sidebar) {
          // Слушаем событие изменения состояния
          this.$refs.sidebar.$on('toggle-collapse', this.handleSidebarToggle);
          // Получаем начальное состояние
          this.isSidebarCollapsed = this.$refs.sidebar.isCollapsed;
        }
      });
  },

  beforeUnmount() {
    if (this.$refs.sidebar) {
      this.$refs.sidebar.$off('toggle-collapse', this.handleSidebarToggle);
    }
  },

  methods: {
    handleSidebarToggle(isCollapsed) {
      this.isSidebarCollapsed = isCollapsed;
    }
  }
}
</script>

<style>
/* ===== МОБИЛЬНЫЕ УЛУЧШЕНИЯ ===== */
::-webkit-scrollbar {
  width: 0;
  height: 0;
  background: transparent;
}

* {
  -webkit-tap-highlight-color: transparent;
  -webkit-touch-callout: none;
}

html {
  touch-action: manipulation;
}

button, 
a, 
input, 
select, 
textarea {
  touch-action: manipulation;
  min-height: 44px;
}

.safe-area {
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}

@media (max-width: 768px) {
  .modal-content {
    border-radius: 20px 20px 0 0 !important;
    max-height: 90vh !important;
    margin-top: auto !important;
  }
}

/* ===== Глобальные стили ===== */
.animated-bg {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: -2;
    background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
}

/* ===== Layout с сайдбаром ===== */
.app-with-sidebar {
    display: flex;
    min-height: 100vh;
}

/* Контентная область справа от сайдбара */
.app-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    transition: margin-left 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Отступы для контента в зависимости от состояния сайдбара */
@media (min-width: 771px) {
    .app-content {
        margin-left: 280px; /* Ширина развернутого сайдбара */
        padding: 0;
    }
    
    /* Когда сайдбар свернут */
    .app-content.sidebar-collapsed {
        margin-left: 64px; /* Ширина свернутого сайдбара */
    }
}

@media (max-width: 770px) {
    .app-content {
        margin-left: 0;
    }
}

.page-content {
    flex: 1;
    padding: 24px 32px;
    width: 100%;
}

/* ===== Адаптив ===== */
@media (max-width: 770px) {
    .page-content {
        padding: 80px 16px 20px;
    }
}

/* ===== Мобильные таблицы ===== */
@media (max-width: 768px) {
  .table-responsive {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  .mobile-card-table {
    border: none;
  }

  .mobile-card-table thead {
    display: none;
  }

  .mobile-card-table tbody tr {
    display: block;
    margin-bottom: 1rem;
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 1rem;
    transition: all 0.2s;
  }

  .mobile-card-table tbody tr:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }

  .mobile-card-table td {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 0;
    border: none;
    border-bottom: 1px solid var(--border-color);
  }

  .mobile-card-table td:last-child {
    border-bottom: none;
  }

  .mobile-card-table td::before {
    content: attr(data-label);
    font-weight: 600;
    color: var(--text-secondary);
    font-size: 0.875rem;
    margin-right: 1rem;
  }

  .mobile-card-table td.col-actions {
    justify-content: flex-end;
    gap: 0.5rem;
  }

  .mobile-card-table td.col-actions::before {
    content: 'Действия';
  }

  .mobile-card-table .action-buttons {
    flex-direction: row !important;
    gap: 0.5rem;
  }
}

/* ===== Планшеты ===== */
@media (min-width: 769px) and (max-width: 1024px) {
  .groups-table th,
  .groups-table td {
    padding: 0.75rem 0.5rem;
    font-size: 0.875rem;
  }

  .action-buttons {
    flex-direction: column;
    gap: 0.25rem;
  }

  .action-btn {
    width: 28px;
    height: 28px;
  }
}
</style>