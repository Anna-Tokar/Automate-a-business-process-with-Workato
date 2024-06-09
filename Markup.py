import pandas as pd
import base64
from io import BytesIO
import requests
    
def main(input):
  file_content = input['markup_file']
  # Загрузка файла Excel
  message_bytes = base64.b64decode(file_content)
  toread = io.BytesIO(message_bytes)
  df = pd.read_excel(toread)
  try:
    # Чтение файла Excel с использованием pandas
    # Замена NAN на 0
    df = df.fillna(0)
  except requests.exceptions.RequestException as e:
    print(f"Ошибка при загрузке файла: {e}")
  except FileNotFoundError as e:
    print(f"Ошибка при чтении файла: {e}")
  except pd.errors.ParserError as e:
    print(f"Ошибка при обработке данных: {e}")
  except Exception as e:
    print(f"Неизвестная ошибка: {e}")
  # Вычисляем наценку и процент
  _get_markup_prev_month(df)
  main_list = df.values.tolist()
  # Сортировка main_list по убыванию столбца 'markup'
  main_list.sort(key=lambda x: x[-1], reverse=True)
  print(main_list)
  return {'markup_items':main_list}

def _get_markup_prev_month(df: pd.DataFrame):
  """
  Функция для получения отношения наценки относительно предыдущей недели

  :param df: Датафрейм с текущими данными без подсчётов отношения ценки
  :return: None
  """
  last_markup = df.iloc[:, -1]  # Последний столбец
  prelast_markup = df.iloc[:, -2]  # Предпоследний столбец
  # Вычесть значения последнего столбца из предпоследнего
  markup = last_markup - prelast_markup
  # Добавить результат в DataFrame
  df['markup'] = markup
  df['markup'] = df['markup'].round(2)
  # Преобразование типа данных столбца 'data' в float
  df['markup'] = df['markup'].astype(float)
  # Округление значений в столбце 'data' до двух знаков после запятой
  df['markup_prec'] = (last_markup / prelast_markup - 1) * 100
  df['markup_prec'] = df['markup_prec'].round(2)
  # Преобразование типа данных столбца 'data' в float
  df['markup_prec'] = df['markup_prec'].astype(float)
