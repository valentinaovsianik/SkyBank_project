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


if __name__ == "__main__":
    to_currency = "RUB"
    from_currency = "USD"
    amount = 25

    result = get_exchange_rates(to_currency, from_currency, amount)

    if result:
        json_result = json.dumps(result, indent=4, ensure_ascii=False)
        print(json_result)
    else:
        print("Не удалось получить данные о курсах валют.")
