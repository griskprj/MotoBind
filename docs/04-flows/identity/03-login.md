
# Логин

**Контекст:** Identity
**Триггер:** отправка формы входа
**Результат:** cookies установлены, редирект на /garage

## Шаги
1. User вводит email, пароль, опционально «запомнить меня».
2. Backend ищет User, проверяет status, is_verified, пароль.
3. Backend выдаёт access (15 мин) + refresh (30 дней или сессионный).
4. Backend ставит cookies: mb_access, mb_refresh, mb_csrf.
5. Frontend редиректит на /garage.

## Что может пойти не так
- Email/пароль неверный → 401 «Неверный email или пароль» (не раскрываем, что именно).
- Email не подтверждён → 403 «Подтвердите email».
- User забанен → 403.
- 5 попыток за 15 мин → 429.

## Эндпоинты
- `POST /api/v2/auth/login` → `{ user }` + Set-Cookie ×3

## Решения
- Токены только в httpOnly cookies, не в localStorage.
- CSRF-токен в mb_csrf (не httpOnly), JS его читает и шлёт в заголовке.
- «Запомнить меня» → refresh-cookie сессионная (умрёт при закрытии браузера).
