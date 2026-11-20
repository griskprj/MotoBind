<template>
  <nav class="app-menu">
    <template v-for="(item, idx) in options" :key="item.key || `item-${idx}`">
      <!-- Divider -->
      <div v-if="item.type === 'divider'" class="app-menu__divider" />

      <!-- Group -->
      <div v-else-if="item.type === 'group'" class="app-menu__group">
        <div v-if="item.label" class="app-menu__group-label">{{ item.label }}</div>
        <ul class="app-menu__list">
          <li
            v-for="child in item.children"
            :key="child.key"
          >
            <button
              type="button"
              class="app-menu__item"
              :class="{ 'app-menu__item--active': isActive(child.key) }"
              @click="onSelect(child.key)"
            >
              <i v-if="child.icon" :class="[child.icon, 'app-menu__icon']" aria-hidden="true" />
              <span class="app-menu__label">{{ child.label }}</span>
              <span
                v-if="child.badge"
                class="app-menu__badge"
              >
                {{ child.badge }}
              </span>
            </button>
          </li>
        </ul>
      </div>

      <!-- Single item -->
      <button
        v-else
        type="button"
        class="app-menu__item"
        :class="{ 'app-menu__item--active': isActive(item.key) }"
        @click="onSelect(item.key)"
      >
        <i v-if="item.icon" :class="[item.icon, 'app-menu__icon']" aria-hidden="true" />
        <span class="app-menu__label">{{ item.label }}</span>
        <span v-if="item.badge" class="app-menu__badge">{{ item.badge }}</span>
      </button>
    </template>
  </nav>
</template>

<script setup>
const props = defineProps({
  /**
   * Массив пунктов. Формат:
   * [
   *   { type: 'group', label: 'Гараж', key: 'garage', children: [
   *     { label: 'Мой гараж', key: '/garage', icon: 'fa fa-motorcycle', badge: 3 },
   *   ]},
   *   { type: 'divider', key: 'd1' },
   *   { label: 'Выйти', key: '/logout', icon: 'fa fa-sign-out' },
   * ]
   */
  options: {
    type: Array,
    required: true,
  },
  /**
   * Текущий активный ключ (обычно route.path)
   */
  activeKey: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['select'])

function isActive(key) {
  if (!key || !props.activeKey) return false
  return props.activeKey === key || props.activeKey.startsWith(key + '/')
}

function onSelect(key) {
  if (!key) return
  emit('select', key)
}
</script>

<style scoped>
.app-menu {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  padding: var(--space-2) 0;
}

.app-menu__group {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-bottom: var(--space-2);
}

.app-menu__group-label {
  padding: var(--space-2) var(--space-3) var(--space-1);
  font-size: var(--text-xs);
  font-weight: var(--fw-semibold);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-muted);
}

.app-menu__list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.app-menu__item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  width: 100%;
  padding: var(--space-2) var(--space-3);
  border: none;
  background: transparent;
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  font-family: inherit;
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  text-align: left;
  cursor: pointer;
  transition: background var(--transition-fast), color var(--transition-fast);
  min-height: 40px;
}

.app-menu__item:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.app-menu__item--active {
  background: var(--accent-trans);
  color: var(--accent-text);
}

.app-menu__item--active:hover {
  background: var(--accent-trans);
  color: var(--accent-text);
}

.app-menu__icon {
  width: 20px;
  text-align: center;
  font-size: var(--text-base);
  flex-shrink: 0;
  color: inherit;
}

.app-menu__label {
  flex: 1;
  min-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.app-menu__badge {
  background: var(--accent);
  color: #fff;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: var(--radius-full);
  min-width: 20px;
  text-align: center;
  flex-shrink: 0;
}

.app-menu__divider {
  height: 1px;
  background: var(--border-light);
  margin: var(--space-2) var(--space-3);
}
</style>
