<template>
  <div class="container">
    <LoadingOverlay :isLoading="loading" text="Загрузка кабинета..."/>

    <Header
      title="Кабинет бизнеса"
      :subtitle="subtitle"
    />

    <!-- === НЕТ АККАУНТА: ФОРМА СОЗДАНИЯ === -->
    <div v-if="!business.hasAccount && !loading" class="create-wrap">
      <div class="create-card">
        <div class="create-icon">
          <i class="fa fa-briefcase"></i>
        </div>
        <h2>Создайте бизнес-аккаунт</h2>
        <p class="create-hint">
          Вы можете вести учёт клиентов и их мотоциклов как частный мастер
          или как станция технического обслуживания.
        </p>

        <!-- Выбор типа -->
        <div class="type-grid">
          <button
            type="button"
            class="type-card"
            :class="{ active: form.type === 'master' }"
            @click="form.type = 'master'"
          >
            <div class="type-icon">
              <i class="fa fa-user-gear"></i>
            </div>
            <div class="type-title">Частный мастер</div>
            <div class="type-desc">Работаю один</div>
          </button>

          <button
            type="button"
            class="type-card"
            :class="{ active: form.type === 'station' }"
            @click="form.type = 'station'"
          >
            <div class="type-icon">
              <i class="fa fa-warehouse"></i>
            </div>
            <div class="type-title">СТО</div>
            <div class="type-desc">Станция обслуживания</div>
          </button>
        </div>

        <!-- Поля -->
        <div class="form-grid">
          <BaseInput
            v-model="form.name"
            :label="form.type === 'master' ? 'Имя мастера' : 'Название СТО'"
            placeholder="Иван Петров"
            required
          />
          <BaseInput v-model="form.city" label="Город" placeholder="Москва" />
          <BaseInput v-model="form.phone" label="Телефон" placeholder="+7 (___) ___-__-__" />
          <BaseInput v-model="form.email" label="Email" type="email" placeholder="mail@example.com" />
          <BaseInput v-model="form.address" label="Адрес" placeholder="ул. Ленина, 1" />
          <BaseInput v-model="form.website" label="Сайт" placeholder="https://..." />
        </div>

        <div class="form-field">
          <label>Описание</label>
          <textarea
            v-model="form.description"
            rows="3"
            placeholder="Чем вы занимаетесь, какой опыт, чем можете помочь"
          ></textarea>
        </div>

        <div class="create-actions">
          <BaseButton
            variant="primary"
            block
            :loading="business.mutating"
            :disabled="!canCreate"
            icon="fa fa-check"
            @click="handleCreate"
          >
            Создать аккаунт
          </BaseButton>
        </div>
      </div>
    </div>

    <!-- === ЕСТЬ АККАУНТ: ПРОФИЛЬ === -->
    <div v-else-if="business.hasAccount" class="dashboard">
      <div class="dashboard-grid">
        <!-- Левая колонка: карточка аккаунта -->
        <aside class="account-card">
          <div class="account-logo-wrap">
            <img
              v-if="business.account.logo_url"
              :src="getBusinessLogoUrl(business.account.logo_url)"
              alt="logo"
              class="account-logo"
              @error="onLogoError"
            >
            <div v-else class="account-logo-placeholder">
              <i class="fa" :class="business.isStation ? 'fa-warehouse' : 'fa-user-gear'"></i>
            </div>
            <button class="logo-edit-btn" @click="triggerLogoInput" title="Изменить лого">
              <i class="fa fa-camera"></i>
            </button>
            <input
              ref="logoInputRef"
              type="file"
              accept="image/*"
              style="display: none"
              @change="handleLogoUpload"
            >
          </div>

          <div class="account-type-badge">
            {{ business.isStation ? 'СТО' : 'Частный мастер' }}
          </div>

          <h3 class="account-name">{{ business.account.name }}</h3>

          <div class="account-slug">
            <i class="fa fa-link"></i>
            <code>/{{ business.account.slug }}</code>
            <button
              class="copy-btn"
              :title="'Скопировать ссылку'"
              @click="copySlug"
            >
              <i class="fa fa-copy"></i>
            </button>
          </div>

          <p v-if="business.account.description" class="account-desc">
            {{ business.account.description }}
          </p>

          <div class="account-info">
            <div v-if="business.account.city" class="info-item">
              <i class="fa fa-map-marker"></i>
              <span>{{ business.account.city }}</span>
            </div>
            <div v-if="business.account.phone" class="info-item">
              <i class="fa fa-phone"></i>
              <span>{{ business.account.phone }}</span>
            </div>
            <div v-if="business.account.email" class="info-item">
              <i class="fa fa-envelope"></i>
              <span>{{ business.account.email }}</span>
            </div>
            <div v-if="business.account.website" class="info-item">
              <i class="fa fa-globe"></i>
              <a :href="business.account.website" target="_blank" rel="noopener">
                {{ business.account.website }}
              </a>
            </div>
          </div>

          <div class="account-actions">
            <BaseButton
              variant="secondary"
              block
              icon="fa fa-pen"
              @click="openEditModal"
            >
              Редактировать
            </BaseButton>
          </div>

          <div v-if="business.account.logo_url" class="logo-remove">
            <button class="btn-outline danger" @click="removeLogo">
              <i class="fa fa-trash"></i> Удалить лого
            </button>
          </div>
        </aside>

        <!-- Правая колонка: быстрые действия + метрики -->
        <main class="account-main">
          <div class="stats-row">
            <div class="metric-card">
              <div class="metric-icon">
                <i class="fa fa-users"></i>
              </div>
              <div class="metric-body">
                <div class="metric-value">{{ business.account.clients_count || 0 }}</div>
                <div class="metric-label">Клиентов</div>
              </div>
            </div>
          </div>

          <div class="quick-actions">
            <h4>Быстрые действия</h4>
            <router-link to="/business/clients" class="quick-card">
              <div class="quick-icon">
                <i class="fa fa-users"></i>
              </div>
              <div class="quick-body">
                <div class="quick-title">Мои клиенты</div>
                <div class="quick-desc">Список клиентов и их мотоциклов</div>
              </div>
              <i class="fa fa-chevron-right quick-arrow"></i>
            </router-link>

            <router-link to="/business/services" class="quick-card">
              <div class="quick-icon"><i class="fa fa-wrench"></i></div>
              <div class="quick-body">
                <div class="quick-title">Мои услуги</div>
                <div class="quick-desc">Каталог услуг с ценами и длительностью</div>
              </div>
              <i class="fa fa-chevron-right quick-arrow"></i>
            </router-link>

            <router-link to="/business/bookings" class="quick-card">
              <div class="quick-icon"><i class="fa fa-calendar-check"></i></div>
              <div class="quick-body">
                <div class="quick-title">Заявки</div>
                <div class="quick-desc">Записи клиентов и их статусы</div>
              </div>
              <i class="fa fa-chevron-right quick-arrow"></i>
            </router-link>
          </div>
        </main>
      </div>
    </div>

    <!-- Модалка редактирования -->
    <EditBusinessAccountModal
      :is-open="showEditModal"
      :account="business.account"
      @close="showEditModal = false"
      @saved="onAccountSaved"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useBusinessStore } from '@/stores'
