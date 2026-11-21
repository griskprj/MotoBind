<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'admin'] })
useSeoMeta({ title: 'Платежи и места — Админка', robots: 'noindex' })

const api = useApi()
const toast = useToast()
const search = ref('')
const debouncedSearch = useDebounce(search, 400)
const status = ref('')
const page = ref(1)
const data = ref<any>(null)
const pending = ref(false)
const gift = reactive({ email: '', quantity: 1, reason: '' })
const giftPending = ref(false)
const refundingId = ref<number | null>(null)
const refundForm = reactive({ reason: '', reference: '' })

async function load() {
  pending.value = true
  try {
    data.value = await api.admin.getSlotPurchases({ page: page.value, per_page: 20, search: debouncedSearch.value || undefined, status: status.value || undefined })
  } catch {
    toast.error('Не удалось загрузить покупки мест')
  } finally {
    pending.value = false
  }
}

onMounted(load)
watch([debouncedSearch, status, page], load)

async function submitGift() {
  giftPending.value = true
  try {
    await api.admin.giftMotorcycleSlots({ ...gift })
    toast.success('Подарочное место выдано')
    gift.email = ''; gift.quantity = 1; gift.reason = ''
    await load()
  } catch {
    toast.error('Не удалось выдать место. Проверьте email и причину.')
  } finally { giftPending.value = false }
}

function startRefund(id: number) {
  refundingId.value = id
  refundForm.reason = ''
  refundForm.reference = ''
}

async function submitRefund(id: number) {
  if (!confirm(`Подтвердите: возврат по заказу #${id} уже выполнен в кабинете Robokassa?`)) return
  try {
    await api.admin.recordSlotRefund(id, { ...refundForm })
    toast.success('Возврат зафиксирован, купленное место отозвано')
    refundingId.value = null
    await load()
  } catch {
    toast.error('Не удалось зафиксировать возврат')
  }
}

const date = (value?: string | null) => value ? new Date(value).toLocaleString('ru-RU') : '—'
const statusLabel: Record<string, string> = { pending: 'Ожидает оплаты', paid: 'Оплачен', refunded: 'Возвращён' }
</script>

