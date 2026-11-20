<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'

const { render } = useMarkdown()
const route = useRoute()
const api = useApi()
const auth = useAuthStore()
const toast = useToast()

const { data: manual, pending, error } = await useAsyncData(
  `manual-${route.params.id}`,
  () => api.manuals.get(route.params.id as string)
)

if (error.value || !manual.value) {
  throw createError({ statusCode: 404, statusMessage: 'Мануал не найден' })
}

const config = useRuntimeConfig()
const canonicalUrl = `${config.public.siteUrl}/manuals/${manual.value.id}`

useSeoMeta({
  title: `${manual.value.title} — MotoBind`,
  description: manual.value.description?.slice(0, 160) || 'Инструкция по ремонту мотоцикла',
  ogTitle: manual.value.title,
  ogDescription: manual.value.description?.slice(0, 200),
  ogImage: `${config.public.siteUrl}/icons/icon-512x512.png`,
  ogType: 'article',
  twitterCard: 'summary_large_image',
  articlePublishedTime: manual.value.created_at,
  robots: 'index, follow',
})

useHead({
  link: [{ rel: 'canonical', href: canonicalUrl }]
})

useHead({
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'HowTo',
        name: manual.value.title,
        description: manual.value.description,
        totalTime: manual.value.time_estimate ? `PT${manual.value.time_estimate.replace(' мин', 'M')}` : undefined,
        tool: manual.value.instruments ? [{ '@type': 'HowToTool', name: manual.value.instruments }] : undefined,
        step: manual.value.steps.map((s, i) => ({
          '@type': 'HowToStep',
          position: i + 1,
          name: s.title,
          text: s.text || '',
        })),
      }),
    },
  ],
})

// --- СОСТОЯНИЕ ВЫПОЛНЕНИЯ ---
const isExecuting = ref(false)
const currentStepIndex = ref(0)
const completedSteps = ref<Set<number>>(new Set())

// Загрузка прогресса из localStorage
onMounted(() => {
  const saved = localStorage.getItem(`manual_progress_${manual.value?.id}`)
  if (saved) {
    try {
      const parsed = JSON.parse(saved)
      completedSteps.value = new Set(parsed.completed || [])
      currentStepIndex.value = parsed.current || 0
      // Если прогресс есть, но не все шаги пройдены, можно предложить продолжить
      if (completedSteps.value.size > 0 && completedSteps.value.size < manual.value.steps.length) {
        // Опционально: показать уведомление "Продолжить?"
      }
    } catch (e) {}
  }
})

// Сохранение прогресса
watch([completedSteps, currentStepIndex], () => {
  if (!manual.value) return
  localStorage.setItem(`manual_progress_${manual.value.id}`, JSON.stringify({
    completed: Array.from(completedSteps.value),
    current: currentStepIndex.value
  }))
}, { deep: true })

// Вычисления прогресса
const totalSteps = computed(() => manual.value?.steps.length || 0)
const progressPercent = computed(() => {
  if (totalSteps.value === 0) return 0
  return Math.round((completedSteps.value.size / totalSteps.value) * 100)
})

const currentStep = computed(() => {
  if (!manual.value || !manual.value.steps[currentStepIndex.value]) return null
  return manual.value.steps[currentStepIndex.value]
})

