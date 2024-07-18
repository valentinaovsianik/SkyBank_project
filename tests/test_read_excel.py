import pytest
import pandas as pd
from datetime import datetime

from src.read_excel import read_excel_file

@pytest.fixture
def mock_excel_data(mocker):
    """Фиксстура для создания мок данных из таблицы excel"""
    data = {
        "Дата операции": [
            datetime(2021, 12, 31, 16, 44, 0),
            datetime(2021, 12, 31, 16, 42, 4),
            datetime(2021, 12, 31, 16, 39, 4),
            datetime(2021, 12, 31, 15, 44, 39),
            datetime(2021, 12, 31, 1, 23, 42),
        ],
        "Дата платежа": [
            datetime(2021, 12, 31),
            datetime(2021, 12, 31),
            datetime(2021, 12, 31),
            datetime(2021, 12, 31),
            datetime(2021, 12, 31)
        ],
        "Номер карты": [
            "*7197",
            "*7197",
            "*7197",
            "*7197",
            "*5091"
        ],
        "Статус": [
            "OK", "OK", "OK", "OK", "OK"
        ],
        "Сумма операции": [
            -160.89, -64.00, -118.12, -78.05, -564.00
        ],
        "Валюта операции": [
            "RUB", "RUB", "RUB", "RUB", "RUB"
        ],
        "Сумма платежа": [
            -160.89, -64.00, -118.12, -78.05, -564.00
        ],
        "Валюта платежа": [
            "RUB", "RUB", "RUB", "RUB", "RUB"
        ],
        "Кэшбэк": [
            None, None, None, None, None
        ],
        "Категория": [
            "Супермаркеты", "Супермаркеты", "Супермаркеты", "Переводы", "Каршеринг"
        ]
    }


    df = pd.DataFrame(data)  # Создаем DataFrame из мок данных

    mocker.patch("pandas.read_excel", return_value=df) # Создаем мок объект для pd.read_excel

    return df.to_dict(orient="records")

def test_read_excel_file_with_mock(mock_excel_data):
    result = read_excel_file("mocked_file.xlsx")
    assert result == mock_excel_data


