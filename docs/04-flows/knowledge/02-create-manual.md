
# Создание мануала

**Контекст:** Knowledge
**Триггер:** «Создать мануал» в /manuals
**Результат:** мануал создан в статусе moderate, ушёл на модерацию

## Шаги
1. User нажимает «Создать мануал».
2. Заполняет:
   - title, description, category, motorcycle (модель),
   - difficult (easy/medium/hard), time_estimate, interval,
   - instruments, parts, warnings, safety_tip,
   - шаги (order, title, text, tip, warning, image).
3. Может сохранить как черновик (status=draft) или отправить на модерацию (moderate).
4. Backend валидирует, создаёт Manual + ManualStep.
5. Изображения шагов — отдельными запросами после создания.
6. Уведомление модераторам (Notification type=system).

## Что может пойти не так
- Нет ни одного шага → 422 «Добавьте хотя бы один шаг».
- order с пропусками → нормализуем (1, 2, 3, ...).
- Изображение > 5 МБ → 413.
- Двойная отправка → блокировка кнопки на клиенте.

## Эндпоинты
- `POST /api/v2/manuals` → `{ manual }`
- `POST /api/v2/manuals/{id}/steps/{step_id}/image` → `{ image_url }`
- `DELETE /api/v2/manuals/{id}/steps/{step_id}/image` → `204`

## Решения
- Статусы: draft → moderate → approved | rejected → archived.
- После rejected автор может править и снова отправить на модерацию.
- Approved мануал автор править не может — только через админа. Иначе модерация бессмысленна.
- Изображения: webp, max 1920px по ширине, сжатие на бэке.
- Один мануал = одна конкретная работа на одной модели. Не «всё про масло», а «замена масла на Yamaha YZF-R6».
