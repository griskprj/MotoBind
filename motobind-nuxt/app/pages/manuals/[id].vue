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
      <div class="manual-topline">
        <NuxtLink to="/manuals" class="back-link">
          <i class="fa-solid fa-arrow-left" aria-hidden="true" />
          Все мануалы
        </NuxtLink>
        <BaseButton
          v-if="manual.author_id === auth.user?.id || auth.isAdmin"
          :to="`/manuals/edit/${manual.id}`"
          variant="secondary"
          size="sm"
        >
          <template #icon><i class="fa-solid fa-pen" aria-hidden="true" /></template>
          Редактировать
        </BaseButton>
      </div>

      <header class="manual-hero">
        <div class="manual-hero__content">
          <div class="manual-meta">
            <BaseBadge variant="brand" size="sm">{{ manual.category }}</BaseBadge>
            <BaseBadge
              v-if="manual.difficult"
              :variant="manual.difficult === 'easy' ? 'success' : manual.difficult === 'medium' ? 'warning' : 'danger'"
              size="sm"
            >
              <i class="fa-solid fa-signal" aria-hidden="true" />
              {{ manual.difficult === 'easy' ? 'Лёгкая' : manual.difficult === 'medium' ? 'Средняя' : 'Высокая' }} сложность
            </BaseBadge>
            <span v-if="manual.time_estimate" class="hero-meta-item">
              <i class="fa-regular fa-clock" aria-hidden="true" /> {{ manual.time_estimate }}
            </span>
            <span v-if="manual.motorcycle" class="hero-meta-item">
              <i class="fa-solid fa-motorcycle" aria-hidden="true" /> {{ manual.motorcycle }}
            </span>
          </div>

          <h1 class="manual-title">{{ manual.title }}</h1>
          <div v-if="manual.description" class="manual-desc markdown-body" v-html="render(manual.description)" />
        </div>
      </header>

      <div class="read-layout">
        <main class="read-main">
          <section
            v-if="manual.safety_tip || manual.warnings || manual.conditions"
            id="preparation"
            class="content-section"
          >
            <div class="section-heading">
              <span class="section-heading__icon section-heading__icon--warning">
                <i class="fa-solid fa-shield-halved" aria-hidden="true" />
              </span>
              <div>
                <h2 class="section-title">Безопасность и подготовка</h2>
                <p class="section-caption">Перед началом работы проверь условия и предупреждения</p>
              </div>
            </div>

            <div class="safety-list">
              <div v-if="manual.safety_tip" class="safety-item safety-item--info">
                <i class="fa-solid fa-lightbulb" aria-hidden="true" />
                <div>
                  <span class="safety-label">Совет по безопасности</span>
                  <p>{{ manual.safety_tip }}</p>
                </div>
              </div>
              <div v-if="manual.warnings" class="safety-item safety-item--danger">
                <i class="fa-solid fa-triangle-exclamation" aria-hidden="true" />
                <div>
                  <span class="safety-label">Важные предупреждения</span>
                  <p>{{ manual.warnings }}</p>
                </div>
              </div>
              <div v-if="manual.conditions" class="safety-item safety-item--success">
                <i class="fa-solid fa-circle-check" aria-hidden="true" />
                <div>
                  <span class="safety-label">Условия выполнения</span>
                  <p>{{ manual.conditions }}</p>
                </div>
              </div>
            </div>
          </section>

          <section v-if="manual.instruments || manual.parts" id="equipment" class="content-section">
            <div class="section-heading">
              <span class="section-heading__icon">
                <i class="fa-solid fa-toolbox" aria-hidden="true" />
              </span>
              <div>
                <h2 class="section-title">Что понадобится</h2>
                <p class="section-caption">Подготовь инструменты и необходимые материалы заранее</p>
              </div>
            </div>
            <div class="tools-grid">
              <article v-if="manual.instruments" class="resource-card">
                <div class="resource-card__title">
                  <i class="fa-solid fa-screwdriver-wrench" aria-hidden="true" />
                  Инструменты
                </div>
                <p>{{ manual.instruments }}</p>
              </article>
              <article v-if="manual.parts" class="resource-card">
                <div class="resource-card__title">
                  <i class="fa-solid fa-box-open" aria-hidden="true" />
                  Материалы и запчасти
                </div>
                <p>{{ manual.parts }}</p>
              </article>
            </div>
          </section>

          <section v-if="manual.interval || manual.tip" class="content-section">
            <div class="section-heading">
              <span class="section-heading__icon">
                <i class="fa-solid fa-circle-info" aria-hidden="true" />
              </span>
              <div>
                <h2 class="section-title">Дополнительная информация</h2>
                <p class="section-caption">Полезные сведения перед выполнением процедуры</p>
              </div>
            </div>
            <div class="details-grid">
              <div v-if="manual.interval" class="detail-tile">
                <span class="detail-tile__label">Периодичность</span>
                <strong>{{ manual.interval }}</strong>
              </div>
              <div v-if="manual.tip" class="detail-tile detail-tile--tip">
                <i class="fa-solid fa-lightbulb" aria-hidden="true" />
                <p>{{ manual.tip }}</p>
              </div>
            </div>
          </section>

          <section id="steps" class="content-section">
            <div class="section-heading section-heading--between">
              <div class="section-heading__main">
                <span class="section-heading__icon">
                  <i class="fa-solid fa-list-ol" aria-hidden="true" />
                </span>
                <div>
                  <h2 class="section-title">Пошаговое выполнение</h2>
                  <p class="section-caption">Следуй этапам последовательно и не пропускай предупреждения</p>
                </div>
              </div>
              <BaseBadge variant="neutral">{{ manual.steps.length }} шагов</BaseBadge>
            </div>

            <div class="steps-list">
              <article v-for="step in manual.steps" :key="step.id" class="step-card">
                <div class="step-card__rail">
                  <span class="step-number">{{ step.order }}</span>
                  <span class="step-rail-line" />
                </div>
                <div class="step-content">
                  <h3 class="step-title">{{ step.title }}</h3>
                  <div v-if="step.text" class="step-text markdown-body" v-html="render(step.text)" />
                  <img
                    v-if="step.image"
                    :src="useMediaUrl()(step.image)!"
                    :alt="`Иллюстрация: ${step.title}`"
                    class="step-image"
                    loading="lazy"
                  />
                  <div v-if="step.result" class="step-result">
                    <i class="fa-solid fa-check-circle" aria-hidden="true" />
                    <div><strong>Результат этапа</strong><p>{{ step.result }}</p></div>
                  </div>
                  <div v-if="step.tip" class="step-alert tip">
                    <i class="fa-solid fa-lightbulb" aria-hidden="true" />
                    <span>{{ step.tip }}</span>
                  </div>
                  <div v-if="step.warning" class="step-alert warning">
                    <i class="fa-solid fa-triangle-exclamation" aria-hidden="true" />
                    <span>{{ step.warning }}</span>
                  </div>
                </div>
              </article>
            </div>
          </section>

          <section v-if="manual.specs && Object.keys(manual.specs).length" id="specs" class="content-section">
            <div class="section-heading">
              <span class="section-heading__icon">
                <i class="fa-solid fa-gauge-high" aria-hidden="true" />
              </span>
              <div>
                <h2 class="section-title">Технические параметры</h2>
                <p class="section-caption">Значения и спецификации, указанные в руководстве</p>
              </div>
            </div>
            <div class="specs-table">
              <div v-for="([key, value], index) in Object.entries(manual.specs)" :key="key" class="spec-row">
                <span>{{ key }}</span>
                <strong>{{ typeof value === 'object' ? JSON.stringify(value) : value }}</strong>
              </div>
            </div>
          </section>

          <section v-if="manual.aftercare" id="aftercare" class="content-section">
            <div class="section-heading">
              <span class="section-heading__icon section-heading__icon--success">
                <i class="fa-solid fa-flag-checkered" aria-hidden="true" />
              </span>
              <div>
                <h2 class="section-title">После завершения</h2>
                <p class="section-caption">Что проверить и сделать после выполнения работ</p>
              </div>
            </div>
            <div class="aftercare-card markdown-body" v-html="render(manual.aftercare)" />
          </section>

          <section v-if="manual.docs_links?.length" id="sources" class="content-section">
            <div class="section-heading">
              <span class="section-heading__icon">
                <i class="fa-solid fa-book-bookmark" aria-hidden="true" />
              </span>
              <div>
                <h2 class="section-title">Источники и документация</h2>
                <p class="section-caption">Материалы, использованные при подготовке мануала</p>
              </div>
            </div>
            <ul class="source-list">
              <li v-for="(url, index) in manual.docs_links" :key="url">
                <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true" />
                <a :href="url" target="_blank" rel="noopener noreferrer">Источник {{ index + 1 }}</a>
              </li>
            </ul>
          </section>
        </main>

        <aside class="read-sidebar">
          <div class="sidebar-card sidebar-card--sticky">
            <h3 class="sidebar-title">О мануале</h3>
            <div class="info-list">
              <div class="info-row">
                <span class="info-label"><i class="fa-solid fa-motorcycle" aria-hidden="true" /> Мотоцикл</span>
                <span class="info-val">{{ manual.motorcycle || 'Не указан' }}</span>
              </div>
              <div class="info-row">
                <span class="info-label"><i class="fa-solid fa-signal" aria-hidden="true" /> Сложность</span>
                <span class="info-val">{{ manual.difficult === 'easy' ? 'Лёгкая' : manual.difficult === 'medium' ? 'Средняя' : manual.difficult === 'hard' ? 'Высокая' : '—' }}</span>
              </div>
              <div class="info-row">
                <span class="info-label"><i class="fa-regular fa-clock" aria-hidden="true" /> Время</span>
                <span class="info-val">{{ manual.time_estimate || '—' }}</span>
              </div>
              <div class="info-row">
                <span class="info-label"><i class="fa-solid fa-list-ol" aria-hidden="true" /> Этапы</span>
                <span class="info-val">{{ manual.steps.length }}</span>
              </div>
              <div class="info-row">
                <span class="info-label"><i class="fa-regular fa-calendar" aria-hidden="true" /> Добавлен</span>
                <span class="info-val">{{ formatDate(manual.created_at) || '—' }}</span>
              </div>
            </div>
            <div class="sidebar-divider" />
            <h3 class="sidebar-title">В этом руководстве</h3>
            <nav class="toc-list" aria-label="Содержание мануала">
              <a v-if="manual.safety_tip || manual.warnings || manual.conditions" href="#preparation">
                <span>01</span> Безопасность и подготовка
              </a>
              <a v-if="manual.instruments || manual.parts" href="#equipment">
                <span>02</span> Инструменты и материалы
              </a>
              <a href="#steps"><span>03</span> Пошаговое выполнение</a>
              <a v-if="manual.specs && Object.keys(manual.specs).length" href="#specs">
                <span>04</span> Технические параметры
              </a>
              <a v-if="manual.aftercare" href="#aftercare"><span>05</span> После завершения</a>
              <a v-if="manual.docs_links?.length" href="#sources"><span>06</span> Источники
              </a>
            </nav>
            <BaseButton block size="lg" @click="startExecution">
              <template #icon><i class="fa-solid fa-play" aria-hidden="true" /></template>
              Начать выполнение
            </BaseButton>
          </div>
        </aside>
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

