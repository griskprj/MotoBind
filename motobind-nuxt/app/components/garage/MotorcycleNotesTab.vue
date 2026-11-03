<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'

const props = defineProps<{
  motorcycle: any
}>()

const emit = defineEmits<{
  (e: 'updated'): void
}>()

// Режимы: 'view' (чтение) или 'edit' (редактирование)
const mode = ref<'view' | 'edit'>('view')

// Локальная копия заметки для редактирования
const localNotes = ref(props.motorcycle.note || '')
const isSaving = ref(false)
const lastSaved = ref<Date | null>(null)
const errorMsg = ref<string | null>(null)

// Синхронизация при обновлении пропса
watch(() => props.motorcycle.note, (newVal) => {
  if (newVal !== localNotes.value) {
    localNotes.value = newVal || ''
  }
})

// Есть ли несохраненные изменения
const isDirty = computed(() => {
  return localNotes.value !== (props.motorcycle.note || '')
})

// Переключение в режим редактирования
function startEditing() {
  localNotes.value = props.motorcycle.note || ''
  errorMsg.value = null
  mode.value = 'edit'
  // Автофокус на редактор после переключения (опционально)
  nextTick(() => {
    const editor = document.querySelector('.md-editor textarea, .cm-content')
    if (editor instanceof HTMLElement) editor.focus()
  })
}

// Отмена редактирования
function cancelEditing() {
  localNotes.value = props.motorcycle.note || ''
  errorMsg.value = null
  mode.value = 'view'
}

// Сохранение
async function saveNotes() {
  if (!isDirty.value) {
    mode.value = 'view'
    return
  }

  isSaving.value = true
  errorMsg.value = null

  try {
    const api = useApi()
    await api.motorcycle.updateNote(props.motorcycle.id, localNotes.value)

    lastSaved.value = new Date()
    mode.value = 'view' // Переключаем обратно в режим чтения
    emit('updated') // Обновляем данные у родителя
  } catch (err: any) {
    console.error('Ошибка сохранения заметки', err)
    errorMsg.value = err?.data?.message || err?.message || 'Не удалось сохранить заметку.'
  } finally {
    isSaving.value = false
  }
}

function formatSaveTime(date: Date) {
  return date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
}

// Есть ли вообще текст для отображения
const hasContent = computed(() => {
  return props.motorcycle.note && props.motorcycle.note.trim().length > 0
})
</script>

<template>
  <div class="notes-tab">
    <!-- Заголовок (Баннер) -->
    <div class="notes-header">
      <div class="header-icon">
        <i class="fa-solid fa-pen-to-square"></i>
      </div>
      <div class="header-content">
        <h2 class="header-title">Заметки</h2>
        <p class="header-subtitle">Личная заметка о мотоцикле. Видна только вам.</p>
      </div>
    </div>

    <!-- Карточка -->
    <div class="editor-card">

      <!-- РЕЖИМ ЧТЕНИЯ -->
      <div v-if="mode === 'view'" class="view-mode">
        <div v-if="hasContent" class="markdown-content">
          <MarkdownRenderer :content="motorcycle.note" />
        </div>
        <div v-else class="empty-state">
          <i class="fa-regular fa-file-lines"></i>
          <p>Заметок пока нет. Нажмите «Редактировать», чтобы добавить первую запись.</p>
        </div>
      </div>

      <!-- РЕЖИМ РЕДАКТИРОВАНИЯ -->
      <div v-else class="edit-mode">
        <div class="editor-wrapper">
          <MarkdownEditor
            v-model="localNotes"
            placeholder="Напишите что-нибудь о мотоцикле... (поддерживается Markdown)"
          />
        </div>
      </div>

      <!-- ФУТЕР -->
      <div class="editor-footer">
        <!-- Статус -->
        <div class="footer-status">
          <span v-if="errorMsg" class="save-status error">
            <i class="fa-solid fa-circle-exclamation"></i> {{ errorMsg }}
          </span>
          <span v-else-if="mode === 'edit' && isDirty" class="save-status muted">
            <i class="fa-solid fa-pen"></i> Есть несохраненные изменения
          </span>
          <span v-else-if="lastSaved" class="save-status">
            <i class="fa-solid fa-check"></i> Сохранено сегодня в {{ formatSaveTime(lastSaved) }}
          </span>
        </div>

        <!-- Кнопки -->
        <div class="footer-actions">
          <!-- В режиме чтения -->
          <template v-if="mode === 'view'">
            <BaseButton variant="secondary" @click="startEditing">
              <template #icon><i class="fa-solid fa-pen"></i></template>
              Редактировать
            </BaseButton>
          </template>

          <!-- В режиме редактирования -->
          <template v-else>
            <BaseButton
              variant="secondary"
              :disabled="isSaving"
              @click="cancelEditing"
            >
              Отменить
            </BaseButton>
            <BaseButton
              variant="primary"
              :disabled="isSaving"
              :loading="isSaving"
              @click="saveNotes"
            >
              <template #icon><i class="fa-solid fa-check"></i></template>
              Сохранить
            </BaseButton>
          </template>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped lang="scss">
.notes-tab {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

/* Заголовок */
.notes-header {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4);
  background: linear-gradient(90deg, rgba(112, 0, 255, 0.1) 0%, rgba(20, 20, 25, 1) 100%);
  border-radius: var(--radius-lg);
  border: 1px solid rgba(112, 0, 255, 0.2);
}

.header-icon {
  width: 48px;
  height: 48px;
  background: rgba(112, 0, 255, 0.2);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #a855f7;
  font-size: 20px;
  flex-shrink: 0;
}

.header-title {
  font-size: var(--text-xl);
  font-weight: var(--fw-bold);
  color: var(--color-text-primary);
  margin-bottom: var(--space-1);
}

.header-subtitle {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

/* Карточка */
.editor-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Режим чтения */
.view-mode {
  padding: var(--space-5);
  min-height: 200px;
}

.markdown-content {
  /* MarkdownRenderer сам стилизует свои элементы,
     но мы можем задать базовый размер шрифта */
  font-size: var(--text-base);
  line-height: 1.6;
  color: var(--color-text);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-8) var(--space-4);
  text-align: center;
  color: var(--color-text-tertiary);
  height: 100%;
  min-height: 200px;

  i {
    font-size: 32px;
    margin-bottom: var(--space-3);
    opacity: 0.5;
  }

  p {
    font-size: var(--text-sm);
    max-width: 400px;
  }
}

/* Режим редактирования */
.edit-mode {
  padding: var(--space-2);
}

.editor-wrapper {
  :deep(.md-editor) {
    border: none !important;
    border-radius: 0 !important;
    background: transparent !important;
  }

  :deep(.md-editor-toolbar-wrapper) {
    border-bottom: 1px solid var(--color-border) !important;
    background: transparent !important;
  }

  :deep(.md-editor-content) {
    background: transparent !important;
  }

  :deep(.cm-editor) {
    background: transparent !important;
  }

  :deep(.md-editor-preview-wrapper) {
    background: transparent !important;
  }
}

/* Футер */
.editor-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-3) var(--space-4);
  background: var(--color-surface-secondary);
  border-top: 1px solid var(--color-border);
  flex-wrap: wrap;
  gap: var(--space-3);
}

.footer-status {
  font-size: var(--text-sm);
}

.save-status {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  color: var(--color-text-secondary);

  i {
    color: #22c55e;
  }

  &.muted {
    opacity: 0.6;
  }

  &.error {
    color: #ef4444;
    i {
      color: #ef4444;
    }
  }
}

.footer-actions {
  display: flex;
  gap: var(--space-2);
}
</style>
