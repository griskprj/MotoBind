<template>
  <section class="diagnostics-section">
    <div class="section-header">
      <div class="section-header-left">
        <i class="fa fa-stethoscope"></i>
        <h4>Диагностика</h4>
      </div>
    </div>

    <p class="diag-title">Проведите онлайн-диагностику, указав симптомы</p>
    <p class="diag-hint">Важно: результаты диагностики не являются профессиональными рекомендациями!</p>

    <div class="diagnostics-actions">
      <button class="diag-cta" @click="emit('start')">
        Провести онлайн-диагностику
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
const emit = defineEmits<{ start: [] }>()
</script>

<style scoped>
.diagnostics-section {
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 20px 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.section-header-left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.section-header-left i {
  color: var(--accent-text);
  font-size: 18px;
}

.section-header h4 {
  font-size: 15px;
  font-weight: var(--fw-semibold);
  margin: 0;
}

.diag-title {
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: center;
  margin-bottom: 8px;
}

.diag-hint {
  font-size: 12px;
  color: var(--text-muted);
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 12px;
  text-align: center;
}

.diagnostics-actions {
  display: flex;
  justify-content: center;
}

.diag-cta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border: 1px solid var(--accent);
  border-radius: var(--radius-md);
  font-size: 13px;
  font-weight: var(--fw-medium);
  cursor: pointer;
  transition: all var(--transition-base);
  min-height: 40px;
  background: transparent;
  color: var(--text-primary);
}

.diag-cta:hover {
  background: var(--accent-trans);
  color: var(--text-primary);
}

@media (max-width: 820px) {
  .diagnostics-section {
    padding: 14px 16px;
  }
}

@media (max-width: 640px) {
  .diagnostics-actions {
    justify-content: stretch;
  }

  .diag-cta {
    width: 100%;
    justify-content: center;
  }
}
</style>
