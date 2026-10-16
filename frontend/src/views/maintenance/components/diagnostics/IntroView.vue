<template>
  <div class="intro-view">
    <!-- Заглушка: нет мотоцикла -->
    <div v-if="!motorcycle" class="empty-state">
      <i class="fa fa-motorcycle"></i>
      <p class="empty-text">Добавьте мотоцикл, чтобы запустить диагностику</p>
      <BaseButton variant="primary" icon="fa fa-plus" @click="goToGarage">
        Перейти в гараж
      </BaseButton>
    </div>

    <template v-else>
      <div class="intro-head">
        <h3>Диагностика</h3>
        <p class="intro-hint">
          Выберите узел для детальной проверки или запустите общую диагностику
        </p>
      </div>

      <!-- Плитки узлов -->
      <div class="intro-nodes">
        <button
          v-for="group in SYMPTOM_GROUPS"
          :key="group.id"
          type="button"
          class="node-card"
          @click="emit('start-node', group.id)"
        >
          <div class="node-card__icon">
            <i :class="group.icon" />
          </div>
          <div class="node-card__body">
            <span class="node-card__title">{{ group.label }}</span>
            <span class="node-card__desc">{{ getGroupHint(group.id) }}</span>
          </div>
          <i class="fa fa-chevron-right node-card__arrow" />
        </button>
      </div>

      <!-- Общая диагностика -->
      <BaseButton
        variant="outline"
        icon="fa fa-stethoscope"
        block
        @click="emit('start-general')"
      >
        Запустить общую диагностику
      </BaseButton>

      <!-- История -->
      <BaseButton
        v-if="store.reportCount > 0"
        variant="secondary"
        icon="fa fa-clock-rotate-left"
        block
        @click="emit('open-history')"
      >
        История диагностик ({{ store.reportCount }})
      </BaseButton>

      <p class="intro-disclaimer">
        <i class="fa fa-info-circle" />
        Результаты диагностики не являются профессиональными рекомендациями
      </p>
    </template>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { BaseButton } from '@/components/ui'
import { useDiagnosticsStore } from '@/stores'
import { SYMPTOM_GROUPS } from '@/constants/diagnisticsRules'

defineProps({
  motorcycle: { type: Object, default: null },
})

const emit = defineEmits(['start-node', 'start-general', 'open-history'])

const router = useRouter()
const store = useDiagnosticsStore()

const GROUP_HINTS = {
  engine: 'Запуск, работа, перегрев, шум',
  drive: 'Цепь, звёзды, смазка',
  brakes: 'Скрип, вибрация, мягкий рычаг',
  electrics: 'АКБ, свет, приборка, предохранители',
  suspension: 'Стук, утечки, раскачивание',
  wheels: 'Шины, давление, вибрации',
}

function getGroupHint(groupId) {
  return GROUP_HINTS[groupId] || ''
}

function goToGarage() {
  router.push('/garage')
}
</script>

<style scoped>
.intro-view {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.intro-head h3 {
  margin: 0 0 var(--space-1);
  font-size: var(--text-base);
}

.intro-hint {
  margin: 0;
  font-size: var(--text-sm);
  color: var(--text-muted);
}

.intro-nodes {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-2);
}

.node-card {
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

.node-card:hover {
  background: var(--bg-card-hover);
  border-color: var(--accent);
}

.node-card__icon {
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

.node-card__body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.node-card__title {
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
}

.node-card__desc {
  font-size: var(--text-xs);
  color: var(--text-muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.node-card__arrow {
  color: var(--text-muted);
  font-size: var(--text-xs);
  opacity: 0.5;
}

.intro-disclaimer {
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

.intro-disclaimer i {
  color: var(--warning-text);
  margin-top: 2px;
}
</style>