// --- ДЕЙСТВИЯ ---
function startExecution() {
  isExecuting.value = true
  currentStepIndex.value = 0
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function toggleStepCompletion(index: number) {
  const newSet = new Set(completedSteps.value)
  if (newSet.has(index)) {
    newSet.delete(index)
  } else {
    newSet.add(index)
    // Автоматически переключаем на следующий шаг, если текущий выполнен
    if (index === currentStepIndex.value && index < totalSteps.value - 1) {
      currentStepIndex.value = index + 1
    }
  }
  completedSteps.value = newSet
}

function goToStep(index: number) {
  currentStepIndex.value = index
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function finishManual() {
  if (completedSteps.value.size === totalSteps.value) {
    toast.success('Поздравляем! Мануал успешно выполнен!')
  } else {
    toast.info('Вы завершили прохождение, но не все шаги отмечены.')
  }
  isExecuting.value = false
  localStorage.removeItem(`manual_progress_${manual.value?.id}`)
  completedSteps.value = new Set()
  currentStepIndex.value = 0
}

function exitExecution() {
  isExecuting.value = false
}

// Форматирование
const formatDate = (iso?: string) => {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short', year: 'numeric' })
}
</script>

<template>
  <div v-if="manual" class="page-manual" :class="{ 'is-executing': isExecuting }">

    <!-- ========================================== -->
    <!-- РЕЖИМ ПРОХОЖДЕНИЯ (Выполнение)             -->
    <!-- ========================================== -->
    <template v-if="isExecuting">
      <!-- Верхняя панель управления -->
      <div class="execution-header">
        <div class="eh-left">
          <div class="eh-icon"><i class="fa-solid fa-play"></i></div>
          <div>
            <h1 class="eh-title">Выполнение мануала</h1>
            <span class="eh-subtitle">Шаг {{ currentStepIndex + 1 }} из {{ totalSteps }}</span>
          </div>
        </div>

        <div class="eh-progress">
          <div class="eh-progress-bar">
            <div class="eh-progress-fill" :style="{ width: progressPercent + '%' }"></div>
          </div>
          <span class="eh-progress-text">{{ progressPercent }}%</span>
        </div>

        <div class="eh-actions">
          <BaseButton variant="secondary" @click="exitExecution">Выйти</BaseButton>
          <BaseButton variant="primary" @click="finishManual">
            <i class="fa-solid fa-check"></i> Завершить
          </BaseButton>
        </div>
      </div>

      <div class="execution-layout">
        <!-- Левая колонка: Текущий шаг -->
        <div class="exec-main">
          <div v-if="currentStep" class="current-step-card">
            <div class="csc-header">
              <span class="badge">Шаг {{ currentStepIndex + 1 }} из {{ totalSteps }}</span>
              <h2 class="csc-title">{{ currentStep.title }}</h2>
            </div>

            <div class="csc-body">
              <div class="csc-text">
                <p v-if="currentStep.text" class="markdown-body" v-html="render(currentStep.text)" />

                <!-- Чек-лист (если в шаге есть подпункты) -->
                <div v-if="currentStep.tip || currentStep.warning" class="step-alerts">
                  <div v-if="currentStep.tip" class="alert-box info">
                    <i class="fa-solid fa-lightbulb"></i>
                    <span>{{ currentStep.tip }}</span>
                  </div>
                  <div v-if="currentStep.warning" class="alert-box danger">
                    <i class="fa-solid fa-triangle-exclamation"></i>
                    <span>{{ currentStep.warning }}</span>
                  </div>
                </div>

                <!-- Кнопка отметки -->
                <div class="csc-actions">
                  <BaseButton
                    variant="secondary"
                    :disabled="currentStepIndex === 0"
                    @click="goToStep(currentStepIndex - 1)"
                  >
                    <i class="fa-solid fa-arrow-left"></i> Назад
                  </BaseButton>

                  <BaseButton
                    variant="primary"
                    @click="toggleStepCompletion(currentStepIndex)"
                  >
                    <i class="fa-solid fa-check"></i> Отметить как выполнено
                  </BaseButton>
                </div>
              </div>

              <!-- Картинка шага -->
              <div v-if="currentStep.image" class="csc-image">
                <img :src="useMediaUrl()(currentStep.image)!" alt="Изображение шага" />
              </div>
            </div>
          </div>
        </div>

        <!-- Правая колонка: Содержание -->
        <div class="exec-sidebar">
          <div class="sidebar-widget">
            <h3 class="sidebar-title">Ход выполнения</h3>
            <div class="sidebar-progress-info">
              <span>{{ completedSteps.size }} из {{ totalSteps }} шагов</span>
              <span>{{ progressPercent }}%</span>
            </div>
            <div class="sidebar-progress-bar">
              <div class="sidebar-progress-fill" :style="{ width: progressPercent + '%' }"></div>
            </div>

            <div class="steps-nav-list">
              <div
                v-for="(step, idx) in manual.steps"
                :key="step.id"
                class="nav-step-item"
                :class="{
                  'is-active': idx === currentStepIndex,
                  'is-completed': completedSteps.has(idx)
                }"
                @click="goToStep(idx)"
              >
                <div class="nav-step-marker">
                  <i v-if="completedSteps.has(idx)" class="fa-solid fa-check"></i>
                  <span v-else>{{ idx + 1 }}</span>
                </div>
                <span class="nav-step-text">{{ step.title }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Нижний блок: Все шаги (Аккордеон) -->
      <div class="all-steps-section">
        <h3 class="section-title"><i class="fa-solid fa-list-ul"></i> Все шаги</h3>
        <div class="accordion-list">
          <div
            v-for="(step, idx) in manual.steps"
            :key="step.id"
            class="accordion-item"
            :class="{ 'is-expanded': idx === currentStepIndex }"
          >
            <div class="accordion-header" @click="goToStep(idx)">
              <div class="acc-num">{{ idx + 1 }}</div>
              <span class="acc-title">{{ step.title }}</span>
              <span v-if="idx === currentStepIndex" class="acc-badge">Текущий</span>
              <i class="fa-solid fa-chevron-down acc-icon"></i>
            </div>
            <div v-if="idx === currentStepIndex" class="accordion-body">
              <p class="markdown-body" v-html="render(step.text || '')" />
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- ========================================== -->
    <!-- РЕЖИМ ЧТЕНИЯ (Просмотр)                    -->
    <!-- ========================================== -->
    <template v-else>
      <header class="manual-header">
        <div class="header-actions">
          <NuxtLink to="/manuals" class="back-link">
            <i class="fa-solid fa-arrow-left"></i> Все мануалы
          </NuxtLink>
          <BaseButton
            v-if="manual.author_id === auth.user?.id || auth.isAdmin"
            :to="`/manuals/edit/${manual.id}`"
            variant="secondary"
            size="sm"
          >
            <i class="fa-solid fa-pen"></i> Редактировать
          </BaseButton>
        </div>

        <div class="meta">
          <span class="category">{{ manual.category }}</span>
          <span v-if="manual.difficult" class="difficulty">
            <i class="fa-solid fa-signal"></i> {{ manual.difficult === 'easy' ? 'Легко' : manual.difficult === 'medium' ? 'Средне' : 'Сложно' }}
          </span>
          <span v-if="manual.time_estimate"><i class="fa-regular fa-clock"></i> {{ manual.time_estimate }}</span>
          <span v-if="manual.motorcycle"><i class="fa-solid fa-motorcycle"></i> {{ manual.motorcycle }}</span>
        </div>

        <h1 class="manual-title">{{ manual.title }}</h1>
        <p class="manual-desc markdown-body" v-html="render(manual.description)" />

        <!-- Кнопка запуска прохождения -->
        <div class="start-execution-btn">
          <BaseButton variant="primary" size="lg" @click="startExecution">
            <i class="fa-solid fa-play"></i> Начать выполнение
          </BaseButton>
        </div>
      </header>

      <div class="read-layout">
        <div class="read-main">
          <!-- Блок безопасности -->
          <section v-if="manual.safety_tip || manual.warnings || manual.conditions" class="safety-section">
            <h2 class="section-title"><i class="fa-solid fa-shield-halved"></i> Безопасность и подготовка</h2>

            <div class="safety-block">
              <!-- Полоса слева (выноска) -->
              <div class="safety-accent"></div>

              <div class="safety-content">
                <div v-if="manual.safety_tip" class="safety-row">
                  <i class="fa-solid fa-lightbulb text-info"></i>
                  <div>
                    <span class="safety-label">Совет по безопасности</span>
                    <p class="safety-text">{{ manual.safety_tip }}</p>
                  </div>
                </div>
                <div v-if="manual.warnings" class="safety-row">
                  <i class="fa-solid fa-triangle-exclamation text-danger"></i>
                  <div>
                    <span class="safety-label">Предупреждения</span>
                    <p class="safety-text">{{ manual.warnings }}</p>
                  </div>
                </div>
                <div v-if="manual.conditions" class="safety-row">
                  <i class="fa-solid fa-circle-check text-success"></i>
                  <div>
                    <span class="safety-label">Условия выполнения</span>
                    <p class="safety-text">{{ manual.conditions }}</p>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- Инструменты и материалы -->
          <section v-if="manual.instruments || manual.parts" class="tools-section">
            <h2 class="section-title"><i class="fa-solid fa-screwdriver-wrench"></i> Инструменты и материалы</h2>
            <div class="tools-grid">
              <div v-if="manual.instruments" class="tool-block">
                <h3><i class="fa-solid fa-screwdriver"></i> Инструменты</h3>
                <p>{{ manual.instruments }}</p>
              </div>
              <div v-if="manual.parts" class="tool-block">
                <h3><i class="fa-solid fa-box"></i> Материалы и запчасти</h3>
                <p>{{ manual.parts }}</p>
              </div>
            </div>
          </section>

          <!-- Шаги -->
          <section class="steps-section">
            <h2 class="section-title"><i class="fa-solid fa-list-ol"></i> Пошаговое выполнение</h2>
            <div class="steps-list">
              <div v-for="step in manual.steps" :key="step.id" class="step-card">
                <div class="step-number">{{ step.order }}</div>
                <div class="step-content">
                  <h3 class="step-title">{{ step.title }}</h3>
                  <p v-if="step.text" class="step-text markdown-body" v-html="render(step.text)" />

                  <img v-if="step.image" :src="useMediaUrl()(step.image)!" class="step-image" loading="lazy" />

                  <div v-if="step.tip" class="step-alert tip">
                    <i class="fa-solid fa-lightbulb"></i> {{ step.tip }}
                  </div>
                  <div v-if="step.warning" class="step-alert warning">
                    <i class="fa-solid fa-triangle-exclamation"></i> {{ step.warning }}
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>

        <!-- Правая колонка (Сайдбар) -->
        <div class="read-sidebar">
          <div class="sidebar-card">
            <h3 class="sidebar-title">Содержание</h3>

            <div class="timeline-list">
              <div
                v-for="(step, idx) in manual.steps"
                :key="step.id"
                class="timeline-item"
                :class="{ 'is-current': idx === 0 }"
              >
                <div class="timeline-marker"></div>
                <span class="timeline-text">{{ idx + 1 }}. {{ step.title }}</span>
              </div>
            </div>
          </div>

          <div class="sidebar-card">
            <h3 class="sidebar-title">О мануале</h3>
            <div class="info-list">
              <div class="info-row">
                <span class="info-label"><i class="fa-solid fa-motorcycle"></i> Мотоцикл</span>
                <span class="info-val">{{ manual.motorcycle || 'Любой' }}</span>
              </div>
              <div class="info-row">
                <span class="info-label"><i class="fa-solid fa-signal"></i> Сложность</span>
                <span class="info-val">{{ manual.difficult === 'easy' ? 'Легко' : manual.difficult === 'medium' ? 'Средне' : 'Сложно' }}</span>
              </div>
              <div class="info-row">
                <span class="info-label"><i class="fa-regular fa-clock"></i> Время</span>
                <span class="info-val">{{ manual.time_estimate || '—' }}</span>
              </div>
              <div class="info-row">
                <span class="info-label"><i class="fa-solid fa-list-ol"></i> Шагов</span>
                <span class="info-val">{{ manual.steps.length }}</span>
              </div>
              <div class="info-row">
                <span class="info-label"><i class="fa-regular fa-calendar"></i> Обновлён</span>
                <span class="info-val">{{ formatDate(manual.updated_at) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.page-manual {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
  padding-bottom: var(--space-10);
}

/* ========================================== */
/* РЕЖИМ ПРОХОЖДЕНИЯ                          */
/* ========================================== */
.execution-header {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  background: linear-gradient(90deg, rgba(112, 0, 255, 0.15) 0%, rgba(20, 20, 25, 1) 100%);
  padding: var(--space-4);
  border-radius: var(--radius-lg);
  border: 1px solid rgba(112, 0, 255, 0.3);

  @include md-up {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}

.eh-left {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}
.eh-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--color-brand);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}
.eh-title {
  font-size: var(--text-lg);
  font-weight: var(--fw-bold);
}
.eh-subtitle {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.eh-progress {
  flex: 1;
  max-width: 400px;
  display: flex;
  align-items: center;
  gap: var(--space-3);
}
.eh-progress-bar {
  flex: 1;
  height: 8px;
  background: var(--color-surface-secondary);
  border-radius: var(--radius-full);
  overflow: hidden;
}
.eh-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #7000ff, #a855f7);
  border-radius: var(--radius-full);
  transition: width 0.3s ease;
}
.eh-progress-text {
  font-size: var(--text-sm);
  font-weight: var(--fw-bold);
  color: var(--color-brand);
}

.eh-actions {
  display: flex;
  gap: var(--space-2);
}

/* Сетка прохождения */
.execution-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);

  @include lg-up {
    grid-template-columns: 1fr 320px;
  }
}

/* Текущий шаг */
.current-step-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
}

