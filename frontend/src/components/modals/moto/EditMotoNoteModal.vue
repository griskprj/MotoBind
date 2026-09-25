<template>
  <BaseModal
    :is-open="isOpen"
    title="Редактирование заметок"
    subtitle="Добавьте важную информацию о мотоцикле"
    icon="file"
    variant="default"
    size="md"
    @close="$emit('close')"
  >
    <div class="form-stack">
      <BaseTextarea
        v-model="note"
        label="Заметки"
        placeholder="Введите заметки о мотоцикле..."
        :maxlength="512"
        :rows="5"
        :show-counter="true"
      />

      <div class="modal-info-block info">
        <div class="modal-info-icon">
          <i class="fa fa-lightbulb"></i>
        </div>
        <p class="modal-info-text">
          Здесь можно хранить любую полезную информацию: особенности модели,
          выполненные доработки, личные наблюдения, планы по обслуживанию и другое.
        </p>
      </div>
    </div>

    <template #actions>
      <BaseButton variant="secondary" block @click="$emit('close')">
        Отменить
      </BaseButton>
      <BaseButton
        variant="primary"
        icon="fa fa-save"
        block
        :loading="loading"
        @click="submit"
      >
        Сохранить
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, watch } from 'vue'
import { BaseModal, BaseButton, BaseTextarea } from '@/components/ui'
import { useToast } from '@/composables/useToast'
import { useMotorcyclesStore } from '@/stores'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  motorcycle: { type: Object, default: null },
})

const emit = defineEmits(['close'])
const toast = useToast()
const motorcyclesStore = useMotorcyclesStore()

const note = ref('')
const loading = ref(false)

watch(
  () => props.isOpen,
  (newVal) => {
    if (newVal && props.motorcycle) {
      note.value = props.motorcycle.note || ''
      loading.value = false
    }
  }
)

watch(
  () => props.motorcycle,
  (newVal) => {
    if (props.isOpen && newVal) note.value = newVal.note || ''
  },
  { deep: true }
)

async function submit() {
  loading.value = true
  try {
    await motorcyclesStore.updateNote(props.motorcycle.id, note.value)
    emit('close')
    toast.success('Заметка обновлена')
  } catch (err) {
    console.error('Failed to update note:', err)
    toast.error(err.response?.data?.error || 'Ошибка обновления заметки')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.form-stack {
  display: flex;
  flex-direction: column;
  gap: 14px;
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

@media (max-width: 640px) {
  .modal-info-block {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  .modal-info-icon {
    margin-top: 0;
  }
}
</style>
