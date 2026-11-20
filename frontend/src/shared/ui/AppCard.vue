<template>
  <n-card
    :title="title"
    :bordered="bordered"
    :hoverable="interactive"
    size="medium"
  >
    <template v-if="icon || $slots.header" #header>
      <div class="app-card__header">
        <i v-if="icon" :class="icon" class="app-card__icon" />
        <slot name="header">{{ title }}</slot>
      </div>
    </template>
    <slot />
    <template v-if="$slots.footer" #footer>
      <slot name="footer" />
    </template>
    <template v-if="$slots.actions" #action>
      <slot name="actions" />
    </template>
  </n-card>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  title?: string
  icon?: string
  bordered?: boolean
  interactive?: boolean
}>(), {
  bordered: false,
  interactive: false,
})
</script>

<style scoped>
.app-card__header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.app-card__icon {
  color: var(--accent);
  font-size: 16px;
}
</style>
