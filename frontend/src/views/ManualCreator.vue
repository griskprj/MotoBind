<template>
    <div class="container">
        <LoadingOverlay :isLoading="isSubmitting" text="Создание мануала..."/>

        <!-- === HEADER === -->
        <Header
            title="Конструктор мануалов"
            subtitle="Создание подробной инструкции по ремонту и обслуживанию"
        />

        <!-- === FORM === -->
        <section class="form-section">
            <div class="info-banner">
                <i class="fa fa-info-circle"></i>
                <span>Правила оформления мануалов <a href='/manual/rules' target='_blank'>здесь</a>.</span>
            </div>

            <form @submit.prevent="submitManual" enctype="multipart/form-data">
                <!-- ===== БЛОК 1: О МАНУАЛЕ ===== -->
                <div class="form-card">
                    <div class="form-card-header">
                        <i class="fa fa-info-circle"></i>
                        <h3>1. О мануале</h3>
                    </div>

                    <div class="form-card-body">
                        <div class="form-group">
                            <label>
                                Категория / Система*
                                <select v-model="form.category" @change="onCategoryChange" required>
                                    <option value="">Выберите категорию</option>
                                    <option value="engine">⚙️ Двигатель</option>
                                    <option value="drive">🔗 Привод</option>
                                    <option value="steering">🔄 Рулевое управление</option>
                                    <option value="suspension">🛞 Подвеска</option>
                                    <option value="electronics">💡 Электроника</option>
                                    <option value="wheel">⚡ Колеса/Шины</option>
                                    <option value="brakes">🛑 Тормозная система</option>
                                    <option value="fuel">⛽ Топливная система</option>
                                    <option value="cooling">❄️ Система охлаждения</option>
                                </select>
                            </label>
                        </div>

                        <div class="form-group">
                            <label>
                                Название процедуры*

                                <!-- Выпадающий список шаблонов -->
                                <select
                                    v-if="!form.customTitle && form.category"
                                    v-model="form.templateId"
                                    @change="onTemplateChange"
                                    :class="{ 'error': errors.title }"
                                >
                                    <option value="">Выберите процедуру</option>
                                    <option
                                        v-for="tpl in availableTemplates"
                                        :key="tpl.id"
                                        :value="tpl.id"
                                    >
                                        {{ tpl.label }}
                                    </option>
                                    <option value="__custom__">✏️ Своё название...</option>
                                </select>

                                <!-- Если категория не выбрана — подсказка -->
                                <div v-else-if="!form.customTitle" class="field-placeholder">
                                    Сначала выберите категорию
                                </div>

                                <!-- Ручной ввод (если выбрано "Своё название" или категория не выбрана) -->
                                <div v-if="form.customTitle || !form.category" class="custom-title-wrapper">
                                    <input
                                        type="text"
                                        v-model="form.title"
                                        placeholder="Введите своё название процедуры"
                                        :class="{ 'error': errors.title }"
                                        maxLength="200"
                                    >
                                    <button
                                        v-if="form.customTitle && form.category"
                                        type="button"
                                        class="btn-back-to-templates"
                                        @click="backToTemplates"
                                        title="Вернуться к списку"
                                    >
                                        <i class="fa fa-list"></i>
                                    </button>
                                </div>

                                <span v-if="errors.title" class="error-message">{{ errors.title }}</span>
                            </label>
                        </div>

                        <div class="form-group">
                            <label>
                                Краткое описание*
                                <textarea
                                    v-model="form.description"
                                    required
                                    rows="2"
                                    placeholder="Краткое описание процедуры, её важность и интервалы"
                                    :class="{ 'error': errors.description }"
                                    maxLength="1000"
                                ></textarea>
                                <span v-if="errors.description" class="error-message">{{ errors.description }}</span>
                            </label>
                        </div>

                        <div class="form-row">
                            <div class="form-group">
                                <label>
                                    Модель мотоцикла*
                                    <input
                                        type="text"
                                        v-model="form.motorcycle"
                                        required
                                        placeholder="Например: BMW S1000RR (2018+)"
                                        :class="{ 'error': errors.motorcycle }"
                                        maxLength="100"
                                    >
                                    <span v-if="errors.motorcycle" class="error-message">{{ errors.motorcycle }}</span>
                                </label>
                            </div>

                            <div class="form-group">
                                <label>
                                    Сложность*
                                    <select v-model="form.difficult" required>
                                        <option value="">Выберите сложность</option>
                                        <option value="easy">Легко</option>
                                        <option value="medium">Средне</option>
                                        <option value="hard">Сложно</option>
                                    </select>
                                </label>
                            </div>
                        </div>

                        <div class="form-row">
                            <div class="form-group">
                                <label>
                                    Ориентировочное время
                                    <input
                                        type="text"
                                        v-model="form.time_estimate"
                                        placeholder="Например: 15–20 минут"
                                        maxLength="64"
                                    >
                                </label>
                            </div>

                            <div class="form-group">
                                <label>
                                    Периодичность
                                    <input
                                        type="text"
                                        v-model="form.interval"
                                        placeholder="Например: каждые 10 000 км или раз в год"
                                        maxLength="64"
                                    >
                                </label>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- ===== БЛОК 2: БЕЗОПАСНОСТЬ И ПОДГОТОВКА ===== -->
                <div class="form-card">
                    <div class="form-card-header">
                        <i class="fa fa-shield"></i>
                        <h3>2. Безопасность и подготовка</h3>
                    </div>

                    <div class="form-card-body">
                        <div class="form-group">
                            <label>
                                Общие рекомендации
                                <textarea
                                    v-model="form.safety_tip"
                                    rows="2"
                                    placeholder="Общие рекомендации по выполнению процедуры"
                                    maxLength="1000"
                                ></textarea>
                            </label>
                        </div>

                        <div class="form-group">
                            <label>
                                ⚠️ Предупреждения (что категорически нельзя делать)
                                <textarea
                                    v-model="form.warnings"
                                    rows="2"
                                    placeholder="Например: Не запускайте двигатель без масла"
                                    maxLength="1000"
                                ></textarea>
                            </label>
                        </div>

                        <div class="form-group">
                            <label>
                                Необходимые условия
                                <textarea
                                    v-model="form.conditions"
                                    rows="2"
                                    placeholder="Например: Двигатель холодный, мотоцикл на центральной подставке"
                                    maxLength="1000"
                                ></textarea>
                            </label>
                        </div>
                    </div>
                </div>

                <!-- ===== БЛОК 3: ИНСТРУМЕНТЫ И МАТЕРИАЛЫ ===== -->
                <div class="form-card">
                    <div class="form-card-header">
                        <i class="fa fa-wrench"></i>
                        <h3>3. Инструменты и материалы</h3>
                    </div>

                    <div class="form-card-body">
                        <div class="form-group">
                            <label>
                                Инструменты
                                <input
                                    type="text"
                                    v-model="form.instruments"
                                    placeholder="Ключ на 18мм, ветошь, динамометрический ключ, ёмкость для слива"
                                    maxLength="500"
                                >
                            </label>
                        </div>

                        <div class="form-group">
                            <label>
                                Материалы и запчасти
                                <input
                                    type="text"
                                    v-model="form.parts"
                                    placeholder="Масло моторное 10W-40 (3.2L), масляный фильтр, уплотнительное кольцо"
                                    maxLength="500"
                                >
                            </label>
                        </div>
                    </div>
                </div>

                <!-- ===== БЛОК 4: ССЫЛКИ НА ДОКУМЕНТАЦИЮ ===== -->
                <div class="form-card">
                    <div class="form-card-header">
                        <i class="fa fa-link"></i>
                        <h3>4. Ссылки на официальную документацию</h3>
                    </div>

                    <div class="form-card-body">
                        <div class="form-group">
                            <label>
                                Ссылки на документацию
                                <div class="links-list">
                                    <div
                                        v-for="(link, index) in form.docs_links"
                                        :key="index"
                                        class="link-item"
                                    >
                                        <input
                                            type="url"
                                            v-model="form.docs_links[index]"
                                            placeholder="https://example.com/manual.pdf"
                                            class="link-input"
                                        >
                                        <button
                                            type="button"
                                            class="btn-remove-link"
                                            @click="removeLink(index)"
                                        >
                                            <i class="fa fa-times"></i>
                                        </button>
                                    </div>
                                </div>
                                <button type="button" class="btn-add-link" @click="addLink">
                                    <i class="fa fa-plus"></i> Добавить ссылку
                                </button>
                            </label>
                        </div>
                    </div>
                </div>

                <!-- ===== БЛОК 5: ТЕХНИЧЕСКИЕ ДАННЫЕ ===== -->
                <div class="form-card">
                    <div class="form-card-header">
                        <i class="fa fa-table"></i>
                        <h3>5. Технические данные</h3>
                    </div>

                    <div class="form-card-body">
                        <div class="form-group">
                            <label>
                                Моменты затяжки (JSON)
                                <textarea
                                    v-model="form.specs_json"
                                    rows="6"
                                    placeholder='{
  "torque": [
    {"name": "Болт сливной пробки", "nm": 25, "note": "сухой"},
    {"name": "Болт крепления фильтра", "nm": 12, "note": "сухой"}
  ],
  "fluids": {
    "oil": "3.2L (с фильтром)",
    "coolant": "1.5L"
  },
  "tolerances": {
    "chain": "2-5 мм"
  }
}'
                                    class="code-input"
                                ></textarea>
                                <span class="field-hint">Введите данные в формате JSON</span>
                            </label>
                        </div>

                        <div class="form-group">
                            <label>Быстрый редактор моментов затяжки</label>
                            <div class="torque-editor">
                                <div
                                    v-for="(item, index) in torqueItems"
                                    :key="index"
                                    class="torque-row"
                                >
                                    <input
                                        v-model="item.name"
                                        placeholder="Название болта"
                                        class="torque-name"
                                    >
                                    <input
                                        v-model="item.nm"
                                        placeholder="Н·м"
                                        type="number"
                                        class="torque-nm"
                                    >
                                    <input
                                        v-model="item.note"
                                        placeholder="Примечание"
                                        class="torque-note"
                                    >
                                    <button
                                        type="button"
                                        class="btn-remove-torque"
                                        @click="removeTorqueItem(index)"
                                    >
                                        <i class="fa fa-times"></i>
                                    </button>
                                </div>
                                <button type="button" class="btn-add-torque" @click="addTorqueItem">
                                    <i class="fa fa-plus"></i> Добавить момент затяжки
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- ===== БЛОК 6: ШАГИ ===== -->
                <div class="form-card">
                    <div class="form-card-header">
                        <i class="fa fa-list-ol"></i>
                        <h3>6. Шаги инструкции</h3>
                        <span class="steps-count">{{ form.steps.length }} шаг(ов)</span>
                    </div>

                    <div class="form-card-body">
                        <div v-if="form.steps.length === 0" class="empty-state">
                            <i class="fa fa-hand-pointer"></i>
                            <p>Нажмите "Добавить шаг", чтобы создать инструкцию</p>
                        </div>

                        <div v-for="(step, index) in form.steps" :key="step.localId" class="step-card">
                            <div class="step-header">
                                <span class="step-number">Шаг {{ index + 1 }}</span>
                                <button type="button" class="btn-remove-step" @click="removeStep(index)">
                                    <i class="fa fa-times"></i>
                                </button>
                            </div>

                            <div class="step-content">
                                <div class="form-group">
                                    <label>
                                        Заголовок шага*
                                        <input
                                            type="text"
                                            v-model="step.title"
                                            required
                                            :placeholder="`Что нужно сделать на шаге ${index + 1}?`"
                                            :class="{ 'error': step.errors && step.errors.title }"
                                            maxLength="200"
                                        >
                                        <span v-if="step.errors && step.errors.title" class="error-message">{{ step.errors.title }}</span>
                                    </label>
                                </div>

                                <div class="form-group">
                                    <label>
                                        Описание шага
                                        <textarea
                                            v-model="step.text"
                                            rows="3"
                                            :placeholder="`Подробное описание шага ${index + 1}`"
                                            maxLength="5000"
                                        ></textarea>
                                    </label>
                                </div>

                                <div class="form-row">
                                    <div class="form-group">
                                        <label>
                                            ⚠️ Предупреждение
                                            <input
                                                type="text"
                                                v-model="step.warning"
                                                placeholder="Чего нельзя делать на этом шаге"
                                                maxLength="256"
                                            >
                                        </label>
                                    </div>

                                    <div class="form-group">
                                        <label>
                                            💡 Совет
                                            <input
                                                type="text"
                                                v-model="step.tip"
                                                placeholder="Лайфхак или рекомендация"
                                                maxLength="256"
                                            >
                                        </label>
                                    </div>
                                </div>

                                <div class="form-group">
                                    <label>
                                        🎯 Результат шага
                                        <input
                                            type="text"
                                            v-model="step.result"
                                            placeholder="Как понять, что шаг выполнен правильно"
                                            maxLength="500"
                                        >
                                    </label>
                                </div>

                                <div class="form-group">
                                    <label>
                                        📷 Изображение шага
                                        <div class="image-upload" @click="$refs['fileInput' + index].click()">
                                            <input
                                                :ref="'fileInput' + index"
                                                type="file"
                                                accept="image/*"
                                                @change="handleImageUpload(index, $event)"
                                                class="file-input"
                                            >
                                            <span class="file-name" v-if="step.imageFile">
                                                {{ step.imageFile.name }}
                                            </span>
                                            <span class="file-name" v-else-if="step.imagePreview && !step.imageFile">
                                                Изображение загружено
                                            </span>
                                            <span class="file-name" v-else>Выберите файл</span>
                                            <button
                                                v-if="step.imageFile || (isEditMode && step.existingImage)"
                                                type="button"
                                                class="btn-remove-image"
                                                @click.stop="removeImage(index)"
                                            >
                                                <i class="fa fa-times"></i>
                                            </button>
                                        </div>
                                        <div v-if="step.imagePreview" class="image-preview">
                                            <img :src="step.imagePreview" :alt="step.title" />
                                        </div>
                                    </label>
                                </div>
                            </div>
                        </div>

                        <button type="button" class="btn-add-step" @click="addStep">
                            <i class="fa fa-plus"></i> Добавить шаг
                        </button>
                    </div>
                </div>

                <!-- ===== БЛОК 7: ПОСЛЕ ЗАВЕРШЕНИЯ ===== -->
                <div class="form-card">
                    <div class="form-card-header">
                        <i class="fa fa-check-circle"></i>
                        <h3>7. После завершения</h3>
                    </div>

                    <div class="form-card-body">
                        <div class="form-group">
                            <label>
                                Финальная проверка
                                <textarea
                                    v-model="form.aftercare"
                                    rows="3"
                                    placeholder="Что проверить после работы: уровень масла, отсутствие течей, затяжку болтов..."
                                    maxLength="2000"
                                ></textarea>
                            </label>
                        </div>
                    </div>
                </div>

                <!-- Кнопки отправки -->
                <div class="form-actions">
                    <button type="button" class="btn btn-secondary" @click="resetForm">Отменить</button>
                    <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
                        <i v-if="isSubmitting" class="fa fa-spinner fa-spin"></i>
                        <span v-else>
                            <i class="fa fa-check"></i>
                            {{ isEditMode ? 'Сохранить изменения' : 'Создать мануал' }}
                        </span>
                    </button>
                </div>
            </form>
        </section>
    </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useManualsStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import { getTemplatesByCategory } from '@/constants/maintenanceTemplates'
