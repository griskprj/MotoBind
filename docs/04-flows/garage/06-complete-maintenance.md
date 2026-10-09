
# Выполнение ТО

**Контекст:** Garage
**Триггер:** «Отметить выполненным» на плановом ТО
**Результат:** Maintenance completed, пробег обновлён, повтор создан (опционально)

## Шаги
1. User нажимает «Выполнено».
2. Форма: completed_mileage (обязательно), completed_date (по умолчанию сегодня), cost (опционально).
3. Чекбокс «Повторить через N км / M дней».
4. Backend:
   - ставит status=completed, completed_mileage, completed_date, cost,
   - обновляет Motorcycle.mileage, если completed_mileage > текущего,
   - если repeat — создаёт новый Maintenance (planned) с интервалом.
5. Cancel всех Reminder, связанных с этим Maintenance.
6. Frontend показывает тост «ТО выполнено».

## Что может пойти не так
- completed_mileage < текущего пробега мотоцикла → 422.
- Забыл ввести пробег → required.
- Повтор без интервала → 422 «Укажите интервал».

## Эндпоинты
- `POST /api/v2/maintenances/{id}/complete` → `{ maintenance, new_planned }`

## Решения
- completed_mileage обязателен.
- cost опционален, по умолчанию 0.
- Повтор: интервал в км ИЛИ в днях, не оба сразу.
- При обновлении пробега — side-effects как в 03 (сброс mileage reminders).
- Запись в историю — сразу, без отдельного шага.