<template>
  <div class="slots-page">
    <header>
      <h1>Платежи и места в гараже</h1>
      <p>Просмотр оплат, выдача подарочных мест и фиксация уже оформленных возвратов.</p>
    </header>

    <BaseCard padding="lg">
      <h2>Подарить место</h2>
      <p class="hint">Причина и email администратора сохраняются в журнале действий.</p>
      <form class="gift-form" @submit.prevent="submitGift">
        <label>Email пользователя<input v-model.trim="gift.email" type="email" required maxlength="128" /></label>
        <label>Количество<input v-model.number="gift.quantity" type="number" min="1" max="20" required /></label>
        <label class="reason">Причина<input v-model.trim="gift.reason" required maxlength="500" placeholder="Например, компенсация по обращению #…" /></label>
        <BaseButton type="submit" :disabled="giftPending">{{ giftPending ? 'Выдаём…' : 'Выдать место' }}</BaseButton>
      </form>
    </BaseCard>

    <section class="filters">
      <input v-model="search" placeholder="Поиск по email, имени или номеру заказа" />
      <select v-model="status"><option value="">Все статусы</option><option value="pending">Ожидает оплаты</option><option value="paid">Оплачен</option><option value="refunded">Возвращён</option></select>
    </section>

    <BaseCard padding="none" class="table-card">
      <div v-if="pending" class="empty">Загрузка…</div>
      <div v-else-if="!data?.purchases?.length" class="empty">Покупок пока нет.</div>
      <div v-else class="table-wrap">
        <table>
          <thead><tr><th>Заказ</th><th>Пользователь</th><th>Сумма</th><th>Статус</th><th>Создан</th><th>Оплачен / возвращён</th><th>Действие</th></tr></thead>
          <tbody>
            <template v-for="purchase in data.purchases" :key="purchase.id">
              <tr>
                <td>#{{ purchase.id }}</td><td>{{ purchase.username || 'Удалённый пользователь' }}<br /><small>{{ purchase.email || '—' }}</small></td>
                <td>{{ purchase.amount }} ₽</td><td>{{ statusLabel[purchase.status] || purchase.status }}</td>
                <td>{{ date(purchase.created_at) }}</td><td>{{ date(purchase.refunded_at || purchase.paid_at) }}<small v-if="purchase.refund_reason"><br />{{ purchase.refund_reason }}<span v-if="purchase.refund_reference"> · {{ purchase.refund_reference }}</span></small></td>
                <td><BaseButton v-if="purchase.status === 'paid'" variant="danger" size="sm" @click="startRefund(purchase.id)">Зафиксировать возврат</BaseButton><span v-else>—</span></td>
              </tr>
              <tr v-if="refundingId === purchase.id" class="refund-row"><td colspan="7">
                <p><strong>Сначала оформите возврат в Robokassa.</strong> Здесь действие только отзывает место в MotoBind и записывает операцию.</p>
                <div class="refund-form"><label>Причина<input v-model.trim="refundForm.reason" required maxlength="500" /></label><label>Номер операции Robokassa (необязательно)<input v-model.trim="refundForm.reference" maxlength="128" /></label><BaseButton variant="danger" :disabled="!refundForm.reason" @click="submitRefund(purchase.id)">Подтвердить фиксацию</BaseButton><BaseButton variant="secondary" @click="refundingId = null">Отмена</BaseButton></div>
              </td></tr>
            </template>
          </tbody>
        </table>
      </div>
    </BaseCard>

    <div v-if="data?.pages > 1" class="pagination"><BaseButton variant="secondary" :disabled="page <= 1" @click="page--">Назад</BaseButton><span>Страница {{ data.current_page }} из {{ data.pages }}</span><BaseButton variant="secondary" :disabled="page >= data.pages" @click="page++">Дальше</BaseButton></div>

    <BaseCard padding="lg">
      <h2>Последние подарочные места</h2>
      <div v-if="!data?.adjustments?.length" class="empty">Выдач пока нет.</div>
      <ul v-else class="audit-list"><li v-for="item in data.adjustments" :key="item.id"><strong>{{ item.user_email }}</strong> — +{{ item.quantity }}; {{ item.reason }}<small>{{ item.admin_email }} · {{ date(item.created_at) }}</small></li></ul>
    </BaseCard>
  </div>
</template>

<style scoped lang="scss">
.slots-page { display: flex; flex-direction: column; gap: var(--space-5); }
h1 { font-size: var(--text-2xl); font-weight: var(--fw-bold); }
h2 { font-size: var(--text-lg); font-weight: var(--fw-semibold); margin-bottom: var(--space-2); }
header p, .hint, small { color: var(--color-text-secondary); }
.gift-form, .refund-form { display: flex; align-items: end; flex-wrap: wrap; gap: var(--space-3); }
label { display: flex; flex-direction: column; gap: var(--space-1); font-size: var(--text-sm); flex: 1; min-width: 180px; }
input, select { padding: 10px 12px; border: 1px solid var(--color-border); border-radius: var(--radius-md); background: var(--color-surface); color: var(--color-text); }
.reason { flex: 2; }
.filters { display: flex; gap: var(--space-3); }
.filters input { flex: 1; }
.table-card { overflow: hidden; }
.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: var(--text-sm); }
th, td { padding: 12px; text-align: left; border-bottom: 1px solid var(--color-border); vertical-align: top; }
th { color: var(--color-text-secondary); white-space: nowrap; }
.empty { padding: var(--space-5); color: var(--color-text-secondary); }
.refund-row td { background: var(--color-surface-secondary); }
.refund-row p { margin-bottom: var(--space-3); }
.pagination { display: flex; align-items: center; justify-content: center; gap: var(--space-4); }
.audit-list { list-style: none; padding: 0; display: grid; gap: var(--space-3); }
.audit-list li { padding-bottom: var(--space-3); border-bottom: 1px solid var(--color-border); }
.audit-list small { display: block; margin-top: 4px; }
@media (max-width: 640px) { .filters { flex-direction: column; } }
</style>
