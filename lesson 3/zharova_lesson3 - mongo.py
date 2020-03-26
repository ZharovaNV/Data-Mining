'''
Источник https://habr.com/ru/

задача:
Обойти ленту популярного за неделю

сохранить данные в базы данных (Mongo, SQL)
необходимые данные:
- Загаловок статьи
- Url статьи
- количество комментариев в статье
- дата и время публикации
- автор (название и url)
- авторы комментариев (название и url)

для Mongo:
создать коллекцию и все можно хранить в одной коллекции

для SQL
создать дополнительную таблицу для автора и автора комментариев и наладить связи
'''


from pymongo import MongoClient
from zharova_lesson3 import HEADERS, URL, BASE_URL, get_next_page, get_post_url, get_page, get_post_data


if __name__ == '__main__':
    client = MongoClient('mongodb://localhost:27017/')
    db = client['habr_mongo']

    data = get_page(URL)

    for soap in get_page(URL):
        posts = get_post_url(soap)
        for url in posts:
            data = get_post_data(url)

            db['posts'].insert_one(data)



