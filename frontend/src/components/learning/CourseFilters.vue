<template>
  <div class="course-filters">
    <div class="course-filters__search">
      <i class="fa fa-search" />
      <input
        :value="filters.search"
        type="text"
        placeholder="Поиск курсов..."
        @input="onSearch"
      />
    </div>

    <select
      :value="filters.category"
      class="course-filters__select"
      @change="onCategory"
    >
      <option value="">Все категории</option>
      <option v-for="c in categories" :key="c.id" :value="c.id">
        {{ c.label }}
      </option>
    </select>

    <select
      :value="filters.level"
      class="course-filters__select"
      @change="onLevel"
    >
      <option value="">Любой уровень</option>
      <option value="beginner">Начальный</option>
      <option value="intermediate">Средний</option>
      <option value="advanced">Продвинутый</option>
    </select>

    <select
      :value="String(filters.is_free)"
      class="course-filters__select"
      @change="onPrice"
    >
      <option value="null">Все</option>
      <option value="true">Бесплатные</option>
      <option value="false">Платные</option>
    </select>
  </div>
</template>

<script setup>
defineProps({
  filters: { type: Object, required: true },
})

const emit = defineEmits(['change'])

const categories = [
  { id: 'riding', label: 'Вождение' },
  { id: 'repair', label: 'Ремонт' },
  { id: 'gear', label: 'Экипировка' },
  { id: 'first_aid', label: 'Первая помощь' },
  { id: 'law', label: 'Право' },
  { id: 'travel', label: 'Путешествия' },
]

function onSearch(e) {
  emit('change', { search: e.target.value })
}

function onCategory(e) {
  emit('change', { category: e.target.value })
}

function onLevel(e) {
  emit('change', { level: e.target.value })
}

function onPrice(e) {
  const v = e.target.value
  emit('change', { is_free: v === 'null' ? null : v === 'true' })
}
</script>

<style scoped>
.course-filters {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  align-items: center;
}

.course-filters__search {
  position: relative;
  flex: 1;
  min-width: 200px;
  display: flex;
  align-items: center;
}

.course-filters__search i {
  position: absolute;
  left: 12px;
  color: var(--text-muted);
  font-size: 13px;
  pointer-events: none;
}

.course-filters__search input {
  width: 100%;
  padding: 10px 12px 10px 34px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--bg-input);
  color: var(--text-primary);
  font-family: inherit;
  font-size: var(--text-sm);
  transition: border-color var(--transition-fast);
}

.course-filters__search input:focus {
  outline: none;
  border-color: var(--accent);
}

.course-filters__select {
  padding: 10px 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--bg-input);
  color: var(--text-primary);
  font-family: inherit;
  font-size: var(--text-sm);
  cursor: pointer;
  min-width: 140px;
}

.course-filters__select:focus {
  outline: none;
  border-color: var(--accent);
}
</style>
