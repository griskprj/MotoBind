<template>
  <section class="attention">
    <div class="attention__head">
      <i class="fa fa-bell" />
      <h3>Требует внимания</h3>
    </div>

    <div class="attention__list">
      <AttentionItem
        v-for="item in items"
        :key="item.id"
        :item="item"
        @open="emit('open-maintenance', $event)"
        @complete="emit('complete', $event)"
        @open-manual="emit('open-manual', $event)"
        @find-master="emit('find-master')"
      />
    </div>
  </section>
</template>

<script setup>
import AttentionItem from './AttentionItem.vue'

defineProps({
  items: { type: Array, required: true },
})

const emit = defineEmits(['open-maintenance', 'complete', 'open-manual', 'find-master'])
</script>

<style scoped>
.attention {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.attention__head {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.attention__head i {
  color: var(--warning-text);
  font-size: var(--text-lg);
}

.attention__head h3 {
  margin: 0;
  font-size: var(--text-base);
  font-weight: var(--fw-semibold);
}

.attention__list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}
</style>