import { getManualImageUrl } from '@/utils/mediaUrl'

import Header from '../components/Header.vue'
import LoadingOverlay from '../components/LoadingOverlay.vue'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const manualsStore = useManualsStore()

// ===== Local state =====
const isSubmitting = ref(false)
const errors = ref({})
const stepIdCounter = ref(0)
const editingManualId = ref(null)
const isEditMode = ref(false)

const form = reactive({
  title: '',
  customTitle: false,
  description: '',
  motorcycle: '',
  difficult: '',
  time_estimate: '',
  interval: '',
  category: '',
  templateId: '',
  safety_tip: '',
  warnings: '',
  conditions: '',
  instruments: '',
  parts: '',
  docs_links: [],
  specs: {},
  specs_json: '',
  steps: [],
  aftercare: '',
  tip: '',
})

const torqueItems = ref([])

// ===== Computed =====
const availableTemplates = computed(() => {
  if (!form.category) return []
  return getTemplatesByCategory(form.category)
})

// ===== Watchers =====
watch(
  torqueItems,
  (newVal) => {
    if (newVal.length > 0) {
      const torque = newVal
        .filter((item) => item.name || item.nm)
        .map((item) => ({
          name: item.name || 'Болт',
          nm: item.nm ? Number(item.nm) : 0,
          note: item.note || '',
        }))
      updateSpecs('torque', torque)
    }
  },
  { deep: true }
)

