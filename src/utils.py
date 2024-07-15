import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()


def get_exchange_rates(to_currency, from_currency, amount):
    """Получает данных о курсах валют с использованием API"""

    api_key = os.getenv("API_KEY")  # Получаем API-ключ

    if not api_key:
        print("Ошибка: API-ключ не установлен.")
        return None

    api_url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={to_currency}&base={from_currency}"
    headers = {"apikey": api_key}

    try:
        response = requests.get(api_url, headers=headers)  # Отправляем get-запрос к API

        if response.status_code == 200: # Проверка статуса ответа
            return response.json()
        else:
            print(f"Ошибка при выполнении запроса: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None


def get_stock_prices(api_key, settings_file, date):
    """Получает цены на акции из json-файла на определенную дату"""

    if not os.path.exists(settings_file): # Проверка на существование файла
        print(f"Файл настроек {settings_file} не найден.")
        return {}

    with open(settings_file, "r") as f: # Загрузка из файла JSON
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
                    print(f"Ошибка запроса для {symbol}: {data.get('status', 'No data')}")
            else:
                print(f"Ошибка при выполнении запроса для {symbol}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса для {symbol}: {e}")

    return prices


if __name__ == "__main__":
    api_key = os.getenv("POLYGON_API_KEY")
    settings_file = "C:\\Users\\Dell\\PycharmProjects\\SkyBank_project_Ovsianik\\user_settings.json"
    date = "2023-07-10"  # Дата в формате YYYY-MM-DD

    if not api_key:
        print("Ошибка: API-ключ не установлен.")
    else:
        prices = get_stock_prices(api_key, settings_file, date)

    if prices:
        for symbol, price in prices.items():
            print(f"\"stock\": \"{symbol}\",\n  \"price\": {price}\n")
    else:
        print("Не удалось получить данные о ценах на акции на {date}")


# if __name__ == "__main__":
#     to_currency = "RUB"
#     from_currency = "USD"
#     amount = 25
#
#     result = get_exchange_rates(to_currency, from_currency, amount)
#
#     if result:
#         json_result = json.dumps(result, indent=4, ensure_ascii=False)
#         print(json_result)
#     else:
#         print("Не удалось получить данные о курсах валют.")
