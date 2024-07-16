import pytest
import json
import datetime
import pandas as pd
from src.views import analyze_transactions, get_top_transactions, get_greeting


@pytest.fixture
def sample_excel_data(tmp_path):
    """Генерирует временный Excel-файл с тестовыми данными и возвращает его путь"""
    df = pd.DataFrame({
        "Номер карты": ["1234567812345678", "2345678923456789"],
        "Сумма операции": [-1000, -500, 200],
        "Бонусы (включая кэшбэк)": [10, 5, 0]
    })
    file_path = tmp_path / "test.xlsx"
    df.to_excel(file_path, index=False)
    return file_path

@pytest.fixture
def sample_excel_data_top(tmp_path):
    """Генерирует тестовйы Excel-файл с тестовыми данными для get_top_transactions и возвращает его путь"""
    df = pd.DataFrame({
        "Дата операции": ["2023-01-01", "2023-01-02", "2023-01-03"],
        "Сумма платежа": [100.0, 200.0, 300.0],
        "Категория": ["Кафе", "Автосервис", "Шопинг"],
        "Описание": ["Еда", "Мойка", "Магазин"]
    })
    file_path = tmp_path / "test_top.xlsx"
    df.to_excel(file_path, index=False)
    return file_path


@pytest.mark.parametrize("file_exists, expected_result", [
    (True, {"last_digits": "5678", "total_spent": -1500.0, "cashback": 15.0}),
    (False, {"error": "Файл nonexistent.xlsx не найден."})
])
def test_analyze_transactions(sample_excel_data, file_exists, expected_result):
    file_path = sample_excel_data if file_exists else "nonexistent.xlsx"
    result = analyze_transactions(file_path)
    assert json.loads(result) == expected_result


@pytest.mark.parametrize("file_exists, date_str, expected_result", [
    (True, "2023-01-03", [
        {"date": "03.01.2023", "amount": 300.0, "category": "Шопинг", "description": "Магазин"},
        {"date": "02.01.2023", "amount": 200.0, "category": "Автосервис", "description": "Мойка"},
        {"date": "01.01.2023", "amount": 100.0, "category": "Кафе", "description": "Еда"}
    ]),
    (False, "2023-01-03", {"error": "Файл nonexistent.xlsx не найден."})
])
def test_get_top_transactions(sample_excel_data_top, file_exists, date_str, expected_result):
    file_path = sample_excel_data_top if file_exists else "nonexistent.xlsx"
    result = get_top_transactions(file_path, date_str)
    assert json.loads(result) == expected_result


@pytest.mark.parametrize("current_hour, expected_greeting", [
    (8, "Доброе утро"),
    (14, "Добрый день"),
    (20, "Добрый вечер"),
    (2, "Доброй ночи")
])
def test_get_greeting(current_hour, expected_greeting):
    fake_now = datetime(datetime.now().year, datetime.now().month, datetime.now().day, current_hour)
    with pytest.raises(AssertionError):
        assert get_greeting() == expected_greeting
