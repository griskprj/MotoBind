<template>
  <div class="container">
    <LoadingOverlay :isLoading="loading" text="Загрузка..."/>

    <div v-if="account" class="public-page">
      <div class="public-header">
        <div class="public-logo">
          <img
            v-if="account.logo_url"
            :src="getBusinessLogoUrl(account.logo_url)"
            alt="logo"
            @error="(e) => (e.target.style.display = 'none')"
          >
          <i v-else class="fa" :class="account.type === 'station' ? 'fa-warehouse' : 'fa-user-gear'"></i>
        </div>

        <div class="public-info">
          <div class="public-type-badge">
            {{ account.type === 'station' ? 'СТО' : 'Частный мастер' }}
          </div>
          <h1>{{ account.name }}</h1>
          <div v-if="account.city" class="public-city">
            <i class="fa fa-map-marker"></i> {{ account.city }}
          </div>

          <BaseButton
            v-if="isAuthenticated && !isOwner"
            variant="primary"
            icon="fa fa-calendar-plus"
            class="public-book-btn"
            @click="openBookingModal"
          >
            Записаться
          </BaseButton>

          <router-link
            v-else-if="!isAuthenticated"
            :to="{ name: 'login', query: { redirect: $route.fullPath } }"
            class="public-book-btn login-cta"
          >
            <i class="fa fa-sign-in-alt"></i> Войдите, чтобы записаться
          </router-link>

          <p v-else class="public-book-btn owner-note">
            <i class="fa fa-info-circle"></i> Это ваш бизнес-аккаунт
          </p>

          <p v-if="account.description" class="public-desc">
            {{ account.description }}
          </p>
        </div>
      </div>

      <div class="public-contacts">
        <h3>Контакты</h3>
        <div class="contact-list">
          <a v-if="account.phone" :href="`tel:${account.phone}`" class="contact-item">
            <i class="fa fa-phone"></i>
            <div>
              <div class="contact-label">Телефон</div>
              <div class="contact-value">{{ account.phone }}</div>
            </div>
          </a>
          <a v-if="account.email" :href="`mailto:${account.email}`" class="contact-item">
            <i class="fa fa-envelope"></i>
            <div>
              <div class="contact-label">Email</div>
              <div class="contact-value">{{ account.email }}</div>
            </div>
          </a>
          <a v-if="account.website" :href="account.website" target="_blank" rel="noopener" class="contact-item">
            <i class="fa fa-globe"></i>
            <div>
              <div class="contact-label">Сайт</div>
              <div class="contact-value">{{ account.website }}</div>
            </div>
          </a>
          <div v-if="account.address" class="contact-item">
            <i class="fa fa-map"></i>
            <div>
              <div class="contact-label">Адрес</div>
              <div class="contact-value">{{ account.address }}</div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="services.length" class="public-services">
        <h3>Услуги</h3>
        <div class="services-list">
          <div
            v-for="s in services"
            :key="s.id"
            class="service-item"
          >
            <div class="service-item-icon">
              <i :class="categoryIcon(s.category)"></i>
            </div>
            <div class="service-item-body">
              <div class="service-item-title">{{ s.title }}</div>
              <div v-if="s.description" class="service-item-desc">{{ s.description }}</div>
            </div>
            <div class="service-item-price">
              <template v-if="s.price_from && s.price_to">{{ s.price_from }}–{{ s.price_to }} ₽</template>
              <template v-else-if="s.price_from">от {{ s.price_from }} ₽</template>
              <template v-else-if="s.price_to">до {{ s.price_to }} ₽</template>
            </div>
          </div>
        </div>
      </div>

      <div class="public-footer">
        <p class="public-hint">
          <i class="fa fa-info-circle"></i>
          Учёт обслуживания, услуги и запись — скоро.
        </p>
      </div>
    </div>

    <div v-else-if="!loading" class="empty">
      <i class="fa fa-user-slash"></i>
      <h3>Мастер не найден</h3>
    </div>
  </div>

  <CreateBookingModal
    v-if="account && isAuthenticated"
    :is-open="showBookingModal"
    :business="account"
    :services="services"
    :motorcycles="motorcyclesStore.items"
    @close="showBookingModal = false"
    @created="onBookingCreated"
  />
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api/api'
import { useServicesStore, useAuthStore, useBookingsStore, useMotorcyclesStore } from '@/stores'
import { getBusinessLogoUrl } from '@/utils/mediaUrl'
import { BaseButton } from '@/components/ui'
import LoadingOverlay from '@/components/LoadingOverlay.vue'
import CreateBookingModal from '../../components/modals/bookings/CreateBookingModal.vue'

const route = useRoute()
const loading = ref(true)
const account = ref(null)

