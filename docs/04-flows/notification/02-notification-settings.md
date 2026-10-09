
# Настройки уведомлений

**Контекст:** Notification
**Триггер:** User открывает /settings/notifications
**Результат:** настройки сохранены, применяются к новым уведомлениям

## Шаги
1. User открывает настройки.
2. Видит список флагов:
   - email_notifications_enabled (глобальный)
   - email_newsletter_enabled (рассылки)
   - email_verification_enabled (письма верификации)
   - reminders_mileage_enabled (напоминания о пробеге)
   - reminders_maintenance_enabled (напоминания о ТО)
3. Меняет, нажимает «Сохранить».
4. Backend обновляет NotificationPreference.

## Что может пойти не так
- User отключил email_notifications_enabled → все email-уведомления молчат, in-app работает.
- User отключил reminders_mileage_enabled → cron не создаёт mileage-напоминания для него.
- Пропала сеть → изменения не сохранены, форма показывает ошибку.

## Эндпоинты
- `GET /api/v2/user/notification-settings` → `{ settings }`
- `PUT /api/v2/user/notification-settings` → `{ settings }`

## Решения
- Флаги — на уровне User, не на уровне типа Notification.
- Глобальный email_notifications_enabled перекрывает всё остальное.
- reminders_* — отдельные флаги, потому что это разные триггеры (пробег / ТО).
- Настройки применяются к новым уведомлениям. Уже созданные не трогаем.
- Дефолт: всё включено, кроме newsletter (её User включает сам при регистрации, если захочет).