.csc-header {
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-3);
  border-bottom: 1px solid var(--color-border);
}

.badge {
  display: inline-block;
  font-size: 11px;
  font-weight: var(--fw-bold);
  color: #a855f7;
  background: rgba(112, 0, 255, 0.15);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  text-transform: uppercase;
  margin-bottom: var(--space-2);
}

.csc-title {
  font-size: var(--text-2xl);
  font-weight: var(--fw-bold);
}

.csc-body {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);

  @include md-up {
    flex-direction: row;
    align-items: flex-start;
  }
}

.csc-text {
  flex: 1;
  font-size: var(--text-base);
  line-height: 1.6;
}

.csc-image {
  flex: 0 0 300px;

  img {
    width: 100%;
    border-radius: var(--radius-md);
    border: 1px solid var(--color-border);
  }
}

.step-alerts {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  margin-top: var(--space-4);
}

.alert-box {
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  padding: var(--space-3);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);

  &.info { background: var(--color-info-soft); color: var(--color-info-strong); }
  &.danger { background: var(--color-danger-soft); color: var(--color-danger-strong); }
}

.csc-actions {
  display: flex;
  justify-content: space-between;
  margin-top: var(--space-6);
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border);
}

/* Сайдбар прохождения */
.sidebar-widget {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
  position: sticky;
  top: 20px;
}

