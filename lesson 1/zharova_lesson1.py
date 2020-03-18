"""
Задача:
Источник данных https://5ka.ru/special_offers/

Необходимо создать структуру JSON файлов где имя файла название категории,
а содержимое файла JSON список словарей товаров пренадлежащих этой категории.
Извлекаем только товары по акции, не перегружайте сервер делайте time.sleep

В Гите хранить файлы результата не нужно, только код который приводит к
созданию соответсвующих файлов
"""

import os
import time
import json
import requests

MAIN_URL = 'https://5ka.ru/api/v2/special_offers/'
HEADERS = {
    'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
}
CAT_URL = 'https://5ka.ru/api/v2/categories/'


def x5ka_cat(url, file_dir):
    """
    Функция создающая файлы по категориям
    """
    response = requests.get(url, headers=HEADERS)
    response_data = response.json()
    for categories in response_data:
        group_name = categories['parent_group_name'].replace('*', '').replace('"', '')
        url_params = {'records_per_page': 20,
                      'categories': categories['parent_group_code']}

        file_name = '_'.join(group_name.split())
        file_data = x5ka(MAIN_URL, url_params)
        with open(os.path.join(file_dir, f'{file_name}.json'), 'w') as file:
            file.write(json.dumps(file_data))


def x5ka(url, params):
    """
    Заполнения файла по одной категории
    """
    result = []
    while url:
        response = requests.get(url, headers=HEADERS, params=params) \
            if params else requests.get(url, headers=HEADERS)
        params = None
        data = response.json()
        result.extend(data.get('results'))
        url = data.get('next')
        time.sleep(1)
    return result


if __name__ == '__main__':

    FILE_DIR = os.path.join(os.getcwd(), 'products')
    if not os.path.exists(FILE_DIR):  # Если пути не существует создаем его
        os.makedirs(FILE_DIR)

    x5ka_cat(CAT_URL, FILE_DIR)
