<template>
  <div class="pagination">
    <button
      type="button"
      class="pagination__btn"
      :disabled="!pagination.has_prev"
      @click="emit('change', pagination.page - 1)"
    >
      <i class="fa fa-chevron-left" />
    </button>

    <span class="pagination__info">
      {{ pagination.page }} / {{ pagination.pages }}
    </span>

    <button
      type="button"
      class="pagination__btn"
      :disabled="!pagination.has_next"
      @click="emit('change', pagination.page + 1)"
    >
      <i class="fa fa-chevron-right" />
    </button>
  </div>
</template>

<script setup>
defineProps({
  pagination: { type: Object, required: true },
})

const emit = defineEmits(['change'])
</script>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
  padding: var(--space-3) 0;
}

.pagination__btn {
  width: 36px;
  height: 36px;
  min-height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  padding: 0;
}

.pagination__btn:hover:not(:disabled) {
  border-color: var(--accent);
  color: var(--accent-text);
}

.pagination__btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.pagination__info {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  min-width: 60px;
  text-align: center;
}
</style>
