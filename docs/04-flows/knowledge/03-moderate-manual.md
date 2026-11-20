
# Модерация мануала

**Контекст:** Knowledge + Moderation
**Триггер:** модератор открывает очередь мануалов
**Результат:** мануал approved или rejected с причиной

## Шаги
1. Модератор открывает /admin/manuals?status=moderate.
2. Видит список, открывает мануал.
3. Проверяет: полнота, корректность, безопасность, отсутствие рекламы.
4. Approve → status=approved, публикация.
5. Reject → ввод причины, status=rejected, причина сохраняется.
6. Автор получает Notification (type=manual_status) с решением.

## Что может пойти не так
- Модератор approve'ит свой мануал → запрещено (автор ≠ модератор).
- Мануал уже обработан другим модератором → 409 «Уже обработан».
- Повторная модерация approved → только админ, статус archived → moderate.

## Эндпоинты
- `GET /api/v2/admin/manuals?status=moderate` → `{ manuals }`
- `POST /api/v2/admin/manuals/{id}/approve` → `{ manual }`
- `POST /api/v2/admin/manuals/{id}/reject` → `{ manual }` — body: `{ reason }`

## Решения
- Модератор не может approve'ить свой мануал. Проверка на бэке.
- Причина reject обязательна, min 10 символов.
- История модерации — в ModerationAction (append-only).
- Approve идемпотентен: повторный approve → 409.
