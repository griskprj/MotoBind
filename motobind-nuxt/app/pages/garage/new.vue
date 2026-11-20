<script setup lang="ts">
import type { ApiError, CreateMotorcyclePayload } from '~/types'
import { asString } from '#imports'

definePageMeta({ middleware: 'auth' })

useSeoMeta({
  title: 'Добавление мотоцикла',
  robots: 'noindex',
})

const api = useApi()
const router = useRouter()
const toast = useToast()
const { errors, setFromApiError, clear } = useFormErrors()

const form = reactive({
  name: '',
  years: '',
  volume: '' as string | number,
  drive_type: 'chain' as 'chain' | 'belt' | 'shaft',
  color: '',
  licensePlate: '',
  vin: '',
})

const photoFile = ref<File | null>(null)
const photoPreview = ref<string | null>(null)

const submitting = ref(false)

function onFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  if (file.size > 15 * 1024 * 1024) {
    toast.error('Фото не должно превышать 15МБ')
    return
  }

  photoFile.value = file

  const reader = new FileReader()
  reader.onload = (e) => {
    photoPreview.value = e.target?.result as string
  }
  reader.readAsDataURL(file)
}

function clearPhoto() {
  photoFile.value = null
  photoPreview.value = null
}

async function onSubmit() {
  clear()
  submitting.value = true

  try {
    const payload: CreateMotorcyclePayload = {
      name: asString(form.name).trim(),
      years: asString(form.years).trim() || null,
      volume: form.volume ? Number(form.volume) : null,
      drive_type: form.drive_type,
      color: form.color.trim() || null,
      licensePlate: asString(form.licensePlate).trim().toUpperCase() || null,
      vin: asString(form.vin).trim().toUpperCase() || null,
    }

    const newMoto = await api.motorcycle.create(payload)

    if (photoFile.value) {
      try {
        await api.motorcycle.uploadPhoto(newMoto.id, photoFile.value)
      } catch (e) {
        toast.error('Мотоцикл создан, но фото не загрузилось. Попробуйте позже.')
        console.error('Photo upload failed:', e)
      }
    }

    toast.success('Мотоцикл успешно добавлен!')

    await router.push(`/garage/${newMoto.id}`)

  } catch (e) {
    const err = e as ApiError
    setFromApiError(err)
    if (!err.fieldErrors) {
      toast.error(err.message || 'Не удалось создать мотоцикл')
    }
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="page-new">
    <header class="page-header">
      <div>
        <NuxtLink to="/garage" class="back-link">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <path d="M15 19l-7-7 7-7" />
          </svg>
          Назад в гараж
        </NuxtLink>
        <h1 class="page-title">Добавить мотоцикл</h1>
        <p class="page-subtitle">Заполните характеристики вашего мотоцикла</p>
      </div>
    </header>

    <BaseCard padding="lg" class="form-card">
      <form class="moto-form" novalidate @submit.prevent="onSubmit">

        <!-- Блок с фото -->
        <div class="photo-section">
          <div v-if="photoPreview" class="photo-preview">
            <img :src="photoPreview" alt="Превью" />
            <button type="button" class="photo-remove" @click="clearPhoto" title="Удалить фото">×</button>
          </div>
          <label v-else class="photo-upload">
            <input type="file" accept="image/*" class="visually-hidden" @change="onFileChange" />
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>Добавить фото</span>
            <span class="photo-hint">JPG, PNG до 5МБ</span>
          </label>
        </div>

        <!-- Блок с текстовыми полями -->
        <div class="form-grid">
          <BaseInput
            v-model="form.name"
            label="Название (марка и модель)"
            placeholder="Например: Honda CB600F"
            required
            class="span-2"
            :error="errors.name"
          />

          <BaseInput
            v-model="form.years"
            label="Год выпуска"
            placeholder="2020"
            :error="errors.years"
          />

          <BaseSelect
            v-model="form.drive_type"
            label="Тип привода"
            :options="[
              { value: 'chain', label: 'Цепь' },
              { value: 'belt', label: 'Ремень' },
              { value: 'shaft', label: 'Кардан' },
            ]"
          />

          <BaseInput
            v-model="form.volume"
            type="number"
            label="Объем двигателя (см³)"
            placeholder="600"
            :error="errors.volume"
          />

          <BaseColorPicker
            v-model="form.color"
            label="Цвет"
            :error="errors.color"
          />

          <BaseInput
            v-model="form.licensePlate"
            label="Госномер"
            placeholder="А123БВ 77"
            :error="errors.licensePlate"
            style="text-transform: uppercase;"
          />

          <BaseInput
            v-model="form.vin"
            label="VIN"
            placeholder="17 символов"
            maxlength="17"
            class="span-2"
            :error="errors.vin"
            style="text-transform: uppercase;"
          />
        </div>

        <p v-if="errors._form" class="form-error-global" role="alert">
          {{ errors._form }}
        </p>

        <div class="form-actions">
          <BaseButton to="/garage" variant="secondary" size="lg">
            Отмена
          </BaseButton>
          <BaseButton type="submit" variant="primary" size="lg" :loading="submitting">
            Сохранить
          </BaseButton>
        </div>
      </form>
    </BaseCard>
  </div>
</template>

<style scoped lang="scss">
@use '~/assets/styles/breakpoints' as *;

.page-new {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.page-header {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  transition: color var(--transition-fast);
  width: fit-content;

  &:hover {
    color: var(--color-brand);
  }
}

.page-title {
  font-size: var(--text-2xl);
  font-weight: var(--fw-bold);
  color: var(--color-text);
}

.page-subtitle {
  font-size: var(--text-base);
  color: var(--color-text-secondary);
}

.form-card {
  background: var(--color-surface);
}

.moto-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.photo-section {
  display: flex;
  justify-content: center;
}

.photo-preview {
  position: relative;
  width: 100%;
  max-width: 400px;
  aspect-ratio: 16 / 9;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--color-border);

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.photo-remove {
  position: absolute;
  top: var(--space-2);
  right: var(--space-2);
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  cursor: pointer;
  backdrop-filter: blur(4px);
  transition: background var(--transition-fast);

  &:hover {
    background: rgba(0, 0, 0, 0.8);
  }
}

.photo-upload {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 400px;
  aspect-ratio: 16 / 9;
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface-secondary);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  gap: var(--space-1);

  &:hover {
    border-color: var(--color-brand);
    background: var(--color-brand-soft);
    color: var(--color-brand);
  }
}

.photo-hint {
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
  margin-top: var(--space-1);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);

  @include sm-up {
    grid-template-columns: 1fr 1fr;
  }
}

.span-2 {
  @include sm-up {
    grid-column: span 2;
  }
}

.form-error-global {
  font-size: var(--text-sm);
  color: var(--color-danger);
  text-align: center;
}

.form-actions {
  display: flex;
  flex-direction: column-reverse;
  gap: var(--space-3);
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border-light);

  @include sm-up {
    flex-direction: row;
    justify-content: flex-end;
  }
}
</style>
