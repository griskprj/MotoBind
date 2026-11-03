<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  activeZones?: string[]
}>()

const emit = defineEmits<{
  (e: 'zone-click', zoneId: string): void
}>()

interface Zone {
  id: string
  label: string
  icon: string
  x: number
  y: number
  color: string
}

const ZONES: Zone[] = [
  { id: 'electrics', label: 'Электрика', x: 32, y: 43, icon: 'fa-solid fa-bolt', color: '#a855f7' },

  { id: 'fork', label: 'Вилка', x: 70, y: 45, icon: 'fa-solid fa-arrows-up-down', color: '#06b6d4' },

  { id: 'fuel', label: 'Топливо', x: 55, y: 38, icon: 'fa-solid fa-gas-pump', color: '#22c55e' },

  { id: 'ignition', label: 'Зажигание', x: 65, y: 28, icon: 'fa-solid fa-fire', color: '#f59e0b' },

  { id: 'engine', label: 'Двигатель', x: 55, y: 55, icon: 'fa-solid fa-gear', color: '#ef4444' },

  { id: 'shift', label: 'Коробка передач', x: 50, y: 65, icon: 'fa-solid fa-gears', color: '#ec4899' },

  { id: 'chain', label: 'Цепь', x: 32, y: 72, icon: 'fa-solid fa-chain', color: '#ec4899' },

  { id: 'brakes_rear', label: 'Тормоза (Зад)', x: 24.5, y: 70, icon: 'fa-solid fa-hand', color: '#3b82f6' },
  { id: 'brakes_front', label: 'Тормоза (Пер)', x: 76.5, y: 70, icon: 'fa-solid fa-hand', color: '#3b82f6' },

  { id: 'wheels', label: 'Колёса', x: 76.5, y: 86.5, icon: 'fa-solid fa-circle-notch', color: '#94a3b8' }
]

const activeSet = computed(() => new Set(props.activeZones || []))

function isActive(id: string) {
  return activeSet.value.has(id)
}

function onClick(zone: Zone) {
  emit('zone-click', zone.id)
}
</script>

<template>
  <div class="zones-widget">
    <h4 class="zones-title">Зоны проверки</h4>

    <div class="bike-schema-wrapper">
      <!-- Контейнер для позиционирования -->
      <div class="bike-schema">

        <img
          src="~/assets/images/bike-schema.svg"
          class="bike-img"
          alt="Схема мотоцикла"
        />

        <!-- Маркеры зон -->
        <button
          v-for="zone in ZONES"
          :key="zone.id"
          class="zone-marker"
          :class="{ active: isActive(zone.id) }"
          :style="{
            left: zone.x + '%',
            top: zone.y + '%',
            '--zone-color': zone.color,
          }"
          :title="zone.label"
          @click="onClick(zone)"
        >
          <i :class="zone.icon"></i>
          <span class="zone-label">{{ zone.label }}</span>
        </button>
      </div>
    </div>

    <!-- Легенда -->
    <div class="zones-legend">
      <button
        v-for="zone in ZONES"
        :key="zone.id"
        class="legend-item"
        :class="{ active: isActive(zone.id) }"
        @click="onClick(zone)"
      >
        <span class="legend-dot" :style="{ background: zone.color }"></span>
        <i :class="zone.icon"></i>
        {{ zone.label }}
      </button>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.zones-widget {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.zones-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.zones-title {
  font-size: var(--text-base);
  font-weight: var(--fw-semibold);
}

.active-count {
  font-size: var(--text-xs);
  color: var(--color-brand);
  background: var(--color-brand-soft);
  padding: 2px 8px;
  border-radius: var(--radius-full);
}

.bike-schema-wrapper {
  background: radial-gradient(circle at center, rgba(112, 0, 255, 0.15) 0%, transparent 60%);
  border-radius: var(--radius-lg);
  padding: var(--space-2);
  border: 1px solid rgba(112, 0, 255, 0.1);

  @include md-up {
    padding: var(--space-4);
  }
}

.bike-schema {
  position: relative;
  width: 100%;
  aspect-ratio: 400 / 240;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bike-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  filter: brightness(0) invert(1) opacity(0.15) drop-shadow(0 0 20px rgba(112, 0, 255, 0.3));
}

.zone-marker {
  position: absolute;
  transform: translate(-50%, -50%);

  width: clamp(22px, 4vw, 32px);
  height: clamp(22px, 4vw, 32px);

  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(20, 20, 25, 0.85);
  color: var(--color-text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;

  font-size: clamp(10px, 1.8vw, 14px);

  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(4px);
  z-index: 2;

  @include md-up {
    border-width: 1px;
  }

  &:hover {
    border-color: var(--zone-color);
    color: var(--zone-color);
    transform: translate(-50%, -50%) scale(1.15);
  }

  &.active {
    background: var(--zone-color);
    border-color: var(--zone-color);
    color: #fff;
    box-shadow:
      0 0 0 4px rgba(255, 255, 255, 0.05),
      0 0 20px var(--zone-color);
    animation: pulse 2s infinite;
  }
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.05), 0 0 20px var(--zone-color);
  }
  50% {
    box-shadow: 0 0 0 8px rgba(255, 255, 255, 0.02), 0 0 30px var(--zone-color);
  }
}

.zone-label {
  display: none;
  position: absolute;
  top: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
  font-size: 10px;
  font-weight: var(--fw-semibold);
  white-space: nowrap;
  padding: 4px 8px;
  background: rgba(10, 10, 15, 0.95);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: #fff;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s;
  z-index: 10;

  @include md-up {
    display: block;
  }
}

@media (hover: hover) and (pointer: fine) {
  .zone-marker:hover .zone-label {
    opacity: 1;
  }
}

.zones-legend {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-2);

  @media (max-width: 400px) {
    grid-template-columns: 1fr;
  }
}

.legend-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;

  &:hover {
    border-color: var(--zone-color);
    color: var(--color-text-primary);
    background: var(--color-surface-secondary);
  }

  &.active {
    border-color: var(--zone-color);
    color: var(--color-text-primary);
    background: rgba(112, 0, 255, 0.08);
    box-shadow: inset 0 0 10px rgba(112, 0, 255, 0.05);

    i {
      color: var(--zone-color);
    }
  }
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.legend-label {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
