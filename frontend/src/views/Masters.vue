<template>
  <div class="container">
    <LoadingOverlay :isLoading="loading" text="Загрузка мастеров..."/>

    <Header
      title="Мастера и СТО"
      subtitle="Найдите специалиста для обслуживания мотоцикла"
    />

    <!-- Фильтры -->
    <div class="filters-bar">
      <div class="search-wrap">
        <i class="fa fa-search"></i>
        <input
          v-model="search"
          type="text"
          placeholder="Название, город"
          @input="onSearchInput"
        >
        <button v-if="search" class="clear-search" @click="clearSearch">
          <i class="fa fa-times"></i>
        </button>
      </div>

      <select v-model="filterType" class="filter-select" @change="loadMasters">
        <option value="">Все типы</option>
        <option value="master">Частные мастера</option>
        <option value="station">СТО</option>
      </select>

      <select v-model="filterCity" class="filter-select" @change="loadMasters">
        <option value="">Все города</option>
        <option v-for="c in cities" :key="c" :value="c">{{ c }}</option>
      </select>
    </div>

    <!-- Результаты -->
    <div class="results-info">
      Найдено: <strong>{{ masters.length }}</strong>
    </div>

    <div v-if="masters.length" class="masters-grid">
      <router-link
        v-for="m in masters"
        :key="m.slug"
        :to="`/business/${m.slug}`"
        class="master-card"
      >
        <div class="master-top">
          <div class="master-logo">
            <img
              v-if="m.logo_url"
              :src="getBusinessLogoUrl(m.logo_url)"
              alt=""
              @error="(e) => (e.target.style.display = 'none')"
            >
            <i v-else class="fa" :class="m.type === 'station' ? 'fa-warehouse' : 'fa-user-gear'"></i>
          </div>
          <div class="master-info">
            <div class="master-type-badge">
              {{ m.type === 'station' ? 'СТО' : 'Мастер' }}
            </div>
            <div class="master-name">{{ m.name }}</div>
            <div v-if="m.city" class="master-city">
              <i class="fa fa-map-marker"></i> {{ m.city }}
            </div>
          </div>
        </div>

        <p v-if="m.description" class="master-desc">{{ m.description }}</p>

        <div class="master-footer">
          <span class="master-services-count">
            <i class="fa fa-wrench"></i>
            {{ m.services_count }} услуг
          </span>
          <span class="master-cta">
            Открыть <i class="fa fa-arrow-right"></i>
          </span>
        </div>
      </router-link>
    </div>

    <div v-else-if="!loading" class="empty">
      <i class="fa fa-search"></i>
      <h3>Мастеров не найдено</h3>
      <p>Попробуйте изменить фильтры</p>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import api from '@/api/api'
import { useToast } from '@/composables/useToast'
import { getBusinessLogoUrl } from '@/utils/mediaUrl'
import Header from '@/components/Header.vue'
import LoadingOverlay from '@/components/LoadingOverlay.vue'

const toast = useToast()

const masters = ref([])
const cities = ref([])
const loading = ref(false)

const search = ref('')
const filterType = ref('')
const filterCity = ref('')

let timer = null

onMounted(() => {
  loadMasters()
  loadCities()
})

async function loadMasters() {
  loading.value = true
  try {
    const params = {}
    if (search.value.trim()) params.search = search.value.trim()
    if (filterType.value) params.type = filterType.value
    if (filterCity.value) params.city = filterCity.value

    const { data } = await api.get('/business/catalog', { params })
    masters.value = data.masters || []
    if (data.cities && !cities.value.length) {
      cities.value = data.cities
    }
  } catch (err) {
    toast.error('Не удалось загрузить мастеров')
  } finally {
    loading.value = false
  }
}

async function loadCities() {
  try {
    const { data } = await api.get('/business/catalog/cities')
    cities.value = data.cities || []
  } catch {
    // молча
  }
}

function onSearchInput() {
  clearTimeout(timer)
  timer = setTimeout(loadMasters, 350)
}

function clearSearch() {
  search.value = ''
  loadMasters()
}
</script>

<style scoped>
.filters-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.search-wrap {
  flex: 1;
  min-width: 240px;
  position: relative;
  display: flex;
  align-items: center;
}
.search-wrap > i {
  position: absolute;
  left: 14px;
  color: var(--text-muted);
  pointer-events: none;
}
.search-wrap input {
  width: 100%;
  padding: 10px 40px 10px 40px;
  border: 1px solid var(--border-input);
  border-radius: var(--radius-md);
  background: var(--bg-input);
  color: var(--text-primary);
  font-size: 14px;
}
.search-wrap input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: var(--shadow-focus);
}
.clear-search {
  position: absolute;
  right: 8px;
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 6px;
  min-height: 28px;
  border-radius: var(--radius-sm);
}

.filter-select {
  padding: 10px 14px;
  background: var(--bg-input);
  border: 1px solid var(--border-input);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  font-size: 14px;
  cursor: pointer;
  min-width: 160px;
}
.filter-select:focus {
  outline: none;
  border-color: var(--accent);
}

.results-info {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 12px;
}
.results-info strong { color: var(--text-primary); }

.masters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 14px;
}

.master-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 18px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  text-decoration: none;
  color: inherit;
  transition: all var(--transition-base);
}
.master-card:hover {
  border-color: var(--accent);
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

.master-top {
  display: flex;
  gap: 14px;
  align-items: center;
}
.master-logo {
  width: 54px;
  height: 54px;
  min-height: 54px;
  border-radius: 50%;
  background: var(--accent-trans);
  color: var(--accent-text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  overflow: hidden;
  flex-shrink: 0;
  border: 2px solid var(--accent);
}
.master-logo img { width: 100%; height: 100%; object-fit: cover; }

.master-info { flex: 1; min-width: 0; }
.master-type-badge {
  display: inline-block;
  padding: 1px 8px;
  border-radius: var(--radius-full);
  background: var(--accent-trans);
  color: var(--accent-text);
  font-size: 10px;
  font-weight: var(--fw-semibold);
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin-bottom: 4px;
}
.master-name {
  font-size: 15px;
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.master-city {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.master-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.master-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  border-top: 1px solid var(--border-light);
  font-size: 12px;
}
.master-services-count {
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 5px;
}
.master-cta {
  color: var(--accent-text);
  font-weight: var(--fw-medium);
  display: flex;
  align-items: center;
  gap: 4px;
}

.empty {
  text-align: center;
  padding: 60px 20px;
  background: var(--bg-card);
  border: 1px dashed var(--border-color);
  border-radius: var(--radius-lg);
}
.empty i { font-size: 42px; color: var(--text-muted); margin-bottom: 12px; display: block; }
.empty h3 { margin: 0 0 8px; }
.empty p { color: var(--text-secondary); margin: 0; }

@media (max-width: 640px) {
  .filters-bar { flex-direction: column; }
  .filter-select { width: 100%; }
  .masters-grid { grid-template-columns: 1fr; }
}
</style>