/* Обновлённый режим чтения */
.manual-topline {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
}
.manual-hero {
  position: relative;
  display: flex;
  align-items: center;
  min-height: 290px;
  padding: clamp(24px, 4vw, 48px);
  overflow: hidden;
  isolation: isolate;
  border: 1px solid color-mix(in srgb, var(--color-brand) 28%, var(--color-border));
  border-radius: var(--radius-xl);
  background: var(--color-surface);
}
.manual-hero__content { position: relative; z-index: 2; width: min(760px, 72%); }
.manual-meta { display: flex; align-items: center; flex-wrap: wrap; gap: var(--space-2); margin-bottom: var(--space-4); }
.hero-meta-item { display: inline-flex; align-items: center; gap: 7px; color: var(--color-text-secondary); font-size: var(--text-sm); }
.manual-title { max-width: 780px; margin: 0; color: var(--color-text); font-size: clamp(28px, 4vw, 42px); font-weight: var(--fw-bold); line-height: 1.12; letter-spacing: -.025em; }
.manual-desc { max-width: 700px; margin-top: var(--space-4); color: var(--color-text-secondary); font-size: var(--text-base); line-height: var(--leading-relaxed); }
.hero-hint { display: inline-flex; align-items: center; gap: var(--space-2); color: var(--color-text-tertiary); font-size: var(--text-sm); }
.read-layout { display: grid; grid-template-columns: minmax(0, 1fr) 300px; align-items: start; gap: var(--space-5); }
.read-main { display: flex; min-width: 0; flex-direction: column; gap: var(--space-6); }
.content-section { scroll-margin-top: 24px; }
.section-heading { display: flex; align-items: center; gap: var(--space-3); margin-bottom: var(--space-4); }
.section-heading--between { justify-content: space-between; }
.section-heading__main { display: flex; align-items: center; gap: var(--space-3); }
.section-heading__icon { display: grid; flex: 0 0 40px; width: 40px; height: 40px; place-items: center; border: 1px solid var(--color-border); border-radius: var(--radius-md); background: var(--color-surface); color: var(--color-brand); }
.section-heading__icon--warning { color: var(--color-warning-strong); background: var(--color-warning-soft); border-color: transparent; }
.section-heading__icon--success { color: var(--color-success-strong); background: var(--color-success-soft); border-color: transparent; }
.section-title { margin: 0; color: var(--color-text); font-size: var(--text-lg); font-weight: var(--fw-bold); }
.section-caption { margin: 3px 0 0; color: var(--color-text-tertiary); font-size: var(--text-xs); line-height: var(--leading-base); }
.safety-list { display: flex; flex-direction: column; gap: var(--space-2); }
.safety-item { display: flex; align-items: flex-start; gap: var(--space-3); padding: var(--space-4); border: 1px solid var(--color-border); border-radius: var(--radius-md); background: var(--color-surface); }
.safety-item > i { margin-top: 2px; }
.safety-item--info > i { color: var(--color-info); }
.safety-item--danger > i { color: var(--color-danger); }
.safety-item--success > i { color: var(--color-success); }
.safety-label { display: block; margin-bottom: 4px; color: var(--color-text); font-size: var(--text-sm); font-weight: var(--fw-semibold); }
.safety-item p, .resource-card p { margin: 0; color: var(--color-text-secondary); font-size: var(--text-sm); line-height: var(--leading-relaxed); }
.tools-grid, .details-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-3); }
.resource-card, .detail-tile { min-width: 0; padding: var(--space-4); border: 1px solid var(--color-border); border-radius: var(--radius-md); background: var(--color-surface); }
.resource-card__title { display: flex; align-items: center; gap: var(--space-2); margin-bottom: var(--space-2); color: var(--color-text); font-size: var(--text-sm); font-weight: var(--fw-semibold); }
.resource-card__title i { color: var(--color-brand); }
.detail-tile { display: flex; flex-direction: column; gap: var(--space-2); }
.detail-tile__label { color: var(--color-text-tertiary); font-size: var(--text-xs); }
.detail-tile strong { color: var(--color-text); font-size: var(--text-base); }
.detail-tile--tip { flex-direction: row; align-items: flex-start; grid-column: 1 / -1; background: var(--color-info-soft); border-color: transparent; }
.detail-tile--tip i { color: var(--color-info-strong); margin-top: 3px; }
.detail-tile--tip p { margin: 0; color: var(--color-info-strong); font-size: var(--text-sm); line-height: var(--leading-relaxed); }
.steps-list { display: flex; flex-direction: column; gap: var(--space-3); }
.step-card { display: flex; gap: var(--space-3); padding: var(--space-4); border: 1px solid var(--color-border); border-radius: var(--radius-lg); background: var(--color-surface); }
.step-card__rail { display: flex; flex: 0 0 34px; flex-direction: column; align-items: center; }
.step-number { display: grid; width: 32px; height: 32px; place-items: center; border: 1px solid color-mix(in srgb, var(--color-brand) 25%, var(--color-border)); border-radius: 50%; background: var(--color-brand-soft); color: var(--color-brand); font-size: var(--text-sm); font-weight: var(--fw-bold); }
.step-rail-line { width: 1px; flex: 1; min-height: 18px; margin-top: 8px; background: var(--color-border); }
.step-card:last-child .step-rail-line { display: none; }
.step-content { display: flex; min-width: 0; flex: 1; flex-direction: column; gap: var(--space-2); padding-top: 5px; }
.step-title { margin: 0; color: var(--color-text); font-size: var(--text-base); font-weight: var(--fw-semibold); }
.step-text { color: var(--color-text-secondary); font-size: var(--text-sm); line-height: var(--leading-relaxed); }
.step-image { display: block; max-width: min(100%, 680px); max-height: 440px; object-fit: contain; border: 1px solid var(--color-border); border-radius: var(--radius-md); margin-top: var(--space-2); }
.step-alert, .step-result { display: flex; align-items: flex-start; gap: var(--space-2); padding: var(--space-3); border-radius: var(--radius-md); font-size: var(--text-sm); line-height: var(--leading-relaxed); }
.step-alert.tip { background: var(--color-info-soft); color: var(--color-info-strong); }
.step-alert.warning { background: var(--color-danger-soft); color: var(--color-danger-strong); }
.step-result { background: var(--color-success-soft); color: var(--color-success-strong); }
.step-result > i { margin-top: 3px; }
.step-result p { margin: 3px 0 0; }
.specs-table { overflow: hidden; border: 1px solid var(--color-border); border-radius: var(--radius-md); background: var(--color-surface); }
.spec-row { display: flex; justify-content: space-between; gap: var(--space-4); padding: var(--space-3) var(--space-4); border-bottom: 1px solid var(--color-border-light); font-size: var(--text-sm); }
.spec-row:last-child { border-bottom: 0; }
.spec-row span { color: var(--color-text-secondary); }
.spec-row strong { color: var(--color-text); text-align: right; overflow-wrap: anywhere; }
.aftercare-card { padding: var(--space-4); border: 1px solid var(--color-border); border-radius: var(--radius-md); background: var(--color-surface); color: var(--color-text-secondary); }
.source-list { display: flex; flex-direction: column; gap: var(--space-2); margin: 0; padding: 0; list-style: none; }
.source-list li { display: flex; align-items: center; gap: var(--space-2); padding: var(--space-3); border: 1px solid var(--color-border); border-radius: var(--radius-md); background: var(--color-surface); font-size: var(--text-sm); }
.source-list i { color: var(--color-brand); }
.source-list a { color: var(--color-text); text-decoration: none; }
.source-list a:hover { color: var(--color-brand); }
.read-sidebar { min-width: 0; }
.sidebar-card { padding: var(--space-4); border: 1px solid var(--color-border); border-radius: var(--radius-lg); background: var(--color-surface); }
.sidebar-card--sticky { position: sticky; top: 24px; }
.sidebar-title { margin: 0 0 var(--space-3); color: var(--color-text); font-size: var(--text-base); font-weight: var(--fw-bold); }
.info-list { display: flex; flex-direction: column; gap: var(--space-3); }
.info-row { display: flex; justify-content: space-between; gap: var(--space-3); font-size: var(--text-xs); }
.info-label { display: inline-flex; align-items: center; gap: var(--space-2); color: var(--color-text-secondary); }
.info-label i { width: 14px; color: var(--color-text-tertiary); text-align: center; }
.info-val { max-width: 55%; color: var(--color-text); font-weight: var(--fw-semibold); text-align: right; overflow-wrap: anywhere; }
.sidebar-divider { height: 1px; margin: var(--space-4) 0; background: var(--color-border); }
.toc-list { display: flex; flex-direction: column; gap: 3px; margin-bottom: var(--space-4); }
.toc-list a { display: flex; align-items: flex-start; gap: var(--space-2); padding: var(--space-2); border-radius: var(--radius-sm); color: var(--color-text-secondary); font-size: var(--text-xs); line-height: 1.4; text-decoration: none; }
.toc-list a:hover { background: var(--color-surface-secondary); color: var(--color-brand); }
.toc-list a span { color: var(--color-brand); font-weight: var(--fw-bold); font-variant-numeric: tabular-nums; }
.markdown-body { color: inherit; }
.markdown-body :deep(p) { margin: 0 0 var(--space-2); }
.markdown-body :deep(p:last-child) { margin-bottom: 0; }
.markdown-body :deep(ul), .markdown-body :deep(ol) { padding-left: var(--space-5); margin: var(--space-2) 0; }
.markdown-body :deep(h2), .markdown-body :deep(h3) { margin: var(--space-3) 0 var(--space-2); color: var(--color-text); }
.markdown-body :deep(a) { color: var(--color-brand); }
@media (max-width: 1100px) {
  .read-layout { grid-template-columns: minmax(0, 1fr) 270px; }
  .manual-hero__visual { right: 2%; opacity: .7; }
}
@media (max-width: 900px) {
  .read-layout { grid-template-columns: 1fr; }
  .read-sidebar { order: -1; }
  .sidebar-card--sticky { position: static; }
  .toc-list { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 640px) {
  .manual-topline { align-items: flex-start; }
  .manual-hero { min-height: 0; padding: var(--space-4); }
  .manual-hero__content { width: 100%; }
  .manual-hero__visual { display: none; }
  .manual-title { font-size: var(--text-2xl); }
  .manual-desc { font-size: var(--text-sm); }
  .hero-actions { align-items: flex-start; flex-direction: column; gap: var(--space-2); }
  .tools-grid, .details-grid { grid-template-columns: 1fr; }
  .step-card { gap: var(--space-2); padding: var(--space-3); }
  .step-card__rail { flex-basis: 28px; }
  .step-number { width: 28px; height: 28px; }
  .toc-list { grid-template-columns: 1fr; }
  .spec-row { flex-direction: column; gap: 4px; }
  .spec-row strong { text-align: left; }
}

</style>