.sidebar-title {
  font-size: var(--text-base);
  font-weight: var(--fw-bold);
  margin-bottom: var(--space-3);
}

.sidebar-progress-info {
  display: flex;
  justify-content: space-between;
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-2);
}

.sidebar-progress-bar {
  height: 6px;
  background: var(--color-surface-secondary);
  border-radius: var(--radius-full);
  overflow: hidden;
  margin-bottom: var(--space-4);
}
.sidebar-progress-fill {
  height: 100%;
  background: var(--color-brand);
  border-radius: var(--radius-full);
}

.steps-nav-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.nav-step-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background 0.2s;

  &:hover {
    background: var(--color-surface-secondary);
  }

  &.is-active {
    background: rgba(112, 0, 255, 0.1);
    .nav-step-marker { background: var(--color-brand); color: #fff; border-color: var(--color-brand); }
    .nav-step-text { color: var(--color-brand); font-weight: var(--fw-medium); }
  }

  &.is-completed {
    .nav-step-marker { background: var(--color-success); color: #fff; border-color: var(--color-success); }
    .nav-step-text { color: var(--color-text-tertiary); text-decoration: line-through; }
  }
}

.nav-step-marker {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: var(--fw-bold);
  color: var(--color-text-secondary);
  flex-shrink: 0;
  transition: all 0.2s;
}

.nav-step-text {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  line-height: 1.3;
}

/* Аккордеон внизу */
.all-steps-section {
  margin-top: var(--space-6);
}

.accordion-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.accordion-item {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
  transition: all 0.2s;

  &.is-expanded {
    border-color: rgba(112, 0, 255, 0.4);
  }
}

.accordion-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  cursor: pointer;

  &:hover {
    background: var(--color-surface-secondary);
  }
}

