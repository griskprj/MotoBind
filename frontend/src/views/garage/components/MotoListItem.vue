<template>
  <div
    class="moto-list-item"
    :class="{ active: selected }"
    @click="emit('select', moto)"
  >
    <div class="moto-card-wrapper">
      <div class="moto-list-preview">
        <img
          v-if="moto.photo_url"
          :src="getMotoPhotoUrl(moto.photo_url)"
          :alt="moto.name"
          loading="lazy"
        >
        <div v-else class="moto-list-placeholder">
          <i class="fa fa-motorcycle"></i>
        </div>
      </div>

      <div class="moto-list-info">
        <div class="moto-list-header">
          <h3 class="moto-list-name">{{ moto.name }}</h3>
          <span class="moto-list-year">{{ moto.years }}</span>
          <span class="moto-list-volume">{{ moto.volume }} см³</span>
        </div>
        <div class="moto-list-meta">
          <span class="moto-list-mileage">
            <i class="fa-solid fa-gauge-high"></i>
            {{ formatMileage(moto.mileage) }}
          </span>
          <span class="moto-list-color">
            <span class="color-dot-sm" :style="{ background: moto.color }"></span>
          </span>
          <span v-if="moto.maintenances?.length" class="moto-list-maintenances">
            <i class="fa fa-wrench"></i>
            {{ moto.maintenances.length }}
          </span>
        </div>
      </div>
    </div>

    <div class="moto-list-actions" @click.stop>
      <button class="icon-btn" title="Редактировать" @click="emit('edit', moto)">
        <i class="fa fa-pen"></i>
      </button>
      <button class="icon-btn" title="Обновить пробег" @click="emit('update-mileage', moto)">
        <i class="fa-solid fa-gauge-high"></i>
      </button>
      <button class="icon-btn" title="Фото" @click="emit('photo', moto)">
        <i class="fa fa-camera"></i>
      </button>
      <button class="icon-btn danger" title="Удалить" @click="emit('delete', moto)">
        <i class="fa fa-trash"></i>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { formatMileage } from '@/utils/formatters'
import { getMotoPhotoUrl } from '@/utils/mediaUrl'

defineProps<{
  moto: any
  selected: boolean
}>()

const emit = defineEmits<{
  select: [any]
  edit: [any]
  'update-mileage': [any]
  photo: [any]
  delete: [any]
}>()
</script>

<style scoped>
.moto-list-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 16px;
  background: var(--bg-secondary);
  border: 2px solid transparent;
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-base);
}

.moto-list-item:hover {
  background: var(--bg-card-hover);
  border-color: var(--border-light);
}

.moto-list-item.active {
  border-color: var(--accent);
  background: var(--accent-trans);
  box-shadow: 0 0 0 1px var(--accent-trans);
}

.moto-card-wrapper {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
  min-width: 0;
}

.moto-list-preview {
  position: relative;
  width: 56px;
  height: 56px;
  border-radius: var(--radius-md);
  overflow: hidden;
  flex-shrink: 0;
  background: var(--bg-card);
}

.moto-list-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.moto-list-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  font-size: 22px;
  background: var(--bg-card);
}

.moto-list-info {
  flex: 1;
  min-width: 0;
}

.moto-list-header {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.moto-list-name {
  font-size: 15px;
  font-weight: var(--fw-semibold);
  margin: 0;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.moto-list-year {
  font-size: 13px;
  color: var(--text-muted);
  flex-shrink: 0;
}

.moto-list-volume {
  font-size: 12px;
  color: var(--text-muted);
  background: var(--bg-primary);
  padding: 2px 12px;
  border-radius: var(--radius-full);
  flex-shrink: 0;
}

.moto-list-meta {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-top: 3px;
  flex-wrap: wrap;
}

.moto-list-mileage {
  font-size: 13px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 4px;
}

.moto-list-mileage i {
  font-size: 12px;
  color: var(--text-muted);
}

.moto-list-color {
  display: flex;
  align-items: center;
}

.color-dot-sm {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 1px solid var(--border-color);
  display: block;
  transition: transform var(--transition-base);
}

.moto-list-item:hover .color-dot-sm {
  transform: scale(1.15);
}

.moto-list-maintenances {
  font-size: 12px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 4px;
}

.moto-list-maintenances i {
  font-size: 12px;
}

.moto-list-actions {
  display: flex;
  gap: 2px;
  flex-shrink: 0;
  opacity: 0.6;
  transition: opacity var(--transition-base);
}

.moto-list-item:hover .moto-list-actions {
  opacity: 1;
}

.icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  min-height: 34px;
  padding: 0;
  border: none;
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  transition: all var(--transition-base);
  font-size: 14px;
  line-height: 1;
  flex-shrink: 0;
  touch-action: manipulation;
}

.icon-btn:hover {
  background: var(--border-light);
  color: var(--text-primary);
}

.icon-btn.danger:hover {
  background: var(--danger-trans);
  color: var(--danger);
}

.icon-btn i {
  pointer-events: none;
}

@media (max-width: 640px) {
  .moto-list-item {
    padding: 10px 12px;
    gap: 10px;
  }

  .moto-list-preview {
    width: 48px;
    height: 48px;
  }

  .moto-list-name {
    font-size: 14px;
  }

  .moto-list-actions {
    opacity: 1;
    gap: 0;
  }

  .icon-btn {
    width: 32px;
    height: 32px;
    min-height: 32px;
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .moto-list-item {
    flex-wrap: wrap;
  }

  .moto-card-wrapper {
    flex-basis: 100%;
  }

  .moto-list-actions {
    width: 100%;
    justify-content: flex-end;
    padding-top: 8px;
    border-top: 1px solid var(--border-light);
    opacity: 1;
  }
}

@media (max-width: 400px) {
  .moto-list-meta {
    gap: 8px;
  }

  .moto-list-volume {
    font-size: 11px;
    padding: 1px 10px;
  }

  .moto-list-actions {
    justify-content: space-between;
  }

  .icon-btn {
    width: 34px;
    height: 34px;
    min-height: 34px;
  }
}
</style>
