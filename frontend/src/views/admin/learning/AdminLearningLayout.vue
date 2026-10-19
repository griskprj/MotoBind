<template>
  <div class="admin-learning">
    <div class="admin-learning__head">
      <h1>Управление обучением</h1>
      <p>Курсы, уроки и статьи</p>
    </div>

    <nav class="admin-learning__nav">
      <router-link
        :to="{ name: 'admin-learning-courses' }"
        class="admin-nav-link"
        active-class="admin-nav-link--active"
      >
        <i class="fa fa-graduation-cap" />
        Курсы
      </router-link>
      <router-link
        :to="{ name: 'admin-learning-articles' }"
        class="admin-nav-link"
        active-class="admin-nav-link--active"
      >
        <i class="fa fa-newspaper" />
        Статьи
      </router-link>
    </nav>

    <router-view />
  </div>
</template>

<style scoped>
.admin-learning {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  max-width: 1200px;
  margin: 0 auto;
}

.admin-learning__head h1 {
  margin: 0 0 4px;
  font-size: var(--text-2xl);
  font-weight: var(--fw-bold);
}

.admin-learning__head p {
  margin: 0;
  font-size: var(--text-sm);
  color: var(--text-muted);
}

.admin-learning__nav {
  display: flex;
  gap: var(--space-2);
  border-bottom: 1px solid var(--border-light);
  padding-bottom: 2px;
}

.admin-nav-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-bottom: 2px solid transparent;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  transition: all var(--transition-fast);
  margin-bottom: -1px;
  min-height: 40px;
}

.admin-nav-link:hover {
  color: var(--text-primary);
}

.admin-nav-link--active {
  color: var(--accent-text);
  border-bottom-color: var(--accent);
}

.admin-nav-link i {
  font-size: 13px;
}
</style>
