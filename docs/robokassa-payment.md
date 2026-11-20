# Оплата дополнительного места в гараже

В MotoBind первое место для мотоцикла бесплатно. Каждая дополнительная покупка
добавляет одно место за 49 ₽ разово.

## Тестовая настройка магазина

В Robokassa укажите:

- **Result URL:** `https://motobind.ru/api/backend/payments/robokassa/result`
- **Метод Result URL:** `POST`
- **Success URL:** `https://motobind.ru/garage`
- **Fail URL:** `https://motobind.ru/garage?payment=fail`
- Алгоритм хеша должен совпадать с `ROBOKASSA_HASH_ALGORITHM`.

Callback идёт через серверный Nuxt proxy на Flask и специально не требует
пользовательской авторизации. Остальные пути API продолжают требовать JWT.

## Секреты окружения Flask

Заполнить на сервере, не в репозитории:

```dotenv
ROBOKASSA_MERCHANT_LOGIN=motobind
ROBOKASSA_HASH_ALGORITHM=MD5
ROBOKASSA_TEST_MODE=true
ROBOKASSA_TEST_PASSWORD_1=...
ROBOKASSA_TEST_PASSWORD_2=...
ROBOKASSA_PASSWORD_1=...
ROBOKASSA_PASSWORD_2=...
ROBOKASSA_PAYMENT_OBJECT=service
ROBOKASSA_PAYMENT_METHOD=full_payment
ROBOKASSA_TAX=none
```

В тестовом режиме используются только тестовые пароли и параметр `IsTest=1`.
Перевод `ROBOKASSA_TEST_MODE=false` разрешён только после активации магазина,
проверки тестового платежа и добавления боевых паролей в секреты сервера.

## Выдача места

Покупка создаёт локальный заказ в статусе `pending`. Место появляется только
после серверного `ResultURL` с корректной подписью, номером заказа и суммой.
Повторное уведомление Robokassa безопасно: уже оплаченный заказ не выдаёт
дополнительные места повторно. Возвраты и ручная отмена оплаченного места пока
не автоматизированы.

Новые аккаунты получают одно бесплатное место. При локальной и серверной
миграции отдельно добавьте в сгенерированный Alembic-файл data migration после
создания `users.extra_motorcycle_slots`, чтобы сохранить текущую вместимость:

```python
op.execute(sa.text(
    "UPDATE users SET extra_motorcycle_slots = "
    "(SELECT CASE WHEN COUNT(*) > 1 THEN COUNT(*) - 1 ELSE 0 END "
    "FROM motorcycles WHERE motorcycles.owner_id = users.id)"
))
```

В проекте `backend/migrations/` не хранится в Git: сгенерируйте ревизию отдельно
в локальной копии и на сервере, проверьте её, затем выполните `flask db upgrade`
в соответствующем окружении. Не копируйте ревизию между окружениями, если их
истории Alembic отличаются.