watch(
  () => form.specs_json,
  (newVal) => {
    try {
      if (newVal && newVal.trim()) {
        form.specs = JSON.parse(newVal)
      }
    } catch {
      // ignore parse errors
    }
  },
  { deep: true }
)

// ===== Lifecycle =====
onMounted(() => {
  const editId = route.query.edit
  if (editId) {
    loadManualForEdit(editId)
  } else {
    addStep()
  }
})

// ===== Category / Template =====
function onCategoryChange() {
  form.templateId = ''
  form.title = ''
  form.customTitle = false
}

function onTemplateChange() {
  if (form.templateId === '__custom__') {
    form.customTitle = true
    form.title = ''
    return
  }

  const tpl = availableTemplates.value.find((t) => t.id === form.templateId)
  form.title = tpl ? tpl.label : ''
}

function backToTemplates() {
  form.customTitle = false
  form.templateId = ''
  form.title = ''
}

// ===== Steps =====
function addStep() {
  form.steps.push({
    id: null,
    localId: ++stepIdCounter.value,
    title: '',
    text: '',
    warning: '',
    tip: '',
    result: '',
    imageFile: null,
    imagePreview: null,
    errors: {},
  })
}

function removeStep(index) {
  if (form.steps.length <= 1) {
    toast.warning('Мануал должен содержать хотя бы один шаг')
    return
  }
  form.steps.splice(index, 1)
}