import { useToast } from '../../composables/useToast'
import { getBusinessLogoUrl } from '../../utils/mediaUrl'
import Header from '../../components/Header.vue'
import LoadingOverlay from '../../components/LoadingOverlay.vue'
import { BaseButton, BaseInput } from '../../components/ui'
import EditBusinessAccountModal from '../../components/modals/business/EditBusinessAccountModal.vue'

const router = useRouter()
const toast = useToast()
const business = useBusinessStore()

const { accountLoading: loading } = storeToRefs(business)

const showEditModal = ref(false)
const logoInputRef = ref(null)

const form = reactive({
  type: 'master',
  name: '',
  description: '',
  city: '',
  address: '',
  phone: '',
  email: '',
  website: '',
})

const subtitle = computed(() => {
  if (!business.hasAccount) return 'Создайте аккаунт мастера или СТО'
  return business.isStation
    ? 'Управляйте станцией и клиентами'
    : 'Управляйте клиентами и их мотоциклами'
})

const canCreate = computed(() => {
  return form.type && form.name && form.name.trim().length >= 2
})

onMounted(async () => {
  try {
    await business.loadAccount()
  } catch (err) {
    toast.error('Не удалось загрузить кабинет')
  }
})

// ===== Создание =====
async function handleCreate() {
  if (!canCreate.value) return
  try {
    await business.createAccount({
      type: form.type,
      name: form.name.trim(),
      description: form.description?.trim() || null,
      city: form.city?.trim() || null,
      address: form.address?.trim() || null,
      phone: form.phone?.trim() || null,
      email: form.email?.trim() || null,
      website: form.website?.trim() || null,
    })
    toast.success('Бизнес-аккаунт создан!')
  } catch (err) {
    toast.error(err.response?.data?.error || 'Ошибка создания')
  }
}

