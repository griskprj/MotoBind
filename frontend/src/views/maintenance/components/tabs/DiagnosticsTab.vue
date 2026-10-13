<template>
  <div class="diagnostics-tab">
    <div class="diagnostics-tab__head">
      <h3>Диагностика</h3>
      <p class="diagnostics-tab__hint">
        Выберите узел для детальной диагностики или запустите общую
      </p>
    </div>

    <div class="diagnostics-tab__nodes">
      <button
        v-for="node in nodes"
        :key="node.key"
        type="button"
        class="diag-node"
        @click="emit('start-diagnostics', node.key)"
      >
        <div class="diag-node__icon">
          <i :class="node.icon" />
        </div>
        <div class="diag-node__body">
          <span class="diag-node__title">{{ node.label }}</span>
          <span class="diag-node__desc">{{ node.description }}</span>
        </div>
        <i class="fa fa-chevron-right diag-node__arrow" />
      </button>
    </div>

    <BaseButton
      variant="outline"
      icon="fa fa-stethoscope"
      block
      @click="emit('start-diagnostics', null)"
    >
      Запустить общую диагностику
    </BaseButton>

    <p class="diagnostics-tab__disclaimer">
      <i class="fa fa-info-circle" />
      Результаты диагностики не являются профессиональными рекомендациями.
    </p>
  </div>
</template>

<script setup>
import { BaseButton } from '@/components/ui'

defineProps({
  motorcycle: { type: Object, default: null },
})

const emit = defineEmits(['start-diagnostics'])

const nodes = [
  {
    key: 'engine',
    label: 'Двигатель',
    description: 'Не заводится, глохнет, стук, дым',
    icon: 'fa fa-gear',
  },
  {
    key: 'brakes',
    label: 'Тормоза',
    description: 'Скрип, вибрация, мягкий ход',
    icon: 'fa fa-circle-stop',
  },
  {
    key: 'suspension',
    label: 'Подвеска',
    description: 'Проседание, стук, утечки',
    icon: 'fa fa-spring',
  },
  {
    key: 'electrical',
    label: 'Электрика',
    description: 'Свет, приборы, стартер',
    icon: 'fa fa-bolt',
  },
  {
    key: 'transmission',
    label: 'Трансмиссия',
    description: 'Цепь, сцепление, КПП',
    icon: 'fa fa-cog',
  },
]
</script>

<style scoped>
.diagnostics-tab {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.diagnostics-tab__head h3 {
  margin: 0 0 var(--space-1);
  font-size: var(--text-base);
}

.diagnostics-tab__hint {
  margin: 0;
  font-size: var(--text-sm);
  color: var(--text-muted);
}

.diagnostics-tab__nodes {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-2);
}

.diag-node {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  cursor: pointer;
  text-align: left;
  font-family: inherit;
  transition: all var(--transition-fast);
  min-height: 64px;
}

.diag-node:hover {
  background: var(--bg-card-hover);
  border-color: var(--accent);
}

.diag-node__icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  background: var(--accent-trans);
  color: var(--accent-text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-base);
  flex-shrink: 0;
}

.diag-node__body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.diag-node__title {
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
}

.diag-node__desc {
  font-size: var(--text-xs);
  color: var(--text-muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.diag-node__arrow {
  color: var(--text-muted);
  font-size: var(--text-xs);
  opacity: 0.5;
}

.diagnostics-tab__disclaimer {
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  margin: 0;
  padding: var(--space-3);
  background: var(--warning-trans);
  border-radius: var(--radius-md);
  font-size: var(--text-xs);
  color: var(--text-secondary);
}

.diagnostics-tab__disclaimer i {
  color: var(--warning-text);
  margin-top: 2px;
}
</style>