async function handleImageUpload(index, event) {
  const file = event.target.files[0]
  if (!file) return

  if (file.size > 5 * 1024 * 1024) {
    toast.error('Размер файла не должен превышать 5MB')
    event.target.value = ''
    return
  }

  if (!file.type.startsWith('image/')) {
    toast.error('Пожалуйста, загрузите изображение')
    event.target.value = ''
    return
  }

  const step = form.steps[index]
  if (isEditMode.value && step.id) {
    try {
      const imageUrl = await manualsStore.uploadStepImage(
        editingManualId.value,
        step.id,
        file
      )
      step.existingImage = imageUrl
      step.imagePreview = getManualImageUrl(imageUrl)
      step.imageFile = null
      toast.success('Изображение загружено')
    } catch (err) {
      console.error('Failed to upload step image:', err)
      toast.error('Не удалось загрузить изображение')
    } finally {
      event.target.value = ''
    }
  } else {
    step.imageFile = file
    const reader = new FileReader()
    reader.onload = (e) => {
      step.imagePreview = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

async function removeImage(index) {
  const step = form.steps[index]
  if (isEditMode.value && step.id && step.existingImage) {
    try {
      await manualsStore.deleteStepImage(editingManualId.value, step.id)
      step.existingImage = null
      step.imagePreview = null
      toast.success('Изображение удалено')
    } catch (err) {
      console.error('Failed to delete step image:', err)
      toast.error('Не удалось удалить изображение')
    }
  } else {
    step.imageFile = null
    step.imagePreview = null
    const input = document.querySelectorAll('.step-card input[type="file"]')[index]
    if (input) input.value = ''
  }
}

// ===== Docs / Specs =====
function addLink() {
  form.docs_links.push('')
}

function removeLink(index) {
  form.docs_links.splice(index, 1)
}

function updateSpecs(key, value) {
  if (!form.specs) form.specs = {}
  form.specs[key] = value
  form.specs_json = JSON.stringify(form.specs, null, 2)
}

function addTorqueItem() {
  torqueItems.value.push({ name: '', nm: '', note: '' })
}

function removeTorqueItem(index) {
  torqueItems.value.splice(index, 1)
}

// ===== Validation =====
function validateForm() {
  errors.value = {}
  let isValid = true

  if (!form.title || form.title.trim().length < 3) {
    errors.value.title = 'Название должно содержать минимум 3 символа'
    isValid = false
  }

  if (!form.description || form.description.trim().length < 10) {
    errors.value.description = 'Описание должно содержать минимум 10 символов'
    isValid = false
  }

  if (!form.motorcycle || form.motorcycle.trim().length < 2) {
    errors.value.motorcycle = 'Укажите модель мотоцикла'
    isValid = false
  }

  if (!form.difficult) {
    errors.value.difficult = 'Выберите сложность'
    isValid = false
  }

  form.steps.forEach((step) => {
    step.errors = {}
    if (!step.title || step.title.trim().length < 2) {
      step.errors.title = 'Заголовок шага обязателен'
      isValid = false
    }
  })

  if (form.steps.length === 0) {
    isValid = false
  }

  return isValid
}

// ===== Payload =====
function buildPayload() {
  return {
    title: form.title.trim(),
    description: form.description.trim(),
    category: form.category || 'general',
    difficult: form.difficult,
    motorcycle: form.motorcycle.trim(),
    time_estimate: form.time_estimate.trim() || null,
    interval: form.interval.trim() || null,
    safety_tip: form.safety_tip.trim() || null,
    warnings: form.warnings.trim() || null,
    conditions: form.conditions.trim() || null,
    docs_links: form.docs_links.filter((link) => link.trim()),
    specs: form.specs || null,
    aftercare: form.aftercare.trim() || null,
    instruments: form.instruments.trim() || null,
    parts: form.parts.trim() || null,
    tip: form.tip.trim() || null,
    steps: form.steps.map((step, index) => ({
      order: index + 1,
      title: step.title.trim(),
      text: step.text.trim() || null,
      warning: step.warning.trim() || null,
      tip: step.tip.trim() || null,
      result: step.result.trim() || null,
    })),
  }
}

// ===== Submit =====
async function submitManual() {
  if (!validateForm()) {
    toast.warning('Проверьте заполненные поля')
    const firstError = document.querySelector('.error')
    if (firstError) {
      firstError.scrollIntoView({ behavior: 'smooth', block: 'center' })
      firstError.focus()
    }
    return
  }

  isSubmitting.value = true

  try {
    if (isEditMode.value) {
      await manualsStore.update(editingManualId.value, buildPayload())
      toast.success('Мануал обновлён и отправлен на повторную проверку')
      router.push(`/manual/${editingManualId.value}`)
    } else {
      const files = {}
      form.steps.forEach((step, index) => {
        if (step.imageFile) {
          files[`image_${index + 1}`] = step.imageFile
        }
      })

      const created = await manualsStore.create(buildPayload(), files)
      toast.success('Мануал успешно создан')
      resetForm()
      router.push(`/manual/${created.id}`)
    }
  } catch (err) {
    console.error('Failed to save manual:', err)
    const message =
      err.response?.data?.message ||
      err.response?.data?.error ||
      'Произошла ошибка'
    toast.error(message)
  } finally {
    isSubmitting.value = false
  }
}

// ===== Load for edit =====
async function loadManualForEdit(id) {
  try {
    const manual = await manualsStore.loadOne(id)
    editingManualId.value = id
    isEditMode.value = true

    form.title = manual.title || ''
    form.description = manual.description || ''
    form.motorcycle = manual.motorcycle || ''
    form.difficult = manual.difficult || ''
    form.time_estimate = manual.time_estimate || ''
    form.interval = manual.interval || ''
    form.category = manual.category || ''
    form.safety_tip = manual.safety_tip || ''
    form.warnings = manual.warnings || ''
    form.conditions = manual.conditions || ''
    form.instruments = manual.instruments || ''
    form.parts = manual.parts || ''
    form.docs_links = manual.docs_links || []
    form.aftercare = manual.aftercare || ''
    form.tip = manual.tip || ''

    if (manual.specs) {
      form.specs = manual.specs
      form.specs_json = JSON.stringify(manual.specs, null, 2)
      if (manual.specs.torque) {
        torqueItems.value = manual.specs.torque.map((item) => ({ ...item }))
      }
    }

    form.steps = manual.steps.map((step, index) => ({
      id: step.id,
      localId: ++stepIdCounter.value,
      order: step.order || index + 1,
      title: step.title || '',
      text: step.text || '',
      warning: step.warning || '',
      tip: step.tip || '',
      result: step.result || '',
      imageFile: null,
      imagePreview: step.image ? getManualImageUrl(step.image) : null,
      existingImage: step.image || null,
      errors: {},
    }))

    if (form.category && manual.title) {
      const templates = getTemplatesByCategory(form.category)
      const match = templates.find(
        (t) => t.label.toLowerCase() === manual.title.toLowerCase()
      )

      if (match) {
        form.templateId = match.id
        form.customTitle = false
        form.title = match.label
      } else {
        form.customTitle = true
        form.title = manual.title
      }
    } else {
      form.customTitle = true
      form.title = manual.title || ''
    }

    if (form.steps.length === 0) addStep()
  } catch (err) {
    console.error('Failed to load manual for edit:', err)
    toast.error('Не удалось загрузить мануал для редактирования')
    router.push('/manuals')
  }
}

// ===== Reset =====
function resetForm() {
  Object.assign(form, {
    title: '',
    customTitle: false,
    description: '',
    motorcycle: '',
    difficult: '',
    time_estimate: '',
    interval: '',
    category: '',
    templateId: '',
    safety_tip: '',
    warnings: '',
    conditions: '',
    instruments: '',
    parts: '',
    docs_links: [],
    specs: {},
    specs_json: '',
    steps: [],
    aftercare: '',
    tip: '',
  })
  errors.value = {}
  stepIdCounter.value = 0
  torqueItems.value = []
  editingManualId.value = null
  isEditMode.value = false
  addStep()
}
</script>

<style scoped>
/* ===== FORM SECTION ===== */
.form-section {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.info-banner {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 16px;
    background: var(--accent-trans);
    border: 1px solid var(--accent-light);
    border-radius: 10px;
    color: var(--text-secondary);
    font-size: 14px;
}

.info-banner a {
    color: var(--accent-text);
    text-decoration: underline;
}

/* ===== FORM CARD ===== */
.form-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 16px;
}

.form-card-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 20px;
    border-bottom: 1px solid var(--border-color);
    background: var(--bg-secondary);
}

.form-card-header i {
    font-size: 18px;
    color: var(--accent);
}

.form-card-header h3 {
    font-size: 16px;
    font-weight: 600;
    margin: 0;
    color: var(--text-primary);
}

.steps-count {
    margin-left: auto;
    font-size: 13px;
    color: var(--text-secondary);
    background: var(--bg-secondary);
    padding: 2px 12px;
    border-radius: 20px;
    border: 1px solid var(--border-color);
}

.form-card-body {
    padding: 20px;
}

/* ===== FORM ELEMENTS ===== */
.form-group {
    margin-bottom: 16px;
}

.form-group:last-child {
    margin-bottom: 0;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}

.form-group label {
    display: block;
    font-weight: 500;
    color: var(--text-secondary);
    margin-bottom: 6px;
    font-size: 14px;
}

.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 10px 14px;
    font-size: 14px;
    font-family: inherit;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: 10px;
    color: var(--text-primary);
    transition: all 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-trans);
}

