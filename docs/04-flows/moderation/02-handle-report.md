
# Обработка жалобы

**Контекст:** Moderation
**Триггер:** модератор открывает очередь жалоб
**Результат:** жалоба resolved или rejected, действия применены

## Шаги
1. Модератор открывает /admin/reports?status=pending.
2. Видит список: категория, snapshot, автор, репортер.
3. Открывает жалобу, изучает контекст.
4. Выбирает действие:
   - **post_deleted** — удалить пост/комментарий/мануал,
   - **user_banned** — забанить автора,
   - **both** — и то, и другое,
   - **none** — жалоба необоснована, отклонить.
5. Опционально — заметка.
6. Backend применяет действие, помечает Report resolved.
7. Автор контента получает Notification (type=moderation).
8. Репортер получает Notification (type=report_status).

## Что может пойти не так
- Модератор банит сам себя → 422.
- Жалоба уже обработана → 409.
- Автор уже забанен → бан no-op, жалоба всё равно resolved.
- Контент уже удалён → удаление no-op.

## Эндпоинты
- `GET /api/v2/admin/reports?status=pending` → `{ reports, stats }`
- `GET /api/v2/admin/reports/{id}` → `{ report }`
- `POST /api/v2/admin/reports/{id}/resolve` → `{ report }` — body: `{ action, note }`
- `DELETE /api/v2/admin/reports/{id}` → `204` — удалить жалобу совсем (спам-жалобы)

## Решения
- Действия: post_deleted | user_banned | both | none.
- Все действия пишутся в ModerationAction (append-only).
- Бан — это `User.status = banned`. Разбан — отдельный эндпоинт.
- Модератор не может банить админа и себя.
- Уведомления: автору — о блокировке или удалении, репортеру — о решении.
- Snapshot не удаляем, даже если контент удалён — нужно для аудита.

## Дополнительно: бан / разбан

- `POST /api/v2/admin/users/{id}/ban` → `{ user }`
- `POST /api/v2/admin/users/{id}/unban` → `{ user }`
- Бан → User.status=banned, все Session revoked, User не может залогиниться.
- Разбан → User.status=active, но логиниться надо заново.
