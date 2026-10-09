<template>
  <ModalWrapper
    :is-open="isOpen"
    :title="title"
    :subtitle="subtitle"
    :icon="variant === 'danger' ? 'triangle-exclamation' : 'circle-question'"
    :icon-color="variant === 'danger' ? 'var(--danger-text)' : 'var(--accent-text)'"
    :bg-icon-color="variant === 'danger' ? 'var(--danger-trans)' : 'var(--accent-trans)'"
    size="sm"
    @close="close"
  >
    <p class="confirm-text">{{ text }}</p>

    <template #actions>
      <BaseButton
        variant="secondary"
        block
        @click="close"
        style="margin-bottom: 8px;"
      >
        Отмена
      </BaseButton>
      <BaseButton
        :variant="variant === 'danger' ? 'danger' : 'primary'"
        block
        icon="fa fa-check"
        :loading="loading"
        @click="confirm"
      >
        {{ confirmText }}
      </BaseButton>
    </template>
  </ModalWrapper>
</template>

<script setup>
import ModalWrapper from '../modals/ModalWrapper.vue'
import { BaseButton } from '../ui'

defineProps({
  isOpen: { type: Boolean, default: false },
  title: { type: String, default: 'Подтвердите действие' },
  subtitle: { type: String, default: '' },
  text: { type: String, default: '' },
  confirmText: { type: String, default: 'Подтвердить' },
  variant: { type: String, default: 'primary' }, // primary | danger
  loading: { type: Boolean, default: false },
})
const emit = defineEmits(['close', 'confirm'])

function close() { emit('close') }
function confirm() { emit('confirm') }
</script>

<style scoped>
.confirm-text {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: var(--leading-base);
  margin: 0;
  text-align: center;
}
</style>