.form-group input::placeholder,
.form-group textarea::placeholder {
    color: var(--text-muted);
}

.form-group input.error,
.form-group textarea.error {
    border-color: var(--danger);
}

.form-group input.error:focus,
.form-group textarea.error:focus {
    box-shadow: 0 0 0 3px var(--danger-trans);
}

.form-group textarea {
    resize: vertical;
    min-height: 60px;
}

.code-input {
    font-family: 'Courier New', monospace;
    font-size: 13px !important;
}

.error-message {
    display: block;
    color: var(--danger);
    font-size: 13px;
    margin-top: 4px;
}

.field-hint {
    display: block;
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 4px;
}

/* ===== LINKS ===== */
.links-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 8px;
}

.link-item {
    display: flex;
    gap: 8px;
    align-items: center;
}

.link-input {
    flex: 1;
    padding: 8px 12px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: 8px;
    color: var(--text-primary);
    font-size: 14px;
}

.btn-remove-link {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 6px;
    transition: all 0.2s;
}

.btn-remove-link:hover {
    background: var(--danger-trans);
    color: var(--danger);
}

.btn-add-link {
    padding: 6px 14px;
    font-size: 13px;
    background: transparent;
    border: 1px dashed var(--accent-trans);
    border-radius: 8px;
    color: var(--accent-text);
    cursor: pointer;
    transition: all 0.2s;
}

