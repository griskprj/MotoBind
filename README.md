<div align="center">
<img src="frontend/public/MotoBindLogo.png" alt="MotoBind Logo" width="120" height="120">
  <h1>MotoBind</h1>
  <p><strong>Умное управление обслуживанием мотоциклов</strong></p>
  <p>
    <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python">
    <img src="https://img.shields.io/badge/Flask-2.3.2-green.svg" alt="Flask">
    <img src="https://img.shields.io/badge/Vue-3.3.4-brightgreen.svg" alt="Vue">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  </p>
</div>

Веб-приложение для учёта **мотоциклов, планирования и отслеживания обслуживания, анализа затрат и состояния узлов.**

## 📋 Функциональность
* Мотоциклы – создание, редактирование, удаление, загрузка фото.
* Обслуживание – добавление выполненных работ с указанием стоимости, даты, пробега, категории узла.
* Плановое обслуживание – создание напоминаний по пробегу, автоматический расчёт статуса (overdue, soon, ok, no_mileage).
* Узлы обслуживания – предустановленные узлы (двигатель, подвеска, электроника и др.) с привязкой к плановым ТO.
* Статистика и графики:
    * Дашборд с общим состоянием всех мотоциклов.
    * Детальный анализ выбранного мотоцикла: затраты, частота ТO, здоровье узлов.
    * Графики затрат и количества обслуживаний по месяцам (ApexCharts).
    * Модальные окна – быстрые действия: обновить пробег, добавить обслуживание, запланировать ТO.
    * Авторизация – JWT, роли пользователей.


## 🛠 Технологии

### Backend
* Python 3.10+
* Flask – микрофреймворк
* Flask-SQLAlchemy + SQLite (возможна замена на PostgreSQL)
* Flask-Migrate – миграции БД
* Flask-JWT-Extended – аутентификация
* Swagger/OpenAPI – документация (через apispec)

### Frontend
* Vue 3 (Composition API)
* ApexCharts – графики
* Axios – HTTP-запросы
* Font Awesome – иконки
* CSS-переменные – для темизации