const servicesStore = useServicesStore()
const services = computed(() => servicesStore.publicServices)

const auth = useAuthStore()
const bookingsStore = useBookingsStore()
const motorcyclesStore = useMotorcyclesStore()

const isAuthenticated = computed(() => auth.isAuthenticated)
const isOwner = computed(() => auth.user?.id && auth.user.id === account.value?.owner_id)
const showBookingModal = ref(false)

onMounted(async () => {
  try {
    const { data } = await api.get(`/business/public/${route.params.slug}`)
    account.value = data
    if (data.slug) {
      await servicesStore.loadPublic(data.slug)
    }
  } catch {
    account.value = null
  } finally {
    loading.value = false
  }
})

async function openBookingModal() {
  if (!motorcyclesStore.items.length) {
    try { await motorcyclesStore.loadAll() } catch {}
  }
  showBookingModal.value = true
}

function onBookingCreated() {
  showBookingModal.value = false
}

function categoryIcon(c) {
  return {
    maintenance: 'fa fa-wrench',
    repair: 'fa fa-screwdriver-wrench',
    diagnostics: 'fa fa-stethoscope',
    tuning: 'fa fa-gauge-high',
    other: 'fa fa-gear',
  }[c] || 'fa fa-gear'
}
</script>

<style scoped>
.public-page {
  max-width: 720px;
  margin: 0 auto;
  padding: 20px 0;
}

.public-header {
  display: flex;
  align-items: center;
  gap: 24px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 32px;
  margin-bottom: 20px;
}

.public-logo {
  width: 96px;
  height: 96px;
  min-height: 96px;
  border-radius: 50%;
  background: var(--accent-trans);
  color: var(--accent-text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 38px;
  overflow: hidden;
  flex-shrink: 0;
  border: 3px solid var(--accent);
}
.public-logo img { width: 100%; height: 100%; object-fit: cover; }

.public-info { flex: 1; min-width: 0; }
.public-type-badge {
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
.public-info h1 {
  margin: 0 0 6px;
  font-size: 26px;
  color: var(--text-primary);
}
.public-city {
  color: var(--text-muted);
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 10px;
}
.public-desc {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: var(--leading-base);
  margin: 0;
}

.public-contacts {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 24px;
}
.public-contacts h3 {
  margin: 0 0 16px;
  font-size: 16px;
  color: var(--text-primary);
}
.contact-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 10px;
}
.contact-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  text-decoration: none;
  color: inherit;
  transition: all var(--transition-base);
}
.contact-item:hover { background: var(--accent-trans); }
.contact-item > i {
  width: 32px;
  height: 32px;
  min-height: 32px;
  border-radius: 50%;
  background: var(--accent-trans);
  color: var(--accent-text);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.contact-item > i:before { font-size: 14px; }
.contact-label {
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.4px;
}
.contact-value {
  font-size: 14px;
  color: var(--text-primary);
  word-break: break-word;
}

.public-book-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 12px;
  padding: 10px 20px;
  border-radius: var(--radius-md);
  font-weight: var(--fw-semibold);
  font-size: 14px;
  text-decoration: none;
}
.login-cta {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}
.login-cta:hover { border-color: var(--accent); color: var(--accent-text); }
.owner-note {
  color: var(--text-muted);
  font-size: 13px;
  background: transparent;
  padding: 0;
}

.public-services {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 24px;
  margin-top: 20px;
}
.public-services h3 { margin: 0 0 16px; font-size: 16px; }

.services-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.service-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 14px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
}
.service-item-icon {
  width: 40px;
  height: 40px;
  min-height: 40px;
  border-radius: var(--radius-md);
  background: var(--accent-trans);
  color: var(--accent-text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}
.service-item-body { flex: 1; min-width: 0; }
.service-item-title {
  font-size: 14px;
  font-weight: var(--fw-semibold);
  color: var(--text-primary);
}
.service-item-desc {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.service-item-price {
  font-size: 14px;
  font-weight: var(--fw-semibold);
  color: var(--accent-text);
  white-space: nowrap;
}

@media (max-width: 640px) {
  .service-item { flex-wrap: wrap; }
  .service-item-price { flex-basis: 100%; text-align: right; margin-top: 6px; }
}

.public-footer { margin-top: 20px; text-align: center; }
.public-hint {
  font-size: 13px;
  color: var(--text-muted);
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.empty {
  text-align: center;
  padding: 60px 20px;
}
.empty i { font-size: 48px; color: var(--text-muted); margin-bottom: 12px; display: block; }

@media (max-width: 640px) {
  .public-header { flex-direction: column; text-align: center; padding: 24px; }
  .public-info { text-align: center; }
  .contact-list { grid-template-columns: 1fr; }
}
</style>
