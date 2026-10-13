<template>
  <article class="manual-card" @click="openManual(manual.id)">
    <!-- Превью -->
    <div class="manual-card__preview">
      <img
        v-if="manual.image_url"
        :src="getManualImageUrl(manual.image_url)"
        :alt="manual.title"
        loading="lazy"
      >
      <div v-else class="manual-card__placeholder">
        <i class="fa fa-book" />
      </div>

      <span
        v-if="manual.category"
        class="manual-card__category"
      >
        {{ categoryLabel(manual.category) }}
      </span>
    </div>

    <!-- Тело -->
    <div class="manual-card__body">
      <h4 class="manual-card__title">{{ manual.title }}</h4>

      <p v-if="manual.moto_name || manual.motorcycle_name" class="manual-card__moto">
        <i class="fa fa-motorcycle" />
        {{ manual.moto_name || manual.motorcycle_name }}
      </p>

      <div class="manual-card__meta">
        <span v-if="manual.steps_count || manual.steps?.length" class="manual-card__meta-item">
          <i class="fa fa-list-ol" />
          {{ manual.steps_count || manual.steps.length }} шагов
        </span>
        <span v-if="manual.author_name" class="manual-card__meta-item">
          <i class="fa fa-user" />
          {{ manual.author_name }}
        </span>
        <span v-if="manual.likes_count" class="manual-card__meta-item">
          <i class="fa fa-heart" />
          {{ manual.likes_count }}
        </span>
      </div>
    </div>
  </article>
</template>

<script setup>
import { getManualImageUrl } from '@/utils/mediaUrl'

defineProps({
  manual: { type: Object, required: true },
})

const emit = defineEmits(['click'])

const CATEGORY_LABELS = {
  engine: 'Двигатель',
  drive: 'Привод',
  steering: 'Рулевое',
  suspension: 'Подвеска',
  electronics: 'Электроника',
  wheel: 'Колёса',
  brakes: 'Тормоза',
  fuel: 'Топливная',
  cooling: 'Охлаждение',
}

function categoryLabel(cat) {
  return CATEGORY_LABELS[cat] || cat
}

function openManal(id) {
  router.push(`/manuals/${id}`)
}
</script>

<style scoped>
.manual-card {
  display: flex;
  flex-direction: column;
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  overflow: hidden;
  cursor: pointer;
  transition: all var(--transition-base);
}

.manual-card:hover {
  border-color: var(--accent);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.manual-card__preview {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  background: var(--bg-card);
  overflow: hidden;
}

.manual-card__preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-base);
}

.manual-card:hover .manual-card__preview img {
  transform: scale(1.05);
}

.manual-card__placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  font-size: 36px;
  opacity: 0.4;
}

.manual-card__category {
  position: absolute;
  top: var(--space-2);
  left: var(--space-2);
  background: var(--accent);
  color: #fff;
  font-size: 11px;
  font-weight: var(--fw-semibold);
  padding: 3px 10px;
  border-radius: var(--radius-full);
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.manual-card__body {
  padding: var(--space-3) var(--space-4) var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.manual-card__title {
  margin: 0;
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
  line-height: var(--leading-tight);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.manual-card__moto {
  margin: 0;
  font-size: var(--text-xs);
  color: var(--text-secondary);
  display: inline-flex;
  align-items: center;
  gap: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.manual-card__moto i {
  color: var(--accent-text);
}

.manual-card__meta {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  font-size: var(--text-xs);
  color: var(--text-muted);
  margin-top: auto;
}

.manual-card__meta-item {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
</style>
