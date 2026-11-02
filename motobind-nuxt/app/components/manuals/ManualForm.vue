<script setup lang="ts">
import type { CreateManualPayload, UpdateManualPayload, Manual, ManualStepPayload } from '~/types'

const props = defineProps<{
  initialData?: Manual | null
}>()

const emit = defineEmits<{
  success: [manual: Manual]
  cancel: []
}>()

const api = useApi()
const toast = useToast()
const { errors, setFromApiError, clear } = useFormErrors()

const isEditMode = computed(() => !!props.initialData)
const submitting = ref(false)

const form = reactive({
  title: '',
  description: '',
  category: 'engine',
  difficult: 'easy' as 'easy' | 'medium' | 'hard',
  motorcycle: '',
  time_estimate: '',
  interval: '',
  safety_tip: '',
  warnings: '',
  conditions: '',
  instruments: '',
  parts: '',
  docs_links: [] as string[],
  aftercare: '',
  tip: '',
})

const steps = ref<ManualStepPayload[]>([])
const stepImages = ref<(File | null)[]>([])
const existingImages = ref<(string | null)[]>([])
const deletedImageOrders = ref<Set<number>>(new Set())

function initForm() {
  clear()
  if (props.initialData) {
    const d = props.initialData
    form.title = d.title || ''
    form.description = d.description || ''
    form.category = d.category || 'engine'
    form.difficult = (d.difficult as any) || 'easy'
    form.motorcycle = d.motorcycle || ''
    form.time_estimate = d.time_estimate || ''
    form.interval = d.interval || ''
    form.safety_tip = d.safety_tip || ''
    form.warnings = d.warnings || ''
    form.conditions = d.conditions || ''
    form.instruments = d.instruments || ''
    form.parts = d.parts || ''
    form.docs_links = d.docs_links ? [...d.docs_links] : []
    form.aftercare = d.aftercare || ''
    form.tip = d.tip || ''

    steps.value = d.steps.map(s => ({
      order: s.order,
      title: s.title,
      text: s.text || '',
      tip: s.tip || '',
      warning: s.warning || '',
      result: s.result || '',
    }))
    stepImages.value = new Array(steps.value.length).fill(null)
    existingImages.value = d.steps.map(s => s.image || null)
    deletedImageOrders.value = new Set()
  } else {
    form.title = ''
    form.description = ''
    form.category = 'engine'
    form.difficult = 'easy'
    form.motorcycle = ''
    form.time_estimate = ''
    form.interval = ''
    form.safety_tip = ''
    form.warnings = ''
    form.conditions = ''
    form.instruments = ''
    form.parts = ''
    form.docs_links = []
    form.aftercare = ''
    form.tip = ''
    steps.value = [{ order: 1, title: '', text: '' }]
    stepImages.value = [null]
    existingImages.value = [null]
  }
}

watch(() => props.initialData, initForm, { immediate: true })

function addStep() {
  steps.value.push({ order: steps.value.length + 1, title: '', text: '' })
  stepImages.value.push(null)
  existingImages.value.push(null)
}

function removeStep(index: number) {
  steps.value.splice(index, 1)
  stepImages.value.splice(index, 1)
  existingImages.value.splice(index, 1)
  steps.value.forEach((s, i) => s.order = i + 1)
}

const newLink = ref('')
function addLink() {
  if (newLink.value.trim()) {
    form.docs_links.push(newLink.value.trim())
    newLink.value = ''
  }
}
function removeLink(index: number) {
  form.docs_links.splice(index, 1)
}

function onRemoveStepImage(index: number) {
  const step = steps.value[index]
  if (step) {
    deletedImageOrders.value.add(step.order)
    existingImages.value[index] = null
  }
}

