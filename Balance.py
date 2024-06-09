import pandas as pd
from openpyxl.styles import PatternFill
from openpyxl import load_workbook
from io import BytesIO
import requests

def main(input):
  try:
    file_content = input['markup_file']
    # Загрузка файла Excel
    message_bytes = base64.b64decode(file_content)
    toread = io.BytesIO(message_bytes)
    df = pd.read_excel(toread)
    # Замена NAN на 0
    df_bal = df_bal.fillna(0)
  except requests.exceptions.RequestException as e:
    print(f"Ошибка при загрузке файла: {e}")
  except FileNotFoundError as e:
    print(f"Ошибка при чтении файла: {e}")
  except pd.errors.ParserError as e:
    print(f"Ошибка при обработке данных: {e}")
  except Exception as e:
    print(f"Неизвестная ошибка: {e}")

  df_grouped = df_bal.groupby(['производитель/импортер', 'код'])['декалитры'].sum().reset_index()
  df_pivot = df_grouped.pivot(index='производитель/импортер', columns='код', values='декалитры').reset_index()
  
  # преобразуем все столбцы, кроме первого, в тип float и округляем до 2 знаков после запятой
  for col in df_pivot.columns[1:]:
    df_pivot[col] = df_pivot[col].astype(float).round(2)
  # добавляем столбец Итого
  _add_total_balances(df_pivot)
  # Сортировка записей по убыванию столбца "Итого"
  df_pivot = df_pivot.sort_values(by='Итого', ascending=False)
  # объединяем столбцы со значениями
  df_columns = df_pivot.columns.tolist()
  balance_items = df_pivot.values.tolist()
  balance_items.insert(0, df_columns)
  return {'balance_items': balance_items}

def _add_total_balances(df: pd.DataFrame):
  """
  Функция для добавления общего количества остатков по производителю и номеру товара

  :param df: Датафрейм с текущими данными без подсчётов Итого
  :return: None
  """
  df['Итого'] = df.iloc[:, 1:].sum(axis=1)
  total_series = pd.Series(df.iloc[:, 1:].sum(numeric_only=True), index=df.columns[1:])
  total_series['производитель/импортер'] = 'Итого'
  df.loc[len(df)] = total_series
