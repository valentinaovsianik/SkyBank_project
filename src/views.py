import datetime
import json
import os

import pandas as pd
import logging
from dotenv import load_dotenv

load_dotenv()

log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(log_dir, exist_ok=True)

# Настраиваем логгер
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler(os.path.join(log_dir, "views.log"), mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def analyze_transactions(file_path):
    """Анализирует транзакции из excel-файла"""
    try:  # Проверяем существование файла
        if not os.path.exists(file_path):
            logger.error(f"Файл {file_path} не найден.")
            return None

        logger.info(f"Начинаем анализ транзакций изфайла {file_path}.")

        df = pd.read_excel(file_path)  # Читаем данные из файла

        last_digits = df.iloc[0]["Номер карты"][-4:]
        total_spent = df[df["Сумма операции"] < 0]["Сумма операции"].sum()
        cashback = abs(total_spent) / 100.0  # Вычисляем кэшбэк (1 рубль на каждые 100 рублей потраченных)

        result = {
            "last_digits": last_digits,
            "total_spent": float(total_spent),
            "cashback": round(cashback, 2),
        }

        logger.info("Анализ транзакций завершен успешно.")
        return json.dumps(result, ensure_ascii=False, indent=4)

    except Exception as e:
        logger.error(f"Ошибка при анализе транзакций: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


def get_top_transactions(file_path: str, date_str: str) -> str:
    """Возвращает топ-5 транзакций по сумме платежа в формате JSON от начала месяца до указанной даты"""
    try:
        end_date = datetime.strptime(date_str, "%Y-%m-%d")
        start_date = end_date.replace(day=1)  # Определяем начало месяца
        transactions_df = pd.read_excel(file_path)
        # Преобразуем столбец "Дата операции" в datetime
        transactions_df["Дата операции"] = pd.to_datetime(transactions_df["Дата операции"], format="%d.%m.%Y %H:%M:%S")

        # Фильтруем транзакции по диапазону дат
        filtered_df = transactions_df[
            (transactions_df["Дата операции"] >= start_date) & (transactions_df["Дата операции"] <= end_date)
        ]
        top_transactions = filtered_df.nlargest(5, "Сумма платежа")  # Выбираем топ-5 транзакций

        top_list = []
        for _, row in top_transactions.iterrows():
            transaction = {
                "date": row["Дата операции"].strftime("%d.%m.%Y"),
                "amount": row["Сумма платежа"],
                "category": row["Категория"],
                "description": row["Описание"],
            }
            top_list.append(transaction)

        # Преобразуем список словарей в JSON строку
        top_json = json.dumps(top_list, ensure_ascii=False, indent=4, default=str)
        logger.info(f"Запроc топ-5 транзакций с {start_date.strftime('%d.%m.%Y')} по {end_date.strftime('%d.%m.%Y')}")
        return top_json

    except Exception as e:
        logger.error(f"Ошибка при получении топ-5 транзакций: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=4)


def get_greeting():
    """Функция приветствия в завсисмости от времени суток"""
    current_time = datetime.datetime.now()
    hour = current_time.hour

    if 6 <= hour < 12:
        greeting = "Доброе утро"
    elif 12 <= hour < 18:
        greeting = "Добрый день"
    elif 18 <= hour < 24:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"
    logger.info(f"Получено приветствие: {greeting}")
    return greeting
