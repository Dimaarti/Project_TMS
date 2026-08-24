China Calc

Веб-приложение на Django для расчёта поставок из Китая в Россию и Беларусь.
Приложение хранит товары клиентов, ручные курсы валют, логистику, дополнительные
расходы, комиссию байера, оплаты клиентов и историю расчётов.

Возможности

Три маршрута: Китай → Россия, Китай → Беларусь и Китай → Россия → Беларусь;
стоимость товаров по внутреннему и клиентскому курсу;
логистика и общие расходы по весу или объёму;
прямые расходы, привязанные к конкретному товару;
индивидуальная комиссия каждого клиента;
история расчётов с одним актуальным результатом на поставку;
оплаты, долг и переплата клиента;
Excel-отчёт по клиенту.

Правила конвертации

Стоимость товара конвертируется напрямую:
CNY → RUB для маршрута Китай → Россия;
CNY → BYN для маршрутов с итоговым расчётом в BYN.

Логистика и расходы следуют маршруту:
Китай → Россия: исходная валюта → RUB;
Китай → Беларусь: исходная валюта → BYN;
Китай → Россия → Беларусь: исходная валюта → RUB → BYN.

Для стоимости товара клиента используется клиентский курс. Для себестоимости,
логистики и расходов используется внутренний курс.

Структура

src/
├── china_calc/
│   ├── account/      # пользователь и авторизация
│   ├── client/       # клиенты
│   ├── finance/      # курсы, калькуляторы, результаты и оплаты
│   ├── reports/      # Excel-отчёт
│   └── shipment/     # поставки, товары и расходы
├── config/           # настройки Django и общие перечисления
└── manage.py
templates/            # HTML-шаблоны

Отдельной модели маршрута нет: маршрут выбирается в Shipment.route_type.
Итоговая валюта определяется этим маршрутом автоматически.

Запуск

Требования: Python 3.14, Poetry и PostgreSQL.

poetry install
cp env.example .env
poetry run python src/manage.py migrate
poetry run python src/manage.py createsuperuser
poetry run python src/manage.py runserver

Основные переменные окружения:

SECRET_KEY=change-me
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
LANGUAGE_CODE=ru
TIME_ZONE=Europe/Minsk

PG_HOST=localhost
PG_USER=postgres
PG_PASS=postgres
PG_NAME=china_calc
PG_PORT=5432

Вместо параметров PostgreSQL можно указать DATABASE_URL. Например, SQLite
удобен для локальной проверки:

DATABASE_URL=sqlite:///db.sqlite3

Тесты и проверки

Тесты написаны на unittest и Django TestCase.

poetry run python src/manage.py test china_calc
poetry run python src/manage.py check
poetry run python src/manage.py makemigrations --check --dry-run
poetry run ruff check src
poetry run ruff format --check src

Явная метка china_calc в команде тестов нужна, потому что manage.py находится
в src, а команда обычно запускается из корня проекта.

Docker

docker compose up --build

Приложение будет доступно по адресу http://127.0.0.1:8000/.

Остановка:

docker compose down

Удаление контейнеров вместе с данными PostgreSQL:

docker compose down -v