.acc-num {
  width: 24px;
  height: 24px;
  background: var(--color-surface-secondary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: var(--fw-bold);
  color: var(--color-text-secondary);
}

.acc-title {
  flex: 1;
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
}

.acc-badge {
  font-size: 10px;
  font-weight: var(--fw-bold);
  color: var(--color-success);
  background: rgba(34, 197, 94, 0.15);
  padding: 2px 6px;
  border-radius: var(--radius-sm);
}

.acc-icon {
  color: var(--color-text-tertiary);
  transition: transform 0.2s;
}
.is-expanded .acc-icon {
  transform: rotate(180deg);
}

.accordion-body {
  padding: var(--space-4);
  border-top: 1px solid var(--color-border-light);
  background: var(--color-surface-secondary);
}

/* ========================================== */
/* РЕЖИМ ЧТЕНИЯ                               */
/* ========================================== */
.manual-header {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.header-actions {
  display: flex;
  justify-content: space-between;
  gap: 8px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  text-decoration: none;

  &:hover { color: var(--color-brand); }
}

.meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  color: var(--color-brand);
}

.manual-title {
  font-size: var(--text-3xl);
  font-weight: var(--fw-bold);
  line-height: var(--leading-tight);
}

.manual-desc {
  font-size: var(--text-lg);
  color: var(--color-text-secondary);
}

.start-execution-btn {
  margin-top: var(--space-2);
}

.read-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-6);

  @include lg-up {
    grid-template-columns: 1fr 300px;
  }
}

.read-main {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.section-title {
  font-size: var(--text-xl);
  font-weight: var(--fw-semibold);
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-4);

  i { color: var(--color-brand); }
}