// ===== Лого =====
function triggerLogoInput() {
  logoInputRef.value?.click()
}

async function handleLogoUpload(e) {
  const file = e.target.files?.[0]
  if (!file) return
  if (file.size > 5 * 1024 * 1024) {
    toast.error('Файл больше 5 МБ')
    e.target.value = ''
    return
  }
  try {
    await business.uploadLogo(file)
    toast.success('Логотип обновлён')
  } catch (err) {
    toast.error(err.response?.data?.error || 'Ошибка загрузки')
  } finally {
    e.target.value = ''
  }
}

async function removeLogo() {
  if (!confirm('Удалить логотип?')) return
  try {
    await business.deleteLogo()
    toast.success('Логотип удалён')
  } catch (err) {
    toast.error('Ошибка удаления')
  }
}

function onLogoError(e) {
  e.target.style.display = 'none'
}

// ===== Прочее =====
function openEditModal() {
  showEditModal.value = true
}

function onAccountSaved() {
  showEditModal.value = false
}

async function copySlug() {
  const url = `${window.location.origin}/business/${business.account.slug}`
  try {
    await navigator.clipboard.writeText(url)
    toast.success('Ссылка скопирована')
  } catch {
    toast.error('Не удалось скопировать')
  }
}
</script>

<style scoped>
/* === CREATE === */
.create-wrap {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}
.create-card {
  width: 100%;
  max-width: 640px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 32px 28px;
}
.create-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--accent-trans);
  color: var(--accent-text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  margin: 0 auto 16px;
}
.create-card h2 {
  text-align: center;
  margin: 0 0 8px;
  font-size: 22px;
}
.create-hint {
  text-align: center;
  color: var(--text-secondary);
  font-size: 14px;
  margin-bottom: 24px;
  line-height: var(--leading-base);
}

.type-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 20px;
}
.type-card {
  background: var(--bg-secondary);
  border: 2px solid var(--border-light);
  border-radius: var(--radius-md);
  padding: 16px;
  text-align: center;
  cursor: pointer;
  transition: all var(--transition-base);
  min-height: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}
.type-card:hover {
  border-color: var(--accent);
  background: var(--accent-trans);
}
.type-card.active {
  border-color: var(--accent);
  background: var(--accent-trans);
}
.type-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--bg-card);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: var(--accent-text);
}
.type-title {
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
  font-size: 14px;
}
.type-desc {
  font-size: 12px;
  color: var(--text-muted);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-bottom: 14px;
}
.form-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 16px;
}
.form-field label {
  font-size: var(--text-sm);
  font-weight: var(--fw-semibold);
  color: var(--text-secondary);
}
.form-field textarea {
  width: 100%;
  padding: 0.625rem 0.75rem;
  font-size: var(--text-sm);
  font-family: inherit;
  background: var(--bg-input);
  border: 1px solid var(--border-input);
  border-radius: var(--radius);
  color: var(--text-primary);
  resize: vertical;
}
.form-field textarea:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: var(--shadow-focus);
}
.create-actions {
  margin-top: 8px;
}

