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


def get_stock_prices(api_key, symbols, date):
    """Получает цены на акции на определенную дату"""

    prices = {}

    for symbol in symbols:
        url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{date}/{date}"
        params = {"apiKey": api_key}

        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "OK" and data.get("resultsCount", 0) > 0:
                    prices[symbol] = data["results"][0]["c"]  # Цена закрытия
                else:
                    print(f"Ошибка запроса для {symbol}: {data.get('status', 'No data')}")
            else:
                print(f"Ошибка при выполнении запроса для {symbol}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса для {symbol}: {e}")

    return prices


if __name__ == "__main__":
    api_key = os.getenv("POLYGON_API_KEY")
    symbols = ["AAPL", "MSFT", "GOOGL"]  # Пример символов акций
    date = "2023-07-10"  # Дата в формате YYYY-MM-DD

    if not api_key:
        print("Ошибка: API-ключ не установлен.")
    else:
        prices = get_stock_prices(api_key, symbols, date)

    if prices:
        for symbol, price in prices.items():
            print(f"Цена закрытия для {symbol} на {date}: {price}")
    else:
        print(f"Не удалось получить данные о ценах на акции на {date}")





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