/* Безопасность */
.safety-block {
  display: flex;
  background: var(--color-surface-secondary);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.safety-accent {
  width: 4px;
  background: var(--color-brand);
  flex-shrink: 0;
}

.safety-content {
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  flex: 1;
}

.safety-row {
  display: flex;
  gap: var(--space-3);
  align-items: flex-start;

  > i {
    font-size: 16px;
    margin-top: 2px;
    flex-shrink: 0;
  }

  .text-info { color: var(--color-brand); }
  .text-danger { color: var(--color-danger); }
  .text-success { color: var(--color-success); }
}

.safety-label {
  display: block;
  font-size: var(--text-xs);
  font-weight: var(--fw-semibold);
  text-transform: uppercase;
  color: var(--color-text-tertiary);
  margin-bottom: 4px;
}

.safety-text {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  line-height: 1.5;
}

/* Инструменты */
.tools-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);

  @include sm-up { grid-template-columns: 1fr 1fr; }
}
.tool-block {
  background: var(--color-surface-secondary);
  padding: var(--space-4);
  border-radius: var(--radius-md);

  h3 {
    font-size: var(--text-sm);
    font-weight: var(--fw-bold);
    margin-bottom: var(--space-2);
    color: var(--color-text-secondary);
    display: flex;
    align-items: center;
    gap: var(--space-2);
  }
  p { font-size: var(--text-base); }
}

/* Шаги (Чтение) */
.steps-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}
.step-card {
  display: flex;
  gap: var(--space-4);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-4);
}
.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(112, 0, 255, 0.15);
  color: var(--color-brand);
  font-weight: var(--fw-bold);
  flex-shrink: 0;
}
.step-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}
.step-title {
  font-size: var(--text-base);
  font-weight: var(--fw-semibold);
}
.step-image {
  max-width: 100%;
  border-radius: var(--radius-md);
  margin: var(--space-3) 0;
}
.step-alert {
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  margin-top: var(--space-2);

  &.tip { background: var(--color-info-soft); color: var(--color-info-strong); }
  &.warning { background: var(--color-danger-soft); color: var(--color-danger-strong); }
}

/* Сайдбар (Чтение) */
.read-sidebar {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}
.sidebar-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
}
.toc-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);

  li {
    display: flex;
    gap: var(--space-3);
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
  }
}
.toc-num {
  color: var(--color-brand);
  font-weight: var(--fw-bold);
}
.info-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}
.info-row {
  display: flex;
  justify-content: space-between;
  font-size: var(--text-sm);
}
.info-label {
  color: var(--color-text-secondary);
  display: flex;
  align-items: center;
  gap: var(--space-2);

  i { width: 16px; text-align: center; }
}
.info-val {
  font-weight: var(--fw-medium);
}

/* Таймлайн Содержания */
.timeline-list {
  display: flex;
  flex-direction: column;
  position: relative;
  padding-left: 8px; /* Отступ для линии */
}

.timeline-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) 0;
  position: relative;
  z-index: 1;
}

.timeline-marker {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  border: 2px solid var(--color-text-tertiary);
  background: var(--color-surface);
  flex-shrink: 0;
  margin-left: 4px;
  transition: all 0.2s;
}

.timeline-text {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  line-height: 1.4;
}

/* Активный (первый) шаг */
.timeline-item.is-current {
  .timeline-marker {
    background: var(--color-brand);
    border-color: var(--color-brand);
    box-shadow: 0 0 0 3px rgba(112, 0, 255, 0.2);
    width: 10px;
    height: 10px;
    margin-left: 3px;
  }

  .timeline-text {
    color: var(--color-text);
    font-weight: var(--fw-medium);
  }
}

/* Общие стили Markdown */
.markdown-body {
  line-height: var(--leading-relaxed);
  :deep(p) { margin: 0 0 var(--space-2); &:last-child { margin-bottom: 0; } }
  :deep(ul), :deep(ol) { padding-left: var(--space-5); margin-bottom: var(--space-2); }
  :deep(code) { padding: 2px 6px; border-radius: var(--radius-sm); background: var(--color-surface-secondary); font-family: var(--font-mono); font-size: 0.9em; }
  :deep(pre) { padding: var(--space-3); border-radius: var(--radius-md); background: var(--color-surface-secondary); overflow-x: auto; margin-bottom: var(--space-3); code { padding: 0; background: none; } }
}
</style>