/* === DASHBOARD === */
.dashboard-grid {
  display: grid;
  grid-template-columns: 340px 1fr;
  gap: 24px;
  align-items: start;
}

.account-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 24px;
  text-align: center;
  position: sticky;
  top: 24px;
}

.account-logo-wrap {
  position: relative;
  width: 110px;
  height: 110px;
  margin: 0 auto 14px;
}
.account-logo {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid var(--accent);
}
.account-logo-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: var(--accent-trans);
  color: var(--accent-text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 42px;
  border: 3px solid var(--accent);
}
.logo-edit-btn {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 36px;
  height: 36px;
  min-height: 36px;
  padding: 0;
  border-radius: 50%;
  background: var(--accent);
  border: none;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  transition: all var(--transition-base);
}
.logo-edit-btn:hover { background: var(--accent-hover); transform: scale(1.05); }

.account-type-badge {
  display: inline-block;
  padding: 2px 12px;
  border-radius: var(--radius-full);
  background: var(--accent-trans);
  color: var(--accent-text);
  font-size: 11px;
  font-weight: var(--fw-semibold);
  text-transform: uppercase;
  letter-spacing: 0.4px;
  margin-bottom: 8px;
}

.account-name {
  margin: 0 0 8px;
  font-size: 19px;
  color: var(--text-primary);
}

.account-slug {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 6px 10px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  margin-bottom: 12px;
  font-size: 12px;
  color: var(--text-secondary);
}
.account-slug code {
  font-family: var(--font-mono);
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.account-slug i { color: var(--text-muted); font-size: 11px; }
.copy-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 4px;
  min-height: 24px;
  border-radius: var(--radius-sm);
  transition: all var(--transition-base);
}
.copy-btn:hover { color: var(--accent-text); background: var(--accent-trans); }

.account-desc {
  font-size: 13px;
  color: var(--text-secondary);
  text-align: left;
  margin: 0 0 14px;
  padding: 10px 14px;
  background: var(--bg-secondary);
  border-left: 3px solid var(--accent);
  border-radius: var(--radius-sm);
  line-height: var(--leading-base);
}

.account-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
  text-align: left;
  margin-bottom: 16px;
}
.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-secondary);
}
.info-item i { width: 16px; min-width: 16px; color: var(--accent-text); }
.info-item a { color: var(--accent-text); }

.account-actions { margin-top: 8px; }
.logo-remove {
  margin-top: 12px;
  display: flex;
  justify-content: center;
}
.btn-link.danger { color: var(--danger-text); }

/* === MAIN === */
.account-main { min-width: 0; }
.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
  margin-bottom: 20px;
}
.metric-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
}
.metric-icon {
  width: 46px;
  height: 46px;
  border-radius: var(--radius-md);
  background: var(--accent-trans);
  color: var(--accent-text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}
.metric-value {
  font-size: 22px;
  font-weight: var(--fw-bold);
  color: var(--text-primary);
  line-height: 1.1;
}
.metric-label {
  font-size: 12px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.4px;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.quick-actions h4 {
  font-size: 15px;
  margin: 0 0 12px;
  color: var(--text-primary);
}
.quick-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  text-decoration: none;
  color: inherit;
  transition: all var(--transition-base);
}
.quick-card:hover {
  border-color: var(--accent);
  background: var(--accent-trans);
  transform: translateY(-2px);
}
.quick-icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  background: var(--accent-trans);
  color: var(--accent-text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}
.quick-body { flex: 1; min-width: 0; }
.quick-title {
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
  font-size: 14px;
}
.quick-desc { font-size: 12px; color: var(--text-muted); }
.quick-arrow { color: var(--text-muted); }

/* === АДАПТИВ === */
@media (max-width: 900px) {
  .dashboard-grid { grid-template-columns: 1fr; }
  .account-card { position: static; }
}
@media (max-width: 640px) {
  .form-grid { grid-template-columns: 1fr; }
  .type-grid { grid-template-columns: 1fr; }
  .create-card { padding: 20px 16px; }
}
</style>
