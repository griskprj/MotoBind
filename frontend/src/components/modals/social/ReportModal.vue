<template>
  <BaseModal
    :is-open="isOpen"
    title="Жалоба на пост"
    subtitle="Выберите причину жалобы. Модератор рассмотрит её в ближайшее время."
    icon="flag"
    variant="danger"
    size="md"
    @close="close"
  >
    <div class="category-list">
      <label
        v-for="cat in categories"
        :key="cat.value"
        class="category-item"
        :class="{ selected: category === cat.value }"
      >
        <input type="radio" :value="cat.value" v-model="category" />
        <div class="category-icon">
          <i :class="cat.icon"></i>
        </div>
        <div class="category-info">
          <span class="category-title">{{ cat.label }}</span>
          <span class="category-desc">{{ cat.description }}</span>
        </div>
      </label>
    </div>

    <div class="form-field">
      <label class="form-label">
        Комментарий <span class="form-label-muted">(необязательно)</span>
      </label>
      <textarea
        v-model="description"
        rows="3"
        maxlength="500"
        class="form-textarea"
        placeholder="Опишите подробнее, что нарушает правила..."
      ></textarea>
      <span class="char-count">{{ description.length }}/500</span>
    </div>

    <template #actions>
      <BaseButton
        variant="secondary"
        block
        :disabled="submitting"
        @click="close"
      >
        Отмена
      </BaseButton>
      <BaseButton
        variant="danger"
        icon="fa fa-flag"
        block
        :disabled="!category"
        :loading="submitting"
        @click="submit"
      >
        Отправить жалобу
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, watch } from 'vue'
import { BaseModal, BaseButton } from '@/components/ui'
import { useToast } from '@/composables/useToast'
import socialApi from '@/api/social'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  post: { type: Object, default: null },
})

const emit = defineEmits(['close', 'reported'])
const toast = useToast()

const category = ref('')
const description = ref('')
const submitting = ref(false)

const categories = [
  {
    value: 'sexual_content',
    label: 'Контент сексуального характера',
    icon: 'fa fa-exclamation-triangle',
    description: 'Порнография, откровенные материалы',
  },
  {
    value: 'hate_speech',
    label: 'Разжигание межнациональной розни',
    icon: 'fa fa-users',
    description: 'Оскорбления по национальному признаку',
  },
  {
    value: 'extremism',
    label: 'Экстремистская символика',
    icon: 'fa fa-ban',
    description: 'Запрещённая символика и материалы',
  },
  {
    value: 'violence',
    label: 'Насилие и жестокость',
    icon: 'fa fa-fist-raised',
    description: 'Сцены насилия, угрозы',
  },
  {
    value: 'drugs',
    label: 'Пропаганда наркотиков',
    icon: 'fa fa-pills',
    description: 'Упоминание и пропаганда запрещённых веществ',
  },
  {
    value: 'spam',
    label: 'Спам и мошенничество',
    icon: 'fa fa-bullhorn',
    description: 'Реклама, обман',
  },
  {
    value: 'other',
    label: 'Другое',
    icon: 'fa fa-ellipsis-h',
    description: 'Иные нарушения',
  },
]

watch(
  () => props.isOpen,
  (newVal) => {
    if (!newVal) {
      category.value = ''
      description.value = ''
      submitting.value = false
    }
  }
)

function close() {
  if (submitting.value) return
  emit('close')
}

async function submit() {
  if (!category.value || submitting.value || !props.post) return

  submitting.value = true
  try {
    await socialApi.reportPost(props.post.id, {
      category: category.value,
      description: description.value.trim() || null,
    })
    emit('reported')
    emit('close')
    toast.success('Жалоба отправлена. Спасибо!')
  } catch (err) {
    console.error('Failed to submit report:', err)
    toast.error(err.response?.data?.error || 'Не удалось отправить жалобу')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.category-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
  max-height: 40vh;
  overflow-y: auto;
  padding-right: 4px;
}

.category-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  border: 2px solid var(--border-color);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  background: var(--bg-secondary);
}

.category-item:hover {
  border-color: var(--accent);
  background: var(--accent-trans);
}

.category-item.selected {
  border-color: var(--accent);
  background: var(--accent-trans);
}

.category-item input[type='radio'] {
  display: none;
}

.category-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: var(--bg-card);
  color: var(--accent-text);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 15px;
}

.category-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.category-title {
  font-weight: 600;
  font-size: 14px;
  color: var(--text-primary);
}

.category-desc {
  font-size: 12px;
  color: var(--text-muted);
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.form-label {
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  color: var(--text-secondary);
}

.form-label-muted {
  color: var(--text-muted);
  font-weight: var(--fw-normal);
}

.form-textarea {
  width: 100%;
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
  font-family: inherit;
  background: var(--bg-input);
  border: 1px solid var(--border-input);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  resize: vertical;
  min-height: 80px;
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.form-textarea:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: var(--shadow-focus);
}

.form-textarea::placeholder {
  color: var(--text-muted);
}

.char-count {
  display: block;
  text-align: right;
  font-size: 12px;
  color: var(--text-muted);
}
</style>
