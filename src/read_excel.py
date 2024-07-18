import pandas as pd


def read_excel_file(file_name: str):
    """Считывает данные из excel-файла и преобразовывает их в формат JSON"""
    try:
        read_file = pd.read_excel(file_name)
        file_to_dict = read_file.to_dict(orient="records")
        return file_to_dict
    except Exception as e:
        return f"Ошибка {e}, повторите попытку."