.btn-add-link:hover {
    background: var(--accent-trans);
}

.custom-title-wrapper {
    display: flex;
    gap: 8px;
    align-items: center;
}

.custom-title-wrapper input {
    flex: 1;
}

.btn-back-to-templates {
    flex-shrink: 0;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    padding: 0;
    background: var(--bg-secondary);
    border: 1px solid var(--border-input);
    border-radius: 10px;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s;
    font-size: 14px;
}

.btn-back-to-templates:hover {
    background: var(--accent-trans);
    border-color: var(--accent);
    color: var(--accent-text);
}

.field-placeholder {
    padding: 10px 14px;
    background: var(--bg-secondary);
    border: 1px dashed var(--border-input);
    border-radius: 10px;
    font-size: 14px;
    color: var(--text-muted);
    font-style: italic;
}

/* ===== TORQUE EDITOR ===== */
.torque-editor {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.torque-row {
    display: grid;
    grid-template-columns: 2fr 1fr 2fr auto;
    gap: 8px;
    align-items: center;
}

.torque-name,
.torque-note {
    padding: 6px 10px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: 6px;
    color: var(--text-primary);
    font-size: 13px;
}

.torque-nm {
    padding: 6px 10px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: 6px;
    color: var(--text-primary);
    font-size: 13px;
    width: 80px;
}

.btn-remove-torque {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 6px;
}

.btn-remove-torque:hover {
    background: var(--danger-trans);
    color: var(--danger);
}

.btn-add-torque {
    padding: 6px 14px;
    font-size: 13px;
    background: transparent;
    border: 1px dashed var(--accent-trans);
    border-radius: 8px;
    color: var(--accent-text);
    cursor: pointer;
    transition: all 0.2s;
    margin-top: 4px;
}

.btn-add-torque:hover {
    background: var(--accent-trans);
}

/* ===== STEPS ===== */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px;
    background: var(--bg-secondary);
    border-radius: 12px;
    border: 2px dashed var(--border-color);
    text-align: center;
    margin-bottom: 16px;
}

