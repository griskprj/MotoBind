<template>
  <div class="admin-courses">
    <div class="admin-courses__head">
      <h2>Курсы</h2>
      <router-link
        :to="{ name: 'admin-learning-course-new' }"
        class="btn btn-primary"
      >
        <i class="fa fa-plus" />
        Новый курс
      </router-link>
    </div>

    <div v-if="store.coursesLoading" class="admin-courses__loading">
      <i class="fa fa-spinner fa-spin" /> Загрузка...
    </div>

    <div v-else-if="!store.courses.length" class="empty-state">
      <i class="fa fa-graduation-cap" />
      <p class="empty-text">Курсов пока нет</p>
      <router-link
        :to="{ name: 'admin-learning-course-new' }"
        class="btn btn-primary"
      >
        Создать первый
      </router-link>
    </div>

    <div v-else class="admin-table">
      <div class="admin-table__row admin-table__row--head">
        <div>Название</div>
        <div>Категория</div>
        <div>Уроков</div>
        <div>Цена</div>
        <div>Статус</div>
        <div></div>
      </div>

      <div
        v-for="c in store.courses"
        :key="c.id"
        class="admin-table__row"
      >
        <div class="admin-table__cell admin-table__cell--title">
          <router-link
            :to="{ name: 'admin-learning-course', params: { id: c.id } }"
            class="admin-table__link"
          >
            {{ c.title }}
          </router-link>
          <span class="admin-table__slug">{{ c.slug }}</span>
        </div>
        <div class="admin-table__cell">
          {{ categoryLabel(c.category) }}
        </div>
        <div class="admin-table__cell">
          {{ c.lessons_count }}
        </div>
        <div class="admin-table__cell">
          {{ c.is_free ? 'Бесплатно' : formatPrice(c.price) }}
        </div>
        <div class="admin-table__cell">
          <span class="status-badge" :class="`status-badge--${c.status}`">
            {{ statusLabel(c.status) }}
          </span>
        </div>
        <div class="admin-table__cell admin-table__cell--actions">
          <router-link
            :to="{ name: 'admin-learning-course', params: { id: c.id } }"
            class="icon-btn"
            title="Редактировать"
          >
            <i class="fa fa-pen" />
          </router-link>
          <button
            type="button"
            class="icon-btn icon-btn--danger"
            title="Удалить"
            @click="confirmDelete(c)"
          >
            <i class="fa fa-trash" />
          </button>
        </div>
      </div>
    </div>

    <BasePagination
      v-if="store.coursesPagination?.pages > 1"
      :pagination="store.coursesPagination"
      @change="onPageChange"
    />

    <ConfirmModal
      :is-open="deleteTarget !== null"
      title="Удалить курс?"
      :message="`Курс «${deleteTarget?.title}» и все его уроки будут удалены безвозвратно.`"
      confirm-text="Удалить"
      @close="deleteTarget = null"
      @confirm="doDelete"
    />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import BasePagination from '@/components/learning/BasePagination.vue'
import ConfirmModal from '@/components/ui/ConfirmModal.vue'
import { useAdminLearningStore } from '@/stores'
import { useToast } from '@/composables/useToast'

const store = useAdminLearningStore()
const toast = useToast()
const deleteTarget = ref(null)

onMounted(load)

function load(page = 1) {
  store.loadCourses(page, 20).catch(() => toast.error('Не удалось загрузить'))
}

function onPageChange(page) {
  load(page)
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function confirmDelete(course) {
  deleteTarget.value = course
}

async function doDelete() {
  if (!deleteTarget.value) return
  try {
    await store.deleteCourse(deleteTarget.value.id)
    toast.success('Курс удалён')
  } catch (err) {
    toast.error(err.response?.data?.error || 'Не удалось удалить')
  } finally {
    deleteTarget.value = null
  }
}

function categoryLabel(c) {
  const map = {
    riding: 'Вождение',
    repair: 'Ремонт',
    gear: 'Экипировка',
    first_aid: 'Первая помощь',
    law: 'Право',
    travel: 'Путешествия',
  }
  return map[c] || c
}

function statusLabel(s) {
  const map = { draft: 'Черновик', published: 'Опубликован', archived: 'В архиве' }
  return map[s] || s
}

function formatPrice(p) {
  return `${Math.floor(p / 100)} ₽`
}
</script>

<style scoped>
.admin-courses {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.admin-courses__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
}

.admin-courses__head h2 {
  margin: 0;
  font-size: var(--text-xl);
}

.admin-courses__loading {
  padding: 40px;
  text-align: center;
  color: var(--text-muted);
  font-size: var(--text-sm);
}

/* Таблица */
.admin-table {
  display: flex;
  flex-direction: column;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.admin-table__row {
  display: grid;
  grid-template-columns: 2fr 1fr 80px 100px 120px 80px;
  gap: 12px;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-light);
  align-items: center;
  font-size: var(--text-sm);
}

.admin-table__row:last-child {
  border-bottom: none;
}

.admin-table__row--head {
  background: var(--bg-secondary);
  font-size: var(--text-xs);
  font-weight: var(--fw-semibold);
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: var(--text-muted);
}

.admin-table__row:not(.admin-table__row--head):hover {
  background: var(--bg-card-hover);
}

.admin-table__cell {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.admin-table__cell--title {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.admin-table__link {
  color: var(--text-primary);
  font-weight: var(--fw-medium);
  text-decoration: none;
}

.admin-table__link:hover {
  color: var(--accent-text);
}

.admin-table__slug {
  font-size: 11px;
  color: var(--text-muted);
  font-family: var(--font-mono);
}

.admin-table__cell--actions {
  display: flex;
  gap: 4px;
  justify-content: flex-end;
  overflow: visible;
}

.icon-btn {
  width: 32px;
  height: 32px;
  min-height: 32px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  padding: 0;
  text-decoration: none;
}

.icon-btn:hover {
  border-color: var(--accent);
  color: var(--accent-text);
  background: var(--accent-trans);
}

.icon-btn--danger:hover {
  border-color: var(--danger);
  color: var(--danger-text);
  background: var(--danger-trans);
}

.status-badge {
  display: inline-flex;
  padding: 3px 10px;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: var(--fw-semibold);
  white-space: nowrap;
}

.status-badge--draft {
  background: var(--border-light);
  color: var(--text-secondary);
}

.status-badge--published {
  background: var(--success-trans);
  color: var(--success-text);
}

.status-badge--archived {
  background: var(--warning-trans);
  color: var(--warning-text);
}

@media (max-width: 860px) {
  .admin-table__row {
    grid-template-columns: 1fr;
    gap: 6px;
  }

  .admin-table__row--head {
    display: none;
  }

  .admin-table__cell--actions {
    justify-content: flex-start;
  }
}
</style>
