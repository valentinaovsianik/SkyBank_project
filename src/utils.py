import json
import os

import logging
import requests
from dotenv import load_dotenv

load_dotenv()

log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")

os.makedirs(log_dir, exist_ok=True)


# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создание обработчика для записи в файл
file_handler = logging.FileHandler(os.path.join(log_dir, "utils.log"), encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Форматтер сообщений
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Добавление обработчика к логгеру
logger.addHandler(file_handler)


def get_exchange_rates(to_currency: str, from_currency: str, amount: float) -> dict:
    """Получает данных о курсах валют с использованием API"""

    api_key = os.getenv("API_KEY")  # Получаем API-ключ

    if not api_key:
        logger.error("Ошибка: API-ключ не установлен.")
        return None

    api_url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={to_currency}&base={from_currency}"
    headers = {"apikey": api_key}

    try:
        response = requests.get(api_url, headers=headers)  # Отправляем get-запрос к API

        if response.status_code == 200:  # Проверка статуса ответа
            return response.json()
        else:
            logger.error(f"Ошибка при выполнении запроса: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка запроса: {e}")
        return None


def get_stock_prices(api_key: str, settings_file: str, date: str) -> dict:
    """Получает цены на акции на определенную дату"""

    if not os.path.exists(settings_file):  # Проверка на существование файла
        logger.error(f"Файл настроек {settings_file} не найден.")
        return {}

    with open(settings_file, "r") as f:  # Загрузка из файла JSON
        settings = json.load(f)
    user_stocks = settings.get("user_stocks", [])

    prices = {}

    for symbol in user_stocks:
        url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{date}/{date}"
        params = {"apiKey": api_key}

        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "OK" and data.get("resultsCount", 0) > 0:
                    price = data["results"][0]["c"]  # Цена закрытия
                    prices[symbol] = price

                else:
                    logger.error(f"Ошибка запроса для {symbol}: {data.get('status', 'No data')}")
            else:
                logger.error(f"Ошибка при выполнении запроса для {symbol}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка запроса для {symbol}: {e}")

    return prices
