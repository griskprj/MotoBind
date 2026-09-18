# Changelog

Все значимые изменения проекта MotoBind.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/),
версионирование — [Semantic Versioning](https://semver.org/lang/ru/).


## [1.4.0] — 2026-09-18

### Added
- **backend/tests**: инфраструктура pytest (`conftest.py`, `pyproject.toml`)
  - fixtures: `app`, `db_session`, `client`, `make_user`, `auth_headers`
  - `TestingConfig` + `create_app(config_override=...)` для изоляции тестов
  - in-memory SQLite с `StaticPool` (shared connection pool)
  - auto-mock email sending
- **backend/tests**: 68 новых тестов (auth, motorcycle, maintenance, statistic)
  - `test_auth.py` — 19 тестов (register/login/refresh/logout/password reset)
  - `test_motorcycle.py` — 19 тестов (CRUD, permissions, validation)
  - `test_maintenance.py` — 17 тестов (CRUD, complete flow, quick-start)
  - `test_statistic.py` — 13 тестов (garage/maintenance/repair/registrations)

### Fixed
- **schemas/manual**: 3 × Pydantic `class Config` deprecated → мигрирован на `ConfigDict` *(если делал в рамках этого релиза; иначе пропусти этот пункт)*
- **api/exceptions**: `handle_pydantic_validation_error` падал с `TypeError` при кастомных `@field_validator` (ValueError в ctx) → теперь sanitize errors перед jsonify
- **maintenance/model**: `description` был `nullable=False`, но схема и сервис передают `None` → 500 на создании ТО без описания
- **maintenance/service**: опечатка `record.statust` в `_recompute_status` → `record.status`
- **statistic/service**: сравнение `maintenance.status` (строка) с `MaintenanceStatus` (enum) → все счётчики всегда 0
- **statistic/service**: сравнение `completed_date` (`date`) с `month_start` (`datetime`) в `get_moto_garage_stats` → 500 для любого мото с выполненным ТО
- **decorators**: `Motorcycle.query.get()` (legacy) → `db.session.get()` (пропущено в Sprint 1)
- **migrations**: новая миграция для `maintenances.description` nullable (для PostgreSQL prod)

### Changed
- **api/exceptions**: `datetime.utcnow()` → `datetime.now(timezone.utc)` (Sprint 0 хвост)
- **tests/conftest**: `pytest_configure` регистрирует кастомные маркеры (`@pytest.mark.auth`, etc.)
- **tests**: SECRET_KEY/JWT_SECRET_KEY в тестах ≥32 символа (убирает PyJWT warning)

### Notes
- JSON-контракт API не менялся (кроме исправленных ошибок 500→400 и правильных счётчиков статистики)
- Тесты нашли 3 скрытых прод-бага (500 на невалидных данных, 500 на ТО без description, 500 на статистике с completed ТО)
- Покрытие: ~74 теста (было 4 нерабочих)

## [1.3.0] — 2026-09-17

### Added
- **frontend/stores**: `useAuthStore` (Pinia, setup store) — единый источник правды для auth state
- **frontend/router/routes**: разделение роутера на модули (`auth.js`, `documents.js`, `admin.js`, `main.js`)
- **frontend/router/guards.js**: выделены navigation guards из `router/index.js`

### Changed
- **frontend/main.js**: подключена Pinia (`app.use(createPinia())`)
- **frontend/api/api.js**: чтение токена напрямую из localStorage (без циклического импорта `stores/auth`), синхронизация store после refresh / logout через lazy import
- **frontend/router/index.js**: использует `useAuthStore()` вместо ручного декода JWT, файл сокращён с ~370 до ~30 строк
- **frontend/components/Sidebar.vue**: `computed isAdmin` из store вместо ручного декода JWT на каждой навигации
- **frontend/views/auth/** (Login, Register, Verify, Reset): используют `useAuthStore()` для setTokens / setUser
- **frontend/views/Profile.vue**, **ManualRules.vue**, **ManualsPanel.vue**, **ManualCreator.vue**: `useAuthStore().logout()` вместо `removeTokens` helper

### Removed
- **frontend/api/auth.js**: удалён (его role выполняет `stores/auth.js`)
- **frontend/views/Dashboard.vue**: удалён (не подключён в роутере)

### Performance
- **frontend/main.js**: убрана глобальная регистрация `VueApexCharts`, компоненты чартов регистрируют его локально
- **главный бандл**: 1.1 МБ → **191 КБ** (apexcharts вынесен в lazy-чанк)
- **AdminPanel чанк**: ~950 КБ, грузится только на `/admin/*` страницах
- **apexcharts чанк** (508 КБ): грузится только на страницах с графиками

### Fixed
- **backend/statistic_service**: `selectinload(User.motorcycle)` → `selectinload(User.motorcycles)` — исправлен 500 на `GET /api/statistic/repair` (колонка вместо relationship)

### Deprecated (в бэклоге, не удалено)
- `vue-router@5` upgrade отложен: требует `@pinia/colada` как peer
- Warning `INEFFECTIVE_DYNAMIC_IMPORT` для `stores/auth` в `api.js` — не критично

### Notes
- JSON-контракт API не изменялся
- Все изменения frontend — внутренние (архитектура), пользователь не заметит кроме ускорения загрузки

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