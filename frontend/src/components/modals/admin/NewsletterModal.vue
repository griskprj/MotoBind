<template>
  <BaseModal
    :is-open="isOpen"
    title="Отправить рассылку"
    subtitle="Всем пользователям или выбранной группе"
    icon="envelope"
    variant="default"
    size="lg"
    @close="close"
  >
    <form @submit.prevent="submit" class="newsletter-form">
      <BaseInput
        v-model="form.subject"
        label="Тема письма"
        placeholder="Новое обновление MotoBind"
        required
      />

      <BaseSelect
        v-model="form.target"
        label="Целевая аудитория"
        required
      >
        <option value="all">Все пользователи</option>
        <option value="active">Только активные</option>
        <option value="admins">Только администраторы</option>
      </BaseSelect>

      <BaseTextarea
        v-model="form.content"
        label="Содержание письма"
        placeholder="Текст письма. Поддерживается HTML..."
        :rows="8"
        required
      />

      <div class="field">
        <label class="field-label">Предпросмотр</label>
        <div class="preview" v-html="form.content || 'Текст письма будет здесь...'"></div>
      </div>

      <div class="info-box">
        <i class="fa fa-info-circle"></i>
        <span>
          Рассылка будет отправлена асинхронно.
          Вы получите уведомление о завершении.
        </span>
      </div>
    </form>

    <template #actions>
      <div class="modal-actions">
        <BaseButton variant="secondary" block @click="close">
          Отмена
        </BaseButton>
        <BaseButton
          variant="primary"
          icon="fa fa-paper-plane"
          block
          :disabled="!isValid"
          :loading="loading"
          @click="submit"
        >
          Отправить
        </BaseButton>
      </div>
    </template>
  </BaseModal>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { BaseModal, BaseButton, BaseInput, BaseSelect, BaseTextarea } from '@/components/ui'
import { useToast } from '@/composables/useToast'
import api from '@/api/api'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
})

const emit = defineEmits(['close', 'sent'])
const toast = useToast()

const loading = ref(false)

const form = reactive({
  subject: '',
  content: '',
  target: 'all',
})

const isValid = computed(() => form.subject.trim() && form.content.trim())

watch(
  () => props.isOpen,
  (val) => {
    if (!val) resetForm()
  }
)

function resetForm() {
  form.subject = ''
  form.content = ''
  form.target = 'all'
  loading.value = false
}

function close() {
  emit('close')
}

async function submit() {
  if (!isValid.value || loading.value) return
  loading.value = true
  try {
    await api.post('/admin/send-newsletter', form)
    emit('sent')
    toast.success('Рассылка запущена!')
    close()
  } catch (err) {
    console.error('Failed to send newsletter:', err)
    toast.error(err.response?.data?.error || 'Ошибка отправки')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.newsletter-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.field-label {
  font-size: 13px;
  font-weight: var(--fw-semibold);
  color: var(--text-secondary);
  display: block;
}

.preview {
  padding: 12px 16px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-light);
  min-height: 60px;
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.preview:empty::before {
  content: 'Текст письма будет здесь...';
  color: var(--text-muted);
  font-style: italic;
}

.info-box {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: var(--radius-md);
  background: var(--accent-trans);
  color: var(--text-secondary);
  font-size: 13px;
}

.info-box i {
  color: var(--accent-text);
  font-size: 18px;
  flex-shrink: 0;
}

.modal-actions {
  display: flex;
  gap: 10px;
  width: 100%;
}

.modal-actions > * {
  flex: 1;
}

@media (max-width: 640px) {
  .modal-actions {
    flex-direction: column;
  }
}
</style>
