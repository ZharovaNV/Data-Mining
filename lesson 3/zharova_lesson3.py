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


import requests
import bs4
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
)
from sqlalchemy.orm import relationship
from zharova_models import Base, Post, Writer, Comment

HEADERS = {
    'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
}
URL = 'https://habr.com/ru/top/weekly/'
BASE_URL = 'https://habr.com/'


def get_next_page(soap: bs4.BeautifulSoup) -> str:
    a = soap.find('a', attrs={'id': 'next_page'})
    return f"{BASE_URL}{a['href']}" if a else None


def get_post_url(soap):
    post_a = soap.select('h2.post__title a')
    return set(itm['href'] for itm in post_a)


def get_page(url):
    while url:
        print(url)
        response = requests.get(url, headers=HEADERS)
        soap = bs4.BeautifulSoup(response.text, 'lxml')
        yield soap
        url = get_next_page(soap)


def get_post_data(post_url):
    '''
    - Загаловок статьи
    - Url статьи
    - количество комментариев в статье
    - дата и время публикации
    - автор (название и url)
    - авторы комментариев (название и url)
    '''
    template_data = {'title': '',
                     'url': post_url,
                     'comment_cnt': 0,
                     'post_time': '',
                     'writer': {'name': '',
                                'url': ''},
                     'comment_author': []}
    response = requests.get(post_url, headers=HEADERS)
    soap = bs4.BeautifulSoup(response.text, 'lxml')
    template_data['title'] = soap.select_one('span.post__title-text').text
    template_data['comment_cnt'] = soap.select_one('span.comments-section__head-counter').text.replace('\n','').strip()
    template_data['post_time'] = soap.select_one('span.post__time').text

    template_data['writer']['name'] = soap.select_one('header.post__meta a span.user-info__nickname').text
    template_data['writer']['url'] = soap.select_one('div.user-info__links a')['href']

    template_data['comment_author'] = [{'name': itm['data-user-login'], 'url': itm['href']} for itm in soap.select('div.comment__head a.user-info')]


    return template_data





if __name__ == '__main__':
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.orm.session import Session

    engine = create_engine('sqlite:///habr.db')
    Base.metadata.create_all(engine)
    session_db = sessionmaker(bind=engine)

    session = session_db()

    data = get_page(URL)

    for soap in get_page(URL):
        posts = get_post_url(soap)
        for url in posts:
            data = get_post_data(url)

            writer = session.query(Writer).filter(Writer.name == data['writer']['name']).first()
            if not writer:
                writer = Writer(data['writer']['name'], data['writer']['url'])
                session.add(writer)
                try:
                    session.commit()
                except Exception as e:
                    session.rollback()

            post = Post(data['title'], data['url'], data['comment_cnt'], writer.id)
            session.add(post)
            try:
                session.commit()
            except Exception as e:
                session.rollback()

            for comment_author in data['comment_author']:
                writer = session.query(Writer).filter(Writer.name == comment_author['name']).first()
                if not writer:
                    writer = Writer(comment_author['name'], comment_author['url'])
                    session.add(writer)
                    try:
                        session.commit()
                    except Exception as e:
                        session.rollback()

                comment = Comment(post.id, writer.id)
                session.add(comment)
                try:
                    session.commit()
                except Exception as e:
                    session.rollback()

    session.close()

