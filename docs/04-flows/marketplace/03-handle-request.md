
# Обработка заявки

**Контекст:** Marketplace
**Триггер:** мастер открывает список заявок
**Результат:** заявка принята / отклонена / завершена

## Шаги
1. Мастер открывает /master/requests.
2. Видит список новых и активных заявок.
3. **Принять** → status=accepted, клиент получает Notification.
4. **Начать работу** → status=in_progress.
5. **Завершить** → status=completed, клиент получает Notification.
   Опционально: мастер создаёт запись в истории ТО клиента (Maintenance), но только с согласия клиента.
6. **Отклонить** → status=declined, причина обязательна.

## Что может пойти не так
- Заявка уже обработана → 409.
- Мастер завершает заявку без completed — нельзя, сначала in_progress.
- Мастер пытается создать Maintenance в чужом гараже без согласия → 403.

## Эндпоинты
- `POST /api/v2/service-requests/{id}/accept` → `{ request }`
- `POST /api/v2/service-requests/{id}/decline` → `{ request }` — body: `{ reason }`
- `POST /api/v2/service-requests/{id}/start` → `{ request }`
- `POST /api/v2/service-requests/{id}/complete` → `{ request }`

## Решения
- Переходы статусов — строго по цепочке. Нельзя прыгнуть с new на completed.
- Причина decline обязательна, min 10 символов.
- Мастер не может создавать Maintenance в чужом гараже в v2. Это P1.
- Уведомления клиенту на каждом переходе.
