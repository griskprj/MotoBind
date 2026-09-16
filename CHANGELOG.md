# Changelog

Все значимые изменения проекта MotoBind.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/),
версионирование — [Semantic Versioning](https://semver.org/lang/ru/).

## [1.2.0] — 2026-09-16

### Added
- **schemas/common.py**: общий `ISO8601Mixin` для сохранения формата datetime между схемами

### Fixed
- **maintenance**: `mark_planned_as_done` не синхронизировал сброс `mileage_update` напоминаний при отметке ТО как выполненного
- **maintenance/stats**: `calculate_maintenance_freq` и `calculate_maintenance_money` падали с `AttributeError` из-за несуществующего `m.date` (подготовка к premium-фиче)
- **db**: 6 мест с `Query.options().get()` в `statistic_service.py` (пропущены в PR #3)

### Changed
- **maintenance/api**: `quick_start` вынесен в `MaintenanceService.quick_start`
- **maintenance/api**: `Schema(**json)` → `model_validate(json or {})`
- **maintenance/api**: убран `try/except ValidationError` — покрыто глобальным Pydantic-хендлером
- **maintenance/api**: локальная переменная `maintenance` переименована в `record` (не затеняет blueprint)
- **maintenance/service**: `MaintenanceStatus` enum перенесён в модель (single source of truth)
- **maintenance/service**: `_recompute_status` вынесен из `update_maintenance`
- **maintenance/schemas**: добавлены `QuickStartSchema`, `MaintenanceResponseSchema`
- **maintenance/model**: `to_dict` помечен deprecated (путь к удалению в будущих спринтах)
- **motorcycle/service**: публичный `MotorcycleService.set_mileage(moto, new)` инкапсулирует побочные эффекты (mileage_updated_at, сброс напоминаний)
- **motorcycle/service**: `update_motorcycle`, `update_motorcycle_mileage` и `mark_planned_as_done` используют `set_mileage`

### Removed
- **maintenance/utils**: удалены мёртвые `maintenance_nodes.py`, `calculate_node_health.py`, `check_maintenance_status.py` (использовали несуществующие relationship)
- **maintenance/model**: убраны неиспользуемые параметры `include_planned_maintenance`, `include_maintenance_nodes` из `Motorcycle.to_dict`

### Performance
- **maintenance/stats**: общий helper `aggregate_by_month` вместо копипасты в freq/money
- **maintenance/stats**: правильный обход 12 месяцев (было `- timedelta(days=i*30)`, плыло)
- **maintenance/stats**: `max()` защищён от пустого списка

### Notes
- JSON-контракт API не изменился (проверено diff'ом до/после 2A.3 и 2A.4)
- В `api/maintenance.py` больше нет прямых обращений к `db`, `Maintenance.query`, `NotificationService`
- Sprint 2A завершает рефакторинг домена `maintenance`

## [1.1.0] — 2026-09-15

### Fixed
- **motorcycle**: гос номер (`licensePlate`) молча игнорировался при обновлении мотоцикла из-за рассинхрона camelCase/snake_case между схемой и моделью
- **motorcycle**: `update_note` не проверял владельца мотоцикла внутри сервиса (полагался только на декоратор)
- **utils/helpers**: `check_motorcycle_owner` и `DEFAULT_NODES` — мёртвый код удалён

### Changed
- **motorcycle/api**: `Schema(**request.get_json())` → `Schema.model_validate(request.get_json() or {})`
- **motorcycle/api**: убраны разбросанные `to_dict(include_*)` вызовы, сериализация вынесена в `_serialize_short` / `_serialize_detail` хелперы
- **motorcycle/service**: добавлен whitelist `ALLOWED_UPDATE_FIELDS` — защита от случайного перезаписывания `owner_id` и других чувствительных полей
- **motorcycle/service**: выделен приватный `_on_mileage_change` — убрано дублирование между `update_motorcycle` и `update_motorcycle_mileage`
- **schemas/motorcycle**: валидаторы `color`, `license_plate`, `vin` вынесены в `MotorcycleValidatorsMixin`
- **schemas/motorcycle**: поле `licensePlate` → `license_plate` с `alias="licensePlate"` (фронт по-прежнему шлёт camelCase)
- **schemas/motorcycle**: добавлены response-схемы `MotorcycleShortSchema`, `MotorcycleDetailSchema`, `MaintenanceShortSchema` + `ISO8601Mixin` для сохранения формата datetime
- **motorcycle/model**: `to_dict()` помечен deprecated (путь к удалению в будущих спринтах)

### Performance
- **motorcycle/service**: `get_user_motorcycles` использует `selectinload(Motorcycle.maintenances)` — закрыт N+1 при загрузке гаража

### Deprecated
- **SQLAlchemy**: `Model.query.get(id)` → `db.session.get(Model, id)` — 50 мест в 12 файлах (`api/*`, `services/*`, `utils/*`)
- `Query.get()` помечен deprecated в SQLAlchemy 1.4, удалён в 2.1
- `Motorcycle.to_dict(include_*)` — использовать `MotorcycleShortSchema` / `MotorcycleDetailSchema` из `app.schemas.motorcycle`

### Notes
- JSON-контракт API не изменился (проверено diff'ом ответов до/после PR #2)
- SQLite (dev) и PostgreSQL (prod) работают одинаково, миграции не требуются

## [1.0.0] — 2026-09-14

### Fixed
- **models**: унифицирован формат datetime (UTC-aware вместо наивных `datetime.utcnow()`)
- **models**: `MaintenanceStatus` теперь сохраняется как `.value` (строка), а не enum-объект
- **models**: `User.to_dict(include_stats=True)` — исправлена опечатка `' posts'` и N+1
- **decorators**: `owner_required` — исправлена проверка `if not obj` (падал с `AttributeError` вместо 404)
- **deps**: конфликты peer-зависимостей frontend (`vite`, `@vitejs/plugin-vue`, `apexcharts`, `vue3-apexcharts`)

### Changed
- **deps**: `apexcharts` 3 → 7, `vue3-apexcharts` 1.6 → 1.11, `vite` → 8.3.0, `vue` → 3.5.42, `@vitejs/plugin-vue` → 6.0.8
- **deps**: `vue-router` зафиксирован на `^4.4.0` (v5 требует Pinia + Vue 3.5.34+, отложено до Sprint 2)
- **deps**: удалены неиспользуемые `chart.js` и `vue-chartjs` (~400 КБ экономии бандла)

### Security
- **decorators**: `owner_required` теперь корректно возвращает 404 для несуществующих объектов и 403 для чужих