
# Напоминания

**Контекст:** Garage
**Триггер:** cron раз в сутки, или действие пользователя (snooze/dismiss)
**Результат:** Reminder создан, отправлен, обработан

## Шаги

### Генерация (cron)
1. Раз в сутки cron обходит всех active User.
2. Для каждого мотоцикла:
   - пробег не обновлялся > 30 дней → создать Reminder `mileage_update`,
   - planned ТО с planned_mileage - mileage ≤ 500 км → `maintenance_soon`,
   - planned ТО с planned_mileage ≤ mileage → `maintenance_overdue`.
3. Существующие pending Reminder с изменившимися условиями — удаляются.

### Отправка
4. Backend отправляет Notification (in-app) + email (если разрешено в настройках).
5. Reminder помечается `last_sent_at`, `next_send_at`.

### Действия пользователя
6. Snooze → `snoozed_until = now + N дней`, статус остаётся pending.
7. Dismiss → статус dismissed, больше не отправляется.

## Что может пойти не так
- Пробег обновлён → mileage_update reminders cancel.
- ТО выполнено → связанные reminders cancel.
- Пользователь отключил email → шлём только in-app.
- Cron упал → следующий запуск наверстает.

## Эндпоинты
- `GET /api/v2/reminders?status=pending` → `{ reminders }`
- `GET /api/v2/reminders/count` → `{ count }`
- `PUT /api/v2/reminders/{id}/snooze` → `{ reminder }`
- `PUT /api/v2/reminders/{id}/dismiss` → `{ reminder }`

## Решения
- Типы: `mileage_update`, `maintenance_soon`, `maintenance_overdue`.
- Повторы: mileage — каждые 14 дней, overdue — каждые 7 дней. Soon — однократно.
- Порог «скоро» — 500 км. Не настраивается в v2.
- Порог «пробег устарел» — 30 дней. Не настраивается в v2.
- Удалённые (dismissed) Reminder живут 30 дней, потом cron их чистит.