.empty-state i {
    font-size: 32px;
    color: var(--accent);
    margin-bottom: 12px;
}

.empty-state p {
    font-size: 16px;
    color: var(--text-secondary);
    margin: 0;
}

.step-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    transition: border-color 0.2s;
}

.step-card:hover {
    border-color: var(--accent-trans);
}

.step-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}

.step-number {
    font-weight: 600;
    font-size: 14px;
    color: var(--accent-text);
    background: var(--accent-trans);
    padding: 2px 14px;
    border-radius: 20px;
}

.btn-remove-step {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 6px;
    transition: all 0.2s;
    font-size: 16px;
}

.btn-remove-step:hover {
    background: var(--danger-trans);
    color: var(--danger);
}

.step-content .form-group {
    margin-bottom: 12px;
}

.step-content .form-group:last-child {
    margin-bottom: 0;
}

/* ===== IMAGE UPLOAD ===== */
.image-upload {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    background: var(--bg-input);
    border: 1px dashed var(--border-input);
    border-radius: 8px;
    cursor: pointer;
    transition: border-color 0.2s;
}

.image-upload:hover {
    border-color: var(--accent);
}

.file-input {
    display: none;
}

.file-name {
    flex: 1;
    font-size: 13px;
    color: var(--text-muted);
}

