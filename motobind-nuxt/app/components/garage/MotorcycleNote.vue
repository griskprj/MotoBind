<script setup lang="ts">
import type { Motorcycle, ApiError } from '~/types'

const props = defineProps<{ motorcycle: Motorcycle }>()
const emit = defineEmits<{ updated: [] }>()

const api = useApi()
const toast = useToast()

const note = ref(props.motorcycle.note || '')
const saving = ref(false)

watch(() => props.motorcycle.note, (val) => {
  note.value = val || ''
})

async function onSave() {
  saving.value = true
  try {
    await api.motorcycle.updateNote(props.motorcycle.id, note.value.trim() || null)
    toast.success('Заметка сохранена')
    emit('updated')
  } catch (e) {
    toast.error((e as ApiError).message)
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <BaseCard padding="lg">
    <h2 class="section-title">Заметка</h2>
    <p class="section-desc">Личные записи, пароли от сигнализации, особенности эксплуатации.</p>

    <form @submit.prevent="onSave" class="note-form">
      <BaseTextarea
        v-model="note"
        placeholder="Например: масло менял 500 км назад, цепь подтянуть через 200 км..."
        :rows="4"
        :maxlength="128"
        autosize
      />
      <div class="form-actions">
        <BaseButton type="submit" variant="secondary" :loading="saving" :disabled="note === (motorcycle.note || '')">
          Сохранить
        </BaseButton>
      </div>
    </form>
  </BaseCard>
</template>

<style scoped lang="scss">
.section-title {
  font-size: var(--text-lg);
  font-weight: var(--fw-semibold);
  color: var(--color-text);
  margin-bottom: var(--space-1);
}

.section-desc {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-4);
}

.note-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}
</style>
