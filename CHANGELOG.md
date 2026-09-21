# Changelog

Все значимые изменения проекта MotoBind.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/),
версионирование — [Semantic Versioning](https://semver.org/lang/ru/).


## [1.11.0] — 2026-09-21

### Added
- **frontend/stores**: Pinia-сторы для всех доменов
  - `useUserStore` — профиль, настройки уведомлений, аватар (upload/delete)
  - `useMotorcyclesStore` — список мотоциклов, выбор, CRUD, пробег, заметка, фото
  - `useMaintenancesStore` — список ТО, фильтры, сортировка, counts
  - `useNotificationsStore` — список, unread count, polling, mark read
  - `useRemindersStore` — напоминания, dismiss, snooze
  - `useModalsStore` — глобальный реестр модалок (задел на Sprint 4)
- **frontend/stores/index.js**: единый экспорт всех сторов
- **frontend/utils/formatters.js**: общие форматтеры и лейблы
  - `formatMileage`, `formatCost`, `declensionMotorcycles`
  - `getStatusLabel`, `getStatusBadgeVariant`, `getCategoryLabel`
  - словари `STATUS_LABELS`, `STATUS_BADGE_VARIANT`, `CATEGORY_LABELS`
- **frontend/utils/mediaUrl.js**: единый резолвер URL для медиа
  - `getUploadUrl`, `getMotoPhotoUrl`, `getAvatarUrl`, `getManualImageUrl`
- **frontend/api/api.js**: in-memory HTTP-кеш для GET-запросов
  - opt-in через `{ cache: <TTL> }` в config запроса
  - автоматическая инвалидация кеша при `POST`, `PUT`, `PATCH`, `DELETE`
  - экспорт `clearApiCache()` для ручной инвалидации

### Changed
- **frontend/Garage.vue**: мигрирован на `useMotorcyclesStore` + `useRemindersStore`
  - `<script>`: ~340 строк → ~90 строк setup-функции
  - удалены локальные копии `formatMileage`, `formatCost`, `declensionMotorcycles`, `getStatusLabel`
  - `alert()` заменены на `toast.error()` / `toast.success()` через `useToast()`
  - ручная загрузка ТО (цикл `for … await api.get`) убрана
- **frontend/stores/motorcycles.js**: `loadAll` использует один запрос к `/motorcycle/`
  - бэкенд уже возвращает вложенные `maintenances` (selectinload закрыт в 1.1.0)
  - мутации (`update`, `updateMileage`, `updateNote`, `uploadPhoto`, `deletePhoto`) используют response напрямую — без повторного GET

### Fixed
- **backend/api/motorcycle.py**: `GET /motorcycle/<id>` теперь проверяет владельца
  - `MotorcycleService.get_motorcycle_by_id` принимает `user_id` и возвращает 404 для чужого мотоцикла
  - ранее любой авторизованный пользователь мог получить мотоцикл по id
- **frontend/api/api.js**: response-interceptor не падает, если `response.config` отсутствует
  - защита `if (config && config.method)` вокруг логики кеша
  - чинён упавший тест `passes successful response through`
- **pre-commit**: `flake8` теперь читает параметры из `args`, а не ищет `.flake8` относительно CWD
  - устранён конфликт `flake8` (дефолт 79) и `black`/`isort` (line-length 120)
  - версия flake8 в pre-commit поднята до 7.1.1 (синхронизация с CI)

### Performance
- **Garage**: загрузка страницы — 6 HTTP-запросов → 2
  - 1 × `GET /motorcycle/` (список с maintenances) + 1 × `GET /reminders/?status=pending`
  - при 5 мотоциклах бывший N+1 (1 + N) давал 6 запросов только на гараж
- **stores**: повторный `loadAll()` в пределах 30 секунд берётся из кеша (19 ms → 1 ms)
- **utils**: `formatMileage`/`formatCost`/`getStatusLabel` больше не дублируются в 5+ компонентах

### Notes
- JSON-контракт API не изменился (кроме багфикса в `GET /motorcycle/<id>` — теперь 404 для чужих)
- Визуал `/garage` идентичен до/после миграции — проверено по скриншотам
- Модалки в `Garage.vue` пока на локальных флагах (`showAddMotoModal` и т.п.);
  перевод на `useModalsStore` — Sprint 4
- Остальные views (`Maintenance`, `Manuals`, `Repair`, `Profile`, `Social`) — Sprint 4

## [1.10.0] — 2026-09-21

### Added
- **frontend/ui**: UI-kit — базовые компоненты
  - `BaseButton` (7 вариантов: primary, secondary, outline, ghost, danger, success, warning; размеры sm/md/lg; loading; icon; block)
  - `BaseInput`, `BaseTextarea` (label, error, hint, counter)
  - `BaseBadge` (6 вариантов + dot)
  - `BaseCard` (header/body/footer слоты, interactive, flat)
  - `BaseModal` (variant вместо bg-icon-color/icon-color, size sm/md/lg/xl, loading)
  - `BaseEmptyState` (icon, title, description, actions slot)
  - `ToastContainer` — глобальный контейнер уведомлений
- **frontend/composables**: `useToast` — toast-сервис (success/error/warning/info)
- **frontend/composables**: `useForm` — composable для форм (values, errors, validate, loading, submit, reset)
- **frontend**: алиас `@` → `src` в `vite.config.js`

### Changed
- **ChangePasswordModal**, **DeleteAccountModal**: мигрированы на UI-kit как примеры
  - ~150 строк CSS → ~20 в каждой
  - `alert()` → `toast.error()`
  - валидация → `useForm.validate`
- **reset.scss**: `overflow-x: hidden` убран с `html`/`body`
- **App.vue**: `overflow-x: hidden` убран из глобальных стилей
- **tokens.scss**: активированы токены spacing/typography/motion/z-index

### Fixed
- **position: fixed** на всех оверлеях (toast, модалки, sidebar, dropdown) — работал некорректно на длинных страницах
  - причина: `overflow-x: hidden` на `html`/`body` создавал containing block для `fixed`-потомков
- **tokens**: `--space-*`, `--text-*`, `--transition-*`, `--z-*` были закомментированы → `var()` резолвился в пустое значение

### Notes
- JSON-контракт API не изменился
- Остальные 25 модалок будут мигрированы на UI-kit в Sprint 4
- Формы: пока мигрированы 2 модалки, остальные — по мере рефакторинга views

## [1.9.0] — 2026-09-21

### Added
- **styles**: дизайн-токены для spacing (`--space-*`), typography (`--text-*`, `--fw-*`),
  motion (`--transition-*`) и z-index (`--z-*`)
- **styles**: палитра `--info` (заменяет хардкод `rgba(59, 130, 246, ...)` в info-блоках)

### Changed
- **styles**: `style.scss` разбит на модули
  - `styles/tokens.scss` — все CSS-переменные
  - `styles/reset.scss` — обнуление
  - `styles/base.scss` — типографика
  - `styles/components.scss` — переиспользуемые классы
  - `styles/utilities.scss` — задел на будущее
  - `styles/print.scss` — печать
  - `styles/index.scss` — точка входа

### Notes
- Визуальных изменений нет — только структурные
- JSON-контракт API не изменился
- Подготовка к UI-kit (Sprint 2)

## [1.8.0] — 2026-09-20

### Added
- **frontend/tests**: инфраструктура Vitest для фронтенда
  - `vitest`, `@vue/test-utils`, `jsdom`, `@vitest/coverage-v8`
  - `vitest.config.js` с jsdom environment и coverage
  - npm-скрипты: `test`, `test:watch`, `test:coverage`
- **frontend/tests**: 53 теста
  - `src/utils/DateFormatter.test.js` — 10 тестов
  - `src/constants/maintenanceTemplates.test.js` — 13 тестов
  - `src/api/api.test.js` — 11 тестов (интерцепторы, refresh, failedQueue)
  - `src/stores/auth.test.js` — 19 тестов (hydration, tokens, getters)

### Fixed
- **frontend/utils**: `formatDate(new Date('invalid'))` возвращал строку `"Invalid Date"` вместо `"—"`
  - причина: ветка `instanceof Date` пропускала проверку `isNaN`
  - найдено первым же тестом Vitest

### Changed
- **frontend**: `.gitignore` дополнен `coverage/`

### Notes
- Первый релиз с покрытием тестами фронтенда
- Итог по тестам:
  - **Backend**: 121 тест (auth, motorcycle, maintenance, statistic, social, manuals)
  - **Frontend**: 53 теста (utils, constants, api client, auth store)
  - **Всего**: 174 теста
- JSON-контракт API не изменён
- Backend domains: все 5 отрефакторены (Sprint 1 – 6)
- Frontend infrastructure: Pinia, split router, lazy apexcharts (Sprint 2B)
- Frontend tests: Vitest + 53 теста (Sprint 8)

## [1.7.1] — 2026-09-20

### Fixed
- **models**: устранены 2 `SAWarning` о конфликтующих SQLAlchemy relationships
  - `Motorcycle.motorcycle_owner` (создавался через `backref`) конфликтовал с `Motorcycle.owner`
  - `User.posts_authored` (создавался через `backref`) конфликтовал с `User.posts`
  - Заменено на `back_populates` — теперь одно каноничное relationship на каждую FK

### Removed
- **api/statistic**: удалены мёртвые эндпоинты Dashboard
  - `GET /api/statistic/dashboard-data`
  - `GET /api/statistic/dashboard-charts`
- **services/statistic_service**: удалены неиспользуемые методы
  - `get_dashboard_data`
  - `get_dashboard_charts`
  - `_calculate_change_percent` (использовался только в `get_dashboard_data`)

Dashboard-страница была удалена из продукта ранее. Эндпоинты не использовались
фронтендом и содержали баги (`maint.status.value` → `AttributeError` после
рефакторинга Sprint 0; смещение месяцев через `i*30` вместо календарных).

### Changed
- **schemas**: единый `model_config = ConfigDict(...)` вместо `class Config`
  (завершение миграции Pydantic v2; в `schemas/manual.py` сделано в 6.0,
  в остальных файлах — в этом релизе)
- **tests**: убраны все warnings (было 2, стало 0)

### Notes
- JSON-контракт API не изменился
- Технический релиз без функциональных изменений
- Готовы к следующему мажорному спринту (7.2 / 8)

## [1.7.0] — 2026-09-19

### Added
- **tests/test_manuals.py**: 23 теста домена manuals
  (create, list, get, update, delete, steps, admin permissions)
- **schemas/manual.py**: `ManualStepResponseSchema`, `ManualForMaintenanceResponseSchema`

### Changed
- **api/manuals.py**: тонкий контроллер — вся логика в `ManualService`
- **api/manuals.py**: Pydantic `Schema(**data)` → `model_validate(data)`
- **api/manuals.py**: убран `try/except Exception` (глобальный handler)
- **api/manuals.py**: ответы через `ManualResponseSchema` вместо `manual.to_dict()`
- **api/manuals.py**: `upload_step_image` / `delete_step_image` — тонкие контроллеры
- **services/manual_service.py**: `ManualService.list_manuals` — пагинация и фильтры в сервисе
- **services/manual_service.py**: `ManualService.get_manual_for_user` — единая проверка доступа
- **services/manual_service.py**: `ManualService.get_manual_for_maintenance_endpoint` — полный цикл
- **services/manual_service.py**: `ManualService.update_manual` — `is_admin` определяется внутри
- **services/manual_service.py**: `ManualService.update_step_image` / `delete_step_image`
- **services/manual_service.py**: `_update_steps` — обновляет существующие шаги по order, сохраняет `id` и `image`
- **schemas/manual.py**: `ManualResponseSchema` соответствует `Manual.to_dict()`

### Fixed
- **api/manuals.py**: `import json` был внутри `try` → `UnboundLocalError` (500 на пустом `data`)
- **api/manuals.py**: `is_admin` был хардкодом `current_user_id == 1` → админ с `id != 1` не видел moderate мануалы
- **services/manual_service.py**: `_update_steps` удалял и пересоздавал шаги → `PUT /api/manual/<id>` **затирал `step.image`** (картинки шагов терялись при редактировании мануала)
- **frontend/ManualCreator.vue**: `step.id` перезаписывался локальным счётчиком → upload/delete image шёл на неправильный `step_id` (404)
- **frontend/ManualCreator.vue**: `imagePreview` был undefined в `uploadStepImage` → `ReferenceError`, preview не устанавливался
- **frontend/ManualCreator.vue**: `this.addStep` без скобок в `mounted` → первый шаг не создавался при создании мануала
- **schemas/manual.py**: `class Config` → `model_config = ConfigDict(...)` (deprecated в Pydantic v2)

### Notes
- JSON-контракт API не изменён (проверено `Compare-Object`)
- Домен `manuals` считается отрефакторенным: сервис + схемы + тонкий API + тесты
- **Все 5 доменов backend отрефакторены** (motorcycle, maintenance, auth, social, manuals)
- Покрытие тестами: 121 тест (auth, motorcycle, maintenance, statistic, social, manuals)


## [1.6.0] — 2026-09-18

### Added
- **schemas/social.py**: response-схемы для домена social
  - `PostResponseSchema`, `PostListResponseSchema`, `CommentResponseSchema`
  - `LikeToggleResponseSchema`, `ReportResponseSchema`, `ReportCategorySchema`
- **tests/test_social.py**: ~20 тестов (posts, likes, comments, reports)

### Changed
- **api/social.py**: тонкий контроллер — без `try/except`, без прямых
  `PostLike.query`, без `int(get_jwt_identity())`
- **api/social.py**: сериализация через Pydantic-схемы вместо ручного `.to_dict()`
- **PostService.create_post**: возвращает `dict` с `is_liked=False` вместо `Post`
- **PostService.update_post**: возвращает `dict` с `is_liked` вместо `Post`
- **PostService.update_post**: логика `is_liked` уехала из API в сервис

### Fixed
- **api/social.py**: убран `except Exception` — глобальные handler'ы `APIException`
  и `PydanticValidationError` возвращают правильные коды (было 500 вместо 400
  при невалидном вводе)
- **report_service.create_report**: опечатка `craeted_at` → `created_at` в `post_snapshot`
- **report_service.create_report**: убран лишний `+ "Z"` (datetime уже aware,
  `.isoformat()` содержит `+00:00`)
- **report_service.get_reports**: убран дублирующийся ключ `current_page` в ответе
- **api/social.py**: убран двойной `url_prefix` в Blueprint (был в `api/social.py` **и** в `__init__.py`)

### Notes
- JSON-контракт API не изменился (проверено `Compare-Object` до/после)
- Домен `social` считается отрефакторенным: сервис + схемы + тонкий API + тесты
- В бэклоге: db.paginate вместо Query.paginate (SQLAlchemy 2.0)

## [1.5.0] — 2026-09-18
...

## [1.5.0] — 2026-09-18

### Added
- **services/auth_service.py**: `AuthService` — вся бизнес-логика аутентификации (register, login, refresh, logout, verify email, password reset) в одном сервисном слое
- **schemas/auth.py**: response-схемы для всех auth-эндпоинтов
  - `UserResponseSchema` — единая схема пользователя
  - `LoginResponseSchema`, `RegisterResponseSchema`, `RefreshResponseSchema`, `VerifyEmailResponseSchema`
  - `MessageResponseSchema`, `CheckVerificationResponseSchema`, `CheckResetTokenResponseSchema`

### Changed
- **api/auth.py**: тонкие контроллеры — нет `db.session` writes, нет `User.query`, нет прямых вызовов `create_access_token` / `create_refresh_token`
- **api/auth.py**: `Schema(**json)` → `Schema.model_validate(json or {})` (Pydantic 2 style)
- **AuthService**: единый `_issue_tokens` — access/refresh с `role` claim всегда

### Fixed
- **auth/verify_email**: токены теперь содержат `role` claim (раньше отсутствовал — ломало admin-режим на фронте до перелогина)
- **auth/verify_email**: применяется `VerifyEmailResponseSchema` (было без схемы)

### Notes
- JSON-контракт API не изменился (кроме баг-фикса в verify_email)
- Покрытие тестами auth: 19 тестов (Sprint 3.1)
- Домен `auth` считается отрефакторенным: сервис + схемы + тонкий API + тесты

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