.btn-remove-image {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 6px;
}

.btn-remove-image:hover {
    background: var(--danger-trans);
    color: var(--danger);
}

.image-preview {
    margin-top: 8px;
    border-radius: 8px;
    overflow: hidden;
    max-width: 300px;
}

.image-preview img {
    width: 100%;
    height: auto;
    max-height: 200px;
    object-fit: cover;
    border-radius: 8px;
    border: 1px solid var(--border-color);
}

/* ===== BUTTONS ===== */
.btn-add-step {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 500;
    border-radius: 10px;
    border: 1px dashed var(--accent-trans);
    background: transparent;
    color: var(--accent-text);
    cursor: pointer;
    transition: all 0.2s;
    width: 100%;
    justify-content: center;
}

.btn-add-step:hover {
    background: var(--accent-trans);
    border-color: var(--accent);
}

.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 10px 24px;
    font-size: 14px;
    font-weight: 500;
    border-radius: 10px;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.btn-primary {
    background: var(--accent);
    color: #fff;
}

.btn-primary:hover:not(:disabled) {
    background: var(--accent-hover);
    transform: translateY(-2px);
}

.btn-secondary {
    background: transparent;
    color: var(--text-secondary);
    border: 1px solid var(--border-input);
}

.btn-secondary:hover:not(:disabled) {
    background: var(--border-color);
}

/* ===== FORM ACTIONS ===== */
.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    padding-top: 20px;
    border-top: 1px solid var(--border-color);
}

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
    .form-row {
        grid-template-columns: 1fr;
        gap: 0;
    }

    .torque-row {
        grid-template-columns: 1fr;
        gap: 4px;
    }

    .torque-nm {
        width: 100%;
    }

    .form-card-header {
        flex-wrap: wrap;
    }

    .steps-count {
        margin-left: 0;
        width: 100%;
    }

    .form-actions {
        flex-direction: column-reverse;
    }

    .form-actions .btn {
        width: 100%;
        justify-content: center;
    }

    .step-card {
        padding: 12px;
    }

    .image-preview {
        max-width: 100%;
    }
}

@media (max-width: 480px) {
    .form-card-body {
        padding: 16px;
    }

    .empty-state {
        padding: 24px;
    }

    .empty-state i {
        font-size: 24px;
    }

    .empty-state p {
        font-size: 14px;
    }

    .link-item {
        flex-direction: column;
    }

    .btn-remove-link {
        align-self: flex-end;
    }
}

.fa-spin {
    animation: fa-spin 1s linear infinite;
}

@keyframes fa-spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>
