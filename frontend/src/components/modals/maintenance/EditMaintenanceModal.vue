<template>
  <BaseModal
    :is-open="isOpen"
    title="Редактирование обслуживания"
    subtitle="Измените данные о обслуживании"
    icon="wrench"
    variant="default"
    size="md"
    @close="$emit('close')"
  >
    <form @submit.prevent="submit" class="edit-form">
      <BaseSelect
        v-model="form.motorcycleId"
        label="Мотоцикл"
        placeholder="Выберите мотоцикл"
        required
      >
        <option
          v-for="moto in motorcycles"
          :key="moto.id"
          :value="moto.id"
        >
          {{ moto.name }} ({{ moto.mileage || 0 }} км)
        </option>
      </BaseSelect>

      <BaseSelect
        v-model="form.category"
        label="Узел / Система"
        placeholder="Выберите категорию"
        required
        @change="onCategoryChange"
      >
        <option value="engine">Двигатель</option>
        <option value="drive">Привод</option>
        <option value="steering">Рулевое управление</option>
        <option value="suspension">Подвеска</option>
        <option value="electronics">Электроника</option>
        <option value="wheel">Колёса / Шины</option>
        <option value="brakes">Тормозная система</option>
        <option value="fuel">Топливная система</option>
        <option value="cooling">Система охлаждения</option>
        <option value="other">Другое</option>
      </BaseSelect>

      <BaseSelect
        v-if="templates.length > 0"
        v-model="form.templateId"
        label="Тип обслуживания"
        placeholder="Выберите тип обслуживания"
        required
        @change="onTemplateChange"
      >
        <option v-for="tpl in templates" :key="tpl.id" :value="tpl.id">
          {{ tpl.label }}
        </option>
      </BaseSelect>

      <BaseInput
        v-if="!form.category || templates.length === 0 || form.category === 'other'"
        v-model="form.title"
        label="Название обслуживания"
        placeholder="Например: Замена масла"
        required
      />

      <BaseTextarea
        v-model="form.description"
        label="Описание работы"
        placeholder="Подробное описание работы"
        :rows="2"
      />

      <hr class="form-divider" />

      <div class="form-row">
        <BaseInput
          v-model.number="form.planned_mileage"
          type="number"
          label="Плановый пробег (км)"
          placeholder="15000"
          :min="0"
        />
        <BaseInput
          v-model="form.planned_date"
          type="date"
          label="Плановая дата"
        />
      </div>

      <div class="form-row">
        <BaseInput
          v-model.number="form.completed_mileage"
          type="number"
          label="Выполненный пробег (км)"
          placeholder="15000"
          :min="0"
        />
        <BaseInput
          v-model="form.completed_date"
          type="date"
          label="Дата выполнения"
        />
      </div>

      <BaseInput
        v-model.number="form.cost"
        type="number"
        label="Стоимость (₽)"
        placeholder="5000"
        :min="0"
      />

      <div class="modal-info-block info">
        <div class="modal-info-icon">
          <i class="fa fa-info-circle"></i>
        </div>
        <p class="modal-info-text">
          Если заполнены выполненные поля, статус изменится на «Выполнено».
          Если заполнены плановые поля — статус будет «Запланировано».
        </p>
      </div>

      <div class="modal-actions">
        <BaseButton variant="secondary" block type="button" @click="$emit('close')">
          Отмена
        </BaseButton>
        <BaseButton
          variant="primary"
          icon="fa fa-save"
          block
          type="submit"
          :disabled="!isFormValid"
          :loading="isSubmitting"
        >
          Сохранить
        </BaseButton>
      </div>
    </form>
  </BaseModal>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import {
  BaseModal,
  BaseButton,
  BaseInput,
  BaseSelect,
  BaseTextarea,
} from '@/components/ui'
import { useToast } from '@/composables/useToast'
import { useMaintenancesStore } from '@/stores'
import { getTemplatesByCategory } from '@/constants/maintenanceTemplates'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  maintenance: { type: Object, default: null },
  motorcycles: { type: Array, default: () => [] },
})

const emit = defineEmits(['close'])
const toast = useToast()
const maintenancesStore = useMaintenancesStore()

const form = reactive({
  motorcycleId: null,
  category: '',
  templateId: '',
  title: '',
  description: '',
  planned_mileage: null,
  planned_date: null,
  completed_mileage: null,
  completed_date: null,
  cost: null,
})

const templates = ref([])
const isSubmitting = ref(false)

const isFormValid = computed(() => {
  return (
    form.motorcycleId &&
    form.category &&
    form.title &&
    form.title.trim().length > 0
  )
})

watch(
  () => props.maintenance,
  (val) => {
    if (val) fillForm(val)
  },
  { immediate: true }
)

watch(
  () => form.category,
  (newVal) => {
    if (newVal) {
      templates.value = getTemplatesByCategory(newVal)
      if (form.templateId) {
        const found = templates.value.find((t) => t.id === form.templateId)
        if (!found) form.templateId = ''
      }
    } else {
      templates.value = []
    }
  }
)

function fillForm(maintenance) {
  form.motorcycleId = maintenance.moto_id || maintenance.motorcycle_id || null
  form.category = maintenance.category || ''
  form.templateId = ''
  form.title = maintenance.title || ''
  form.description = maintenance.description || ''
  form.planned_mileage = maintenance.planned_mileage || null
  form.planned_date = maintenance.planned_date || null
  form.completed_mileage = maintenance.completed_mileage || null
  form.completed_date = maintenance.completed_date || null
  form.cost = maintenance.cost || null

  if (form.category) {
    templates.value = getTemplatesByCategory(form.category)
    const found = templates.value.find((t) => t.label === form.title)
    if (found) form.templateId = found.id
  }
}

function onCategoryChange() {
  form.templateId = ''
  templates.value = form.category ? getTemplatesByCategory(form.category) : []
}

function onTemplateChange() {
  const found = templates.value.find((t) => t.id === form.templateId)
  if (found) form.title = found.label
}

async function submit() {
  if (!isFormValid.value) {
    toast.warning('Заполните все обязательные поля')
    return
  }

  if (form.completed_mileage && !form.completed_date) {
    toast.error('Укажите дату выполнения')
    return
  }

  isSubmitting.value = true
  try {
    const payload = {
      maintenanceId: props.maintenance.id,
      motorcycleId: form.motorcycleId,
      category: form.category,
      title: form.title.trim(),
      description: form.description?.trim() || null,
      planned_mileage: form.planned_mileage || null,
      planned_date: form.planned_date || null,
      completed_mileage: form.completed_mileage || null,
      completed_date: form.completed_date || null,
      cost: form.cost || null,
    }

    await maintenancesStore.update(props.maintenance.id, payload)

    emit('close')
    toast.success('Обслуживание обновлено')
  } catch (err) {
    console.error('Failed to update maintenance:', err)
    toast.error(err.response?.data?.message || 'Ошибка при обновлении')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.edit-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.form-divider {
  border: none;
  border-top: 1px solid var(--border-light);
  margin: 4px 0;
}

.modal-info-block {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 10px;
}

.modal-info-block.info {
  background: var(--accent-trans);
  border: 1px solid var(--accent-light);
}

.modal-info-icon {
  font-size: 18px;
  color: var(--accent-text);
  flex-shrink: 0;
  margin-top: 2px;
}

.modal-info-text {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
}

.modal-actions {
  display: flex;
  gap: 10px;
  margin-top: 4px;
}

.modal-actions > * {
  flex: 1;
}

@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .modal-info-block {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .modal-info-icon {
    margin-top: 0;
  }

  .modal-actions {
    flex-direction: column;
  }
}
</style>
