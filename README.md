# 🏦 My Finance App

Приложение для анализа личных финансов с интеграцией с банковскими выписками и финансовыми API.

## 🚀 Возможности

- 📊 Загрузка и анализ банковских выписок в формате Excel
- 📈 Анализ расходов по категориям
- 💰 Расчет кэшбэка и бонусов
- 🌐 Получение актуальных курсов валют
- 📉 Мониторинг цен акций
- 📅 Фильтрация операций по дате
- 🏠 Главная страница с общей статистикой
- 📊 Детальная страница событий

## 🛠 Технологии

- **FastAPI** - веб-фреймворк
- **Pandas** - обработка Excel файлов
- **Pydantic** - валидация данных
- **Poetry** - управление зависимостями
- **Pytest** - тестирование
- **Mypy** - статическая типизация

## 📁 Структура проекта
my_finance_app/
├── src/
│ ├── main.py # Точка входа FastAPI
│ ├── config.py # Настройки приложения
│ ├── models/
│ │ └── operation.py # Модель финансовой операции
│ ├── services/
│ │ ├── excel_processor.py # Обработка Excel файлов
│ │ ├── analyzer.py # Анализ финансовых данных
│ │ └── finance_api.py # Внешние API (валюты, акции)
│ └── views/
│ ├── home.py # Логика главной страницы
│ └── events.py # Логика страницы событий
├── tests/
│ ├── test_models.py # Тесты моделей
│ ├── test_views.py # Тесты представлений
│ └── test_services/
│ ├── test_finance_api.py # Тесты API
│ ├── test_analyzer.py # Тесты анализатора
│ └── test_excel_processor.py # Тесты обработки Excel
├── data/
│ └── operations.xlsx # Пример банковской выписки
├── .env # Переменные окружения
├── .flake8 # Конфигурация Flake8
├── pyproject.toml # Зависимости Poetry
├── user_settings.json # Пользовательские настройки
└── README.md # Документация

## ⚡ Быстрый старт

### 1. Установка зависимостей

```bash
poetry install
```
### 2. Настройка окружения
#### Создайте файл .env:
```env
EXCEL_FILE_PATH=data/operations.xlsx
SUPPORTED_CURRENCIES=USD,EUR,GBP,CNY
SUPPORTED_STOCKS=AAPL,GOOGL,MSFT,TSLA,AMZN
```
### 3. Запуск приложения
```bash
poetry run python src/main.py
```
## 📊 API Endpoints
### Главная страница
```text
GET /
```
Параметры:
 - date - дата в формате YYYY-MM-DD HH:MM:SS (опционально)

### Страница событий
```text
GET /events/{date_str}?period=[W|M|Y|ALL]
```
Параметры:
 - date_str - дата в формате YYYY-MM-DD HH:MM:SS
 - period - период (W - неделя, M - месяц, Y - год, ALL - все время)

## 📋 Формат Excel файла
 - Файл должен содержать следующие колонки:

 - Дата операции - дата и время операции

 - Дата платежа - дата проведения платежа

 - Номер карты - маскированный номер карты

 - Статус - статус операции

 - Сумма операции - сумма с знаком (- для расходов)

 - Валюта операции - валюта операции

 - Кэшбэк - начисленный кэшбэк

 - Категория - категория операции

 - MCC - код мерчанта

 - Описание - описание операции

 - Бонусы - начисленные бонусы

 - Округление - округление на инвесткопилку

## 🧪 Тестирование
### Запуск всех тестов
```bash
poetry run pytest
```
### Запуск с покрытием
```bash
poetry run pytest --cov=src --cov-report=html
```
### Проверка типов
```bash
poetry run mypy src/
```
### Линтинг
```bash
poetry run flake8 src/
poetry run black --check src/
poetry run isort --check src/
```
## ⚙️ Настройка
### Пользовательские настройки
#### Создайте user_settings.json:

```json
{
  "user_currencies": ["USD", "EUR"],
  "user_stocks": ["AAPL", "GOOGL"]
}
```
## 🔮 Примеры использования
### Анализ расходов за месяц
```python
from src.services.excel_processor import load_operations_from_excel
from src.services.analyzer import analyze_spending

operations = load_operations_from_excel("data/operations.xlsx")
analysis = analyze_spending(operations)

print(f"Общие расходы: {analysis['total_spent']}")
print("По категориям:", analysis['by_category'])
Получение курсов валют
```
```python
from src.services.finance_api import get_currency_rates

rates = get_currency_rates()
print("Курс USD:", rates["USD"])
print("Курс EUR:", rates["EUR"])
```
## 🐛 Troubleshooting
### common issues:
1. Файл не найден - убедитесь что файл operations.xlsx exists в папке data/

2. Ошибки формата - проверьте структуру Excel файла

3. Проблемы с API - при ошибках сети используются fallback значения

### Логирование
#### Для debug добавьте логирование в нужных модулях:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```
## 📄 Лицензия
MIT License

## 🤝 Contributing
 - Форкните репозиторий

 - Создайте feature branch

 - Commit your changes

 - Push to the branch

 - Create a Pull Request

