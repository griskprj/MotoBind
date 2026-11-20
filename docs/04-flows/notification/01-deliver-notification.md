
# Доставка уведомления

**Контекст:** Notification
**Триггер:** другое действие (лайк, ТО выполнено, мануал одобрен, ...)
**Результат:** Notification создан, User видит бейдж/колокольчик

## Шаги
1. Сервис (PostService, MaintenanceService, ...) вызывает NotificationService.send().
2. Backend создаёт Notification (type, title, content, link).
3. In-app: колокольчик показывает unread_count.
4. Email (опционально): если User.email_notifications_enabled=true и тип разрешён.
5. User открывает колокольчик → список, клик по уведомлению → переход по link.
6. Прочитанные → is_read=true, unread_count--.

## Что может пойти не так
- Email не ушёл → Notification всё равно создан, in-app работает.
- Link ведёт на удалённый контент → 404, но Notification не ломается.
- User отключил все email → in-app всё равно приходит.

## Эндпоинты
- `GET /api/v2/notifications?page=1` → `{ notifications, pagination }`
- `GET /api/v2/notifications/unread-count` → `{ count }`
- `PUT /api/v2/notifications/{id}/read` → `204`
- `PUT /api/v2/notifications/read-all` → `204`
- `DELETE /api/v2/notifications/{id}` → `204`

## Решения
- Notification создаётся только сервисом, не пользователем.
- Типы: reminder | social | moderation | manual_status | system.
- Прочитанные хранятся 30 дней, потом cron удаляет.
- Polling unread-count раз в 30 секунд на клиенте. WebSocket — P1.
- Уведомления о своих действиях не создаём (сам себя лайкнул — не уведомляем).