async function onSubmit() {
  submitting.value = true
  clear()

  try {
    if (!form.title.trim()) throw new Error('Введите название')
    if (steps.value.length === 0) throw new Error('Добавьте хотя бы один шаг')
    if (steps.value.some(s => !s.title.trim())) throw new Error('Заполните заголовки всех шагов')

    if (isEditMode.value && props.initialData) {
      const payload: UpdateManualPayload = {
        ...form,
        steps: steps.value,
      }
      if (!payload.description) delete payload.description
      if (!payload.time_estimate) delete payload.time_estimate
      if (!payload.interval) delete payload.interval
      if (!payload.safety_tip) delete payload.safety_tip
      if (!payload.warnings) delete payload.warnings
      if (!payload.conditions) delete payload.conditions
      if (!payload.instruments) delete payload.instruments
      if (!payload.parts) delete payload.parts
      if (!payload.aftercare) delete payload.aftercare
      if (!payload.tip) delete payload.tip
      if (payload.docs_links && payload.docs_links.length === 0) delete payload.docs_links

      const updated = await api.manuals.update(props.initialData.id, payload)

      if (deletedImageOrders.value.size > 0) {
        const updatedSteps = updated.steps || []
        for (const order of deletedImageOrders.value) {
          const updatedStep = updatedSteps.find(s => s.order === order)
          if (updatedStep) {
            await api.manuals.deleteStepImage(updated.id, updatedStep.id)
          }
        }
      }

      if (stepImages.value.some(f => f !== null)) {
        const updatedSteps = updated.steps || []

        for (let i = 0; i < steps.value.length; i++) {
          const file = stepImages.value[i]
          if (file) {
            const stepOrder = steps.value[i]?.order

            const updatedStep = updatedSteps.find(s => s.order === stepOrder)
            if (updatedStep) {
              await api.manuals.uploadStepImage(updated.id, updatedStep.id, file)
            }
          }
        }
      }

      toast.success('Мануал обновлён')
      emit('success', updated)
    } else {
      const payload: CreateManualPayload = {
        ...form,
        steps: steps.value,
      }
      const newManual = await api.manuals.create(payload, stepImages.value)
      toast.success('Мануал отправлен на модерацию')
      emit('success', newManual)
    }
  } catch (e: any) {
    if (e.fieldErrors) setFromApiError(e)
    else toast.error(e.message || 'Ошибка сохранения')
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <form @submit.prevent="onSubmit" class="manual-form">
    <!-- Основная информация -->
    <BaseCard padding="lg">
      <h2 class="section-title">Основная информация</h2>
      <div class="form-grid">
        <BaseInput v-model="form.title" label="Название" required class="span-2" :error="errors.title" />
        <BaseInput v-model="form.motorcycle" label="Мотоцикл" placeholder="Например: Bajaj Pulsar NS 125" required :error="errors.motorcycle" />

        <BaseSelect v-model="form.category" label="Категория" :options="[
          { value: 'engine', label: 'Двигатель' },
          { value: 'drive', label: 'Трансмиссия' },
          { value: 'brakes', label: 'Тормоза' },
          { value: 'wheel', label: 'Колеса' },
          { value: 'suspension', label: 'Подвеска' },
          { value: 'electronics', label: 'Электрика' },
          { value: 'other', label: 'Прочее' },
        ]" :error="errors.category" />

        <BaseSelect v-model="form.difficult" label="Сложность" :options="[
          { value: 'easy', label: 'Легко' },
          { value: 'medium', label: 'Средне' },
          { value: 'hard', label: 'Сложно' },
        ]" :error="errors.difficult" />

        <BaseInput v-model="form.time_estimate" label="Время выполнения" placeholder="Например: 30 мин" :error="errors.time_estimate" />
        <BaseInput v-model="form.interval" label="Периодичность" placeholder="Например: каждые 5000 км" :error="errors.interval" />

        <div class="span-2">
          <label class="field-label">Описание</label>
          <MarkdownEditor v-model="form.description" placeholder="Краткое описание мануала..." />
        </div>
      </div>
    </BaseCard>

    <!-- Безопасность -->
    <BaseCard padding="lg">
      <h2 class="section-title">Безопасность и подготовка</h2>
      <div class="form-grid">
        <BaseInput v-model="form.safety_tip" label="Совет по безопасности" class="span-2" :error="errors.safety_tip" />
        <BaseInput v-model="form.warnings" label="Предупреждения" class="span-2" :error="errors.warnings" />
        <BaseInput v-model="form.conditions" label="Условия выполнения" class="span-2" :error="errors.conditions" />
      </div>
    </BaseCard>

    <!-- Инструменты и материалы -->
    <BaseCard padding="lg">
      <h2 class="section-title">Инструменты и материалы</h2>
      <div class="form-grid">
        <BaseInput v-model="form.instruments" label="Инструменты" placeholder="Ключ на 17, отвёртка..." :error="errors.instruments" />
        <BaseInput v-model="form.parts" label="Запчасти и материалы" placeholder="Масло, фильтр..." :error="errors.parts" />
      </div>
    </BaseCard>

    <!-- Ссылки -->
    <BaseCard padding="lg">
      <h2 class="section-title">Ссылки на документацию</h2>
      <div class="docs-list">
        <div v-for="(link, i) in form.docs_links" :key="i" class="doc-item">
          <span>{{ link }}</span>
          <BaseButton variant="danger" size="sm" icon-only @click="removeLink(i)">
            <i class="fa-solid fa-trash"></i>
          </BaseButton>
        </div>
        <div class="doc-add">
          <BaseInput v-model="newLink" placeholder="https://..." @keydown.enter.prevent="addLink" />
          <BaseButton variant="secondary" @click="addLink">Добавить</BaseButton>
        </div>
      </div>
    </BaseCard>

    <!-- Шаги -->
    <div class="steps-section">
      <div class="steps-header">
        <h2 class="section-title">Шаги выполнения</h2>
        <BaseButton variant="secondary" @click="addStep">
          <template #icon><i class="fa-solid fa-plus"></i></template>
          Добавить шаг
        </BaseButton>
      </div>

      <div class="steps-list">
        <ManualStepForm
          v-for="(step, i) in steps"
          :key="i"
          :index="i"
          v-model="steps[i]"
          v-model:image-file="stepImages[i]"
          :existing-image="existingImages[i]"
          :is-edit-mode="isEditMode"
          :step-id="initialData?.steps?.[i]?.id || null"
          @remove="removeStep(i)"
          @remove-image="onRemoveStepImage(i)"
        />
      </div>
    </div>

    <!-- После завершения -->
    <BaseCard padding="lg">
      <h2 class="section-title">После завершения</h2>
      <div class="form-grid">
        <div class="span-2">
          <label class="field-label">Рекомендации после работы</label>
          <MarkdownEditor v-model="form.aftercare" placeholder="Что проверить после завершения..." />
        </div>
        <BaseInput v-model="form.tip" label="Общий совет" class="span-2" :error="errors.tip" />
      </div>
    </BaseCard>

    <div class="form-actions">
      <BaseButton type="button" variant="secondary" @click="emit('cancel')">Отмена</BaseButton>
      <BaseButton type="submit" variant="primary" :loading="submitting">
        {{ isEditMode ? 'Сохранить изменения' : 'Отправить на модерацию' }}
      </BaseButton>
    </div>
  </form>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.manual-form { display: flex; flex-direction: column; gap: var(--space-6); }

.section-title {
  font-size: var(--text-lg);
  font-weight: var(--fw-semibold);
  margin-bottom: var(--space-4);
  color: var(--color-text);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);
  @include sm-up { grid-template-columns: 1fr 1fr; }
}
.span-2 { @include sm-up { grid-column: span 2; } }

.field-label {
  display: block;
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  color: var(--color-text);
  margin-bottom: var(--space-1);
}

.docs-list { display: flex; flex-direction: column; gap: var(--space-2); }
.doc-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-2);
  background: var(--color-surface-secondary);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
}
.doc-add { display: flex; gap: var(--space-2); align-items: flex-end; }

.steps-section { display: flex; flex-direction: column; gap: var(--space-4); }
.steps-header { display: flex; justify-content: space-between; align-items: center; }
.steps-list { display: flex; flex-direction: column; gap: var(--space-4); }

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-3);
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border);
}
</style>
